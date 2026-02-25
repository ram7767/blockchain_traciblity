"""
AgricultureApp Views — Clean, modular view functions.
Organized by: Public, Auth, Admin, Farmer, Consumer sections.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from datetime import date
import os
import logging

from .models import UserProfile, Product, TransportLog, Purchase
from .decorators import login_required_custom, admin_required, farmer_required, consumer_required
from .services.blockchain_service import blockchain
from .services.qr_service import generate_product_qr, get_ngrok_url

logger = logging.getLogger(__name__)


# ============================================================
# Helper Functions
# ============================================================

def get_current_user(request):
    """Get the current logged-in UserProfile from session."""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return UserProfile.objects.get(pk=user_id, is_active=True)
        except UserProfile.DoesNotExist:
            pass
    return None


def get_base_context(request):
    """Build base context dict with user info for all templates."""
    user = get_current_user(request)
    return {
        'current_user': user,
        'user_type': request.session.get('user_type', ''),
        'blockchain_status': blockchain.is_available,
    }


# ============================================================
# PUBLIC VIEWS — No login required
# ============================================================

def index(request):
    """Homepage — show all available products as guest browsing."""
    ctx = get_base_context(request)
    ctx['products'] = Product.objects.filter(is_available=True, quantity__gt=0)
    ctx['total_farmers'] = UserProfile.objects.filter(user_type='Farmer', is_active=True).count()
    ctx['total_products'] = Product.objects.filter(is_available=True).count()
    ctx['total_consumers'] = UserProfile.objects.filter(user_type='Consumer', is_active=True).count()
    return render(request, 'index.html', ctx)


def product_detail(request, product_id):
    """Public product detail page — shows farmer info, transport chain, QR."""
    product = get_object_or_404(Product, pk=product_id)
    transport_logs = product.transport_logs.all()

    ctx = get_base_context(request)
    ctx['product'] = product
    ctx['transport_logs'] = transport_logs
    ctx['farmer'] = product.farmer

    # Build shareable URL
    ngrok_url = get_ngrok_url()
    base = ngrok_url if ngrok_url else request.build_absolute_uri('/')[:-1]
    ctx['share_url'] = f"{base}/product/{product.pk}/"

    return render(request, 'product_detail.html', ctx)


# ============================================================
# AUTH VIEWS
# ============================================================

def login_view(request):
    """Unified login page with role selector."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user_type = request.POST.get('user_type', '').strip()

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'login.html', get_base_context(request))

        # Admin special case
        if user_type == 'Admin':
            if username == 'admin' and password == 'admin':
                request.session['user_id'] = 0
                request.session['username'] = 'admin'
                request.session['user_type'] = 'Admin'
                messages.success(request, 'Welcome, Admin!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials.')
                return render(request, 'login.html', get_base_context(request))

        # Farmer / Consumer login
        try:
            user = UserProfile.objects.get(
                username=username, password=password,
                user_type=user_type, is_active=True
            )
            request.session['user_id'] = user.pk
            request.session['username'] = user.username
            request.session['user_type'] = user.user_type
            messages.success(request, f'Welcome, {user.username}!')

            if user.user_type == 'Farmer':
                return redirect('farmer_dashboard')
            else:
                return redirect('consumer_dashboard')

        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid credentials. Please check your username, password, and role.')

    ctx = get_base_context(request)
    return render(request, 'login.html', ctx)


def register_view(request):
    """Registration page for new farmers and consumers."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        contact = request.POST.get('contact', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        user_type = request.POST.get('user_type', 'Farmer')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'register.html', get_base_context(request))

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
            return render(request, 'register.html', get_base_context(request))

        # Create user in DB
        user = UserProfile.objects.create(
            username=username, password=password,
            contact=contact, email=email, address=address,
            user_type=user_type
        )

        # Save to blockchain
        data = f"signup#{username}#{password}#{contact}#{email}#{address}#{user_type}\n"
        receipt = blockchain.save_user(data)
        if receipt:
            user.blockchain_hash = str(receipt.get('transactionHash', ''))
            user.save()

        messages.success(request, 'Registration successful! You can now login.')
        return redirect('login')

    ctx = get_base_context(request)
    return render(request, 'register.html', ctx)


def logout_view(request):
    """Logout and clear session."""
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('index')


# ============================================================
# ADMIN VIEWS
# ============================================================

@admin_required
def admin_dashboard(request):
    """Admin dashboard with stats and user management."""
    ctx = get_base_context(request)
    ctx['farmers'] = UserProfile.objects.filter(user_type='Farmer')
    ctx['consumers'] = UserProfile.objects.filter(user_type='Consumer')
    ctx['products'] = Product.objects.all()
    ctx['purchases'] = Purchase.objects.all()
    ctx['total_sales'] = sum(p.total_amount for p in Purchase.objects.all())
    return render(request, 'admin/dashboard.html', ctx)


@admin_required
def admin_add_user(request):
    """Admin: Add a new farmer or consumer."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        contact = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        user_type = request.POST.get('user_type', 'Farmer')

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists.')
        elif not username or not password:
            messages.error(request, 'Username and password are required.')
        else:
            UserProfile.objects.create(
                username=username, password=password,
                email=email, contact=contact,
                address=address, user_type=user_type
            )
            messages.success(request, f'{user_type} "{username}" added successfully.')

        return redirect('admin_dashboard')

    ctx = get_base_context(request)
    return render(request, 'admin/add_user.html', ctx)


@admin_required
def admin_toggle_user(request, user_id):
    """Admin: Activate/deactivate a user."""
    try:
        user = UserProfile.objects.get(pk=user_id)
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User "{user.username}" has been {status}.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('admin_dashboard')


@admin_required
def admin_delete_user(request, user_id):
    """Admin: Delete a user permanently."""
    try:
        user = UserProfile.objects.get(pk=user_id)
        name = user.username
        user.delete()
        messages.success(request, f'User "{name}" has been deleted.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('admin_dashboard')


@admin_required
def admin_view_sales(request):
    """Admin: View all purchase/sales records."""
    ctx = get_base_context(request)
    ctx['purchases'] = Purchase.objects.select_related('consumer', 'product', 'farmer').all()
    return render(request, 'admin/view_sales.html', ctx)


# ============================================================
# FARMER VIEWS
# ============================================================

@farmer_required
def farmer_dashboard(request):
    """Farmer dashboard — my products and sales overview."""
    user = get_current_user(request)
    ctx = get_base_context(request)
    ctx['products'] = Product.objects.filter(farmer=user)
    ctx['sales'] = Purchase.objects.filter(farmer=user)
    ctx['total_sales'] = sum(s.total_amount for s in ctx['sales'])
    return render(request, 'farmer/dashboard.html', ctx)


@farmer_required
def farmer_add_product(request):
    """Farmer: Add a new product with transport details."""
    user = get_current_user(request)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0')
        quantity = request.POST.get('quantity', '0')
        category = request.POST.get('category', 'Other')
        origin_location = request.POST.get('origin_location', '').strip()
        harvest_date = request.POST.get('harvest_date', '')

        # Check duplicate
        if Product.objects.filter(farmer=user, name=name).exists():
            messages.error(request, f'Product "{name}" already exists.')
            return redirect('farmer_add_product')

        # Handle image upload
        image_path = ''
        if 'image' in request.FILES:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'products'))
            os.makedirs(fs.location, exist_ok=True)
            filename = fs.save(request.FILES['image'].name, request.FILES['image'])
            image_path = f'products/{filename}'

        # Create product
        product = Product.objects.create(
            farmer=user, name=name, description=description,
            price=float(price), quantity=float(quantity),
            category=category, image=image_path,
            origin_location=origin_location,
            harvest_date=harvest_date if harvest_date else None,
        )

        # Generate QR code
        ngrok_url = get_ngrok_url()
        base = ngrok_url if ngrok_url else 'http://127.0.0.1:8000'
        qr_path = generate_product_qr(product, base)
        if qr_path:
            product.qr_code = qr_path
            product.save()

        # Save to blockchain
        data = f"addproduct#{user.username}#{name}#{price}#{quantity}#{description}#{str(date.today())}\n"
        receipt = blockchain.save_product(data)
        if receipt:
            product.blockchain_hash = str(receipt.get('transactionHash', ''))
            product.save()

        # Add initial transport log
        transport_location = request.POST.get('transport_location', '').strip()
        if transport_location:
            TransportLog.objects.create(
                product=product, stage='Harvested',
                location=transport_location,
                handler=user.username,
                notes=f'Product harvested at {origin_location}'
            )

        messages.success(request, f'Product "{name}" added successfully!')
        return redirect('farmer_dashboard')

    ctx = get_base_context(request)
    return render(request, 'farmer/add_product.html', ctx)


@farmer_required
def farmer_update_product(request, product_id):
    """Farmer: Update product quantity and add transport log."""
    user = get_current_user(request)
    product = get_object_or_404(Product, pk=product_id, farmer=user)

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'update_quantity':
            add_qty = float(request.POST.get('quantity', '0'))
            product.quantity += add_qty
            product.save()

            # Update blockchain
            blockchain_data = f"addproduct#{user.username}#{product.name}#{product.price}#{product.quantity}#{product.description}#{str(date.today())}\n"
            blockchain.save_product(blockchain_data)

            messages.success(request, f'Quantity updated to {product.quantity}.')

        elif action == 'add_transport':
            stage = request.POST.get('stage', '')
            location = request.POST.get('location', '').strip()
            handler = request.POST.get('handler', '').strip()
            notes = request.POST.get('notes', '').strip()

            if stage and location:
                TransportLog.objects.create(
                    product=product, stage=stage,
                    location=location, handler=handler, notes=notes
                )
                messages.success(request, 'Transport log added.')
            else:
                messages.error(request, 'Stage and location are required.')

        return redirect('farmer_update_product', product_id=product.pk)

    ctx = get_base_context(request)
    ctx['product'] = product
    ctx['transport_logs'] = product.transport_logs.all()
    return render(request, 'farmer/update_product.html', ctx)


@farmer_required
def farmer_view_sales(request):
    """Farmer: View my sales."""
    user = get_current_user(request)
    ctx = get_base_context(request)
    ctx['sales'] = Purchase.objects.filter(farmer=user).select_related('consumer', 'product')
    return render(request, 'farmer/view_sales.html', ctx)


# ============================================================
# CONSUMER VIEWS
# ============================================================

@consumer_required
def consumer_dashboard(request):
    """Consumer dashboard — browse products and view purchase history."""
    ctx = get_base_context(request)
    ctx['products'] = Product.objects.filter(is_available=True, quantity__gt=0)
    ctx['purchases'] = Purchase.objects.filter(
        consumer=get_current_user(request)
    ).select_related('product', 'farmer')
    return render(request, 'consumer/dashboard.html', ctx)


@consumer_required
def consumer_purchase(request, product_id):
    """Consumer: Purchase a product."""
    user = get_current_user(request)
    product = get_object_or_404(Product, pk=product_id, is_available=True)

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', '1'))

        if quantity > float(product.quantity):
            messages.error(request, f'Only {product.quantity} available.')
            return redirect('consumer_purchase', product_id=product.pk)

        total = float(product.price) * quantity

        # Create purchase
        purchase = Purchase.objects.create(
            consumer=user, product=product,
            farmer=product.farmer,
            quantity=quantity, total_amount=total
        )

        # Update product quantity
        product.quantity -= quantity
        if product.quantity <= 0:
            product.is_available = False
        product.save()

        # Save to blockchain
        data = f"{user.username}#{product.farmer.username}#{product.name}#{quantity}#{total}#{str(date.today())}\n"
        receipt = blockchain.save_purchase(data)
        if receipt:
            purchase.blockchain_hash = str(receipt.get('transactionHash', ''))
            purchase.save()

        # Add transport log for purchase
        TransportLog.objects.create(
            product=product, stage='Delivered',
            location=user.address or 'Customer Location',
            handler='Delivery Service',
            notes=f'Purchased by {user.username} — Qty: {quantity}'
        )

        messages.success(request, f'Purchase successful! Total: ₹{total:.2f}')
        return redirect('consumer_dashboard')

    ctx = get_base_context(request)
    ctx['product'] = product
    ctx['farmer'] = product.farmer
    return render(request, 'consumer/purchase.html', ctx)

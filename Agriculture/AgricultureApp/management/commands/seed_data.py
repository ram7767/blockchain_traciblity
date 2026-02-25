"""
Django Management Command: seed_data
Seeds the database with sample farmers, consumers, 100+ products, and transport logs.
Idempotent — only seeds if the database is empty.
"""

import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from AgricultureApp.models import UserProfile, Product, TransportLog, Purchase


class Command(BaseCommand):
    help = 'Seed database with sample data (5 farmers, 5 consumers, 100+ products, transport logs)'

    def handle(self, *args, **options):
        # Check if already seeded
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING('⚠️  Database already has data — skipping seed'))
            return

        self.stdout.write('🌱 Seeding database with sample data...')

        # =============================================
        # FARMERS
        # =============================================
        farmers_data = [
            {
                'username': 'rajesh_kumar', 'password': 'farmer123',
                'email': 'rajesh@agrichain.com', 'contact': '9876543210',
                'address': 'Village Chandpur, Dist. Pune, Maharashtra',
            },
            {
                'username': 'anitha_devi', 'password': 'farmer123',
                'email': 'anitha@agrichain.com', 'contact': '9876543211',
                'address': 'Kothagudem, Bhadradri, Telangana',
            },
            {
                'username': 'suresh_reddy', 'password': 'farmer123',
                'email': 'suresh@agrichain.com', 'contact': '9876543212',
                'address': 'Anantapur, Andhra Pradesh',
            },
            {
                'username': 'lakshmi_bai', 'password': 'farmer123',
                'email': 'lakshmi@agrichain.com', 'contact': '9876543213',
                'address': 'Hosur, Krishnagiri, Tamil Nadu',
            },
            {
                'username': 'mohan_singh', 'password': 'farmer123',
                'email': 'mohan@agrichain.com', 'contact': '9876543214',
                'address': 'Karnal, Haryana',
            },
        ]

        farmers = []
        for fd in farmers_data:
            farmer = UserProfile.objects.create(user_type='Farmer', **fd)
            farmers.append(farmer)
            self.stdout.write(f'  👨‍🌾 Farmer: {farmer.username}')

        # =============================================
        # CONSUMERS
        # =============================================
        consumers_data = [
            {
                'username': 'priya_sharma', 'password': 'customer123',
                'email': 'priya@email.com', 'contact': '9988776655',
                'address': 'Banjara Hills, Hyderabad, Telangana',
            },
            {
                'username': 'amit_patel', 'password': 'customer123',
                'email': 'amit@email.com', 'contact': '9988776656',
                'address': 'Koramangala, Bangalore, Karnataka',
            },
            {
                'username': 'sneha_gupta', 'password': 'customer123',
                'email': 'sneha@email.com', 'contact': '9988776657',
                'address': 'Andheri West, Mumbai, Maharashtra',
            },
            {
                'username': 'vikram_joshi', 'password': 'customer123',
                'email': 'vikram@email.com', 'contact': '9988776658',
                'address': 'Connaught Place, New Delhi',
            },
            {
                'username': 'divya_nair', 'password': 'customer123',
                'email': 'divya@email.com', 'contact': '9988776659',
                'address': 'T. Nagar, Chennai, Tamil Nadu',
            },
        ]

        consumers = []
        for cd in consumers_data:
            consumer = UserProfile.objects.create(user_type='Consumer', **cd)
            consumers.append(consumer)
            self.stdout.write(f'  🛒 Consumer: {consumer.username}')

        # =============================================
        # 110 PRODUCTS (across 5 categories, distributed among farmers)
        # =============================================
        products_catalog = [
            # ---- FRUITS (25) ----
            ('Alphonso Mango', 'Fruits', 350, 'Premium Ratnagiri Alphonso mangoes, hand-picked and naturally ripened. GI-tagged origin.', 'Ratnagiri, Maharashtra'),
            ('Red Banana', 'Fruits', 80, 'Rare red-skinned bananas rich in beta-carotene and potassium. Organically grown.', 'Kamalapur, Karnataka'),
            ('Nagpur Orange', 'Fruits', 120, 'Fresh Nagpur oranges with high vitamin C content. Direct from the orange capital of India.', 'Nagpur, Maharashtra'),
            ('Kashmir Apple', 'Fruits', 250, 'Hand-picked Kashmiri apples from high-altitude orchards. Naturally sweet and crisp.', 'Shopian, Kashmir'),
            ('Pomegranate', 'Fruits', 180, 'Bhagwa variety pomegranate with deep red arils. Rich in antioxidants.', 'Solapur, Maharashtra'),
            ('Guava', 'Fruits', 60, 'Allahabad Safeda guavas, crisp and sweet. High in dietary fiber.', 'Prayagraj, UP'),
            ('Papaya', 'Fruits', 45, 'Taiwan Red Lady variety papayas, golden flesh with sweet taste.', 'Coimbatore, Tamil Nadu'),
            ('Dragon Fruit', 'Fruits', 280, 'Exotic pink dragon fruit grown using vertical farming techniques.', 'Sangli, Maharashtra'),
            ('Custard Apple', 'Fruits', 150, 'Sitaphal — creamy, sweet tropical fruit. Organically cultivated.', 'Pune, Maharashtra'),
            ('Jackfruit', 'Fruits', 90, 'Giant jackfruit pods, perfect for curries and desserts. Chemical-free.', 'Panruti, Tamil Nadu'),
            ('Watermelon', 'Fruits', 35, 'Sweet seedless watermelons, perfect for summer hydration. Farm-fresh.', 'Chitradurga, Karnataka'),
            ('Muskmelon', 'Fruits', 55, 'Aromatic muskmelons with high sugar content. Drip-irrigated.', 'Lucknow, UP'),
            ('Kiwi', 'Fruits', 320, 'Himalayan kiwi fruit, tart and rich in vitamin C. Cold-climate grown.', 'Arunachal Pradesh'),
            ('Passion Fruit', 'Fruits', 400, 'Purple passion fruit with intense tropical flavor. Limited batch.', 'Wayanad, Kerala'),
            ('Sapota (Chikoo)', 'Fruits', 70, 'Kalipatti variety sapota, very sweet and grainy texture.', 'Bordi, Maharashtra'),
            ('Lychee', 'Fruits', 200, 'Shahi Litchi from Bihar, juicy and fragrant. Short seasonal availability.', 'Muzaffarpur, Bihar'),
            ('Sweet Lime (Mosambi)', 'Fruits', 65, 'Fresh mosambi for juice, mild and sweet citrus flavor.', 'Aurangabad, Maharashtra'),
            ('Pineapple', 'Fruits', 75, 'Giant Queen pineapples, sweet-tart flavor profile.', 'Silchar, Assam'),
            ('Coconut', 'Fruits', 40, 'Tender coconut water and fresh white kernel. Daily harvest.', 'Pollachi, Tamil Nadu'),
            ('Fig (Anjeer)', 'Fruits', 450, 'Fresh premium figs, soft and honey-sweet. Limited organic batch.', 'Pune, Maharashtra'),
            ('Amla (Indian Gooseberry)', 'Fruits', 95, 'Vitamin C powerhouse, used in Ayurvedic preparations. Sun-dried available.', 'Pratapgarh, UP'),
            ('Starfruit', 'Fruits', 110, 'Exotic star-shaped fruit with tangy-sweet taste. Chemical-free orchard.', 'Goa'),
            ('Ber (Indian Jujube)', 'Fruits', 50, 'Crunchy desert fruit, rich in minerals. Drought-resistant farming.', 'Jodhpur, Rajasthan'),
            ('Wood Apple', 'Fruits', 85, 'Traditional hard-shelled fruit used for juices and chutneys.', 'Bastar, Chhattisgarh'),
            ('Jamun', 'Fruits', 130, 'Purple java plum, excellent for blood sugar management. Seasonal.', 'Varanasi, UP'),

            # ---- VEGETABLES (30) ----
            ('Organic Tomato', 'Vegetables', 45, 'Vine-ripened organic tomatoes, pesticide-free. Perfect for salads and cooking.', 'Kurnool, Andhra Pradesh'),
            ('Baby Spinach', 'Vegetables', 60, 'Tender baby spinach leaves, hydroponically grown. Washed and ready-to-eat.', 'Ooty, Tamil Nadu'),
            ('Red Onion', 'Vegetables', 35, 'Nashik red onions, pungent and flavorful. Stored in climate-controlled facility.', 'Nashik, Maharashtra'),
            ('Green Chili', 'Vegetables', 25, 'Guntur green chilies, medium-hot spice level. Farm-picked daily.', 'Guntur, Andhra Pradesh'),
            ('Brinjal (Eggplant)', 'Vegetables', 30, 'Purple long brinjal variety, ideal for bharta and curries.', 'Jalandhar, Punjab'),
            ('Cauliflower', 'Vegetables', 40, 'Snow-white cauliflower heads, tightly packed florets. Winter harvest.', 'Karnal, Haryana'),
            ('Cabbage', 'Vegetables', 25, 'Green globe cabbage, crisp and fresh. Great for salads and stir-fry.', 'Shimla, Himachal Pradesh'),
            ('Potato', 'Vegetables', 22, 'Kufri Jyoti variety potatoes, versatile cooking potato. Cold-stored.', 'Agra, UP'),
            ('Carrot', 'Vegetables', 50, 'Ooty carrots, deep orange and naturally sweet. High in beta-carotene.', 'Ooty, Tamil Nadu'),
            ('Beetroot', 'Vegetables', 45, 'Deep crimson beetroot, excellent for juicing. Organic certified.', 'Chikmagalur, Karnataka'),
            ('Bitter Gourd', 'Vegetables', 55, 'Fresh karela, excellent for diabetes management. Bitter but healthy.', 'Varanasi, UP'),
            ('Ridge Gourd', 'Vegetables', 30, 'Tender turai/luffa, low-calorie vegetable. Pesticide-free.', 'Nashik, Maharashtra'),
            ('Bottle Gourd', 'Vegetables', 28, 'Lauki/doodhi, versatile cooking vegetable. Great for weight management.', 'Meerut, UP'),
            ('Lady Finger (Okra)', 'Vegetables', 40, 'Bhindi — tender and non-fibrous. Drip-irrigated organic farming.', 'Indore, MP'),
            ('French Beans', 'Vegetables', 65, 'Crisp green beans, string-free variety. Hill-station grown.', 'Kodaikanal, Tamil Nadu'),
            ('Drumstick', 'Vegetables', 35, 'Fresh moringa pods, rich in nutrients. Tree-to-table freshness.', 'Tirunelveli, Tamil Nadu'),
            ('Curry Leaves', 'Vegetables', 15, 'Aromatic curry leaves bundle, essential for South Indian cooking.', 'Madurai, Tamil Nadu'),
            ('Green Peas', 'Vegetables', 80, 'Sweet green matar, shelled and fresh. Winter season special.', 'Amritsar, Punjab'),
            ('Sweet Corn', 'Vegetables', 35, 'Golden sweet corn cobs, perfect for grilling. Non-GMO seeds.', 'Pune, Maharashtra'),
            ('Mushroom (Button)', 'Vegetables', 120, 'Fresh white button mushrooms, grown in controlled poly-houses.', 'Solan, Himachal Pradesh'),
            ('Capsicum (Bell Pepper)', 'Vegetables', 90, 'Mixed color bell peppers — red, yellow, green. Greenhouse grown.', 'Bangalore, Karnataka'),
            ('Radish', 'Vegetables', 20, 'Japanese white radish (mooli), crunchy and mild. Great for salads.', 'Hisar, Haryana'),
            ('Zucchini', 'Vegetables', 75, 'Italian green zucchini, versatile for grilling, baking, spiralizing.', 'Mahabaleshwar, Maharashtra'),
            ('Broccoli', 'Vegetables', 110, 'Premium broccoli florets, superfood vegetable. Cold-climate grown.', 'Ooty, Tamil Nadu'),
            ('Lettuce', 'Vegetables', 85, 'Iceberg and romaine lettuce mix. Hydroponically grown, pesticide-free.', 'Pune, Maharashtra'),
            ('Ash Gourd', 'Vegetables', 25, 'Winter melon, great for traditional sweets and juices. Ayurvedic staple.', 'Thrissur, Kerala'),
            ('Yam (Suran)', 'Vegetables', 50, 'Purple elephant yam, used in traditional Indian dishes.', 'Midnapore, West Bengal'),
            ('Sweet Potato', 'Vegetables', 40, 'Orange-flesh sweet potatoes, naturally sweet and nutritious.', 'Bhubaneswar, Odisha'),
            ('Cluster Beans (Guar)', 'Vegetables', 35, 'Tender gavar beans, traditional Rajasthani vegetable. Drought-resistant.', 'Jaipur, Rajasthan'),
            ('Taro Root (Arbi)', 'Vegetables', 45, 'Colocasia roots, starchy and earthy flavor. Monsoon harvest.', 'Lucknow, UP'),

            # ---- GRAINS (25) ----
            ('Basmati Rice', 'Grains', 180, 'Aged 1121 Basmati rice, extra-long grain. Aromatic and fluffy when cooked.', 'Karnal, Haryana'),
            ('Brown Rice', 'Grains', 120, 'Unpolished brown rice, high in fiber and minerals. Organically grown.', 'Warangal, Telangana'),
            ('Red Rice', 'Grains', 150, 'Matta rice from Kerala, nutty flavor and high fiber. Traditional staple.', 'Palakkad, Kerala'),
            ('Wheat', 'Grains', 45, 'Lok-1 variety wheat, perfect for chapatis and bread. Stone-ground.', 'Indore, MP'),
            ('Pearl Millet (Bajra)', 'Grains', 55, 'Gluten-free bajra, ideal for rotis and porridge. Iron-rich.', 'Jodhpur, Rajasthan'),
            ('Finger Millet (Ragi)', 'Grains', 65, 'Calcium-rich ragi, perfect for dosa, roti and porridge. Organic.', 'Tumkur, Karnataka'),
            ('Sorghum (Jowar)', 'Grains', 50, 'Whole jowar grains, gluten-free superfood grain. Dual-purpose variety.', 'Solapur, Maharashtra'),
            ('Foxtail Millet', 'Grains', 90, 'Ancient grain revival — thinai/kangni. Rich in iron and B vitamins.', 'Anantapur, Andhra Pradesh'),
            ('Barnyard Millet', 'Grains', 95, 'Sanwa/kuthiraivali — excellent fasting grain. Low glycemic index.', 'Uttarkashi, Uttarakhand'),
            ('Quinoa (Indian)', 'Grains', 350, 'Locally grown quinoa, complete protein source. Chemical-free cultivation.', 'Anantapur, Andhra Pradesh'),
            ('Black Rice', 'Grains', 280, 'Forbidden rice — Manipur black rice with antioxidants. Rare grain.', 'Imphal, Manipur'),
            ('Toor Dal', 'Grains', 130, 'Split pigeon pea dal, staple protein source. Mill-fresh and clean.', 'Latur, Maharashtra'),
            ('Moong Dal', 'Grains', 140, 'Split green gram, easy to digest. Versatile for dal, chilla, sprouts.', 'Rajkot, Gujarat'),
            ('Chana Dal', 'Grains', 90, 'Bengal gram split, nutty flavor. Perfect for dal and sweets.', 'Gulbarga, Karnataka'),
            ('Masoor Dal', 'Grains', 100, 'Red lentils, quick-cooking and protein-rich. Essential pantry staple.', 'Raipur, Chhattisgarh'),
            ('Urad Dal', 'Grains', 120, 'Black gram split, essential for idli, vada, and dal makhani.', 'Indore, MP'),
            ('Chickpea (Kabuli Chana)', 'Grains', 110, 'Large white chickpeas, perfect for hummus and chhole. Premium grade.', 'Hanumangarh, Rajasthan'),
            ('Flax Seeds', 'Grains', 200, 'Golden flax seeds, omega-3 rich superfood. Cold-pressed quality.', 'Kangra, Himachal Pradesh'),
            ('Sesame Seeds', 'Grains', 180, 'White sesame/til, essential for traditional cooking and sweets.', 'Rajkot, Gujarat'),
            ('Groundnut', 'Grains', 85, 'Bold variety groundnuts, roasted or raw. High protein snack.', 'Junagadh, Gujarat'),
            ('Sunflower Seeds', 'Grains', 220, 'Hulled roasted sunflower seeds, vitamin E powerhouse.', 'Belgaum, Karnataka'),
            ('Amaranth (Rajgira)', 'Grains', 160, 'Gluten-free ancient grain, pops like popcorn. High protein.', 'Aurangabad, Maharashtra'),
            ('Chia Seeds', 'Grains', 380, 'Locally cultivated chia seeds, fiber and omega-3 rich superfood.', 'Chittoor, Andhra Pradesh'),
            ('Maize (Corn)', 'Grains', 30, 'Yellow maize kernels, versatile for flour, feed, and popcorn.', 'Davangere, Karnataka'),
            ('Oats (Steel Cut)', 'Grains', 170, 'Steel-cut Indian oats, high fiber breakfast grain. Minimally processed.', 'Jabalpur, MP'),

            # ---- DAIRY (15) ----
            ('A2 Cow Milk', 'Dairy', 75, 'Pure A2 desi cow milk, unhomogenized. Daily morning delivery.', 'Anand, Gujarat'),
            ('Buffalo Milk', 'Dairy', 65, 'Rich Murrah buffalo milk, high fat content. Fresh and creamy.', 'Karnal, Haryana'),
            ('Fresh Paneer', 'Dairy', 320, 'Handmade cottage cheese from A2 milk. No preservatives.', 'Mathura, UP'),
            ('Desi Ghee', 'Dairy', 700, 'Bilona method A2 cow ghee, golden and aromatic. Ayurvedic grade.', 'Rajkot, Gujarat'),
            ('Curd (Dahi)', 'Dairy', 50, 'Thick-set traditional dahi, probiotic-rich. Made from full-cream milk.', 'Kolhapur, Maharashtra'),
            ('Buttermilk (Chaas)', 'Dairy', 30, 'Spiced traditional chaas with cumin and curry leaves. Refreshing.', 'Jaipur, Rajasthan'),
            ('Makhana (Fox Nut)', 'Dairy', 450, 'Roasted lotus seeds, superfood snack. Handpicked and graded.', 'Madhubani, Bihar'),
            ('Honey (Raw)', 'Dairy', 350, 'Unprocessed wild forest honey, multi-floral. NMR tested.', 'Nilgiris, Tamil Nadu'),
            ('Jaggery (Gur)', 'Dairy', 80, 'Organic sugarcane jaggery, chemical-free processing. Rich in iron.', 'Kolhapur, Maharashtra'),
            ('Buffalo Curd', 'Dairy', 55, 'Extra thick buffalo milk curd, creamy texture. Traditional set.', 'Guntur, Andhra Pradesh'),
            ('Goat Milk', 'Dairy', 120, 'Pure goat milk, easier to digest. Best for lactose-sensitive individuals.', 'Salem, Tamil Nadu'),
            ('Lassi', 'Dairy', 40, 'Sweet Punjabi lassi, thick and creamy. Traditional recipe.', 'Amritsar, Punjab'),
            ('Cream (Malai)', 'Dairy', 150, 'Fresh milk cream, perfect for sweets and desserts.', 'Anand, Gujarat'),
            ('Mishti Doi', 'Dairy', 90, 'Authentic Bengali sweetened yogurt, caramelized and thick.', 'Kolkata, West Bengal'),
            ('Shrikhand', 'Dairy', 200, 'Saffron-flavored hung curd dessert. Traditional Gujarati recipe.', 'Ahmedabad, Gujarat'),

            # ---- OTHER (15) ----
            ('Turmeric Powder', 'Other', 250, 'Lakadong turmeric, 7%+ curcumin content. Organically processed.', 'Jaintia Hills, Meghalaya'),
            ('Black Pepper', 'Other', 600, 'Malabar black pepper, bold and pungent. Sun-dried whole peppercorns.', 'Idukki, Kerala'),
            ('Cardamom', 'Other', 2500, 'Alleppey green cardamom, intensely aromatic. 8mm+ bold grade.', 'Thekkady, Kerala'),
            ('Cinnamon', 'Other', 400, 'Ceylon cinnamon sticks, sweet and delicate. Premium Malabar variety.', 'Trivandrum, Kerala'),
            ('Coffee Beans', 'Other', 550, 'Arabica plantation AA, medium roast. Shade-grown at 4000ft altitude.', 'Coorg, Karnataka'),
            ('Green Tea', 'Other', 380, 'Darjeeling first flush green tea, muscatel notes. FTGFOP grade.', 'Darjeeling, West Bengal'),
            ('Moringa Powder', 'Other', 300, 'Dried moringa leaf powder, superfood supplement. 90+ nutrients.', 'Hosur, Tamil Nadu'),
            ('Virgin Coconut Oil', 'Other', 450, 'Cold-pressed virgin coconut oil, unrefined. Multi-use wellness oil.', 'Thrissur, Kerala'),
            ('Cashew Nuts', 'Other', 800, 'W240 whole cashews, premium Goan quality. Light ivory color.', 'Goa'),
            ('Almond', 'Other', 750, 'Mamra almonds from Kashmir, oil-rich and crunchy. Hand-cracked.', 'Srinagar, Kashmir'),
            ('Dried Mango', 'Other', 200, 'Sun-dried mango slices (amchur), tangy and preservative-free.', 'Ratnagiri, Maharashtra'),
            ('Tamarind', 'Other', 60, 'Seedless tamarind block, sour and tangy. Essential for South Indian cooking.', 'Tirunelveli, Tamil Nadu'),
            ('Saffron', 'Other', 5000, 'Pure Kashmiri kesar (saffron), ISO grade 1. Hand-harvested.', 'Pampore, Kashmir'),
            ('Rose Water', 'Other', 180, 'Steam-distilled rose water from Kannauj roses. Food and beauty grade.', 'Kannauj, UP'),
            ('Tulsi (Holy Basil) Leaves', 'Other', 45, 'Dried tulsi leaves for tea and Ayurvedic use. Krishn tulsi variety.', 'Lucknow, UP'),
        ]

        self.stdout.write(f'\n  📦 Creating {len(products_catalog)} products...')

        transport_stages = ['Harvested', 'Packed', 'InTransit', 'AtWarehouse', 'Delivered']
        transport_handlers = [
            'Farm Workers', 'Packing Unit', 'AgriLogistics Pvt Ltd',
            'Cold Chain Solutions', 'FreshDrop Delivery', 'Local Transport',
            'Warehouse Team', 'Quality Inspector'
        ]

        all_products = []
        for i, (name, category, price, description, origin) in enumerate(products_catalog):
            farmer = farmers[i % len(farmers)]
            days_ago = random.randint(1, 60)
            harvest = date.today() - timedelta(days=days_ago)
            qty = random.choice([10, 15, 20, 25, 30, 50, 75, 100, 150, 200, 500])

            product = Product.objects.create(
                farmer=farmer,
                name=name,
                description=description,
                price=price,
                quantity=qty,
                category=category,
                origin_location=origin,
                harvest_date=harvest,
            )
            all_products.append(product)

            # Add 2-4 transport logs per product
            num_logs = random.randint(2, 4)
            for j in range(num_logs):
                stage = transport_stages[min(j, len(transport_stages) - 1)]
                log_time = harvest + timedelta(days=j * random.randint(1, 3))
                TransportLog.objects.create(
                    product=product,
                    stage=stage,
                    location=origin if j == 0 else random.choice([
                        'District Warehouse, ' + origin.split(',')[-1].strip(),
                        'Cold Storage Hub, ' + origin.split(',')[-1].strip(),
                        'Regional Distribution Center',
                        'Local Market Hub',
                        'Quality Testing Lab',
                    ]),
                    handler=random.choice(transport_handlers),
                    notes=f'{stage} — Batch #{product.pk:04d}',
                )

        self.stdout.write(f'  ✅ Created {len(all_products)} products with transport logs')

        # =============================================
        # SAMPLE PURCHASES (20 purchases)
        # =============================================
        self.stdout.write('\n  🛒 Creating sample purchases...')
        purchase_count = 0
        for consumer in consumers:
            # Each consumer buys 4 random products
            bought = random.sample(all_products, 4)
            for product in bought:
                qty = random.choice([1, 2, 3, 5])
                if qty > product.quantity:
                    qty = 1
                total = float(product.price) * qty
                Purchase.objects.create(
                    consumer=consumer,
                    product=product,
                    farmer=product.farmer,
                    quantity=qty,
                    total_amount=total,
                )
                product.quantity -= qty
                product.save()
                purchase_count += 1

                # Add delivery transport log
                TransportLog.objects.create(
                    product=product,
                    stage='Delivered',
                    location=consumer.address,
                    handler='FreshDrop Delivery',
                    notes=f'Delivered to {consumer.username} — Qty: {qty}',
                )

        self.stdout.write(f'  ✅ Created {purchase_count} sample purchases')

        # =============================================
        # SUMMARY
        # =============================================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS('  🌱 Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  👨‍🌾 Farmers:   {len(farmers)}'))
        self.stdout.write(self.style.SUCCESS(f'  🛒 Consumers: {len(consumers)}'))
        self.stdout.write(self.style.SUCCESS(f'  📦 Products:  {len(all_products)}'))
        self.stdout.write(self.style.SUCCESS(f'  🚚 Purchases: {purchase_count}'))
        self.stdout.write(self.style.SUCCESS('═' * 50))

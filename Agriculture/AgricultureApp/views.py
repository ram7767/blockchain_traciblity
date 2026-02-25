from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import os
from django.core.files.storage import FileSystemStorage
import pickle
import pyqrcode
import png
from pyqrcode import QRCode

global details, username
details=''
global contract, product_name


def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Agricultural.json' #agriculture contract code
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #hash address to access agriculture contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'addproduct':
        details = contract.functions.getTracingData().call()
    if contract_type == 'purchase':
        details = contract.functions.getPurchase().call()     
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Agricultural.json' #agriculture contract file
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addproduct':
        details+=currentData
        msg = contract.functions.setTracingData(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'purchase':
        details+=currentData
        msg = contract.functions.setPurchase(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    
    

def updateQuantityBlock(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Agricultural.json' #student contract file
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setTracingData(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def ViewSales(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Consumer Name</font></th>'
        output+='<th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Amount</font></th>'
        output+='<th><font size=3 color=black>Card Details</font></th>'
        output+='<th><font size=3 color=black>CVV</font></th>'
        output+='<th><font size=3 color=black>Purchase Date</font></th></tr>'
        readDetails("purchase")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[2])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td></tr>'                    
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

def ViewFarmerSales(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Consumer Name</font></th>'
        output+='<th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Amount</font></th>'
        output+='<th><font size=3 color=black>Card Details</font></th>'
        output+='<th><font size=3 color=black>CVV</font></th>'
        output+='<th><font size=3 color=black>Purchase Date</font></th></tr>'
        readDetails("purchase")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[1] == username:
                output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td></tr>'                            
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'FarmerScreen.html', context)     
    
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def FarmerLogin(request):
    if request.method == 'GET':
       return render(request, 'FarmerLogin.html', {})

def ConsumerLogin(request):
    if request.method == 'GET':
       return render(request, 'ConsumerLogin.html', {})    
    
def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UpdateQuantityAction(request):
    if request.method == 'POST':
        farmer = request.POST.get('t1', False)
        pname = request.POST.get('t2', False)
        quantity = request.POST.get('t3', False)
        index = 0
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == farmer and arr[2] == pname:
                    today = date.today()
                    index = i
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(float(arr[4])+float(quantity))+"#"+arr[5]+"#"+arr[6]+"#"+str(today)+"\n"
                    break
        for i in range(len(rows)-1):
            if i != index:
                record += rows[i]+"\n"
        updateQuantityBlock(record)
        context= {'data':"Quantity details updated"}
        return render(request, 'AdminScreen.html', context)    

def UpdateQuantity(request):
    if request.method == 'GET':
        global product_name
        farmer = request.GET['farmer']
        pname = request.GET['pname']
        output = '<tr><td><font size="" color="black">Farmer&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value='+farmer+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Product&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t2" style="font-family: Comic Sans MS" size="30" value='+pname+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Quantity</font></td>'
        output += '<td><input type="text" name="t3" style="font-family: Comic Sans MS" size="15" /></td></tr>'
        context= {'data1':output}
        return render(request, 'UpdateQuantity.html', context)      

def UpdateProduct(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Date</font></th>'
        output+='<th><font size=3 color=black>QR Code</font></th>'
        output+='<th><font size=3 color=black>Update Quantity</font></th></tr>'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct':
                output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
                output+='<td><img src="/static/products/'+arr[6]+'" width="200" height="200"></img></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
                output+='<td><img src="/static/qrcode/'+arr[1]+arr[2]+'.png" width="200" height="200"></img></td>'
                output+='<td><a href=\'UpdateQuantity?farmer="'+arr[1]+'"&pname="'+arr[2]+'"\'><font size=3 color=black>Click Here</font></a></td></tr>'                    
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)      

def AddProduct(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Farmer&nbsp;Name</font></td><td><select name="farmer">'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                output += '<option value="'+arr[1]+'">'+arr[1]+'</option>'
        output += '</select></td></tr>'
        context= {'data1': output}
        return render(request, 'AddProduct.html', context)

def AddProductAction(request):
    if request.method == 'POST':
        farmer = request.POST.get('farmer', False)
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES['t5']
        imagename = request.FILES['t5'].name

        status = "none"
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct" and arr[1] == farmer and arr[2] == cname:
                status = "Your Farming product already exists in Blockchain"
                break
        if status == "none":
            today = date.today()
            fs = FileSystemStorage()
            filename = fs.save('AgricultureApp/static/products/'+imagename, image)
            data = "addproduct#"+farmer+"#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+imagename+"#"+str(today)+"\n"
            saveDataBlockChain(data,"addproduct")
            url = pyqrcode.create(farmer+cname)
            url.png('AgricultureApp/static/qrcode/'+farmer+cname+'.png', scale = 6)
            status = "Product details saved in Blockchain"
        context= {'data':"Product details saved in Blockchain"}
        return render(request, 'AdminScreen.html', context)    

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        usertype = request.POST.get('type', False)
        record = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username:
                    record = "exists"
                    break
        if record == 'none':
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+usertype+"\n"
            saveDataBlockChain(data,"signup")
            context= {'data':'Signup process completd and record saved in Blockchain'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Register.html', context)    

def AdminLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "AdminLogin.html"
        context= {'data':'Invalid login details'}
        if username == 'admin' and password == 'admin':
            context = {'data':"Welcome "+username}
            status = "AdminScreen.html"
        return render(request, status, context)         

def FarmerLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "FarmerLogin.html"
        context= {'data':'Invalid login details'}
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username and arr[2] == password and arr[6] == 'Farmer':
                    context = {'data':"Welcome "+username}
                    status = 'FarmerScreen.html'
                    break
        return render(request, status, context)              

def ConsumerLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = "ConsumerLogin.html"
        context= {'data':'Invalid login details'}
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == username and arr[2] == password and arr[6] == 'Consumer':
                    context = {'data':"Welcome "+username}
                    status = 'ConsumerScreen.html'
                    break
        return render(request, status, context)


def UpdateFarmerQuantityAction(request):
    if request.method == 'POST':
        farmer = request.POST.get('t1', False)
        pname = request.POST.get('t2', False)
        quantity = request.POST.get('t3', False)
        index = 0
        record = ''
        readDetails("addproduct")
        rows = details.split("\n")
        tot_qty = 0
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct":
                if arr[1] == farmer and arr[2] == pname:
                    today = date.today()
                    index = i
                    record = arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+str(float(arr[4])+float(quantity))+"#"+arr[5]+"#"+arr[6]+"#"+str(today)+"\n"
                    break
        for i in range(len(rows)-1):
            if i != index:
                record += rows[i]+"\n"
        updateQuantityBlock(record)
        context= {'data':"Quantity details updated"}
        return render(request, 'FarmerScreen.html', context)    

def UpdateFarmerQuantity(request):
    if request.method == 'GET':
        global product_name
        farmer = request.GET['farmer']
        pname = request.GET['pname']
        output = '<tr><td><font size="" color="black">Farmer&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value='+farmer+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Product&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t2" style="font-family: Comic Sans MS" size="30" value='+pname+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Quantity</font></td>'
        output += '<td><input type="text" name="t3" style="font-family: Comic Sans MS" size="15" /></td></tr>'
        context= {'data1':output}
        return render(request, 'UpdateFarmerQuantity.html', context)      

def UpdateFarmerProduct(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Date</font></th>'
        output+='<th><font size=3 color=black>QR Code</font></th>'
        output+='<th><font size=3 color=black>Update Quantity</font></th></tr>'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct' and arr[1] == username:
                output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
                output+='<td><img src="/static/products/'+arr[6]+'" width="200" height="200"></img></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
                output+='<td><img src="/static/qrcode/'+arr[1]+arr[2]+'.png" width="200" height="200"></img></td>'
                output+='<td><a href=\'UpdateFarmerQuantity?farmer="'+arr[1]+'"&pname="'+arr[2]+'"\'><font size=3 color=black>Click Here</font></a></td></tr>'                    
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'FarmerScreen.html', context)      

def AddFarmerProduct(request):
    if request.method == 'GET':
        return render(request, 'AddFarmerProduct.html', {})

def AddFarmerProductAction(request):
    if request.method == 'POST':
        global username
        farmer = username
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES['t5']
        imagename = request.FILES['t5'].name

        status = "none"
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "addproduct" and arr[1] == farmer and arr[2] == cname:
                status = "Your Farming product already exists in Blockchain"
                break
        if status == "none":
            today = date.today()
            fs = FileSystemStorage()
            filename = fs.save('AgricultureApp/static/products/'+imagename, image)
            data = "addproduct#"+farmer+"#"+cname+"#"+price+"#"+qty+"#"+desc+"#"+imagename+"#"+str(today)+"\n"
            saveDataBlockChain(data,"addproduct")
            url = pyqrcode.create(farmer+cname)
            url.png('AgricultureApp/static/qrcode/'+farmer+cname+'.png', scale = 6)
            status = "Product details saved in Blockchain"
        context= {'data':"Product details saved in Blockchain"}
        return render(request, 'FarmerScreen.html', context)


def PurchaseAction(request):
    if request.method == 'GET':
        global username
        farmer = request.GET['farmer']
        pname = request.GET['pname']
        price = request.GET['price']
        output = '<tr><td><font size="" color="black">Farmer&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value='+farmer+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Product&nbsp;Name</font></td>'
        output += '<td><input type="text" name="t2" style="font-family: Comic Sans MS" size="30" value='+pname+' readonly/></td></tr>'
        output += '<tr><td><font size="" color="black">Product&nbsp;Price</font></td>'
        output += '<td><input type="text" name="t3" style="font-family: Comic Sans MS" size="15" value='+price+' readonly/></td></tr>'
        context= {'data1':output}
        return render(request, 'Purchase.html', context)   


def Purchase(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Farmer Name</font></th>'
        output+='<th><font size=3 color=black>Product Name</font></th>'
        output+='<th><font size=3 color=black>Price</font></th>'
        output+='<th><font size=3 color=black>Quantity</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Image</font></th>'
        output+='<th><font size=3 color=black>Date</font></th>'
        output+='<th><font size=3 color=black>QR Code</font></th>'
        output+='<th><font size=3 color=black>Update Quantity</font></th></tr>'
        readDetails("addproduct")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == 'addproduct':
                output+='<tr><td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
                output+='<td><img src="/static/products/'+arr[6]+'" width="200" height="200"></img></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
                output+='<td><img src="/static/qrcode/'+arr[1]+arr[2]+'.png" width="200" height="200"></img></td>'
                output+='<td><a href=\'PurchaseAction?farmer="'+arr[1]+'"&pname="'+arr[2]+'"&price="'+arr[3]+'"\'><font size=3 color=black>Click Here</font></a></td></tr>'                    
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ConsumerScreen.html', context)      

def SavePurchase(request):
    if request.method == 'POST':
        global username
        farmer = request.POST.get('t1', False)
        pname = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        qty = request.POST.get('t4', False)
        card = request.POST.get('t5', False)
        cvv = request.POST.get('t6', False)
        today = date.today()
        data = username+"#"+farmer+"#"+pname+"#"+qty+"#"+str(float(price)*float(qty))+"#"+card+"#"+cvv+"#"+str(today)+"\n"
        saveDataBlockChain(data,"purchase")
        status = "Your Purchase details saved in Blockchain<br/>Total Amount = "+str(float(price)*float(qty))
        context= {'data':status}
        return render(request, 'ConsumerScreen.html', context)



    

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import industryRequirement, farmerRequest, feedbacks, transactions
from django.shortcuts import get_object_or_404
from django.contrib import messages
import qrcode
import base64
from io import BytesIO
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Create your views here.
def main_page(request):
    return render(request,'base/index.html',{})

def flogin_page(request):
    if request.method == 'POST' and 'l' in request.POST:
        m = request.POST.get('m')
        p = request.POST.get('p')
        if User.objects.filter(username = m, last_name = "Farmer").exists():
            user = authenticate(request, username = m, password = p)
            if user is not None:
                login(request,user)
                return redirect('Farmer Page')
        else:
            return HttpResponse('Error, user does not exist')    
        
        
    if request.method == 'POST' and 's' in request.POST:
        name = request.POST.get('name')
        utype = request.POST.get('type')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        # Validate if the username already exists
        if User.objects.filter(username=mobile).exists():
            return render(request, 'base/flogin.html', {
                'error_message': 'User with this mobile number already exists.'
            })

        new_user = User.objects.create_user(username = mobile,email = email,password = pwd)
        new_user.first_name = name
        new_user.last_name = utype
        new_user.save()
        return redirect('Flogin Page')
   
    return render(request,'base/flogin.html',{})

def ilogin_page(request):
    if request.method == 'POST' and 'l' in request.POST:
        m = request.POST.get('m')
        p = request.POST.get('p')
        if User.objects.filter(username = m, last_name = "Industry").exists():
            user = authenticate(request, username = m, password = p)
            if user is not None:
                login(request,user)
                return redirect('Industry Page')
        else:
            return JsonResponse('Error, user does not exist')
        
    if request.method == 'POST' and 's' in request.POST:
        name = request.POST.get('name')
        utype = request.POST.get('type')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        # Validate if the username already exists
        if User.objects.filter(username=mobile).exists():
            return render(request, 'base/ilogin.html', {
                'error_message': 'User with this mobile number already exists.'
            })

        new_user = User.objects.create_user(username = mobile,email = email,password = pwd)
        new_user.first_name = name
        new_user.last_name = utype
        new_user.save()
        return redirect('Ilogin Page')
    return render(request,'base/ilogin.html',{})

def dlogin_page(request):
    if request.method == 'POST' and 'l' in request.POST:
        m = request.POST.get('m')
        p = request.POST.get('p')
        if User.objects.filter(username = m, last_name = "Analyst").exists():
            user = authenticate(request, username = m, password = p)
            if user is not None:
                login(request,user)
                return redirect('DA Page')
        else:
            return HttpResponse('Error, user does not exist')
        
    if request.method == 'POST' and 's' in request.POST:
        name = request.POST.get('name')
        utype = request.POST.get('type')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        # Validate if the username already exists
        if User.objects.filter(username=mobile).exists():
            return render(request, 'base/dlogin.html', {
                'error_message': 'User with this mobile number already exists.'
            })

        new_user = User.objects.create_user(username = mobile,email = email,password = pwd)
        new_user.first_name = name
        new_user.last_name = utype
        new_user.save()
        return redirect('Dlogin Page')
    return render(request,'base/dlogin.html',{})

@login_required
def farmer_page(request):
    farmerName = request.user.first_name
    if request.method == 'POST':
        industryName = request.POST.get('industryName')
        priceOffered = request.POST.get('priceOffered')
        materialType = request.POST.get('materialType')
        quantityAvailable = request.POST.get('quantityAvailable')
        phoneNumber = request.POST.get('phoneNumber')
        upiID = request.POST.get('upiID')
        status = "processing"
        
        if farmerRequest.objects.filter(farmerName = farmerName, industryName = industryName, materialType = materialType).exists():
            x = get_object_or_404(farmerRequest, farmerName = farmerName, industryName = industryName, materialType = materialType)
            x.quantityAvailable = quantityAvailable
            x.phoneNumber = phoneNumber
            x.upiID = upiID
            x.save()
        else:
            req = farmerRequest(farmerName = farmerName, industryName = industryName, materialType = materialType, priceOffered = priceOffered, quantityAvailable = quantityAvailable, phoneNumber = phoneNumber, upiID = upiID, status = status)
            req.save()
            
        return redirect('Farmer Page')
        
    offers = industryRequirement.objects.all()
    offers = offers.filter(quantityRequired__gt=0) 
    requests = farmerRequest.objects.filter(farmerName = farmerName)
    for r in requests:
        r.totalPrice = r.quantityAvailable * r.priceOffered
    trans = transactions.objects.filter(farmerName = farmerName)
    for t in trans:
        t.Date = str(t.Date).replace(',','-')
    return render(request,'farm/farmer.html',{'requests': requests, 'offers': offers, 'name': farmerName, 'trans': trans})    

# Function to interact with GPT
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# View for the chatbot page
def chatbot(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        prompt = "Please provide responses only to greetings, interactional inputs, or queries related to this page. For all other inquiries, kindly respond with 'Please ask relevant questions'.\nDescription: The Farmer Page is designed to help farmers efficiently manage their interactions with industries. It features sections such as Dashboard, Industry Offers, Transactions, Feedback, and Logout. The Dashboard allows farmers to track the status of their requests, while the Industry Offers section enables them to compare and select the best available options. After making a selection, farmers can access a Request Form to add or update their details and submit requests to industries. The Transactions section provides a way to monitor financial activities, and the Feedback feature allows farmers to share their thoughts with the admin. Finally, the Logout option lets farmers safely exit from their account./nInput: "+user_message
        bot_response = chat_with_gpt(prompt)
        return JsonResponse({"reply": bot_response})
    return render(request, "main/index.html")


@login_required
def industry_page(request):
    industryName = request.user.first_name
    if request.method == 'POST':
        materialType = request.POST.get('materialType')
        priceOffered = request.POST.get('priceOffered')
        quantityRequired = request.POST.get('quantityRequired')
        
        if industryRequirement.objects.filter(industryName = industryName, materialType = materialType).exists():
            x = get_object_or_404(industryRequirement, industryName = industryName, materialType = materialType)
            x.priceOffered = priceOffered
            x.quantityRequired = quantityRequired
            x.save()
        else:
            req = industryRequirement(industryName = industryName, materialType = materialType, priceOffered=priceOffered, quantityRequired = quantityRequired)
            req.save()
            
        return redirect('Industry Page')
          
    requests = farmerRequest.objects.filter(industryName = industryName)
    trans = transactions.objects.filter(industryName = industryName)
    for t in trans:
        t.Date = str(t.Date).replace(',','-')
    return render(request,'indus/industry.html',{'requests': requests, 'name': industryName, 'trans':trans})

def update_quantity(request):
    if request.method == 'POST':
        farmerName = request.POST.get('farmerName')
        industryName = request.POST.get('industryName')
        materialType = request.POST.get('materialType')
        quantity = int(request.POST.get('quantity'))
        
        industry_req = get_object_or_404(industryRequirement, industryName=industryName, materialType=materialType)
        y = get_object_or_404(farmerRequest, farmerName=farmerName, industryName=industryName, materialType=materialType)
        farmerName = y.farmerName
        
        if industry_req.quantityRequired >= quantity:
            industry_req.quantityRequired -= quantity
            industry_req.save()
            y.status = "Accepted"
            y.save()
            messages.success(request, f"Quantity updated successfully for {industryName} and Request from {farmerName} is hidden successfully.")
            
    return HttpResponse(status=204) 

def generate_payment(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        iname = request.POST.get('iname')
        mtype = request.POST.get('mtype')
        upi_id = request.POST.get('upi')
        amount = request.POST.get('am')

        if not upi_id or not amount:
            return JsonResponse({'error': 'UPI ID and amount are required'}, status=400)

        try:
            amount = float(amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid amount provided'}, status=400)

        # Generate QR code data
        qr_data = f"upi://pay?pa={upi_id}&am={amount}"
        qr = qrcode.make(qr_data)

        # Save QR code as an image in memory
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        # Convert QR code image to base64
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        y = get_object_or_404(farmerRequest, farmerName=fname, industryName=iname, materialType=mtype)
        # Render the template
        return render(request, 'indus/payment.html', {'y':y, 'upi_id': upi_id, 'amount': amount, 'qr_code': qr_base64})
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

def confirm_payment(request):
    if request.method == 'POST':
        ALLOWED_IMAGE_TYPES = [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/webp"
        ]
        txn_id = request.POST.get('txn_id')
        ss = request.FILES.get('ss')
        fname = request.POST.get('fname')
        iname = request.POST.get('iname')
        mtype = request.POST.get('mtype')
        ftype = ss.content_type
        req = get_object_or_404(farmerRequest, farmerName=fname, industryName=iname, materialType=mtype)
        amount = req.quantityAvailable * req.priceOffered
        quantity = req.quantityAvailable

        if ftype not in ALLOWED_IMAGE_TYPES:
            return JsonResponse({
                "error": "Invalid file type. Only image files are allowed."
            }, status=400)
        t = transactions(txn_id = txn_id, farmerName = fname, industryName = iname, materialType = mtype, quantity = quantity, amount = amount, ss = ss)
        t.save()
        req.delete()
        messages.success(request, f"Request from {fname} for selling {mtype} is deleted successfully.")
        return redirect('Industry Page')
    
    return HttpResponse(status=204)

@login_required
def da_page(request):
    trans = transactions.objects.all()
    for t in trans:
        t.Date = str(t.Date).replace(',','-')
    return render(request,'da/DA.html',{'trans': trans})

def feedback(request):
    if request.method == 'POST':
        utype = request.POST.get('utype')
        feed = request.POST.get('feed')
        f = feedbacks(userType = utype, feedback = feed)
        f.save()
        if utype == "Farmer":
            return redirect("Farmer Page")
        elif utype == "Industry":
            return redirect("Industry Page")
        elif utype == "Analyst":
            return redirect("DA Page")
    return HttpResponse(status=204) 

def logoutuser(request):
    logout(request)
    return redirect('Main Page')

 
    
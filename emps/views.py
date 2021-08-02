from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .forms import EmpPerModelForm , EmpPersonalform
from .models import EmpPersonal 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
import pdb #For Debugging the Code we Use PDB

# Create your views here.

def user_register(request):
    return HttpResponse("Hi..You have successfully Registered!")

def basic_load(request):
   return render(request,'index.html')

def user_modelform(request):
    form = EmpPerModelForm(request.POST)
    print(form)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponse(("Successfully Submitted the Details"))
        else:
            return HttpResponse("Invalid Data")
    return render(request,'modelform.html',{"form" :form})

def user_form(request):
    form = EmpPersonalform()
    if request.method =='POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        age = request.POST.get('age')
        address = request.POST.get('address')
        country = request.POST.get('country')
        print(name, mobile, email, age, address, country)
        EmpPersonal.objects.create(name=name, mobile=mobile, email=email, age=age, address=address, country=country) #meth1
        return HttpResponse("Successfully completed the Registration")
    return render(request, "normal_form.html", {"form" : form})

def html_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        age = request.POST.get('age')
        address = request.POST.get('address')
        country = request.POST.get('country')
        document = request.FILES.get('document')
        user_data = User.objects.create(username=name, email=email, is_active=True, is_staff=True)
        user_data.set_password(password)
        user_data.save()
        emp_det = EmpPersonal(name=name, mobile=mobile, email=email, age=age, address=address, country=country, user = user_data, document=document) #meth2
        emp_det.save()
        # return HttpResponse("Successfully registered")
    return render(request, 'htmlform.html')

def get_userlist(request):
    all_data = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            all_data = EmpPersonal.objects.all()
        else:
            all_data= EmpPersonal.objects.filter(user = request.user)
    return render(request, 'all_data.html', {'data': all_data})

def single_data(request,id):
    user_data = EmpPersonal.objects.get(id=id)
    return render(request, 'single_data.html', {'data': user_data})

def update_data(request,id):
    user_data = EmpPersonal.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        age = request.POST.get('age')
        address = request.POST.get('address')
        country = request.POST.get('country')
        filter_data = EmpPersonal.objects.filter(id = id)
        filter_data.update(name=name, mobile=mobile, email=email, age=age, address=address, country=country)
        return HttpResponse("Data Updated Successfully")
    return render(request, 'update_form.html', {'data': user_data})

def delete_user(request, id):
    EmpPersonal.objects.get(id = id).delete()
    messages.success(request, "Deleted Successfully")
    return redirect("get_userlist")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        check_user = authenticate(username=username,password=password)
        if check_user:
            login((request), check_user)
            messages.success(request, 'Hi {}, You have successfully Logged in'.format(check_user))
            return redirect("get_userlist")
            
        else:
            messages.error(request, "Invalid Credentials, Try again..!")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect("user_login")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        email_check = EmpPersonal.objects.filter(email=email)
        if email_check:
            otp_check = EmpPersonal.objects.filter(email=email)
            otp = random.randint(100000, 999999)
            save_otp = otp_check[0]
            save_otp.otp = str(otp)
            save_otp.save()
            msg = "Hi {},\n Below is the Verification code for Changing password {}".format(email_check[0].name,otp)
            send_mail('Forgot Password - Verification code', msg, settings.EMAIL_HOST_USER, [email_check[0].email])
            return redirect('verify_otp')
        else:
            messages.warning(request, "Email Id is Incorrect...! Try Again")
    return render(request, 'forgot_password.html')
 
def verify_otp(request):
    if request.method == 'POST':
        gen_otp = request.POST['otp']
        checking_otp = EmpPersonal.objects.filter(otp = gen_otp)
        if checking_otp:
            return redirect('changing_password',id=checking_otp[0].id)
        else:
            messages.warning(request, "OTP Verification Failed..! Please Enter Valid OTP, Try Again ")
    return render(request, 'verify_otp.html')

def changing_password(request,id):
    emp_info = EmpPersonal.objects.get(id = id)
    if request.method == "POST":
        password = request.POST['password']
        check_email = emp_info.email
        user_data = User.objects.get(email = check_email)
        user_data.set_password(password)
        user_data.save()
        return redirect('user_login')
    return render(request, "new_password.html")

class Hello_sample(View): #Get, Post, Update, Delete (Methods)
    def get(self, request):
        return HttpResponse("Hello World (Using Class)")

# Generic Views -- CreateView, List_view, Update_view, DeleteView, DetailView.

class EmpPer_cls(CreateView):
    model = EmpPersonal
   # template_name = "" Template can be rendered by using this Variable
   # fields = "__all__" 
    fields = ("name", "mobile", "email", "age", "address", "country", "document")
    success_url = reverse_lazy("hello_cls")
    def form_valid(self, form):
        #pdb.set_trace() For Debugging Purpose
        name = form.data.get('name')
        email = form.data.get('email')
        password = form.data.get('password')
        user_data = User.objects.create(username=name, email=email, is_staff=True, is_active=True)
        user_data.set_password(password)
        user_data.save()
        form_data = form.save(commit=False)
        form_data.user = user_data

        return super().form_valid(form)

class EmpPer_List(ListView):
    model = EmpPersonal
    template_name = "emppersonal_list.html"

class EmpPer_Update(UpdateView):
    model = EmpPersonal
    fields = ("name", "mobile", "email", "age", "address", "country", "document")
    success_url = reverse_lazy("hello_cls")

class EmpPer_Delete(DeleteView):
    model = EmpPersonal
    success_url = reverse_lazy("hello_cls")

class EmpPer_Detail(DetailView):
    model = EmpPersonal

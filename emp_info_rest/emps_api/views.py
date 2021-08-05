from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EmpPersonal
from django.core import serializers
from django.contrib.auth.models import User
from .serializers import EmpSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework import viewsets
# Create your views here.

@api_view(['GET','POST'])
def hello_api(request):
    if request.method == "GET":
        return Response({'message':'Hello world...!'})
    elif request.method == "POST":
        print(request)
        return Response(request.data)

@api_view(['GET','POST'])
def get_data(request):
    if request.method == "GET":
        emp_data = EmpPersonal.objects.all()
        print(emp_data)
        emp_data_value = []
        for ele in emp_data:
            data = {
                'name' : ele.name,
                'mobile' : ele.mobile,
                'email' : ele.email,
                'age' : ele.age,
                'address' : ele.address,
                'country' : ele.country,
            }
            emp_data_value.append(data)

        return Response(emp_data_value)
    elif request.method == "POST":
        # print(request.data)
        user_data = User(username=request.data.get('name'), email=request.data.get('email'), is_active=True, is_staff=True)
        user_data.set_password(request.data.get('password'))
        user_data.save()
        EmpPersonal.objects.create(name=request.data.get('name'), mobile=request.data.get('mobile'), email=request.data.get('email'), age=request.data.get('age'), address=request.data.get('address'), country=request.data.get('country'), user=user_data)
        return Response(request.data)

@api_view(['GET','PUT','DELETE'])
def get_single_data(request,id):
    try:
        emp_data = EmpPersonal.objects.get(id=id)
    except:
        return Response({"message": "User Data Not Exists...!Try Again"})
    if request.method == "GET":
        ser_data = EmpSerializer(emp_data)
        # data = {
        #         'name' : emp_data.name,
        #         'mobile' : emp_data.mobile,
        #         'email' : emp_data.email,
        #         'age' : emp_data.age,
        #         'address' : emp_data.address,
        #         'country' : emp_data.country,
        #         }
        return Response(ser_data.data)
    elif request.method == "PUT":
        #print(request.data)
        emp_data.name = request.data.get('name')
        emp_data.mobile = request.data.get('mobile')
        emp_data.email = request.data.get('email')
        emp_data.age = request.data.get('age')
        emp_data.address = request.data.get('address')
        emp_data.country = request.data.get('country')
        emp_data.save()
        return Response({'message' : "Data Updated Successfully"})
    elif request.method == "DELETE":
        print(emp_data.user.id)
        User.objects.get(id = emp_data.user.id).delete()
        emp_data.delete()
        return Response({"message":"Data Deleted Sucessfully..!"})

@api_view(['PUT'])
def change_password(request,id):
    try:
        emp_data = EmpPersonal.objects.get(id=id)
    except:
        return Response({"Message": "Data Not Exists..! Try Again"})

    if request.method == "PUT":
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password == confirm_password:
            user_data = User.objects.get(id = emp_data.user.id)
            user_data.set_password(password)
            user_data.save()
            return Response({"message":"Password Updated Sucessfully.."})
        else:
            return Response({"message":"Password Mismatched...! Try again"})


class EmpPersonalListView(APIView):
    def get(self, request):
        emp_data = EmpPersonal.objects.all()
        serializer = EmpSerializer(emp_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmpSerializer(data = request.data)
        if serializer.is_valid():
            print(serializer.data)
            user_data = User(username = serializer.data.get('name'), email= serializer.data.get('email'), is_active=True, is_staff=True)
            user_data.set_password(request.data.get('password'))
            user_data.save()
            EmpPersonal.objects.create(name=serializer.data.get('name'), mobile=serializer.data.get('mobile'), email=serializer.data.get('email'), age=serializer.data.get('age'), address=serializer.data.get('address'), country=serializer.data.get('country'), user = user_data)
            return Response({"message":"Data added Successfully"})
        return Response({"message":"Data is Not valid, Missing some Validations"})

class EmpDetailView(APIView):
    def get(self,request,id):
        emp_data = EmpPersonal.objects.get(id =id)
        serializer = EmpSerializer(emp_data)
        return Response(serializer.data)
    
    def put(self, request, id):
        emp_data = EmpPersonal.objects.get(id =id)
        serializer = EmpSerializer(emp_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Data Updated Successfully.."})
    
    def delete(self, request, id):
        emp_data = EmpPersonal.objects.get(id =id)
        User.objects.get(id=emp_data.user.id).delete()
        emp_data.delete()
        return Response({"message":"Deleted Successfully.."})

class EmpList_Generic(ListAPIView):
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

    # def get_queryset(self):
    #     data = EmpPersonal.objects.filter(age__gt=20)
    #     return data

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = EmpSerializer(queryset,many=True)
    #     return Response(serializer.data)

class EmpCreate_Generic(CreateAPIView):
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer
    
    def create(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user_data = User(username = serializer.data.get('name'), email= serializer.data.get('email'), is_active=True, is_staff=True)
            user_data.set_password(request.data.get('password'))
            user_data.save()
            EmpPersonal.objects.create(name=serializer.data.get('name'), mobile=serializer.data.get('mobile'), email=serializer.data.get('email'), age=serializer.data.get('age'), address=serializer.data.get('address'), country=serializer.data.get('country'), user = user_data)
            return Response({"message":"Data added Successfully"})
        return Response({"message":"Data is Not valid, Missing some Validations"})

class EmpRetrieve_Generic(RetrieveAPIView):
    lookup_field = 'id'  # It can  be anything like name,mobile...etc
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

class EmpUpdate_Generic(UpdateAPIView):
    lookup_field = 'id'
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

class EmpDelete_Generic(DestroyAPIView):
    lookup_field = 'id'
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

class EmpList_Create_Generic(ListCreateAPIView):
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

    def create(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user_data = User(username = serializer.data.get('name'), email= serializer.data.get('email'), is_active=True, is_staff=True)
            user_data.set_password(request.data.get('password'))
            user_data.save()
            EmpPersonal.objects.create(name=serializer.data.get('name'), mobile=serializer.data.get('mobile'), email=serializer.data.get('email'), age=serializer.data.get('age'), address=serializer.data.get('address'), country=serializer.data.get('country'), user = user_data)
            return Response({"message":"Data added Successfully"})
        return Response({"message":"Data is Not valid, Missing some Validations"})

class EmpRetrieve_Update_Generic(RetrieveUpdateAPIView):
    lookup_field = 'name'
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

class EmpRetrieve_Delete_Generic(RetrieveDestroyAPIView):
    lookup_field = 'name'
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

    def destroy(self, request, *args, **kwargs):
        print(self.get_object().name)
        User.objects.get(username=self.get_object().name).delete()
        return Response({"message":"Data Deleted Successfully"})

class EmpRetrieve_Delete_Update_Generic(RetrieveUpdateDestroyAPIView ):
    lookup_field = 'name'
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

@api_view(['POST'])
def user_send_email(request):
    if request.method == 'POST':
        email = request.data['email']
        email_check = User.objects.filter(email=email)
        if email_check:
            otp_save = EmpPersonal.objects.filter(email=email)
            otp = random.randint(000000, 999999)
            save_data = otp_save[0]
            save_data.otp = str(otp)
            save_data.save()
            msg = "Hi {},\n Below is the Verification code for Changing password {}".format(email_check[0].username,otp)
            send_mail('Forgot Password - Verification code', msg, settings.EMAIL_HOST_USER, [email_check[0].email])
            return redirect('verify_otp')
        else:
            return Response({"message" : "Email ID Invalid"})
#    return render(request, 'send_email.html')

@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        gen_otp = request.data['otp']
        check_otp = EmpPersonal.objects.filter(otp=gen_otp)
        if check_otp:
            return redirect('new_password',id = check_otp[0].id)
        else:
            return Response({"message" : "OTP Authentication Failed"})
#    return render(request, 'verify_otp.html')

@api_view(['POST'])
def new_password(request,id):
    emp_info = EmpPersonal.objects.get(id=id)
    if request.method == 'POST':
        password_ver = request.data['password']
        check_email = emp_info.email
        user_data = User.objects.get(email=check_email)
        user_data.set_password(password_ver)
        user_data.save()
    return Response({"message" : "Password Updated"})

class EmpViewset(viewsets.ModelViewSet):
    queryset = EmpPersonal.objects.all()
    serializer_class = EmpSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_data = User(username=request.data.get('name'),email=request.data.get('email'),is_active=True, is_staff=True)
        user_data.set_password(request.data.get('password'))
        user_data.save()
        EmpPersonal.objects.create(name=request.data.get('name'), mobile=request.data.get('mobile'), email=request.data.get('email'), age=request.data.get('age'), address=request.data.get('address'), country=request.data.get('country'), user=user_data)
        return Response({"message":"Employee Registered Successfully.."})


from django.shortcuts import render
from .models import *
from random import randint
from .utils import *


# Create your views here.

def LoginPage(request):
    return render(request,"doctorfinder/login.html")

def RegistrationPage(request):
    return render(request,'doctorfinder/registration.html')

def RegisterUser(request):
    try:
        if request.POST['role'] == 'doctor':
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            gender = request.POST['gender']
            email = request.POST['email']
            speciality = request.POST['speciality']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone'])

            user = User.objects.filter(email = email)
            if user:
                message = 'This email already exists'
                return render(request,'doctorfinder/registration.html',{'message':message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(email = email, password= password,role = role, otp = otp)  
                    newdoctor = Doctor.objects.create(user_id = newuser,firstname = firstname, lastname = lastname, gender = gender, speciality = speciality, city = city, mobile = mobile, birthdate = dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject,'mail_template',email,{'name':firstname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    return render(request,'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request,'doctorfinder/registration.html',{'message':message})

        else:
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirm']
            gender = request.POST['gender']
            email = request.POST['email']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone'])
            user = User.objects.filter(email = email)
            if user:
                message = 'This email already exists'
                return render(request,'doctorfinder/registration.html',{'message':message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(email = email, password= password,role = role, otp = otp)  
                    newpatient = Patient.objects.create(user_id = newuser,firstname = firstname, lastname = lastname, gender = gender, city = city, mobile = mobile, birthdate = dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject,'mail_template',email,{'name':firstname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    return render(request,'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request,'doctorfinder/registration.html',{'message':message})
    except User.DoesNotExist:
        message = 'This email already exists'
        return render(request,'doctorfinder/registration.html',{'message':message})

def login_evaluation(request):
    if request.POST['role'] == 'doctor':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email = email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'doctor':
                doctor = Doctor.objects.filter(user_id = user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = doctor[0].firstname
                return render(request,"doctorfinder/homepage-doctor.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request,"doctorfinder/login.html",{'message':message})
        else:
            message = "user doesn't exist"
            return render(request,"doctorfinder/login.html",{'message':message})
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email = email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'patient':
                patient = Patient.objects.filter(user_id = user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = patient[0].firstname
                return render(request,"doctorfinder/homepage-doctor.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request,"doctorfinder/login.html",{'message':message})
        else:
            message = "user doesn't exist"
            return render(request,"doctorfinder/login.html",{'message':message})

def forgot_password(request):
    return render(request,"doctorfinder/forgot_password.html")
def forgot_password_email(request):
    try:
        email = request.POST['email']

        user = User.objects.get(email = email)
        if user:
            otp = randint(100000, 9999999)
            user.otp=otp
            user.save()
            email_subject = "Your OTP For Forgot Password Is : "
            sendmail(email_subject,'mail_template',email,{'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
            return render(request,'doctorfinder/enterOTP.html',{'email':email})
        else:
            message = "Email Does Not Exist"
            return render(request,'doctorfinder/forgot_password.html',{'message':message})

    except User.DoesNotExist:
        message = 'This email does not exists'
        return render(request,'doctorfinder/forgot_password.html',{'message':message})

def reset_password(request):
    try:
        email = request.POST['email']
        otp=request.POST['otp']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        user = User.objects.get(email = email)
        print(type(user.otp))
        print(type(otp))
        print(password)
        print(confirmpassword)
        if user:
            if str(user.otp)==otp:
                print("otp")
                if password==confirmpassword:
                    print("pass")
                    user.password=password
                    user.save()
                    email_subject = "Your Password Updated Successfully "
                    sendmail(email_subject,'mail_template',email,'')
                    return render(request,'doctorfinder/login.html',{'email':email})
                else:
                    return render(request,'doctorfinder/enterOTP.html')
            else:
                return render(request,'doctorfinder/enterOTP.html')


        else:
            message = "Email Does Not Exist"
            return render(request,'doctorfinder/login.html',{'message':message})

    except User.DoesNotExist:
        message = 'This email does not exists'
        return render(request,'doctorfinder/login.html',{'message':message})
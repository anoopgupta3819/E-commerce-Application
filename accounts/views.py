from django.http.response import HttpResponse
from django.shortcuts import  redirect,render
from vendor.forms import vendorForm
from   .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from django.shortcuts import redirect



# Create your views here.

def registerUser(request):
        if request.user.is_authenticated:
              messages.warning(request,'You are already logged in!')
              return redirect('dashboard')
        elif request.method == 'POST':
                print(request.POST)
                form = UserForm(request.POST)
                if form.is_valid():
                        #create the user using  form



                    #=========================working good ================================== but checking new method
                    #password = form.cleaned_data['password']
                    #user = form.save(commit = False)
                    #user.set_password(password)
                    #user.role = user.CUSTOMER
                    #form.save()

                    #create  the user using  create_user method
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    email= form.cleaned_data['email']
                    password= form.cleaned_data['password']

                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.role = User.CUSTOMER
                    user.save()
                    messages.success(request,'Your account has been registered Sucessfully')
                   # print('user is created')
                    return redirect('registerUser')
        else :
               form = UserForm()
        context = { 
                'form': form,
        }
        return render(request,'accounts/registerUser.html',context)  

#def registerUser(request):
    #if request.mrthod == 'POST':
       # print(request.POST)
    #else:
       # form = UserForm() 
   # context = {
   # 'form': form,
   # }
    
    #return render(request,'accounts/registerUser.html',context) 

def registerVendor(request):
      if request.method =='POST':
             #store the data and create the user
             form = UserForm(request.POST)
             v_form = vendorForm(request.POST,request.FILES)
             if form.is_valid() and v_form.is_valid:
                     first_name = form.cleaned_data['first_name']
                     last_name = form.cleaned_data['last_name']
                     username = form.cleaned_data['username']
                     email= form.cleaned_data['email']
                     password= form.cleaned_data['password']
                     user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                     user.role = User.VENDOR
                     user.save()
                     vendor = v_form.save(commit=False)
                     vendor.user = user
                     user_profile = UserProfile.objects.get(user=user)
                     vendor.user_profile = user_profile
                     vendor.save()
                     messages.success(request,'Your account has been registered Sucessfully!Please wait for the approval.')
                     return redirect('registerVendor')
             
                    
                    
             else:
                    print('invalid form')
                    print(form.errors)
                    
      else:
            form = UserForm()
            v_form = vendorForm()
      context = {
             'form':form,
             'v_form':v_form,
      }
     
      return render(request,'accounts/registerVendor.html',context)

def login(request):
       if request.user.is_authenticated:
              messages.warning(request,'You are already logged in!')
              return redirect('dashboard')
       elif request.method =='POST':
              email = request.POST['email']
              password = request.POST['password']

              user = auth.authenticate(email=email,password=password)
              if user is not None:
                     auth.login(request,user)
                     messages.success(request,'You are now logged in.')
                     return redirect('dashboard')
              else:
                     messages.error(request,'Invalid login credentials')
                     return redirect('login')
       return render(request,'accounts/login.html')

def logout(request):
       auth.logout(request)
       messages.info(request,'You are logged out.')
       return redirect('login')

def myAccount(request):
       return redirect('')



def dashboard(request):
       return render(request,'accounts/dashboard.html')
 
 
 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,reverse
from django.views import View
from .forms import LoginForm, OtpLoginForm, CheckOtpForm,AddressCreationForm
import ghasedakpack
from random import randint
from .models import Otp
from uuid import uuid4
User = get_user_model()

SMS = ghasedakpack.Ghasedak("c22e62eff82dc6aaecff807ffe6fb633d856da0a748467a2869cb3d94729db71")


def user_login(request):
    return render(request, "account/login.html", {})


class UserLogin(View):

    def get(self,request):
        form = LoginForm()
        return render(request,'account/login.html',{'form':form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request,user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                form.add_error('phone','invalid username')
        else:
            form.add_error('phone','invalid data')
        return render(request,'account/login.html',{'form':form})

class OtpLoginView(View):
    def get(self,request):
        form = OtpLoginForm()
        return render(request, 'account/otp_login.html', {'form':form})

    def post(self,request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000,9999)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1':randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'],code=randcode,token=token)
            print(randcode)
            return redirect(reverse('account:user_checkotp') + f'?token={token}')
        else:
            form.add_error('phone','invalid data')
        return render(request, 'account/otp_login.html', {'form':form})


class CheckOtpView(View):

    def get(self,request):
        form = CheckOtpForm()
        return render(request,'account/checkotp.html',{'form':form})

    def post(self,request):
        token = request.GET.get('token', )
        form = CheckOtpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                    otp=Otp.objects.get(token=token)
                    user,is_created= User.objects.get_or_create(phone=otp.phone)
                    login(request,user,backend="django.contrib.auth.backends.ModelBackend")
                    otp.delete()
                    return redirect('/')

        else:
            form.add_error('phone','invalid data')
        return render(request,'account/checkotp.html',{'form':form})

class AddressAddView(View):
    def post(self,request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id  # Assuming you're using Django's built-in user authentication
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return render(request,'account/add_address.html',context={'form':form})

    def get(self,request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', context={'form': form})

def User_Logout(request):
    logout(request)
    return redirect('/')



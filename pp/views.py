from .models import GalleryModel
from .forms import GalleryForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import HttpResponse

# for creating register and login 
from .forms import RegisterForm, GalleryForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth import get_user_model, login, authenticate, logout
from .forms import LoginForm, SetPasswordForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required

from . models import GalleryModel

#sending mail
from django.core.mail import send_mail
from django.conf import settings
from .utils import file_link



def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            
            subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            recipient = [form.cleaned_data.get('email'),]
            from_email = settings.DEFAULT_FORM_EMAIL
            
            send_mail(subject, message, from_email, recipient)

            messageSent = True

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for your email confirmation")
    else:
        return HttpResponse("Activation link is invalid")



#function for login view
def login_view(request):
    form = LoginForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                # message = f'Hey {user.username}, you have entered safe zone'
                return redirect('home')

            else:
                message = f'Hey anonymous guy, Credentials are invalid!!'

    return render(request, 'login.html', context={'form' : form, 'message' : message})




def custom_logout(request):
    logout(request)
    return redirect("home")



def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form' :form})
 


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            associated_user = get_user_model().objects.filter(Q(email = user_email)).first()

            if associated_user:
                subject = "Password Reset Request"
                message = render_to_string("template_reset_password.html",{
                    'user' : associated_user,
                    'domain' : get_current_site(request).domain,
                    'uid' : urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token' : account_activation_token.make_token(associated_user),
                })
                recipient = [user_email]
                from_email = settings.DEFAULT_FORM_EMAIL
                sent = send_mail(subject, message, from_email, recipient )

               
            
            return redirect('home')
        

    form = PasswordResetForm()

    return render(request, 'password_reset.html', {'form': form})



def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.      DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
   

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")










def home_page(request):
    return render(request, 'index.html')


def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    return render(request, 'contact.html')


def fashion_page(request):
    return render(request, 'fashion.html')


def photography_page(request):
    return render(request, 'photography.html')


def single_page(request):
    return render(request, 'single.html')

def travel_page(request):
    return render(request, 'travel.html')



@login_required(login_url='login')
def gallery_page(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            file_name = form.cleaned_data.get('image')
            instance.link = file_link(file_name)
            instance.owner = request.user
            instance.save()
            return redirect('gallery')
        else:
            print(form.errors)  # Debug output for form validation errors
    else:
        form = GalleryForm()

    posts = GalleryModel.objects.all()
    context = {'form': form, 'posts': posts}
    return render(request, 'gallery.html', context)




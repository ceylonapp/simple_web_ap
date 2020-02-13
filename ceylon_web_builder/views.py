from user_module.models import WebUser
from .models import FaqModel, GuideLineModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.


def get_user_auth_details(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return username, password


def login_page(request):
    context = {}
    if request.method == "POST":
        username, password = get_user_auth_details(request)
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(f"/user/{username}")
        else:
            context["error"] = {
                "authentication_fail": True
            }
    return render(request, "login.html", context=context)


def create_account(request):
    if request.method == "POST":
        username, password = get_user_auth_details(request)
        is_user_exists = User.objects.filter(username=username).count() > 0
        if not is_user_exists:
            user = User.objects.create_user(username=username, password=password)
            ad_user = WebUser()
            ad_user.user = user
            ad_user.save()

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(f"/user/{username}")
        else:
            return render(request, "login.html", context={
                "error": {
                    "username_exist": True
                }
            })

    return render(request, "login.html")


def user_profile(request, username):
    context = {}
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")

        user = User.objects.get(id=request.user.id)
        ad_user = WebUser.objects.get(user_id=request.user.id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        context = {
            "username": username
        }
    if request.user and request.user.username == username:
        context["logged_user"] = True
        context["profile"] = WebUser.objects.get(user=request.user)

    return render(request, "user.html", context=context)


def logout_action(request):
    logout(request)
    return HttpResponseRedirect("/home")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


def password_reset_complete_view(request):
    return render(request, "password_reset_success.html", context={})


def forgot_password_page(request):
    errors = {}
    messages = {}
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()
        if user:
            email: str = user.email
            form = PasswordResetForm({'email': email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=True, from_email="admin@admalla.com")

        messages["success_message"] = "Password Reset instructions are sent to your email."

    return render(request, "forgotpasword.html", context={"errors": errors, "messages": messages})


def faq_view(request):
    context = {
        "faq_list": FaqModel.objects.filter(is_active=True).order_by("-order").all()
    }
    return render(request, "faq.html", context=context)


def guideline_view(request):
    context = {
        "guide_line_list": GuideLineModel.objects.filter(is_active=True).order_by("-order").all()
    }
    return render(request, "guide_line.html", context=context)


def home_page(request):
    return render(request, "index.html")


def submit_task(request):
    return render(request, "post.html")

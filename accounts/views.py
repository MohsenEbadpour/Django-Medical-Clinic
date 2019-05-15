from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .models import User, Sick, Doctor
from .forms import UserLoginForm, SignupForm, EditForm
from posts.models import Post
from turn.models import Shift, Turn
from .decorators import staff_required
# Create your views here.


def home(request):
    posts = Post.objects.all()
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(context__icontains=query)
        ).distinct()
    return render(request, "accounts/home.html", {"posts": posts})


@login_required
@staff_required
def doctor_management(request):
    all_doctors = Doctor.objects.all()
    doctors = []
    for doctor in all_doctors:
        doctors.append([doctor, Shift.objects.filter(doctor=doctor).count()])
    return render(request, "accounts/doctor-manage.html", {"doctors": doctors})


@login_required
@staff_required
def doctor_delete(request, id=None):
    doctor = get_object_or_404(Doctor, id=id)
    user = doctor.user
    doctor.delete()
    user.delete()
    messages.success(request, "دکتر مورد نظر با موفقیت حذف گردید")
    return HttpResponseRedirect(reverse("accounts:doctor-manage"))


@login_required
@staff_required
def sick_management(request):
    all_sick = Sick.objects.all()
    sicks = []
    for sick in all_sick:
        sicks.append([sick, Turn.objects.filter(sick=sick).count()])
    return render(request, "accounts/sick-manage.html", {"sicks": sicks})


@login_required
@staff_required
def sick_delete(request, id=None):
    sick = get_object_or_404(Sick, id=id)
    user = sick.user
    sick.delete()
    user.delete()
    messages.success(request, "بیمار مورد نظر با موفقیت حذف گردید")
    return HttpResponseRedirect(reverse("accounts:sick-manage"))


@login_required
@staff_required
def doctor_cash_list(request):
    all_doctors = Doctor.objects.all()
    doctors = []
    for doctor in all_doctors:
            total = 0
            for shift in Shift.objects.filter(doctor=doctor):
                total += shift.turn_set.filter(
                    is_passed=True).count()*shift.cash
            doctors.append([doctor, total])
            print(total)
    return render(request, "accounts/doctor-manage.html", {"doctors": doctors, "readonly": True})


@login_required
@staff_required
def sick_cash_list(request):
    all_sick = Sick.objects.all()
    sicks = []
    for sick in all_sick:
        sicks.append([sick, Turn.objects.filter(sick=sick).count()])
    return render(request, "accounts/sick-manage.html", {"sicks": sicks, "readonly": True})


@login_required
def account(request):
    return render(request, "accounts/account.html", {})


def login_function(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.user.get_url())
    form = UserLoginForm()
    if request.POST:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(email=form.clean_email())
            login(request, user)
            return HttpResponseRedirect(reverse("accounts:home"))
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_function(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:home"))


def signup_sick_function(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.user.get_url())

    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            sick = Sick()
            sick.name = form.cleaned_data.get('name')
            sick.id_number = form.cleaned_data.get('id_number')
            sick.phone = form.cleaned_data.get('phone')
            sick.user = user
            user.save()
            sick.save()
            user = authenticate(username=user.email,
                                password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, "ثبت نام شما با موفقیت انجام شد")
            return HttpResponseRedirect(reverse("accounts:account"))

    return render(request, "accounts/editorsignup.html", {"form": form, "sick": True})


def signup_doctor_function(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.user.get_url())
    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            doctor = Doctor()
            doctor.name = form.cleaned_data.get('name')
            doctor.id_number = form.cleaned_data.get('id_number')
            doctor.phone = form.cleaned_data.get('phone')
            doctor.user = user
            user.save()
            doctor.save()
            user = authenticate(username=user.email,
                                password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, "ثبت نام شما با موفقیت انجام شد")
            return HttpResponseRedirect(reverse("accounts:account"))

    return render(request, "accounts/editorsignup.html", {"form": form})


@login_required
def edit(request):
    user = request.user
    if hasattr(user, "staff"):
        instance = user.staff
    elif hasattr(user, "sick"):
        instance = user.sick
    else:
        instance = user.doctor

    form = EditForm()
    if request.POST:
        form = EditForm(request.POST or None)
        if form.is_valid():
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data.get('password'))
            instance.name = form.cleaned_data.get('name')
            instance.id_number = form.cleaned_data.get('id_number')
            instance.phone = form.cleaned_data.get('phone')
            user.save()
            instance.save()
            user_login = authenticate(username=form.cleaned_data.get(
                'email'), password=form.cleaned_data.get('password'))
            login(request, user_login)
            messages.success(request, "ویرایش شما با موفقیت انجام شد")
            return HttpResponseRedirect(reverse("accounts:account"))

    return render(request, "accounts/editorsignup.html", {"form": form, "readonly": True, "instance": instance})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from accounts.models import User, Sick, Doctor, Staff
from .models import Shift, Turn
from accounts.decorators import sick_required, doctor_required, staff_required
import datetime
from django.utils import timezone
from django.db.models import Sum

DATE_TIME_FORMAT = "%m/%d/%Y %H:%M %p"


def temp(request):
    return HttpResponse("<h1>Temp</h1>")


@login_required
@staff_required
def create_shift(request):
    if request.POST:
        shift = Shift()
        shift.doctor = get_object_or_404(
            Doctor, id=int(request.POST['doctor']))
        shift.cash = int(request.POST['cash'])
        shift.max_count = int(request.POST['max_count'])
        shift.room = str(request.POST['room'])
        shift.is_completed = False
        s = str(request.POST['start_date'])
        e = str(request.POST['end_date'])
        start = datetime.datetime.strptime(s, DATE_TIME_FORMAT)
        end = datetime.datetime.strptime(e, DATE_TIME_FORMAT)
        shift.start_date = start
        shift.end_date = end
        shift.save()
        messages.success(request, "ویزیت با موفقیت ایجاد گردید")
        return HttpResponseRedirect(reverse("turn:shift-manage"))

    doctors = Doctor.objects.all()
    return render(request, "turn/createoredit.html", {"doctors": doctors})


@login_required
@staff_required
def edit_shift(request, id=None):
    shift = get_object_or_404(Shift, id=id)
    shifts = Shift.objects.filter(end_date__lte=timezone.now())
    if shift in shifts :
    	return HttpResponseRedirect(reverse("turn:shift-manage"))
    if request.POST:
        s = str(request.POST['start_date'])
        e = str(request.POST['end_date'])
        start = datetime.datetime.strptime(s, DATE_TIME_FORMAT)
        end = datetime.datetime.strptime(e, DATE_TIME_FORMAT)
        shift.room = str(request.POST['room'])
        shift.start_date = start
        shift.end_date = end
        shift.save()
        messages.success(request, "شیفت با موفقیت ویرایش یافت")
        return HttpResponseRedirect(reverse("turn:shift-manage"))
    return render(request, "turn/createoredit.html", {"shift": shift, "readonly": True})


@login_required
@staff_required
def delete_shift(request,id=None):
	shift = get_object_or_404(Shift,id=id)
	shift.delete()
	messages.success(request, "شیفت با موفقیت حذف شد")
	return HttpResponseRedirect(reverse("turn:shift-manage"))

@login_required
@staff_required
def passed_shifts(request):
	shifts = Shift.objects.filter(end_date__lte=timezone.now())
	return render(request, "turn/passed.html", {"shifts": shifts})



@login_required
@staff_required
def manage(request):
    shifts = Shift.objects.filter(end_date__gte=timezone.now())
    return render(request, "turn/manage.html", {"shifts": shifts})

@login_required
@staff_required
def detail_shift(request,id=None):
	shift = get_object_or_404(Shift,id=id)
	turns = shift.turn_set.all()
	return render(request, "turn/detail.html", {"shift": shift,"turns":turns,"readonly":True})


@login_required
@sick_required
def shift_list_for_sick(request):
    shifts = Shift.objects.filter(
        is_completed=False, start_date__gte=timezone.now())
    turns = Turn.objects.filter(sick=request.user.sick)
    result = []
    for shift in shifts:
        if turns.filter(shift=shift).count() != 0:
            result.append([True, shift])
        else:
            result.append([False, shift])
    return render(request, "turn/shift_list_for_sick.html", {"shifts": result, "turns": result})




@login_required
@sick_required
def set_turn_for_sick(request, id=None):
    shift = get_object_or_404(Shift, id=id)
    if request.user.sick.cash < shift.cash:
        messages.success(request, "اعتبار حساب شما کم است")
        return HttpResponseRedirect(reverse("turn:list"))
    if not(shift.is_completed):
        turn = Turn(shift=shift, sick=request.user.sick)
        turn.save()
        user = request.user.sick
        user.cash -= shift.cash
        user.save()
        messages.success(request, "نوبت دهی با موفقیت انجام شد")
        if shift.turn_set.all().count() == shift.max_count:
            shift.is_completed = True
            shift.save()
    return HttpResponseRedirect(reverse("turn:list"))


@login_required
@sick_required
def passed_for_sick(request):
    turns = Turn.objects.filter(is_passed=True, sick=request.user.sick)
    return render(request, "turn/passed-sick.html", {"turns": turns})


@login_required
@sick_required
def load_for_sick(request):
    turns = Turn.objects.filter(is_passed=False, sick=request.user.sick)
    return render(request, "turn/load-sick.html", {"turns": turns})


@login_required
@sick_required
def increase_cash_for_sick_list(request):
    return render(request, "turn/increase-cash.html", {})


@login_required
@sick_required
def increase_cash_for_sick(request, amount=None):
    user = request.user.sick
    user.cash += amount
    user.save()
    messages.success(request, "اعتبار شما با موفقیت افزایش یافت")
    return HttpResponseRedirect(reverse("turn:cash-increase"))


@login_required
@sick_required
def cash_for_sick(request):
    turns = Turn.objects.filter(sick=request.user.sick)
    total = 0
    for turn in turns:
        total += turn.shift.cash
    return render(request, "turn/cash-list.html", {"turns": turns, "total": total})


@login_required
@doctor_required
def cash_for_doctor(request):
    shifts = Shift.objects.filter(doctor=request.user.doctor)
    total = 0
    turns = []
    for shift in shifts:
        for turn in shift.turn_set.filter(is_passed=True):
            total += int(shift.cash)
            turns.append(turn)
    return render(request, "turn/cash-list.html", {"turns": turns, "total": total, "doctor": True})


@login_required
@doctor_required
def passed_for_doctor(request):
    shifts = Shift.objects.filter(doctor=request.user.doctor)
    turns = []
    for shift in shifts:
        for turn in shift.turn_set.filter(is_passed=True):
            turns.append(turn)
    return render(request, "turn/passed-sick.html", {"turns": turns, "doctor": True})


@login_required
@doctor_required
def shift_list_for_doctor(request):
    shifts = Shift.objects.filter(end_date__gte=timezone.now(),doctor=request.user.doctor)
    return render(request, "turn/shift_list_for_doctor.html", {"shifts": shifts})


@login_required
@doctor_required
def take_visite(request, id=None):

    if request.POST:

        shift = Shift.objects.get(id=request.POST['shift'])
        doctor = Doctor.objects.get(id=request.POST['doctor'])
        turn = Turn.objects.get(id=request.POST['turn'])
        sick = Sick.objects.get(id=request.POST['sick'])
        if (doctor != request.user.doctor) or (shift.doctor != doctor) or (turn.shift != shift) or (turn.sick != sick) or (turn.shift != shift):
            raise Http404()
        turn.reason = str(request.POST['reason'])
        turn.note = str(request.POST['note'])
        turn.is_passed = True
        turn.save()
        doctor.cash+=shift.cash
        doctor.save()
    shift = get_object_or_404(Shift, id=id)
    if shift.doctor != request.user.doctor:
        raise Http404()

    turn = shift.turn_set.filter(is_passed=False).order_by('id').first()
    if turn is None:
        messages.success(
            request, "بیماری برای ویزیت وجود ندارد / ویزیت همه بیمارها تمام شده است")
        return HttpResponseRedirect(reverse("turn:doctor-shifts"))
    sick = turn.sick
    turns = Turn.objects.filter(is_passed=True, sick=sick)
    return render(request, "turn/visite-doctor.html", {"shift": shift, "turn": turn, "sick": sick, "turns": turns})

from django.db import models
from django.conf import settings
from django.apps import apps
from accounts.models import Staff, Doctor, Sick
from django.urls import reverse

from django.db.models.signals import pre_save
from django.dispatch import receiver


class Shift(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    room = models.CharField(max_length=200)
    cash = models.PositiveIntegerField()
    max_count = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(str(self.doctor)+" - "+str(self.start_date.date()) + " - " + str(self.start_date.time()))

    def get_url(self):
        return reverse("turn:shift", kwargs={"id": self.id})


class Turn(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    sick = models.ForeignKey(Sick, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200,blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_passed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(str(self.shift.doctor) + " - " + str(self.sick))

    def get_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})


@receiver(pre_save, sender=Shift)
def PRE_SAVE(sender, instance, *args, **kwargs):
    if instance.start_date > instance.end_date:
        instance.start_date, instance.end_date = instance.end_date, instance.start_date


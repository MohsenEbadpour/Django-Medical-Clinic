from django.db import models
from django.conf import settings 
from django.apps import apps
from accounts.models import Staff
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	context = models.TextField()
	date = models.DateTimeField(auto_now=True)
	hashtags = models.CharField(max_length=200)
	staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
	is_published = models.BooleanField(default=True)

	class Meta :
		ordering = ['-id']

	def __str__(self):
		return str(self.title)
		
	def get_url(self):
		return reverse("posts:detail",kwargs={"id":self.id})


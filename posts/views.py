from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.conf import Settings
from accounts.decorators import staff_required
from .forms import PostForm
from .models import Post


@login_required
@staff_required
def post_create(request):
	if request.POST:
		form = PostForm(request.POST or None)
		post = Post(title=request.POST.get('title'),context=request.POST['context'],hashtags=request.POST.get('hashtags'))
		if request.POST.get('is_published'):
			post.is_published = True
		else :
			post.is_published = False
		post.staff = request.user.staff
		post.save()
		return HttpResponseRedirect(reverse("posts:detail",kwargs={"id": post.id}))
	return render(request,"posts/createoredit.html",{})
	



def post_detail(request,id=None):
	post = get_object_or_404(Post,id=id)
	if not(post.is_published) and not(hasattr(request.user, "staff")):
		raise Http404
	return render(request,"posts/detail.html",{"post":post,"hashtags":list(str(post.hashtags).split())})
	

@login_required
@staff_required
def post_edit(request,id=None):
	post = get_object_or_404(Post,id=id)
	if request.POST:
		form = PostForm(request.POST or None)
		post.title = request.POST.get('title')
		post.context = request.POST['context']
		post.hashtags = request.POST.get('hashtags')
		if request.POST.get('is_published'):
			post.is_published = True
		else :
			post.is_published = False
		post.staff = request.user.staff
		post.save()
		messages.success(request,"تغییرات شما با موفقیت ذخیره شد")
		return HttpResponseRedirect(reverse("posts:detail",kwargs={"id": post.id}))
	return render(request,"posts/createoredit.html",{"post":post , "readonly":True})


@login_required
@staff_required
def post_delete(request,id=None):
	post = get_object_or_404(Post,id=id)
	post.delete()
	return redirect("posts:archives")


def post_archives(request):
	posts = Post.objects.all()
	return render(request,"posts/archives.html",{"posts":posts })
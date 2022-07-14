from django.shortcuts import  render, redirect
from .forms import NewUserForm, LinkForm
from .models import Link
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pyshorteners

s = pyshorteners.Shortener()

def homepage(request):
	print(request.user)
	context = {"links": Link.objects.filter(author = request.user)}
	return render(request, "links/home.html", context)

def shortener(request):
	if request.method == "POST":
		link_form = LinkForm(request.POST)
		if link_form.is_valid():
			new_link = link_form.save(commit=False)
			new_link.author = request.user
			new_link.short = s.tinyurl.short(link_form["original"].value())
			new_link.save()
			messages.success(request, ("Link was shortened and added to your storage!"))
		else:
			messages.error(request, "Error saving form")
		
		
		return redirect("links:homepage")
	link_form = LinkForm()
	links = Link.objects.all()
	return render(request=request, template_name="links/shortener.html", context={'link_form':link_form, 'links':links})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("links:homepage")
		messages.error(request, "Invalid data.")
	form = NewUserForm()
	return render (request=request, template_name="links/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Logged in as {username}.")
				return redirect("links:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="links/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Logged out.") 
	return redirect("links:login")
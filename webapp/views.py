from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.base import View
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from webapp.models import Store, StoreCategory, ProductCategory, BlogPost, BlogTopic, Offer, Profile, StoreBookmark, OfferBookmark
from django.urls import reverse
from django.contrib import auth
from webapp.forms import UserForm
import json

def homeView(request):
	if request.method=='POST':
		pk=request.POST.get('store')[0]
		# store=Store.objects.get(pk=pk)
		# print(store.home_url)
		return redirect(reverse('store-details', kwargs={'pk' : pk, }))
	return render(request, 'index.html', {
			'shoppingStores':Store.objects.all()[:4],
		})

def aboutView(request):
	return render(request, 'about.html', {})

def teamView(request):
	return render(request, 'team.html', {})

def contactView(request):
	return render(request, 'contact.html', {})

def categoryView(request, catId):
	category=ProductCategory.objects.get(catId=catId)
	return render(request, 'stores-list.html', {'category': category})

def categoryListView(request):
	return render(request, 'categories.html', {'categories': StoreCategory.objects.all(),'eCat':ProductCategory.objects.get(catId='electronics')})

def storeDetailView(request, pk):
	return render(request, 'store-details.html', {'store': Store.objects.get(pk=pk)})

def gallaryView(request):
	return render(request, 'gallery.html',{})

def blogListView(request):
	return render(request, 'blogs.html', {'blog_list' :BlogPost.objects.all()})

def blogDetailView(request, pk):
	return render(request, 'blog-details.html', {'blog':BlogPost.objects.get(pk=pk)})

def signupView(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form=UserCreationForm()
	return render(request, 'signup.html', {'form':form})

def loginView(request):
	return render(request, 'login.html', {})

def logoutView(request):
	logout(request)
	return redirect('home')

def favouriteStoresView(request, pk):
	pass

def addFavouriteOfferView(request, pk):
	pass

# Class Base Views
class UserProfileView(DetailView):
	model=Profile
	context_object_name='user_profile'
	template_name='user_profile.html'

	def get_context_data(self, **kwargs):
		context=super(UserProfileView, self).get_context_data(**kwargs)
		return context

class UserProfileUpdateView(UpdateView):
	model=User
	fields=['username', 'first_name', 'last_name', 'email']
	context_object_name='user'
	template_name='user_profile_edit.html'
	
	def get_context_data(self, **kwargs):
		context=super(UserProfileUpdateView, self).get_context_data(**kwargs)
		context['password_change_form']=PasswordChangeForm(user=self.request.user)
		# context['user_change_form']=UserForm(insance=self.request.user)
		return context
	
	def get_absolute_url(self):
		return reverse('update-user-profile', kwargs={'pk':self.get_object().pk})

	def form_valid(self, form):
		if form.is_valid():
			form.save()
			messages.success(self.request, 'Your changes successfully updated!')
		else:
			messages.error(self.request, 'Please correct the error below.')
		return super(UserProfileUpdateView, self).form_valid(form)

class OfferListView(ListView):
	moderl=Offer
	template_name='store-details.html'
	context_object_name="offers"
	paginate_by=9

	def get_queryset(self):
		try:
			return Offer.objects.filter(store__pk=self.kwargs.get('pk'))
		except Exception as e:
			raise e

	def get_context_data(self, **kwargs):
		context=super(OfferListView, self).get_context_data(**kwargs)
		context['store']=Store.objects.get(pk=self.kwargs.get('pk'))
		return context

class StoreListView(ListView):
	model=Store
	context_object_name="stores"
	template_name='stores-list.html'
	paginate_by=9

	def get_queryset(self):
		cat=ProductCategory.objects.get(pk=self.kwargs.get('pk'))
		return cat.stores.all()

	def get_context_data(self, **kwargs):
		context=super(StoreListView, self).get_context_data(**kwargs)
		context['category']=ProductCategory.objects.get(pk=self.kwargs.get('pk'))
		return context

class StoreBookmarkView(View):
	model=StoreBookmark

	def post(self, request, pk):
		user=auth.get_user(request)
		# Trying to get a bookmark from the table, or create a new one
		bookmark, created = self.model.objects.get_or_create(user=user, store_id=pk)
		# If no new bookmark has been created,
		# Then we believe that the request was to delete the bookmark
		if not created:
			bookmark.delete()
		return HttpResponse(json.dumps({
				"result":created,
				"count": self.model.objects.filter(store_id=pk).count()
			}), content_type="application/json")

class OfferBookmarkView(View):
	model=OfferBookmark

	def post(self, request, pk):
		user=auth.get_user(request)
		# Trying to get a bookmark from the table, or create a new one
		bookmark, created = self.model.objects.get_or_create(user=user, offer_id=pk)
		# If no new bookmark has been created,
		# Then we believe that the request was to delete the bookmark
		if not created:
			bookmark.delete()
		return HttpResponse(json.dumps({
				"result":created,
				"count": self.model.objects.filter(offer_id=pk).count()
			}), content_type="application/json")

class FavouriteStoresView(DetailView):
	model=User
	template_name='user_favourite_stores.html'
	context_object_name='store'

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context=super(FavouriteStoresView, self).get_context_data()
		return context

class FavouriteOffersView(DetailView):
	model=User
	template_name='user_favourite_offers.html'
	context_object_name='user'

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context=super(FavouriteOffersView, self).get_context_data(**kwargs)
		return context

class ApprovedDonationsView(DetailView):
	model=User
	template_name='approved_user_donations.html'
	context_object_name='user'

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context=super(ApprovedDonationsView, self).get_context_data()
		return context

class PendingDonationsView(DetailView):
	model=User
	template_name='pending_user_donations.html'
	context_object_name='store'

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context=super(PendingDonationsView, self).get_context_data()
		return context


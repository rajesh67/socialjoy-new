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
from webapp.models import Store, Category, BlogPost, BlogTopic, Offer, Profile, StoreBookmark, OfferBookmark
from django.urls import reverse
from django.contrib import auth
from webapp.forms import UserForm
import json
from search.documents import StoreDocument, OfferDocument
from itertools import chain

def homeView(request):
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
	category=Category.objects.get(catId=catId)
	return render(request, 'stores-list.html', {'category': category})

def categoryListView(request):
	return render(request, 'categories.html', {'categories': StoreCategory.objects.all(),'eCat':Category.objects.get(catId='electronics')})

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
			if 'catId' in self.request.GET.keys():
				catId=self.request.GET.get('catId')
				cat=Category.objects.get(catId=catId)
				return Offer.objects.filter(store__pk=self.kwargs.get('pk'), category=cat)
			else:
				return Offer.objects.filter(store__pk=self.kwargs.get('pk'))
		except Exception as e:
			raise e
	def get_offers_categories(self, store):
		cats=[]
		try:
			for off in store.offers.all():
				cat=Category.objects.get(name=off.category.name)
				cats.append(cat)
			return set(cats)
		except Exception as e:
			pass

	def get_context_data(self, **kwargs):
		context=super(OfferListView, self).get_context_data(**kwargs)
		context['store']=Store.objects.get(pk=self.kwargs.get('pk'))
		context['cats_list']=self.get_offers_categories(context['store'])
		return context

class StoreListView(ListView):
	model=Store
	context_object_name="stores"
	template_name='stores-list.html'
	paginate_by=9

	def get_queryset(self):
		cat=Category.objects.get(pk=self.kwargs.get('pk'))
		return cat.stores.all()

	def get_context_data(self, **kwargs):
		context=super(StoreListView, self).get_context_data(**kwargs)
		context['category']=Category.objects.get(pk=self.kwargs.get('pk'))
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

class StoreSearchView(ListView):
	model=Store
	context_object_name="stores_list"
	template_name="stores.html"
	paginate_by=24

	def get_queryset(self):
		q=self.request.GET.get('q')
		if q:
			return StoreDocument.search().filter("match", name=q).to_queryset()
		return super(StoreSearchView, self).get_queryset()

	def get_context_data(self, **kwargs):
		context=super(StoreSearchView, self).get_context_data(**kwargs)
		context['cats_list']=Category.objects.all()
		return context

	def search_stores_by_category(self, categoryId):
		store_qs_catId=StoreDocument.search().filter("match", categoryId=categoryId).to_queryset()
		stores_chain=chain(store_qs_catId)
		store_results=sorted(stores_chain, key=lambda instance: instance.pk, reverse=True )
		# print("Found %s Stores for %s "%(stores_chain, q))
		return render(self.request, 'stores.html',{
				'stores_list' : store_results,
				'cats_list' : Category.objects.all()
			})

	def search_stores(self, keywords):
		# store_qs_desc=StoreDocument.search().filter("match", description=keywords).to_queryset()
		store_results=StoreDocument.search().filter("match", name=keywords).to_queryset()
		# print("Found %s Stores for %s "%(stores_chain, q))
		return render(self.request, 'stores.html',{
				'stores_list' : store_results,
				'cats_list' : Category.objects.all()
			})

class OfferSearchView(ListView):
	model=Offer
	context_object_name='offers_list'
	paginate_by=24
	template_name='offers.html'

	def get_queryset(self):
		q=self.request.GET.get('q')
		if q:
			qs=OfferDocument.search().filter("match", title=q).to_queryset()
			return qs
		return super(OfferSearchView, self).get_queryset()

	def get_context_data(self, **kwargs):
		context=super(OfferSearchView, self).get_context_data(**kwargs)
		context['cats_list']=Category.objects.all()
		return context

	def search_offers(self, keywords):
		# qs_desc=OfferDocument.search().filter("match", description=keywords).to_queryset()
		qs_name=OfferDocument.search().filter("match", title=keywords).to_queryset()
		offer_chain=chain(qs_name)
		offer_results=sorted(offer_chain, key=lambda instance: instance.pk, reverse=True )
		# print("Found %s Stores for %s "%(stores_chain, q))
		return render(self.request, 'offers.html',{
				'offers_list' : offer_results,
				'cats_list' : Category.objects.all()
			})

class CategoryWiseStoreListView(ListView):
	model=Store
	template_name='stores.html'
	context_object_name="stores_list"
	paginate_by=12

	def get_queryset(self):
		try:
			cat=Category.objects.get(pk=self.kwargs.get('pk'))
			return cat.store_set.all()
		except Exception as e:
			raise e

	def get_context_data(self, **kwargs):
		context=super(CategoryWiseStoreListView, self).get_context_data(**kwargs)
		context['cats_list']=Category.objects.all()
		return context
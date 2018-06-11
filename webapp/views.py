from django.shortcuts import render, render_to_response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from webapp.models import Store, StoreCategory, ProductCategory, BlogPost, BlogTopic

def homeView(request):
	return render(request, 'index.html', {
			'shoppingStores':Store.objects.all()[:4]
		})

def aboutView(request):
	return render(request, 'about.html', {})

def teamView(request):
	return render(request, 'team.html', {})

def contactView(request):
	return render(request, 'contact.html', {})

def categoryView(request, catName):
	category=ProductCategory.objects.get(catId=catName)
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

# Class Base Views
class OfferListView(ListView):
	pass


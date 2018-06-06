from django.conf.urls import url, include
from webapp import views

urlpatterns=[
	url(r'^$', views.homeView, name="home"),
	url(r'^about-us/$', views.aboutView, name="about-us"),
	url(r'^team/$', views.teamView, name="team"),
	url(r'^gallery/$', views.gallaryView, name="gallery"),
	url(r'^contact-us/$', views.contactView, name="contact-us"),
	url(r'^all/$', views.categoryListView, name="category-list"),
	url(r'^categories/(?P<catName>[a-zA-Z-_0-9]+)/$', views.categoryView, name="stores-list"),
	url(r'^stores/(?P<pk>[0-9]+)/$', views.storeDetailView, name="store-details"),

	url(r'^blogs/$', views.blogListView, name="blog-list"),
	url(r'^blogs/(?P<pk>[0-9]+)/$', views.blogDetailView, name="blog-details"),
]
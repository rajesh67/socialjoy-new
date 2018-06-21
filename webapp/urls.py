from django.conf.urls import url, include
from webapp import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns=[
	url(r'^store/(?P<pk>\d+)/bookmark/$', login_required(views.StoreBookmarkView.as_view()), name="bookmark-store"),
	url(r'^offer/(?P<pk>\d+)/bookmark/$', login_required(views.OfferBookmarkView.as_view()), name="bookmark-offer"),
	url(r'^signup/$', views.signupView, name="signup"),
	url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
	url(r'^logout/$', views.logoutView, name="logout"),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserProfileView.as_view(), name="user-profile"),
	url(r'^users/(?P<pk>[0-9]+)/edit/$', views.UserProfileUpdateView.as_view(), name="update-user-profile"),
	
	url(r'^donations/approved/$', login_required(views.ApprovedDonationsView.as_view()), name="user-approved-donations"),
	url(r'^donations/pending/$', login_required(views.PendingDonationsView.as_view()), name="user-pending-donations"),

	url(r'^favourites/stores/$', login_required(views.FavouriteStoresView.as_view()), name="user-favourite-stores"),
	url(r'^favourites/offers/$', login_required(views.FavouriteOffersView.as_view()), name="user-favourite-offers"),

	url(r'^favourites/stores/(?P<pk>[0-9]+)/$', views.OfferListView.as_view(), name="add-favourite-stores"),
	url(r'^favourites/offers/(?P<pk>[0-9]+)/$', views.OfferListView.as_view(), name="add-favourite-offers"),

	url(r'^$', views.homeView, name="home"),
	url(r'^about-us/$', views.aboutView, name="about-us"),
	url(r'^team/$', views.teamView, name="team"),
	url(r'^gallery/$', views.gallaryView, name="gallery"),
	url(r'^contact-us/$', views.contactView, name="contact-us"),
	url(r'^all/$', views.categoryListView, name="category-list"),
	url(r'^categories/(?P<pk>[0-9]+)/$', views.StoreListView.as_view(), name="stores-list"),
	url(r'^stores/(?P<pk>[0-9]+)/$', views.OfferListView.as_view(), name="store-details"),
	# url(r'^stores/(?P<pk>[0-9]+)/offers/$', views.StoreOffersFilterView.as_view(), name="store-offers-filter"),

	url(r'^stores/$', views.StoreSearchView.as_view(), name="store-search"),
	url(r'^stores/categories/(?P<pk>[0-9]+)/$', views.CategoryWiseStoreListView.as_view(), name="cat-store-list"),
	url(r'^offers/$', views.OfferSearchView.as_view(), name="offer-search"),

	url(r'^blogs/$', views.blogListView, name="blog-list"),
	url(r'^blogs/(?P<pk>[0-9]+)/$', views.blogDetailView, name="blog-details"),
]
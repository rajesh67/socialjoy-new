from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
import datetime

class Store(models.Model):
	name=models.CharField(max_length=100, null=True, blank=True)
	short_name=models.CharField(max_length=10, null=True, blank=True)
	home_url=models.URLField(max_length=150, null=True, blank=True)
	description=models.TextField(null=True, blank=True)
	affiliate_id=models.CharField(max_length=100, null=True, blank=True)
	affiliate_token=models.CharField(max_length=250, null=True, blank=True)
	logo_image=models.ImageField(upload_to='stores/', null=True)
	aff_name=models.CharField(max_length=128, null=True, blank=True)
	featured=models.BooleanField(default=False)
	categories=models.ManyToManyField('Category')
	
	def __str__(self):
		return self.aff_name

	def get_bookmark_count(self):
		return self.storebookmark_set().all().count()

	def get_similar_stores(self):
		cat=self.categories.last()
		if cat:
			return cat.store_set.all().exclude(pk=self.pk)[:3]
		return None

class Category(models.Model):
	catId=models.CharField(max_length=30, null=True, blank=True)
	name=models.CharField(max_length=30)

	def __str__(self):
		return self.name

	def get_featured_stores(self):
		return self.stores.filter(featured=True)

	def get_top_stores(self):
		return self.store_set.all()[:5]

class Offer(models.Model):
	offerId=models.CharField(max_length=10)
	title=models.CharField(max_length=1024, null=True)
	description=models.TextField(blank=True, null=True)
	terms=models.TextField(blank=True, null=True)
	coupoun_code=models.CharField(max_length=50, null=True, blank=True)
	url=models.URLField(max_length=2500, null=True)
	status=models.CharField(max_length=10, null=True)
	startTime=models.DateTimeField(null=True)
	endTime=models.DateTimeField(null=True)
	imageUrl=models.URLField(max_length=2500, null=True)

	store=models.ForeignKey('Store', related_name="offers", on_delete=models.CASCADE, null=True)
	category=models.ForeignKey('Category', related_name='offers', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.title

	def get_bookmark_count(self):
		return self.offerbookmark_set().all().count()

	def get_category_name(self):
		if self.category:
			return self.category.catId
		return "None"

	def get_store_name(self):
		if self.store:
			return self.store.name
		return "None"


class OfferUpdate(models.Model):
	updated_on=models.DateTimeField(default=datetime.datetime.now())
	category=models.OneToOneField('Category', related_name="offerUpdate", on_delete=models.CASCADE)
	offers_file=models.FileField(upload_to='get_upload_path')

	def get_upload_path(self):
		return 'offers/cuelinks/%s/'%self.category.catId

	def __str__(self):
		return self.updated_on.date

# 
@receiver(post_save, sender=OfferUpdate)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		# Create / Update  All Offers In the Uploaded File
		pass
	instance.save()

class StoreBookmark(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	store=models.ForeignKey(Store, on_delete=models.CASCADE)

class OfferBookmark(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	offer=models.ForeignKey(Offer, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image=models.ImageField(upload_to='users/', null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

#----------------Our Services Cotents ----------------------


#---------------------Blogs -------------------------------
class BlogTopic(models.Model):
	name=models.CharField(max_length=30)

	def __str__(self):
		return self.name

class BlogPost(models.Model):
	POST_STATUS=(
		(0, 'Draft'),
		(1, 'Published')
	)
	status=models.IntegerField(choices=POST_STATUS, default=0)
	coverImage=models.ImageField(upload_to='blogs/', null=True)
	title=models.CharField(max_length=2048)
	subTitle=models.CharField(max_length=1048)
	shortDescription=models.TextField()
	description=models.TextField()
	posted_on=models.DateTimeField(default=datetime.datetime.now())
	tags=models.ManyToManyField('BlogTopic', related_name="blog_topics")
	
	user=models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title



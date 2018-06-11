from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime

class StoreCategory(models.Model):
	name=models.CharField(max_length=128)

	def __str__(self):
		return self.name

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
	parent_cats=models.ManyToManyField('StoreCategory', related_name='stores')

	def __str__(self):
		return self.aff_name

class ProductCategory(models.Model):
	catId=models.CharField(max_length=30, null=True, blank=True)
	name=models.CharField(max_length=30)
	stores=models.ManyToManyField('Store', related_name="categories", null=True, blank=True)

	def __str__(self):
		return self.name

	def get_featured_stores(self):
		return self.stores.filter(featured=True)

	def get_top_stores(self):
		return self.stores.all()[:5]

class Offer(models.Model):
	offerId=models.CharField(max_length=10)
	title=models.CharField(max_length=1024)
	description=models.TextField(blank=True, null=True)
	terms=models.TextField(blank=True, null=True)
	coupoun_code=models.CharField(max_length=50, null=True, blank=True)
	url=models.URLField(max_length=2500)
	status=models.CharField(max_length=10)
	startTime=models.DateTimeField(null=True)
	endTime=models.DateTimeField(null=True)
	imageUrl=models.URLField(max_length=2500)

	store=models.ForeignKey('Store', related_name="offers", on_delete=models.CASCADE, null=True)
	category=models.ForeignKey('ProductCategory', related_name='offers', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.title

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



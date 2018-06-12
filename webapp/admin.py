from django.contrib import admin

# Register your models here.
from webapp.models import StoreCategory, Store, ProductCategory, Offer
from django_summernote.admin import SummernoteModelAdmin
from webapp.models import BlogPost, BlogTopic, Profile

class BlogPostAdmin(SummernoteModelAdmin):
	summernote_fields='__all__'

admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(BlogTopic)
admin.site.register(StoreCategory)
admin.site.register(Store)
admin.site.register(ProductCategory)
admin.site.register(Offer)

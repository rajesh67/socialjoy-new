from django.contrib import admin

# Register your models here.
from webapp.models import StoreCategory, Store, ProductCategory, Offer

admin.site.register(StoreCategory)
admin.site.register(Store)
admin.site.register(ProductCategory)
admin.site.register(Offer)

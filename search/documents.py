from django_elasticsearch_dsl import Index, DocType, fields
from webapp.models import Store, Offer, Category

#=============================Store Index =========================================
#Name of Elastic Search Index
store=Index('stores')
# See Elasticsearch Indices API reference for available settings
store.settings(
	number_of_shards=1,
	number_of_replicas=0
)

@store.doc_type
class StoreDocument(DocType):
	class Meta:
		model=Store #he model associated with this DocTyp
		fields=[
			"id",
			"name",
			"home_url",
			"description",
			"logo_image",
			"featured",
			"aff_name",
		]

#==============================Offers Index =======================================
offer=Index('offers')
offer.settings(
	number_of_shards=1,
	number_of_replicas=0,
)

@offer.doc_type
class OfferDocument(DocType):
	categoryId=fields.TextField(attr='get_category_name')
	storeName=fields.TextField(attr='get_store_name')
	class Meta:
		model=Offer
		fields=[
			"offerId",
			"title",
			"description",
			"coupoun_code",
			"url",
			"status",
			"imageUrl",
		]
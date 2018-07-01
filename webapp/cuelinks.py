import datetime
import csv
from webapp.models import (
	Store,
	Offer,
	Category,
)

STORE_OFFERS_DATA_FILES='offers/{storeName}/{catId}/{date}.csv'

class CuelinksOffersHandler():

	def __init__(self, *args, **kwargs):
		return super(CuelinksOffersHandler, self).__init__(*args, **kwargs)

	def read_offers_csv(self, catId):
		self.catId=catId
		date=datetime.datetime.now().date().strftime('%d-%m-%y')
		fileName=STORE_OFFERS_DATA_FILES.format(storeName='cuelinks', date=date, catId=catId)
		offers=[]
		with open(fileName, 'r') as f:
			reader=csv.reader(f, delimiter=',')
			for line in reader:
				offers.append(line)
			f.close()
		return offers[1:]

	def create_offer(self, offer_data, catId):
		offer, created=Offer.objects.get_or_create(offerId=offer_data[0])
		if created:
			offer.title=offer_data[1]
			offer.store, created=Store.objects.get_or_create(aff_name=offer_data[2])
			offer.category, new=Category.objects.get_or_create(name=offer_data[3])

			offer.description=offer_data[4]
			offer.terms=offer_data[5]
			offer.coupoun_code=offer_data[6]
			offer.url=offer_data[7]
			offer.status=offer_data[8]
			offer.startTime=datetime.datetime.strptime(offer_data[9], '%Y-%m-%d')
			offer.endTime=datetime.datetime.strptime(offer_data[10], '%Y-%m-%d')
			offer.imageUrl=offer_data[12]
			offer.save()
		return offer

	def save_offers(self, offersList):
		offers=[]
		for offer in offersList:
			# print(offer)
			off, created=Offer.objects.get_or_create(
				offerId=int(offer[0])
			)
			if created:
				if offer[9]:
					off.startTime=datetime.datetime.strptime(offer[9], '%Y-%m-%d'),
				if offer[10]:
					off.endTime=datetime.datetime.strptime(offer[10], '%Y-%m-%d')
				off.title=str(offer[1])
				# off.categories=offer[3]
				# off.description=offer[4]
				# off.terms=str(offer[5])
				off.coupoun_code=str(offer[6])
				off.url=str(offer[7])
				off.status=str(offer[8])
				off.imageUrl=str(offer[12])
				print("Created Basic Info")
				off.store=Store.objects.get(aff_name=str(offer[2]))
				print("Store Added")
				off.category=Category.objects.get(catId=str(self.catId))
				print("Category Added")
				off.save()
			offers.append(off)
		return offers
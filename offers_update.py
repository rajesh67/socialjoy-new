import json
import csv
import datetime

from webapp.models import (
	Store, Category, Offer
)

def create_offer(offer_data, catId):
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
		offer.startTime=datetime.datetime.strptime(offer[9], '%Y-%m-%d')
		offer.endTime=datetime.datetime.strptime(offer[10], '%Y-%m-%d')
		offer.imageUrl=offer_data[12]
		offer.save()

if __name__ == '__main__':
	print("Reading File")
	with open('offers/cuelinks/fashion/11-06-18.csv', 'r') as offersFile:
		fieldNames=['Id','Title','Merchant','Categories','Description','Terms','Coupon Code','URL','Status','Start Date','End Date','Offer Added At','Image URL']
		offerReader=csv.reader(offersFile, delimiter=',')
		count=0
		catId='fashion'
		stores=[]
		for row in offerReader:
			count=count+1
			# print(row[0],row[2],row[3], row[6], row[8])
			print(row[1])
			stores.append(row[2])
		stores_set=set(stores)
		print("Total %s offers and %s stores"%(count, len(stores_set)))
		offersFile.close()
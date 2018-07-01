from django.core.management.base import BaseCommand, CommandError
from webapp.models import Store, Offer
from webapp.cuelinks import CuelinksOffersHandler


class Command(BaseCommand):
	help = 'Updates the specified category cuelinks offers for e.g.- electronics, baby-kids'

	def add_arguments(self, parser):
		parser.add_argument('catId', nargs='+', type=str)

	def handle(self, *args, **kwargs):
		try:
			catId=kwargs['catId'][0]
			handle=CuelinksOffersHandler()
			offers=handle.read_offers_csv(catId)
			offerList=[]
			for off in offers:
				offer=handle.create_offer(off, catId)
				offerList.append(offer)
			print("SuccesFully Updated {0} Offers".format(offerList.__len__()))
		except Exception as e:
			print(e)
			raise CommandError('Could Not Execute This Command')
		self.stdout.write(self.style.SUCCESS("SuccesFully Executed!"))
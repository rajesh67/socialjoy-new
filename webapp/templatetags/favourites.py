from django import template
import re

register=template.Library()


@register.filter(name='check_store_fav')
def check_store_fav(user, store):
	bookmarks=user.storebookmark_set.all()
	pkList=[b.pk for b in bookmarks]
	if store.pk not in pkList:
		return False

@register.filter(name='get_discount')
def get_discount(offer):
	dis=re.findall(r'\d+%', offer.title)
	if dis:
		return dis[0]
	rs=re.findall(r'Rs.[0-9,]+|INR [0-9,]+', offer.title)
	if rs:
		return rs[0]
	else:
		return None

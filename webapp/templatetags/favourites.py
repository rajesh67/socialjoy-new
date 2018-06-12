from django import template


register=template.Library()


@register.filter(name='check_store_fav')
def check_store_fav(user, store):
	bookmarks=user.storebookmark_set.all()
	pkList=[b.pk for b in bookmarks]
	if store.pk not in pkList:
		return False
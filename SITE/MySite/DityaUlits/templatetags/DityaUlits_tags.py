from django import template
from DityaUlits.models import *

#from django import template
#from women.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('DityaUlits/list_categories.html')
def show_categories(sort=None, cat_selected=0):

    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}
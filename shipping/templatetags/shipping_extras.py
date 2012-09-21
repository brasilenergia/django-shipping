# coding: utf-8
from django import template
from shipping.models import Country

register = template.Library()


@register.inclusion_tag('shipping/freight.html')
def shipping_freight():
    countries = Country.objects.filter(zone__status=1).filter(status=1)\
        .order_by('name').all()

    return {'countries': countries}

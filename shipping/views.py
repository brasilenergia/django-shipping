# coding: utf-8
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from shipping.models import State, Zone, Country


def countries(request):
    countries = Country.objects.filter(zone__status=1).filter(status=1)\
        .order_by('name').all()

    response = {'countries': []}
    for country in countries:
        response['countries'].append({'iso': country.iso, 'name': country.name})

    return HttpResponse(json.dumps(response), mimetype="application/json;charset=utf-8")


def estimation(request):
    dimensions = request.POST.getlist('dimensions')
    zipcode = request.POST.get('zipcode')
    state_id = request.POST.get('state_id')

    state = get_object_or_404(State, id=state_id)

    carrier = state.country.zone.get_carrier()
    price = carrier.estimate_shipping(dimensions, state, zipcode)

    response = json.dumps({'price': price})
    return HttpResponse(response, mimetype="application/json;charset=utf-8")

# coding: utf-8
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from shipping.models import State


def estimation(request):
    dimensions = request.POST.getlist('dimensions')
    zipcode = request.POST.get('zipcode')
    state_id = request.POST.get('state_id')

    state = get_object_or_404(State, id=state_id)

    carrier = state.country.zone.get_carrier()
    price = carrier.estimate_shipping_for_zipcode(dimensions, zipcode)

    response = json.dumps({'price': price})
    return HttpResponse(response, mimetype="application/json;charset=utf-8")

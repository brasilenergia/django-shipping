# coding: utf-8
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from shipping.models import Package, State
from shipping.packing.package import Package as ShippingPackage
from shipping.packing import binpack


def estimate(dimensions, zipcode, state):
    packages = [ShippingPackage(dimension) for dimension in dimensions]
    best, rest = binpack(packages)


def estimation(request):
    dimensions = request.POST.getlist('dimensions')
    zipcode = request.POST.get('zipcode')
    state_id = request.POST.get('state_id')

    state = get_object_or_404(State, id=state)
    import pdb;pdb.set_trace()
    response = json.dumps({'price': 'R$ 1000.10'})
    return HttpResponse(response, mimetype="application/json;charset=utf-8")

# coding: utf-8
import sure
from django.test import TestCase
from shipping.models import State


class EstimationTestCase(TestCase):

    def test_estimation_shipping_correios(self):
        riodejaneiro_state = State.objects.get(id=117)
        zipcode = "22031012"

        response = self.client.post('/shipping/estimation', {
            'state': riodejaneiro_state.id,
            'zipcode': zipcode,
            'packages': ('100x100x100', '200x200x200')
        })

        response.content.should.be('{"price": "R$ 1000.10"}')
        response.status_code.should.be(200)

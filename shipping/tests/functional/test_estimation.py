# coding: utf-8
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

        import pdb;pdb.set_trace()

# coding: utf-8
import sure
from django.test import TestCase
from shipping.models import State, CorreiosCarrier, Bin


class EstimationTestCase(TestCase):

    def test_estimation_shipping_by_correios(self):
        correios = CorreiosCarrier.objects.create(name='carrier test', status=1,
            correios_company="", correios_password="", zip_code="2203070")

        bins = [
            Bin.objects.create(name='bin one', height=100, width=100,
                length=100, weight=0.1, carrier=correios),
            Bin.objects.create(name='bin two', height=200, width=200,
                length=200, weight=0.2, carrier=correios),
            Bin.objects.create(name='bin three', height=300, width=300,
                length=300, weight=0.3, carrier=correios),
        ]

        riodejaneiro_state = State.objects.get(id=117)
        zipcode = "22031012"

        zone = riodejaneiro_state.country.zone
        zone.carrier = correios
        zone.save()

        try:
            response = self.client.post('/shipping/estimation', {
                'state_id': riodejaneiro_state.id,
                'zipcode': zipcode,
                'dimensions': ('100x100x100x1.1', '200x200x200x0.2')
            })
            response.content.should.be.eql('{"price": "R$ 1000.10"}')
            response.status_code.should.be(200)
        finally:
            zone.carrier = None
            zone.save()
            correios.delete()

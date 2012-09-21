# coding: utf-8
import sure
import json
from django.test import TestCase
from shipping.models import State, Country


class CountryTestCase(TestCase):

    def test_get_countries_list(self):
        response = self.client.get('/shipping/countries.json')
        response_data = json.loads(response.content)

        {u'iso': u'BR', u'name': u'Brazil'}.should.be\
            .within(response_data['countries'])

        {u'iso': u'US', u'name': u'United State'}.should.be\
            .within(response_data['countries'])

        response_data['countries'].should.have.length_of(106)

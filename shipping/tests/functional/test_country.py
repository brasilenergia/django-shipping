# coding: utf-8
import sure
import json
from django.test import TestCase


class CountryTestCase(TestCase):

    def test_get_countries_list(self):
        response = self.client.get('/shipping/countries.json')
        response_data = json.loads(response.content)

        {u'iso': u'BR', u'name': u'Brazil'}.should.be\
            .within(response_data['countries'])

        {u'iso': u'US', u'name': u'United State'}.should.be\
            .within(response_data['countries'])

        response_data['countries'].should.have.length_of(106)

    def test_get_brazilina_states_by_country(self):
        response = self.client.get('/shipping/countries/BR.json')
        response_data = json.loads(response.content)

        {u'iso': 'RJ', u'name': u'Rio de Janeiro', u'id': 117}.should.be\
            .within(response_data['states'])

        {u'iso': 'SP', u'name': u'São Paulo', u'id': 123}.should.be\
            .within(response_data['states'])
        response_data['states'].should.have.length_of(27)

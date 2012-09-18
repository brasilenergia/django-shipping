# -*- coding: utf-8 -*-
import os
from south.db import db
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        path = lambda p: os.path.join(os.path.dirname(__file__), p)

        db.execute_many(open(path('zone.sql')).read())
        db.execute_many(open(path('country.sql')).read())
        db.execute_many(open(path('state.sql')).read())

    def backwards(self, orm):
        db.execute_many('delete * from shipping_zone;')
        db.execute_many('delete * from shipping_country;')
        db.execute_many('delete * from state;')

    models = {
        'shipping.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'zones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shipping.Zone']", 'symmetrical': 'False'})
        },
        'shipping.correioscarrier': {
            'Meta': {'object_name': 'CorreiosCarrier', '_ormbases': ['shipping.Carrier']},
            'carrier_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shipping.Carrier']", 'unique': 'True', 'primary_key': 'True'}),
            'correios_company': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'correios_password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'shipping.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.Zone']"})
        },
        'shipping.package': {
            'Meta': {'object_name': 'Package'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.Carrier']"}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'shipping.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.Country']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shipping.upscarrier': {
            'Meta': {'object_name': 'UPSCarrier', '_ormbases': ['shipping.Carrier']},
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'carrier_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shipping.Carrier']", 'unique': 'True', 'primary_key': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.Country']"}),
            'dimension_unit': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'package_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.Package']"}),
            'pickup_type': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'rate_service': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shipping.State']"}),
            'ups_api_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ups_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ups_login': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ups_password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight_unit': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'shipping.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['shipping']
    symmetrical = True

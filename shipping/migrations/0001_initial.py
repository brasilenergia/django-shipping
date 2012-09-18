# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zone'
        db.create_table('shipping_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal('shipping', ['Zone'])

        # Adding model 'Country'
        db.create_table('shipping_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.Zone'])),
        ))
        db.send_create_signal('shipping', ['Country'])

        # Adding model 'State'
        db.create_table('shipping_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.Country'], null=True)),
        ))
        db.send_create_signal('shipping', ['State'])

        # Adding model 'Package'
        db.create_table('shipping_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('weight', self.gf('django.db.models.fields.FloatField')()),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.Carrier'])),
        ))
        db.send_create_signal('shipping', ['Package'])

        # Adding model 'Carrier'
        db.create_table('shipping_carrier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
        ))
        db.send_create_signal('shipping', ['Carrier'])

        # Adding M2M table for field zones on 'Carrier'
        db.create_table('shipping_carrier_zones', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('carrier', models.ForeignKey(orm['shipping.carrier'], null=False)),
            ('zone', models.ForeignKey(orm['shipping.zone'], null=False))
        ))
        db.create_unique('shipping_carrier_zones', ['carrier_id', 'zone_id'])

        # Adding model 'UPSCarrier'
        db.create_table('shipping_upscarrier', (
            ('carrier_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['shipping.Carrier'], unique=True, primary_key=True)),
            ('ups_login', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ups_password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ups_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ups_api_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('weight_unit', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('dimension_unit', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.Country'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.State'])),
            ('rate_service', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('pickup_type', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('package_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shipping.Package'])),
        ))
        db.send_create_signal('shipping', ['UPSCarrier'])

        # Adding model 'CorreiosCarrier'
        db.create_table('shipping_correioscarrier', (
            ('carrier_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['shipping.Carrier'], unique=True, primary_key=True)),
            ('correios_company', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('correios_password', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('shipping', ['CorreiosCarrier'])


    def backwards(self, orm):
        # Deleting model 'Zone'
        db.delete_table('shipping_zone')

        # Deleting model 'Country'
        db.delete_table('shipping_country')

        # Deleting model 'State'
        db.delete_table('shipping_state')

        # Deleting model 'Package'
        db.delete_table('shipping_package')

        # Deleting model 'Carrier'
        db.delete_table('shipping_carrier')

        # Removing M2M table for field zones on 'Carrier'
        db.delete_table('shipping_carrier_zones')

        # Deleting model 'UPSCarrier'
        db.delete_table('shipping_upscarrier')

        # Deleting model 'CorreiosCarrier'
        db.delete_table('shipping_correioscarrier')


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
# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import DataMigration


class Migration(DataMigration):

    def forwards(self, orm):
        carrier = orm['UPSCarrier'].objects.create(name='UPS', status=1)

        # Large-18" x 13" x 3"
        orm['Bin'].objects.create(name='UPS Express Box - Large',
            height=45.72, width=33.02, length=7.62, carrier=carrier)

        # Medium-15" x 11" x 3"
        orm['Bin'].objects.create(name='UPS Express Box - Medium',
            height=38.1, width=27.94, length=7.62, carrier=carrier)

        # Small- 13" x 11" x 2"
        orm['Bin'].objects.create(name='UPS Express Box - Small',
            height=33.02, width=27.94, length=5.08, carrier=carrier)

        carrier = orm['CorreiosCarrier'].objects.create(name='Correios',
            status=1)

    def backwards(self, orm):
        db.execute_many('delete * from carrier;')
        db.execute_many('delete * from bin;')

    complete_apps = ['shipping']

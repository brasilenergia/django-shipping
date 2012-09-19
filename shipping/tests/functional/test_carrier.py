# coding: utf-8
import unittest
import sure
from shipping.models import Carrier, Bin
from shipping.packing.package import Package


class CarrierTestsCase(unittest.TestCase):

    def test_can_be_get_best_bin_for_packages(self):

        carrier = Carrier.objects.create(name='carrier test', status=1)

        bins = [
            Bin.objects.create(name='bin one', height=100, width=100,
                length=100, weight=0.1, carrier=carrier),
            Bin.objects.create(name='bin two', height=200, width=200,
                length=200, weight=0.2, carrier=carrier),
            Bin.objects.create(name='bin three', height=300, width=300,
                length=300, weight=0.3, carrier=carrier),
        ]

        packages = [
            Package('50x40x30'),
            Package('100x100x30'),
            Package('200x200x30'),
        ]

        best_bin = carrier.get_best_bin_for_packages(packages)
        best_bin.should.be.eql(bins[1])

        carrier.delete()

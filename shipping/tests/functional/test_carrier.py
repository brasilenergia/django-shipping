# coding: utf-8
import unittest
import sure
from shipping.models import Carrier, Bin
from shipping.packing.package import Package


class CarrierTestsCase(unittest.TestCase):

    def test_can_be_get_best_bin_for_packages(self):

        carrier = Carrier.objects.create(name='carrier test', status=1)

        bins = [
            Bin.objects.create(name='bin one', height=20, width=20,
                length=20, weight=0.1, carrier=carrier),
            Bin.objects.create(name='bin two', height=30, width=30,
                length=30, weight=0.2, carrier=carrier),
            Bin.objects.create(name='bin three', height=40, width=40,
                length=40, weight=0.3, carrier=carrier),
        ]

        packages = [
            Package('10x10x10'),
            Package('8x17x30'),
            Package('6x32x12'),
        ]

        best_bin = carrier.get_best_bin_for_packages(packages)
        best_bin.should.be.eql(bins[2])

        carrier.delete()

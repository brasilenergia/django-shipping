# coding: utf-8
import unittest
import sure
from shipping.packing import binpack
from shipping.packing.package import Package


class PackingTests(unittest.TestCase):

    def test_can_be_packing_two_packages_in_one_bin(self):

        package_one = Package("100x100x100")
        package_two = Package("200x200x200")

        packages = [package_one, package_two]
        bin = Package("300x300x300")

        best, rest = binpack(packages, bin)

        package_one.should.be.within(best[0])
        package_two.should.be.within(best[0])
        best[0].should.be.length_of(2)
        rest.should.be([0])

    def test_can_be_packing_four_packages_in_two_bin(self):
        package_one = Package("100x100x100")
        package_two = Package("200x200x200")
        package_three = Package("100x100x100")
        package_four = Package("200x200x200")

        packages = [package_one, package_two, package_three, package_four]
        bin = Package("300x300x300")

        best, rest = binpack(packages, bin)

        package_one.should.be.within(best[0])
        package_two.should.be.within(best[0])
        package_three.should.be.within(best[0])

        package_four.should.be.within(best[1])

        best.should.be.length_of(2)
        best[0].should.be.length_of(3)
        best[1].should.be.length_of(1)
        rest.should.be([])

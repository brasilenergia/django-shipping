# coding: utf-8
import unittest
from shipping.binpack.package import Package


class PackageTests(unittest.TestCase):
    """Simple tests for Package objects."""

    def test_init(self):
        """Tests object initialisation with different constructors."""
        self.assertEqual(Package((100, 100, 200)), Package(('100', '200', '100')))
        self.assertEqual(Package((100.0, 200.0, 200.0)), Package('200x200x100'))

    def test_eq(self):
        """Tests __eq__() implementation."""
        self.assertEqual(Package((200, 100, 200)), Package(('200', '100', '200')))
        self.assertNotEqual(Package((200, 200, 100)), Package(('100', '100', '200')))

    def test_volume(self):
        """Tests volume calculation"""
        self.assertEqual(4000000, Package((100, 200, 200)).volume)
        self.assertEqual(8000, Package((20, 20, 20)).volume)

    def test_str(self):
        """Test __unicode__ implementation."""
        self.assertEqual('200x200x100', Package((100, 200, 200)).__str__())
        self.assertEqual('200x200x100', Package('100x200x200').__str__())

    def test_repr(self):
        """Test __repr__ implementation."""
        self.assertEqual('<Package 200x200x100 44>', Package((100, 200, 200), 44).__repr__())

    def test_gurtmass(self):
        """Test gurtmass calculation."""
        self.assertEqual(800, Package((100, 200, 200)).gurtmass)
        self.assertEqual(900, Package((100, 200, 300)).gurtmass)
        self.assertEqual(1000, Package((200, 200, 200)).gurtmass)
        self.assertEqual(3060, Package((1600, 250, 480)).gurtmass)

    def test_mul(self):
        """Test multiplication."""
        self.assertEqual(Package((200, 200, 200)), Package((100, 200, 200)) * 2)

    def test_sort(self):
        """Test multiplication."""
        data = [Package((1600, 490, 480)), Package((1600, 470, 480)), Package((1600, 480, 480))]
        data.sort()
        self.assertEqual(data,
                         [Package((1600, 470, 480)), Package((1600, 480, 480)),
                          Package((1600, 490, 480))])

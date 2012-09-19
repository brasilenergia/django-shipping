# coding: utf-8
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from shipping.packing.package import Package
from shipping.packing import binpack

STATUS = (
    (0, 'Unavailable'),
    (1, 'Available')
)


class Zone(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(max_length=2, choices=STATUS)
    carrier = models.ForeignKey('Carrier', null=True)

    def get_carrier(self):
        """ get the appropriate carrier class
        """
        carriers_class = ('correioscarrier', 'upscarrier')

        for carrier_class in carriers_class:
            try:
                return getattr(self.carrier, carrier_class)
            except ObjectDoesNotExist:
                pass

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso = models.CharField(max_length=20)
    status = models.IntegerField(max_length=2, choices=STATUS)
    zone = models.ForeignKey(Zone)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    iso = models.CharField(max_length=20)
    country = models.ForeignKey(Country, null=True)

    def __unicode__(self):
        return self.name


class Bin(models.Model):
    name = models.CharField(max_length=255)
    width = models.IntegerField(help_text="width in centimeters")
    height = models.IntegerField(help_text="height in centimeters")
    length = models.IntegerField(help_text="length in centimeters")
    weight = models.FloatField(help_text="peso in kilograms")

    carrier = models.ForeignKey('Carrier', related_name='bins')

    def get_package(self):
        return Package((self.height, self.width, self.length))

    def __unicode__(self):
        if self.width and self.height and self.length:
            return "{name} ({w}x{h}x{l})".format(name=self.name, w=self.width,
                h=self.height, l=self.length)

        return self.name


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(max_length=2, choices=STATUS)

    def estimate_shipping_for_zipcode(self, dimensions, zipcode):
        """ method that finds optimal solution for packing the products
        and according to the zone's carrier calc shipping estimation to zipcode

        :Parameter
          - dimensions: a list of product's dimension '{height}x{width}x{length}x{weight}'
          - zipcode: a valid zip code
          - state: a valid state
        """
        packages = []
        for dimension in dimensions:
            height, width, length, weight = dimension.split('x')
            size = (int(height), int(width), int(length))

            package = Package(size, weight=float(weight))
            packages.append(package)

        best_bin = self.get_best_bin_for_packages(packages)

        if not best_bin:
            raise ValueError('This carrier does not have a valid bin')

        # calc the best packing
        best_packing, rest = binpack(packages, best_bin.get_package())

        total_coast = 0.0
        for pack in best_packing:

            # calc total weight, sum of all packages plus bin weight
            weight_total = sum([package.weight for package in pack]) + best_bin.weight

            # calc price for shipping each pack
            total_coast += self.calculate_shipping_coast(best_bin, weight_total)

        return total_coast

    def get_best_bin_for_packages(self, packages):
        """ choose the best bin for a list of packages
        """
        my_packages = []
        for bin in self.bins.all():
            package = bin.get_package()
            package.bin = bin
            my_packages.append(package)

        greater_package = max(packages)
        my_packages.sort()

        for package in my_packages:
            if package > greater_package:
                return package.bin

        # when best bin not found, returns de greater bin
        if my_packages:
            return max(my_packages).bin

    def __unicode__(self):
        return self.name


class UPSCarrier(Carrier):
    WEIGHT_UNITS = (
        ('kg', 'kilograms'),
        ('lb', 'pounds'),
    )
    DIMENSION_UNITS = (
        ('cm', 'centimeters'),
        ('in', 'inches'),
    )

    # general
    ups_login = models.CharField(max_length=255)
    ups_password = models.CharField(max_length=255)
    ups_id = models.CharField(max_length=255)
    ups_api_key = models.CharField(max_length=255)

    # local confs
    weight_unit = models.CharField(max_length=3, choices=WEIGHT_UNITS)
    dimension_unit = models.CharField(max_length=3, choices=DIMENSION_UNITS)

    # sender address
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)

    # services
    RATE_SERVICES = (
        (1, "United States Domestic Shipments"),
        (2, "Shipments Originating in United States"),
        (3, "Shipments Originating in Puerto Rico"),
        (4, "Shipments Originating in Canada"),
        (5, "Shipments Originating in Mexico"),
        (6, "Polish Domestic Shipments"),
        (7, "Shipments Originating in the European Union"),
        (8, "Shipments Originating in Other Countries"),
    )
    rate_service = models.IntegerField(max_length=2, choices=RATE_SERVICES)

    PICKUP_TYPES = (
        (1, "Daily Pickup"),
        (3, "Customer Counter"),
        (6, "One Time Pickup"),
        (7, "On Call Air"),
        (11, "Suggested Retail Rates"),
        (19, "Letter Center"),
        (20, "Air Service Center")
    )
    pickup_type = models.IntegerField(max_length=2, choices=PICKUP_TYPES)

    package_type = models.ForeignKey('Bin')


class CorreiosCarrier(Carrier):
    correios_company = models.CharField(max_length=200, help_text='required when using E-Sedex')
    correios_password = models.CharField(max_length=200, help_text='required when using E-Sedex')
    zip_code = models.CharField(max_length=20)

    def calculate_shipping_coast(self, bin, weight_total):
        return 1.0

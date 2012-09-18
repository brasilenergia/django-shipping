# coding: utf-8
from django.db import models

STATUS = (
    (0, 'Unavailable'),
    (1, 'Available')
)


class Zone(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(max_length=2, choices=STATUS)

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


class Package(models.Model):
    name = models.CharField(max_length=255)
    width = models.IntegerField(help_text="width in centimeters")
    height = models.IntegerField(help_text="height in centimeters")
    length = models.IntegerField(help_text="length in centimeters")
    weight = models.FloatField(help_text="peso in kilograms")

    carrier = models.ForeignKey('Carrier')

    def __unicode__(self):
        if self.width and self.height and self.length:
            return "%s (%s)" % (self.name, "x".join([self.width, self.height, self.length]))

        return self.name


class Carrier(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(max_length=2, choices=STATUS)
    zones = models.ManyToManyField(Zone)

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

    package_type = models.ForeignKey('Package')


class CorreiosCarrier(Carrier):
    correios_company = models.CharField(max_length=200, help_text='required when using E-Sedex')
    correios_password = models.CharField(max_length=200, help_text='required when using E-Sedex')
    zip_code = models.CharField(max_length=20)

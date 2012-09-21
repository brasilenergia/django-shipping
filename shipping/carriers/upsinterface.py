# coding: utf-8
from ups.client import UPSClient
from ups.model import Address, Package as UPSPackage


class UPSInterface(object):

    def __init__(self, ups_carrier):

        self.credentials = {
            'username': ups_carrier.ups_login,
            'password': ups_carrier.ups_password,
            'access_license': ups_carrier.ups_api_key,
            'shipper_number': ups_carrier.ups_id,
        }
        self.shipper = Address(name='shipper address name', city=ups_carrier.city,
            address=ups_carrier.address_line_1, state=ups_carrier.state.iso,
            zip=ups_carrier.zip_code, country=ups_carrier.country.iso,
            address2=ups_carrier.address_line_2)
        self.package_type = ups_carrier.package_type

    def get_shipping_cost(self, package, weight_total, zip_to):
        ups_package = UPSPackage(weight=weight_total, length=package.length,
            width=package.width, height=package.heigth)

        recipient = Address(name='recipient address name', city='',
            address='', state='', zip=zip_to, country='')

        ups = UPSClient(self.credentials)
        rate_result =  ups.rate([ups_package], self.shipper, recipient, self.package_type)

        import pdb;pdb.set_trace()

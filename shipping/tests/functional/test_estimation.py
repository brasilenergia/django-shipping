# coding: utf-8
import sure
import fudge
from django.test import TestCase
from shipping.models import State, CorreiosCarrier, UPSCarrier, Bin, Country


class EstimationTestCase(TestCase):

    @fudge.patch('shipping.carriers.correios.urllib2')
    def test_estimation_shipping_by_correios(self, urllib2_fake):
        correios_params = (
            'strRetorno=xml',
            'nVlValorDeclarado=0',
            'nCdServico=40010',
            'nVlDiametro=56',
            'sCdMaoPropria=',
            'nVlComprimento=40',
            'nVlLargura=40',
            'sDsSenha=123',
            'nVlAltura=40',
            'nCdEmpresa=001',
            'nCdFormato=1',
            'sCepDestino=22031012',
            'sCepOrigem=2203070',
            'VlPeso=1%2C6',
            'sCdAvisoRecebimento=N'
        )

        correios_response = """<Servicos><cServico>
            <Codigo>40010</Codigo>
            <Valor>12,10</Valor>
            <PrazoEntrega>1</PrazoEntrega>
            <ValorMaoPropria>0,00</ValorMaoPropria>
            <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
            <ValorValorDeclarado>1,00</ValorValorDeclarado>
            <EntregaDomiciliar>S</EntregaDomiciliar>
            <EntregaSabado>S</EntregaSabado>
            <Erro>0</Erro>
            <MsgErro></MsgErro>
        </cServico></Servicos>"""

        correios = CorreiosCarrier.objects.create(name='carrier test', status=1,
            correios_company="001", correios_password="123", zip_code="2203070")

        def fake_urlopen(url, timeout):
            for param in correios_params:
                param.should.be.within(url)

            return fudge.Fake('response').expects('read').returns(correios_response)

        urllib2_fake.expects('urlopen').calls(fake_urlopen)

        Bin.objects.create(name='bin one', height=20, width=20,
            length=20, weight=0.1, carrier=correios),
        Bin.objects.create(name='bin two', height=30, width=30,
            length=30, weight=0.2, carrier=correios),
        Bin.objects.create(name='bin three', height=40, width=40,
            length=40, weight=0.3, carrier=correios),

        riodejaneiro_state = State.objects.get(id=117)
        zipcode = "22031012"

        zone = riodejaneiro_state.country.zone
        zone.carrier = correios
        zone.save()

        try:
            response = self.client.post('/shipping/estimation', {
                'country_code': riodejaneiro_state.country.iso,
                'zipcode': zipcode,
                'dimensions': ('10x10x10x1.1', '8x17x30x0.2')
            })
            response.content.should.be.eql('{"currency": "BRL", "price": 12.1}')
            response.status_code.should.be(200)
        finally:
            zone.carrier = None
            zone.save()
            correios.delete()

    @fudge.patch('shipping.carriers.upsinterface.UPSClient')
    def test_estimation_shipping_by_ups(self, fake_ups_client):
        ups_carrier = UPSCarrier.objects.create(name='UPS Test', ups_login='login',
            ups_password='pass', ups_id='myid', ups_api_key='1', zip_code='2203070',
            address_line_1='address line 1', city='rio de janeiro',
            country=Country.objects.get(id=58), state=State.objects.get(id=117),
            package_type='21', status=1)

        Bin.objects.create(name='UPS Express Box - Large',
            height=45.72, width=33.02, length=7.62, weight=0,
            carrier=ups_carrier)

        # Medium-15" x 11" x 3"
        Bin.objects.create(name='UPS Express Box - Medium',
            height=38.1, width=27.94, length=7.62, weight=0,
            carrier=ups_carrier)

        # Small- 13" x 11" x 2"
        small_package = Bin.objects.create(name='UPS Express Box - Small',
            height=33.02, width=27.94, length=5.08, weight=0,
            carrier=ups_carrier)

        alabama_state = State.objects.get(id=1)
        zipcode = "36201"

        zone = alabama_state.country.zone
        zone.carrier = ups_carrier
        zone.save()

        def rate(packages, shipper, recipient, package_type):
            packages[0].height.should.be.eql(small_package.height)
            packages[0].width.should.be.eql(small_package.width)
            packages[0].length.should.be.eql(small_package.length)

            shipper.city.should.be.eql(ups_carrier.city)
            shipper.state.should.be.eql(ups_carrier.state.iso)
            shipper.country.should.be.eql(ups_carrier.country.iso)
            shipper.zip.should.be.eql(ups_carrier.zip_code)

            recipient.city.should.be.eql('')
            recipient.state.should.be.eql(alabama_state.iso)
            recipient.country.should.be.eql(alabama_state.country.iso)
            recipient.zip.should.be.eql(zipcode)

            package_type.should.be.eql('21')

            return {'info': [{
                'package': '',
                'delivery_day': '',
                'cost': 10.1,
                'currency': 'USD'
            }]}

        fake_ups_client.is_callable().returns_fake().expects('rate').calls(rate)
        try:
            response = self.client.post('/shipping/estimation', {
                'state': alabama_state.id,
                'country_code': alabama_state.country.iso,
                'zipcode': zipcode,
                'dimensions': ('10x10x2x1.1', '1.2x17x30x0.2')
            })
            response.content.should.be.eql('{"currency": "USD", "price": 10.1}')
            response.status_code.should.be(200)
        finally:
            zone.carrier = None
            zone.save()
            ups_carrier.delete()

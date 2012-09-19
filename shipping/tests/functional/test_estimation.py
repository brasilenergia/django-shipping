# coding: utf-8
import sure
import fudge
from django.test import TestCase
from shipping.models import State, CorreiosCarrier, Bin


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
            'nVlPeso=1.6',
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
                'state_id': riodejaneiro_state.id,
                'zipcode': zipcode,
                'dimensions': ('10x10x10x1.1', '8x17x30x0.2')
            })
            response.content.should.be.eql('{"price": 12.1}')
            response.status_code.should.be(200)
        finally:
            zone.carrier = None
            zone.save()
            correios.delete()

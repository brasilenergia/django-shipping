#coding: utf-8
import urllib2
import urllib
import simplexml
import math


class CorreiosFormat:
    """enumerate available correios formats
    """
    PACOTE = 1
    ROLO = 2


class CorreiosService:
    """enumerate available correios services
    """
    PAC = '41106'
    SEDEX = '40010'
    SEDEX10 = '40215'
    SEDEXHOJE = '40290'
    SEDEXCOBRAR = '40045'


class CorreiosInterface(object):
    """implements basic integration with federal brazilian carrier, Correios.
    """
    _endpoint = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
    _min_dimensions = {
        CorreiosFormat.PACOTE: (18, 5, 0, 0),
        CorreiosFormat.ROLO: (16, 0, 2, 5)
    }

    def __init__(self, zip_from, company=None, password=None,
        service=CorreiosService.SEDEX, format=CorreiosFormat.PACOTE):
        """create a new instance of correios carrier

        :Parameters
          - zip_from: zipcode of where package will be delivered
          - password: correios company password
          - company: correios company code
          - service: correios service
          - format: format of package
        """
        self._zip_from = zip_from
        self._password = password
        self._company = company
        self._service = service
        self._format = format

        self._length = None
        self._diameter = None
        self._height = None
        self._width = None
        self._zip_to = None

        self._aviso_recebimento = 'N'
        self._valor_declarado = 0
        self._mao_propria = 'N'

    def _get_diameter(self):
        """returns the diameter of the sphere inscrit in the package
        """
        return int(math.sqrt(math.pow(self._length, 2) +
            math.pow(self._width, 2)))

    def _set_dimensions(self, package, weight_total):
        self._length, self._diameter, self._height, self._width = self._min_dimensions.get(self._format)
        self._weight = 0.3

        if package.heigth > self._height:
            self._height = package.heigth

        if package.width > self._width:
            self._width = package.width

        if package.length > self._length:
            self._length = package.length

        if weight_total > self._weight:
            self._weight = weight_total

        # height can't be greater than length
        if self._height > self._length:
            self._height = self._length

        # width can't be less than 11cm when length is less than 25cm
        if self._format == CorreiosFormat.PACOTE and self._width < 11 \
            and self._length < 25:
            self._width = 11

        # set diameter
        diameter = self._get_diameter()
        if diameter > self._diameter:
            self._diameter = diameter

    def _get_parameters(self):
        params = {
            'nCdEmpresa': self._company,
            'sDsSenha': self._password,
            'strRetorno': 'xml',
            'sCdMaoPropria': self._mao_propria,
            'nVlValorDeclarado': self._valor_declarado,
            'sCdAvisoRecebimento': self._aviso_recebimento,
            'nCdFormato': self._format,
            'sCepOrigem': self._zip_from,
            'sCepDestino': self._zip_to,
            'nCdServico': self._service,
            'nVlAltura': self._height,
            'nVlLargura': self._width,
            'nVlComprimento': self._length,
            'nVlDiametro': self._diameter,
            'nVlPeso': self._weight
        }

        return params

    def _make_request(self):
        url = '%s?%s' % (self._endpoint,
            urllib.urlencode(self._get_parameters()))

        data = urllib2.urlopen(url, timeout=5).read()
        """
        Exemplo do retorno:
            <cServico>
                <Codigo>40045</Codigo>
                <Valor>12,10</Valor>
                <PrazoEntrega>1</PrazoEntrega>
                <ValorMaoPropria>0,00</ValorMaoPropria>
                <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
                <ValorValorDeclarado>1,00</ValorValorDeclarado>
                <EntregaDomiciliar>S</EntregaDomiciliar>
                <EntregaSabado>S</EntregaSabado>
                <Erro>0</Erro>
                <MsgErro></MsgErro>
            </cServico>
        """
        response = simplexml.loads(data)

        result = response['Servicos']['cServico']

        erro = int(result.get('Erro'))
        if erro != 0:
            raise ValueError(result.get('MsgErro'))
        else:
            return result.get('Valor')

    def get_shipping_cost(self, package, weight_total, zip_to):
        self._set_dimensions(package, weight_total)
        self._zip_to = zip_to

        price = self._make_request()

        return float(price.replace(',', '.'))

import os
import base64
import random

import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from xhtml2pdf import pisa

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Sucursal,
    Entidade,
    SucursalUserGroup,
    Ficheiros,
    Stock,
)
from .serializers import (
    SucursalSerializer,
    EntidadeSerializer,
    FicheiroSerializer,
    FicheiroGravarSerializer,
    StockSerializer,
)
from .classes.Translate import Translate
from .utils.DiscManegar import DiscManegar





class  SucursalAPIView(viewsets.ModelViewSet):
    #permission_classes = (permissions.IsAuthenticated)
    search_fields = ['id','nome']
    filter_backends = (filters.SearchFilter,)
    
    serializer_class = SucursalSerializer
    queryset = Sucursal.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by('-id')

    @action(
        detail=True,
        methods=['GET'],
    )
    def grupos(self, request, id):
        sucursalUserGroups = SucursalUserGroup.objects.all().filter(sucursal__id=id, user__id=request.user.id)
        suc = []
        for sucursalUserGroup in sucursalUserGroups:
            suc.append({'id': sucursalUserGroup.group.id, 'name': sucursalUserGroup.group.name})

        return Response(suc)

    @action(
        detail=True,
        methods=['GET'],
    )
    def Url(self, request, id):
        sucursal = Sucursal.objects.get(id=id)
        entidade = Entidade.objects.get(id=sucursal.entidade.id)
        return Response(str(entidade.tipo_entidade.id)+'/'+str(sucursal.entidade.id)+'/'+str(sucursal.id))
    
    

    @action(
        detail=True,
        methods=['GET'],
    )
    def getCapasSite(self, request, id):
        ficheiros = Ficheiros.objects.filter(sucursal__id=id, funcionalidade='CapaSite')
        ficheiros = FicheiroSerializer(ficheiros, many=True)
        data = (ficheiros.data)
        return Response(data, status=status.HTTP_200_OK)
    

    @action(
        detail=True,
        methods=['POST'],
    )
    def postCapasSite(self, request, id):
        sucursal = Sucursal.objects.get(id=id)

        request.data['entidade'] = str(sucursal.entidade.id)
        request.data['sucursal'] = str(sucursal.id)
        uploaded_file = request.FILES['ficheiro']

        if DiscManegar.freeSpace(sucursal.entidade.id, request.FILES['ficheiro']):
            resposta = {'alert_error': 'Nao e possivel fazer upload de ficheiro<br><b>Contacte o adminstrador</b>'}
            return Response(resposta , status=status.HTTP_400_BAD_REQUEST)

        request.data['size'] = uploaded_file.size
        request.data['modelo'] = 'sucursal'
        request.data['estado'] = 'Activo'
        request.data['funcionalidade'] = 'CapaSite'

        ficheiro = FicheiroGravarSerializer(data=request.data)
        if ficheiro.is_valid(raise_exception=True):
            ficheiro.save()
            ficheiro = FicheiroSerializer(Ficheiros.objects.get(id=ficheiro.data['id']))
            DiscManegar.updateSpace(sucursal.entidade.id, request.FILES['ficheiro'])
            return Response(ficheiro.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ficheiro.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(
        detail=True,
        methods=['GET'],
    )
    def getStocks(self, request, *args, **kwargs):
        transformer = self.get_object()
        stock = Stock.objects.filter(sucursal=transformer)
        stocks =StockSerializer(stock, many=True)
        return Response(stocks.data, status.HTTP_200_OK)
   

    

    @action(
        detail=True,
        methods=['GET'],
    )
    def qr(self, request, id):
        var_qr = {}
        origin = request.headers['Origin']
        LANGUAGE_CODE = 'pt-pt'

        TIME_ZONE = 'UTC'
        settings.LANGUAGE_CODE = 'pt-pt'
        # django.setup()
        print(settings.LANGUAGE_CODE)

        root = settings.MEDIA_ROOT
        lingua = self.request.query_params.get('lang')

        ean = barcode.get('code128', id, writer=ImageWriter())
        filename = ean.save(str(root) +'/' + str(random.random()) + 'qr' + str(random.random()))

        file = Image.open(str(filename))
        file = open(str(filename), 'rb').read()


        blob_barcode = base64.b64encode((file))
        if os.path.exists(filename):
            os.remove(filename)


        qr = qrcode.QRCode(box_size=2)
        qr.add_data(str('var_qr'))
        qr.make()
        img_qr = qr.make_image()
        # img_qr.
        img = img_qr.get_image()

        name = str(root) +'/' + str(random.random()) + 'qr' + str(random.random()) + '.png'
        img_qr.save(name)
        file = Image.open(str(name))
        file = open(str(name), 'rb').read()
        blob = base64.b64encode(bytes(file))
        if os.path.exists(name):
            os.remove(name)

        pk = id


        template_path = 'core/sucursal/qr_pdf.html'

        sucursal = Sucursal.objects.get(id=pk)
        sucursal1 = sucursal

    

        entidade = EntidadeSerializer(sucursal.entidade)

        sucursal = SucursalSerializer(sucursal)
        ficheiro  = Ficheiros.objects.get(entidade = sucursal1.entidade.id, funcionalidade = 'Logo')
        logo_name = ficheiro.ficheiro.path
        try:
            file = open(logo_name, 'rb').read()
            logo = base64.b64encode(bytes(file))
        except Exception as e:
            logo = logo_name.split('.')[-1]
        print(logo, logo_name, ficheiro)
        
        url = origin + '/#/?s=' + sucursal.data['id'] + '&q=1' 
        var_qr['entidade'] = entidade.data['nome']
        var_qr['sucursal'] = sucursal.data['nome']
        for key, value in var_qr.items():
            url = url + '&' + key + '=' + value
        # print(url)
        qr = qrcode.QRCode(box_size=2)
        qr.add_data(str(url))
        qr.make()
        img_qr = qr.make_image()
    

        name = str(root) +'/' + str(random.random()) + 'qr' + str(random.random()) + '.png'
        img_qr.save(name)
        file = Image.open(str(name))
        file = open(str(name), 'rb').read()
        qr_to_scan = base64.b64encode(bytes(file))


        if os.path.exists(name):
            os.remove(name)
        context = {
            'qr': blob,
            'qr_to_scan': qr_to_scan,
            'barcode': blob_barcode, 
            'entidade': entidade.data,
            'sucursal': sucursal.data,
            'logo':logo,
            'titulo': Translate.tdc(lingua, 'QR'),
            'nome': Translate.tdc(lingua, 'Sucursal'),
            'de': Translate.tdc(lingua, 'de'),
            'morada': Translate.tdc(lingua, 'Morada'),
            'pagina': Translate.tdc(lingua, 'Pagina')
        }
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        # if you need to download
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        response['Content-Disposition'] = 'filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        

        # create a pdf                  link_callback=link_callback
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return Response(context, status=status.HTTP_200_OK)
        return response

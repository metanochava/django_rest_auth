from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import Group

from .models import (
    User,
    Entidade,
    EntidadeUser,
    Sucursal,
    SucursalUser,
    SucursalUserGroup,
    UserLogin,
    Pessoa,
)
from .serializers import (
    UserSerializer,
    EntidadeSerializer,
    SucursalSerializer,
    UserLoginSerializer,
    PessoaSerializer,
    MeSerializer,
)


class UsuarioAPIView(viewsets.ModelViewSet):
    search_fields = ['id','username']
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        if (self.request.query_params.get('allPaginado')):
            return self.queryset.filter().order_by('id')
        else:
            self._paginator = None
            return self.queryset.filter().order_by('id')

    @action(
        detail=True,
        methods=['GET'],
    )
    def userEntidades(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        user = UserSerializer(user)
        tipo_entidade_id = request.headers.get('ET')
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')
        grupo_id = request.headers.get('G')

        ar = []
        userEntidades = EntidadeUser.objects.filter(user__id=id, entidade__tipo_entidade__id=tipo_entidade_id)
        if (userEntidades):
            for userEntidade in userEntidades:
                entidade = Entidade.objects.get(id=userEntidade.entidade.id)
                entidade = EntidadeSerializer(entidade, context={'request': request})
                ar.append({'id': entidade.data['id'], 'tipoEntidade': entidade.data['tipo_entidade'],  'nome': entidade.data['nome'], 'created_at': entidade.data['created_at'].split('-')[0], 'logo': entidade.data['logo']['url']})
           

        return Response(ar, status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
    )
    def logins(self, request, id, *args, **kwargs):
        userLogin = UserLogin.objects.filter(user_id = id).order_by('-data', 'hora')
        userLogins = UserLoginSerializer(userLogin, many=True)
        return Response(userLogins.data, status=status.HTTP_200_OK)
    
    
    @action(
        detail=True,
        methods=['GET'],
    )
    def userSucursals(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        user = UserSerializer(user)
        tipo_entidade_id = request.headers.get('ET')
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')
        grupo_id = request.headers.get('G')

        ar = []
        userSucursals = SucursalUser.objects.filter(user__id=id, sucursal__entidade__tipo_entidade__id=tipo_entidade_id, sucursal__entidade__id=entidade_id)
        if (userSucursals):
            for userSucursal in userSucursals:
                sucursal = Sucursal.objects.get(id=userSucursal.sucursal.id)
                sucursal = SucursalSerializer(sucursal)
                ar.append({'id': sucursal.data['id'], 'nome': sucursal.data['nome']})

        return Response(ar, status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['POST'],
    )
    def addUserSucursal(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        tipo_entidade_id = request.headers.get('ET')
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')
        grupo_id = request.headers.get('G')
        sucursal = Sucursal.objects.get(id= request.data['sucursal'])

        ar = []
        userSucursals = SucursalUser.objects.filter(user__id=id, sucursal__id= sucursal.id,  sucursal__entidade__tipo_entidade__id=tipo_entidade_id, sucursal__entidade__id=entidade_id)
        if (len(userSucursals) <= 1):
            su = SucursalUser()
            su.user = user
            su.sucursal  = sucursal
            su.save()
            # data = json.loads(json.dumps(paciente.data, cls=DjangoJSONEncoder))
        add = {'alert_success':  '<b>' + sucursal.nome+ '</b> foi adicionado com sucesso'}
            # data.update(add)
        return Response(add, status = status.HTTP_201_CREATED)
    
    @action(
        detail=True,
        methods=['POST'],
    )
    def removeUserSucursal(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        tipo_entidade_id = request.headers.get('ET')
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')
        grupo_id = request.headers.get('G')
        sucursal = Sucursal.objects.get(id= request.data['sucursal'])

        userSucursals = SucursalUser.objects.get(user__id=id, sucursal__id= sucursal.id, sucursal__entidade__tipo_entidade__id=tipo_entidade_id, sucursal__entidade__id=entidade_id)
        userSucursals.delete()
        add = {'alert_success': '<b>' + sucursal.nome+ '</b> foi removido com sucesso'}
        return Response(add, status = status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['GET'],
    )
    def userGrupos(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        user = UserSerializer(user)

        if self.request.query_params.get('sucursal') == 'nulo' or self.request.query_params.get('sucursal') == None:
            tipo_entidade_id = request.headers.get('ET')
            entidade_id = request.headers.get('E')
            sucursal_id = request.headers.get('S')
            grupo_id = request.headers.get('G')
        else:
            sucursal_id = self.request.query_params.get('sucursal')

        sucursalUserGroups = SucursalUserGroup.objects.filter(user__id=id, sucursal__id=sucursal_id)
        ar = []
        if (sucursalUserGroups):
            for sucursalUserGroup in sucursalUserGroups:
                group = Group.objects.get(id=sucursalUserGroup.group.id)
                ar.append({'id': group.id, 'name': group.name})

        if True:
            return Response(ar, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET'],
    )
    def userPermicoes(self, request, id, *args, **kwargs):
        user = User.objects.get(id=id)
        user = UserSerializer(user)
        tipo_entidade_id = request.headers.get('ET')
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')
        grupo_id = request.headers.get('G')

        group_id = grupo_id
        sucursalUserGroup = SucursalUserGroup.objects.filter(user__id = id, sucursal__id = sucursal_id, group__id = group_id)
        
        per = []
        if (sucursalUserGroup):
            grupo = Group.objects.get(id=sucursalUserGroup[0].group.id)
            permissions = grupo.permissions.all()

            for permission in permissions:
                per.append({'id': permission.id, 'nome': permission.codename, 'nomeseparado': permission.name})

        if True:
            return Response(per, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)


    @action(
        detail=True,
        methods=['GET'],
    )
    def userPessoa(self, request, id, *args, **kwargs):

        pessoa = Pessoa.objects.get(user__id=id)
        pessoa = PessoaSerializer(pessoa)
        if pessoa:
            return Response(pessoa.data, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)


    @action(
        detail=True,
        methods=['POST'],
    )
    def removerPerfil(self, request, id ):
        user = User.objects.get(id=id)
        group_id = request.data['perfil']['id']
        sucursal_id = request.data['sucursal_id']
        sucursalUserGroups = SucursalUserGroup.objects.filter(user__id=id, sucursal__id=sucursal_id, group__id= group_id).first()
        sucursalUserGroups.delete()
        ar = []
        sucursalUserGroups = SucursalUserGroup.objects.filter(user__id=id, sucursal__id=sucursal_id)
        if (sucursalUserGroups):
            for sucursalUserGroup in sucursalUserGroups:
                group = Group.objects.get(id=sucursalUserGroup.group.id)
                ar.append({'id': group.id, 'name': group.name})
                # print(ar)

        if True:
            return Response(ar, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)


    @action(
        detail=True,
        methods=['POST'],
    )
    def adicionarPerfil(self, request, id):
        user = User.objects.get(id=id)
        group_id = request.data['perfil']['id']
        group = Group.objects.get(id = group_id)
        sucursal_id = request.data['sucursal_id']
        sucursal = Sucursal.objects.get(id=sucursal_id)
        sucursalUserGroups = SucursalUserGroup.objects.filter(user__id=id, sucursal__id=sucursal_id, group__id= group_id).first()

        if None==sucursalUserGroups:
            sucursalUserGroup = SucursalUserGroup()
            sucursalUserGroup.user = user
            sucursalUserGroup.group = group
            sucursalUserGroup.sucursal = sucursal
            sucursalUserGroup.save()
        sucursalUserGroups = SucursalUserGroup.objects.filter(user__id=id, sucursal__id=sucursal_id)

        ar = []
        if (sucursalUserGroups):
            for sucursalUserGroup in sucursalUserGroups:
                group = Group.objects.get(id=sucursalUserGroup.group.id)
                ar.append({'id': group.id, 'name': group.name})
                # print(ar)

        if True:
            return Response(ar, status.HTTP_200_OK)
        return Response([], status.HTTP_400_BAD_REQUEST)


class MeAPIView(generics.GenericAPIView):
    serializer_class = MeSerializer

    def get(self, request):
        serializer = self.serializer_class(
            request.user,
            context={'request': request}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


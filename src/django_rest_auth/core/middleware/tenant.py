
class TenantContextMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.entidade_id = request.headers.get('E')
        request.sucursal_id = request.headers.get('S')
        request.grupo_id = request.headers.get('G')
        request.tipo_entidade_id = request.headers.get('ET')
        request.lang_id = request.headers.get('L')

        return self.get_response(request)

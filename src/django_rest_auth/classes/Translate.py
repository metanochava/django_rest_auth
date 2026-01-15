import re
import importlib
from django.apps import apps
from django.core.cache import cache
from ..models import Idioma, Traducao  # import apenas os modelos necessários

CACHE_TIMEOUT = 60 * 60  # 1 hora


class Translate:

    @staticmethod
    def tdc(request, texto):
        """
        Função equivalente à função JS 'traducao'.
        Procura a tradução direta e aplica replace_traducao se necessário.
        """

        # 1️⃣ Obtém traduções
        translations = Translate.getTranslations(request)
        if not translations:
            return texto

        # 2️⃣ Normaliza a chave
        chave = texto.lower().strip()

        # 3️⃣ Busca tradução direta
        traducao_direta = translations.get(chave)
        if not traducao_direta:
            return texto

        # 4️⃣ Aplica placeholders se existirem
        return Translate.replace_traducao(texto, traducao_direta)

    @staticmethod
    def getTranslations(request):
        """
        Obtém traduções do cache, banco de dados e módulos lang dos apps.
        """
        lang_id = request.headers.get('L')
        if not lang_id:
            return {}

        try:
            idioma = Idioma.objects.get(id=lang_id)
        except Idioma.DoesNotExist:
            return {}

        lang_code = idioma.code.lower().replace('-', '')
        cache_key = f"traducao:{lang_code}"

        # 1️⃣ Tenta obter do cache
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        traducoes = {}

        # 2️⃣ Base de dados
        db_traducoes = Traducao.objects.filter(idioma_id=idioma.id)
        for tra in db_traducoes:
            traducoes[tra.chave.lower().strip()] = tra.traducao  # normaliza a chave

        # 3️⃣ Módulos lang dos apps
        for app in apps.get_app_configs():
            module_name = f"{app.name}.lang.{lang_code}"
            try:
                file_traducoes = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue

            if hasattr(file_traducoes, "key_value") and isinstance(file_traducoes.key_value, dict):
                # normaliza as chaves dos módulos também
                traducoes.update({k.lower().strip(): v for k, v in file_traducoes.key_value.items()})

        # 4️⃣ Salva no cache
        cache.set(cache_key, traducoes, CACHE_TIMEOUT)

        return traducoes

    @staticmethod
    def captura(texto=''):
        """
        Captura placeholders do tipo '%- valor -%' no texto.
        """
        return re.findall(r'\s*%-\s*[\w\s-]+\s*-%\s*', texto)

    @staticmethod
    def replace_traducao(texto='', texto_de_traducao=''):
        """
        Substitui placeholders no texto_de_traducao pelos valores capturados em texto.
        """
        valores = Translate.captura(texto)
        if not valores:
            return texto_de_traducao

        i = 0

        def replacer(_):
            nonlocal i
            v = valores[i] if i < len(valores) else None
            i += 1
            return (' ' + v.replace('%-', '').replace('-%', '').strip() + ' ') if v else ''

        return re.sub(r'\s*%-\s*[\w\s-]+\s*-%\s*', replacer, texto_de_traducao)

import json
from urllib import error, parse, request

from config import API_URL, REQUEST_TIMEOUT


class ApiError(Exception):
    pass


class ApiClient:

    def __init__(self, base_url: str = API_URL):
        self._base_url = base_url.rstrip("/")

    @property
    def base_url(self) -> str:
        return self._base_url

    def listar_localidades(self, incluir_inativos: bool = True) -> list[dict]:
        return self.get(
            "/localidades",
            {"incluir_inativos": incluir_inativos},
        )

    def listar_registros(
        self,
        incluir_inativos: bool = True,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        localidade_id: int | None = None,
    ) -> list[dict]:
        return self.get(
            "/registros",
            {
                "incluir_inativos": incluir_inativos,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "localidade_id": localidade_id,
            },
        )

    def listar_thresholds(self, incluir_inativos: bool = True) -> list[dict]:
        return self.get(
            "/thresholds",
            {"incluir_inativos": incluir_inativos},
        )

    def get(self, caminho: str, params: dict | None = None):
        return self._requisicao("GET", caminho, params=params)

    def post(self, caminho: str, dados: dict):
        return self._requisicao("POST", caminho, dados=dados)

    def put(self, caminho: str, dados: dict):
        return self._requisicao("PUT", caminho, dados=dados)

    def delete(self, caminho: str):
        return self._requisicao("DELETE", caminho)

    def baixar_csv(self, caminho: str, params: dict | None = None):
        url = self._montar_url(caminho, params)
        requisicao = request.Request(url, method="GET")

        try:
            with request.urlopen(
                requisicao,
                timeout=REQUEST_TIMEOUT,
            ) as resposta:
                conteudo = resposta.read()
                disposicao = resposta.headers.get(
                    "Content-Disposition",
                    "",
                )
        except error.HTTPError as erro:
            raise ApiError(self._mensagem_http(erro)) from erro
        except error.URLError as erro:
            raise ApiError(
                "Não foi possível conectar à API. Verifique se ela está em execução."
            ) from erro

        nome_arquivo = "exportacao.csv"

        if "filename=" in disposicao:
            nome_arquivo = disposicao.split("filename=")[-1].strip('"')

        return nome_arquivo, conteudo

    def _requisicao(
        self,
        metodo: str,
        caminho: str,
        params: dict | None = None,
        dados: dict | None = None,
    ):
        url = self._montar_url(caminho, params)
        corpo = None
        cabecalhos = {}

        if dados is not None:
            corpo = json.dumps(dados).encode("utf-8")
            cabecalhos["Content-Type"] = "application/json"

        requisicao = request.Request(
            url,
            data=corpo,
            headers=cabecalhos,
            method=metodo,
        )

        try:
            with request.urlopen(
                requisicao,
                timeout=REQUEST_TIMEOUT,
            ) as resposta:
                conteudo = resposta.read()

                if not conteudo:
                    return None

                return json.loads(conteudo.decode("utf-8"))
        except error.HTTPError as erro:
            raise ApiError(self._mensagem_http(erro)) from erro
        except error.URLError as erro:
            raise ApiError(
                "Não foi possível conectar à API. Verifique se ela está em execução."
            ) from erro
        except json.JSONDecodeError as erro:
            raise ApiError("A API retornou uma resposta inválida.") from erro

    def _montar_url(self, caminho: str, params: dict | None = None) -> str:
        url = f"{self._base_url}/{caminho.lstrip('/')}"

        if not params:
            return url

        filtrados = {
            chave: valor
            for chave, valor in params.items()
            if valor is not None and valor != ""
        }

        if not filtrados:
            return url

        return f"{url}?{parse.urlencode(filtrados, doseq=True)}"

    @staticmethod
    def _mensagem_http(erro: error.HTTPError) -> str:
        try:
            conteudo = erro.read().decode("utf-8")
            dados = json.loads(conteudo)
            detalhe = dados.get("erro", conteudo)
        except Exception:
            detalhe = "erro desconhecido"

        return f"HTTP {erro.code}: {detalhe}"

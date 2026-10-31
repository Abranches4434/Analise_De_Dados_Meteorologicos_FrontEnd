import tkinter as tk
from tkinter import ttk

from ui.base import BaseCadastroFrame


ESTADOS = (
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
)


class LocalidadesFrame(BaseCadastroFrame):

    titulo = "Localidades"

    def __init__(self, master, app):
        self._id = tk.StringVar()
        self._nome = tk.StringVar()
        self._cidade = tk.StringVar()
        self._estado = tk.StringVar()
        self._latitude = tk.StringVar()
        self._longitude = tk.StringVar()
        self._ativo = tk.BooleanVar(value=True)
        self._dados_por_id = {}
        super().__init__(master, app)

    def _montar_conteudo(self):
        formulario = ttk.LabelFrame(
            self,
            text="Dados da localidade",
            padding=10,
        )
        formulario.pack(fill="x", pady=(0, 8))

        self._id_entry = self._criar_entrada(
            formulario, 0, 0, "ID:", self._id, largura=10
        )
        self._id_entry.configure(state="readonly")

        self._criar_entrada(
            formulario, 0, 2, "Nome:", self._nome, largura=30
        )
        self._criar_entrada(
            formulario, 0, 4, "Cidade:", self._cidade, largura=24
        )

        self._criar_combo(
            formulario, 1, 0, "Estado:", self._estado, ESTADOS
        )
        self._criar_entrada(
            formulario, 1, 2, "Latitude:", self._latitude
        )
        self._criar_entrada(
            formulario, 1, 4, "Longitude:", self._longitude
        )

        self._criar_check(formulario, 2, 0, "Ativa", self._ativo)

        tabela = ttk.LabelFrame(
            self,
            text="Localidades cadastradas",
            padding=6,
        )
        tabela.pack(fill="both", expand=True)

        colunas = (
            ("ID", "ID"),
            ("Nome", "Nome"),
            ("Cidade", "Cidade"),
            ("Estado", "UF"),
            ("Latitude", "Latitude"),
            ("Longitude", "Longitude"),
            ("Ativo", "Ativa"),
        )
        self._tree = self._criar_tabela(
            tabela,
            colunas,
            larguras=(60, 180, 150, 60, 110, 110, 70),
        )
        self._tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _montar_botoes(self):
        self._criar_barra_botoes(
            self,
            (
                ("Novo / Limpar", self.limpar),
                ("Salvar", self.salvar),
                ("Excluir (inativar)", self.excluir),
                ("Atualizar lista", self.carregar),
            ),
        )

    def carregar(self):
        def acao():
            localidades = self.api.listar_localidades()
            self._dados_por_id = {
                str(localidade["IDLocalidade"]): localidade
                for localidade in localidades
            }
            linhas = [
                (
                    localidade["IDLocalidade"],
                    localidade["Nome"],
                    localidade["Cidade"],
                    localidade["Estado"],
                    f"{localidade['Latitude']:.6f}",
                    f"{localidade['Longitude']:.6f}",
                    "Sim" if localidade["Ativo"] else "Não",
                )
                for localidade in localidades
            ]
            self._preencher_tabela(self._tree, linhas)
            self.app.atualizar_localidades()

        self._executar(acao)

    def _ao_selecionar(self, _evento=None):
        selecao = self._obter_selecao(self._tree)

        if selecao is None:
            return

        localidade = self._dados_por_id.get(str(selecao[0]))

        if localidade is None:
            return

        self._id.set(localidade["IDLocalidade"])
        self._nome.set(localidade["Nome"])
        self._cidade.set(localidade["Cidade"])
        self._estado.set(localidade["Estado"])
        self._latitude.set(str(localidade["Latitude"]))
        self._longitude.set(str(localidade["Longitude"]))
        self._ativo.set(localidade["Ativo"])

    def salvar(self):
        try:
            dados = self._montar_payload()
        except ValueError as erro:
            self._mostrar_erro(erro)
            return

        def acao():
            if self._id.get():
                self.api.put(f"/localidades/{self._id.get()}", dados)
            else:
                self.api.post("/localidades", dados)
            self.carregar()
            self.limpar()

        self._executar(acao, "Localidade salva com sucesso.")

    def excluir(self):
        if not self._id.get():
            self._mostrar_erro("Selecione uma localidade para inativar.")
            return

        if not self._confirmar(
            "Deseja inativar a localidade selecionada?"
        ):
            return

        def acao():
            self.api.delete(f"/localidades/{self._id.get()}")
            self.carregar()
            self.limpar()

        self._executar(acao, "Localidade inativada.")

    def limpar(self):
        self._id.set("")
        self._nome.set("")
        self._cidade.set("")
        self._estado.set("")
        self._latitude.set("")
        self._longitude.set("")
        self._ativo.set(True)
        self._tree.selection_remove(*self._tree.selection())

    def _montar_payload(self):
        nome = self._nome.get().strip()
        cidade = self._cidade.get().strip()
        estado = self._estado.get().strip()

        if not nome:
            raise ValueError("Informe o nome da localidade.")
        if not cidade:
            raise ValueError("Informe a cidade.")
        if not estado:
            raise ValueError("Selecione o estado.")

        latitude = self._converter_decimal(
            self._latitude.get(),
            "latitude",
        )
        longitude = self._converter_decimal(
            self._longitude.get(),
            "longitude",
        )

        if not -90 <= latitude <= 90:
            raise ValueError("A latitude deve estar entre -90 e 90.")
        if not -180 <= longitude <= 180:
            raise ValueError("A longitude deve estar entre -180 e 180.")

        return {
            "Nome": nome,
            "Cidade": cidade,
            "Estado": estado,
            "Latitude": latitude,
            "Longitude": longitude,
            "Ativo": self._ativo.get(),
        }

    @staticmethod
    def _converter_decimal(valor, nome):
        try:
            return float(valor.strip().replace(",", "."))
        except ValueError as erro:
            raise ValueError(f"Informe uma {nome} válida.") from erro

import tkinter as tk
from tkinter import ttk

from ui.base import BaseCadastroFrame
from ui.tema import CORES


VARIAVEIS = (
    "TEMPERATURA",
    "UMIDADE",
    "PRECIPITACAO",
    "VELOCIDADEVENTO",
    "PRESSAOATMOSFERICA",
)

TIPOS_LIMIAR = ("MAXIMO", "MINIMO", "DIASSEMCHUVA")

ESTACOES = ("ANUAL", "PRIMAVERA", "VERAO", "OUTONO", "INVERNO")


class ThresholdsFrame(BaseCadastroFrame):

    titulo = "Thresholds"
    subtitulo = "Limiares meteorológicos por localidade e estação"
    cor_destaque = CORES["laranja"]

    def __init__(self, master, app):
        self._id = tk.StringVar()
        self._localidade = tk.StringVar()
        self._variavel = tk.StringVar(value="TEMPERATURA")
        self._tipo = tk.StringVar(value="MAXIMO")
        self._estacao = tk.StringVar(value="ANUAL")
        self._valor = tk.StringVar()
        self._ativo = tk.BooleanVar(value=True)

        self._mapa_localidades = {}
        self._rotulos_localidades = {}
        self._rotulo_por_id = {}
        super().__init__(master, app)

    def _montar_conteudo(self):
        formulario = ttk.LabelFrame(
            self,
            text="Dados do threshold",
            padding=10,
        )
        formulario.pack(fill="x", pady=(0, 8))

        self._id_entry = self._criar_entrada(
            formulario, 0, 0, "ID:", self._id, largura=10
        )
        self._id_entry.configure(state="readonly")

        self._localidade_combo = self._criar_combo(
            formulario,
            0,
            2,
            "Localidade:",
            self._localidade,
            [],
            largura=28,
        )
        self._criar_check(formulario, 0, 4, "Ativo", self._ativo)

        self._criar_combo(
            formulario,
            1,
            0,
            "Variável:",
            self._variavel,
            VARIAVEIS,
            largura=24,
        )
        self._criar_combo(
            formulario,
            1,
            2,
            "Tipo de limiar:",
            self._tipo,
            TIPOS_LIMIAR,
            largura=18,
        )
        self._criar_combo(
            formulario,
            1,
            4,
            "Estação:",
            self._estacao,
            ESTACOES,
            largura=14,
        )

        self._criar_entrada(
            formulario, 2, 0, "Valor:", self._valor
        )

        tabela = ttk.LabelFrame(
            self,
            text="Thresholds cadastrados",
            padding=6,
        )
        tabela.pack(fill="both", expand=True)

        colunas = (
            ("ID", "ID"),
            ("Localidade", "Localidade"),
            ("Variavel", "Variável"),
            ("TipoLimiar", "Tipo"),
            ("Estacao", "Estação"),
            ("Valor", "Valor"),
            ("Ativo", "Ativo"),
        )
        self._tree = self._criar_tabela(
            tabela,
            colunas,
            larguras=(60, 190, 170, 120, 100, 80, 60),
        )
        self._tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _montar_botoes(self):
        self._criar_barra_botoes(
            self,
            (
                ("Novo / Limpar", self.limpar, "neutro"),
                ("Salvar", self.salvar, "sucesso"),
                ("Excluir (inativar)", self.excluir, "perigo"),
                ("Atualizar lista", self.carregar, "laranja"),
            ),
        )

    def atualizar_localidades(self, localidades):
        ativos = [
            localidade
            for localidade in localidades
            if localidade["Ativo"]
        ]
        self._mapa_localidades = {
            localidade["IDLocalidade"]: localidade
            for localidade in localidades
        }
        self._rotulos_localidades = {
            f"{localidade['IDLocalidade']} - {localidade['Nome']}": localidade[
                "IDLocalidade"
            ]
            for localidade in ativos
        }
        self._rotulo_por_id = {
            localidade["IDLocalidade"]: (
                f"{localidade['IDLocalidade']} - {localidade['Nome']}"
            )
            for localidade in ativos
        }

        rotulos = list(self._rotulos_localidades)
        self._localidade_combo.configure(values=rotulos)

        if self._localidade.get() not in rotulos:
            self._localidade.set("")

    def carregar(self):
        def acao():
            thresholds = self.api.listar_thresholds()
            linhas = [
                (
                    threshold["IDThreshold"],
                    self._nome_localidade(threshold["FKLocalidade"]),
                    threshold["Variavel"],
                    threshold["TipoLimiar"],
                    threshold["EstacaoDoAno"],
                    threshold["Valor"],
                    "Sim" if threshold["Ativo"] else "Não",
                )
                for threshold in thresholds
            ]
            self._preencher_tabela(self._tree, linhas)

        self._executar(acao)

    def _ao_selecionar(self, _evento=None):
        selecao = self._obter_selecao(self._tree)

        if selecao is None:
            return

        threshold_id = int(selecao[0])
        threshold = self.api.get(f"/thresholds/{threshold_id}")

        if threshold is None:
            return

        self._id.set(threshold["IDThreshold"])
        self._localidade.set(
            self._rotulo_por_id.get(
                threshold["FKLocalidade"],
                str(threshold["FKLocalidade"]),
            )
        )
        self._variavel.set(threshold["Variavel"])
        self._tipo.set(threshold["TipoLimiar"])
        self._estacao.set(threshold["EstacaoDoAno"])
        self._valor.set(threshold["Valor"])
        self._ativo.set(threshold["Ativo"])

    def salvar(self):
        try:
            dados = self._montar_payload()
        except ValueError as erro:
            self._mostrar_erro(erro)
            return

        def acao():
            if self._id.get():
                self.api.put(f"/thresholds/{self._id.get()}", dados)
            else:
                self.api.post("/thresholds", dados)
            self.carregar()
            self.limpar()

        self._executar(acao, "Threshold salvo com sucesso.")

    def excluir(self):
        if not self._id.get():
            self._mostrar_erro("Selecione um threshold para inativar.")
            return

        if not self._confirmar(
            "Deseja inativar o threshold selecionado?"
        ):
            return

        def acao():
            self.api.delete(f"/thresholds/{self._id.get()}")
            self.carregar()
            self.limpar()

        self._executar(acao, "Threshold inativado.")

    def limpar(self):
        self._id.set("")
        self._localidade.set("")
        self._variavel.set("TEMPERATURA")
        self._tipo.set("MAXIMO")
        self._estacao.set("ANUAL")
        self._valor.set("")
        self._ativo.set(True)
        self._tree.selection_remove(*self._tree.selection())

    def _montar_payload(self):
        if not self._localidade.get():
            raise ValueError("Selecione a localidade do threshold.")

        localidade_id = self._rotulos_localidades.get(
            self._localidade.get()
        )

        if localidade_id is None:
            raise ValueError("A localidade selecionada não está ativa.")

        try:
            valor = float(self._valor.get().strip().replace(",", "."))
        except ValueError as erro:
            raise ValueError("Informe um valor numérico válido.") from erro

        return {
            "FKLocalidade": localidade_id,
            "Variavel": self._variavel.get(),
            "TipoLimiar": self._tipo.get(),
            "EstacaoDoAno": self._estacao.get(),
            "Valor": valor,
            "Ativo": self._ativo.get(),
        }

    def _nome_localidade(self, localidade_id):
        localidade = self._mapa_localidades.get(localidade_id)
        return localidade["Nome"] if localidade else str(localidade_id)

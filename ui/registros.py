import tkinter as tk
from datetime import date, time
from tkinter import ttk

from ui.base import BaseCadastroFrame


class RegistrosFrame(BaseCadastroFrame):

    titulo = "Registros climáticos"

    def __init__(self, master, app):
        self._id = tk.StringVar()
        self._localidade = tk.StringVar()
        self._data = tk.StringVar()
        self._hora = tk.StringVar()
        self._temp_max = tk.StringVar()
        self._temp_min = tk.StringVar()
        self._temp_media = tk.StringVar()
        self._umidade = tk.StringVar()
        self._precipitacao = tk.StringVar()
        self._vento = tk.StringVar()
        self._pressao = tk.StringVar()
        self._ativo = tk.BooleanVar(value=True)

        self._filtro_inicio = tk.StringVar()
        self._filtro_fim = tk.StringVar()
        self._filtro_localidade = tk.StringVar(value="Todas")

        self._mapa_localidades = {}
        self._rotulos_localidades = {}
        self._rotulo_por_id = {}
        super().__init__(master, app)

    def _montar_conteudo(self):
        filtros = ttk.LabelFrame(self, text="Filtros da listagem", padding=8)
        filtros.pack(fill="x", pady=(0, 8))

        self._criar_entrada(
            filtros, 0, 0, "Data início:", self._filtro_inicio
        )
        self._criar_entrada(
            filtros, 0, 2, "Data fim:", self._filtro_fim
        )
        self._filtro_combo = self._criar_combo(
            filtros,
            0,
            4,
            "Localidade:",
            self._filtro_localidade,
            ["Todas"],
            largura=28,
        )

        acoes = ttk.Frame(filtros)
        acoes.grid(row=1, column=0, columnspan=6, sticky="w", pady=(4, 0))
        ttk.Button(
            acoes,
            text="Filtrar",
            command=self.carregar,
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            acoes,
            text="Limpar filtros",
            command=self._limpar_filtros,
        ).pack(side="left")

        formulario = ttk.LabelFrame(
            self,
            text="Dados do registro",
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
        self._criar_check(
            formulario, 0, 4, "Ativo", self._ativo
        )

        self._criar_entrada(
            formulario, 1, 0, "Data (AAAA-MM-DD):", self._data
        )
        self._criar_entrada(
            formulario, 1, 2, "Hora (HH:MM:SS):", self._hora
        )
        self._criar_entrada(
            formulario, 1, 4, "Temp. máxima:", self._temp_max
        )

        self._criar_entrada(
            formulario, 2, 0, "Temp. mínima:", self._temp_min
        )
        self._criar_entrada(
            formulario, 2, 2, "Temp. média:", self._temp_media
        )
        self._criar_entrada(
            formulario, 2, 4, "Umidade (%):", self._umidade
        )

        self._criar_entrada(
            formulario, 3, 0, "Precipitação:", self._precipitacao
        )
        self._criar_entrada(
            formulario, 3, 2, "Vento:", self._vento
        )
        self._criar_entrada(
            formulario, 3, 4, "Pressão:", self._pressao
        )

        tabela = ttk.LabelFrame(
            self,
            text="Registros cadastrados",
            padding=6,
        )
        tabela.pack(fill="both", expand=True)

        colunas = (
            ("ID", "ID"),
            ("Localidade", "Localidade"),
            ("Data", "Data"),
            ("Hora", "Hora"),
            ("TempMax", "Máx."),
            ("TempMin", "Mín."),
            ("TempMedia", "Média"),
            ("Umidade", "Umidade"),
            ("Precipitacao", "Chuva"),
            ("Vento", "Vento"),
            ("Pressao", "Pressão"),
            ("Ativo", "Ativo"),
        )
        self._tree = self._criar_tabela(
            tabela,
            colunas,
            larguras=(
                60, 170, 95, 80, 65, 65, 65, 75, 70, 65, 75, 60
            ),
            altura=11,
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
        self._filtro_combo.configure(values=["Todas", *rotulos])

        if self._localidade.get() not in rotulos:
            self._localidade.set("")

    def carregar(self):
        def acao():
            data_inicio = self._validar_data_filtro(
                self._filtro_inicio.get(),
                "data de início",
            )
            data_fim = self._validar_data_filtro(
                self._filtro_fim.get(),
                "data final",
            )
            localidade_id = None

            if self._filtro_localidade.get() != "Todas":
                localidade_id = self._rotulos_localidades.get(
                    self._filtro_localidade.get()
                )

            registros = self.api.listar_registros(
                incluir_inativos=True,
                data_inicio=data_inicio,
                data_fim=data_fim,
                localidade_id=localidade_id,
            )
            linhas = [
                (
                    registro["IDRegistrosClimaticos"],
                    self._nome_localidade(registro["FKLocalidade"]),
                    registro["Data"],
                    registro["Hora"],
                    registro["TempMax"],
                    registro["TempMin"],
                    registro["TempMedia"],
                    registro["UmidadeRelativa"],
                    registro["Precipitacao"],
                    registro["VelocidadeVento"],
                    registro["PressaoAtmosferica"],
                    "Sim" if registro["Ativo"] else "Não",
                )
                for registro in registros
            ]
            self._preencher_tabela(self._tree, linhas)

        self._executar(acao)

    def _ao_selecionar(self, _evento=None):
        selecao = self._obter_selecao(self._tree)

        if selecao is None:
            return

        registro_id = int(selecao[0])
        registro = self.api.get(f"/registros/{registro_id}")

        if registro is None:
            return

        self._id.set(registro["IDRegistrosClimaticos"])
        self._localidade.set(
            self._rotulo_por_id.get(
                registro["FKLocalidade"],
                str(registro["FKLocalidade"]),
            )
        )
        self._data.set(registro["Data"])
        self._hora.set(registro["Hora"])
        self._temp_max.set(registro["TempMax"])
        self._temp_min.set(registro["TempMin"])
        self._temp_media.set(registro["TempMedia"])
        self._umidade.set(registro["UmidadeRelativa"])
        self._precipitacao.set(registro["Precipitacao"])
        self._vento.set(registro["VelocidadeVento"])
        self._pressao.set(registro["PressaoAtmosferica"])
        self._ativo.set(registro["Ativo"])

    def salvar(self):
        try:
            dados = self._montar_payload()
        except ValueError as erro:
            self._mostrar_erro(erro)
            return

        def acao():
            if self._id.get():
                self.api.put(f"/registros/{self._id.get()}", dados)
            else:
                self.api.post("/registros", dados)
            self.carregar()
            self.limpar()

        self._executar(acao, "Registro salvo com sucesso.")

    def excluir(self):
        if not self._id.get():
            self._mostrar_erro("Selecione um registro para inativar.")
            return

        if not self._confirmar(
            "Deseja inativar o registro selecionado?"
        ):
            return

        def acao():
            self.api.delete(f"/registros/{self._id.get()}")
            self.carregar()
            self.limpar()

        self._executar(acao, "Registro inativado.")

    def limpar(self):
        self._id.set("")
        self._localidade.set("")
        self._data.set("")
        self._hora.set("")
        self._temp_max.set("")
        self._temp_min.set("")
        self._temp_media.set("")
        self._umidade.set("")
        self._precipitacao.set("")
        self._vento.set("")
        self._pressao.set("")
        self._ativo.set(True)
        self._tree.selection_remove(*self._tree.selection())

    def _limpar_filtros(self):
        self._filtro_inicio.set("")
        self._filtro_fim.set("")
        self._filtro_localidade.set("Todas")
        self.carregar()

    def _montar_payload(self):
        if not self._localidade.get():
            raise ValueError("Selecione a localidade do registro.")

        localidade_id = self._rotulos_localidades.get(
            self._localidade.get()
        )

        if localidade_id is None:
            raise ValueError("A localidade selecionada não está ativa.")

        return {
            "FKLocalidade": localidade_id,
            "Data": self._validar_data(self._data.get()),
            "Hora": self._validar_hora(self._hora.get()),
            "TempMax": self._converter_numero(
                self._temp_max.get(), "temperatura máxima"
            ),
            "TempMin": self._converter_numero(
                self._temp_min.get(), "temperatura mínima"
            ),
            "TempMedia": self._converter_numero(
                self._temp_media.get(), "temperatura média"
            ),
            "UmidadeRelativa": self._converter_numero(
                self._umidade.get(), "umidade relativa"
            ),
            "Precipitacao": self._converter_numero(
                self._precipitacao.get(), "precipitação"
            ),
            "VelocidadeVento": self._converter_numero(
                self._vento.get(), "velocidade do vento"
            ),
            "PressaoAtmosferica": self._converter_numero(
                self._pressao.get(), "pressão atmosférica"
            ),
            "Ativo": self._ativo.get(),
        }

    @staticmethod
    def _converter_numero(valor, nome):
        try:
            return float(valor.strip().replace(",", "."))
        except ValueError as erro:
            raise ValueError(f"Informe um valor válido para {nome}.") from erro

    @staticmethod
    def _validar_data(valor):
        try:
            return date.fromisoformat(valor.strip()).isoformat()
        except ValueError as erro:
            raise ValueError(
                "Informe a data no formato AAAA-MM-DD."
            ) from erro

    @staticmethod
    def _validar_hora(valor):
        try:
            return time.fromisoformat(valor.strip()).isoformat()
        except ValueError as erro:
            raise ValueError(
                "Informe a hora no formato HH:MM ou HH:MM:SS."
            ) from erro

    @staticmethod
    def _validar_data_filtro(valor, nome):
        if not valor.strip():
            return None

        try:
            return date.fromisoformat(valor.strip()).isoformat()
        except ValueError as erro:
            raise ValueError(
                f"Informe a {nome} no formato AAAA-MM-DD."
            ) from erro

    def _nome_localidade(self, localidade_id):
        localidade = self._mapa_localidades.get(localidade_id)
        return localidade["Nome"] if localidade else str(localidade_id)

import tkinter as tk
from datetime import date
from tkinter import filedialog, ttk

from ui.base import BaseFrame
from ui.tema import (
    CORES,
    BotaoAnimado,
    configurar_listbox,
    criar_cabecalho_pagina,
)


TIPOS_EXPORTACAO = (
    "registros",
    "estatisticas",
    "comparacao",
    "eventos",
    "sazonalidade",
)


class AnalisesFrame(BaseFrame):

    titulo = "Análises"
    subtitulo = "Indicadores, comparações, eventos extremos e exportação"
    cor_destaque = CORES["roxo"]

    def _construir(self):
        self._data_inicio = tk.StringVar()
        self._data_fim = tk.StringVar()
        self._localidade = tk.StringVar(value="Todas")
        self._agrupamento = tk.StringVar(value="mes")
        self._tipo_exportacao = tk.StringVar(value="estatisticas")

        self._mapa_localidades = {}
        self._rotulos_localidades = {}
        self._rotulo_por_id = {}
        self._tree = None

        criar_cabecalho_pagina(
            self,
            self.titulo,
            self.subtitulo,
            self.cor_destaque,
        )

        filtros = ttk.LabelFrame(self, text="Filtros", padding=8)
        filtros.pack(fill="x", pady=(0, 8))
        filtros.columnconfigure(7, weight=1)

        self._criar_entrada(
            filtros, 0, 0, "Data início:", self._data_inicio, largura=16
        )
        self._criar_entrada(
            filtros, 0, 2, "Data fim:", self._data_fim, largura=16
        )
        self._localidade_combo = self._criar_combo(
            filtros,
            0,
            4,
            "Localidade:",
            self._localidade,
            ["Todas"],
            largura=20,
        )
        self._criar_combo(
            filtros,
            0,
            6,
            "Agrupamento:",
            self._agrupamento,
            ("mes", "estacao"),
            largura=12,
        )

        comparacao = ttk.LabelFrame(
            filtros,
            text="Localidades para comparação",
            padding=6,
        )
        comparacao.grid(
            row=1,
            column=0,
            columnspan=8,
            sticky="ew",
            pady=(6, 0),
        )
        self._lista_comparacao = tk.Listbox(
            comparacao,
            selectmode="extended",
            height=3,
            exportselection=False,
        )
        configurar_listbox(self._lista_comparacao)
        self._lista_comparacao.pack(fill="x")

        acoes = ttk.Frame(self)
        acoes.pack(fill="x", pady=(0, 6))

        for texto, comando, variante in (
            ("Estatísticas", self.carregar_estatisticas, "azul"),
            ("Comparação", self.carregar_comparacao, "teal"),
            ("Eventos extremos", self.carregar_eventos, "laranja"),
            ("Sazonalidade", self.carregar_sazonalidade, "roxo"),
        ):
            BotaoAnimado(
                acoes,
                texto,
                comando,
                variante=variante,
            ).pack(side="left", padx=(0, 8))

        exportacao = ttk.Frame(acoes, style="Pagina.TFrame")
        exportacao.pack(side="right", padx=(8, 0))
        ttk.Label(exportacao, text="Exportar:").pack(side="left")
        self._combo_exportacao = ttk.Combobox(
            exportacao,
            textvariable=self._tipo_exportacao,
            values=TIPOS_EXPORTACAO,
            state="readonly",
            width=14,
        )
        self._combo_exportacao.pack(side="left", padx=(6, 6))
        BotaoAnimado(
            exportacao,
            "Salvar CSV",
            self.exportar,
            variante="sucesso",
            altura=32,
        ).pack(side="left")

        self._titulo_resultado = ttk.Label(
            self,
            text="Selecione uma análise.",
            style="Resultado.TLabel",
        )
        self._titulo_resultado.pack(anchor="w", pady=(0, 4))

        resultado = ttk.LabelFrame(
            self,
            text="Resultado",
            padding=6,
        )
        resultado.pack(fill="both", expand=True)
        self._container_resultado = resultado

        self._status = ttk.Label(self, text="", style="StatusPagina.TLabel")
        self._status.pack(anchor="w", pady=(6, 0))

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
        self._localidade_combo.configure(values=["Todas", *rotulos])

        if self._localidade.get() not in ["Todas", *rotulos]:
            self._localidade.set("Todas")

        selecionados = {
            self._lista_comparacao.get(indice)
            for indice in self._lista_comparacao.curselection()
        }
        self._lista_comparacao.delete(0, tk.END)

        for rotulo in rotulos:
            self._lista_comparacao.insert(tk.END, rotulo)

        for indice, rotulo in enumerate(rotulos):
            if rotulo in selecionados:
                self._lista_comparacao.selection_set(indice)

    def carregar_estatisticas(self):
        def acao():
            resposta = self.api.get(
                "/analises/estatisticas",
                self._parametros_basicos(),
            )
            linhas = [
                (
                    estatistica["Variavel"],
                    estatistica["Descricao"],
                    estatistica["Media"],
                    estatistica["Mediana"],
                    estatistica["Maximo"],
                    estatistica["Minimo"],
                    estatistica["Quantidade"],
                )
                for estatistica in resposta["Estatisticas"]
            ]
            self._mostrar_resultado(
                f"Estatísticas — {resposta['Nome']}",
                (
                    ("Variavel", "Variável"),
                    ("Descricao", "Descrição"),
                    ("Media", "Média"),
                    ("Mediana", "Mediana"),
                    ("Maximo", "Máximo"),
                    ("Minimo", "Mínimo"),
                    ("Quantidade", "Qtd."),
                ),
                linhas,
                (130, 190, 90, 90, 90, 90, 70),
                f"{resposta['QuantidadeRegistros']} registros no período.",
            )

        self._executar(acao)

    def carregar_comparacao(self):
        localidade_ids = self._ids_comparacao()

        if len(localidade_ids) < 2:
            self._mostrar_erro(
                "Selecione pelo menos duas localidades na lista de comparação."
            )
            return

        def acao():
            parametros = self._parametros_basicos()
            parametros["localidade_ids"] = ",".join(
                str(item) for item in localidade_ids
            )
            resposta = self.api.get(
                "/analises/comparacao",
                parametros,
            )
            linhas = []

            for localidade in resposta["Localidades"]:
                for estatistica in localidade["Estatisticas"]:
                    linhas.append(
                        (
                            localidade["Nome"],
                            estatistica["Variavel"],
                            estatistica["Media"],
                            estatistica["Mediana"],
                            estatistica["Maximo"],
                            estatistica["Minimo"],
                            estatistica["Quantidade"],
                        )
                    )

            self._mostrar_resultado(
                "Comparação de localidades",
                (
                    ("Localidade", "Localidade"),
                    ("Variavel", "Variável"),
                    ("Media", "Média"),
                    ("Mediana", "Mediana"),
                    ("Maximo", "Máximo"),
                    ("Minimo", "Mínimo"),
                    ("Quantidade", "Qtd."),
                ),
                linhas,
                (200, 130, 90, 90, 90, 90, 70),
                f"{len(resposta['Localidades'])} localidades comparadas.",
            )

        self._executar(acao)

    def carregar_eventos(self):
        localidade_id = self._localidade_id()

        if localidade_id is None:
            self._mostrar_erro(
                "Selecione uma localidade para consultar eventos extremos."
            )
            return

        def acao():
            parametros = self._parametros_basicos()
            parametros["localidade_id"] = localidade_id
            resposta = self.api.get(
                "/analises/eventos-extremos",
                parametros,
            )
            linhas = [
                (
                    evento["Variavel"],
                    evento["TipoLimiar"],
                    evento["EstacaoDoAno"],
                    evento["Limiar"],
                    evento.get("Valor", ""),
                    evento.get("Data", ""),
                    evento.get("Hora", ""),
                    evento.get("DataInicio", ""),
                    evento.get("DataFim", ""),
                    evento.get("Dias", ""),
                    evento["Descricao"],
                )
                for evento in resposta["Eventos"]
            ]
            self._mostrar_resultado(
                f"Eventos extremos — {resposta['Nome']}",
                (
                    ("Variavel", "Variável"),
                    ("Tipo", "Tipo"),
                    ("Estacao", "Estação"),
                    ("Limiar", "Limiar"),
                    ("Valor", "Valor"),
                    ("Data", "Data"),
                    ("Hora", "Hora"),
                    ("DataInicio", "Início"),
                    ("DataFim", "Fim"),
                    ("Dias", "Dias"),
                    ("Descricao", "Descrição"),
                ),
                linhas,
                (120, 110, 85, 70, 70, 90, 70, 90, 90, 50, 360),
                resposta.get(
                    "Aviso",
                    f"{resposta['QuantidadeEventos']} eventos encontrados.",
                ),
            )

        self._executar(acao)

    def carregar_sazonalidade(self):
        def acao():
            parametros = self._parametros_basicos()
            parametros["agrupamento"] = self._agrupamento.get()
            resposta = self.api.get(
                "/analises/sazonalidade",
                parametros,
            )
            linhas = [
                (
                    grupo["Grupo"],
                    grupo["Quantidade"],
                    self._formatar(grupo["Medias"]["TempMax"]),
                    self._formatar(grupo["Medias"]["TempMin"]),
                    self._formatar(grupo["Medias"]["TempMedia"]),
                    self._formatar(grupo["Medias"]["UmidadeRelativa"]),
                    self._formatar(grupo["Medias"]["Precipitacao"]),
                    self._formatar(grupo["Medias"]["VelocidadeVento"]),
                    self._formatar(grupo["Medias"]["PressaoAtmosferica"]),
                )
                for grupo in resposta["Grupos"]
            ]
            self._mostrar_resultado(
                f"Sazonalidade — {resposta['Nome']}",
                (
                    ("Grupo", "Grupo"),
                    ("Quantidade", "Qtd."),
                    ("TempMax", "Máx."),
                    ("TempMin", "Mín."),
                    ("TempMedia", "Média"),
                    ("Umidade", "Umidade"),
                    ("Precipitacao", "Chuva"),
                    ("Vento", "Vento"),
                    ("Pressao", "Pressão"),
                ),
                linhas,
                (110, 70, 80, 80, 80, 90, 80, 80, 90),
                f"Agrupamento por {resposta['Agrupamento']}.",
            )

        self._executar(acao)

    def exportar(self):
        tipo = self._tipo_exportacao.get()

        try:
            parametros = self._parametros_basicos()
            localidade_id = self._localidade_id()
            localidade_ids = self._ids_comparacao()

            if tipo == "eventos" and localidade_id is None:
                raise ValueError(
                    "Selecione uma localidade para exportar eventos extremos."
                )

            if tipo == "comparacao" and len(localidade_ids) < 2:
                raise ValueError(
                    "Selecione pelo menos duas localidades para exportar a comparação."
                )

            if localidade_id is not None:
                parametros["localidade_id"] = localidade_id

            if localidade_ids:
                parametros["localidade_ids"] = ",".join(
                    str(item) for item in localidade_ids
                )

            parametros["agrupamento"] = self._agrupamento.get()
        except ValueError as erro:
            self._mostrar_erro(erro)
            return

        def acao():
            nome_sugerido, conteudo = self.api.baixar_csv(
                f"/exportacoes/{tipo}",
                parametros,
            )
            caminho = filedialog.asksaveasfilename(
                parent=self,
                title="Salvar exportação",
                initialfile=nome_sugerido,
                defaultextension=".csv",
                filetypes=(("Arquivo CSV", "*.csv"), ("Todos", "*.*")),
            )

            if not caminho:
                return

            with open(caminho, "wb") as arquivo:
                arquivo.write(conteudo)

            self._mostrar_info(f"Arquivo salvo em:\n{caminho}")

        self._executar(acao)

    def _mostrar_resultado(
        self,
        titulo,
        colunas,
        linhas,
        larguras,
        resumo,
    ):
        self._titulo_resultado.configure(text=titulo)

        for filho in self._container_resultado.winfo_children():
            filho.destroy()

        self._tree = self._criar_tabela(
            self._container_resultado,
            colunas,
            larguras=larguras,
            altura=15,
            selecao="extended",
        )
        self._preencher_tabela(self._tree, linhas)
        self._status.configure(text=resumo)

    def _parametros_basicos(self):
        return {
            "data_inicio": self._validar_data(
                self._data_inicio.get(),
                "data de início",
            ),
            "data_fim": self._validar_data(
                self._data_fim.get(),
                "data final",
            ),
        }

    def _localidade_id(self):
        if self._localidade.get() == "Todas":
            return None

        return self._rotulos_localidades.get(self._localidade.get())

    def _ids_comparacao(self):
        return [
            self._rotulos_localidades[self._lista_comparacao.get(indice)]
            for indice in self._lista_comparacao.curselection()
            if self._lista_comparacao.get(indice) in self._rotulos_localidades
        ]

    @staticmethod
    def _validar_data(valor, nome):
        if not valor.strip():
            return None

        try:
            return date.fromisoformat(valor.strip()).isoformat()
        except ValueError as erro:
            raise ValueError(
                f"Informe a {nome} no formato AAAA-MM-DD."
            ) from erro

    @staticmethod
    def _formatar(valor):
        if valor is None:
            return "-"

        return f"{valor:.2f}"

import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk

from ui.dialogos import confirmar, mostrar_erro, mostrar_info
from ui.tema import (
    CORES,
    BotaoAnimado,
    configurar_hover_tabela,
    criar_cabecalho_pagina,
)


class BaseFrame(ttk.Frame, ABC):

    def __init__(self, master, app):
        super().__init__(master, padding=10, style="Pagina.TFrame")
        self._app = app
        self._api = app.api
        self._construir()

    @property
    def app(self):
        return self._app

    @property
    def api(self):
        return self._api

    @abstractmethod
    def _construir(self):
        raise NotImplementedError

    def _criar_tabela(
        self,
        parent,
        colunas,
        larguras=None,
        altura=14,
        selecao="browse",
    ):
        container = ttk.Frame(parent, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(
            container,
            columns=[coluna[0] for coluna in colunas],
            show="headings",
            height=altura,
            selectmode=selecao,
        )

        for indice, (chave, rotulo) in enumerate(colunas):
            tree.heading(chave, text=rotulo)
            largura = larguras[indice] if larguras else 120
            tree.column(chave, width=largura, anchor="w")

        barra_vertical = ttk.Scrollbar(
            container,
            orient="vertical",
            command=tree.yview,
        )
        barra_horizontal = ttk.Scrollbar(
            container,
            orient="horizontal",
            command=tree.xview,
        )
        tree.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )

        configurar_hover_tabela(tree)

        tree.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        return tree

    @staticmethod
    def _preencher_tabela(tree, linhas):
        tree.delete(*tree.get_children())
        tree._item_hover = None

        for indice, linha in enumerate(linhas):
            tree.insert(
                "",
                "end",
                values=linha,
                tags=("linha_par" if indice % 2 == 0 else "linha_impar",),
            )

    @staticmethod
    def _obter_selecao(tree):
        selecionados = tree.selection()

        if not selecionados:
            return None

        return tree.item(selecionados[0], "values")

    def _mostrar_erro(self, mensagem):
        mostrar_erro(self, mensagem)

    def _mostrar_info(self, mensagem):
        mostrar_info(self, mensagem)

    def _confirmar(self, mensagem):
        return confirmar(self, mensagem)

    def _executar(self, acao, mensagem_sucesso=None):
        try:
            resultado = acao()

            if mensagem_sucesso:
                self._mostrar_info(mensagem_sucesso)

            return resultado
        except Exception as erro:
            self._mostrar_erro(erro)
            return None

    def _criar_entrada(
        self,
        parent,
        linha,
        coluna,
        rotulo,
        variavel,
        largura=22,
    ):
        ttk.Label(parent, text=rotulo, style="Campo.TLabel").grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=(0, 6),
            pady=3,
        )
        entrada = ttk.Entry(
            parent,
            textvariable=variavel,
            width=largura,
        )
        entrada.grid(
            row=linha,
            column=coluna + 1,
            sticky="w",
            padx=(0, 8),
            pady=3,
        )
        return entrada

    def _criar_combo(
        self,
        parent,
        linha,
        coluna,
        rotulo,
        variavel,
        opcoes,
        largura=20,
    ):
        ttk.Label(parent, text=rotulo, style="Campo.TLabel").grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=(0, 6),
            pady=3,
        )
        combo = ttk.Combobox(
            parent,
            textvariable=variavel,
            values=opcoes,
            state="readonly",
            width=largura,
        )
        combo.grid(
            row=linha,
            column=coluna + 1,
            sticky="w",
            padx=(0, 8),
            pady=3,
        )
        return combo

    def _criar_check(self, parent, linha, coluna, rotulo, variavel):
        check = ttk.Checkbutton(
            parent,
            text=rotulo,
            variable=variavel,
            style="TCheckbutton",
        )
        check.grid(
            row=linha,
            column=coluna,
            columnspan=2,
            sticky="w",
            pady=3,
        )
        return check

    @staticmethod
    def _criar_barra_botoes(parent, botoes):
        barra = ttk.Frame(parent, style="Pagina.TFrame")
        barra.pack(fill="x", pady=(0, 6))

        for item in botoes:
            texto, comando = item[:2]
            variante = item[2] if len(item) > 2 else "primario"
            BotaoAnimado(
                barra,
                texto,
                comando,
                variante=variante,
                altura=32,
            ).pack(side="left", padx=(0, 8))

        return barra


class BaseCadastroFrame(BaseFrame, ABC):

    titulo = ""
    subtitulo = ""
    cor_destaque = CORES["azul"]

    def _construir(self):
        criar_cabecalho_pagina(
            self,
            self.titulo,
            self.subtitulo,
            self.cor_destaque,
        )

        self._montar_botoes()
        self._montar_conteudo()
        self.carregar()

    @abstractmethod
    def _montar_conteudo(self):
        raise NotImplementedError

    @abstractmethod
    def _montar_botoes(self):
        raise NotImplementedError

    @abstractmethod
    def carregar(self):
        raise NotImplementedError

    @abstractmethod
    def salvar(self):
        raise NotImplementedError

    @abstractmethod
    def excluir(self):
        raise NotImplementedError

    @abstractmethod
    def limpar(self):
        raise NotImplementedError

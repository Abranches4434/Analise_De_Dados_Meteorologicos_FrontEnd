import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox, ttk


class BaseFrame(ttk.Frame, ABC):

    def __init__(self, master, app):
        super().__init__(master, padding=10)
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
        container = ttk.Frame(parent)
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

        tree.grid(row=0, column=0, sticky="nsew")
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        return tree

    @staticmethod
    def _preencher_tabela(tree, linhas):
        tree.delete(*tree.get_children())

        for linha in linhas:
            tree.insert("", "end", values=linha)

    @staticmethod
    def _obter_selecao(tree):
        selecionados = tree.selection()

        if not selecionados:
            return None

        return tree.item(selecionados[0], "values")

    def _mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", str(mensagem), parent=self)

    def _mostrar_info(self, mensagem):
        messagebox.showinfo("Informação", str(mensagem), parent=self)

    def _confirmar(self, mensagem):
        return messagebox.askyesno("Confirmação", mensagem, parent=self)

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
        ttk.Label(parent, text=rotulo).grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=(0, 6),
            pady=4,
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
            padx=(0, 16),
            pady=4,
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
        ttk.Label(parent, text=rotulo).grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=(0, 6),
            pady=4,
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
            padx=(0, 16),
            pady=4,
        )
        return combo

    def _criar_check(self, parent, linha, coluna, rotulo, variavel):
        check = ttk.Checkbutton(
            parent,
            text=rotulo,
            variable=variavel,
        )
        check.grid(
            row=linha,
            column=coluna,
            columnspan=2,
            sticky="w",
            pady=4,
        )
        return check

    @staticmethod
    def _criar_barra_botoes(parent, botoes):
        barra = ttk.Frame(parent)
        barra.pack(fill="x", pady=(8, 0))

        for texto, comando in botoes:
            ttk.Button(
                barra,
                text=texto,
                command=comando,
            ).pack(side="left", padx=(0, 6))

        return barra


class BaseCadastroFrame(BaseFrame, ABC):

    titulo = ""

    def _construir(self):
        ttk.Label(
            self,
            text=self.titulo,
            font=("TkDefaultFont", 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        self._montar_conteudo()
        self._montar_botoes()
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

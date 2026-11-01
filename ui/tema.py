import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


CORES = {
    "fundo": "#F3F6FA",
    "superficie": "#FFFFFF",
    "superficie_alt": "#F8FAFC",
    "zebra": "#F7FAFD",
    "borda": "#D6E0EA",
    "texto": "#1C2833",
    "texto_suave": "#5F6A78",
    "navy": "#0F2340",
    "navy_2": "#19375C",
    "navy_3": "#244B73",
    "teal": "#009688",
    "teal_escuro": "#00695C",
    "azul": "#2563EB",
    "azul_claro": "#DBEAFE",
    "laranja": "#E67E22",
    "verde": "#278B4C",
    "vermelho": "#C0392B",
    "roxo": "#7C5AC7",
    "amarelo": "#F1C40F",
    "branco": "#FFFFFF",
    "hover_linha": "#E8F1FB",
    "sombra": "#C9D6E3",
    "status": "#DDE7F0",
}

FONTES = {
    "app_titulo": ("DejaVu Sans", 18, "bold"),
    "app_subtitulo": ("DejaVu Sans", 9),
    "titulo": ("DejaVu Sans", 15, "bold"),
    "subtitulo": ("DejaVu Sans", 9),
    "corpo": ("DejaVu Sans", 10),
    "botao": ("DejaVu Sans", 10, "bold"),
    "aba": ("DejaVu Sans", 10, "bold"),
    "cabecalho_tabela": ("DejaVu Sans", 10, "bold"),
    "pequena": ("DejaVu Sans", 9),
}

VARIANTES_BOTAO = {
    "primario": {
        "base": "#2563EB",
        "hover": "#3B82F6",
        "press": "#1D4ED8",
        "texto": "#FFFFFF",
        "sombra": "#1E3A8A",
        "foco": "#F1C40F",
    },
    "teal": {
        "base": "#009688",
        "hover": "#14B8A6",
        "press": "#00796B",
        "texto": "#FFFFFF",
        "sombra": "#005B52",
        "foco": "#F1C40F",
    },
    "sucesso": {
        "base": "#278B4C",
        "hover": "#34A853",
        "press": "#1E6B3A",
        "texto": "#FFFFFF",
        "sombra": "#14532D",
        "foco": "#F1C40F",
    },
    "perigo": {
        "base": "#C0392B",
        "hover": "#E74C3C",
        "press": "#96281B",
        "texto": "#FFFFFF",
        "sombra": "#7F1D1D",
        "foco": "#F1C40F",
    },
    "azul": {
        "base": "#2563EB",
        "hover": "#3B82F6",
        "press": "#1D4ED8",
        "texto": "#FFFFFF",
        "sombra": "#1E3A8A",
        "foco": "#F1C40F",
    },
    "roxo": {
        "base": "#7C5AC7",
        "hover": "#9173D8",
        "press": "#5B3FA0",
        "texto": "#FFFFFF",
        "sombra": "#3F2A73",
        "foco": "#F1C40F",
    },
    "laranja": {
        "base": "#E67E22",
        "hover": "#F39C12",
        "press": "#B85C0E",
        "texto": "#FFFFFF",
        "sombra": "#7C2D12",
        "foco": "#F1C40F",
    },
    "neutro": {
        "base": "#FFFFFF",
        "hover": "#F1F5F9",
        "press": "#E2E8F0",
        "texto": "#1C2833",
        "sombra": "#CBD5E1",
        "foco": "#2563EB",
    },
}


def _escolher_familia(root):
    familias = set(tkfont.families(root))

    for familia in ("Noto Sans", "DejaVu Sans", "Liberation Sans"):
        if familia in familias:
            return familia

    return "DejaVu Sans"


def _configurar_fontes(root):
    familia = _escolher_familia(root)

    for nome, tamanho, peso in (
        ("TkDefaultFont", 10, "normal"),
        ("TkTextFont", 10, "normal"),
        ("TkMenuFont", 10, "normal"),
        ("TkHeadingFont", 10, "bold"),
        ("TkCaptionFont", 9, "normal"),
        ("TkSmallCaptionFont", 9, "normal"),
        ("TkIconFont", 10, "normal"),
    ):
        try:
            fonte = tkfont.nametofont(nome)
            fonte.configure(family=familia, size=tamanho, weight=peso)
        except tk.TclError:
            pass

    FONTES.update({
        "app_titulo": (familia, 18, "bold"),
        "app_subtitulo": (familia, 9),
        "titulo": (familia, 15, "bold"),
        "subtitulo": (familia, 9),
        "corpo": (familia, 10),
        "botao": (familia, 10, "bold"),
        "aba": (familia, 10, "bold"),
        "cabecalho_tabela": (familia, 10, "bold"),
        "pequena": (familia, 9),
    })


def configurar_tema(root):
    _configurar_fontes(root)
    root.configure(bg=CORES["fundo"])

    estilo = ttk.Style(root)

    if "clam" in estilo.theme_names():
        estilo.theme_use("clam")

    estilo.configure("TFrame", background=CORES["fundo"])
    estilo.configure("Pagina.TFrame", background=CORES["fundo"])
    estilo.configure("Card.TFrame", background=CORES["superficie"])

    estilo.configure(
        "TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto"],
        font=FONTES["corpo"],
    )
    estilo.configure(
        "TituloPagina.TLabel",
        background=CORES["fundo"],
        foreground=CORES["navy"],
        font=FONTES["titulo"],
    )
    estilo.configure(
        "Subtitulo.TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto_suave"],
        font=FONTES["subtitulo"],
    )
    estilo.configure(
        "Campo.TLabel",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=FONTES["corpo"],
    )
    estilo.configure(
        "Resultado.TLabel",
        background=CORES["fundo"],
        foreground=CORES["navy"],
        font=(FONTES["corpo"][0], 11, "bold"),
    )
    estilo.configure(
        "StatusPagina.TLabel",
        background=CORES["fundo"],
        foreground=CORES["texto_suave"],
        font=FONTES["pequena"],
    )

    estilo.configure(
        "TLabelframe",
        background=CORES["superficie"],
        bordercolor=CORES["borda"],
        lightcolor=CORES["superficie"],
        darkcolor=CORES["borda"],
        relief="solid",
        borderwidth=1,
    )
    estilo.configure(
        "TLabelframe.Label",
        background=CORES["superficie"],
        foreground=CORES["navy"],
        font=FONTES["cabecalho_tabela"],
    )

    estilo.configure(
        "TEntry",
        fieldbackground=CORES["superficie"],
        foreground=CORES["texto"],
        bordercolor=CORES["borda"],
        lightcolor=CORES["borda"],
        darkcolor=CORES["borda"],
        insertcolor=CORES["texto"],
        padding=5,
    )
    estilo.map(
        "TEntry",
        bordercolor=[("focus", CORES["azul"])],
        lightcolor=[("focus", CORES["azul"])],
        darkcolor=[("focus", CORES["azul"])],
        fieldbackground=[("readonly", "#EEF2F6")],
        foreground=[("readonly", CORES["texto_suave"])],
    )

    estilo.configure(
        "TCombobox",
        fieldbackground=CORES["superficie"],
        background=CORES["superficie"],
        foreground=CORES["texto"],
        arrowcolor=CORES["navy"],
        bordercolor=CORES["borda"],
        lightcolor=CORES["borda"],
        darkcolor=CORES["borda"],
        padding=6,
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", CORES["superficie"])],
        bordercolor=[("focus", CORES["azul"])],
        lightcolor=[("focus", CORES["azul"])],
        darkcolor=[("focus", CORES["azul"])],
    )

    estilo.configure(
        "TCheckbutton",
        background=CORES["superficie"],
        foreground=CORES["texto"],
        font=FONTES["corpo"],
    )
    estilo.map(
        "TCheckbutton",
        background=[("active", CORES["superficie"])],
        foreground=[("active", CORES["teal_escuro"])],
    )

    estilo.configure(
        "TNotebook",
        background=CORES["fundo"],
        borderwidth=0,
        tabmargins=(0, 4, 0, 0),
    )
    estilo.configure(
        "TNotebook.Tab",
        background="#E3EAF2",
        foreground=CORES["texto_suave"],
        padding=(16, 7),
        font=FONTES["aba"],
        borderwidth=0,
    )
    estilo.map(
        "TNotebook.Tab",
        background=[("selected", CORES["teal"]), ("active", "#D6E4F0")],
        foreground=[("selected", CORES["branco"]), ("active", CORES["navy"])],
    )

    estilo.configure(
        "Treeview",
        background=CORES["superficie"],
        fieldbackground=CORES["superficie"],
        foreground=CORES["texto"],
        rowheight=26,
        font=FONTES["corpo"],
        borderwidth=0,
    )
    estilo.map(
        "Treeview",
        background=[("selected", CORES["azul"])],
        foreground=[("selected", CORES["branco"])],
    )
    estilo.configure(
        "Treeview.Heading",
        background=CORES["navy"],
        foreground=CORES["branco"],
        font=FONTES["cabecalho_tabela"],
        relief="flat",
        padding=(6, 6),
    )
    estilo.map(
        "Treeview.Heading",
        background=[("active", CORES["navy_2"])],
        foreground=[("active", CORES["branco"])],
    )

    for orientacao in ("Vertical", "Horizontal"):
        estilo.configure(
            f"{orientacao}.TScrollbar",
            background="#C6D3E0",
            troughcolor=CORES["superficie"],
            bordercolor=CORES["superficie"],
            arrowcolor=CORES["navy"],
        )
        estilo.map(
            f"{orientacao}.TScrollbar",
            background=[("active", CORES["teal"])],
        )

    estilo.configure("TSeparator", background=CORES["borda"])
    estilo.configure(
        "TButton",
        background=CORES["superficie"],
        foreground=CORES["navy"],
        padding=(12, 7),
        font=FONTES["botao"],
    )
    estilo.map(
        "TButton",
        background=[("active", CORES["azul_claro"]), ("pressed", CORES["borda"])],
        foreground=[("active", CORES["navy"])],
    )

    root.option_add("*TCombobox*Listbox.background", CORES["superficie"])
    root.option_add("*TCombobox*Listbox.foreground", CORES["texto"])
    root.option_add("*TCombobox*Listbox.selectBackground", CORES["azul"])
    root.option_add("*TCombobox*Listbox.selectForeground", CORES["branco"])


def cor_fundo(widget):
    if isinstance(
        widget,
        (tk.Tk, tk.Toplevel, tk.Frame, tk.Canvas, tk.Label, tk.Button),
    ):
        try:
            return widget.cget("bg")
        except tk.TclError:
            pass

    try:
        estilo = ttk.Style(widget)
        nome = widget.cget("style") or widget.winfo_class()
        cor = estilo.lookup(nome, "background")
        return cor or CORES["fundo"]
    except tk.TclError:
        return CORES["fundo"]


def _hex_para_rgb(cor):
    cor = cor.lstrip("#")
    return tuple(int(cor[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_para_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        *(max(0, min(255, int(valor))) for valor in rgb)
    )


def _interpolar(inicio, fim, fator):
    rgb_inicio = _hex_para_rgb(inicio)
    rgb_fim = _hex_para_rgb(fim)
    return _rgb_para_hex(
        tuple(
            a + (b - a) * fator
            for a, b in zip(rgb_inicio, rgb_fim)
        )
    )


def _pontos_arredondados(x1, y1, x2, y2, raio):
    return (
        x1 + raio, y1,
        x2 - raio, y1,
        x2, y1,
        x2, y1 + raio,
        x2, y2 - raio,
        x2, y2,
        x2 - raio, y2,
        x1 + raio, y2,
        x1, y2,
        x1, y2 - raio,
        x1, y1 + raio,
        x1, y1,
    )


def desenhar_arredondado(canvas, x1, y1, x2, y2, raio, **opcoes):
    return canvas.create_polygon(
        _pontos_arredondados(x1, y1, x2, y2, raio),
        smooth=True,
        splinesteps=32,
        **opcoes,
    )


class BotaoAnimado(tk.Canvas):

    def __init__(
        self,
        master,
        texto,
        comando=None,
        variante="primario",
        largura=None,
        altura=36,
        raio=9,
    ):
        self._variante = VARIANTES_BOTAO.get(
            variante,
            VARIANTES_BOTAO["primario"],
        )
        self._comando = comando
        self._texto_botao = texto
        self._altura = altura
        self._raio = raio
        self._cor_atual = self._variante["base"]
        self._sombra_offset = 2
        self._hover = False
        self._pressionado = False
        self._animacao_id = None
        self._habilitado = True

        fonte = tkfont.Font(font=FONTES["botao"])
        largura_texto = fonte.measure(texto)
        self._largura = max(
            100,
            largura if largura is not None else largura_texto + 38,
        )

        self._fundo_pai = cor_fundo(master)
        super().__init__(
            master,
            width=self._largura,
            height=altura,
            bg=self._fundo_pai,
            highlightthickness=0,
            bd=0,
            takefocus=1,
            cursor="hand2",
        )

        self._sombra = None
        self._fundo = None
        self._texto = None
        self._foco = None
        self._desenhar()

        self.bind("<Enter>", self._ao_entrar)
        self.bind("<Leave>", self._ao_sair)
        self.bind("<ButtonPress-1>", self._ao_pressionar)
        self.bind("<ButtonRelease-1>", self._ao_soltar)
        self.bind("<FocusIn>", self._ao_ganhar_foco)
        self.bind("<FocusOut>", self._ao_perder_foco)
        self.bind("<Return>", self._acionar_teclado)
        self.bind("<space>", self._acionar_teclado)
        self.bind("<Destroy>", self._ao_destruir)

    def _desenhar(self):
        x1, y1 = 1, 1
        x2 = self._largura - 1
        y2 = self._altura - 1 - self._sombra_offset
        y_sombra = y2 + self._sombra_offset

        self._sombra = desenhar_arredondado(
            self,
            x1 + 1,
            y1 + self._sombra_offset,
            x2 + 1,
            y_sombra + 1,
            self._raio,
            fill=self._variante["sombra"],
            outline=self._variante["sombra"],
        )
        self._fundo = desenhar_arredondado(
            self,
            x1,
            y1,
            x2,
            y2,
            self._raio,
            fill=self._cor_atual,
            outline=self._cor_atual,
        )
        self._texto = self.create_text(
            self._largura / 2,
            (y1 + y2) / 2,
            text=self._texto_botao,
            fill=self._variante["texto"],
            font=FONTES["botao"],
        )
        self._foco = desenhar_arredondado(
            self,
            x1 + 2,
            y1 + 2,
            x2 - 2,
            y2 - 2,
            max(1, self._raio - 2),
            fill="",
            outline=self._variante["foco"],
            width=2,
            state="hidden",
        )

    def _reposicionar(self):
        x1, y1 = 1, 1
        x2 = self._largura - 1
        y2 = self._altura - 1 - self._sombra_offset
        y_sombra = y2 + self._sombra_offset

        self.coords(
            self._sombra,
            *_pontos_arredondados(
                x1 + 1,
                y1 + self._sombra_offset,
                x2 + 1,
                y_sombra + 1,
                self._raio,
            ),
        )
        self.coords(
            self._fundo,
            *_pontos_arredondados(x1, y1, x2, y2, self._raio),
        )
        self.coords(self._texto, self._largura / 2, (y1 + y2) / 2)
        self.coords(
            self._foco,
            *_pontos_arredondados(
                x1 + 2,
                y1 + 2,
                x2 - 2,
                y2 - 2,
                max(1, self._raio - 2),
            ),
        )

    def _definir_sombra(self, offset):
        if offset == self._sombra_offset:
            return

        self._sombra_offset = offset
        self._reposicionar()

    def _animar_para(self, destino):
        if self._animacao_id is not None:
            try:
                self.after_cancel(self._animacao_id)
            except tk.TclError:
                pass
            self._animacao_id = None

        origem = self._cor_atual
        passos = 9

        def passo(indice=1):
            if not self.winfo_exists():
                return

            fator = 1 - (1 - indice / passos) ** 3
            cor = _interpolar(origem, destino, fator)
            self._cor_atual = cor
            self.itemconfigure(self._fundo, fill=cor, outline=cor)

            if indice < passos:
                self._animacao_id = self.after(
                    16,
                    lambda: passo(indice + 1),
                )
            else:
                self._animacao_id = None

        passo()

    def _ao_entrar(self, _evento=None):
        if not self._habilitado:
            return

        self._hover = True
        self._definir_sombra(3)
        self._animar_para(self._variante["hover"])

    def _ao_sair(self, _evento=None):
        if not self._habilitado:
            return

        self._hover = False

        if not self._pressionado:
            self._definir_sombra(2)
            self._animar_para(self._variante["base"])

    def _ao_pressionar(self, _evento=None):
        if not self._habilitado:
            return

        self.focus_set()
        self._pressionado = True
        self._definir_sombra(1)
        self._animar_para(self._variante["press"])

    def _ao_soltar(self, evento):
        if not self._habilitado:
            return

        self._pressionado = False
        dentro = (
            0 <= evento.x <= self._largura
            and 0 <= evento.y <= self._altura
        )

        if dentro:
            self._ao_entrar()
            self._invocar()
        else:
            self._ao_sair()

    def _invocar(self):
        if not self._habilitado or self._comando is None:
            return

        self._comando()

    def _acionar_teclado(self, _evento=None):
        if not self._habilitado:
            return "break"

        self._pressionado = True
        self._definir_sombra(1)
        self._animar_para(self._variante["press"])

        def concluir():
            if not self.winfo_exists():
                return
            self._pressionado = False
            self._definir_sombra(2 if not self._hover else 3)
            self._animar_para(
                self._variante["hover"]
                if self._hover
                else self._variante["base"]
            )
            self._invocar()

        self.after(90, concluir)
        return "break"

    def _ao_ganhar_foco(self, _evento=None):
        self.itemconfigure(self._foco, state="normal")

    def _ao_perder_foco(self, _evento=None):
        self.itemconfigure(self._foco, state="hidden")

    def _ao_destruir(self, _evento=None):
        if self._animacao_id is not None:
            try:
                self.after_cancel(self._animacao_id)
            except tk.TclError:
                pass

    def definir_habilitado(self, habilitado):
        self._habilitado = bool(habilitado)
        self.configure(cursor="hand2" if habilitado else "arrow")

        if not habilitado:
            self._animar_para("#CBD5E1")

    def focar(self):
        self.focus_set()


class Cabecalho(tk.Canvas):

    def __init__(self, master, api_url):
        super().__init__(
            master,
            height=70,
            highlightthickness=0,
            bd=0,
        )
        self._api_url = api_url
        self._online = True
        self._erro = False
        self.bind("<Configure>", self._redesenhar)

    def definir_status(self, online, mensagem=None):
        self._online = bool(online)
        self._erro = not online

        if mensagem is not None:
            self._api_url = mensagem

        self._redesenhar()

    def _redesenhar(self, _evento=None):
        self.delete("all")
        largura = self.winfo_width()
        altura = self.winfo_height()

        if largura <= 1 or altura <= 1:
            return

        passos = max(1, largura // 5)

        for indice in range(passos):
            fator = indice / max(1, passos - 1)
            cor = _interpolar(CORES["navy"], CORES["navy_2"], fator)
            x1 = int(largura * indice / passos)
            x2 = int(largura * (indice + 1) / passos) + 1
            self.create_rectangle(
                x1,
                0,
                x2,
                altura,
                fill=cor,
                outline=cor,
            )

        self.create_oval(
            largura - 160,
            -70,
            largura + 50,
            140,
            outline="#2B4A6F",
            width=2,
        )
        self.create_oval(
            largura - 110,
            -25,
            largura + 20,
            105,
            outline="#2B4A6F",
            width=1,
        )

        faixas = max(1, largura // 6)

        for indice in range(faixas):
            fator = indice / max(1, faixas - 1)
            cor = _interpolar(CORES["teal"], CORES["laranja"], fator)
            x1 = int(largura * indice / faixas)
            x2 = int(largura * (indice + 1) / faixas) + 1
            self.create_rectangle(
                x1,
                altura - 4,
                x2,
                altura,
                fill=cor,
                outline=cor,
            )

        self.create_text(
            24,
            altura / 2 - 9,
            anchor="w",
            text="Análise de Dados Meteorológicos",
            fill=CORES["branco"],
            font=FONTES["app_titulo"],
        )
        self.create_text(
            24,
            altura / 2 + 19,
            anchor="w",
            text="Monitoramento climático • Flask + PostgreSQL",
            fill="#B9C7D8",
            font=FONTES["app_subtitulo"],
        )

        fonte = tkfont.Font(font=FONTES["pequena"])
        rotulo = f"API  {self._api_url}"
        largura_badge = fonte.measure(rotulo) + 50
        x2 = largura - 24
        x1 = x2 - largura_badge
        y1 = altura / 2 - 16
        y2 = altura / 2 + 16

        desenhar_arredondado(
            self,
            x1,
            y1,
            x2,
            y2,
            13,
            fill="#173A5E",
            outline="#2B587F",
        )
        cor_status = CORES["verde"] if self._online else CORES["vermelho"]
        self.create_oval(
            x1 + 14,
            altura / 2 - 5,
            x1 + 24,
            altura / 2 + 5,
            fill=cor_status,
            outline=cor_status,
        )
        self.create_text(
            x1 + 32,
            altura / 2,
            anchor="w",
            text=self._api_url,
            fill=CORES["status"],
            font=FONTES["pequena"],
        )


def criar_cabecalho_pagina(parent, titulo, subtitulo, cor):
    cabecalho = ttk.Frame(parent, style="Pagina.TFrame")
    cabecalho.pack(fill="x", pady=(0, 6))

    tk.Frame(
        cabecalho,
        bg=cor,
        width=4,
        height=28,
    ).pack(side="left", fill="y", padx=(0, 10))

    bloco = ttk.Frame(cabecalho, style="Pagina.TFrame")
    bloco.pack(side="left")

    ttk.Label(
        bloco,
        text=titulo,
        style="TituloPagina.TLabel",
    ).pack(side="left", anchor="s")

    if subtitulo:
        ttk.Label(
            bloco,
            text=subtitulo,
            style="Subtitulo.TLabel",
        ).pack(side="left", anchor="s", padx=(10, 0), pady=(0, 3))

    return cabecalho


def configurar_listbox(listbox):
    listbox.configure(
        bg=CORES["superficie"],
        fg=CORES["texto"],
        selectbackground=CORES["azul"],
        selectforeground=CORES["branco"],
        highlightthickness=1,
        highlightbackground=CORES["borda"],
        highlightcolor=CORES["azul"],
        relief="flat",
        bd=0,
        activestyle="none",
        font=FONTES["corpo"],
    )


def configurar_hover_tabela(tree):
    tree.tag_configure("linha_par", background=CORES["superficie"])
    tree.tag_configure("linha_impar", background=CORES["zebra"])
    tree.tag_configure(
        "hover",
        background=CORES["hover_linha"],
        foreground=CORES["texto"],
    )
    tree._item_hover = None

    def remover_hover(item):
        if not item:
            return

        try:
            tags = [
                tag
                for tag in tree.item(item, "tags")
                if tag != "hover"
            ]
            tree.item(item, tags=tags)
        except tk.TclError:
            pass

    def ao_mover(evento):
        item = tree.identify_row(evento.y)

        if item == tree._item_hover:
            return

        remover_hover(tree._item_hover)
        tree._item_hover = item

        if item:
            tags = [
                tag
                for tag in tree.item(item, "tags")
                if tag != "hover"
            ]
            tree.item(item, tags=[*tags, "hover"])

    def ao_sair(_evento=None):
        remover_hover(tree._item_hover)
        tree._item_hover = None

    tree.bind("<Motion>", ao_mover, add="+")
    tree.bind("<Leave>", ao_sair, add="+")

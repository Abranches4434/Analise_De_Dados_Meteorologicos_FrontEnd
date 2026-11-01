import tkinter as tk

from ui.tema import CORES, FONTES, BotaoAnimado


class DialogoPersonalizado(tk.Toplevel):

    def __init__(
        self,
        parent,
        titulo,
        mensagem,
        tipo="info",
        confirmacao=False,
        texto_confirmar="Confirmar",
        variante_confirmar="primario",
    ):
        super().__init__(parent.winfo_toplevel())
        self.withdraw()
        self.overrideredirect(True)
        self.configure(bg=CORES["borda"])
        self._resultado = False
        self._confirmacao = confirmacao
        self._tipo = tipo
        self._cor = self._cor_do_tipo(tipo)
        self._botao_padrao = None

        self._montar(titulo, mensagem, texto_confirmar, variante_confirmar)
        self.update_idletasks()
        self._centralizar(parent)
        self.deiconify()
        self.transient(parent.winfo_toplevel())
        self.lift()
        self.grab_set()
        self.focus_force()
        self.after(30, self._focar_padrao)

        self.bind("<Escape>", lambda _evento: self._cancelar())
        self.protocol("WM_DELETE_WINDOW", self._cancelar)

    @property
    def resultado(self):
        return self._resultado

    @staticmethod
    def _cor_do_tipo(tipo):
        if tipo == "erro":
            return CORES["vermelho"]
        if tipo == "confirmacao":
            return CORES["laranja"]
        return CORES["teal"]

    @staticmethod
    def _simbolo_do_tipo(tipo):
        if tipo == "erro":
            return "!"
        if tipo == "confirmacao":
            return "?"
        return "i"

    def _montar(
        self,
        titulo,
        mensagem,
        texto_confirmar,
        variante_confirmar,
    ):
        borda = tk.Frame(self, bg=CORES["borda"], padx=2, pady=2)
        borda.pack(fill="both", expand=True)

        cartao = tk.Frame(borda, bg=CORES["superficie"])
        cartao.pack(fill="both", expand=True)

        cabecalho = tk.Frame(
            cartao,
            bg=self._cor,
            height=58,
        )
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        icone = tk.Canvas(
            cabecalho,
            width=30,
            height=30,
            bg=self._cor,
            highlightthickness=0,
            bd=0,
        )
        icone.pack(side="left", padx=(20, 12), pady=14)
        icone.create_oval(
            2,
            2,
            28,
            28,
            fill=CORES["branco"],
            outline=CORES["branco"],
        )
        icone.create_text(
            15,
            15,
            text=self._simbolo_do_tipo(self._tipo),
            fill=self._cor,
            font=(FONTES["corpo"][0], 13, "bold"),
        )

        tk.Label(
            cabecalho,
            text=titulo,
            bg=self._cor,
            fg=CORES["branco"],
            font=(FONTES["corpo"][0], 13, "bold"),
            anchor="w",
        ).pack(side="left", fill="both", expand=True, pady=14)

        corpo = tk.Frame(
            cartao,
            bg=CORES["superficie"],
            padx=26,
            pady=22,
        )
        corpo.pack(fill="both", expand=True)

        tk.Label(
            corpo,
            text=str(mensagem),
            bg=CORES["superficie"],
            fg=CORES["texto"],
            justify="left",
            anchor="w",
            wraplength=430,
            font=FONTES["corpo"],
        ).pack(fill="x")

        rodape = tk.Frame(
            cartao,
            bg=CORES["superficie"],
            padx=26,
        )
        rodape.pack(fill="x", pady=(0, 22))

        if self._confirmacao:
            botao_cancelar = BotaoAnimado(
                rodape,
                "Cancelar",
                self._cancelar,
                variante="neutro",
            )
            botao_cancelar.pack(side="right", padx=(10, 0))
            self._botao_padrao = botao_cancelar

            botao_confirmar = BotaoAnimado(
                rodape,
                texto_confirmar,
                self._confirmar,
                variante=variante_confirmar,
            )
            botao_confirmar.pack(side="right")
        else:
            texto = "Fechar" if self._tipo == "erro" else "Entendi"
            variante = "perigo" if self._tipo == "erro" else "teal"
            botao = BotaoAnimado(
                rodape,
                texto,
                self._confirmar,
                variante=variante,
            )
            botao.pack(side="right")
            self._botao_padrao = botao

    def _centralizar(self, parent):
        raiz = parent.winfo_toplevel()
        largura = max(480, self.winfo_reqwidth())
        altura = self.winfo_reqheight()

        x = raiz.winfo_rootx() + (raiz.winfo_width() - largura) // 2
        y = raiz.winfo_rooty() + (raiz.winfo_height() - altura) // 2

        self.geometry(f"{largura}x{altura}+{max(x, 0)}+{max(y, 0)}")

    def _focar_padrao(self):
        if self._botao_padrao is not None:
            self._botao_padrao.focar()

    def _confirmar(self):
        self._resultado = True
        self._fechar()

    def _cancelar(self):
        self._resultado = False
        self._fechar()

    def _fechar(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass

        self.destroy()


def _mostrar_dialogo(
    parent,
    titulo,
    mensagem,
    tipo,
    confirmacao=False,
    texto_confirmar="Confirmar",
    variante_confirmar="primario",
):
    dialogo = DialogoPersonalizado(
        parent,
        titulo,
        mensagem,
        tipo=tipo,
        confirmacao=confirmacao,
        texto_confirmar=texto_confirmar,
        variante_confirmar=variante_confirmar,
    )
    dialogo.wait_window(dialogo)
    return dialogo.resultado


def mostrar_erro(parent, mensagem):
    _mostrar_dialogo(
        parent,
        "Erro",
        mensagem,
        tipo="erro",
    )


def mostrar_info(parent, mensagem):
    _mostrar_dialogo(
        parent,
        "Informação",
        mensagem,
        tipo="info",
    )


def confirmar(parent, mensagem, titulo="Confirmação"):
    return _mostrar_dialogo(
        parent,
        titulo,
        mensagem,
        tipo="confirmacao",
        confirmacao=True,
        texto_confirmar="Confirmar",
        variante_confirmar="perigo",
    )

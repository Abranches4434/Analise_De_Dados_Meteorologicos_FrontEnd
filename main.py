import tkinter as tk
from tkinter import ttk

from api import ApiClient
from ui.analises import AnalisesFrame
from ui.localidades import LocalidadesFrame
from ui.registros import RegistrosFrame
from ui.tema import CORES, FONTES, Cabecalho, configurar_tema
from ui.thresholds import ThresholdsFrame


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Análise de Dados Meteorológicos")
        self._definir_geometria()

        self._api = ApiClient()
        self.status_var = tk.StringVar()
        self._registros_frame = None
        self._thresholds_frame = None
        self._analises_frame = None
        self._cabecalho = None
        self._status_dot = None

        self._configurar_estilo()
        self._montar_interface()
        self.atualizar_localidades()

    @property
    def api(self):
        return self._api

    def _definir_geometria(self):
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        largura = min(1280, max(1024, largura_tela - 60))
        altura = min(820, max(660, altura_tela - 40))
        posicao_x = max((largura_tela - largura) // 2, 0)
        posicao_y = max((altura_tela - altura) // 2, 10)

        self.geometry(
            f"{largura}x{altura}+{posicao_x}+{posicao_y}"
        )
        self.minsize(1024, 640)

    def _configurar_estilo(self):
        configurar_tema(self)

    def _montar_interface(self):
        self._cabecalho = Cabecalho(self, self.api.base_url)
        self._cabecalho.pack(fill="x")

        self._montar_barra_status()

        notebook = ttk.Notebook(self)
        notebook.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(2, 10),
        )

        self._localidades_frame = LocalidadesFrame(notebook, self)
        notebook.add(self._localidades_frame, text="Localidades")

        self._registros_frame = RegistrosFrame(notebook, self)
        notebook.add(self._registros_frame, text="Registros")

        self._thresholds_frame = ThresholdsFrame(notebook, self)
        notebook.add(self._thresholds_frame, text="Thresholds")

        self._analises_frame = AnalisesFrame(notebook, self)
        notebook.add(self._analises_frame, text="Análises")

        self._notebook = notebook

    def _montar_barra_status(self):
        barra = tk.Frame(
            self,
            bg=CORES["navy"],
            height=34,
        )
        barra.pack(side="bottom", fill="x")
        barra.pack_propagate(False)

        self._status_dot = tk.Canvas(
            barra,
            width=12,
            height=12,
            bg=CORES["navy"],
            highlightthickness=0,
            bd=0,
        )
        self._status_dot.pack(side="left", padx=(16, 8))
        self._status_dot.create_oval(
            2,
            2,
            10,
            10,
            fill=CORES["teal"],
            outline=CORES["teal"],
            tags="dot",
        )

        tk.Label(
            barra,
            textvariable=self.status_var,
            bg=CORES["navy"],
            fg=CORES["status"],
            anchor="w",
            font=FONTES["pequena"],
        ).pack(side="left", fill="x", expand=True, padx=(0, 16))

    def _definir_status(self, mensagem, estado="ok"):
        self.status_var.set(mensagem)
        cores = {
            "ok": CORES["verde"],
            "erro": CORES["vermelho"],
            "info": CORES["teal"],
        }
        cor = cores.get(estado, CORES["teal"])

        if self._status_dot is not None:
            self._status_dot.itemconfigure(
                "dot",
                fill=cor,
                outline=cor,
            )

        if self._cabecalho is not None:
            self._cabecalho.definir_status(estado != "erro")

    def atualizar_localidades(self):
        try:
            localidades = self.api.listar_localidades(
                incluir_inativos=True
            )
        except Exception as erro:
            self._definir_status(
                f"Falha ao carregar localidades: {erro}",
                "erro",
            )
            return

        for frame in (
            self._registros_frame,
            self._thresholds_frame,
            self._analises_frame,
        ):
            if frame is not None:
                frame.atualizar_localidades(localidades)

        if self._registros_frame is not None:
            self._registros_frame.carregar()

        if self._thresholds_frame is not None:
            self._thresholds_frame.carregar()

        self._definir_status(
            f"API conectada em {self.api.base_url} — "
            f"{len(localidades)} localidades carregadas.",
            "ok",
        )


def main():
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()

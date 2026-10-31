import tkinter as tk
from tkinter import ttk

from api import ApiClient
from ui.analises import AnalisesFrame
from ui.localidades import LocalidadesFrame
from ui.registros import RegistrosFrame
from ui.thresholds import ThresholdsFrame


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Análise de Dados Meteorológicos")
        self.geometry("1240x800")
        self.minsize(1024, 680)

        self._api = ApiClient()
        self.status_var = tk.StringVar()
        self._registros_frame = None
        self._thresholds_frame = None
        self._analises_frame = None

        self._configurar_estilo()
        self._montar_interface()
        self.atualizar_localidades()

    @property
    def api(self):
        return self._api

    def _configurar_estilo(self):
        estilo = ttk.Style(self)

        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        estilo.configure("TNotebook.Tab", padding=(14, 8))
        estilo.configure("Treeview", rowheight=24)

    def _montar_interface(self):
        barra_superior = ttk.Frame(self, padding=(10, 8))
        barra_superior.pack(fill="x")
        ttk.Label(
            barra_superior,
            text="Análise de Dados Meteorológicos",
            font=("TkDefaultFont", 16, "bold"),
        ).pack(side="left")
        ttk.Label(
            barra_superior,
            text=f"API: {self.api.base_url}",
        ).pack(side="right")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self._localidades_frame = LocalidadesFrame(notebook, self)
        notebook.add(self._localidades_frame, text="Localidades")

        self._registros_frame = RegistrosFrame(notebook, self)
        notebook.add(self._registros_frame, text="Registros")

        self._thresholds_frame = ThresholdsFrame(notebook, self)
        notebook.add(self._thresholds_frame, text="Thresholds")

        self._analises_frame = AnalisesFrame(notebook, self)
        notebook.add(self._analises_frame, text="Análises")

        self._notebook = notebook

        ttk.Label(
            self,
            textvariable=self.status_var,
            anchor="w",
            padding=(10, 4),
        ).pack(fill="x")

    def atualizar_localidades(self):
        try:
            localidades = self.api.listar_localidades(
                incluir_inativos=True
            )
        except Exception as erro:
            self.status_var.set(f"Falha ao carregar localidades: {erro}")
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

        self.status_var.set(
            f"API conectada em {self.api.base_url} — "
            f"{len(localidades)} localidades carregadas."
        )


def main():
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()

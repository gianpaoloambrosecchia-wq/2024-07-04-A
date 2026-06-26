import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        if year is None or shape is None:
            self._view.create_alert("Selezionare un anno e poi una forma dai menù appositi")
            self._view.update_page()
            return
        self._model.buildGraph(int(year), shape)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di nodi: {numNodes}", color="purple")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di archi: {numEdges}", color="purple")
        )

        numCC, maxCC = self._model.getCompConnDetails()
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {numCC} componenti connesse", color="purple")
        )
        for cc in maxCC:
            self._view.txt_result1.controls.append(
                ft.Text(cc)
            )
        self._view.update_page()


    def handle_path(self, e):
        path, score = self._model.getPath()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(
            ft.Text(f"Il percorso ottimo ha punteggio: {score}", color="purple")
        )
        for p in path:
            self._view.txt_result2.controls.append(
                ft.Text(f"{p.id} | mese = {p.datetime.month}  durata = {p.duration}")
            )
        self._view.update_page()


    def fillDDYears(self):
        years = self._model.getAllYears()
        for year in years:
            self._view.ddyear.options.append(
                ft.dropdown.Option(year)
            )
        self._view.update_page()


    def fillDDShapes(self, e):
        year = self._view.ddyear.value
        shapes = self._model.getShapesForYear(year)
        for s in shapes:
            self._view.ddshape.options.append(
                ft.dropdown.Option(s)
            )
        self._view.update_page()

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    #-------------------------------------------------------------------------------------------------------------------------------
    def fillDDMinCromosomi(self):

        cromosomi = self._model.getAllCromosomi()
        for c in cromosomi:
            self._view.dd_min_ch.options.append( ft.dropdown.Option(c))

    def fillDDMaxCromosomi(self):

        cromosomi = self._model.getAllCromosomi()
        for c in cromosomi:
            self._view.dd_max_ch.options.append( ft.dropdown.Option(c))

    # -------------------------------------------------------------------------------------------------------------------------------
    def handle_graph(self, e):

        cMin = self._view.dd_min_ch.value
        cMax = self._view.dd_max_ch.value

        if cMin == "":
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, inserire un valore per Cromosoma minimo", color="red"))
            self._view.update_page()
            return

        if cMax == "":
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Attenzione, inserire un valore per Cromosoma massimo", color="red"))
            self._view.update_page()
            return

        if int(cMin) >= int(cMax):  #necessario perchè lui li vede come stringe quindi nove>dieci in ordine alfabetico
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append( ft.Text("Attenzione, inserire un valore di Cromosoma minimo più piccolo di Cromosoma massimo", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin, cMax)
        numNodi, numArchi = self._model.getDetailsGraph()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append( ft.Text(f"Creato grafo con {numNodi} nodi e {numArchi} archi "))
        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------
    def handle_dettagli(self, e):

        lista = self._model.getMaxNodi()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi col maggior numero di archi uscenti sono: "))
        for tupla in lista:
            self._view.txt_result1.controls.append(
                ft.Text(f"{tupla[0]} | num. archi uscenti: {tupla[1]} | peso tot: {tupla[2]}"))

        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------
    def handle_path(self, e):

        bestPath, bestScore = self._model.getCamminoOttimo()

        if bestPath == "":
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append( ft.Text("Attenzione, non è stato trovato nessun cammino ottimo", color="red"))
            self._view.update_page()
            return

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append( ft.Text(f"Il cammino ottimo ha {len(bestPath)} nodi e peso totale: {bestScore}"))
        self._view.txt_result2.controls.append(ft.Text("Di seguito la sequenza del cammino ottimo"))
        for p in bestPath:
            self._view.txt_result2.controls.append( ft.Text(p))

        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------

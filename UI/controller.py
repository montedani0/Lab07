import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.clean()
        mese = self._mese
        if mese == 0:
            self._view.create_alert("Selezionare un mese!")
            return

        umidita = self._model.umidita_media(mese)

        for c in umidita.keys():
            self._view.lst_result.controls.append(ft.Text(f"{c}: {umidita[c]}"))
            self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

    def handle_sequenza(self, e):
        # 1. PULIZIA DEL TAVOLO
        # Cancella i risultati vecchi dallo schermo, altrimenti si accodano!
        self._view.lst_result.controls.clear()

        # 2. PRENDO L'ORDINAZIONE (Quale mese ha scelto l'utente?)
        # Usiamo la variabile self._mese (come avevamo sistemato prima per l'umidità media)
        mese_scelto = self._mese

        # Controllo di sicurezza: ha scelto un mese nella tendina?
        if mese_scelto is None or mese_scelto == 0:
            self._view.create_alert("Attenzione: seleziona un mese prima di calcolare la sequenza!")
            return

        # 3. VADO IN CUCINA!
        # Chiamo il Model passandogli il mese, e mi faccio dare i due risultati
        self._view.lst_result.controls.append(ft.Text("Calcolo in corso... attendere!"))
        self._view.update_page()  # Aggiorno la pagina per far vedere la scritta "Calcolo in corso"

        sequenza_migliore, costo_minimo = self._model.calcola_sequenza(mese_scelto)

        self._view.lst_result.controls.clear()  # Tolgo la scritta "Calcolo in corso"

        self._view.lst_result.controls.append(ft.Text(f"Costo minimo trovato: {costo_minimo}"))
        self._view.lst_result.controls.append(ft.Text("La sequenza ottima è:"))

        # Stampo la lista dei 15 giorni bella in ordine
        for i in range(len(sequenza_migliore)):
            citta = sequenza_migliore[i]
            giorno = i + 1
            self._view.lst_result.controls.append(ft.Text(f"Giorno {giorno}: {citta}"))

        # 5. AGGIORNO LO SCHERMO
        self._view.update_page()


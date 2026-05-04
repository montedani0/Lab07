import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.dizionario_umidita = {}



        self.best_sequenza = []
        self.best_costo = float('inf')

        # --- 1. L'INNESCO (come risolvi_quadrato) ---

    def calcola_sequenza(self, mese):
        # Carico il dizionario_umidita dal DB usando MeteoDao
        self.dizionario_umidita = MeteoDao.spesa(mese)


        # Azzero i dati prima di partire
        self.best_sequenza = []
        self.best_costo = float('inf')

        # Faccio partire la ricorsione passandogli un diario vuoto
        self._ricorsione([])

        return self.best_sequenza, self.best_costo

        # --- 2. IL MOTORE RICORSIVO ---

    def _ricorsione(self, parziale):
        # CASO BASE: la sequenza è arrivata a 15 giorni
        if len(parziale) == 15:
            # Chiamo un metodo che calcola il costo finale (il biglietto + umidità)
            costo = self._calcola_costo(parziale)

            # Se è il costo più basso che ho trovato finora, me lo salvo!
            if costo < self.best_costo:
                self.best_costo = costo
                self.best_sequenza = copy.deepcopy(parziale)  # Faccio la copia

        # CASO RICORSIVO: devo ancora costruire i 15 giorni
        else:
            for citta in ["Genova", "Milano", "Torino"]:
                # 1) Aggiungo la città a parziale
                parziale.append(citta)

                # 2) Verifico le regole del gioco! (esattamente come il prof)
                if self._parziale_is_valido(parziale):
                    # 3) Andare avanti nella ricorsione
                    self._ricorsione(parziale)

                # 4) Backtracking: tolgo la città appena inserita per provarne un'altra
                parziale.pop()

    def _parziale_is_valido(self, parziale):
        # 1. PRENDO LA CITTA' CHE HO APPENA AGGIUNTO
        citta_appena_aggiunta = parziale[-1]

        # 2. REGOLA DEI 6 GIORNI
        # Se contando questa città supero i 6 giorni totali, la mossa è illegale.
        if parziale.count(citta_appena_aggiunta) > 6:
            return False

        # 3. REGOLA DEI 3 GIORNI
        # Se è il primissimo giorno, posso andare dove voglio!
        if len(parziale) == 1:
            return True

        # Guardo dove stavo ieri
        citta_di_ieri = parziale[-2]

        # Se sono rimasto nella stessa città di ieri, va benissimo.
        if citta_appena_aggiunta == citta_di_ieri:
            return True

        # --- Cambio città ---

        # Se cerco di cambiare città ma il mio viaggio è iniziato da 3 giorni o meno
        # (es. sono al Giorno 2 o 3), non posso fisicamente aver fatto 3 giorni prima.
        if len(parziale) <= 3:
            return False

        # Prendo i 3 giorni PRIMA di quello che ho appena inserito
        # Esempio: se parziale è ['Milano', 'Milano', 'Milano', 'Torino']
        # I tre giorni prima sono 'Milano', 'Milano', 'Milano'
        tre_giorni_precedenti = parziale[-4:-1]

        if tre_giorni_precedenti == [citta_di_ieri, citta_di_ieri, citta_di_ieri]:
            return True  # OK! Ho fatto 3 giorni, posso scappare.
        else:
            return False  # Illegale, non ho fatto 3 giorni consecutivi.

    def _calcola_costo(self, sequenza):
        costo_totale = 0

        # Scorro tutta la sequenza dei 15 giorni
        for i in range(len(sequenza)):
            citta = sequenza[i]
            giorno = i + 1

            # 1. AGGIUNGO L'UMIDITA'
            # Cerco nel dizionario usando la tupla (città, giorno)
            costo_totale += self.dizionario_umidita[(citta, giorno)]

            # 2. AGGIUNGO IL BIGLIETTO DEL TRENO (I 100 EURO)
            # Lo pago solo se NON è il primo giorno, e se ho cambiato città rispetto a ieri
            if i > 0:
                citta_di_ieri = sequenza[i - 1]
                if citta != citta_di_ieri:
                    costo_totale += 100

        return costo_totale

    def situazione(self):
        return MeteoDao.get_all_situazioni()

    def umidita_media(self,mese):
        return MeteoDao.umidita_media(mese)


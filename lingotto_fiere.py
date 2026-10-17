from base64 import standard_b64decode

class stand:
    def __init__(self, codice, superficie, padiglione, prezzo):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo = float(prezzo)
        self.espositore = None

    def calcola_prezzo_finale(self):
        return self.prezzo

    def __lt__(self, altro):
        return (
            self.calcola_prezzo_finale()
            < altro.calcola_prezzo_finale()
        )

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Assegnato"
        return (
            f"{self.codice}: Standard | {self.superficie:g} mq"
            f" - Padiglione {self.padiglione}"
            f" - Prezzo {self.calcola_prezzo_finale():.2f}€"
            f" - {stato}"
        )


class standspesextra(stand):
    def __init__(self, codice, superficie, padiglione, prezzo, Nprese):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo = float(prezzo)
        self.espositore = None
        self.Nprese = int(Nprese)

    def calcola_prezzo_finale(self):
        return self.prezzo * (1 + 0.07 * self.Nprese)

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Assegnato"
        return (
            f"{self.codice}: Prese Extra | {self.superficie:g} mq"
            f" - Padiglione {self.padiglione}"
            f" - Prezzo {self.calcola_prezzo_finale():.2f}€"
            f" - Prese aggiuntive: {self.Nprese}"
            f" - {stato}"
        )


class standpremium(stand):
    def __init__(self, codice, superficie, padiglione, prezzo, posizione):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo = float(prezzo)
        self.espositore = None
        self.posizione = posizione

    def calcola_prezzo_finale(self):
        return self.prezzo * 1.30

    def __str__(self):
        stato = "Disponibile" if self.espositore is None else "Assegnato"
        return (
            f"{self.codice}: Premium | {self.superficie:g} mq"
            f" - Padiglione {self.padiglione}"
            f" - Prezzo {self.calcola_prezzo_finale():.2f}€"
            f" - Posizione: {self.posizione}"
            f" - {stato}"
        )


class espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __str__(self):
        if self.stand is None:
            assegnazione = "Nessuno stand assegnato"
        else:
            assegnazione = f"Stand assegnato: {self.stand.codice}"

        return (
            f"{self.codice}: {self.nome} {self.cognome}"
            f" - {assegnazione}"
        )


class LingottoFiere:
    def __init__(self, nome):
        self.nome = nome
        self.stand = []
        self.espositore = []

    def carica_file_dati(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                campi = [
                    campo.strip()
                    for campo in riga.strip().split(",")
                ]

                if not campi or not campi[0]:
                    continue

                codice = campi[0]

                if codice.startswith("ST"):
                    if len(campi) == 4:
                        nuovo_stand = stand(
                            campi[0], campi[1], campi[2], campi[3]
                        )

                    elif len(campi) == 5:
                        try:
                            numero_prese = int(campi[4])
                        except ValueError:
                            nuovo_stand = standpremium(
                                campi[0], campi[1], campi[2],
                                campi[3], campi[4]
                            )
                        else:
                            nuovo_stand = standspesextra(
                                campi[0], campi[1], campi[2],
                                campi[3], numero_prese
                            )
                    else:
                        continue

                    self.stand.append(nuovo_stand)

                elif codice.startswith("ES") and len(campi) == 3:
                    nuovo_espositore = espositore(
                        campi[0], campi[1], campi[2]
                    )
                    self.espositore.append(nuovo_espositore)

    def assegna_stand_a_espositore(
        self, codice_stand, codice_espositore
    ):
        stand_trovato = None
        espositore_trovato = None

        for elemento in self.stand:
            if elemento.codice == codice_stand:
                stand_trovato = elemento
                break

        for elemento in self.espositore:
            if elemento.codice == codice_espositore:
                espositore_trovato = elemento
                break

        if stand_trovato is None:
            raise Exception("Stand non trovato")

        if espositore_trovato is None:
            raise Exception("Espositore non trovato")

        if stand_trovato.espositore is not None:
            raise Exception("Lo stand è già assegnato")

        if espositore_trovato.stand is not None:
            raise Exception("L'espositore ha già uno stand")

        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato

    def elenca_espositori(self):
        for elemento in self.espositore:
            print(elemento)

    def stand_ordinati_per_prezzo(self):
        return sorted(self.stand)
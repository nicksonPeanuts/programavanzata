import numpy as np
import json

class Palette:

    def __init__(self, file):
        self.file = file
        self.loading_file()

    # carichiamo il file json dove va caricato
    def loading_file(self):
        """
        metodo per il caricamento del file json con tutti i check di tipo per i dati
        serve per caricare il file palette con tutti i colori
        """
        with open(self.file, "r", encoding="utf-8") as file_json:
            colori = json.load(file_json)

        # verifichiamo che il file json contenga 16 colori
        if not isinstance(colori, list):
            raise TypeError("La palette non è una lista")

        if len(colori) != 16:
            raise ValueError("I colori non sono 16!")

        # check colori
        for color in colori:
            if not isinstance(color, list):
                raise TypeError("IL colore non è una lista")
            if not len(color) == 3:
                raise ValueError("RGB deve avere 3 elementi")
            for i in color:
                if not isinstance(i, int):
                    raise ValueError("I colori non sono interi")
                if not (0 <= i <= 255):
                    raise ValueError("RGB non nel range giusto")

        # salviamo solo alla fine e tutto è andato bene
        self.colori = colori

    def risolvi_indice(self, indice):
        """
        risolve gli indici dei colori da usare
        """
        # check del tipo di dato
        if not isinstance(indice, int):
            raise TypeError("indice non intero")

        if not (indice >= 0 and indice <= 15):
            raise ValueError("indice deve stare fra 0 e 15")

        return self.colori[indice]

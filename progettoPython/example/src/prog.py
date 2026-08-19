# Nome: Nicola
# Cognome: Pinat
# Matricola: SM3201546

import json
import numpy as np

class Palette():

    # DESCRIZIONE DELLA CLASSE

    # la classe palette ha bisogno del file JSON 
    def __init__(self, file):
        self.file = file
        self.loading_file()

    # carichiamo il file json dove va caricato
    def loading_file(self):
        with open(self.file, "r", encoding="utf-8") as file_json:
            colori = json.load(file_json)

        # verifichiamo che il file json contenga 16 coloriù
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
                if not (i >= 0 and i <= 255):
                    raise ValueError("RGB non nel range giusto")
            


        # salviamo solo alla fine e tutto è andato bene
        self.colori = colori

    def risolvi(self, indice):
        # check del tipo di dato
        if not isinstance(indice, int):
            raise TypeError("indice non intero")

        if not (indice >= 0 and indice <= 15):
            raise ValueError("indice deve stare fra 0 e 15")

        return self.colori[indice]


class VirtualVRAM():

    def __init__(self, tile, sprite):
        self.tile_sheet = tile
        self.sprite_sheet = sprite


        # avviamo il caricamento nel costruttore
        self.loading_files()

        self.matrix_tile = self.decoder(self.bin_tile)
        self.matrix_sprite = self.decoder(self.bin_sprite)

    def loading_files(self):

        # tiles
        with open(self.tile_sheet, "rb") as tile_sheet_bin:
            dati_tile = tile_sheet_bin.read()
            if not len(dati_tile) == 32768:
                raise ValueError("Il file non contiene 32768 byte")
            self.bin_tile = dati_tile

        # sprites
        with open(self.sprite_sheet, "rb") as sprite_sheet_bin:
            dati_sprite = sprite_sheet_bin.read()
            if not len(dati_sprite) == 32768:
                raise ValueError("Il file non contiene 32768 byte")
            self.bin_sprite = dati_sprite
        



    def decoder(self, file_encoded):
        # USIAMO I FILE BINARI E FACCIAMO IL DECODING DI QUELLO CHE DEVE ESSERE FATTO
        # trasferisco subito in una matrice 256 * 256 e poi decodifico la matrice cella per cella (?)

        matrix = np.zeros((256,256), dtype="uint8")

        for pos, byte in enumerate(file_encoded):
            # leggere i byte uno ad uno e separa i 
            # nibble
            nibble_up = byte >> 4
            nibble_down = byte & 0x0F
            matrix.flat[2*pos] = nibble_up
            matrix.flat[2*pos + 1] = nibble_down


        return matrix



    
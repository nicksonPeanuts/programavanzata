import json
import numpy as np



class VirtualVRAM:

    def __init__(self, tile, sprite):
        self.bin_sprite = None
        self.bin_tile = None
        self.tile_sheet = tile
        self.sprite_sheet = sprite


        # avviamo il caricamento nel costruttore
        self.loading_files()

        # due matrici di grandezza 256*256
        # la prima contiene valori da 0 a 15 ( colore )
        self.matrix_tile = self.decoder(self.bin_tile)

        # questa contiene valori da 0 a 15
        self.matrix_sprite = self.decoder(self.bin_sprite)

    def loading_files(self):
        """
            metodo per il caricamento del file json con tutti i check di tipo per i dati
        """
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
        """
        metodo per il decoding di un file binario,
        creiamo una matrice con numpy e iterando in file encoded facciamo
        la decodifica dei byte separando i nibble

        input: file_encoded

        output: matrice decodificata
        """

        matrix = np.zeros((256,256), dtype="uint8")

        for pos, byte in enumerate(file_encoded):
            # leggere i byte uno ad uno e separa i
            # nibble
            nibble_up = byte >> 4
            nibble_down = byte & 0x0F
            matrix.flat[2*pos] = nibble_up
            matrix.flat[2*pos + 1] = nibble_down
        return matrix

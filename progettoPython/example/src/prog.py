# Nome: Nicola
# Cognome: Pinat
# Matricola: SM3201546

import json
import numpy as np

class Palette:

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


class VirtualVRAM:

    def __init__(self, tile, sprite):
        self.bin_sprite = None
        self.bin_tile = None
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


#
class SceneParser:
    def __init__(self, scene):
        self.scene = scene
        self.transparent_index = None
        self.tile_map = None
        self.sprites = []

        # carichiamo anche qui la scena al momento della crazione dell'oggetto
        self.loading(self, scene)


    def loading(self, file_json):
        # cerchiamo di aprire il file json
        try:
            with open(file_json, "r", encoding= "utf-8") as file:
                # questo diventerà un dizionario python corrispondente
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ValueError(f"Errore nel caricamento del file JSON della scena: {e}")

        # una volta aperto e caricati i dati in data, carichiamo e verifichiamo il resto

        # TRANSPARENT INDEX:
        if "transparent_index" not in data:
            raise KeyError("La scena non contiene la chiave 'transparent_index'")

        # controlli di tipo
        trans_ind = data["transparent_index"]
        if type(trans_ind) is not int:
            raise TypeError("transparent index non è del tipo giusto")
        if not (0 <= trans_ind <= 15):
            raise ValueError("transparent index non è nel range giusto")

        self.transparent_index = data["transparent_index"]

        # TILE MAP
        if "tile_map" not in data:
            raise KeyError("La scena non contiene la chiave tile_map")
        # veritica dimensioni matrice
        tile = data["tile_map"]

        if not len(tile) == 15:
            raise ValueError("il numero di righe di tile_map non è 15")

        # controllo elementi e lunghezza della riga
        for row in tile:
            if not len(row) == 20:
                raise ValueError("il numero di elementi per riga non è 20")

            for element in row:
                if type(element) is not int:
                    raise TypeError("errore, un valore nella tile_map non è intero")
                if not 0 <= element <= 63:
                    raise ValueError("errore, un elemento nella tile_map non è nel range giusto")
        # assegnazione come numpy array, in modo da poter essere aggevolato coi calcoli successivamente
        self.tile_map = np.array(tile, dtype=np.uint8)

        # SPRITES
        if "sprites" not in data:
            raise KeyError("La scena non contiene la chiave sprites")

        sprites = data["sprites"]

        if type(sprites) is not list:
            raise TypeError("la sprites list non è una lista")

        sprites_keys = {"id", "x", "y", "flip_h", "flip_v", "rotation"}

        # validazione per ogni elemento della lista
        for element in sprites:
            # controllo che sia una instanza di dizionario
            if not isinstance(element, dict):
                raise TypeError("un elemento di sprites non è un dizionario")

            # controllo che le chiavi siano le stesse
            if set(element.keys()) != sprites_keys:
                raise KeyError("Le chiavi di un dizionario di sprites non sono quelle giuste")

            # controllo chiave valore che siano del tipo e nel range giusto
            # Validazione 'id'
            val_id = element["id"]
            if type(val_id) is not int:
                raise TypeError("id deve essere un intero")
            if not (0 <= val_id <= 15):
                raise ValueError("id deve essere compreso tra 0 e 15")

            # Validazione 'x' e 'y'
            val_x = element["x"]
            val_y = element["y"]
            if type(val_x) is not int or type(val_y) is not int:
                raise TypeError("x e y devono essere interi")

            # Validazione 'flip_h' e 'flip_v'
            val_fh = element["flip_h"]
            val_fv = element["flip_v"]
            if not isinstance(val_fh, bool) or not isinstance(val_fv, bool):
                raise TypeError("flip_h e flip_v devono essere booleani")

            # Validazione 'rotation'
            val_rot = element["rotation"]
            if type(val_rot) is not int:
                raise TypeError("rotation deve essere un intero")
            if val_rot not in {0, 90, 180, 270}:
                raise ValueError("rotation deve essere 0, 90, 180 o 270")

        # caricamento di sprites
        self.sprites = sprites



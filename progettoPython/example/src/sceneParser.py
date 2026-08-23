import numpy as np
import json


class SceneParser:
    def __init__(self, scene):
        self.scene = scene
        self.transparent_index = None
        self.tile_map = None
        self.sprites = []

        # carichiamo anche qui la scena al momento della creazione dell'oggetto
        self.loading(scene)


    def loading(self, file_json) -> None:
        """
            carichiamo il json della scena,
            input: file json della scena

        """
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

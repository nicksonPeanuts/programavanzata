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
        """
        metodo per il caricamento del file json con tutti i check di tipo per i dati
        """
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

    def risolvi_indice(self, indice):
        """
        risolve gli indici
        """
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


class SceneParser:
    def __init__(self, scene):
        self.scene = scene
        self.transparent_index = None
        self.tile_map = None
        self.sprites = []

        # carichiamo anche qui la scena al momento della crazione dell'oggetto
        self.loading(scene)


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




#   4. Una classe Blitter che permetta di estrarre tile e sprite dai rispettivi
#   sheet, applicare flip, rotazioni e trasparenza, e copiare i risultati nel frame
#   buffer.

class Blitter:
    """
    Classe responsabile dell'estrazione dei tile e degli sprite dai rispettivi
    sheet, dell'applicazione delle trasformazioni (flip, rotazioni) e della
    scrittura (blitting) con gestione della trasparenza e clipping nel frame buffer.
    """

    def __init__(self, vram: VirtualVRAM, transparent_index: int):
        """
        Inizializza il Blitter con le matrici di VRAM e l'indice di trasparenza degli sprite.
        """
        self.vram = vram
        if not isinstance(transparent_index, int) or not (0 <= transparent_index <= 15):
            raise ValueError("L'indice di trasparenza deve essere un intero tra 0 e 15")
        self.transparent_index = transparent_index

    def blit_tile(self, tile_id: int, dest_row: int, dest_col: int, frame_buffer: np.ndarray) -> None:
        """
        Estrae un tile 32x32 dallo sheet e lo copia nel frame buffer alla riga e colonna specificate.
        """
        if not (0 <= tile_id <= 63):
            raise ValueError(f"ID tile non valido: {tile_id}. Deve essere compreso tra 0 e 63.")
        if not (0 <= dest_row < 15) or not (0 <= dest_col < 20):
            raise ValueError(f"Destinazione tile map fuori dai limiti: riga {dest_row}, colonna {dest_col}")

        # Calcola le coordinate del tile nello sheet (griglia 8x8)
        t_row = tile_id // 8
        t_col = tile_id % 8

        # prendiamo solo una parte della matrice 
        tile_pixels = self.vram.matrix_tile[
            t_row * 32: (t_row + 1) * 32,
            t_col * 32: (t_col + 1) * 32
        ]

        # Scrive direttamente sul frame buffer (640x480)
        frame_buffer[
            dest_row * 32: (dest_row + 1) * 32,
            dest_col * 32: (dest_col + 1) * 32
        ] = tile_pixels

    def blit_sprite(self, sprite_id: int, dest_x: int, dest_y: int,
                    flip_h: bool, flip_v: bool, rotation: int,
                    frame_buffer: np.ndarray) -> None:
        """
        Estrae uno sprite 64x64, applica flip, rotazione, gestisce la trasparenza
        e lo copia nel frame buffer con clipping automatico se parzialmente fuori schermo.
        """
        if not (0 <= sprite_id <= 15):
            raise ValueError(f"ID sprite non valido: {sprite_id}. Deve essere compreso tra 0 e 15.")
        if rotation not in {0, 90, 180, 270}:
            raise ValueError(f"Rotazione non valida: {rotation}. Deve essere 0, 90, 180 o 270.")

        # 1. Estrazione dello sprite dallo sheet (griglia 4x4 di elementi 64x64)
        s_row = sprite_id // 4
        s_col = sprite_id % 4

        sprite = self.vram.matrix_sprite[
            s_row * 64: (s_row + 1) * 64,
            s_col * 64: (s_col + 1) * 64
        ].copy()

        # 2. Applicazione trasformazioni (prima flip, poi rotazione)
        if flip_h:
            sprite = np.fliplr(sprite)
        if flip_v:
            sprite = np.flipud(sprite)

        if rotation == 90:
            sprite = np.rot90(sprite, k=-1)  # 90° in senso orario
        elif rotation == 180:
            sprite = np.rot90(sprite, k=2)  # 180°
        elif rotation == 270:
            sprite = np.rot90(sprite, k=1)  # 270° in senso orario (90° antiorario)

        # 3. Calcolo dell'intersezione (clipping) con il frame buffer (480x640)
        y_start_fb = max(0, dest_y)
        y_end_fb = min(480, dest_y + 64)
        x_start_fb = max(0, dest_x)
        x_end_fb = min(640, dest_x + 64)

        if y_start_fb >= y_end_fb or x_start_fb >= x_end_fb:
            raise ValueError("Lo sprite è fuori dallo schermo")  # Lo sprite è completamente fuori dallo schermo

        # Calcola le coordinate relative dello sprite da copiare
        y_start_sprite = y_start_fb - dest_y
        y_end_sprite = y_end_fb - dest_y
        x_start_sprite = x_start_fb - dest_x
        x_end_sprite = x_end_fb - dest_x

        sprite_slice = sprite[y_start_sprite:y_end_sprite, x_start_sprite:x_end_sprite]
        fb_slice = frame_buffer[y_start_fb:y_end_fb, x_start_fb:x_end_fb]

        # 4. Copia considerando la trasparenza degli sprite
        mask = (sprite_slice != self.transparent_index)
        fb_slice[mask] = sprite_slice[mask]


from PIL import Image

class RenderingPipeline:
    """
    Classe responsabile della gestione dell'intera pipeline di rendering.
    Combina il fondale (tile map) e gli sprite sul frame buffer indicizzato,
    converte il buffer finale in formato RGB e salva l'immagine in PNG tramite Pillow.
    """

    def __init__(self, palette: Palette, vram: VirtualVRAM, scene: SceneParser):
        """
        Inizializza la pipeline con le istanze di Palette, VirtualVRAM e SceneParser.
        """
        if not isinstance(palette, Palette):
            raise TypeError("L'oggetto palette deve essere un'istanza di Palette")
        if not isinstance(vram, VirtualVRAM):
            raise TypeError("L'oggetto vram deve essere un'istanza di VirtualVRAM")
        if not isinstance(scene, SceneParser):
            raise TypeError("L'oggetto scene deve essere un'istanza di SceneParser")

        self.palette = palette
        self.vram = vram
        self.scene = scene

        # Inizializza il frame buffer indicizzato 480x640 (480 righe per 640 colonne)
        self.frame_buffer = np.zeros((480, 640), dtype=np.uint8)

    def render(self) -> np.ndarray:
        """
        Esegue la composizione completa della scena.
        Disegna prima l'intero fondale (tile map), poi sovrappone gli sprite
        nell'ordine in cui compaiono nel JSON della scena.
        """
        # 1. Inizializzazione del Blitter con la VRAM e l'indice di trasparenza della scena
        blitter = Blitter(self.vram, self.scene.transparent_index)

        # 2. Disegno del fondale usando la tile_map (15 righe, 20 colonne)
        for r in range(15):
            for c in range(20):
                tile_id = self.scene.tile_map[r, c]
                blitter.blit_tile(tile_id, r, c, self.frame_buffer)

        # 3. Disegno degli sprite (nell'ordine definito nel file JSON della scena)
        for sprite in self.scene.sprites:
            blitter.blit_sprite(
                sprite_id=sprite["id"],
                dest_x=sprite["x"],
                dest_y=sprite["y"],
                flip_h=sprite["flip_h"],
                flip_v=sprite["flip_v"],
                rotation=sprite["rotation"],
                frame_buffer=self.frame_buffer
            )

        return self.frame_buffer

    def convert_to_rgb(self) -> np.ndarray:
        """
        Converte il frame buffer indicizzato in un array RGB (480x640x3).
        Sfrutta l'indicizzazione avanzata di NumPy (LUT) per massimizzare le prestazioni.
        """
        # Creiamo una Look-Up Table (LUT) a partire dai colori della palette
        # self.palette.colori è una lista di 16 elementi, ciascuno è [R, G, B]
        lut = np.array(self.palette.colori, dtype=np.uint8)

        # Mappa ciascun pixel indicizzato nel frame buffer direttamente al colore RGB corrispondente
        rgb_buffer = lut[self.frame_buffer]
        return rgb_buffer

    def save_png(self, output_path: str) -> None:
        """
        Esegue l'intero rendering, converte l'output in RGB e lo salva come file PNG.
        Usa Pillow esclusivamente per la conversione finale ed il salvataggio su disco.
        """
        if not output_path.lower().endswith('.png'):
            raise ValueError("Il percorso del file di output deve avere estensione .png")

        # Genera il frame buffer composto
        self.render()

        # Converte il buffer indicizzato in RGB
        rgb_buffer = self.convert_to_rgb()

        try:
            # Crea l'immagine Pillow a partire dall'array NumPy RGB
            img = Image.fromarray(rgb_buffer, mode="RGB")
            # Salva l'immagine finale in formato PNG
            img.save(output_path)
        except OSError as e:
            raise OSError(f"Errore durante il salvataggio dell'immagine PNG '{output_path}': {e}")
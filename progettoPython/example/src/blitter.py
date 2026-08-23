import numpy as np
import json

from virtualRAM import VirtualVRAM


class Blitter:
    """
    Classe responsabile dell'estrazione dei tile e degli sprite dai rispettivi
    sheet, dell'applicazione delle trasformazioni (flip, rotazioni) e della
    scrittura (blitting) con gestione della trasparenza e clipping nel frame buffer.
    """

    def __init__(self, vram: VirtualVRAM, transparent_index: int):
        """
        input: vram ( oggetto VirtualRAM e trasparent index )
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

        # Scrive direttamente sul frame buffer (640x480), il nostro "schermo"
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

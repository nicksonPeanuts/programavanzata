import numpy as np
from PIL import Image
from blitter import Blitter
from palette import Palette
from virtualRAM import VirtualVRAM
from sceneParser import SceneParser

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

    def run_rendering(self, output_path: str) -> None:
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
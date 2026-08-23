# Nome: Nicola
# Cognome: Pinat
# Matricola: SM3201546

import sys
from classi import Palette, VirtualVRAM, SceneParser, RenderingPipeline

def main():
    """
    Funzione principale del programma. Riceve gli argomenti da riga di comando,
    valida l'input, istanzia la pipeline di rendering ed esporta l'immagine PNG.
    """
    # Verifica che il numero di argomenti sia esattamente quello richiesto
    if len(sys.argv) != 6:
        print("Uso corretto: python main.py <palette.json> <scene.json> <tiles.bin> <sprites.bin> <output.png>")
        raise ValueError(f"Numero di argomenti errato. Previsti 5 argomenti, ricevuti {len(sys.argv) - 1}")

    palette_path = sys.argv[1]
    scene_path = sys.argv[2]
    tiles_path = sys.argv[3]
    sprites_path = sys.argv[4]
    output_path = sys.argv[5]

    print("--- Inizio rendering della scena ---")
    print(f"Palette: {palette_path}")
    print(f"Scena: {scene_path}")
    print(f"Tiles: {tiles_path}")
    print(f"Sprites: {sprites_path}")
    print(f"Output: {output_path}")

    # Caricamento e parsing delle risorse con gestione degli errori
    try:
        palette = Palette(palette_path)
    except Exception as e:
        raise ValueError(f"Errore nel caricamento della Palette: {e}")

    try:
        scene = SceneParser(scene_path)
    except Exception as e:
        raise ValueError(f"Errore nel parsing della Scena: {e}")

    try:
        vram = VirtualVRAM(scene_path=tiles_path, sprite_path=sprites_path)
    except TypeError:
        # Nel caso in cui il costruttore di VirtualVRAM utilizzi argomenti posizionali o nomi diversi
        try:
            vram = VirtualVRAM(tiles_path, sprites_path)
        except Exception as e:
            raise ValueError(f"Errore nel caricamento dei dati binari in VirtualVRAM: {e}")
    except Exception as e:
        raise ValueError(f"Errore nel caricamento dei dati binari in VirtualVRAM: {e}")

    # Esecuzione della pipeline di rendering e salvataggio dell'immagine
    try:
        pipeline = RenderingPipeline(palette, vram, scene)
        pipeline.save_png(output_path)
    except Exception as e:
        raise RuntimeError(f"Errore durante l'esecuzione del renderer: {e}")

    print("Rendering completato con successo!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Si e' verificato un errore critico: {e}", file=sys.stderr)
        sys.exit(1)

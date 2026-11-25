import os
import glob
from PIL import Image

BRAIN_DIR = r"C:\Users\ADMIN\.gemini\antigravity\brain\73b9c58f-058c-426a-b43f-d34ec4624adc"

# Mapping prefix to destination targets and target size
ASSET_CONFIG = {
    # Relics (512x512)
    "item_hammer_celestial": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_hammer_celestial.webp",
            r"webgame\assets\art\items\item_hammer_celestial.webp",
        ]
    },
    "item_anvil_primordial": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_anvil_primordial.webp",
            r"webgame\assets\art\items\item_anvil_primordial.webp",
        ]
    },
    "item_bellows_samadhi": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_bellows_samadhi.webp",
            r"webgame\assets\art\items\item_bellows_samadhi.webp",
        ]
    },
    "item_gauntlets_dragonscale": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_gauntlets_dragonscale.webp",
            r"webgame\assets\art\items\item_gauntlets_dragonscale.webp",
        ]
    },
    "item_apron_celestial_mail": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_apron_celestial_mail.webp",
            r"webgame\assets\art\items\item_apron_celestial_mail.webp",
        ]
    },
    "item_relic_bagua_core": {
        "size": (512, 512),
        "dests": [
            r"frontend\public\assets\art\items\item_relic_bagua_core.webp",
            r"webgame\assets\art\items\item_relic_bagua_core.webp",
        ]
    },

    # Runes (256x256)
    "gem_rune_thunder": {
        "size": (256, 256),
        "dests": [
            r"frontend\public\assets\art\runes\gem_rune_thunder.webp",
            r"webgame\assets\art\runes\gem_rune_thunder.webp",
        ]
    },
    "gem_rune_fire": {
        "size": (256, 256),
        "dests": [
            r"frontend\public\assets\art\runes\gem_rune_fire.webp",
            r"webgame\assets\art\runes\gem_rune_fire.webp",
        ]
    },
    "gem_rune_gravity": {
        "size": (256, 256),
        "dests": [
            r"frontend\public\assets\art\runes\gem_rune_gravity.webp",
            r"webgame\assets\art\runes\gem_rune_gravity.webp",
        ]
    },
    "gem_rune_mystic": {
        "size": (256, 256),
        "dests": [
            r"frontend\public\assets\art\runes\gem_rune_mystic.webp",
            r"webgame\assets\art\runes\gem_rune_mystic.webp",
        ]
    },
    "gem_rune_fortune": {
        "size": (256, 256),
        "dests": [
            r"frontend\public\assets\art\runes\gem_rune_fortune.webp",
            r"webgame\assets\art\runes\gem_rune_fortune.webp",
        ]
    },

    # Stat Sigils (128x128)
    "sigil_stat_str": {
        "size": (128, 128),
        "dests": [
            r"frontend\public\assets\art\sigils\sigil_stat_str.webp",
            r"webgame\assets\art\sigils\sigil_stat_str.webp",
        ]
    },
    "sigil_stat_agi": {
        "size": (128, 128),
        "dests": [
            r"frontend\public\assets\art\sigils\sigil_stat_agi.webp",
            r"webgame\assets\art\sigils\sigil_stat_agi.webp",
        ]
    },
    "sigil_stat_int": {
        "size": (128, 128),
        "dests": [
            r"frontend\public\assets\art\sigils\sigil_stat_int.webp",
            r"webgame\assets\art\sigils\sigil_stat_int.webp",
        ]
    },
    "sigil_stat_pen": {
        "size": (128, 128),
        "dests": [
            r"frontend\public\assets\art\sigils\sigil_stat_pen.webp",
            r"webgame\assets\art\sigils\sigil_stat_pen.webp",
        ]
    },
    "sigil_stat_spr": {
        "size": (128, 128),
        "dests": [
            r"frontend\public\assets\art\sigils\sigil_stat_spr.webp",
            r"webgame\assets\art\sigils\sigil_stat_spr.webp",
        ]
    },
}

def process_all():
    found_count = 0
    for key, cfg in ASSET_CONFIG.items():
        pattern = os.path.join(BRAIN_DIR, f"{key}_*.jpg")
        matches = glob.glob(pattern)
        if not matches:
            print(f"[-] Waiting for: {key}")
            continue
        # Pick the latest matching file
        latest_file = max(matches, key=os.path.getmtime)
        size = cfg["size"]
        try:
            im = Image.open(latest_file).convert("RGBA")
            if im.size != size:
                im = im.resize(size, Image.Resampling.LANCZOS)
            for dest in cfg["dests"]:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                im.save(dest, "WEBP", quality=90)
                print(f"[+] Converted {os.path.basename(latest_file)} -> {dest} ({size[0]}x{size[1]})")
            found_count += 1
        except Exception as e:
            print(f"[!] Error converting {latest_file}: {e}")
    
    print(f"\nSummary: {found_count} / {len(ASSET_CONFIG)} assets processed.")
    return found_count

if __name__ == "__main__":
    process_all()

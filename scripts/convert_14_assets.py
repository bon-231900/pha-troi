import os
from PIL import Image
import numpy as np

os.makedirs('webgame/assets/art', exist_ok=True)
os.makedirs('frontend/public/assets/art', exist_ok=True)

assets = [
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/sky_celestial_moon_raw_1793790849125.jpg',
        'dst': 'sky_celestial_moon.webp',
        'mode': 'screen'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/sky_cracks_overlay_raw_1793790863841.jpg',
        'dst': 'sky_cracks_overlay.webp',
        'mode': 'screen'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/sky_aurora_nebula_raw_1793790894296.jpg',
        'dst': 'sky_aurora_nebula.webp',
        'mode': 'screen'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/sky_drifting_clouds_raw_1793790908985.jpg',
        'dst': 'sky_drifting_clouds.webp',
        'mode': 'screen'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/mid_peer_blacksmiths_raw_1793790872404.jpg',
        'dst': 'mid_peer_blacksmiths.webp',
        'mode': 'black_key'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/bg_distant_mountains_clean_v2_1793790907409.jpg',
        'dst': 'bg_distant_mountains_clean.webp',
        'mode': 'mountains'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/mid_stepped_terraces_raw_1793790921063.jpg',
        'dst': 'mid_stepped_terraces.webp',
        'mode': 'black_key'
    },
    {
        'src': 'C:/Users/ADMIN/.gemini/antigravity/brain/4ac532ff-c4ae-4325-afcc-f630c6b43d10/floating_daoist_shrine_island_1793790932739.jpg',
        'dst': 'bg_floating_temple.webp',
        'mode': 'black_key'
    }
]

for a in assets:
    im = Image.open(a['src']).convert('RGBA')
    arr = np.array(im, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    lum = (r * 0.299 + g * 0.587 + b * 0.114)
    
    if a['mode'] == 'screen':
        alpha = np.clip(lum * 1.5, 0, 255)
        arr[:, :, 3] = alpha
    elif a['mode'] == 'black_key':
        alpha = np.clip((lum - 10.0) * 12.0, 0, 255)
        arr[:, :, 3] = alpha
    elif a['mode'] == 'mountains':
        alpha = np.clip((lum - 14.0) * 10.0, 0, 255)
        arr[:, :, 3] = alpha
    
    out_im = Image.fromarray(arr.astype(np.uint8))
    p1 = os.path.join('webgame/assets/art', a['dst'])
    p2 = os.path.join('frontend/public/assets/art', a['dst'])
    out_im.save(p1, 'WEBP', quality=90)
    out_im.save(p2, 'WEBP', quality=90)
    print(f"Successfully converted {a['dst']} -> {out_im.size}")

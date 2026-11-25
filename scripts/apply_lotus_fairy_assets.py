# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from PIL import Image

SRC_IMG = r'C:\Users\ADMIN\.gemini\antigravity\brain\73b9c58f-058c-426a-b43f-d34ec4624adc\.user_uploaded\media_1794034957401_4fcc3aa4.jpg'
src = cv2.imread(SRC_IMG)
H, W, _ = src.shape
row2_bgr = src[H//2:H, :]

FRAME_W = 360
FRAME_H = 480
TARGET_PED_X = 238
TARGET_PED_Y = 318
SCALE = 2.45

# Pedestal template from Slice 0
ped_tmpl = row2_bgr[85:136, 75:115]

chosen_slices = [
    (0, 130),    # 0: Idle
    (125, 260),  # 1: Qi gather
    (365, 530),  # 2: Condense
    (515, 695),  # 3: Launch
    (685, 875),  # 4: Impact explosion
    (860, 1024), # 5: Recovery
]

def extract_alpha_clean(bgr_crop):
    b, g, r = cv2.split(bgr_crop)
    max_c = np.maximum(np.maximum(b, g), r).astype(np.float32)
    alpha = np.clip((max_c - 13.0) / 28.0, 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    gray = cv2.cvtColor(bgr_crop, cv2.COLOR_BGR2GRAY)
    _, solid_thresh = cv2.threshold(gray, 28, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(solid_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid_mask = np.zeros_like(gray)
    for c in cnts:
        if cv2.contourArea(c) > 300:
            cv2.drawContours(solid_mask, [c], -1, 255, -1)
            
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    solid_mask = cv2.erode(solid_mask, kernel, iterations=1)
    final_alpha = np.where(solid_mask > 0, np.maximum(alpha, 255), alpha)
    
    a_norm = np.clip(final_alpha.astype(np.float32) / 255.0, 0.001, 1.0)
    un_b = np.clip(b.astype(np.float32) / (a_norm ** 0.75), 0, 255).astype(np.uint8)
    un_g = np.clip(g.astype(np.float32) / (a_norm ** 0.75), 0, 255).astype(np.uint8)
    un_r = np.clip(r.astype(np.float32) / (a_norm ** 0.75), 0, 255).astype(np.uint8)
    
    return cv2.merge([un_b, un_g, un_r, final_alpha])

frames = []
for idx, (x0, x1) in enumerate(chosen_slices):
    crop_bgr = row2_bgr[:, x0:x1]
    
    sub_res = cv2.matchTemplate(crop_bgr, ped_tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(sub_res)
    ped_local_x, ped_local_y = max_loc
    
    rgba = extract_alpha_clean(crop_bgr)
    
    nw = int(crop_bgr.shape[1] * SCALE)
    nh = int(crop_bgr.shape[0] * SCALE)
    scaled_rgba = cv2.resize(rgba, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    scaled_ped_x = int(ped_local_x * SCALE)
    scaled_ped_y = int(ped_local_y * SCALE)
    
    canvas = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
    
    paste_x = TARGET_PED_X - scaled_ped_x
    paste_y = TARGET_PED_Y - scaled_ped_y
    
    dst_y0 = max(0, paste_y)
    dst_y1 = min(FRAME_H, paste_y + nh)
    dst_x0 = max(0, paste_x)
    dst_x1 = min(FRAME_W, paste_x + nw)
    
    src_y0 = max(0, -paste_y)
    src_y1 = src_y0 + (dst_y1 - dst_y0)
    src_x0 = max(0, -paste_x)
    src_x1 = src_x0 + (dst_x1 - dst_x0)
    
    canvas[dst_y0:dst_y1, dst_x0:dst_x1] = scaled_rgba[src_y0:src_y1, src_x0:src_x1]
    
    pil_frame = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
    frames.append(pil_frame)

# 1. Save Strip (2160x480)
strip = Image.new('RGBA', (2160, 480), (0, 0, 0, 0))
for i, f in enumerate(frames):
    strip.paste(f, (i * 360, 0))

fe_strip_path = 'frontend/public/assets/art/skins/skin_mystic_fairy/spritesheet_strip.webp'
wg_strip_path = 'webgame/assets/art/skins/skin_mystic_fairy/spritesheet_strip.webp'

strip.save(fe_strip_path, 'WEBP', lossless=True)
strip.save(wg_strip_path, 'WEBP', lossless=True)

# 2. Save Card (270x360)
# Crop around Frame 0 character
card_crop = frames[0].crop((20, 85, 290, 445)) # 270x360
fe_card_path = 'frontend/public/assets/art/skins/skin_mystic_fairy/card.webp'
wg_card_path = 'webgame/assets/art/skins/skin_mystic_fairy/card.webp'

card_crop.save(fe_card_path, 'WEBP', quality=95)
card_crop.save(wg_card_path, 'WEBP', quality=95)

# 3. Save test frame 0
frames[0].save('frontend/public/assets/art/skins/skin_mystic_fairy/frame0_test.png')
frames[0].save('webgame/assets/art/skins/skin_mystic_fairy/frame0_test.png')

print("Successfully packaged Lotus Fairy spritesheet & card into frontend and webgame!")

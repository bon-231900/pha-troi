# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from PIL import Image

SRC_IMG = r'C:\Users\ADMIN\.gemini\antigravity\brain\73b9c58f-058c-426a-b43f-d34ec4624adc\.user_uploaded\media_1794034957401_4fcc3aa4.jpg'
OUT_DIR = 'frontend/public/assets/art/skins/skin_mystic_fairy'

# Load source
src = cv2.imread(SRC_IMG)
assert src is not None, "Failed to load source image!"
H, W, _ = src.shape

# Split Row 1 and Row 2
row1_bgr = src[0:H//2, :]
row2_bgr = src[H//2:H, :]

FRAME_W = 360
FRAME_H = 480
BASELINE_Y = 440

def extract_alpha(bgr_crop, th_low=12, th_high=35):
    """Clean black background removal with smooth edge feathering and glow preservation"""
    b, g, r = cv2.split(bgr_crop)
    max_c = np.maximum(np.maximum(b, g), r).astype(np.float32)
    alpha = np.clip((max_c - th_low) / float(th_high - th_low), 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    # Internal body mask protection (ensure clothes/hair inside aren't semi-transparent)
    gray = cv2.cvtColor(bgr_crop, cv2.COLOR_BGR2GRAY)
    _, solid_thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(solid_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid_mask = np.zeros_like(gray)
    for c in cnts:
        if cv2.contourArea(c) > 400:
            cv2.drawContours(solid_mask, [c], -1, 255, -1)
            
    # Erode solid mask slightly so external glow stays soft
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    solid_mask = cv2.erode(solid_mask, kernel, iterations=1)
    final_alpha = np.where(solid_mask > 0, np.maximum(alpha, 255), alpha)
    
    return cv2.merge([b, g, r, final_alpha])

def build_strip_from_slices(row_bgr, slice_boxes, scale_factor=2.85, char_center_x=175):
    """Process a series of slices into 6 aligned 360x480 frames"""
    processed_frames = []
    
    for idx, (x0, x1) in enumerate(slice_boxes):
        crop_bgr = row_bgr[:, x0:x1]
        rgba = extract_alpha(crop_bgr)
        
        # Find feet/pedestal bottom
        alpha = rgba[:, :, 3]
        ys, xs = np.where(alpha > 35)
        if len(ys) == 0:
            continue
            
        fig_h = ys.max() - ys.min()
        fig_w = xs.max() - xs.min()
        
        # Scale figure smoothly
        new_w = int(crop_bgr.shape[1] * scale_factor)
        new_h = int(crop_bgr.shape[0] * scale_factor)
        scaled_rgba = cv2.resize(rgba, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Recalculate scaled bounds
        s_alpha = scaled_rgba[:, :, 3]
        s_ys, s_xs = np.where(s_alpha > 35)
        
        scaled_bottom = s_ys.max()
        scaled_center_x = (s_xs.min() + s_xs.max()) // 2
        
        # Create standard 360x480 canvas
        canvas = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)
        
        # Calculate paste coordinates
        offset_y = BASELINE_Y - scaled_bottom
        offset_x = char_center_x - scaled_center_x
        
        # Bounding box on canvas
        dst_y0 = max(0, offset_y)
        dst_y1 = min(FRAME_H, offset_y + new_h)
        dst_x0 = max(0, offset_x)
        dst_x1 = min(FRAME_W, offset_x + new_w)
        
        src_y0 = max(0, -offset_y)
        src_y1 = src_y0 + (dst_y1 - dst_y0)
        src_x0 = max(0, -offset_x)
        src_x1 = src_x0 + (dst_x1 - dst_x0)
        
        canvas[dst_y0:dst_y1, dst_x0:dst_x1] = scaled_rgba[src_y0:src_y1, src_x0:src_x1]
        
        pil_frame = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
        processed_frames.append(pil_frame)
        
    return processed_frames

# Select 6 frames from Row 2 (The Standing Lotus Mudra & Blast sequence):
# Frame 0: Idle (Fig 0)
# Frame 1: Wind-up Qi (Fig 1)
# Frame 2: Apex Condensation (Fig 3)
# Frame 3: Lotus Wave Launch (Fig 4)
# Frame 4: Giant Lotus Impact Burst (Fig 5)
# Frame 5: Settled Glow Recovery (Fig 6)
row2_slices_6 = [
    (10, 125),   # 0: Idle
    (125, 250),  # 1: Windup Qi
    (375, 520),  # 2: Apex
    (520, 690),  # 3: Launch
    (690, 865),  # 4: Impact Burst
    (865, 1022), # 5: Recovery
]

frames_r2 = build_strip_from_slices(row2_bgr, row2_slices_6, scale_factor=2.95, char_center_x=175)

# Also test Row 1 (Airborne Swoop & Arc):
row1_slices_6 = [
    (15, 138),   # 0: Idle
    (155, 285),  # 1: Windup
    (295, 420),  # 2: Levitate
    (430, 555),  # 3: Airborne charge
    (575, 710),  # 4: Arc slash slam
    (725, 870),  # 5: Landing impact
]
frames_r1 = build_strip_from_slices(row1_bgr, row1_slices_6, scale_factor=2.80, char_center_x=175)

# Save test animation GIFs to brain directory
brain_dir = r'C:\Users\ADMIN\.gemini\antigravity\brain\73b9c58f-058c-426a-b43f-d34ec4624adc'
frames_r2[0].save(os.path.join(brain_dir, 'lotus_fairy_r2_preview.gif'), save_all=True, append_images=frames_r2[1:], duration=140, loop=0)
frames_r1[0].save(os.path.join(brain_dir, 'lotus_fairy_r1_preview.gif'), save_all=True, append_images=frames_r1[1:], duration=140, loop=0)

# Build Row 2 6-frame strip (2160 x 480)
strip_r2 = Image.new('RGBA', (2160, 480), (0, 0, 0, 0))
for i, f in enumerate(frames_r2):
    strip_r2.paste(f, (i * 360, 0))

strip_r2.save(os.path.join(brain_dir, 'lotus_fairy_r2_strip.webp'), 'WEBP', lossless=True)

# Build Row 1 6-frame strip (2160 x 480)
strip_r1 = Image.new('RGBA', (2160, 480), (0, 0, 0, 0))
for i, f in enumerate(frames_r1):
    strip_r1.paste(f, (i * 360, 0))

strip_r1.save(os.path.join(brain_dir, 'lotus_fairy_r1_strip.webp'), 'WEBP', lossless=True)

print("Generated both preview GIFs and 6-frame spritesheet strips successfully!")

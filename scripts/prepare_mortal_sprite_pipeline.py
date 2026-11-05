# -*- coding: utf-8 -*-
"""
Pipeline xử lý và đóng gói Sprite Sheet chuẩn 6 Khung Hình cho Phàm Nhân Thiết Tượng (skin_default)
Quy chuẩn:
- Per-frame: 360 x 480 px
- Spritesheet strip: 2160 x 480 px (6 frames)
- Feet anchor: y = 440
- Anvil strike: (213, 342)
"""
import os
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import cv2
import numpy as np
from PIL import Image

def remove_black_background(img_bgr, threshold=15, soft_range=30):
    """Tách nền đen sạch sẽ, giữ nguyên chi tiết tóc và khói tàn lửa"""
    # Max of B, G, R channels
    max_c = np.max(img_bgr, axis=2).astype(np.float32)
    # Alpha mask: 0 when max_c <= threshold, ramps up to 255 at threshold + soft_range
    alpha = np.clip((max_c - threshold) / float(soft_range), 0.0, 1.0) * 255.0
    alpha = alpha.astype(np.uint8)
    
    # Fill internal holes (nếu cơ thể bên trong có vùng tối)
    # Lấy contours ngoài cùng của vật thể
    thresh_bin = (alpha > 40).astype(np.uint8) * 255
    contours, _ = cv2.findContours(thresh_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    solid_mask = np.zeros_like(alpha)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            cv2.drawContours(solid_mask, [cnt], -1, 255, -1)
            
    # Bên trong body chắc chắn alpha = 255
    final_alpha = np.where(solid_mask > 0, np.maximum(alpha, 255), alpha)
    
    # Ghép BGR + Alpha
    b, g, r = cv2.split(img_bgr)
    return cv2.merge([b, g, r, final_alpha])

def find_feet_and_scale(rgba_img, target_char_height=360):
    """Tìm đáy chân nhân vật và scale về chiều cao chuẩn trong khung 360x480"""
    alpha = rgba_img[:, :, 3]
    ys, xs = (alpha > 30).nonzero()
    if len(ys) == 0:
        return rgba_img, 0, 0
    min_y, max_y = ys.min(), ys.max()
    min_x, max_x = xs.min(), xs.max()
    
    char_h = max_y - min_y
    scale = target_char_height / float(char_h)
    new_w = int(rgba_img.shape[1] * scale)
    new_h = int(rgba_img.shape[0] * scale)
    
    scaled = cv2.resize(rgba_img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    return scaled, scale, max_y * scale

print("Mortal Sprite Pipeline ready.")

import os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import numpy as np

os.makedirs('webgame/assets/art/sky_states', exist_ok=True)
os.makedirs('frontend/public/assets/art/sky_states', exist_ok=True)

base_crack_path = 'webgame/assets/art/sky_cracks_overlay.webp'
crack_im = Image.open(base_crack_path).convert('RGBA')
cw, ch = crack_im.size # 1376, 768

crack_arr = np.array(crack_im, dtype=np.float32)
r = crack_arr[:, :, 0]
g = crack_arr[:, :, 1]
b = crack_arr[:, :, 2]
a = crack_arr[:, :, 3]
lum = r * 0.299 + g * 0.587 + b * 0.114

# Center of celestial dome nexus
cy, cx = ch * 0.45, cw * 0.5
y_coords, x_coords = np.ogrid[:ch, :cw]
dist = np.sqrt(((x_coords - cx) / (cw * 0.5))**2 + ((y_coords - cy) / (ch * 0.5))**2)

# =========================================================================
# STATE 1: LÀNH LẶN NGUYÊN VẸN (100% HP - Pristine Sky Vault)
# =========================================================================
# Hoàn toàn trong suốt (0% vết nứt)
s1 = np.zeros((ch, cw, 4), dtype=np.uint8)
im1 = Image.fromarray(s1)
im1.save('webgame/assets/art/sky_states/sky_state_1_pristine.webp', 'WEBP', quality=90)
im1.save('frontend/public/assets/art/sky_states/sky_state_1_pristine.webp', 'WEBP', quality=90)
print('Saved State 1: Pristine')

# =========================================================================
# STATE 2: CHỚM NỨT (80% HP - Incipient Hairline Fractures)
# =========================================================================
# Chỉ xuất hiện các tia nứt mảnh nhẹ tại tâm (dist < 0.32)
# Chuyển sắc thái sang ánh bạc - lân tinh huyền ảo
mask2 = np.clip((0.32 - dist) / 0.15, 0, 1)
# Chỉ lấy các đường nứt sắc bén (lum > 70)
mask2 = mask2 * np.clip((lum - 50.0) / 60.0, 0, 1)

arr2 = np.zeros_like(crack_arr)
# Sắc thái Lôi Đỉnh / Bạc Ánh Trăng: R, G, B ngả sang cyan-gold
arr2[:, :, 0] = np.clip(r * 0.6 + 60, 0, 255)
arr2[:, :, 1] = np.clip(g * 0.85 + 90, 0, 255)
arr2[:, :, 2] = np.clip(b * 1.2 + 130, 0, 255)
arr2[:, :, 3] = np.clip(a * mask2 * 0.85, 0, 255)

im2 = Image.fromarray(arr2.astype(np.uint8))
im2.save('webgame/assets/art/sky_states/sky_state_2_incipient.webp', 'WEBP', quality=90)
im2.save('frontend/public/assets/art/sky_states/sky_state_2_incipient.webp', 'WEBP', quality=90)
print('Saved State 2: Incipient')

# =========================================================================
# STATE 3: RẠN NỨT LAN TỎA (60% HP - Spreading Fractures)
# =========================================================================
# Vết nứt lan ra bán kính 60% (dist < 0.62)
mask3 = np.clip((0.62 - dist) / 0.20, 0, 1)
mask3 = mask3 * np.clip((lum - 30.0) / 45.0, 0, 1)

arr3 = np.zeros_like(crack_arr)
# Màu vàng kim - hổ phách
arr3[:, :, 0] = np.clip(r * 1.1, 0, 255)
arr3[:, :, 1] = np.clip(g * 0.95, 0, 255)
arr3[:, :, 2] = np.clip(b * 0.5, 0, 255)
arr3[:, :, 3] = np.clip(a * mask3 * 0.92, 0, 255)

im3 = Image.fromarray(arr3.astype(np.uint8))
im3.save('webgame/assets/art/sky_states/sky_state_3_spreading.webp', 'WEBP', quality=90)
im3.save('frontend/public/assets/art/sky_states/sky_state_3_spreading.webp', 'WEBP', quality=90)
print('Saved State 3: Spreading')

# =========================================================================
# STATE 4: NỨT VỠ NẶNG NỀ (40% HP - Severe Molten Chasms)
# =========================================================================
# Vết nứt lan ra 85% diện tích (dist < 0.90)
mask4 = np.clip((0.90 - dist) / 0.22, 0, 1)

arr4 = np.zeros_like(crack_arr)
# Màu cam lửa dung nham rực cháy
arr4[:, :, 0] = np.clip(r * 1.15 + 20, 0, 255)
arr4[:, :, 1] = np.clip(g * 0.85, 0, 255)
arr4[:, :, 2] = np.clip(b * 0.35, 0, 255)
arr4[:, :, 3] = np.clip(a * mask4, 0, 255)

im4 = Image.fromarray(arr4.astype(np.uint8))
im4.save('webgame/assets/art/sky_states/sky_state_4_severe.webp', 'WEBP', quality=90)
im4.save('frontend/public/assets/art/sky_states/sky_state_4_severe.webp', 'WEBP', quality=90)
print('Saved State 4: Severe')

# =========================================================================
# STATE 5: THIÊN KIẾP SỤP ĐỔ (20% HP - Cataclysmic Fractures)
# =========================================================================
# 100% vết nứt bung tỏa cực đại, rực lửa đỏ thẫm
arr5 = np.zeros_like(crack_arr)
arr5[:, :, 0] = np.clip(r * 1.25 + 40, 0, 255)
arr5[:, :, 1] = np.clip(g * 0.80, 0, 255)
arr5[:, :, 2] = np.clip(b * 0.25, 0, 255)
arr5[:, :, 3] = np.clip(a * 1.1, 0, 255)

im5 = Image.fromarray(arr5.astype(np.uint8))
im5.save('webgame/assets/art/sky_states/sky_state_5_cataclysm.webp', 'WEBP', quality=90)
im5.save('frontend/public/assets/art/sky_states/sky_state_5_cataclysm.webp', 'WEBP', quality=90)
print('Saved State 5: Cataclysm')

# =========================================================================
# STATE 6: MÁI VÒM TAN VỠ HOÀN TOÀN / PHÁ TRỜI (0% HP - Complete Shatter)
# =========================================================================
# Hạch tâm nổ toang, lộ ra lỗ hổng vũ trụ khổng lồ, hàng ngàn mảnh vỡ tinh thể văng tứ phía
arr6 = np.zeros_like(crack_arr)

# Lỗ hổng trung tâm vỡ toang (core blowout): vùng tâm trắng chói lòa
core_blowout = np.clip(1.0 - (dist / 0.42), 0, 1) ** 2
# Mảnh vỡ xung quanh (debris shards): gia tăng độ sáng và góc văng
np.random.seed(42)
shatter_noise = np.random.uniform(0.6, 1.4, size=(ch, cw))

arr6[:, :, 0] = np.clip(r * 1.3 * shatter_noise + core_blowout * 255, 0, 255)
arr6[:, :, 1] = np.clip(g * 1.0 * shatter_noise + core_blowout * 240, 0, 255)
arr6[:, :, 2] = np.clip(b * 0.8 * shatter_noise + core_blowout * 200, 0, 255)
arr6[:, :, 3] = np.clip(a * 1.25 + core_blowout * 255, 0, 255)

im6 = Image.fromarray(arr6.astype(np.uint8))
im6.save('webgame/assets/art/sky_states/sky_state_6_shattered.webp', 'WEBP', quality=90)
im6.save('frontend/public/assets/art/sky_states/sky_state_6_shattered.webp', 'WEBP', quality=90)
print('Saved State 6: Shattered')

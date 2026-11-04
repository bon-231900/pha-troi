# -*- coding: utf-8 -*-
with open('webgame/demo_parallax_forge.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace render section with professional, balanced composition
target_start = "      // BASE GROUND LINE (Nơi nhân vật, đe và đài đá cùng đứng chuẩn xác)"
target_end = "      // LAYER 6: FOREGROUND PILLARS (Chỉ hiện khi người dùng bật, đẩy sát 2 mép)"

new_render = """      // =============================================================
      // BỐ CỤC CHUẨN XÁC, LOGIC & THOÁNG ĐÃNG
      // =============================================================
      // 1. Mặt sàn chuẩn (Ground Line) ở 75% chiều cao màn hình
      const groundY = height * 0.78;
      const centerX = width * 0.5;

      // -------------------------------------------------------------
      // LAYER 0: BẦU TRỜI ĐÊM HUYỀN BÍ & VÒM THIÊN CẤM
      // -------------------------------------------------------------
      const gradSky = ctx.createLinearGradient(0, 0, 0, height);
      gradSky.addColorStop(0, '#040711');
      gradSky.addColorStop(0.45, '#080E1E');
      gradSky.addColorStop(0.75, '#0B132B');
      gradSky.addColorStop(1, '#020408');
      ctx.fillStyle = gradSky;
      ctx.fillRect(0, 0, width, height);

      // Tinh vân & Cực quang tiên hiệp
      const nebTime = now * 0.0004;
      ctx.save();
      ctx.globalAlpha = 0.28;
      ctx.fillStyle = SECT_COLORS[currentSect].glow;
      ctx.filter = 'blur(70px)';
      ctx.beginPath();
      ctx.ellipse(centerX, height * 0.22, width * 0.35, height * 0.12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // -------------------------------------------------------------
      // LAYER 1: DÃY NÚI TIÊN CẢNH (HẬU CẢNH XA - Parallax 0.015)
      // Đặt nằm ngang đường chân trời, mở rộng không gian thoáng đãng
      // -------------------------------------------------------------
      const mountainAsset = ASSETS.mountain;
      if (mountainAsset.loaded) {
        const paraX1 = currentMouseX * 16;
        const paraY1 = currentMouseY * 6;
        const mImg = mountainAsset.img;
        
        const mScale = Math.max(width / mImg.width, (height * 0.65) / mImg.height);
        const mW = mImg.width * mScale;
        const mH = mImg.height * mScale;
        const mX = (width - mW) * 0.5 - paraX1;
        // Đặt chân núi hạ thấp xuống phía dưới
        const mY = groundY - mH * 0.72 - paraY1;

        ctx.save();
        ctx.globalAlpha = 0.85;
        ctx.drawImage(mImg, mX, mY, mW, mH);
        ctx.restore();
      }

      // -------------------------------------------------------------
      // LAYER 2: ĐẠI HỎA LÒ CỬU TRỌNG (ĐẶT BÊN CÁNH TRÁI HẬU CẢNH - Parallax 0.035)
      // Đặt ở vị trí hợp lý trong khu lò rèn, KHÔNG ĐÈ LÊN ĐẦU NHÂN VẬT!
      // -------------------------------------------------------------
      const furnaceAsset = ASSETS.furnace;
      if (furnaceAsset.loaded) {
        const paraX2 = currentMouseX * 28;
        const paraY2 = currentMouseY * 10;
        const fImg = furnaceAsset.img;

        // Kích thước chuẩn trung cảnh: cao 220px, đặt bên cánh trái (width * 0.22)
        const fH = Math.min(230, height * 0.32);
        const fScale = fH / fImg.height;
        const fW = fImg.width * fScale;
        const fX = width * 0.22 - fW * 0.5 - paraX2;
        const fY = groundY - fH + 15 - paraY2;

        // Hào quang lửa lò bập bùng
        const flamePulse = 0.7 + Math.sin(now * 0.005) * 0.2 + (flashIntensity * 0.4);
        ctx.save();
        ctx.globalAlpha = 0.45 * flamePulse;
        ctx.filter = 'blur(25px)';
        ctx.fillStyle = '#FF5500';
        ctx.beginPath();
        ctx.ellipse(fX + fW * 0.5, fY + fH * 0.55, fW * 0.45, fH * 0.3, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Vẽ thân lò rèn khổng lồ
        ctx.drawImage(fImg, fX, fY, fW, fH);
      }

      // -------------------------------------------------------------
      // LAYER 3: VẠN CỔ ĐÚC THẦN ĐÀI (BỆ ĐÁ SÀN NHÀ - Parallax 0.06)
      // Nằm vững chãi dưới chân nhân vật và đe thần!
      // -------------------------------------------------------------
      const altarAsset = ASSETS.altar;
      const paraX3 = currentMouseX * 42;
      const paraY3 = currentMouseY * 14;

      if (altarAsset.loaded) {
        const aImg = altarAsset.img;
        // Bệ đá rộng nâng đỡ cả nhân vật và đe
        const aW = Math.min(680, width * 0.75);
        const aScale = aW / aImg.width;
        const aH = aImg.height * aScale;
        const aX = centerX - aW * 0.5 - paraX3;
        // Đặt mặt phẳng thềm đá khớp với groundY
        const aY = groundY - aH * 0.35 - paraY3;

        // Đổ bóng sâu dưới bệ đá
        ctx.save();
        ctx.fillStyle = 'rgba(0,0,0,0.85)';
        ctx.filter = 'blur(20px)';
        ctx.beginPath();
        ctx.ellipse(centerX - paraX3, groundY + aH * 0.45, aW * 0.45, 24, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Vẽ Thần Đài
        ctx.drawImage(aImg, aX, aY, aW, aH);

        // Hào quang Bát Quái phát quang theo hệ phái
        const runeColor = SECT_COLORS[currentSect].glow;
        const runePulse = 0.28 + Math.sin(now * 0.003) * 0.12 + (flashIntensity * 0.4);
        ctx.save();
        ctx.globalAlpha = runePulse;
        ctx.filter = 'blur(16px)';
        ctx.fillStyle = runeColor;
        ctx.beginPath();
        ctx.ellipse(centerX - paraX3, groundY - 6 - paraY3, aW * 0.28, 20, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      // -------------------------------------------------------------
      // LAYER 4: TIÊU ĐIỂM CHÍNH · THỢ RÈN TIÊN NHÂN & ĐE THẦN HOÀNG KIM
      // Chuẩn 100% tỉ lệ game gốc: Người đứng trái, Đe đứng phải, đứng cùng mặt phẳng!
      // -------------------------------------------------------------
      const paraX4 = currentMouseX * 52;
      const paraY4 = currentMouseY * 16;
      const stageFootY = groundY - paraY4;
      const heroFootX = centerX - 42 - paraX4;
      const anvilFootX = centerX + 40 - paraX4;

      // 4A. Bóng đổ mềm dưới chân người và đe
      ctx.save();
      ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
      ctx.filter = 'blur(7px)';
      ctx.beginPath();
      ctx.ellipse(heroFootX, stageFootY + 2, 34, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(anvilFootX, stageFootY + 4, 38, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // 4B. Vẽ Đe Thần Hoàng Kim (demo_anvil.webp)
      const anvilAsset = ASSETS.anvil;
      if (anvilAsset.loaded) {
        const anvImg = anvilAsset.img;
        const anvH = 96; // Chiều cao ngang hông nhân vật
        const anvW = (anvImg.width / anvImg.height) * anvH;
        ctx.drawImage(anvImg, anvilFootX - anvW * 0.5, stageFootY - anvH + 8, anvW, anvH);
      }

      // 4C. Vẽ Nhân Vật Tiên Nhân (Sprite Sheet 6 Khung Hình hero_spritesheet_strip.webp)
      const sheetAsset = ASSETS.heroSheet;
      if (sheetAsset.loaded) {
        const sheet = sheetAsset.img;
        const FRAME_W = 360;
        const FRAME_H = 480;

        const renderScale = 0.44;
        const dw = FRAME_W * renderScale;
        const dh = FRAME_H * renderScale;
        const baseLineY = 430 * renderScale; // Gốc tọa độ chân tiếp đất

        const sx = frameIdx * FRAME_W;
        const sy = 0;

        const spriteLeft = heroFootX - dw * 0.5;
        const spriteTop = stageFootY - baseLineY;

        ctx.save();
        if (frameIdx === 3) {
          ctx.shadowColor = SECT_COLORS[currentSect].light;
          ctx.shadowBlur = 24;
        }
        ctx.drawImage(sheet, sx, sy, FRAME_W, FRAME_H, spriteLeft, spriteTop, dw, dh);
        ctx.restore();

        // Danh hiệu trên đầu nhân vật
        ctx.save();
        ctx.font = '700 12px "Segoe UI", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const labelText = `THỢ RÈN CHÍNH · [${currentSect.toUpperCase()}]`;
        const tw = ctx.measureText(labelText).width;
        const tagY = spriteTop - 14;

        ctx.fillStyle = 'rgba(6, 10, 20, 0.85)';
        ctx.strokeStyle = SECT_COLORS[currentSect].glow;
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.roundRect(heroFootX - tw * 0.5 - 8, tagY - 11, tw + 16, 22, 4);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#F8FAFC';
        ctx.fillText(labelText, heroFootX, tagY);
        ctx.restore();
      }

      // -------------------------------------------------------------
      // LAYER 5: DYNAMIC SPARKS & FLASH LIGHTING
      // -------------------------------------------------------------
      for (let i = sparks.length - 1; i >= 0; i--) {
        const sp = sparks[i];
        sp.x += sp.vx;
        sp.y += sp.vy;
        sp.vy += 0.32;
        sp.life -= sp.decay;

        if (sp.life <= 0) {
          sparks.splice(i, 1);
          continue;
        }

        ctx.save();
        ctx.globalAlpha = Math.max(0, sp.life);
        ctx.fillStyle = sp.color;
        ctx.shadowColor = sp.color;
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(sp.x, sp.y, sp.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      // Flash illumination upon strike
      if (flashIntensity > 0) {
        ctx.save();
        ctx.globalAlpha = flashIntensity * 0.35;
        ctx.fillStyle = SECT_COLORS[currentSect].light;
        ctx.filter = 'blur(45px)';
        ctx.beginPath();
        ctx.arc(anvilFootX, stageFootY - 45, 140, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
"""

start_pos = code.find(target_start)
end_pos = code.find(target_end)

assert start_pos != -1, "target_start not found"
assert end_pos != -1, "target_end not found"

new_code = code[:start_pos] + new_render + "\n" + code[end_pos:]

with open('webgame/demo_parallax_forge.html', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Demo parallax layout successfully rebalanced!")

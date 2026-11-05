import re

path = 'frontend/src/components/CommunityPanoramicForgeCanvas.tsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update PeerSlotConfig and DEFAULT_PEER_SLOTS
old_peer_slots_def = """// Tier 3: Frontline Peer Blacksmith Slots (Flanking Main Hero)
interface PeerSlotConfig {
  id: number;
  xNorm: number;
  yOffset: number;
  scale: number;
  facing: 1 | -1;
  speed: number;
  phase: number;
  isReal: boolean;
  name: string;
  stance: StanceKey;
}

const DEFAULT_PEER_SLOTS: PeerSlotConfig[] = [
  { id: 0, xNorm: 0.12, yOffset: 6, scale: 0.34, facing: 1, speed: 1.15, phase: 0.1, isReal: false, name: '', stance: 'Q' },
  { id: 1, xNorm: 0.24, yOffset: 2, scale: 0.35, facing: 1, speed: 0.95, phase: 0.35, isReal: false, name: '', stance: 'W' },
  { id: 2, xNorm: 0.36, yOffset: 0, scale: 0.36, facing: 1, speed: 1.05, phase: 0.7, isReal: false, name: '', stance: 'Q' },
  { id: 3, xNorm: 0.64, yOffset: 0, scale: 0.36, facing: -1, speed: 1.0, phase: 0.55, isReal: false, name: '', stance: 'R' },
  { id: 4, xNorm: 0.76, yOffset: 2, scale: 0.35, facing: -1, speed: 1.2, phase: 0.85, isReal: false, name: '', stance: 'E' },
  { id: 5, xNorm: 0.88, yOffset: 6, scale: 0.34, facing: -1, speed: 1.1, phase: 0.65, isReal: false, name: '', stance: 'W' },
];"""

new_peer_slots_def = """// 24 Multi-Tier Co-Op Forge Stations (Vạn Cổ Đúc Thần Đài)
interface PeerSlotConfig {
  id: number;
  xNorm: number; // Normalized to amphitheater width
  yNorm: number; // Normalized to amphitheater height
  scale: number;
  facing: 1 | -1;
  speed: number;
  phase: number;
  isReal: boolean;
  name: string;
  stance: StanceKey;
  tier: 1 | 2 | 3;
}

const DEFAULT_PEER_SLOTS: PeerSlotConfig[] = [
  // Tier 1: Foreground Stone Promenade (8 stations, closest to camera)
  { id: 0, xNorm: 255 / 1376, yNorm: 535 / 768, scale: 0.35, facing: 1, speed: 1.15, phase: 0.10, isReal: false, name: '', stance: 'Q', tier: 1 },
  { id: 1, xNorm: 350 / 1376, yNorm: 550 / 768, scale: 0.36, facing: 1, speed: 0.95, phase: 0.35, isReal: false, name: '', stance: 'W', tier: 1 },
  { id: 2, xNorm: 455 / 1376, yNorm: 560 / 768, scale: 0.38, facing: 1, speed: 1.05, phase: 0.70, isReal: false, name: '', stance: 'E', tier: 1 },
  { id: 3, xNorm: 565 / 1376, yNorm: 545 / 768, scale: 0.38, facing: 1, speed: 1.20, phase: 0.45, isReal: false, name: '', stance: 'R', tier: 1 },
  { id: 4, xNorm: 810 / 1376, yNorm: 545 / 768, scale: 0.38, facing: -1, speed: 1.00, phase: 0.55, isReal: false, name: '', stance: 'R', tier: 1 },
  { id: 5, xNorm: 920 / 1376, yNorm: 560 / 768, scale: 0.38, facing: -1, speed: 1.10, phase: 0.85, isReal: false, name: '', stance: 'E', tier: 1 },
  { id: 6, xNorm: 1025 / 1376, yNorm: 550 / 768, scale: 0.36, facing: -1, speed: 1.15, phase: 0.25, isReal: false, name: '', stance: 'W', tier: 1 },
  { id: 7, xNorm: 1120 / 1376, yNorm: 535 / 768, scale: 0.35, facing: -1, speed: 1.05, phase: 0.65, isReal: false, name: '', stance: 'Q', tier: 1 },

  // Tier 2: Midground Stepped Terraces & Colosseum Wings (12 stations)
  // Left Wing (6)
  { id: 8,  xNorm: 140 / 1376, yNorm: 475 / 768, scale: 0.26, facing: 1, speed: 1.00, phase: 0.15, isReal: false, name: '', stance: 'Q', tier: 2 },
  { id: 9,  xNorm: 225 / 1376, yNorm: 450 / 768, scale: 0.25, facing: 1, speed: 1.10, phase: 0.40, isReal: false, name: '', stance: 'W', tier: 2 },
  { id: 10, xNorm: 305 / 1376, yNorm: 425 / 768, scale: 0.24, facing: 1, speed: 0.90, phase: 0.60, isReal: false, name: '', stance: 'E', tier: 2 },
  { id: 11, xNorm: 245 / 1376, yNorm: 505 / 768, scale: 0.27, facing: 1, speed: 1.15, phase: 0.80, isReal: false, name: '', stance: 'R', tier: 2 },
  { id: 12, xNorm: 345 / 1376, yNorm: 490 / 768, scale: 0.26, facing: 1, speed: 1.05, phase: 0.30, isReal: false, name: '', stance: 'Q', tier: 2 },
  { id: 13, xNorm: 425 / 1376, yNorm: 465 / 768, scale: 0.25, facing: 1, speed: 1.25, phase: 0.50, isReal: false, name: '', stance: 'W', tier: 2 },
  // Right Wing (6)
  { id: 14, xNorm: 950 / 1376, yNorm: 465 / 768, scale: 0.25, facing: -1, speed: 1.20, phase: 0.20, isReal: false, name: '', stance: 'W', tier: 2 },
  { id: 15, xNorm: 1030 / 1376, yNorm: 490 / 768, scale: 0.26, facing: -1, speed: 1.00, phase: 0.75, isReal: false, name: '', stance: 'Q', tier: 2 },
  { id: 16, xNorm: 1130 / 1376, yNorm: 505 / 768, scale: 0.27, facing: -1, speed: 1.10, phase: 0.35, isReal: false, name: '', stance: 'R', tier: 2 },
  { id: 17, xNorm: 1070 / 1376, yNorm: 425 / 768, scale: 0.24, facing: -1, speed: 0.95, phase: 0.55, isReal: false, name: '', stance: 'E', tier: 2 },
  { id: 18, xNorm: 1150 / 1376, yNorm: 450 / 768, scale: 0.25, facing: -1, speed: 1.15, phase: 0.90, isReal: false, name: '', stance: 'W', tier: 2 },
  { id: 19, xNorm: 1235 / 1376, yNorm: 475 / 768, scale: 0.26, facing: -1, speed: 1.05, phase: 0.10, isReal: false, name: '', stance: 'Q', tier: 2 },

  // Tier 3: High Mountain Spire Platforms (4 stations in misty heights)
  { id: 20, xNorm: 110 / 1376, yNorm: 365 / 768, scale: 0.18, facing: 1, speed: 1.05, phase: 0.25, isReal: false, name: '', stance: 'Q', tier: 3 },
  { id: 21, xNorm: 205 / 1376, yNorm: 350 / 768, scale: 0.17, facing: 1, speed: 1.10, phase: 0.65, isReal: false, name: '', stance: 'W', tier: 3 },
  { id: 22, xNorm: 1170 / 1376, yNorm: 350 / 768, scale: 0.17, facing: -1, speed: 1.00, phase: 0.45, isReal: false, name: '', stance: 'W', tier: 3 },
  { id: 23, xNorm: 1265 / 1376, yNorm: 365 / 768, scale: 0.18, facing: -1, speed: 1.15, phase: 0.85, isReal: false, name: '', stance: 'Q', tier: 3 },
];"""

assert old_peer_slots_def in code, "old_peer_slots_def not found"
code = code.replace(old_peer_slots_def, new_peer_slots_def, 1)

# 2. Update assets dictionary
old_assets_def = """      badgeHoangKim: { src: `${cleanBase}assets/art/ui/badge_hoang_kim.webp`, img: new Image(), loaded: false },
      badgeBaoKich: { src: `${cleanBase}assets/art/ui/badge_bao_kich.webp`, img: new Image(), loaded: false },
    };"""

new_assets_def = """      badgeHoangKim: { src: `${cleanBase}assets/art/ui/badge_hoang_kim.webp`, img: new Image(), loaded: false },
      badgeBaoKich: { src: `${cleanBase}assets/art/ui/badge_bao_kich.webp`, img: new Image(), loaded: false },
      amphitheater: { src: `${cleanBase}assets/art/grand_amphitheater_terraces.webp`, img: new Image(), loaded: false },
      anvilFire: { src: `${cleanBase}assets/art/props/prop_anvil_fire_bagua.webp`, img: new Image(), loaded: false },
      anvilLightning: { src: `${cleanBase}assets/art/props/prop_anvil_lightning_dragon.webp`, img: new Image(), loaded: false },
      anvilMountain: { src: `${cleanBase}assets/art/props/prop_anvil_mountain_stone.webp`, img: new Image(), loaded: false },
      brazier: { src: `${cleanBase}assets/art/props/prop_furnace_bronze_brazier.webp`, img: new Image(), loaded: false },
      daoistMarker: { src: `${cleanBase}assets/art/props/prop_altar_daoist_marker.webp`, img: new Image(), loaded: false },
    };"""

assert old_assets_def in code, "old_assets_def not found"
code = code.replace(old_assets_def, new_assets_def, 1)

# 3. Update triggerPeerWaveClosureRef and triggerRemotePeerStrikeClosureRef
old_peer_wave = """    triggerPeerWaveClosureRef.current = () => {
      peerSlots.forEach((slot, idx) => {
        if (!slot.isReal) return; // Only real connected peers
        peerStrikeTimers[idx] = 0;
        const px = slot.xNorm * viewW;
        const py = viewH * 0.825 + slot.yOffset;
        const sect = STANCE_TO_SECT[slot.stance] || 'thunder';
        spawnLightningBolt(px, py - 8, SECT_COLORS[sect].glow, 0.9);
      });
      screenShake = 10;
      flashIntensity = 0.9;
    };"""

new_peer_wave = """    triggerPeerWaveClosureRef.current = () => {
      const isPortrait = viewW < viewH;
      const amphiW = Math.max(viewW * 1.05, viewH * (1376 / 768) * (isPortrait ? 1.3 : 1.05));
      const amphiH = amphiW * (768 / 1376);
      const amphiX = (viewW - amphiW) * 0.5 - currentMouseX * 24;
      const amphiY = isPortrait ? viewH * 0.32 - currentMouseY * 8 : viewH - amphiH + 8 - currentMouseY * 10;

      peerSlots.forEach((slot, idx) => {
        if (!slot.isReal) return; // Only real connected peers
        peerStrikeTimers[idx] = 0;
        const px = amphiX + slot.xNorm * amphiW;
        const py = amphiY + slot.yNorm * amphiH;
        const sect = STANCE_TO_SECT[slot.stance] || 'thunder';
        spawnLightningBolt(px, py - 8, SECT_COLORS[sect].glow, 0.9);
      });
      screenShake = 10;
      flashIntensity = 0.9;
    };"""

assert old_peer_wave in code, "old_peer_wave not found"
code = code.replace(old_peer_wave, new_peer_wave, 1)

old_remote_strike = """    triggerRemotePeerStrikeClosureRef.current = (payload: RemotePeerStrikePayload) => {
      const slotIdx = payload.slotIndex;
      if (slotIdx >= 0 && slotIdx < peerSlots.length) {
        peerStrikeTimers[slotIdx] = 0;
        const slot = peerSlots[slotIdx];
        const px = slot.xNorm * viewW;
        const py = viewH * 0.825 + slot.yOffset;
        const sect = STANCE_TO_SECT[payload.stance] || 'thunder';
        const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

        spawnLightningBolt(px + (slot.facing === 1 ? 14 : -14), py - 8, sc.glow, 0.95);

        for (let i = 0; i < 8; i++) {
          const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 1.6;
          const spd = 80 + Math.random() * 160;
          spawnParticle(
            px + (slot.facing === 1 ? 14 : -14),
            py - 8,
            Math.cos(ang) * spd,
            Math.sin(ang) * spd,
            1.8,
            sc.spark,
            0.4,
            false
          );
        }
      }
    };"""

new_remote_strike = """    triggerRemotePeerStrikeClosureRef.current = (payload: RemotePeerStrikePayload) => {
      const slotIdx = payload.slotIndex;
      if (slotIdx >= 0 && slotIdx < peerSlots.length) {
        peerStrikeTimers[slotIdx] = 0;
        const slot = peerSlots[slotIdx];
        const isPortrait = viewW < viewH;
        const amphiW = Math.max(viewW * 1.05, viewH * (1376 / 768) * (isPortrait ? 1.3 : 1.05));
        const amphiH = amphiW * (768 / 1376);
        const amphiX = (viewW - amphiW) * 0.5 - currentMouseX * 24;
        const amphiY = isPortrait ? viewH * 0.32 - currentMouseY * 8 : viewH - amphiH + 8 - currentMouseY * 10;
        const px = amphiX + slot.xNorm * amphiW;
        const py = amphiY + slot.yNorm * amphiH;
        const sect = STANCE_TO_SECT[payload.stance] || 'thunder';
        const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;

        spawnLightningBolt(px + (slot.facing === 1 ? 14 : -14), py - 8, sc.glow, 0.95);

        for (let i = 0; i < 8; i++) {
          const ang = Math.PI * 1.5 + (Math.random() - 0.5) * 1.6;
          const spd = 80 + Math.random() * 160;
          spawnParticle(
            px + (slot.facing === 1 ? 14 : -14),
            py - 8,
            Math.cos(ang) * spd,
            Math.sin(ang) * spd,
            1.8,
            sc.spark,
            0.4,
            false
          );
        }
      }
    };"""

assert old_remote_strike in code, "old_remote_strike not found"
code = code.replace(old_remote_strike, new_remote_strike, 1)

# 4. Replace Layers 5, 6, 7, 8, 9, 10 with the grand amphitheater rendering
old_layers_start = "        // ---------------------------------------------------------------------\n        // LAYER 5: BASALT HORIZON RIDGE (64% HEIGHT)"
old_layers_end = "        // ---------------------------------------------------------------------\n        // LAYER 11: MAIN HERO (BALANCED 0.38 SCALE, EQUAL PROMINENCE)"

idx1 = code.find(old_layers_start)
idx2 = code.find(old_layers_end)
assert idx1 != -1, "old_layers_start not found"
assert idx2 != -1, "old_layers_end not found"

new_layers_replacement = """        // ---------------------------------------------------------------------
        // LAYER 5: 2.5D GRAND BASALT AMPHITHEATER (VẠN CỔ ĐÚC THẦN ĐÀI)
        // ---------------------------------------------------------------------
        const isPortrait = viewW < viewH;
        const amphiW = Math.max(viewW * 1.05, viewH * (1376 / 768) * (isPortrait ? 1.3 : 1.05));
        const amphiH = amphiW * (768 / 1376);
        const amphiX = (viewW - amphiW) * 0.5 - currentMouseX * 24;
        const amphiY = isPortrait ? viewH * 0.32 - currentMouseY * 8 : viewH - amphiH + 8 - currentMouseY * 10;

        if (assets.amphitheater.loaded) {
          const amImg = assets.amphitheater.img;
          ctx.save();
          ctx.drawImage(amImg, amphiX, amphiY, amphiW, amphiH);

          // Ethereal Qi mist & Magma fissure atmospheric pulse
          const fissurePulse = 0.65 + Math.sin(now * 0.003) * 0.35 + flashIntensity * 0.4;
          ctx.globalCompositeOperation = 'screen';
          ctx.globalAlpha = Math.min(0.38, fissurePulse * 0.30);
          const magmaGrad = ctx.createRadialGradient(
            viewW * 0.5 - currentMouseX * 24, amphiY + amphiH * 0.72, 40,
            viewW * 0.5 - currentMouseX * 24, amphiY + amphiH * 0.72, viewW * 0.55
          );
          magmaGrad.addColorStop(0, 'rgba(255, 120, 20, 0.40)');
          magmaGrad.addColorStop(0.5, 'rgba(0, 240, 255, 0.18)');
          magmaGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
          ctx.fillStyle = magmaGrad;
          ctx.fillRect(0, amphiY + amphiH * 0.40, viewW, amphiH * 0.60);
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 6: DECORATIVE BRONZE BRAZIERS (CENTRAL STAIR FLANKS)
        // ---------------------------------------------------------------------
        if (assets.brazier.loaded) {
          const bImg = assets.brazier.img;
          const brazierStations = [
            { xNorm: 525 / 1376, yNorm: 515 / 768, scale: 0.32 },
            { xNorm: 850 / 1376, yNorm: 515 / 768, scale: 0.32 },
          ];
          brazierStations.forEach((bz) => {
            const bx = amphiX + bz.xNorm * amphiW;
            const by = amphiY + bz.yNorm * amphiH;
            const bw = 54 * bz.scale;
            const bh = bw * (bImg.height / bImg.width);

            // Brazier shadow
            ctx.save();
            ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
            ctx.filter = 'blur(6px)';
            ctx.beginPath();
            ctx.ellipse(bx, by + 2, bw * 0.45, 6, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Brazier sprite
            ctx.save();
            ctx.drawImage(bImg, bx - bw * 0.5, by - bh, bw, bh);

            // Flickering eternal forge flame glow
            const flamePulse = 0.5 + Math.sin(now * 0.007 + bx) * 0.3;
            ctx.globalCompositeOperation = 'screen';
            ctx.globalAlpha = flamePulse * 0.55;
            ctx.fillStyle = '#FF7700';
            ctx.filter = 'blur(8px)';
            ctx.beginPath();
            ctx.arc(bx, by - bh * 0.72, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
          });
        }

        // ---------------------------------------------------------------------
        // HELPER: DRAW PEER FORGE STATION (PEDESTAL + ANVIL + BLACKSMITH + PLAQUE)
        // ---------------------------------------------------------------------
        const activeSect = STANCE_TO_SECT[activeStanceRef.current] || 'thunder';
        const activeSectColor = SECT_COLORS[activeSect] || SECT_COLORS.thunder;

        const drawPeerStation = (slot: PeerSlotConfig) => {
          if (!slot.isReal) return; // Only render when real human peer is present (no bots)
          const px = amphiX + slot.xNorm * amphiW;
          const py = amphiY + slot.yNorm * amphiH;

          // 1. Pedestal
          if (assets.pedestal.loaded) {
            const pedImg = assets.pedestal.img;
            const pedW = 145 * (slot.scale / 0.35);
            const pedH = pedW * (pedImg.height / pedImg.width);

            ctx.save();
            ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
            ctx.filter = 'blur(8px)';
            ctx.beginPath();
            ctx.ellipse(px, py + pedH * 0.32, pedW * 0.45, 10, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            ctx.save();
            ctx.drawImage(pedImg, px - pedW * 0.5, py - pedH * 0.28, pedW, pedH);

            // Sect Rune Glow
            const sect = STANCE_TO_SECT[slot.stance] || 'thunder';
            const sc = SECT_COLORS[sect] || SECT_COLORS.thunder;
            ctx.globalAlpha = 0.45 + Math.sin(now * 0.004 + slot.id) * 0.15;
            ctx.filter = 'blur(10px)';
            ctx.fillStyle = sc.glow;
            ctx.beginPath();
            ctx.ellipse(px, py - 3, pedW * 0.3, 7, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
          }

          // 2. Peer Blacksmith Sprite (Animated 6-frame)
          if (assets.peerSheet.loaded) {
            const sheetColor = assets.peerSheet.img;
            const PEER_FW = 458;
            const PEER_FH = 384;
            const cycleTime = 1.05 / slot.speed;
            const cycleSec = (now * 0.001 + slot.phase * 10) % cycleTime;
            const progress = cycleSec / cycleTime;

            let pFrame = 0;
            if (progress < 0.20) pFrame = 0;
            else if (progress < 0.42) pFrame = 1;
            else if (progress < 0.60) pFrame = 2;
            else if (progress < 0.78) pFrame = 3;
            else if (progress < 0.90) pFrame = 4;
            else pFrame = 5;

            const pw = PEER_FW * slot.scale;
            const ph = PEER_FH * slot.scale;

            ctx.save();
            ctx.translate(px, py);
            if (slot.facing === -1) {
              ctx.scale(-1, 1);
            }
            const sx = pFrame * PEER_FW;
            ctx.drawImage(sheetColor, sx, 0, PEER_FW, PEER_FH, -pw * 0.42, -ph + 12, pw, ph);
            ctx.restore();
          }

          // 3. Custom Sect Anvil Prop
          const anvilAsset =
            slot.stance === 'W'
              ? assets.anvilFire
              : slot.stance === 'E'
              ? assets.anvilMountain
              : assets.anvilLightning;

          if (anvilAsset && anvilAsset.loaded) {
            const aImg = anvilAsset.img;
            const anW = 42 * (slot.scale / 0.35);
            const anH = anW * (aImg.height / aImg.width);
            const anX = px + (slot.facing === 1 ? 8 : -8) - anW * 0.5;
            const anY = py - anH + 4;

            ctx.save();
            ctx.drawImage(aImg, anX, anY, anW, anH);
            ctx.restore();
          }

          // 4. Tiên Hiệp Plaque Nameplate (Charm / Caveat Calligraphy)
          if (slot.name && slot.name.trim()) {
            const ph = 384 * slot.scale;
            const nameY = py - ph + 4;
            drawXianxiaPlaque(ctx, px, nameY, slot.name, slot.stance, false, true);
          }
        };

        // ---------------------------------------------------------------------
        // LAYER 7: TIER 3 HIGH MOUNTAIN SPIRE STATIONS (BACKGROUND PEERS)
        // ---------------------------------------------------------------------
        peerSlots.filter((s) => s.tier === 3).forEach(drawPeerStation);

        // ---------------------------------------------------------------------
        // LAYER 8: TIER 2 MIDGROUND TERRACE STATIONS (COLOSSEUM WINGS)
        // ---------------------------------------------------------------------
        peerSlots.filter((s) => s.tier === 2).forEach(drawPeerStation);

        // ---------------------------------------------------------------------
        // LAYER 9: CENTRAL ALTAR PLATFORM (MAIN HERO DAIS)
        // ---------------------------------------------------------------------
        const daisTopY = amphiY + amphiH * (375 / 768);
        const aW = isPortrait ? Math.min(270, viewW * 0.58) : Math.min(300, viewW * 0.22);
        const aH = aW * (assets.mainAltar.img.height / assets.mainAltar.img.width);
        const aX = centerX - aW * 0.5 - currentMouseX * 24;
        const aY = daisTopY - aH * 0.65;
        const groundY = aY + aH * 0.58;

        if (assets.mainAltar.loaded) {
          const aImg = assets.mainAltar.img;

          // Shadow
          ctx.save();
          ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
          ctx.filter = 'blur(16px)';
          ctx.beginPath();
          ctx.ellipse(centerX - currentMouseX * 24, groundY + aH * 0.15, aW * 0.45, 14, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();

          // Altar Image
          ctx.save();
          ctx.drawImage(aImg, aX, aY, aW, aH);

          // Central Rune Pool
          const runeColor = activeSectColor.glow;
          const runePulse = 0.35 + Math.sin(now * 0.003) * 0.15 + flashIntensity * 0.45;
          ctx.globalAlpha = runePulse;
          ctx.filter = 'blur(12px)';
          ctx.fillStyle = runeColor;
          ctx.beginPath();
          ctx.ellipse(centerX - currentMouseX * 24, groundY - 2, aW * 0.26, 10, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }

        // ---------------------------------------------------------------------
        // LAYER 10: TIER 1 FOREGROUND PROMENADE STATIONS (FLANKING HERO)
        // ---------------------------------------------------------------------
        peerSlots.filter((s) => s.tier === 1).forEach(drawPeerStation);

"""

code = code[:idx1] + new_layers_replacement + code[idx2:]

# Also update Hero Character mouse parallax from currentMouseX * 64/56 to currentMouseX * 24
# so hero stays strictly centered on the Bagua altar!
old_hero_parallax = "const heroFootX = centerX - 14 - currentMouseX * 64;"
new_hero_parallax = "const heroFootX = centerX - 14 - currentMouseX * 24;"
code = code.replace(old_hero_parallax, new_hero_parallax, 1)

old_hero_plaque_parallax = "drawXianxiaPlaque(ctx, centerX - currentMouseX * 64, tagY, labelText, activeStanceRef.current, true, true);"
new_hero_plaque_parallax = "drawXianxiaPlaque(ctx, centerX - currentMouseX * 24, tagY, labelText, activeStanceRef.current, true, true);"
code = code.replace(old_hero_plaque_parallax, new_hero_plaque_parallax, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated CommunityPanoramicForgeCanvas.tsx!")

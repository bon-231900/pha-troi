// ============================================================================
// TOÀN DÂN PHÁ TRỜI: THE CELESTIAL FORGE
// AUDIO ENGINE (WEB AUDIO API SYNTHESIZER) - PHASE 2 ENHANCED
// ============================================================================

class SoundManager {
    constructor() {
        this.ctx = null;
        this.muted = false;
        this.volume = 0.45;
        this.initialized = false;
        this.ambientChorusRunning = false;
        this.ambientGain = null;
    }

    init() {
        if (this.initialized) return;
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
            this.initialized = true;
            this.startAmbientChorus();
        } catch (e) {
            console.warn("Web Audio API not supported", e);
        }
    }

    ensureContext() {
        if (!this.initialized) this.init();
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggleMute() {
        this.muted = !this.muted;
        if (this.ambientGain) {
            this.ambientGain.gain.setValueAtTime(this.muted ? 0 : this.volume * 0.15, this.ctx.currentTime);
        }
        return this.muted;
    }

    // Dynamic Forge Chorus: Âm hưởng đại công trường rì rầm xa xăm
    startAmbientChorus() {
        if (!this.ctx || this.ambientChorusRunning) return;
        this.ambientChorusRunning = true;

        // Tiếng lò lửa & hơi nhiệt rì rầm (Brown Noise filtered)
        const bufferSize = this.ctx.sampleRate * 2;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufferSize; i++) {
            const white = Math.random() * 2 - 1;
            output[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = output[i];
            output[i] *= 3.5;
        }

        const whiteNoise = this.ctx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 160;

        this.ambientGain = this.ctx.createGain();
        this.ambientGain.gain.setValueAtTime(this.muted ? 0 : this.volume * 0.12, this.ctx.currentTime);

        whiteNoise.connect(filter);
        filter.connect(this.ambientGain);
        this.ambientGain.connect(this.ctx.destination);
        whiteNoise.start();

        // Tiếng gõ đe lách cách xa xăm ngẫu nhiên của thợ rèn khác
        const playDistantClink = () => {
            if (!this.muted && this.ctx && this.ctx.state === 'running') {
                const now = this.ctx.currentTime;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(1400 + Math.random() * 600, now);
                osc.frequency.exponentialRampToValueAtTime(500, now + 0.08);

                const pan = this.ctx.createStereoPanner ? this.ctx.createStereoPanner() : null;
                if (pan) pan.pan.setValueAtTime(Math.random() * 1.6 - 0.8, now);

                gain.gain.setValueAtTime(this.volume * 0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

                if (pan) {
                    osc.connect(gain);
                    gain.connect(pan);
                    pan.connect(this.ctx.destination);
                } else {
                    osc.connect(gain);
                    gain.connect(this.ctx.destination);
                }
                osc.start(now);
                osc.stop(now + 0.08);
            }
            setTimeout(playDistantClink, 800 + Math.random() * 1400);
        };
        playDistantClink();
    }

    // Tiếng búa nện vào đe thần theo phân vùng nhịp
    playAnvilStrike(zone = 'warm', isCrit = false) {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;

        if (zone === 'golden') {
            // ĐIỂM HOÀNG KIM: Tiếng "KENG!" đanh thép sắc bén
            const oscRing = this.ctx.createOscillator();
            const gainRing = this.ctx.createGain();
            oscRing.type = 'sine';
            oscRing.frequency.setValueAtTime(1280, now);
            oscRing.frequency.exponentialRampToValueAtTime(420, now + 0.18);
            gainRing.gain.setValueAtTime(this.volume * (isCrit ? 0.85 : 0.65), now);
            gainRing.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
            oscRing.connect(gainRing);
            gainRing.connect(this.ctx.destination);
            oscRing.start(now);
            oscRing.stop(now + 0.18);

            // Bass trầm đe đá
            const oscBass = this.ctx.createOscillator();
            const gainBass = this.ctx.createGain();
            oscBass.type = 'triangle';
            oscBass.frequency.setValueAtTime(180, now);
            oscBass.frequency.exponentialRampToValueAtTime(32, now + 0.22);
            gainBass.gain.setValueAtTime(this.volume * 0.9, now);
            gainBass.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
            oscBass.connect(gainBass);
            gainBass.connect(this.ctx.destination);
            oscBass.start(now);
            oscBass.stop(now + 0.22);

            if (isCrit) {
                // Sóng chấn động Bạo Kích
                const oscCrit = this.ctx.createOscillator();
                const gainCrit = this.ctx.createGain();
                oscCrit.type = 'sawtooth';
                oscCrit.frequency.setValueAtTime(540, now);
                oscCrit.frequency.exponentialRampToValueAtTime(90, now + 0.35);
                const filter = this.ctx.createBiquadFilter();
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(1400, now);
                gainCrit.gain.setValueAtTime(this.volume * 0.55, now);
                gainCrit.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
                oscCrit.connect(filter);
                filter.connect(gainCrit);
                gainCrit.connect(this.ctx.destination);
                oscCrit.start(now);
                oscCrit.stop(now + 0.35);
            }
        } else if (zone === 'warm') {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(820, now);
            osc.frequency.exponentialRampToValueAtTime(260, now + 0.12);
            gain.gain.setValueAtTime(this.volume * 0.45, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.12);

            const oscBass = this.ctx.createOscillator();
            const gainBass = this.ctx.createGain();
            oscBass.type = 'triangle';
            oscBass.frequency.setValueAtTime(130, now);
            oscBass.frequency.exponentialRampToValueAtTime(40, now + 0.12);
            gainBass.gain.setValueAtTime(this.volume * 0.5, now);
            gainBass.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
            oscBass.connect(gainBass);
            gainBass.connect(this.ctx.destination);
            oscBass.start(now);
            oscBass.stop(now + 0.12);
        } else {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(320, now);
            osc.frequency.exponentialRampToValueAtTime(80, now + 0.1);
            gain.gain.setValueAtTime(this.volume * 0.35, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.1);
        }
    }

    // Kích hoạt trạng thái Cuồng Nhiệt Overdrive Fever (10s)
    playOverdriveStart() {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(110, now);
        osc.frequency.exponentialRampToValueAtTime(440, now + 0.4);

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(800, now);

        gain.gain.setValueAtTime(this.volume * 0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.5);
    }

    // Tiếng đập siêu tốc trong Overdrive
    playOverdriveStrike() {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(950 + Math.random() * 200, now);
        osc.frequency.exponentialRampToValueAtTime(250, now + 0.08);

        gain.gain.setValueAtTime(this.volume * 0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.08);
    }

    // Tiếng nâng cấp thành công
    playUpgrade() {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + idx * 0.04);

            gain.gain.setValueAtTime(0, now + idx * 0.04);
            gain.gain.linearRampToValueAtTime(this.volume * 0.35, now + idx * 0.04 + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.04 + 0.22);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + idx * 0.04);
            osc.stop(now + idx * 0.04 + 0.22);
        });
    }

    // Tiếng Chuyển Sinh / Tôi Luyện Thần Hồn (Rebirth Gong)
    playRebirthGong() {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(98, now); // G2
        osc.frequency.exponentialRampToValueAtTime(45, now + 2.5);

        gain.gain.setValueAtTime(this.volume * 0.9, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 2.5);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 2.5);

        // Chuông ngân thần bí
        const oscBell = this.ctx.createOscillator();
        const gainBell = this.ctx.createGain();
        oscBell.type = 'triangle';
        oscBell.frequency.setValueAtTime(587.33, now); // D5
        oscBell.frequency.exponentialRampToValueAtTime(293.66, now + 1.8);
        gainBell.gain.setValueAtTime(this.volume * 0.5, now);
        gainBell.gain.exponentialRampToValueAtTime(0.001, now + 1.8);
        oscBell.connect(gainBell);
        gainBell.connect(this.ctx.destination);
        oscBell.start(now);
        oscBell.stop(now + 1.8);
    }

    // Mái Vòm Thiên Cấm bị phá vỡ (Victory Shatter)
    playFirmamentShatter() {
        if (this.muted) return;
        this.ensureContext();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        for (let i = 0; i < 6; i++) {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(900 + Math.random() * 700, now + i * 0.05);
            gain.gain.setValueAtTime(this.volume * 0.35, now + i * 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.05 + 0.35);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + i * 0.05);
            osc.stop(now + i * 0.05 + 0.35);
        }

        const chords = [261.63, 329.63, 392.00, 523.25, 659.25, 1046.50];
        chords.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + 0.2 + idx * 0.07);

            gain.gain.setValueAtTime(0, now + 0.2 + idx * 0.07);
            gain.gain.linearRampToValueAtTime(this.volume * 0.45, now + 0.2 + idx * 0.07 + 0.03);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2 + idx * 0.07 + 0.8);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + 0.2 + idx * 0.07);
            osc.stop(now + 0.2 + idx * 0.07 + 0.8);
        });
    }
}

window.soundManager = new SoundManager();

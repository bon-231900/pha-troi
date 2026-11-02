import { JudgmentGrade, StanceKey } from './rules';

class CelestialAudioEngine {
  private ctx: AudioContext | null = null;
  public muted: boolean = false;

  private ensureContext(): AudioContext | null {
    if (this.muted || typeof window === 'undefined') return null;
    try {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (AudioCtx) {
          this.ctx = new AudioCtx();
        }
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume().catch(() => {});
      }
      return this.ctx;
    } catch {
      return null;
    }
  }

  public triggerHaptic(pattern: number | number[]) {
    if (this.muted || typeof navigator === 'undefined' || !navigator.vibrate) return;
    try {
      navigator.vibrate(pattern);
    } catch {
      // Ignore on unsupported devices
    }
  }

  public playAnvilStrike(grade: JudgmentGrade, stance: StanceKey, overdrive: boolean) {
    if (grade === 'PERFECT') {
      this.triggerHaptic(overdrive ? [45, 20, 80, 20, 95] : [35, 25, 65]);
    } else if (grade === 'GREAT') {
      this.triggerHaptic([22]);
    } else {
      this.triggerHaptic([12]);
    }

    const ctx = this.ensureContext();
    if (!ctx) return;

    const now = ctx.currentTime;

    if (grade === 'MISS') {
      // Dull thud + steam hiss
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(110, now);
      osc.frequency.exponentialRampToValueAtTime(38, now + 0.18);

      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.2);
      return;
    }

    // Stance root pitch variation
    const stanceBaseFreq: Record<StanceKey, number> = {
      Q: 587.33, // D5 (Thunder high crisp)
      W: 440.0,  // A4 (Fire warm)
      E: 392.0,  // G4 (Heavy armor breaker)
      R: 523.25, // C5 (Resonance harmonic)
    };

    const root = stanceBaseFreq[stance] * (0.97 + Math.random() * 0.06);

    // 1. Sub-bass impact hammer blow
    const subOsc = ctx.createOscillator();
    const subGain = ctx.createGain();
    subOsc.type = 'sine';
    subOsc.frequency.setValueAtTime(grade === 'PERFECT' ? 155 : 120, now);
    subOsc.frequency.exponentialRampToValueAtTime(32, now + 0.24);
    subGain.gain.setValueAtTime(grade === 'PERFECT' ? 0.45 : 0.28, now);
    subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
    subOsc.connect(subGain);
    subGain.connect(ctx.destination);
    subOsc.start(now);
    subOsc.stop(now + 0.26);

    // 2. Metallic Anvil Ringing Harmonics (inharmonic ratios typical of forged steel)
    const ratios = grade === 'PERFECT' ? [1, 1.51, 2.42, 3.86] : [1, 1.49, 2.38];
    const ringDuration = grade === 'PERFECT' ? (overdrive ? 0.95 : 0.72) : 0.42;

    ratios.forEach((ratio, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = idx % 2 === 0 ? 'triangle' : 'sine';
      osc.frequency.setValueAtTime(root * ratio, now);

      const peakGain = (grade === 'PERFECT' ? 0.22 : 0.14) / (idx + 1);
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(peakGain, now + 0.004);
      gain.gain.exponentialRampToValueAtTime(0.0008, now + ringDuration / (1 + idx * 0.35));

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + ringDuration);
    });

    // 3. Electric Lightning Snap on PERFECT or Overdrive
    if (grade === 'PERFECT' || overdrive) {
      const zapOsc = ctx.createOscillator();
      const zapGain = ctx.createGain();
      zapOsc.type = 'sawtooth';
      zapOsc.frequency.setValueAtTime(root * 4.5, now);
      zapOsc.frequency.exponentialRampToValueAtTime(root * 1.2, now + 0.11);

      zapGain.gain.setValueAtTime(0.12, now);
      zapGain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      zapOsc.connect(zapGain);
      zapGain.connect(ctx.destination);
      zapOsc.start(now);
      zapOsc.stop(now + 0.13);
    }
  }

  public playStanceSwitch(stance: StanceKey) {
    this.triggerHaptic(10);
    const ctx = this.ensureContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const freqs: Record<StanceKey, number> = {
      Q: 660,
      W: 520,
      E: 440,
      R: 740,
    };

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freqs[stance], now);
    osc.frequency.exponentialRampToValueAtTime(freqs[stance] * 1.35, now + 0.065);

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);

    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.075);
  }

  public playGlobalBurstFanfare() {
    this.triggerHaptic([60, 30, 90, 30, 140]);
    const ctx = this.ensureContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const chord = [261.63, 329.63, 392.0, 523.25, 659.25];
    chord.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + i * 0.04);

      gain.gain.setValueAtTime(0.001, now + i * 0.04);
      gain.gain.linearRampToValueAtTime(0.14, now + i * 0.04 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0008, now + 1.1);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now + i * 0.04);
      osc.stop(now + 1.15);
    });
  }
}

export const soundEngine = new CelestialAudioEngine();

/**
 * Web Haptic Feedback Utility for Mobile (Android & iOS WebKit Vibration API)
 */

export const hapticEngine = {
  enabled: true,

  isSupported(): boolean {
    return typeof window !== 'undefined' && 'navigator' in window && typeof navigator.vibrate === 'function';
  },

  /**
   * Crisp, light haptic tick on regular hammer strike (10-15ms)
   */
  playStrike(isCrit = false, isGolden = false): void {
    if (!this.enabled || !this.isSupported()) return;
    try {
      if (isGolden) {
        // Double burst for Golden Hit
        navigator.vibrate([20, 30, 25]);
      } else if (isCrit) {
        // Sharp heavy pulse for Critical Strike
        navigator.vibrate([35, 20, 20]);
      } else {
        // Crisp single pulse
        navigator.vibrate(12);
      }
    } catch {}
  },

  /**
   * Heavy resonance vibration when Overdrive triggers or boss shield breaks
   */
  playHeavyRumble(): void {
    if (!this.enabled || !this.isSupported()) return;
    try {
      navigator.vibrate([40, 40, 50, 30, 60]);
    } catch {}
  },

  /**
   * Quick subtle click for UI button taps
   */
  playButtonTap(): void {
    if (!this.enabled || !this.isSupported()) return;
    try {
      navigator.vibrate(8);
    } catch {}
  },
};

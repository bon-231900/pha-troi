// ============================================================================
// SAFE LOCAL STORAGE UTILITY WITH IN-MEMORY FALLBACK
// Protects against SecurityError in Safari Private Mode, webviews, and blocked cookies
// ============================================================================

class SafeStorage {
  private memStore: Map<string, string> = new Map();
  private isStorageAvailable: boolean = false;

  constructor() {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const testKey = '__storage_test__';
        window.localStorage.setItem(testKey, testKey);
        window.localStorage.removeItem(testKey);
        this.isStorageAvailable = true;
      }
    } catch {
      this.isStorageAvailable = false;
    }
  }

  public getItem(key: string): string | null {
    if (this.isStorageAvailable) {
      try {
        return window.localStorage.getItem(key);
      } catch {
        // Fallback to memory
      }
    }
    return this.memStore.get(key) ?? null;
  }

  public setItem(key: string, value: string): void {
    if (this.isStorageAvailable) {
      try {
        window.localStorage.setItem(key, value);
        return;
      } catch {
        // Fallback to memory if quota exceeded or security error
      }
    }
    this.memStore.set(key, value);
  }

  public removeItem(key: string): void {
    if (this.isStorageAvailable) {
      try {
        window.localStorage.removeItem(key);
      } catch {
        // Fallback to memory
      }
    }
    this.memStore.delete(key);
  }
}

export const safeStorage = new SafeStorage();

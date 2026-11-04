// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM) - GOOGLE SIGN-IN & CLOUD SAVE CLIENT
// ==============================================================================

import { safeStorage } from './storage';

export const GOOGLE_CLIENT_ID = '325984073866-an8facrtq5edm0aetm5ok3qmrf00oq7t.apps.googleusercontent.com';
const API_BASE_URL = 'https://phatroi-api.beanbinh2000.workers.dev/api';

export interface GoogleUserProfile {
  googleId: string;
  email: string;
  name: string;
  avatar: string;
}

export interface GoogleAuthResponse {
  success: boolean;
  isNew?: boolean;
  profile?: GoogleUserProfile;
  saveData?: string;
  lastSyncAt?: number;
  error?: string;
}

interface GoogleTokenResponse {
  access_token?: string;
  error?: string;
  error_description?: string;
}

interface GoogleTokenClient {
  requestAccessToken: (overrideConfig?: { prompt?: string }) => void;
}

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: {
            client_id: string;
            callback: (res: { credential: string }) => void;
            auto_select?: boolean;
            cancel_on_tap_outside?: boolean;
          }) => void;
          prompt: (notification?: (notification: unknown) => void) => void;
          renderButton: (
            parent: HTMLElement,
            options: {
              theme?: 'outline' | 'filled_blue' | 'filled_black';
              size?: 'large' | 'medium' | 'small';
              text?: 'signin_with' | 'signup_with' | 'continue_with';
              shape?: 'rectangular' | 'pill' | 'circle' | 'square';
              logo_alignment?: 'left' | 'center';
              width?: number;
            }
          ) => void;
          disableAutoSelect: () => void;
        };
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: (response: GoogleTokenResponse) => void;
            error_callback?: (err: unknown) => void;
          }) => GoogleTokenClient;
        };
      };
    };
  }
}

class GoogleAuthService {
  private userProfile: GoogleUserProfile | null = null;
  private isInitialized: boolean = false;
  private lastCloudSyncTime: number = 0;
  private tokenClient: GoogleTokenClient | null = null;
  private localSaveGetter: (() => string) | null = null;
  private onLoginCallbacks: Array<(profile: GoogleUserProfile, remoteSaveData?: string) => void> = [];

  constructor() {
    this.loadStoredProfile();
  }

  public getProfile(): GoogleUserProfile | null {
    return this.userProfile;
  }

  public isLoggedIn(): boolean {
    return !!this.userProfile;
  }

  public getLastSyncTime(): number {
    return this.lastCloudSyncTime;
  }

  public onLogin(callback: (profile: GoogleUserProfile, remoteSaveData?: string) => void) {
    this.onLoginCallbacks.push(callback);
  }

  private loadStoredProfile() {
    try {
      const stored = safeStorage.getItem('phatroi_google_profile');
      if (stored) {
        this.userProfile = JSON.parse(stored);
      }
    } catch {}
  }

  /**
   * Tải Google Identity Services SDK và khởi tạo cả Popup OAuth2 lẫn One Tap
   */
  public async initGsi(getLocalSaveData: () => string): Promise<boolean> {
    this.localSaveGetter = getLocalSaveData;
    if (typeof window === 'undefined') return false;

    return new Promise((resolve) => {
      const setup = () => {
        if (!window.google?.accounts) {
          resolve(false);
          return;
        }

        try {
          // 1. Khởi tạo Popup OAuth2 Client (Mở cửa sổ nhỏ popup khi bấm nút)
          if (window.google.accounts.oauth2) {
            this.tokenClient = window.google.accounts.oauth2.initTokenClient({
              client_id: GOOGLE_CLIENT_ID,
              scope: 'email profile openid',
              callback: async (response: GoogleTokenResponse) => {
                if (response.error || !response.access_token) {
                  console.warn('[Google OAuth Error]', response);
                  return;
                }
                const saveJson = this.localSaveGetter ? this.localSaveGetter() : '';
                await this.handleAccessTokenResponse(response.access_token, saveJson);
              },
              error_callback: (err: unknown) => {
                console.warn('[Google OAuth Popup Dismissed or Error]', err);
              },
            });
          }

          // 2. Khởi tạo ID Token Listener (Dành cho One Tap nếu có)
          if (window.google.accounts.id) {
            window.google.accounts.id.initialize({
              client_id: GOOGLE_CLIENT_ID,
              callback: (response) => {
                const saveJson = this.localSaveGetter ? this.localSaveGetter() : '';
                this.handleCredentialResponse(response.credential, saveJson);
              },
              auto_select: false,
              cancel_on_tap_outside: true,
            });
          }

          this.isInitialized = true;
          resolve(true);
        } catch (e) {
          console.warn('[GIS Init Error]', e);
          resolve(false);
        }
      };

      if (window.google?.accounts?.oauth2 || window.google?.accounts?.id) {
        setup();
      } else {
        const existingScript = document.querySelector('script[src*="accounts.google.com/gsi/client"]');
        if (existingScript) {
          existingScript.addEventListener('load', setup);
        } else {
          const script = document.createElement('script');
          script.src = 'https://accounts.google.com/gsi/client';
          script.async = true;
          script.defer = true;
          script.onload = setup;
          script.onerror = () => resolve(false);
          document.head.appendChild(script);
        }
      }
    });
  }

  /**
   * Mở cửa sổ nhỏ popup của Google để người chơi đăng nhập Gmail
   */
  public promptLogin() {
    if (typeof window === 'undefined') return;

    // Ưu tiên 1: Dùng tokenClient để bật popup cửa sổ nhỏ chọn tài khoản Google
    if (this.tokenClient) {
      try {
        this.tokenClient.requestAccessToken({ prompt: 'select_account' });
        return;
      } catch (err) {
        console.warn('[Failed to open Google Popup]', err);
      }
    }

    // Ưu tiên 2: Khởi tạo nóng tokenClient nếu window.google đã sẵn sàng
    if (window.google?.accounts?.oauth2) {
      try {
        this.tokenClient = window.google.accounts.oauth2.initTokenClient({
          client_id: GOOGLE_CLIENT_ID,
          scope: 'email profile openid',
          callback: async (response: GoogleTokenResponse) => {
            if (response.error || !response.access_token) return;
            const saveJson = this.localSaveGetter ? this.localSaveGetter() : '';
            await this.handleAccessTokenResponse(response.access_token, saveJson);
          },
        });
        this.tokenClient.requestAccessToken({ prompt: 'select_account' });
        return;
      } catch (err) {
        console.warn('[Hot init tokenClient error]', err);
      }
    }

    // Dự phòng: Thử gọi One Tap
    if (window.google?.accounts?.id) {
      try {
        window.google.accounts.id.prompt();
      } catch (e) {
        console.warn('[Google Auth Prompt Error]', e);
      }
    }
  }

  /**
   * Gắn nút Google Sign-In vào phần tử DOM (nếu cần)
   */
  public renderGoogleButton(element: HTMLElement) {
    if (!this.isInitialized || typeof window === 'undefined' || !window.google?.accounts?.id) {
      return;
    }
    try {
      window.google.accounts.id.renderButton(element, {
        theme: 'filled_black',
        size: 'medium',
        shape: 'pill',
        text: 'continue_with',
      });
    } catch {}
  }

  /**
   * Xử lý sau khi người dùng đăng nhập bằng Popup OAuth2
   */
  public async handleAccessTokenResponse(accessToken: string, localSaveData: string): Promise<GoogleAuthResponse> {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          accessToken,
          localSaveData,
        }),
      });

      const data = (await res.json()) as GoogleAuthResponse;

      if (data.success && data.profile) {
        this.userProfile = data.profile;
        this.lastCloudSyncTime = data.lastSyncAt || Date.now();
        safeStorage.setItem('phatroi_google_profile', JSON.stringify(data.profile));

        // Kích hoạt callbacks thông báo đăng nhập thành công
        this.onLoginCallbacks.forEach((cb) => cb(data.profile!, data.saveData));
        return data;
      }

      // Fallback: nếu API Worker có trục trặc mạng, gọi trực tiếp Google UserInfo
      const directGoogleRes = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      if (directGoogleRes.ok) {
        const userInfo = (await directGoogleRes.json()) as {
          sub: string;
          email: string;
          name?: string;
          picture?: string;
        };
        const fallbackProfile: GoogleUserProfile = {
          googleId: userInfo.sub,
          email: userInfo.email,
          name: userInfo.name || userInfo.email.split('@')[0],
          avatar: userInfo.picture || '',
        };
        this.userProfile = fallbackProfile;
        this.lastCloudSyncTime = Date.now();
        safeStorage.setItem('phatroi_google_profile', JSON.stringify(fallbackProfile));
        this.onLoginCallbacks.forEach((cb) => cb(fallbackProfile, localSaveData));
        return { success: true, profile: fallbackProfile, saveData: localSaveData };
      }

      return data;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      return { success: false, error: msg };
    }
  }

  /**
   * Xử lý sau khi người dùng chọn tài khoản Google qua One Tap ID Token
   */
  public async handleCredentialResponse(credential: string, localSaveData: string): Promise<GoogleAuthResponse> {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          credential,
          localSaveData,
        }),
      });

      const data = (await res.json()) as GoogleAuthResponse;

      if (data.success && data.profile) {
        this.userProfile = data.profile;
        this.lastCloudSyncTime = data.lastSyncAt || Date.now();
        safeStorage.setItem('phatroi_google_profile', JSON.stringify(data.profile));

        // Thông báo cho các listeners
        this.onLoginCallbacks.forEach((cb) => cb(data.profile!, data.saveData));
        return data;
      }
      return data;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      return { success: false, error: msg };
    }
  }

  /**
   * Đẩy dữ liệu tiến độ chơi game lên Cloudflare D1
   */
  public async pushCloudSave(saveDataString: string): Promise<boolean> {
    if (!this.userProfile) return false;

    try {
      const res = await fetch(`${API_BASE_URL}/player/cloud-save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          googleId: this.userProfile.googleId,
          saveData: saveDataString,
        }),
      });

      const data = (await res.json()) as { success: boolean; lastSyncAt?: number };
      if (data.success) {
        this.lastCloudSyncTime = data.lastSyncAt || Date.now();
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  /**
   * Đăng xuất khỏi tài khoản Google trong game
   */
  public logout() {
    this.userProfile = null;
    safeStorage.removeItem('phatroi_google_profile');
    if (typeof window !== 'undefined' && window.google?.accounts?.id) {
      try {
        window.google.accounts.id.disableAutoSelect();
      } catch {}
    }
  }
}

export const googleAuthService = new GoogleAuthService();

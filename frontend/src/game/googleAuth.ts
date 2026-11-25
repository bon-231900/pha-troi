// ==============================================================================
// DỰ ÁN WEBGAME "PHÁ TRỜI" (PHATROI.COM) - GOOGLE SIGN-IN & CLOUD SAVE CLIENT
// ==============================================================================

import { safeStorage } from './storage';

export const GOOGLE_CLIENT_ID = '325984073866-an8facrtq5edm0aetm5ok3qmrf00oq7t.apps.googleusercontent.com';
const API_BASE_URL = 'https://phatroi-api.beanbinh2000.workers.dev/api';
const PROFILE_STORAGE_KEY = 'phatroi_google_profile';
const SESSION_TOKEN_STORAGE_KEY = 'phatroi_session_token';

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
  sessionToken?: string;
  sessionExpiresAt?: number;
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
  private sessionToken: string | null = null;
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

  public hasActiveSession(): boolean {
    return !!(this.userProfile && this.sessionToken);
  }

  public getLastSyncTime(): number {
    return this.lastCloudSyncTime;
  }

  public onLogin(callback: (profile: GoogleUserProfile, remoteSaveData?: string) => void) {
    this.onLoginCallbacks.push(callback);
  }

  private loadStoredProfile() {
    try {
      const stored = safeStorage.getItem(PROFILE_STORAGE_KEY);
      if (stored) {
        this.userProfile = JSON.parse(stored);
      }
    } catch {
      this.userProfile = null;
    }

    try {
      const storedToken = safeStorage.getItem(SESSION_TOKEN_STORAGE_KEY);
      this.sessionToken = storedToken && storedToken.trim() ? storedToken.trim() : null;
    } catch {
      this.sessionToken = null;
    }
  }

  private setSessionToken(token: string) {
    this.sessionToken = token;
    safeStorage.setItem(SESSION_TOKEN_STORAGE_KEY, token);
  }

  private clearSessionToken() {
    this.sessionToken = null;
    safeStorage.removeItem(SESSION_TOKEN_STORAGE_KEY);
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
   * Gửi token Google lên Cloudflare Worker để xác thực và cấp sessionToken HMAC
   */
  private async authenticateWithWorker(
    payload: { accessToken: string; localSaveData: string } | { credential: string; localSaveData: string }
  ): Promise<GoogleAuthResponse> {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = (await res.json().catch(() => null)) as GoogleAuthResponse | null;
      const sessionToken = typeof data?.sessionToken === 'string' ? data.sessionToken.trim() : '';

      if (!res.ok || !data || !data.success || !data.profile || !sessionToken) {
        this.clearSessionToken();
        return {
          success: false,
          error:
            data?.error ||
            (res.ok
              ? data?.success && data?.profile
                ? 'Máy chủ không cấp session token hợp lệ'
                : 'Xác thực tài khoản Google không thành công'
              : `Lỗi máy chủ xác thực (${res.status})`),
        };
      }

      this.userProfile = data.profile;
      this.lastCloudSyncTime = data.lastSyncAt || Date.now();
      safeStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(data.profile));
      this.setSessionToken(sessionToken);

      // Kích hoạt callbacks thông báo đăng nhập thành công
      this.onLoginCallbacks.forEach((cb) => cb(data.profile!, data.saveData));
      return data;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      return { success: false, error: msg };
    }
  }

  /**
   * Xử lý sau khi người dùng đăng nhập bằng Popup OAuth2
   */
  public async handleAccessTokenResponse(accessToken: string, localSaveData: string): Promise<GoogleAuthResponse> {
    return this.authenticateWithWorker({ accessToken, localSaveData });
  }

  /**
   * Xử lý sau khi người dùng chọn tài khoản Google qua One Tap ID Token
   */
  public async handleCredentialResponse(credential: string, localSaveData: string): Promise<GoogleAuthResponse> {
    return this.authenticateWithWorker({ credential, localSaveData });
  }

  /**
   * Đẩy dữ liệu tiến độ chơi game lên Cloudflare D1
   */
  public async pushCloudSave(saveDataString: string): Promise<boolean> {
    if (!this.userProfile || !this.sessionToken) return false;

    const token = this.sessionToken;
    const googleId = this.userProfile.googleId;

    try {
      const res = await fetch(`${API_BASE_URL}/player/cloud-save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          googleId,
          saveData: saveDataString,
        }),
      });

      if (res.status === 401 || res.status === 403) {
        if (this.sessionToken === token) {
          this.clearSessionToken();
        }
        return false;
      }

      if (!res.ok) return false;

      const data = (await res.json().catch(() => null)) as { success?: boolean; lastSyncAt?: number } | null;
      if (data?.success) {
        if (this.sessionToken === token) {
          this.lastCloudSyncTime = data.lastSyncAt || Date.now();
        }
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  /**
   * Tải dữ liệu tiến độ chơi game từ Cloudflare D1
   */
  public async pullCloudLoad(): Promise<GoogleAuthResponse | null> {
    if (!this.sessionToken) return null;

    const token = this.sessionToken;

    try {
      const res = await fetch(`${API_BASE_URL}/player/cloud-load`, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.status === 401 || res.status === 403) {
        if (this.sessionToken === token) {
          this.clearSessionToken();
        }
        return null;
      }

      const data = (await res.json().catch(() => null)) as GoogleAuthResponse | null;
      if (!res.ok || !data) return null;

      if (data.success && this.sessionToken === token) {
        if (data.profile) {
          this.userProfile = data.profile;
          safeStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(data.profile));
        }
        if (data.lastSyncAt) {
          this.lastCloudSyncTime = data.lastSyncAt;
        }
      }

      return data;
    } catch {
      return null;
    }
  }

  /**
   * Đăng xuất khỏi tài khoản Google trong game
   */
  public logout() {
    this.userProfile = null;
    this.lastCloudSyncTime = 0;
    this.clearSessionToken();
    safeStorage.removeItem(PROFILE_STORAGE_KEY);
    if (typeof window !== 'undefined' && window.google?.accounts?.id) {
      try {
        window.google.accounts.id.disableAutoSelect();
      } catch {}
    }
  }
}

export const googleAuthService = new GoogleAuthService();

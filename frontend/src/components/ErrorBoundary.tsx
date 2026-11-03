import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error caught by ErrorBoundary:', error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleClearStorageAndReload = () => {
    try {
      localStorage.clear();
      sessionStorage.clear();
    } catch {}
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      const isWebGL = this.state.error?.message?.toLowerCase().includes('webgl') ||
        this.state.error?.message?.toLowerCase().includes('context');

      return (
        <div className="min-h-screen h-screen w-screen bg-[#080A10] text-slate-100 flex flex-col items-center justify-center p-6 select-none font-sans">
          <div className="max-w-lg w-full bg-slate-900/90 border border-amber-500/40 rounded-2xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl text-center flex flex-col items-center">
            {/* Forge Emblem */}
            <div className="w-16 h-16 rounded-full bg-amber-500/10 border border-amber-400/30 flex items-center justify-center mb-5 text-2xl shadow-lg shadow-amber-500/20 animate-pulse">
              🔥
            </div>

            <h1 className="text-xl sm:text-2xl font-bold text-amber-300 font-display mb-2 tracking-wide">
              {isWebGL
                ? 'LÒ RÈN CẦN BẬT TĂNG TỐC PHẦN CỨNG'
                : 'THIÊN CỔ LÒ RÈN TẠM THỜI GIÁN ĐOẠN'}
            </h1>

            <p className="text-sm text-slate-300 mb-6 leading-relaxed">
              {isWebGL ? (
                <>
                  Trình duyệt của bạn đang tắt <b>WebGL</b> hoặc tính năng <b>Tăng tốc phần cứng (Hardware Acceleration)</b>.<br /><br />
                  <span className="text-slate-400 text-xs">
                    Vui lòng vào <b>Cài đặt trình duyệt &gt; Hệ thống &gt; Bật Tăng tốc phần cứng</b> (hoặc mở bằng Chrome, Safari, Edge) để chiêm ngưỡng Mái Vòm Thiên Giới.
                  </span>
                </>
              ) : (
                'Đã xảy ra sự cố không lường trước trong quá trình nạp linh khí. Vui lòng làm mới trang hoặc thử lại.'
              )}
            </p>

            {this.state.error && (
              <div className="w-full bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-left font-mono text-xs text-red-400 mb-6 max-h-24 overflow-y-auto">
                {this.state.error.message}
              </div>
            )}

            <div className="flex flex-col sm:flex-row items-center gap-3 w-full">
              <button
                type="button"
                onClick={this.handleReload}
                className="w-full py-3 px-4 rounded-xl bg-amber-400 hover:bg-amber-300 active:bg-amber-500 text-slate-950 font-bold text-sm tracking-wider cursor-pointer shadow-lg shadow-amber-500/25 transition-all"
              >
                Làm Mới Trang [F5]
              </button>
              <button
                type="button"
                onClick={this.handleClearStorageAndReload}
                className="w-full py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs tracking-wide cursor-pointer transition-all border border-slate-700"
              >
                Xóa Cache & Vào Lại
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

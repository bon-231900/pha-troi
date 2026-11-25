with open('frontend/src/components/BeginnerTutorialGuide.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add close button in minimized view
target_minimized = '''          <button
            type="button"
            className="text-amber-400 hover:text-amber-200 p-0.5 rounded transition"
            title="Mở rộng hướng dẫn"
          >
            <ChevronDown className="w-4 h-4" />
          </button>
        </div>'''

replacement_minimized = '''          <div className="flex items-center gap-1.5">
            <button
              type="button"
              className="text-amber-400 hover:text-amber-200 p-0.5 rounded transition"
              title="Mở rộng hướng dẫn"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setShowSkipConfirm(true);
              }}
              className="text-slate-400 hover:text-rose-400 p-0.5 rounded transition"
              title="Đóng hướng dẫn"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>'''

# 2. Add close button in expanded header
target_header = '''              <button
                type="button"
                onClick={() => setShowSkipConfirm(true)}
                className="px-2 py-0.5 rounded-md hover:bg-rose-950/40 border border-transparent hover:border-rose-500/40 text-[10px] text-slate-400 hover:text-rose-300 transition cursor-pointer"
                title="Bỏ qua hướng dẫn"
              >
                Bỏ qua
              </button>
            </div>'''

replacement_header = '''              <button
                type="button"
                onClick={() => setShowSkipConfirm(true)}
                className="px-2 py-0.5 rounded-md hover:bg-rose-950/40 border border-transparent hover:border-rose-500/40 text-[10px] text-slate-400 hover:text-rose-300 transition cursor-pointer"
                title="Bỏ qua hướng dẫn"
              >
                Bỏ qua
              </button>
              <button
                type="button"
                onClick={() => setShowSkipConfirm(true)}
                className="p-1 rounded-lg hover:bg-rose-950/60 text-slate-400 hover:text-rose-300 transition cursor-pointer ml-0.5"
                title="Đóng vĩnh viễn"
              >
                <X className="w-4 h-4" />
              </button>
            </div>'''

assert target_minimized in c, 'target_minimized not found'
assert target_header in c, 'target_header not found'

c = c.replace(target_minimized, replacement_minimized, 1)
c = c.replace(target_header, replacement_header, 1)

with open('frontend/src/components/BeginnerTutorialGuide.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated BeginnerTutorialGuide.tsx successfully!')

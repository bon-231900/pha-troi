# -*- coding: utf-8 -*-
with open('frontend/src/App.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update TopBossHeader invocation
old_top_header = """        leftPanelOpen={leftPanelOpen}
        onToggleLeftPanel={() => setLeftPanelOpen((prev) => !prev)}
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen((prev) => !prev)}
      />"""

new_top_header = """        leftPanelOpen={leftPanelOpen}
        onToggleLeftPanel={() => setLeftPanelOpen((prev) => !prev)}
        rightPanelOpen={rightPanelOpen}
        onToggleRightPanel={() => setRightPanelOpen((prev) => !prev)}
        playerClass={getPlayerClass(playerClassId || 'thunder')}
        onOpenClassModal={() => setShowClassModal(true)}
      />"""

code = code.replace(old_top_header, new_top_header, 1)

# 2. Replace Bottom-Left Dock (4 Stances + Overdrive) with ClassSkillBar
old_dock = """      {/* 3. CORNER HUD DOCKS (Positioned at corners to leave the Center Hero & Anvil 100% Unobstructed) */}
      {/* 3A. Bottom-Left Dock: 4 Hammer Stances + Overdrive 8/8 Bar */}
      <div
        className={`fixed bottom-3 left-3 sm:left-5 z-20 flex flex-col gap-1.5 pointer-events-auto max-w-[310px] sm:max-w-[360px] transition-all duration-300 ${
          hudVisible
            ? 'opacity-100 translate-y-0'
            : 'opacity-0 translate-y-6 pointer-events-none'
        }`}
      >
        {/* 4 Hammer Stances Bar (Q - W - E - R) */}
        <div
          role="group"
          aria-label="4 Thế Búa Q W E R"
          className="flex items-center gap-1 sm:gap-1.5 p-1 rounded-xl bg-slate-950/85 border border-slate-800/90 backdrop-blur-md shadow-lg"
        >
          {stanceKeys.map((k) => {
            const st = HAMMER_STANCES[k];
            const isSelected = activeStance === k;
            return (
              <button
                key={k}
                type="button"
                onClick={() => handleSelectStance(k)}
                className={`flex items-center gap-1 px-2 py-1.5 rounded-lg border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-slate-900 border-amber-400 text-amber-300 shadow-md shadow-amber-500/20 scale-[1.02]'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
                title={`[${k}] ${st.name} - ${st.role}`}
              >
                <span
                  className="w-4 h-4 rounded text-[10px] font-tech font-bold flex items-center justify-center"
                  style={{
                    backgroundColor: isSelected ? st.color : 'rgba(255,255,255,0.06)',
                    color: isSelected ? '#05070F' : '#94A3B8',
                  }}
                >
                  {k}
                </span>
                <span className="hidden sm:inline text-xs font-semibold whitespace-nowrap">
                  {st.name}
                </span>
              </button>
            );
          })}
        </div>

        {/* Overdrive 8/8 Bar */}
        <div
          className={`rounded-xl px-2.5 py-1.5 border backdrop-blur-md transition-colors ${
            overdriveActive
              ? 'bg-cyan-500/20 border-cyan-400 shadow-md shadow-cyan-400/20'
              : 'bg-slate-950/85 border-slate-800/90'
          }`}
        >
          <div className="flex items-center justify-between text-[10px] sm:text-[11px] font-tech mb-1">
            <span className={overdriveActive ? 'text-cyan-300 font-bold' : 'text-slate-400'}>
              {overdriveActive
                ? `LÔI ĐÌNH QUÁ TẢI (${overdriveTimeLeft.toFixed(1)}s)`
                : 'Overdrive · Chuỗi 8/8'}
            </span>
            <span className="font-bold text-amber-300">
              {overdriveActive ? 'x2.0 DMG' : `${overdriveCharge.toFixed(1)}/8`}
            </span>
          </div>

          <div className="grid grid-cols-8 gap-0.5 sm:gap-1">
            {Array.from({ length: OVERDRIVE_MAX }).map((_, idx) => {
              const filled = overdriveActive || overdriveCharge >= idx + 1;
              const half = !filled && overdriveCharge >= idx + 0.5;
              return (
                <div
                  key={idx}
                  className={`h-1.5 rounded-sm transition-all ${
                    overdriveActive
                      ? 'bg-cyan-400 shadow-sm shadow-cyan-400/60'
                      : filled
                      ? 'bg-amber-400'
                      : half
                      ? 'bg-amber-400/50'
                      : 'bg-slate-800'
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>"""

new_dock = """      {/* 3. CORNER HUD DOCKS (Positioned at corners to leave the Center Hero & Anvil 100% Unobstructed) */}
      {/* 3A. Bottom-Left Dock: 4 Class Skills Q W E R + 3-Tier Overcharge Gauge */}
      <ClassSkillBar
        playerClass={getPlayerClass(playerClassId || 'thunder')}
        overdriveCharge={overdriveCharge}
        overdriveActive={overdriveActive}
        overdriveTimeLeft={overdriveTimeLeft}
        totalForgeLevel={upgrades.reduce((sum, u) => sum + u.level, 0)}
        cooldowns={skillCooldowns}
        onCastSkill={handleCastClassSkill}
        onOpenClassSelect={() => setShowClassModal(true)}
        hudVisible={hudVisible}
      />"""

code = code.replace(old_dock, new_dock, 1)

# 3. Add CharacterCreationModal
target_modal = """      {(gameState === 'paused' || gameState === 'gameover') && ("""
modal_code = """      {/* 4. Character Creation & Single-Class Commitment Modal */}
      {(showClassModal || (!playerClassId && gameState === 'playing')) && (
        <CharacterCreationModal
          currentClassId={playerClassId}
          currentName={playerName}
          isInitialCreation={!playerClassId}
          onConfirm={handleCommitClass}
          onCancel={() => setShowClassModal(false)}
        />
      )}

      {(gameState === 'paused' || gameState === 'gameover') && ("""

code = code.replace(target_modal, modal_code, 1)

with open('frontend/src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Part 2 of App.tsx patch completed successfully!")

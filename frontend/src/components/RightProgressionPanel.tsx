import React, { useState } from 'react';
import {
  ForgeUpgrade,
  SpiritNode,
  getUpgradeCost,
  canUnlockSpiritNode,
  calculateSpiritMultiplier,
} from '../game/rules';
import { Hammer, Sparkles, Trophy, X, Check } from 'lucide-react';

export interface LeaderboardEntry {
  id: string;
  name: string;
  sect: string;
  damageBillions: number;
  isPlayer?: boolean;
}

interface RightProgressionPanelProps {
  upgrades: ForgeUpgrade[];
  spiritNodes: SpiritNode[];
  linhThach: number;
  tinhHoa: number;
  leaderboard: LeaderboardEntry[];
  mobileDrawerOpen: boolean;
  onCloseMobileDrawer: () => void;
  onBuyUpgrade: (upgradeId: string) => void;
  onUnlockSpiritNode: (nodeId: string) => void;
}

export const RightProgressionPanel: React.FC<RightProgressionPanelProps> = ({
  upgrades,
  spiritNodes,
  linhThach,
  tinhHoa,
  leaderboard,
  mobileDrawerOpen,
  onCloseMobileDrawer,
  onBuyUpgrade,
  onUnlockSpiritNode,
}) => {
  const [activeTab, setActiveTab] = useState<'upgrades' | 'spirit' | 'leaderboard'>('upgrades');
  const [selectedNodeId, setSelectedNodeId] = useState<string>('node_thunder_eye');

  const selectedNode =
    spiritNodes.find((n) => n.id === selectedNodeId) || spiritNodes[0];
  const spiritTotalMult = calculateSpiritMultiplier(spiritNodes);

  const renderPanelContent = () => (
    <div className="flex flex-col h-full">
      {/* Segmented Control Tabs */}
      <div
        role="tablist"
        aria-label="Quản lý Rèn Đúc, Thần Hồn và Bảng Vàng"
        className="grid grid-cols-3 gap-1 p-1 bg-[#080A10] border border-slate-800 rounded-xl mb-3 shrink-0"
      >
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'upgrades'}
          onClick={() => setActiveTab('upgrades')}
          className={`flex items-center justify-center gap-1.5 py-2 px-2 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'upgrades'
              ? 'bg-amber-400 text-slate-950 font-semibold'
              : 'text-slate-300 hover:text-white'
          }`}
        >
          <Hammer className="w-3.5 h-3.5" />
          <span>Nâng Cấp</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'spirit'}
          onClick={() => setActiveTab('spirit')}
          className={`flex items-center justify-center gap-1.5 py-2 px-2 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'spirit'
              ? 'bg-cyan-400 text-slate-950 font-semibold'
              : 'text-slate-300 hover:text-white'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Thần Hồn</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'leaderboard'}
          onClick={() => setActiveTab('leaderboard')}
          className={`flex items-center justify-center gap-1.5 py-2 px-2 rounded-lg text-xs font-medium transition-colors cursor-pointer whitespace-nowrap ${
            activeTab === 'leaderboard'
              ? 'bg-amber-400 text-slate-950 font-semibold'
              : 'text-slate-300 hover:text-white'
          }`}
        >
          <Trophy className="w-3.5 h-3.5" />
          <span>Bảng Vàng</span>
        </button>
      </div>

      {/* Resource Bar Summary inside Panel */}
      <div className="flex items-center justify-between px-3 py-2 rounded-lg bg-[#080A10] border border-slate-800/80 mb-3 font-tech text-xs shrink-0">
        <div>
          <span className="text-slate-400">Linh Thạch: </span>
          <span className="text-cyan-300 font-bold">{linhThach.toLocaleString('en-US')}</span>
        </div>
        <span>·</span>
        <div>
          <span className="text-slate-400">Tinh Hoa: </span>
          <span className="text-amber-300 font-bold">{tinhHoa}</span>
        </div>
        <span>·</span>
        <div>
          <span className="text-slate-400">Thần Hồn: </span>
          <span className="text-emerald-300 font-bold">x{spiritTotalMult.toFixed(2)}</span>
        </div>
      </div>

      {/* Tab Body */}
      <div className="flex-1 overflow-y-auto pr-0.5 space-y-2.5">
        {activeTab === 'upgrades' && (
          <div className="space-y-2.5">
            {upgrades.map((up) => {
              const cost = getUpgradeCost(up);
              const canAfford = linhThach >= cost && up.level < up.maxLevel;
              return (
                <div
                  key={up.id}
                  className="p-3 rounded-xl bg-[#080A10] border border-slate-800/90 flex flex-col gap-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="font-semibold text-sm text-slate-100">{up.name}</div>
                      <div className="text-xs text-slate-400">{up.subtitle}</div>
                    </div>
                    <span className="font-tech text-xs text-amber-300 font-semibold whitespace-nowrap">
                      Cấp {up.level}/{up.maxLevel}
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-1 border-t border-slate-800/70">
                    <div className="text-xs font-tech text-slate-300">
                      Hiện tăng:{' '}
                      <span className="text-cyan-300 font-semibold">
                        +{(up.level * up.powerPerLevel).toFixed(2)}B
                      </span>
                    </div>
                    <button
                      type="button"
                      disabled={!canAfford}
                      onClick={() => onBuyUpgrade(up.id)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-tech font-bold transition-all whitespace-nowrap shrink-0 ${
                        canAfford
                          ? 'bg-amber-400 hover:bg-amber-300 text-slate-950 cursor-pointer shadow-sm shadow-amber-400/20'
                          : 'bg-slate-800/80 text-slate-500 cursor-not-allowed'
                      }`}
                    >
                      {up.level >= up.maxLevel
                        ? 'TỐI ĐA'
                        : `Rèn Cấp · ${cost.toLocaleString('en-US')} LT`}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {activeTab === 'spirit' && (
          <div className="flex flex-col gap-3">
            {/* Constellation SVG Map (Cây Thần Hồn Dạng Chòm Sao) */}
            <div className="relative rounded-xl bg-[#080A10] border border-slate-800 p-3 overflow-hidden">
              <div className="text-xs font-tech text-slate-400 mb-1 flex items-center justify-between">
                <span>Chòm Sao Cửu Trọng Thần Hồn</span>
                <span className="text-amber-300">Chạm tinh tú để khai mở</span>
              </div>

              <svg viewBox="0 0 100 100" className="w-full h-52">
                {/* Constellation Connecting Lines */}
                {spiritNodes.map((node) => {
                  if (!node.requires) return null;
                  const parent = spiritNodes.find((p) => p.id === node.requires);
                  if (!parent) return null;
                  const activeLink = node.unlocked && parent.unlocked;
                  return (
                    <line
                      key={`${parent.id}-${node.id}`}
                      x1={parent.x}
                      y1={parent.y}
                      x2={node.x}
                      y2={node.y}
                      stroke={activeLink ? '#00F0FF' : '#334155'}
                      strokeWidth={activeLink ? '1.2' : '0.8'}
                      strokeDasharray={activeLink ? undefined : '2 2'}
                    />
                  );
                })}

                {/* Constellation Star Nodes */}
                {spiritNodes.map((node) => {
                  const isSelected = selectedNode.id === node.id;
                  const unlockable = canUnlockSpiritNode(node.id, spiritNodes, tinhHoa);
                  return (
                    <g
                      key={node.id}
                      onClick={() => setSelectedNodeId(node.id)}
                      className="cursor-pointer"
                    >
                      {isSelected && (
                        <circle
                          cx={node.x}
                          cy={node.y}
                          r="8.5"
                          fill="none"
                          stroke="#FFD23F"
                          strokeWidth="0.9"
                          strokeDasharray="2 1.5"
                        />
                      )}
                      <circle
                        cx={node.x}
                        cy={node.y}
                        r={node.unlocked ? '5.2' : '4.5'}
                        fill={
                          node.unlocked
                            ? '#00F0FF'
                            : unlockable
                            ? '#FFD23F'
                            : '#1E293B'
                        }
                        stroke={isSelected ? '#FFFFFF' : '#080A10'}
                        strokeWidth="1.2"
                      />
                      <text
                        x={node.x}
                        y={node.y + 10}
                        textAnchor="middle"
                        fill={node.unlocked ? '#E2E8F0' : '#94A3B8'}
                        fontSize="4.2"
                        fontWeight="600"
                      >
                        {node.name}
                      </text>
                    </g>
                  );
                })}
              </svg>
            </div>

            {/* Selected Constellation Node Details & Unlock Action */}
            <div className="p-3.5 rounded-xl bg-[#080A10] border border-slate-800 flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xs font-tech text-cyan-300">
                    {selectedNode.constellation}
                  </div>
                  <h4 className="font-display font-bold text-sm text-amber-300">
                    {selectedNode.name}
                  </h4>
                </div>
                <span className="text-xs font-tech font-bold text-emerald-300">
                  +{Math.round(selectedNode.bonusMult * 100)}% Công Lực
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                {selectedNode.description}
              </p>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-xs font-tech text-slate-400">
                  {selectedNode.unlocked
                    ? 'Trạng thái: Đã Khai Mở'
                    : `Yêu cầu: ${selectedNode.costTinhHoa} Tinh Hoa`}
                </span>

                {selectedNode.unlocked ? (
                  <span className="inline-flex items-center gap-1 text-xs font-tech font-bold text-cyan-300">
                    <Check className="w-3.5 h-3.5" /> Đã Kích Hoạt
                  </span>
                ) : (
                  <button
                    type="button"
                    disabled={!canUnlockSpiritNode(selectedNode.id, spiritNodes, tinhHoa)}
                    onClick={() => onUnlockSpiritNode(selectedNode.id)}
                    className={`px-3.5 py-1.5 rounded-lg text-xs font-tech font-bold transition-all whitespace-nowrap ${
                      canUnlockSpiritNode(selectedNode.id, spiritNodes, tinhHoa)
                        ? 'bg-cyan-400 hover:bg-cyan-300 text-slate-950 cursor-pointer'
                        : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    Khai Mở Tinh Hồn
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'leaderboard' && (
          <div className="space-y-2">
            <div className="text-xs text-slate-400 font-tech px-1">
              Bảng Vàng Cửu Trọng · Xếp hạng theo Sát Thương Tích Lũy
            </div>
            {leaderboard.map((row, index) => (
              <div
                key={row.id}
                className={`p-3 rounded-xl border flex items-center justify-between gap-2 ${
                  row.isPlayer
                    ? 'bg-amber-500/10 border-amber-400/70'
                    : 'bg-[#080A10] border-slate-800/90'
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <span
                    className={`w-6 h-6 rounded-md font-tech font-bold text-xs flex items-center justify-center shrink-0 ${
                      index === 0
                        ? 'bg-amber-400 text-slate-950'
                        : index === 1
                        ? 'bg-cyan-400 text-slate-950'
                        : index === 2
                        ? 'bg-orange-400 text-slate-950'
                        : 'bg-slate-800 text-slate-300'
                    }`}
                  >
                    {index + 1}
                  </span>
                  <div className="min-w-0">
                    <div
                      className={`text-xs font-semibold truncate ${
                        row.isPlayer ? 'text-amber-300' : 'text-slate-100'
                      }`}
                    >
                      {row.name}
                    </div>
                    <div className="text-[11px] text-slate-400 truncate">{row.sect}</div>
                  </div>
                </div>

                <div className="text-right font-tech shrink-0">
                  <div className="text-xs font-bold text-amber-300">
                    {row.damageBillions.toFixed(2)}B
                  </div>
                  <div className="text-[10px] text-slate-400">Sát thương</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Right Column */}
      <aside
        aria-label="Nâng Cấp, Cây Thần Hồn và Bảng Vàng"
        className="hidden lg:flex lg:w-[340px] xl:w-[370px] flex-col p-4 bg-[#111625]/70 border-l border-slate-800/90 shrink-0 overflow-hidden"
      >
        {renderPanelContent()}
      </aside>

      {/* Mobile Portrait Bottom Sheet Drawer (Ngăn Kéo Vuốt Lên) */}
      {mobileDrawerOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="Ngăn kéo Nâng Cấp và Cây Thần Hồn"
          className="fixed inset-0 z-50 lg:hidden flex flex-col justify-end bg-black/70"
        >
          <div className="w-full max-h-[82vh] bg-[#111625] border-t border-slate-700 rounded-t-3xl p-4 flex flex-col overflow-hidden">
            {/* Grab Handle + Header */}
            <div className="w-10 h-1.5 bg-slate-600 rounded-full mx-auto mb-2 shrink-0" />
            <div className="flex items-center justify-between mb-3 shrink-0">
              <h3 className="font-display font-bold text-base text-amber-300">
                Thần Lò Tiến Hóa · Cửu Trọng Thiên
              </h3>
              <button
                type="button"
                aria-label="Đóng ngăn kéo"
                onClick={onCloseMobileDrawer}
                className="p-2 rounded-lg bg-[#080A10] text-slate-300 hover:text-white cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto">{renderPanelContent()}</div>
          </div>
        </div>
      )}
    </>
  );
};

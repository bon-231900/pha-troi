# BÁO CÁO TOÀN DIỆN KIẾN TRÚC & AN NINH HỆ THỐNG: PHÁ TRỜI NOVEL OS V2 REFACTOR
**Mã tài liệu**: `AUDIT-V2-20260915`  
**Ngày thực hiện**: 15/09/2026  
**Trạng thái**: PHASE 0 — READ ONLY COMPLETED (CHỜ TÁC GIẢ DUYỆT)  
**Mục tiêu hệ thống**: Chuyển đổi từ *Advanced Prototype* sang *Reliable, Auditable, Deterministic Novel Operating System* chịu tải **3.000+ chương** (~8–10 triệu từ).

---

## MỤC LỤC
1. [Tóm Tắt Điều Hành (Executive Summary)](#1-tóm-tắt-điều-hành-executive-summary)
2. [Phần A: Phân Tích Kiến Trúc & Luồng Dữ Liệu Hiện Tại (Architecture & Data Flow)](#phần-a-phân-tích-kiến-trúc--luồng-dữ-liệu-hiện-tại-architecture--data-flow)
3. [Phần B: Kiểm Tra An Ninh & Rò Rỉ Bí Mật (Security & Secret Leakage)](#phần-b-kiểm-tra-an-ninh--rò-rỉ-bí-mật-security--secret-leakage)
4. [Phần C: Toàn Vẹn Dữ Liệu & Ma Trận Thẩm Quyền Nguồn Sự Thật (Data Integrity & Authority Matrix)](#phần-c-toàn-vẹn-dữ-liệu--ma-trận-thẩm-quyền-nguồn-sự-thật-data-integrity--authority-matrix)
5. [Phần D: Kiểm Thử & Cách Ly Môi Trường (Testing & Isolation)](#phần-d-kiểm-thử--cách-ly-môi-trường-testing--isolation)
6. [Phần E: Ranh Giới AI & Tách Biệt Nhận Thức (AI Boundaries & Epistemic Separation)](#phần-e-ranh-giới-ai--tách-biệt-nhận-thức-ai-boundaries--epistemic-separation)
7. [Phần F: An Toàn Git & Triển Khai GitHub Pages (Git Safety & Deployment Boundary)](#phần-f-an-toàn-git--triển-khai-github-pages-git-safety--deployment-boundary)
8. [Phần G: Thiết Kế Mô Hình Narrative Event & Projection (Event-Driven State Architecture)](#phần-g-thiết-kế-mô-hình-narrative-event--projection-event-driven-state-architecture)
9. [Phần H: Lộ Trình Triển Khai Từng Bước (Incremental Migration Roadmap: Phase 1 – Phase 9)](#phần-h-lộ-trình-triển-khai-từng-bước-incremental-migration-roadmap-phase-1--phase-9)
10. [Phần I: Ma Trận Đánh Giá Rủi Ro & Cơ Chế Hoàn Tác (Risk Assessment & Rollback Matrix)](#phần-i-ma-trận-đánh-giá-rủi-ro--cơ-chế-hoàn-tác-risk-assessment--rollback-matrix)

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Dự án **Phá Trời Novel OS** đã xây dựng một nền tảng tạo dựng tiểu thuyết đô thị tu tiên phong phú với 57 chương bản thảo thực tế (~150.000 từ), 21 động cơ chuyên biệt, cơ chế tra cứu BM25 qua SQLite FTS5 và hệ thống theo dõi nhận thức (epistemic state). 

Tuy nhiên, cuộc rà soát mã nguồn (Phase 0) phát hiện hệ thống đang ở ranh giới giữa một **Prototype hoạt động cục bộ** và một **Operating System chịu tải 3.000 chương**. Tồn tại 4 lỗ hổng nghiêm trọng mức độ **P0 (Blockers)** đe dọa trực tiếp đến tính bảo mật tác phẩm và an toàn dữ liệu, cùng 6 rủi ro kiến trúc mức độ **P1** có thể làm sụp đổ tính nhất quán khi số chương tăng cao.

### Tổng hợp phân loại phát hiện:
* **P0 Blockers**: 4 điểm (Rò rỉ bí mật trong ContextBuilder; Bí mật tác giả & Database lộ trên Git remote và GitHub Pages; `git add .` tùy tiện trong commit tự động; Git remote URL nhúng trực tiếp Personal Access Token).
* **P1 Architectural Risks**: 6 điểm (CoAuthorEngine ôm 600 dòng code cứng từ chương 1-22; RevisionEngine dùng regex mù; ProposalManager chỉ đổi chuỗi trạng thái không có mutation thực tế; Bộ kiểm thử Unit test ghi đè trực tiếp vào cơ sở dữ liệu thật; Sort thứ tự ưu tiên bằng chữ cái làm tụt hạng CRITICAL; Đường dẫn tuyệt đối Windows `d:\tieu-thuyet` bám rễ trong mã nguồn lõi).
* **P2 Improvements**: 5 điểm (FTS5 thiếu Entity Registry chuẩn hóa; ForeshadowingEngine cảnh báo ngủ quên cứng ngắc theo mốc 50 chương; TimelineEngine nuốt ngoại lệ âm thầm; Thiếu các chỉ mục SQL trọng yếu; Static reader chỉ đọc cố định Arc 1 bỏ quên Arc 2).

---

## PHẦN A: PHÂN TÍCH KIẾN TRÚC & LUỒNG DỮ LIỆU HIỆN TẠI (ARCHITECTURE & DATA FLOW)

### 1. Sơ đồ luồng dữ liệu hiện tại (Current Data Flow)
```
[User Request / CLI]
       │
       ▼
[CoAuthorEngine] ──(Gọi trực tiếp)──► [ContextBuilder]
       │                                     │
       │                                     ├─► SQLite (entities, states, ledger)
       │                                     ├─► FTS5 search_index
       │                                     └─► (Rò rỉ: actual_meaning từ ledger)
       ▼
[AI Model / Mock Draft]
       │
       ▼
[CritiqueEngine] ──► Kiểm tra 11 chiều (Hardcoded typos, hardcoded items)
       │         ──► Ghi trực tiếp lỗi vào SQLite (continuity_errors)
       ▼
[RevisionEngine] ──► re.sub() xóa cụm từ mù quáng
       │
       ▼
[Bản thảo ch_XXX.md] (Ghi đè tệp tin)
       ├─► [DocxPipeline] ──► Tạo ch_XXX.docx
       ├─► [RetrievalEngine] ──► Index vào FTS5
       ├─► [CoAuthorEngine._update_state_post_chapter] ──► Chạy chuỗi if/elif khổng lồ ghi DB
       └─► [GitManager.commit_minor] ──► Chạy `git add .` (Nguy hiểm)
```

### 2. Các điểm nghẽn và khớp nối nguy hiểm (Dangerous Coupling & Bottlenecks)
1. **Khớp nối cứng (Tight Coupling) trong CoAuthorEngine**:
   - Tệp [coauthor_engine.py](file:///d:/tieu-thuyet/system/engines/coauthor_engine.py) dài gần 100KB (799 dòng). Nó đồng thời đóng vai trò: Orchestrator, Fixture Generator, Database Mutator, và Git Committer.
   - Hàm `_update_state_post_chapter` (dòng 145-680) chứa một chuỗi `elif chapter_num == 3: ... elif chapter_num == 22:` trực tiếp gõ lệnh SQL thô chèn hàng chục dòng vào `character_states`, `timeline_events`, `foreshadowing_ledger`. Khi tiểu thuyết đạt chương 100 hay 3.000, file này sẽ phình to lên hàng chục nghìn dòng, không thể bảo trì.
2. **Không có trừu tượng hóa mô hình AI (Model Provider Abstraction)**:
   - Tệp [router.py](file:///d:/tieu-thuyet/system/core/router.py#L64) trả về trực tiếp string tên model: `"pro"`, `"flash"`, `"flash_lite"`.
   - Không có interface chuẩn (`ModelProvider`, `ModelRequest`, `ModelResponse`). Nếu đổi từ Gemini API sang OpenAI, Claude, hoặc Local LLM (Ollama/vLLM), phải sửa đổi trực tiếp vào core routing.
3. **Phân mảnh nguồn sự thật (Duplicated State)**:
   - Thông tin nhân vật nằm rải rác ở 3 nơi: SQLite bảng `entities`, bảng `character_states`, và tệp JSON [canon/characters/minh_an.json](file:///d:/tieu-thuyet/canon/characters/minh_an.json).
   - [CharacterEngine.get_character](file:///d:/tieu-thuyet/system/engines/character_engine.py#L27-L32) đọc DB, sau đó đọc đè JSON file lên trên. Nếu DB cập nhật mà file JSON không cập nhật, dữ liệu sẽ lệch pha nghiêm trọng.
4. **Không có ngân sách Context thực tế (Context Budgeting)**:
   - [ContextBuilder.build_context_pack](file:///d:/tieu-thuyet/system/engines/context_builder.py) tuyên bố tối ưu token, nhưng trên thực tế chỉ dùng `LIMIT 5` hoặc `LIMIT 3` cứng nhắc. Khi một cảnh có 10 nhân vật xuất hiện, hệ thống sẽ chạy 10 vòng lặp SQL và không hề có cơ chế tính toán tổng độ dài token thực tế (`max_tokens_budget`) để cắt gọt thông minh theo mức độ ưu tiên.

---

## PHẦN B: KIỂM TRA AN NINH & RÒ RỈ BÍ MẬT (SECURITY & SECRET LEAKAGE)

### 1. Lỗ hổng P0: Rò rỉ bí mật tối hậu trong ContextBuilder
Tại [system/engines/context_builder.py](file:///d:/tieu-thuyet/system/engines/context_builder.py#L107-L111):
```python
cur.execute("""SELECT id, seed_description, actual_meaning FROM foreshadowing_ledger 
               WHERE status IN ('PLANTED', 'ACTIVE') AND planted_chapter <= ?
               ORDER BY planted_chapter DESC LIMIT 3""", (chapter_num,))
for r in cur.fetchall():
    pack["active_foreshadowing"].append({"id": r[0], "seed": r[1], "meaning": r[2]})
```
* **Mô tả hiểm họa**: Trường `actual_meaning` trong `foreshadowing_ledger` chứa đựng giải thích tối hậu của Tác giả (ví dụ: *“Nguyên lý sơ khai của con đường Khí Huyết Đạo tại Trái Đất bị phong ấn”*, *“Quy tắc Băng Phách của Lâm Tịch rò rỉ”*). Đoạn mã trên lấy trực tiếp `actual_meaning` và nạp thẳng vào `pack["active_foreshadowing"]` để truyền cho LLM viết văn!
* **Hậu quả**: LLM nhìn thấy toàn bộ âm mưu tương lai của tác giả và vô thức để lộ tình tiết qua suy nghĩ, độc thoại hoặc giọng kể trước thời điểm payoff hàng trăm chương.
* **Biện pháp khắc phục**: Tách biệt dứt khoát `AuthorForeshadowingRecord` (chứa `actual_meaning`, `payoff_notes`) và `WriterForeshadowingView` (chỉ chứa `seed_description`, `observable_clues`, `planted_chapter`).

### 2. Lỗ hổng P0: Bí mật tác giả & Database bị đưa lên Git và GitHub Pages
1. **Tệp `author_secret/` bị theo dõi bởi Git**:
   - `author_secret/secrets.json` và `author_secret/reveal_ledger.json` đã được commit trong lịch sử: commit `67290a9` và `09b3252`.
   - File `.gitignore` hiện tại **HOÀN TOÀN KHÔNG CÓ** dòng `author_secret/`!
   - Kiểm tra `git ls-tree origin/main` cho thấy cả thư mục `author_secret` và `database` đều tồn tại công khai trên nhánh từ xa.
2. **Triển khai GitHub Pages phơi bày toàn bộ repository**:
   - Tệp cấu hình [.github/workflows/deploy.yml](file:///d:/tieu-thuyet/.github/workflows/deploy.yml#L29-L31) cấu hình:
     ```yaml
     - name: Upload artifact
       uses: actions/upload-pages-artifact@v3
       with:
         path: '.'
     ```
   - Việc cấu hình `path: '.'` có nghĩa là toàn bộ thư mục gốc của repository (bao gồm `database/novel_os.db`, `author_secret/secrets.json`, mã nguồn backend `system/`) đều được đóng gói thành artifact web tĩnh. Bất kỳ ai truy cập `https://bon-231900.github.io/pha-troi/author_secret/secrets.json` đều có thể tải về toàn bộ bí mật tác giả nếu Pages đang chạy trên cấu hình này!
3. **Hardcode chuỗi bí mật trong mã nguồn Python**:
   - Tại [system/engines/knowledge_engine.py](file:///d:/tieu-thuyet/system/engines/knowledge_engine.py#L72):
     ```python
     if "chiến trường hạch tâm" in lower_text or "tần số ý chí không khuất phục" in lower_text:
         leaks.append(...)
     ```
   - Đoạn mã dùng để kiểm tra rò rỉ bí mật lại chứa chính... các cụm từ tuyệt mật được viết cứng bằng tiếng Việt trong code! Bất cứ ai đọc file `knowledge_engine.py` cũng biết ngay bí mật.
4. **Git Remote URL để lộ Personal Access Token (PAT)**:
   - Lệnh `git remote -v` cho thấy:
     `origin https://bon-231900:ghp_REDACTED_CREDENTIAL_TOKEN@github.com/bon-231900/pha-troi.git`
   - Token GitHub dạng `ghp_...` nằm lộ thiên trong cấu hình Git remote. Cần phải thu hồi (revoke) token này ngay lập tức trên tài khoản GitHub và chuyển sang dùng credential helper hoặc SSH key.

---

## PHẦN C: TOÀN VẸN DỮ LIỆU & MA TRẬN THẨM QUYỀN NGUỒN SỰ THẬT (DATA INTEGRITY & AUTHORITY MATRIX)

Hệ thống hiện tại có 4 hình thức lưu trữ: SQLite Database (`database/novel_os.db`), Tệp Markdown (`manuscript/markdown/`), Tệp JSON (`canon/`, `author_secret/`), và Tệp Word DOCX (`manuscript/word/`). Hiện chưa có quy định pháp lý rõ ràng về việc file nào có quyền quyết định tối cao nếu xảy ra sai lệch.

### Ma trận thẩm quyền kiến trúc đề xuất (Target Authority Matrix):
| Phân hệ (Domain) | Nguồn sự thật tối cao (Canonical Source) | Dữ liệu phái sinh (Derived State) | AI Writable? | Ghi chú vận hành |
| :--- | :--- | :--- | :---: | :--- |
| **Bản thảo (Manuscript)** | `manuscript/markdown/*.md` | FTS5 Index, Word DOCX, Reader JSON | **NO** | AI chỉ sinh Draft. Tác giả bấm Approve mới lưu Markdown. |
| **Canon Quy tắc & Thế giới quan** | `canon/rules/*.md` & `canon/**/*.json` | SQLite `canon_entries`, SQLite `world_nodes` | **NO** | Tuyệt đối không để AI sửa trực tiếp. Thay đổi qua Proposal. |
| **Bí mật tác giả (Author Vault)** | `author_secret/secrets.json` (Local Only) | Memory Cache (Read-only) | **NO** | Cách ly vật lý, không commit Git, không đưa vào context AI. |
| **Biến cố cốt truyện (Narrative Events)** | SQLite `narrative_events` | SQLite Projections, Snapshots | **NO** | AI đề xuất `ProposedEvent`. Chỉ Author duyệt mới chuyển thành Event. |
| **Trạng thái nhân vật (Character State)** | SQLite `narrative_events` (Replayable) | SQLite `character_states` (Projection) | **NO** | Không bao giờ chạy `UPDATE character_states` trực tiếp. |
| **Nhận thức nhân vật (Epistemic Matrix)** | SQLite `narrative_events` | SQLite `knowledge_matrix` (Projection) | **NO** | Nảy sinh từ biến cố nhận thức (`KNOWLEDGE_ACQUIRED`). |
| **Dòng thời gian (Timeline)** | SQLite `narrative_events` | SQLite `timeline_events` (Projection) | **NO** | Dự phóng theo trục thời gian thế giới (`world_chronology`). |
| **Phục bút (Foreshadowing Ledger)** | SQLite `foreshadowing_ledger` | Context Writer View (Sanitized) | **NO** | Quản lý độc lập giữa hạt mầm công khai và ý nghĩa ngầm. |
| **Tuyến truyện (Story Threads)** | SQLite `story_threads` | Báo cáo ngủ quên (`audit_dormant_threads`) | **NO** | Cập nhật qua biến cố tương tác tuyến. |
| **Đề xuất của AI (Proposals)** | SQLite `proposals` | None | **YES** | AI được quyền tạo đề xuất đề xuất thay đổi hoặc bổ sung. |
| **Bản nháp (Drafts)** | Memory / Temporary Staging Files | None | **YES** | AI có toàn quyền tạo và biên tập nháp trước khi kiểm duyệt. |
| **Phản biện & Đánh giá (Critique)** | SQLite `continuity_errors` / In-memory | Telemetry Logs | **YES** | Các động cơ phân tích kết quả tự động ghi nhận phát hiện. |

---

## PHẦN D: KIỂM THỬ & CÁCH LY MÔI TRƯỜNG (TESTING & ISOLATION)

### 1. Phá hoại cơ sở dữ liệu thật trong quá trình chạy Unit Test
Kiểm tra tệp [tests/test_narrative_suite.py](file:///d:/tieu-thuyet/tests/test_narrative_suite.py#L25) và [tests/test_3000_upgrade_suite.py](file:///d:/tieu-thuyet/tests/test_3000_upgrade_suite.py#L30):
- Cả hai bộ test đều khởi tạo:
  ```python
  cls.db_path = DB_PATH  # Trỏ thẳng vào "database/novel_os.db"!
  ```
- Trong `test_02_dead_character_appears`:
  ```python
  cur.execute("INSERT OR REPLACE INTO entities (id, name, type, status) VALUES ('char_dead_npc', 'Trần Văn Chết', 'character', 'DEAD')")
  conn.commit()
  ```
- Trong `test_20_long_term_continuity_consistency` và `test_21_long_form_memory_simulation`:
  - Thêm vĩnh viễn sự kiện giả lập `EVT-CH100`, sự kiện phục bút giả `FSH-SIM-A`, nhân vật giả `char_ally_d` vào cơ sở dữ liệu sản xuất!
- Trong `test_3000_upgrade_suite.py`:
  - Tạo tuyến truyện giả `TH-TEST-DORMANT` và không hề dọn dẹp (teardown).
* **Hậu quả chí mạng**: Mỗi lần chạy `pytest` hoặc `unittest`, cơ sở dữ liệu thật của tiểu thuyết bị ô nhiễm hàng chục bản ghi rác của NPC thử nghiệm, phá hỏng tính thiêng liêng của Canon!

### 2. Sự phụ thuộc cứng vào hệ điều hành và đường dẫn cục bộ
- Trong [system/core/config.py](file:///d:/tieu-thuyet/system/core/config.py#L8):
  `ROOT_DIR = r"d:\tieu-thuyet"`
- Trong [system/reader_app/build_static.py](file:///d:/tieu-thuyet/system/reader_app/build_static.py#L12):
  `BASE_DIR = r"d:\tieu-thuyet"`
- Trong [scripts/upgrade_schema_3000.py](file:///d:/tieu-thuyet/scripts/upgrade_schema_3000.py#L13):
  `DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"`
* **Hậu quả**: Toàn bộ dự án sẽ gãy sụp lập tức nếu chạy trên máy của cộng sự khác, trên môi trường Linux CI/CD của GitHub Actions, hoặc khi di chuyển thư mục sang ổ đĩa khác.
* **Yêu cầu sửa đổi**: Thay thế bằng `Path(__file__).resolve().parent.parent...` hoặc biến môi trường `NOVEL_OS_ROOT`.

---

## PHẦN E: RANH GIỚI AI & TÁCH BIỆT NHẬN THỨC (AI BOUNDARIES & EPISTEMIC SEPARATION)

### 1. Phân định rõ quyền hạn của AI
Hệ thống V2 phải tuân thủ nghiêm ngặt nguyên lý: **AI là Trợ thủ / Người quan sát (Observer / Proposer / Drafter), KHÔNG PHẢI là Thẩm phán hay Đấng sáng tạo tối cao (Canonical Authority).**

```
┌────────────────────────────────────────────────────────┐
│                        AI LAYER                        │
│  - Đọc: Context Pack (đã được lọc sạch bí mật)         │
│  - Tạo: Draft, Suggested Diff, Critique Signals         │
│  - Đề xuất: ProposedEvent, ProposedCanon, ProposedFix  │
└──────────────────────────┬─────────────────────────────┘
                           │ (Chỉ gửi đề xuất)
                           ▼
┌────────────────────────────────────────────────────────┐
│               DETERMINISTIC VALIDATOR                  │
│  - So khớp với Bộ luật Canon đã khóa (NOVEL_LOCK)      │
│  - Kiểm tra tính đơn điệu của dòng thời gian            │
│  - Kiểm tra ranh giới nhận thức của nhân vật           │
└──────────────────────────┬─────────────────────────────┘
                           │ (Chỉ khi hợp lệ)
                           ▼
┌────────────────────────────────────────────────────────┐
│                 AUTHOR APPROVAL GATE                   │
│  - Tác giả duyệt đề xuất qua CLI / Studio UI           │
│  - Thẩm định rủi ro phân nhánh cốt truyện              │
└──────────────────────────┬─────────────────────────────┘
                           │ (Sau khi tác giả duyệt)
                           ▼
┌────────────────────────────────────────────────────────┐
│             TRANSACTIONAL CANON UPDATE                 │
│  - Ghi NarrativeEvent vào Event Store                  │
│  - Cập nhật các bảng Projection                        │
│  - Tạo Git Transaction Commit có chữ ký tác giả        │
└────────────────────────────────────────────────────────┘
```

### 2. Sự hạn chế của RevisionEngine hiện tại
Hiện tại, [system/engines/revision_engine.py](file:///d:/tieu-thuyet/system/engines/revision_engine.py) chỉ có đúng 14 dòng:
```python
if iss.get("category") == "STYLE":
    refined_text = re.sub(r'(?i)và hắn không biết rằng[,:]?', '', refined_text)
    refined_text = re.sub(r'(?i)hắn vĩnh viễn không thể ngờ được[,:]?', '', refined_text)
```
- Sử dụng `re.sub` tự động xóa chuỗi trong bản thảo sẽ gây lỗi ngữ pháp (thừa dấu phẩy, câu mất vị ngữ, lủng củng).
- Không cung cấp **Diff** trực quan cho tác giả thấy trước và sau khi sửa.
- Không thể hoàn tác (undo/rollback) một lần sửa nếu kết quả làm mất phong cách văn học.

---

## PHẦN F: AN TOÀN GIT & TRIỂN KHAI GITHUB PAGES (GIT SAFETY & DEPLOYMENT BOUNDARY)

### 1. Nguy cơ tiềm ẩn từ `git add .` trong tự động hóa
Kiểm tra [system/core/git_manager.py](file:///d:/tieu-thuyet/system/core/git_manager.py#L40-L45):
```python
def commit_minor(self, message: str, files: list = None) -> tuple[bool, str]:
    if files:
        for f in files:
            self._run_git(["add", f])
    else:
        self._run_git(["add", "."])  # CỰC KỲ NGUY HIỂM
```
- Khi `CoAuthorEngine` hoàn tất một chương, nó gọi `self.git_manager.commit_minor(...)` mà không truyền tham số `files`.
- Lệnh `git add .` lập tức quét toàn bộ thư mục gốc, bao gồm các tệp tạm trong `scratch/`, tệp ghi đè `database/novel_os.db`, và nếu ai đó vừa tạo file ghi chú trong `author_secret/`, nó cũng bị nạp vào git index và commit lên lịch sử phiên bản vĩnh viễn!
- **Yêu cầu V2**: Loại bỏ hoàn toàn `git add .` trong toàn bộ code tự động. Mọi giao dịch Git phải có danh sách tệp tường minh (`explicit manifest`).

### 2. Lỗi kiến trúc triển khai Reader Static Web
1. Tệp [system/reader_app/build_static.py](file:///d:/tieu-thuyet/system/reader_app/build_static.py#L13) chỉ quét:
   `MANUSCRIPT_DIR = os.path.join(BASE_DIR, "manuscript", "markdown", "volume_01", "arc_01")`
   - Bỏ sót hoàn toàn các chương từ 47 đến 57 nằm trong thư mục `arc_02`!
2. Workflow GitHub Actions [.github/workflows/deploy.yml](file:///d:/tieu-thuyet/.github/workflows/deploy.yml) triển khai thư mục gốc thay vì thư mục `dist/`.
- **Yêu cầu V2**:
  - Tách bạch tuyệt đối: Quá trình build đọc bản thảo đã duyệt $\rightarrow$ xuất ra `system/reader_app/dist/` (chỉ chứa HTML, CSS, JS tĩnh và các JSON chương đã làm sạch, tuyệt đối không có DB, vault hay code Python).
  - GitHub Pages chỉ deploy duy nhất thư mục `dist/`.

---

## PHẦN G: THIẾT KẾ MÔ HÌNH NARRATIVE EVENT & PROJECTION (EVENT-DRIVEN STATE ARCHITECTURE)

Để hệ thống vận hành bền vững qua 3.000 chương mà không bị sai lệch dữ liệu do cập nhật đè (destructive updates), V2 sẽ chuyển đổi lõi quản trị trạng thái sang mô hình **Event Sourcing & Projections**.

### 1. Định nghĩa thực thể `NarrativeEvent`
Thay vì `UPDATE character_states SET cultivation_realm = ...`, mọi biến động trong thế giới tiểu thuyết đều được ghi nhận như một sự kiện lịch sử bất biến (immutable event):

```json
{
  "event_id": "EVT-20261007-0042-01",
  "transaction_id": "TX-01JC8Q9X8...",
  "chapter_num": 42,
  "scene_num": 2,
  "event_type": "ITEM_ACQUIRED",
  "actor_id": "char_minh_an",
  "target_id": "item_hac_thiet_doan_con",
  "payload": {
    "item_name": "Hắc Thiết Đoản Côn",
    "origin": "Lò rèn của chú Bảy thợ sắt Bình Thạnh",
    "weight_kg": 4.5,
    "material": "Sắt vụn phế liệu gia công nhiệt",
    "spiritual_status": "Vật phẩm phàm trần không có linh khí"
  },
  "source": "MANUSCRIPT_PARSE",
  "confidence": 1.0,
  "approved_by": "Author",
  "created_at": "2026-09-15T14:30:00Z"
}
```

### 2. Danh mục Event Types cơ bản (Core Narrative Events):
* `CHARACTER_CREATED`: Nhân vật mới xuất hiện.
* `CHARACTER_STATE_CHANGED`: Thay đổi cảm xúc, thể lực, thương tổn.
* `CHARACTER_DIED`: Nhân vật tử vong vĩnh viễn (kích hoạt luật Khóa Tử Vong).
* `LOCATION_ENTERED` / `LOCATION_LEFT`: Di chuyển địa lý.
* `ITEM_ACQUIRED` / `ITEM_LOST` / `ITEM_USED`: Biến động túi đồ.
* `KNOWLEDGE_ACQUIRED` / `KNOWLEDGE_CHANGED`: Chuyển đổi trạng thái nhận thức (`UNKNOWN -> SUSPECTED -> KNOWN`).
* `RELATIONSHIP_CHANGED`: Tăng giảm chỉ số nhận thức tình cảm / hảo cảm / thù địch.
* `POWER_CHANGED`: Tiến cảnh, suy giảm hoặc tổn hại đạo cơ.
* `THREAD_TOUCHED` / `THREAD_RESOLVED`: Tiến trình tuyến truyện.
* `FORESHADOWING_PLANTED` / `FORESHADOWING_PAYOFF`: Vòng đời phục bút.

### 3. Mô hình Dự phóng (Projection Model)
Bảng `character_states`, `knowledge_matrix`, `timeline_events` hiện tại sẽ trở thành **Read Projections**:
- Nếu phát hiện trạng thái nhân vật bị mâu thuẫn ở chương 250, tác giả chỉ cần kiểm tra chuỗi sự kiện `narrative_events` liên quan đến nhân vật đó từ chương 1 đến 250.
- Nếu schema bảng trạng thái thay đổi trong tương lai, toàn bộ cơ sở dữ liệu trạng thái hiện tại có thể được **tái tạo lại hoàn chỉnh 100% (Rebuild Projection)** từ đầu mà không làm mất lịch sử tác phẩm!

---

## PHẦN H: LỘ TRÌNH TRIỂN KHAI TỪNG BƯỚC (INCREMENTAL MIGRATION ROADMAP: PHASE 1 – PHASE 9)

Tuân thủ nguyên tắc **Tối Cao số 2 và số 8**: Tuyệt đối không xóa viết lại toàn bộ; áp dụng mẫu Facade/Adapter, nâng cấp tuần tự có kiểm thử và đường lùi.

```mermaid
graph TD
    P0[Phase 0: Read Only Audit] --> P1[Phase 1: P0 Security & Leak Fixes]
    P1 --> P2[Phase 2: Authority Matrix & Path Portability]
    P2 --> P3[Phase 3: NarrativeEvent Store & Character Migration]
    P3 --> P4[Phase 4: Knowledge Epistemic & Timeline Engine]
    P4 --> P5[Phase 5: Relationships & Inventory Engine]
    P5 --> P6[Phase 6: Threads & Foreshadowing Redesign]
    P6 --> P7[Phase 7: CoAuthor Orchestration & Model Adapter]
    P7 --> P8[Phase 8: Test Suite Isolation & Benchmark]
    P8 --> P9[Phase 9: Documentation, ADR & Cleanup]
```

### Chi tiết kế hoạch từng giai đoạn:

#### GIAI ĐOẠN 1: AN NINH P0 & CÁCH LY BÍ MẬT (PHASE 1)
- **Mục tiêu**: Bịt kín toàn bộ điểm rò rỉ bí mật sang AI context, bảo vệ Git và GitHub Pages.
- **Hành động cụ thể**:
  1. Cập nhật [.github/workflows/deploy.yml](file:///d:/tieu-thuyet/.github/workflows/deploy.yml) chỉ xuất bản artifact từ thư mục `system/reader_app/dist/`.
  2. Bổ sung `author_secret/` vào `.gitignore`. Hướng dẫn tác giả phương án thu hồi GitHub Token bị lộ và kế hoạch làm sạch lịch sử Git (nếu tác giả duyệt).
  3. Tái cấu trúc [system/engines/context_builder.py](file:///d:/tieu-thuyet/system/engines/context_builder.py): Xóa triệt để việc query cột `actual_meaning` vào context AI; tạo lớp view an toàn `WriterForeshadowingView`.
  4. Viết Unit test `test_secret_leak_protection.py` chứng minh không có bất kỳ chuỗi bí mật nào lọt vào AI context pack.

#### GIAI ĐOẠN 2: MA TRẬN THẨM QUYỀN & CHUẨN HÓA ĐƯỜNG DẪN (PHASE 2)
- **Mục tiêu**: Xóa bỏ các đường dẫn cứng `d:\tieu-thuyet`, xác lập pháp lý nguồn dữ liệu.
- **Hành động cụ thể**:
  1. Refactor [system/core/config.py](file:///d:/tieu-thuyet/system/core/config.py) sử dụng `pathlib.Path(__file__).resolve().parent.parent` có hỗ trợ biến môi trường `NOVEL_OS_ROOT`. Đảm bảo chạy mượt mà trên cả Windows và Linux CI.
  2. Xuất bản tài liệu kiến trúc chính thức `docs/ARCHITECTURE_AUTHORITY_MATRIX.md`.

#### GIAI ĐOẠN 3: NỀN MÓNG NARRATIVE EVENT & MIGRATION NHÂN VẬT (PHASE 3)
- **Mục tiêu**: Thiết lập bảng sự kiện `narrative_events` và kiểm nghiệm mô hình projection trên thực thể Character.
- **Hành động cụ thể**:
  1. Tạo bảng `narrative_events` trong SQLite schema và bổ sung script migration an toàn.
  2. Xây dựng `CharacterProjection` để tính toán trạng thái hiện thời của nhân vật từ event log.
  3. Chuyển đổi dữ liệu 57 chương hiện tại của nhân vật chính (`Minh An`, `Lâm Tịch`) sang chuỗi NarrativeEvent hạt nhân.
  4. Chạy đối soát (diff check) giữa state cũ và state sinh ra từ projection để đảm bảo độ trùng khớp 100%.

#### GIAI ĐOẠN 4: NÂNG CẤP KNOWLEDGE & DÒNG THỜI GIAN ĐA CHIỀU (PHASE 4)
- **Mục tiêu**: Loại bỏ kiểm tra bằng từ khóa thô sơ, hỗ trợ Flashback và dòng thời gian phi tuyến tính.
- **Hành động cụ thể**:
  1. Cấu trúc hóa `KnowledgeEngine` theo bộ 3 `(Subject, Predicate, Object)` kèm trạng thái nhận thức rõ ràng, không phụ thuộc vào chuỗi từ khóa cứng.
  2. Cải tạo [system/engines/timeline_engine.py](file:///d:/tieu-thuyet/system/engines/timeline_engine.py): Hỗ trợ các chế độ thời gian `LINEAR`, `FLASHBACK`, `PARALLEL`, `DREAM`, `VISION`, `TIME_SKIP`. Loại bỏ khối `except Exception: pass`.

#### GIAI ĐOẠN 5: QUAN HỆ NHÂN VẬT & TÚI ĐỒ (PHASE 5)
- **Mục tiêu**: Đưa quản lý túi đồ và quan hệ tình cảm cực chậm (Slow Burn) vào kiểm duyệt tất định.
- **Hành động cụ thể**:
  1. Bổ sung các event `ITEM_ACQUIRED`, `ITEM_LOST`, `RELATIONSHIP_INTERACTION`.
  2. Liên kết `CritiqueEngine` với bảng trạng thái túi đồ thời điểm chương đó để ngăn chặn triệt để lỗi "đột nhiên rút bảo kiếm từ không khí".

#### GIAI ĐOẠN 6: CẢI TẠO TUYẾN TRUYỆN & SỔ CÁI PHỤC BÚT (PHASE 6)
- **Mục tiêu**: Sửa lỗi sắp xếp ưu tiên tuyến truyện, hỗ trợ phục bút trường thiên 500+ chương.
- **Hành động cụ thể**:
  1. Trong `StoryThreadEngine`: Chuyển trường `urgency` và `importance` sang điểm số nguyên (`CORE=4, MAJOR=3, MINOR=2, BACKGROUND=1`) để lệnh SQL `ORDER BY urgency DESC` hoạt động chính xác tuyệt đối.
  2. Trong `ForeshadowingEngine`: Bổ sung khái niệm `payoff_window`, `long_arc`, `planned_dormancy`, `latest_safe_revisit` thay vì chỉ dùng ngưỡng cứng 50 chương.

#### GIAI ĐOẠN 7: TÁCH COAUTHOR ORCHESTRATION & MODEL ADAPTER (PHASE 7)
- **Mục tiêu**: Dọn dẹp 600 dòng code cứng trong `CoAuthorEngine`, tích hợp cơ chế Proposal thực thụ.
- **Hành động cụ thể**:
  1. Trích xuất toàn bộ dữ liệu mẫu chương 1-22 ra tệp `database/fixtures/bootstrap_chapters_1_22.json`.
  2. Thiết kế mẫu `ModelAdapter` (`BaseModelProvider`, `GeminiProvider`, `OpenAICompatibleProvider`) cho `TaskRouter`.
  3. Nâng cấp [ProposalManager](file:///d:/tieu-thuyet/system/engines/proposal_manager.py): Khi tác giả gọi `approve_proposal()`, hệ thống tự động sinh `NarrativeEvent`, cập nhật projection, và chuẩn bị commit manifest an toàn.
  4. Cải tạo `RevisionEngine` sinh patch dạng Diff trực quan thay vì regex mù.

#### GIAI ĐOẠN 8: CÁCH LY UNIT TEST, INDEXES & BENCHMARK THỰC NGHIỆM (PHASE 8)
- **Mục tiêu**: Bảo vệ tuyệt đối DB sản xuất, tăng tốc độ truy vấn cho quy mô 3.000 chương.
- **Hành động cụ thể**:
  1. Tái cấu trúc toàn bộ `tests/`: Tất cả test case kế thừa từ fixture tạo cơ sở dữ liệu SQLite trong bộ nhớ tạm (`:memory:`) hoặc file temp `test_novel_os.db` được xóa sạch sau khi teardown. Cấm tuyệt đối chạm vào `database/novel_os.db`.
  2. Bổ sung đầy đủ 7 chỉ mục SQL quan trọng cho `character_states`, `knowledge_matrix`, `timeline_events`, `foreshadowing_ledger`.
  3. Gắn nhãn rõ ràng cho bộ benchmark 3.000 chương là `SYNTHETIC BENCHMARK`.
  4. Sửa `GitManager`: Loại bỏ hoàn toàn `git add .`, bắt buộc truyền `manifest` danh sách tệp.

#### GIAI ĐOẠN 9: TỔNG KẾT TÀI LIỆU, LÀM SẠCH & CHUẨN BỊ VẬN HÀNH (PHASE 9)
- **Mục tiêu**: Đồng bộ toàn bộ tài liệu kiến trúc, đóng gói release V2.
- **Hành động cụ thể**:
  1. Cập nhật đầy đủ `README.md`, `ARCHITECTURE.md`, `WORKFLOW.md`, `DECISIONS.md`.
  2. Viết các ADR giải trình kiến trúc trong `docs/adr/`.
  3. Đảm bảo toàn bộ test suite pass 100% với 0 regression.

---

## PHẦN I: MA TRẬN ĐÁNH GIÁ RỦI RO & CƠ CHẾ HOÀN TÁC (RISK ASSESSMENT & ROLLBACK MATRIX)

| Phân loại | Mã rủi ro | Mô tả sự cố | Mức độ tác động | Giải pháp ngăn chặn / Giảm thiểu | Quy trình hoàn tác (Rollback Protocol) |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Bảo mật** | `RSK-SEC-01` | Lộ bí mật qua GitHub Pages | **P0** | Ngay lập tức sửa `.github/workflows/deploy.yml` chỉ trỏ vào `dist/`. | Rollback workflow commit về bản an toàn; gỡ artifact trên GitHub Actions. |
| **Bảo mật** | `RSK-SEC-02` | Rò rỉ `actual_meaning` vào LLM | **P0** | Bỏ trường `actual_meaning` khỏi `ContextBuilder`. Chỉ cho phép đọc `WriterForeshadowingView`. | Revert thay đổi trong `context_builder.py`; bản thảo nháp chưa duyệt thì chưa ảnh hưởng canon. |
| **Bảo mật** | `RSK-SEC-03` | Token cá nhân lộ trên Git remote | **P0** | Thu hồi token trên GitHub; xóa token khỏi url remote cục bộ. | Không ảnh hưởng đến dữ liệu tiểu thuyết; chỉ cấu hình lại remote URL. |
| **Dữ liệu** | `RSK-DAT-01` | Mất mát/sai lệch DB khi migrate | **P1** | Sao lưu vật lý `novel_os.db` thành `novel_os.db.bak_{timestamp}` trước mỗi thao tác schema. | Khôi phục trực tiếp từ file backup; kiểm tra mã băm SHA256. |
| **Dữ liệu** | `RSK-DAT-02` | Projection lệch pha so với lịch sử | **P1** | Viết script đối soát song song (dual-run validator) so khớp từng trường dữ liệu. | Giữ nguyên bảng cũ, chỉ đọc từ bảng cũ cho đến khi projection đạt 100% khớp. |
| **Vận hành** | `RSK-OPS-01` | `git add .` vô tình stage file rác | **P0** | Xóa hoàn toàn `git add .` trong mã nguồn; dùng tệp manifest tường minh. | Lệnh `git restore --staged .` trước khi bất kỳ commit tự động nào được kích hoạt. |
| **Kiểm thử** | `RSK-TST-01` | Test làm bẩn cơ sở dữ liệu thật | **P1** | Đổi toàn bộ test sang dùng temp SQLite database, chặn cứng đường dẫn DB sản xuất trong test. | Khôi phục lại DB từ snapshot git sạch (`git checkout database/novel_os.db`). |

---

## KẾT LUẬN & KIẾN NGHỊ

Hệ thống **Phá Trời Novel OS** đã có nền móng ý tưởng rất sâu sắc về cấu trúc tự sự và tu tiên hiện đại. Việc thực hiện đợt tái thiết V2 theo lộ trình trên sẽ biến dự án thành một pháo đài kiến trúc bền bỉ, giúp Tác giả hoàn toàn an tâm sáng tác từ chương 58 đến chương 3.000 mà không bao giờ phải lo sợ việc rò rỉ bí mật, lệch dòng thời gian, hay sập gãy dữ liệu.

**BƯỚC TIẾP THEO (NEXT STEP)**:  
Dừng toàn bộ thao tác sửa code (STOP) để Tác giả thẩm định báo cáo này. Khi Tác giả phê duyệt báo cáo và cho phép bắt đầu, hệ thống sẽ mở màn thực hiện **Phase 1: P0 Security & Secret Isolation**.

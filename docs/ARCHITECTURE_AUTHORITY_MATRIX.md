# MA TRẬN THẨM QUYỀN KIẾN TRÚC: PHÁ TRỜI NOVEL OS
**Tài liệu**: `docs/ARCHITECTURE_AUTHORITY_MATRIX.md`  
**Phiên bản**: V2 (Áp dụng cho quy mô 3.000+ chương)  
**Trạng thái**: BAN HÀNH CHÍNH THỨC  
**Nguyên tắc cốt lõi**: Phân định ranh giới nguồn sự thật, quyền hạn của Tác giả, và giới hạn bất khả xâm phạm của AI.

---

## 1. NGUYÊN TẮC THẨM QUYỀN BẤT BIẾN (CANONICAL INVARIANTS)

1. **Tác Giả Là Thẩm Thẩm Quyền Tối Cao (Author Authority)**:
   - Mọi thực thể thế giới, diễn biến cốt truyện và quy tắc tu chân chỉ trở thành Canon khi có sự phê duyệt tường minh của Tác giả (`approved_by = 'Author'`).
2. **AI Không Phải Nguồn Sự Thật (AI is Not Canonical Authority)**:
   - AI đóng vai trò **Người quan sát, Đề xuất và Soạn thảo nháp** (`Observer -> Proposer -> Drafter`).
   - Tuyệt đối không có bất kỳ luồng ngầm nào cho phép AI tự động cập nhật hoặc ghi đè trạng thái Canon mà không qua cổng kiểm duyệt của Tác giả.
3. **Bí Mật Tác Giả Là Vùng Cấm Tuyệt Đối (Author Vault Isolation)**:
   - Thư mục `author_secret/` là tài sản riêng tư cục bộ, không bao giờ được đưa vào Git remote, context của AI viết văn, hay bản build công khai của độc giả.

---

## 2. MA TRẬN THẨM QUYỀN THEO TỪNG PHÂN HỆ (AUTHORITY MATRIX)

| Phân hệ (Domain) | Nguồn Sự Thật Tối Cao (Canonical Source) | Dữ Liệu Phái Sinh (Derived State / Projections) | AI Có Quyền Ghi? (AI Writable?) | Quy Tắc Kiểm Soát & Giới Hạn |
| :--- | :--- | :--- | :---: | :--- |
| **Bản Thảo (Manuscript)** | `manuscript/markdown/**/*.md` | FTS5 BM25 Index, Word DOCX, Reader JSON | **NO** | AI chỉ tạo bản nháp tạm thời (Draft). Chỉ khi Tác giả duyệt thì file Markdown mới được ghi. |
| **Quy Tắc Canon (Canon Rules)** | `canon/rules/*.md` | SQLite `canon_entries` | **NO** | Cấm AI sửa đổi trực tiếp. Mọi thay đổi phải qua `ProposalManager` và được Tác giả duyệt. |
| **Bối Cảnh Thế Giới (Cosmology & World)** | `canon/world/*.json`, `canon/cosmology/*.json` | SQLite `world_nodes`, `world_edges` | **NO** | Bản đồ vũ trụ và địa danh được khóa theo phân tầng hiện thực và siêu nhiên. |
| **Bí Mật Tác Giả (Author Secrets)** | `author_secret/secrets.json` (Local Only) | Bộ nhớ tạm (Memory Cache, Read-only) | **NO** | Cách ly vật lý. Bị loại khỏi Git, Context AI, và Reader. Chỉ dùng kiểm tra rò rỉ thụ động. |
| **Biến Cố Tự Sự (Narrative Events)** | SQLite `narrative_events` | SQLite Projections, Lịch sử tái dựng | **NO** | AI chỉ tạo `ProposedEvent`. Chỉ Tác giả phê duyệt mới chuyển thành Event chính thức. |
| **Trạng Thái Nhân Vật (Character State)** | SQLite `narrative_events` (Replayable) | SQLite `character_states` (Projection) | **NO** | Trạng thái là kết quả dự phóng từ các sự kiện trong quá khứ. Cấm sửa đè trực tiếp. |
| **Ma Trận Nhận Thức (Epistemic Matrix)** | SQLite `narrative_events` | SQLite `knowledge_matrix` (Projection) | **NO** | Quản lý 7 trạng thái nhận thức (`KNOWN`, `SUSPECTED`, `BELIEVED`, `MISUNDERSTOOD`, `FALSE_BELIEF`, `UNKNOWN`, `FORGOTTEN`). |
| **Dòng Thời Gian (Timeline)** | SQLite `narrative_events` | SQLite `timeline_events` (Projection) | **NO** | Phân tách thứ tự chương (`chapter_order`) và niên đại vũ trụ (`world_chronology`). Hỗ trợ Flashback, Parallel. |
| **Phục Bút (Foreshadowing)** | SQLite `foreshadowing_ledger` | Context Writer View (Sanitized) | **NO** | Phân tách `AuthorForeshadowingRecord` (chứa ý nghĩa tối hậu) và `WriterForeshadowingView` (chỉ manh mối quan sát). |
| **Tuyến Cốt Truyện (Story Threads)** | SQLite `story_threads` | Báo cáo ngủ quên (`audit_dormant_threads`) | **NO** | Điểm ưu tiên số hóa (`CORE=4, MAJOR=3, MINOR=2, BACKGROUND=1`). |
| **Đề Xuất Cải Tiến (Proposals)** | SQLite `proposals` | None | **YES** | AI có toàn quyền tạo đề xuất kèm phân tích rủi ro và các phương án thay thế. |
| **Bản Soạn Thảo (Drafts)** | Memory / Temp Files | None | **YES** | AI tạo văn xuôi nháp để gửi sang khâu Phản biện (Critique). |
| **Phản Biện (Critique & Errors)** | SQLite `continuity_errors` | Telemetry Logs | **YES** | Động cơ kiểm tra tự động phát hiện lỗi và cảnh báo cho Tác giả. |
| **Sản Phẩm Độc Giả (Public Reader)** | `system/reader_app/dist/` | Static HTML, CSS, JS, Clean JSON | **NO** | Được tạo tự động bởi pipeline `generate_static_site`, kiểm toán bởi `verify_public_dist.py`. |

---

## 3. LUỒNG THỰC THI CHUẨN TỪ ĐỀ XUẤT ĐẾN CANON (THE CANONICAL TRANSITION PIPELINE)

Mọi thay đổi đối với trạng thái thế giới hoặc bản thảo phải tuân thủ quy trình bất biến:

```text
[1. AI Đề Xuất / Soạn Thảo]
         │
         ▼
[2. Kiểm Tra Tất Định (Critique Engine)] ──► Phát hiện lỗi liên tục / Rò rỉ bí mật
         │
         ▼
[3. Tạo Đề Xuất (Proposal / Proposed Event)] ──► Lưu trữ trạng thái PENDING
         │
         ▼
[4. Phê Duyệt Của Tác Giả (Author Gate)]
   ├── Tác giả TỪ CHỐI  ──► Proposal = REJECTED (Dừng luồng)
   └── Tác giả PHÊ DUYỆT ──► Proposal = APPROVED
                                  │
                                  ▼
[5. Đột Biến Canon (Canonical Mutation)]
   ├── Ghi NarrativeEvent vào Event Store
   ├── Cập nhật các bảng Projection tương ứng
   └── Xuất bản thảo Markdown đã duyệt
         │
         ▼
[6. Giao Dịch Git Minh Bạch (Git Manifest Transaction)]
   └── Commit chính xác danh sách tệp thay đổi, không chạy "git add ."
```

---

## 4. QUY ĐỊNH AN TOÀN DỮ LIỆU & KIỂM THỬ

1. **Bảo tồn cơ sở dữ liệu thật**:
   - Mọi bài kiểm thử Unit test và mô phỏng benchmark phải chạy trên cơ sở dữ liệu SQLite in-memory (`:memory:`) hoặc tệp tạm (`test_*.db`). Tuyệt đối cấm kết nối và ghi dữ liệu rác vào `database/novel_os.db`.
2. **Tính độc lập với môi trường**:
   - Mọi đoạn mã phải sử dụng đường dẫn tương đối hoặc biến môi trường `NOVEL_OS_ROOT`. Cấm hardcode ký tự ổ đĩa của môi trường phát triển cục bộ.
3. **Phân phối công khai sạch**:
   - Thư mục `dist/` trước khi đưa lên GitHub Pages phải được xác minh 100% bằng script `scripts/verify_public_dist.py`.

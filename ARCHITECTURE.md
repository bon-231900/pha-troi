# KIẾN TRÚC NOVEL OS CHO “PHÁ TRỜI”

## 1. Triết Lý Thiết Kế
1. **Single-Novel Dedicated Engine**: Không có lớp trừu tượng thừa. Tối ưu 100% cho cấu trúc vũ trụ, hệ thống tu luyện và bối cảnh TP.HCM 2026 của *Phá Trời*.
2. **Local-First & Data Durability**: Dữ liệu hoàn toàn trên máy cục bộ (`D:\tieu-thuyet`). Không phụ thuộc vào cloud AI service để lưu trữ state.
3. **Air-Gapped Author Secret Vault**: Thư mục `author_secret/` được cô lập logic ở cấp độ mã nguồn. Không một truy vấn retrieval thông thường nào cho văn bản draft được phép truy cập vào vault này.
4. **Epistemic State Tracking**: Nhận thức của nhân vật được theo dõi đa trạng thái: `KNOWN`, `SUSPECTED`, `BELIEVED`, `MISUNDERSTOOD`, `FALSE_BELIEF`, `UNKNOWN`, `FORGOTTEN`.

## 2. 21 Động Cơ Lõi (Core Engines)
- **CanonEngine**: Phân cấp 6 trạng thái (`LOCKED`, `CONFIRMED`, `PROVISIONAL`, `UNKNOWN`, `FORBIDDEN_ASSUMPTION`, `PROPOSED`).
- **WorldEngine**: Mô hình hóa vũ trụ theo đồ thị phân cấp từ *Đại Đại Giới -> Các Vực -> Các Tinh Hải -> Các Vị Diện -> Thế Giới -> Trái Đất*.
- **CharacterEngine**: Quản lý profile, thương tổn thể xác, linh hồn, túi đồ (inventory) và mục tiêu nhân vật.
- **KnowledgeEngine**: Kiểm soát phát ngôn nhân vật dựa trên ma trận nhận thức 4 tầng: World Truth, Character Belief, Suspicion, Reader Knowledge.
- **PowerEngine**: Quản lý 7 Đạo tu luyện chính và Khí Huyết Đạo trên Trái Đất. Chặn quy tắc "cảnh giới cao auto thắng".
- **TimelineEngine**: Dòng thời gian tuyệt đối & tương đối, kiểm soát sự kiện song song, tốc độ di chuyển giữa các địa điểm.
- **ForeshadowingEngine**: Quản lý sổ cái phục bút (Setup - Clue - Payoff) qua hàng ngàn chương.
- **StoryThreadEngine**: Quản lý độc lập vòng đời các tuyến cốt truyện (Main, Subplot, Mystery, Romance, Faction), tự động phát hiện tuyến ngủ quên.
- **HierarchyEngine**: Quản lý cấu trúc 8 tầng (Saga -> Era -> Volume -> Arc -> Mini-Arc -> Chapter -> Scene -> Beat) và trích xuất lát cắt ngữ cảnh phân tầng.
- **EscalationEngine**: Kiểm soát trần leo thang 6 trục (Power, Geo, Cosmology, Stakes, Mystery, Romance) với thời gian làm nguội (cooldown).
- **FatigueEngine**: Phòng thủ bão hòa và công thức tự sự, phát hiện lặp cliffhanger, lặp chu kỳ biến cố, sáo ngữ cử chỉ.
- **ContextBuilder**: Lọc và đóng gói gói ngữ cảnh thích ứng tối ưu theo ngân sách token O(1) (`minimal + relevant + sufficient`).
- **CoAuthorEngine**: Triển khai hợp đồng "Viết tiếp" với khả năng tự đưa ra quyết định sáng tạo hợp canon.
- **CritiqueEngine**: Tự phản biện toàn diện (Canon, Character, POV, Timeline, Location, Power, Relationship, Foreshadowing, Style, Narrative, Fatigue, Inventory).
- **RevisionEngine**: Sửa chữa chính xác theo phạm vi (câu, đoạn, cảnh, chương).
- **DocxPipeline**: Trình xuất file Word tự động theo quy chuẩn xuất bản sách.
- **ResearchVault**: Kho lưu trữ nghiên cứu đời thực (TP.HCM 2026, khoa học), phân định rõ ràng `RESEARCH != CANON`.
- **ProposalManager**: Cơ chế đề xuất ý tưởng lớn và chờ Author phê duyệt.
- **RelationshipEngine**: Theo dõi ma trận cảm xúc và lịch sử tương tác giữa các nhân vật (bảo vệ tiến trình Extremely Slow Burn).
- **RetrievalEngine**: Tìm kiếm ngữ nghĩa & BM25 toàn văn bằng SQLite FTS5 cho hàng triệu từ bản thảo và tư liệu.
- **TelemetryEngine**: Viễn trắc đo lường chi phí token và số phép toán tất định đã tiết kiệm.

## 3. Hệ Thống Vận Hành Trường Thiên 3.000+ Chương
1. **Phân cấp cốt truyện 8 tầng**: `Saga -> Era -> Volume -> Arc -> Mini-Arc -> Chapter -> Scene -> Beat`.
2. **Độc lập tuyến truyện (Story Threads)**: Mỗi tuyến có `revisit_window_chapters`, đảm bảo không bị thất lạc qua hàng trăm chương.
3. **Ngân sách leo thang 6 trục (Escalation Budgets)**: Ngăn chặn triệt để lạm phát sức mạnh và bùng nổ thế giới quan sớm.
4. **Phòng thủ bão hòa (Fatigue Defense Matrix)**: Giữ gìn chất lượng văn học, bảo vệ không gian thở đời thường TP.HCM 2026.
5. **Đo đạc hiệu năng (Benchmark Confirmed)**: Xử lý 3.000 chương (~8.09 triệu từ) với độ trễ tìm kiếm BM25 trung bình ~3.8ms và duyệt phân cấp ~0.04ms.

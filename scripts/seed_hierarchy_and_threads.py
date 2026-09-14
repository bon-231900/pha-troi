# -*- coding: utf-8 -*-
"""Script khởi tạo dữ liệu ban đầu cho story_hierarchy, story_threads, escalation_budgets, mystery_depth."""

import sqlite3
import json
import os
import sys
import glob
from datetime import datetime

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"
MANUSCRIPT_DIR = r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().isoformat()

    print("[1/4] Khởi tạo phân cấp story_hierarchy (Saga -> Era -> Volume -> Arc -> Mini-Arc -> Chapters 1..42)...")

    # 1. Saga
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, objective, stakes, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "saga_01", "saga", None, 1,
        "Đại Kỷ Nguyên I: Thức Tỉnh & Phong Ấn Chi Môn",
        "Kỷ nguyên mở đầu toàn bộ sử thi Phá Trời, bắt đầu từ sự hồi sinh linh mạch vi mô tại Trái Đất và sự cộng sinh giữa Nguyễn Minh An và tàn hồn Lâm Tịch.",
        "Thiết lập nền móng nhân sinh, khám phá bản chất phong ấn Trái Đất, chống lại sự sụp đổ trật tự đô thị.",
        "Sự tồn vong của linh hồn Lâm Tịch và an nguy tính mạng của Minh An cùng thành phố Sài Gòn.",
        "IN_PROGRESS", now_iso, now_iso
    ))

    # 2. Era
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, objective, stakes, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "era_01", "era", "saga_01", 1,
        "Thời Kỳ Linh Khí Hồi Lưu Tại Trái Đất (2026 - 2030)",
        "Giai đoạn Trái Đất bước vào chu kỳ nới lỏng phong ấn viễn cổ sau hàng ức năm làm Tử Địa.",
        "Tìm hiểu các điểm dị biến năng lượng đô thị mà không làm kinh động thế giới phàm tục.",
        "Bảo vệ cuộc sống đời thường, ngăn ngừa hiểm họa tà tu và dị thú thức tỉnh.",
        "IN_PROGRESS", now_iso, now_iso
    ))

    # 3. Volume 1
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, objective, stakes, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "volume_01", "volume", "era_01", 1,
        "Quyển 1: Sóng Ngầm Thành Phố",
        "Tập trung hoàn toàn tại TP.HCM năm 2026. Minh An gặp Lâm Tịch, bước vào con đường Khí Huyết Đạo, giải mã bí mật sụt lún bờ sông Sài Gòn.",
        "Minh An rèn luyện thể chất, Lâm Tịch giữ vững tàn hồn; giải quyết dị biến Thủy Môn Thủ Thiêm.",
        "Tính mạng của Minh An, an toàn bờ kè Bình Thạnh và Thủ Thiêm.",
        "IN_PROGRESS", now_iso, now_iso
    ))

    # 4. Arc 1
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, objective, stakes, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "arc_01", "arc", "volume_01", 1,
        "Hồi 1: Thức Hải & Vọng Nguyệt Đàm (Chương 1 - 42)",
        "Gồm 42 chương đầu tiên: Minh An phát hiện sự hiện diện của Lâm Tịch, trải qua các giai đoạn trui rèn khí huyết, khảo sát địa chất sông Sài Gòn, kích hoạt Thủy Môn và lắng nghe tiếng chuông trấn thủy.",
        "Hoàn thành Luyện Cốt sơ kỳ, khảo sát thành công Thủy Môn, đặt nền móng chuyển giao sang Hồi 2.",
        "Nguy cơ vỡ nát thức hải và sụp đổ kết cấu công trình ngầm bờ sông.",
        "COMPLETED", now_iso, now_iso
    ))

    # Mini Arcs
    mini_arcs = [
        ("mini_arc_01_01", "arc_01", 1, "Tiểu Hồi 1: Thức Tỉnh & Thích Nghi (Ch 1 - 15)", "Minh An thích nghi với giọng nói trong đầu, trải qua các cơn đau buốt thức hải và bắt đầu Luyện Cốt.", "COMPLETED"),
        ("mini_arc_01_02", "arc_01", 2, "Tiểu Hồi 2: Dòng Ngầm & Khảo Sát Địa Chất (Ch 16 - 30)", "Công việc cơ quan tại Ung Văn Khiêm, các đợt ngập lụt, khảo sát bất thường đáy sông Thủ Thiêm.", "COMPLETED"),
        ("mini_arc_01_03", "arc_01", 3, "Tiểu Hồi 3: Cổ Tháp & Thủy Môn Khởi Động (Ch 31 - 42)", "Phát hiện cấu trúc kim loại dị thường, lặn sâu 35m, kích hoạt Thủy Môn, tiếng chuông cổ vang lên.", "COMPLETED"),
    ]

    for maid, pid, oidx, mtitle, msum, mstat in mini_arcs:
        cur.execute("""
        INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, status, created_at, updated_at)
        VALUES (?, 'mini_arc', ?, ?, ?, ?, ?, ?, ?)
        """, (maid, pid, oidx, mtitle, msum, mstat, now_iso, now_iso))

    # 5. Đọc 42 chương hiện có và chèn vào story_hierarchy
    ch_files = sorted(glob.glob(os.path.join(MANUSCRIPT_DIR, "ch_*.md")))
    for ch_path in ch_files:
        fname = os.path.basename(ch_path)
        ch_num = int(fname.split("_")[1].split(".")[0])
        with open(ch_path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        title = lines[0].replace("#", "").strip() if lines else f"Chương {ch_num}"
        word_count = len(content.split())

        # Phân loại vào mini_arc
        if ch_num <= 15:
            parent_mini = "mini_arc_01_01"
        elif ch_num <= 30:
            parent_mini = "mini_arc_01_02"
        else:
            parent_mini = "mini_arc_01_03"

        cid = f"ch_{ch_num:03d}"
        cur.execute("""
        INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, word_count, status, pov, created_at, updated_at)
        VALUES (?, 'chapter', ?, ?, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
        """, (cid, parent_mini, ch_num, title, f"Bản thảo hoàn chỉnh Chương {ch_num}", word_count, now_iso, now_iso))

    print(f"    -> Đã nạp thành công {len(ch_files)} chương vào story_hierarchy.")

    # 2. Khởi tạo Story Threads
    print("[2/4] Khởi tạo các tuyến truyện cốt lõi vào story_threads...")
    threads = [
        (
            "TH-PLT-001", "MAIN_PLOT", "Cộng Sinh Minh An - Lâm Tịch & Hồi Phục Đạo Cơ",
            "Mối quan hệ cộng sinh giữa người bình thường Nguyễn Minh An và tàn hồn chí cường Lâm Tịch, cùng tìm cách bảo vệ linh hồn và thích nghi với quy tắc Trái Đất.",
            1, 3000, "ACTIVE", "Đang ở giai đoạn thích nghi và thiết lập lòng tin ban đầu sau sự kiện Thủy Môn.",
            "Minh An biết Lâm Tịch là nữ nhân viễn cổ tàn hồn, có kiếm gãy trong thức hải.",
            "Lâm Tịch từng tham gia trận chiến chí cao làm nát đại giới; kiếm gãy là bản mạng đạo khí.",
            "Độc giả biết Lâm Tịch mệt mỏi cùng cực, muốn tìm chốn bình yên chứ không màng tranh đoạt.",
            42, 15, "HIGH", "CORE"
        ),
        (
            "TH-PLT-002", "MAIN_PLOT", "Tiến Trình Tu Luyện Khí Huyết & Thể Đạo của Minh An",
            "Con đường tu luyện duy nhất phù hợp với Trái Đất mạt pháp: Tôi Thể, Luyện Cốt, Hoán Huyết. Đi từ người phàm thể trạng trung bình đến thể phách vững chắc.",
            3, 1000, "ACTIVE", "Minh An hoàn thành giai đoạn sơ bộ tôi luyện xương cốt sau khi tiếp nhận dòng năng lượng Thủy Môn ở Ch 41-42.",
            "Minh An biết mình đang tiến triển Luyện Cốt theo phương pháp Lâm Tịch chỉ dẫn.",
            "Thể Đạo là con đường tàn khốc đòi hỏi ý chí phàm nhân sắt đá, không có đường tắt.",
            "Độc giả thấy rõ sự nỗ lực kiên trì của Minh An từng ngày.",
            42, 10, "HIGH", "CORE"
        ),
        (
            "TH-MYS-001", "MYSTERY", "Bí Mật Cổ Tháp & Trận Nhãn Thủy Môn Sông Sài Gòn",
            "Công trình dị thường nằm sâu 35m dưới bùn đáy sông Sài Gòn phát ra âm ba và sóng năng lượng.",
            16, 60, "ACTIVE", "Thủy Môn vừa được khởi động ở Ch 42, tiếng chuông cổ ngân vang, báo hiệu giai đoạn khảo sát sâu.",
            "Minh An và đồng nghiệp phát hiện dị thường địa chất; Lâm Tịch nhận ra dấu vết phong ấn quen thuộc.",
            "Đây là một trong 9 trận nhãn phong tỏa thủy mạch Trái Đất từ kỷ nguyên trước.",
            "Độc giả cảm nhận quy mô to lớn ẩn dưới lòng đô thị hiện đại.",
            42, 5, "CRITICAL", "MAJOR"
        ),
        (
            "TH-MYS-002", "MYSTERY", "Nguyên Nhân Trái Đất Biến Thành Vị Diện Bị Phong Ấn",
            "Vì sao Trái Đất bị cô lập khỏi chư thiên vạn giới, linh khí khô kiệt và các con đường tu luyện khác bị cắt đứt.",
            1, 2000, "ACTIVE", "Chưa có manh mối trực tiếp, chỉ có những tàn dư trận pháp ngầm.",
            "Minh An chỉ lờ mờ nhận ra thế giới không đơn giản như mắt thấy.",
            "Trái Đất là nơi chôn giấu bí mật tối thượng của kỷ nguyên viễn cổ.",
            "Độc giả tò mò về bức tranh vũ trụ lớn.",
            40, 25, "MEDIUM", "CORE"
        ),
        (
            "TH-REL-001", "RELATIONSHIP", "Mối Quan Hệ Minh An - Lâm Tịch (Extremely Slow Burn)",
            "Tiến trình tình cảm và thấu hiểu giữa Minh An và Lâm Tịch: từ cảnh giác, lạ lẫm, đến đồng hành, chia sẻ và đồng cảm sâu sắc.",
            1, 3000, "ACTIVE", "Giai đoạn đồng cam cộng khổ, Minh An quan tâm đời thường, Lâm Tịch đáp lại bằng sự tin cậy.",
            "Cả hai tôn trọng không gian riêng của nhau.",
            "Lâm Tịch đã rung động trước sự quan tâm mộc mạc của Minh An nhưng chưa từng thể hiện.",
            "Độc giả cảm nhận sự ấm áp tĩnh lặng giữa hai tâm hồn cô đơn.",
            42, 10, "HIGH", "CORE"
        ),
        (
            "TH-CHR-001", "CHARACTER_ARC", "Trách Nhiệm Đời Thường & Gia Đình của Minh An Tại Sài Gòn",
            "Áp lực công việc văn phòng, đồng nghiệp, tiền thuê nhà, gia đình ở quê; giữ vững bản sắc một người trẻ Việt Nam năm 2026.",
            1, 300, "ACTIVE", "Cân bằng giữa công việc khảo sát địa chất và thời gian tu tập thể đạo.",
            "Minh An luôn coi trọng đạo đức và nghĩa vụ công việc hàng ngày.",
            "Nền tảng đạo đức đời thường chính là tâm tính giúp Minh An không bị biến chất khi có sức mạnh.",
            "Độc giả đồng cảm sâu sắc với hiện thực mưu sinh của nhân vật.",
            40, 15, "MEDIUM", "MAJOR"
        ),
        (
            "TH-WLD-001", "WORLDBUILDING", "Dị Biến Năng Lượng Đô Thị & Phản Ứng Chính Quyền/Khoa Học",
            "Cách mà chính quyền, viện nghiên cứu địa chất và các cơ quan chức năng TP.HCM phản ứng trước các hiện tượng sụt lún, từ trường dị thường.",
            10, 150, "ACTIVE", "Các đội khảo sát kỹ thuật đang triển khai thiết bị quan trắc tại khu vực Thủ Thiêm - Bình Thạnh.",
            "Các kỹ sư và chuyên gia coi đây là hiện tượng sụt lún địa chất đô thị phức tạp.",
            "Khoa học hiện đại sẽ dần chạm đến ranh giới của năng lượng cổ xưa.",
            "Độc giả thấy tính thực tế và logic chặt chẽ của xã hội Việt Nam 2026.",
            42, 10, "MEDIUM", "MAJOR"
        )
    ]

    for tid, ttype, title, desc, orig, targ, stat, cstate, kinfo, hinfo, rknow, last_t, rwin, urg, imp in threads:
        cur.execute("""
        INSERT OR REPLACE INTO story_threads (
            thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter,
            status, current_state, known_info, hidden_info, reader_knowledge,
            last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tid, ttype, title, desc, orig, targ, stat, cstate, kinfo, hinfo, rknow, last_t, rwin, urg, imp, now_iso, now_iso))

    print(f"    -> Đã khởi tạo {len(threads)} tuyến truyện cốt lõi.")

    # 3. Khởi tạo Escalation Budgets
    print("[3/4] Khởi tạo ngân sách leo thang escalation_budgets cho Quyển 1...")
    budgets = [
        ("BUD-VOL1-PWR", "VOLUME", "volume_01", "POWER_CEILING", 1.8, 2.5, 5, 41, "Giới hạn sức mạnh: Sơ kỳ Luyện Cốt, sức mạnh thể chất phàm nhân cường tráng, cấm bay lượn, cấm chưởng phong."),
        ("BUD-VOL1-GEO", "VOLUME", "volume_01", "GEOGRAPHY_SCALE", 1.2, 2.0, 5, 40, "Phạm vi địa lý: Chỉ trong nội thành TP.HCM (Bình Thạnh, Thủ Thiêm, Nhà Bè, Cần Giờ)."),
        ("BUD-VOL1-COS", "VOLUME", "volume_01", "COSMOLOGY_DEPTH", 1.0, 2.0, 8, 35, "Thế giới quan: Chỉ cảm nhận dấu vết năng lượng cổ trận ngầm, cấm tiếp xúc chư thiên vạn giới."),
        ("BUD-VOL1-STK", "VOLUME", "volume_01", "STAKES_LEVEL", 1.5, 2.5, 4, 42, "Cổ phần nguy hiểm: Nguy cơ cá nhân và an toàn kết cấu công trình ven sông, cấm nguy cơ diệt thế."),
        ("BUD-VOL1-MYS", "VOLUME", "volume_01", "MYSTERY_REVEAL", 1.8, 2.2, 5, 42, "Giải mã bí mật: Mức độ 1.8/4.0 (Đã biết Thủy Môn có kết cấu hợp kim và âm ba, chưa biết bản chất trận pháp tối thượng)."),
        ("BUD-VOL1-EMO", "VOLUME", "volume_01", "EMOTIONAL_INTIMACY", 1.5, 2.0, 10, 41, "Tiến trình tình cảm: Mức độ 1.5/10.0 (Đồng hành tin cậy, thấu hiểu đời thường, cấm tỏ tình, cấm skinship lãng mạn sớm).")
    ]

    for bid, stype, sid, axis, cur_lvl, ceil, cdown, last_ch, desc in budgets:
        cur.execute("""
        INSERT OR REPLACE INTO escalation_budgets (
            budget_id, scope_type, scope_id, axis, current_level, allowed_ceiling, cooldown_chapters,
            last_escalated_chapter, description, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
        """, (bid, stype, sid, axis, cur_lvl, ceil, cdown, last_ch, desc, now_iso, now_iso))

    print(f"    -> Đã khởi tạo {len(budgets)} ngân sách leo thang.")

    # 4. Khởi tạo Mystery Depth
    print("[4/4] Khởi tạo ma trận chiều sâu bí mật mystery_depth...")
    mysteries = [
        (
            "MYS-THUY-MON", "Bí Ẩn Cổ Tháp & Thủy Môn Dưới Lòng Sông Sài Gòn",
            "Hiện tượng sụt lún địa chất và dị thường từ trường cục bộ tại công trình bờ kè sông Sài Gòn.",
            "Một cấu trúc hợp kim ngầm phi tự nhiên có niên đại cực cổ, phát ra sóng năng lượng và dao động âm ba áp suất cao khi triều cường.",
            "Trận nhãn Thủy Môn thuộc Cửu Khóa Trấn Thủy Cổ Trận từ thời kỷ nguyên phong ấn, có liên kết với mạch ngầm Biển Đông.",
            "Điểm neo hạch tâm phong tỏa linh mạch Trái Đất, chứa đựng phong ấn trấn áp tàn tích thần ma viễn cổ.",
            json.dumps(["Đứt gãy địa chấn do nạo vét lòng sông", "Tàn tích công sự thời chiến", "Rò rỉ khí metan ngầm"]),
            json.dumps({"volume_01": 2, "volume_02": 3, "volume_05": 4}),
            2, "IN_PROGRESS"
        ),
        (
            "MYS-TRAI-DAT-SEAL", "Phong Ấn Trái Đất & Mạt Pháp Kỷ Nguyên",
            "Trái Đất là một hành tinh bình thường trong vũ trụ, không có phép thuật hay tu tiên.",
            "Các luồng khí mạch tự nhiên trên Trái Đất bị tắc nghẽn bởi một trường lực vô hình dạng mạng lưới.",
            "Trái Đất từng là chiến trường hạch tâm viễn cổ, bị đại năng phong ấn để cô lập hiểm họa diệt thế.",
            "Trái Đất chính là Lò Luyện Phong Thiên giam giữ chân tướng sụp đổ của toàn bộ Đạo giới viễn cổ.",
            json.dumps(["Thuyết tiến hóa tự nhiên không có dị năng", "Ảo giác tập thể do bức xạ mặt trời"]),
            json.dumps({"volume_01": 1, "volume_03": 2, "volume_07": 3, "volume_12": 4}),
            1, "UNRESOLVED"
        )
    ]

    for mid, mname, surf, inter, deep, ult, false_th, sched, cur_layer, mstat in mysteries:
        cur.execute("""
        INSERT OR REPLACE INTO mystery_depth (
            mystery_id, name, surface_explanation, intermediate_explanation, deep_explanation,
            ultimate_truth, false_theories, reveal_schedule, current_revealed_layer, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (mid, mname, surf, inter, deep, ult, false_th, sched, cur_layer, mstat, now_iso, now_iso))

    print(f"    -> Đã khởi tạo {len(mysteries)} hồ sơ chiều sâu bí mật.")

    conn.commit()
    conn.close()
    print("[+] Hoàn tất nạp dữ liệu nền tảng cho 3.000+ chương vào SQLite database!")

if __name__ == "__main__":
    seed_data()

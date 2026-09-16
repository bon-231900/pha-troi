# -*- coding: utf-8 -*-
"""Seed database with strategic multi-tier foreshadowing, mystery depth, and story threads."""

import os
import sys
import json
import sqlite3

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. SEED FORESHADOWING LEDGER (FSH-029 to FSH-033)
    seeds = [
        (
            "FSH-029",
            "Máy phổ kế huỳnh quang tia X tại Viện ghi nhận chuỗi đồng vị kim loại dị thường không có trong bảng tuần hoàn Mendeleev trên chuôi đoản đao và gỗ cọc Ba Son",
            66,
            1,
            json.dumps(["Bản phân tích huỳnh quang tia X tại phòng thí nghiệm", "Chỉ số phổ chấn 0.12 Hz"], ensure_ascii=False),
            "Chỉ dẫn mở rộng sang đường dây buôn lậu khoáng thạch cổ xưa và mỏ bauxit cổ tại Tây Nguyên của Cửu Long Thiên Hải, mở màn Arc 3",
            100,
            1,
            "PLANTED"
        ),
        (
            "FSH-030",
            "Minh An nhìn thấy hoa văn khắc chìm dưới chân mố Cầu Mống không phải chữ Pháp hay chữ Hán triều Nguyễn, mà là ký tự hình mặt trời lông vũ cổ xưa",
            66,
            1,
            json.dumps(["Mố cầu Mống thép đen", "Bản đồ trắc địa số 3D của Tuấn"], ensure_ascii=False),
            "Liên kết trận đồ Thủy Môn phương Nam với bãi cọc cổ Bạch Đằng và nền văn minh tu chân Đông Sơn - Sa Huỳnh thời tiền sử",
            250,
            1,
            "PLANTED"
        ),
        (
            "FSH-031",
            "Khi ba viên ngọc chiếu sáng tinh đồ Cực Tù trên trần phòng trọ, Lâm Tịch thoáng chấn động nhận ra một góc ấn ký chư thiên giống hệt huy hiệu tông môn của nàng ở Cửu Thiên",
            66,
            1,
            json.dumps(["Đài sen ngọc bích", "Tinh đồ Cực Tù Lục Trọng Giới 3D"], ensure_ascii=False),
            "Gợi mở chân tướng: Sư môn của Lâm Tịch ở Cửu Thiên từng là một trong những thế lực tham gia phong ấn Cực Tù triệu năm trước",
            600,
            1,
            "PLANTED"
        ),
        (
            "FSH-032",
            "Khi Minh An ngồi thiền vận chuyển Ngọc Tủy, nhịp đập tủy ngọc trong xương anh vô thức đồng bộ với tần số vi chấn ngầm 0.12 Hz của lõi Trái Đất",
            66,
            1,
            json.dumps(["Thức thứ 7 Ngọc Tủy Quy Nhất", "Dao động từ trường 0.12 Hz của Tuấn"], ensure_ascii=False),
            "Mối liên kết bản nguyên giữa nhục thân phàm nhân tu luyện Thể Đạo và Trái Tim Thể Đạo Thủy Tổ bị giam giữ sâu trong lõi Trái Đất",
            1200,
            1,
            "PLANTED"
        ),
        (
            "FSH-033",
            "Lâm Tịch nhắc đến việc 6 con đường tu luyện kia đều phụ thuộc linh khí và thiên địa quy tắc, chỉ duy nhất Thể Đạo lấy nhục thân làm vũ trụ độc lập",
            66,
            1,
            json.dumps(["Lời chỉ dẫn về Hoán Huyết Hóa Cương", "Sự sụp đổ của các con đường tu luyện trên Trái Đất"], ensure_ascii=False),
            "Lý do Thể Đạo là con đường duy nhất không bị Thiên Đạo ký sinh, đặt nền tảng triết lý tối hậu cho hành trình Phá Trời",
            400,
            1,
            "PLANTED"
        )
    ]

    for s in seeds:
        cur.execute("""
        INSERT OR REPLACE INTO foreshadowing_ledger 
        (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, payoff_scene, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, s)

    # 2. SEED MYSTERY DEPTH (MYS-001 to MYS-004)
    mysteries = [
        (
            "MYS-001",
            "Mạng lưới 12 Cọc Tiêu Thủy Môn và Đại Phong Ấn Việt Nam",
            "Công trình nạo vét và cọc tiêu điều tiết thủy lợi ngầm chống sạt lở sông ngòi do triều Nguyễn và Pháp xây dựng",
            "12 cọc tiêu phong thủy cổ xưa trấn áp long mạch địa tầng Nam Bộ, chống sụt lún và ngăn chặn rò rỉ từ trường ngầm",
            "Đại trận đồ trấn giữ bờ cõi do Thủ Hộ Nhất Mạch của các triều đại Hùng Vương, Lý, Trần, Nguyễn đời đời gia cố để bảo vệ Trái Đất khỏi ánh nhìn chư thiên",
            "Lớp then cài ngoại vi của Cực Tù Lục Trọng Giới, khóa chặt các thủy nhãn huyết mạch kết nối Trái Đất với Tinh Hải viễn cổ",
            json.dumps(["Chỉ là cọc bê tông và gỗ lim chống xói lở", "Di tích cảng buôn cổ"], ensure_ascii=False),
            json.dumps({"layer_1": 1, "layer_2": 45, "layer_3": 150, "layer_4": 300}, ensure_ascii=False),
            2,
            "ACTIVE"
        ),
        (
            "MYS-002",
            "Bản chất Cực Tù Lục Trọng Giới & Trái Tim Thể Đạo Thủy Tổ",
            "Trái Đất là vùng đất phế tích mạt pháp ngẫu nhiên không có linh khí trong vũ trụ",
            "Vị diện bị phong ấn bằng đại trận viễn cổ để ngăn chặn các thế lực hắc ám bên ngoài xâm lấn",
            "Lồng giam tầng thứ sáu do chư thiên vạn giới hợp lực thiết lập nhằm giam giữ thực thể hung hãn nhất thời hỗn mang",
            "Nơi giam giữ Trái Tim của Thể Đạo Thủy Tổ — vị Thần Ma đầu tiên dám dùng nhục thân đấm vỡ Thiên Môn; lõi Trái Đất chính là nhịp đập của trái tim ấy",
            json.dumps(["Trái Đất chỉ là hành tinh vô danh", "Vùng đất bỏ hoang của các thần"], ensure_ascii=False),
            json.dumps({"layer_1": 1, "layer_2": 66, "layer_3": 500, "layer_4": 1200}, ensure_ascii=False),
            2,
            "ACTIVE"
        ),
        (
            "MYS-003",
            "Thân thế Lâm Tịch & Chân tướng thực thể TRỜI",
            "Lâm Tịch là nữ tu sĩ thời cổ bị kẻ thù hãm hại làm tan rã thể xác, chỉ còn tàn hồn may mắn sống sót",
            "Đại năng cấp cao của Linh Đạo tại Cửu Thiên, gặp biến cố diệt thế dẫn tới vỡ nát thân xác",
            "Đệ nhất Kiếm Tôn Linh Đạo bước tới cảnh giới Chí Tôn, phát hiện Thiên Đạo là thực thể ký sinh nuốt chửng linh hồn tu sĩ nên bị chư thần vây sát",
            "Bản chất của TRỜI là chiếc lồng chăn nuôi vạn giới; 6 con đường tu luyện kia đều là cạm bẫy ký sinh; chỉ có Thể Đạo mới đủ sức chém đứt xiềng xích",
            json.dumps(["Lâm Tịch bị ma đạo ám hại", "Nàng là tàn hồn phong ấn thông thường"], ensure_ascii=False),
            json.dumps({"layer_1": 1, "layer_2": 100, "layer_3": 600, "layer_4": 1800}, ensure_ascii=False),
            1,
            "ACTIVE"
        ),
        (
            "MYS-004",
            "Con Đường Thể Đạo Trong Kỷ Nguyên Tuyệt Linh & Bản Thể Phàm Nhân",
            "Một môn võ thuật khí công bí truyền cổ xưa dùng để rèn luyện sức khỏe cơ bắp",
            "Phương pháp rèn luyện khí huyết duy nhất còn sót lại trên Trái Đất khi linh khí trời đất cạn kiệt",
            "Con đường tu luyện nhục thân cổ xưa lấy thân thể làm tiểu vũ trụ độc lập, không lệ thuộc vào bất kỳ quy tắc hay linh khí nào của Thiên Đạo",
            "Vũ khí tối thượng phá vỡ Thiên Mệnh: Người phàm trần 100% rèn luyện từ con số 0 tạo nên Chân Thân thuần khiết tuyệt đối mà Thiên Đạo không thể đồng hóa",
            json.dumps(["Khí công phàm trần thông thường", "Thể dục trị liệu chấn thương"], ensure_ascii=False),
            json.dumps({"layer_1": 1, "layer_2": 30, "layer_3": 400, "layer_4": 1500}, ensure_ascii=False),
            2,
            "ACTIVE"
        )
    ]

    for m in mysteries:
        cur.execute("""
        INSERT OR REPLACE INTO mystery_depth
        (mystery_id, name, surface_explanation, intermediate_explanation, deep_explanation, ultimate_truth, false_theories, reveal_schedule, current_revealed_layer, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, m)

    # 3. SEED STORY THREADS (TH-MYS-002, TH-WLD-001, TH-PLT-003)
    threads = [
        (
            "TH-MYS-002",
            "MYSTERY",
            "Giải Mã Tinh Đồ Cực Tù Lục Trọng Giới",
            "Hành trình thu thập 12 cọc Thủy Môn Tiêu để đánh thức la bàn định vị phong ấn và giải mã bí mật thời viễn cổ của Trái Đất.",
            66,
            300,
            "ACTIVE",
            "Đã thu thập 3 cọc tiêu phương Nam (Lò Gốm, Phú Định, Mũi Đèn Đỏ); định vị cọc số 5 Cầu Mống và cọc số 6 Ba Son.",
            "3 cọc tiêu tạo thành tam giác cân khóa tâm điểm Bến Nghé - Ba Son; tinh đồ 3D hé lộ 12 điểm nút Bát Quái Cửu Cung.",
            "Trái Đất là Cực Tù tầng thứ sáu giam giữ Thể Đạo Thủy Tổ; 12 cọc là then cài ngoại vi do triều Nguyễn gia cố.",
            "Độc giả biết Trái Đất từng là Cực Tù Lục Trọng Giới và cọc số 5, 6 nằm tại Cầu Mống và Ba Son.",
            66,
            15,
            "HIGH",
            "CRITICAL"
        ),
        (
            "TH-WLD-001",
            "WORLDBUILDING",
            "Mạng Lưới Thủ Hộ Nhất Mạch Của Tiền Nhân Việt Nam",
            "Khám phá các di tích, bia ký và trận đồ ngầm do các triều đại lịch sử Việt Nam bí mật xây dựng dọc bờ cõi.",
            14,
            500,
            "ACTIVE",
            "Đã phát hiện cổ thư ông Ba Khiêm, hồ sơ trắc địa triều Nguyễn 1898 và hệ thống cọc tiêu sông ngòi Sài Gòn.",
            "Tiền nhân triều Nguyễn và các triều đại xưa xây dựng thành quách kết hợp trận đồ sông ngòi tự nhiên.",
            "Các triều đại Việt Nam thực chất là Thủ Hộ Nhất Mạch bảo vệ long mạch và che giấu đại phong ấn Trái Đất.",
            "Độc giả biết tiền nhân có tri thức phong thủy địa tầng thâm sâu qua các cổ thư và cọc tiêu.",
            66,
            20,
            "MEDIUM",
            "HIGH"
        ),
        (
            "TH-PLT-003",
            "MAIN_PLOT",
            "Đột Phá Hoán Huyết Hóa Cương (Thức Thứ Tám Đoán Cốt)",
            "Tiến trình chuyển hóa tủy ngọc thành Cương Huyết, bước đệm chuyển tiếp từ Luyện Cốt sang Thần Tạng của Thể Đạo.",
            66,
            80,
            "ACTIVE",
            "Lâm Tịch hé lộ điều kiện mở khóa Thức thứ tám khi thu thập đủ 6 cọc tiêu trung tâm Sài Gòn.",
            "Cần năng lượng thuần âm từ 6 trận nhãn Thủy Môn để kích hoạt tiến trình Hoán Huyết.",
            "Hoán Huyết Hóa Cương là bước biến đổi sinh học vi mô tuyệt đối, tạo tiền đề để nhục thân kháng lại áp chế của ngoại giới.",
            "Độc giả biết Thức thứ 8 là Hoán Huyết Hóa Cương và cần mở 6 cọc đầu tiên.",
            66,
            10,
            "HIGH",
            "CRITICAL"
        )
    ]

    for t in threads:
        cur.execute("""
        INSERT OR REPLACE INTO story_threads
        (thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter, status, current_state, known_info, hidden_info, reader_knowledge, last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, t)

    conn.commit()
    conn.close()
    print("[+] Seeding foreshadowing_ledger, mystery_depth, story_threads completed successfully.")

if __name__ == "__main__":
    seed_data()

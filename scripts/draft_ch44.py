# -*- coding: utf-8 -*-
"""Script soạn thảo và kiểm duyệt bản thảo Chương 44: Then Cài Trấn Thủy Và Dòng Chảy Hạ Lưu."""

import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, r"d:\tieu-thuyet")

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"
MANUSCRIPT_DIR = r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01"
CH44_PATH = os.path.join(MANUSCRIPT_DIR, "ch_044.md")

CHAPTER_CONTENT = """---
chapter: 44
title: "Then Cài Trấn Thủy Và Dòng Chảy Hạ Lưu"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Đáy ngã ba sông Nhà Bè (độ sâu 38m), TP.HCM"
date: "2026-10-07"
word_count: 2780
---

# Chương 44: Then Cài Trấn Thủy Và Dòng Chảy Hạ Lưu

Một giờ mười lăm phút chiều ngày mùng bảy tháng Mười năm 2026.

Ở độ sâu ba mươi tám mét dưới lòng sông Soài Rạp, thế giới bên ngoài lồng lặn là một cõi thinh lặng đặc quánh, lạnh buốt và áp bức đến nghẹt thở. 

Dòng nước đỏ ngầu phù sa quất liên hồi vào bộ đồ lặn cao su dày cộp của tôi. Dù đã có dây cáp rốn bọc thép nối liền với thân lồng lặn giữ thăng bằng, lực kéo của dòng xoáy ngầm vẫn mạnh đến mức khiến hai bắp chân tôi căng cứng, mỗi bước tiến về phía trước trên lớp bùn nhão đều giống như đang lội ngược dòng một trận lũ quét vô hình.

"Lặn 01 và Lặn 02, chú ý chân vịt và dây tín hiệu!" Giọng Đại úy Hùng vang lên trong tai nghe qua đường truyền vô tuyến dưới nước, âm sắc hơi rè do nhiễu sóng cơ học nhưng dứt khoát: "Tàu điều hành ghi nhận dòng chảy tầng đáy đang đạt vận tốc hai phẩy sáu mét trên giây. Hai đồng chí neo dây cáp hãm vào mỏm đá bên trái, hỗ trợ cậu An tiếp cận miệng vòm cống!"

"Lặn 01 rõ!" Người chiến sĩ đặc nhiệm dày dạn kinh nghiệm đi bên cạnh tôi ra hiệu bằng tay, nhanh nhẹn bắn móc neo titan có ngạnh thép vào khe đá thanh hoa cổ, ghìm chặt sợi dây cáp định vị phụ.

Tôi bước thêm hai bước, đưa ngọn đèn chiếu điểm công suất lớn quét dọc theo vách đá sừng sững trước mặt.

Dưới luồng sáng vàng đậm xuyên thấu màn nước đỏ, cấu trúc của công trình ngầm dần hiện rõ từng mảng chi tiết:

Đó là một vòm cổng bằng đá khối đồ sộ có bề ngang gần năm mét, vươn cao khỏi tầng bùn đáy chừng ba mét. Những phiến đá thanh hoa màu xám đen được gọt đẽo vuông vức, khớp nối với nhau khít khao bằng một lớp vữa cổ xưa có pha bột vỏ sò và mật mía đã hóa thạch ngàn năm. Trên gờ vòm đá, hoa văn móng rồng uốn lượn chìm nổi dưới lớp gỉ đồng xanh thẫm và những cụm hà biển bám chặt như lớp giáp vảy.

Thế nhưng, điều khiến dòng nước ngã ba sông Nhà Bè biến chuyển dị thường trưa nay không phải do bản thân công trình, mà nằm ở điểm tắc nghẽn nghiêm trọng ngay giữa tâm cửa cống:

Một khối rác ngầm khổng lồ đang kẹt cứng trong miệng vòm đá. Đó là ba thân cây sao đen cổ thụ có đường kính gần một mét — dấu tích của những cánh rừng nguyên sinh phương Nam bị lũ cuốn trôi từ hàng trăm năm trước — đan chéo vào nhau tựa như một chiếc nẹp gỗ khổng lồ. Bùn khoáng chu sa, oxit sắt đỏ sẫm cùng các mảnh vỡ kim loại của những chiếc thuyền gỗ thời cận đại đã bồi đắp quanh ba thân cây ấy, tạo thành một chiếc nút chặn gần như kín mít.

Chính vì chiếc nút chặn này bít kín miệng xả ngầm, khối nước khổng lồ từ thượng lưu sông Sài Gòn và sông Đồng Nai dồn về hạ lưu không thể thoát đều ra cửa biển, sinh ra hiện tượng chênh lệch áp suất thủy tĩnh khủng khiếp. Dòng nước bị dồn nén dưới đáy sâu rít lên từng hồi gầm rĩ, đùn ngược bột khoáng chu sa lên mặt sông tạo thành vệt thủy triều đỏ và sương mù dày đặc.

"Tiến sĩ Nam, chú Tùng, hai người có nhìn thấy hình ảnh qua camera mũ của tôi không?" Tôi hít một hơi khí Nitrox mát lạnh, lên tiếng qua micro.

"Thấy rất rõ, cậu An!" Giọng Tiến sĩ Trịnh Hoài Nam vang lên đầy vẻ căng thẳng từ boong tàu điều hành: "Cảm biến áp suất trên camera ghi nhận chênh lệch áp lực giữa hai mặt nút chặn lên tới ba phẩy hai bar. Khối nước thượng nguồn đang đè lên vách đá này tương đương hàng chục ngàn tấn lực! Nếu chúng ta dùng tời kéo giật thô bạo hoặc dùng thuốc nổ để phá búi cây mục, sóng xung kích trong môi trường nước nén sẽ làm nứt toác toàn bộ chân đế vòm đá cổ, gây sụt lở nghiêm trọng luồng hàng hải Soài Rạp!"

"Không được dùng bộc phá, Nam à!" Tiếng chú Phan Thanh Tùng chen vào, giọng run lên vì xúc động: "Cậu An, hãy nhìn sang mạn phải chân vòm đá! Trên họa đồ thủy đạo cổ khắc trên lưng rùa đá Thủy Trấn Thạch mà chúng ta phục chế ở hố móng Thủ Thiêm, cổ nhân có ghi chú rõ ràng về một cơ chế có tên là **Ngạc Khảm** — một then trượt xả áp bằng đồng đen nằm ở mép phải móng rồng! Phải mở then trượt xả áp phụ trước để dòng nước thoát bớt, cân bằng áp lực hai bên thì nút cây mục mới tự lỏng ra được!"

Lời nhắc của chú Tùng như một tia chớp rọi sáng tâm trí tôi. 

Họa đồ trên lưng rùa đá cổ! Đó chính là lời giải cơ học mà tiền nhân để lại cho hậu thế.

Tôi quay sang Lặn 01 và Lặn 02, chỉ tay về phía góc phải của chân vòm đá. Hai người nhái lập tức hiểu ý, cùng tôi di chuyển men theo vách đá phủ đầy rêu phong trơn trượt.

Lớp bùn dưới đáy sâu ngập tới quá đầu gối. Tôi quỳ một chân xuống bùn lầy, dùng chiếc bay gạt chuyên dụng bằng thép không gỉ cạo từng mảng rêu mục và vỏ hà biển bám chặt trên bề mặt phiến đá góc phải.

*Xoẹt... Xoẹt...*

Từng mảng trầm tích hóa thạch dày cộp bong ra, để lộ một khối kim loại màu đồng đen thẫm ẩn sâu trong hốc đá. Đó là một thanh then cài hình đầu rồng ngậm then trượt, dài khoảng sáu mươi cen-ti-mét, đúc bằng hợp kim cổ xưa có ánh kim lấp lánh không hề bị rỉ sét sau bao thế kỷ ngâm mình dưới đáy nước.

"Đã tìm thấy then cài Ngạc Khảm!" Tôi báo cáo qua bộ đàm.

"Tuyệt vời!" Đại úy Hùng chỉ đạo ngay: "Lặn 01, dùng xà beng titan bẩy thử chốt trượt!"

Người chiến sĩ đặc nhiệm mang mã hiệu Lặn 01 lập tức rút thanh đòn bẩy hợp kim dài một mét gắn bên hông lồng lặn, lựa khéo đầu dẹp vào khe hở giữa then đồng và rãnh trượt bằng đá. Anh dồn toàn bộ trọng lượng cơ thể cùng sự hỗ trợ của Lặn 02 để bẩy then cài.

Thế nhưng, sau hàng trăm năm chịu áp lực bùn cát nén chặt, chiếc then cài bằng đồng đen vẫn nằm im lìm như một phần của khối đá nguyên khối, không nhúc nhích lấy một ly.

"Đồng hồ điểm mười hai phút thời gian đáy!" Tiếng kỹ sư Tuấn cảnh báo gấp gáp từ cabin: "Khí thở Nitrox trong bình của đội lặn đã tiêu hao bốn mươi phần trăm! Các đồng chí chỉ còn tối đa bảy phút thao tác trước khi bắt buộc phải quay lại lồng lặn để thực hiện quy trình giảm áp nổi lên!"

Thời gian đang cạn dần từng giây.

Dưới áp suất năm atmosphere, màng nhĩ tôi bắt đầu có cảm giác buốt nhức âm ỉ. Mỗi nhịp thở dường như đòi hỏi nhiều nỗ lực hơn từ cơ hoành.

*"Minh An..."*

Thanh âm của Lâm Tịch lại vang lên trong tâm thức tôi, khẽ khàng nhưng rành rọt từng tiếng:

*"Đừng dùng lực phàm của cơ bắp để giằng co... Cổ nhân đúc then cài này theo nguyên lý cối xay nước, then đồng có rãnh then khóa hình xoắn ốc ngược chiều kim đồng hồ. Dùng lực đẩy ngang sẽ chỉ làm chốt nêm chặt thêm.*

*Vận chuyển Khí Huyết vào khớp cổ tay và màng xương bàn tay. Hạ trọng tâm cơ thể, dùng lực xoay tròn của tủy xương vặn chốt then theo góc nghiêng bốn mươi lăm độ sang mạn thuyền..."*

Lời hướng dẫn ngắn gọn nhưng chuẩn xác vô ngần của Lâm Tịch lập tức định hình lại phương án hành động trong đầu tôi. 

Nàng không hề dùng thần lực viễn cổ để phá khóa; nàng chỉ dùng kinh nghiệm quan sát cơ học ngàn năm để chỉ cho tôi đúng quy luật vận động của vật thể.

"Đồng chí Dũng, đồng chí Thành, dừng tay lại!" Tôi ra hiệu cho hai người nhái, giọng nói qua micro bình tĩnh và chắc nịch: "Không bẩy ngang được đâu. Then này có rãnh ren xoắn ốc ngược. Để tôi phối hợp cùng các đồng chí!"

Hai người chiến sĩ đặc nhiệm lập tức điều chỉnh thế đứng, giữ chặt thân thanh đòn bẩy theo hướng dẫn của tôi.

Tôi bước sát lại gần, đặt hai bàn tay bọc găng cao su chuyên dụng áp chặt lên đầu then cài bằng đồng đen.

Nhắm nghiền mắt lại giữa làn nước tối tăm, tôi gạt bỏ mọi sự lo âu về áp suất và thời gian. Tôi dẫn luồng nhiệt lưu Khí Huyết từ đan điền cuộn trào lên cột sống, tỏa ra hai khớp vai rồi rót thẳng vào từng đốt xương ngón tay theo chu trình Tam Chu Thiên. Xương tủy trong cơ thể tôi khẽ ngân nga một tiếng thanh tao như ngọc khánh, cộng hưởng hoàn mỹ với nhịp dao động cơ học của khối đá ngầm.

"Một... Hai... Ba... Xoay!" Tôi quát khẽ qua bộ đàm.

Đồng thời với cú phát lực vặn chéo của hai người lính đặc nhiệm, toàn bộ sức mạnh Luyện Cốt sơ kỳ từ đôi cánh tay tôi bùng nổ, truyền thẳng một xung lực xoắn cực mạnh vào chốt then đồng!

*Rắc!*

Một tiếng rạn nứt giòn giã vang lên dưới đáy nước sâu.

Lớp cặn vôi hóa ngàn năm kẹp trong rãnh trượt vỡ vụn. Chiếc then cài bằng đồng đen trượt mạnh sang mạn phải một khoảng năm cen-ti-mét, ăn khớp vào rãnh hãm phụ với một tiếng *cạch* đanh gọn!

*Ầm ầm ầm!*

Ngay khoảnh khắc chiếc then cài dịch chuyển, một mảng đá ngầm bên sườn vách cống bỗng tụt sâu xuống nửa mét, mở ra một khe xả áp phụ rộng bằng hai bàn tay người lớn!

Dòng nước dồn nén nghẹt thở từ phía thượng nguồn lập tức tìm được lối thoát, cuồn cuộn ùa qua khe hở mới mở với một tốc độ kinh hoàng. Luồng áp lực thủy tĩnh khổng lồ từng đè nặng lên cửa cống chính bỗng chốc được giải tỏa hơn một nửa!

Dưới sự chênh lệch áp suất vừa được cân bằng, khối thân cây sao đen mục cùng lớp bùn khoáng kẹt cứng giữa miệng vòm Thủy Môn bỗng nhiên lung lay dữ dội. Lực hút của dòng nước xuôi dòng kéo bật gốc cây mục đầu tiên, cuốn phăng nó trôi tuột qua lòng cống ngầm, xuôi thẳng về phía cửa biển Cần Giờ!

Điểm nghẽn ngàn năm đã chính thức được khai thông!

Khi dòng chảy đáy sâu thông suốt trở lại, một hiện tượng kỳ diệu đã diễn ra ngay trước mắt chúng tôi:

Dòng xoáy nước hung hãn tại ngã ba sông Nhà Bè bắt đầu chậm dần lại, tiếng gầm rít xé lòng dưới đáy sông dịu đi rõ rệt. Trên đỉnh vòm Thủy Môn, khối cự thạch hình cầu Huyết Ngọc Trấn Ba — vốn phát ra những đợt ánh sáng đỏ rực do ma sát áp suất cao suốt buổi sáng — nay đã dần mất đi độ kích động cơ học. Ánh đỏ gay gắt mờ dần, chuyển sang một sắc hồng ấm áp rồi tắt hẳn, trở về hình hài một khối đá thạch anh chu sa phủ rêu phong sừng sững, lặng lẽ ngự trị giữa dòng nước lành.

"Báo cáo tàu điều hành: Then cài xả áp đã mở thành công! Nút cây mục đã bị dòng nước cuốn trôi! Áp lực dòng đáy giảm sáu mươi phần trăm!" Giọng Lặn 01 vang lên hào sảng qua cụm loa truyền thanh trên boong tàu.

Qua tai nghe, tôi nghe thấy tiếng hò reo vang dội của các kỹ sư, tiếng vỗ tay rộn rã của chú Tùng và Tiến sĩ Nam từ trên mặt nước vọng xuống.

"Thời gian đáy đã chạm mốc mười tám phút!" Đại úy Hùng ra lệnh dứt khoát: "Tất cả đội lặn lập tức thu hồi dây rốn, bước vào lồng an toàn! Dàn tời cáp bắt đầu quy trình kéo giảm áp!"

"Rõ!"

Tôi cùng hai người lính đặc nhiệm hải quân bước lùi lại, bước chân vào khoang lồng lặn titan. Cánh cửa thép nặng nề khép lại, then khóa gài chặt.

*Keng... Keng...*

Dây cáp chịu lực từ từ nhấc bổng lồng lặn rời khỏi đáy bùn sâu ba mươi tám mét. 

Theo đúng quy chuẩn an toàn y học dưới nước, chiếc lồng lặn dừng lại ở độ sâu mười lăm mét trong năm phút để cơ thể chúng tôi đào thải lượng khí nitơ hòa tan trong máu, rồi tiếp tục dừng ở độ sâu sáu mét và ba mét.

Trong suốt thời gian giảm áp tĩnh lặng ấy, tôi ngồi tựa lưng vào vách titan, nhắm mắt điều hòa luồng khí huyết ấm áp trong lồng ngực. Từng khớp xương ê ẩm dần hồi phục sinh lực, sự buốt giá nơi đầu ngón chân tan biến dần dưới lớp áo sưởi nhiệt.

Một giờ bốn mươi lăm phút chiều.

Cần cẩu thủy lực đưa chiếc lồng lặn chạm nhẹ xuống sàn tàu `Đại Dương 09`.

Khi cánh cửa thép mở toang, ánh nắng ban trưa rực rỡ và làn gió lộng lẫy của phương Nam ùa vào khoang lồng, xua tan hoàn toàn mùi dưỡng khí nén nhân tạo.

Tôi tháo chiếc mũ lặn nặng nề ra khỏi cổ áo, đưa tay vuốt mái tóc ướt đẫm mồ hôi.

Trước mắt tôi, mặt sông Soài Rạp đã trở lại một màu phù sa nâu đỏ hiền hòa quen thuộc. Dải sương mù xám bạc đã tan biến vào hư không, trả lại bầu trời thu xanh ngắt không một gợn mây. Xa xa, những chiếc sà lan chở cát và tàu chở dầu lại tấp nập rẽ sóng xuôi ngược trên luồng hàng hải bình yên.

Đại úy Hùng và Tiến sĩ Nam bước tới, đưa tay đỡ lấy vai tôi. Nụ cười rạng rỡ hiện rõ trên từng khuôn mặt sạm màu nắng gió.

Cửa cống Thủy Môn ngàn năm dưới đáy sông Nhà Bè đã được giải tỏa êm đềm, không cần đến một tiếng nổ bộc phá, không làm kinh động đến trật tự của thành phố mười triệu dân năm 2026.
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 44 vào manuscript...")
    with open(CH44_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã tạo tệp: {CH44_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 44 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=44,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich"],
        text=CHAPTER_CONTENT
    )
    print(f"    -> Kết quả kiểm duyệt: Passed={audit_res['passed']}, Tổng lỗi={audit_res['total_issues']}")
    if audit_res["issues"]:
        for iss in audit_res["issues"]:
            print(f"       * [{iss['category']} - {iss['severity']}]: {iss['description']}")
    
    if not audit_res["passed"]:
        print("[-] Kiểm duyệt thất bại! Có lỗi CRITICAL/HIGH.")
        return False

    # 3. Cập nhật Database
    print("[3/5] Đồng bộ trạng thái vào cơ sở dữ liệu novel_os.db...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().isoformat()
    word_count = len(CHAPTER_CONTENT.split())

    # 3.1 story_hierarchy
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, word_count, status, pov, created_at, updated_at)
    VALUES (?, 'chapter', 'mini_arc_01_03', 44, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_044", "Chương 44: Then Cài Trấn Thủy Và Dòng Chảy Hạ Lưu",
        "Minh An cùng hai thợ lặn đặc nhiệm hải quân tại độ sâu 38m đáy sông Soài Rạp tiếp cận miệng vòm Thủy Môn kẹt ba thân cây sao đen cổ thụ và phù sa chu sa. Dựa vào họa đồ lưng rùa đá Thủy Trấn Thạch (Payoff FSH-026), Minh An phát hiện then cài xả áp Ngạc Khảm bằng đồng đen. Dưới sự chỉ dẫn cơ học của Lâm Tịch về then xoắn ốc ngược, Minh An kết hợp lực Luyện Cốt sơ kỳ mở then xả áp phụ. Áp suất được giải tỏa, dòng xoáy dị thường và vệt nước đỏ lắng xuống, viên Huyết Ngọc tắt ánh sáng trở về giấc ngủ (Payoff FSH-027, tiến triển FSH-028). Đội lặn giảm áp an toàn và trở lại boong tàu Đại Dương 09.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 44, 1, '2026-10-07T14:45:00+07:00', 44, 'loc_nha_be', ?, ?, ?)
    """, (
        "EVT-CH044-01", "Chiến dịch mở then cài xả áp Thủy Môn Cổ Phách và bình ổn ngã ba sông Nhà Bè",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "chú Tùng", "Lặn 01 Dũng", "Lặn 02 Thành"], ensure_ascii=False),
        "Trưa và chiều 07/10/2026 (~13:15 - 14:45). Minh An cùng Lặn 01 và Lặn 02 khảo sát vòm Thủy Môn tại độ sâu 38m. Phát hiện búi cây mục nghẽn dòng nước sinh ra áp lực 3.2 bar chênh lệch. Dựa vào họa đồ lưng rùa đá, Minh An tìm ra then cài xả áp Ngạc Khảm bên mạn phải móng rồng. Lâm Tịch chỉ dẫn cơ chế xoắn ốc ngược, Minh An vận khí Tam Chu Thiên trợ lực mở chốt then đồng đen ngàn năm. Rãnh xả áp mở toang, dòng nước cuốn trôi nút cây nghẽn, áp lực dòng đáy giảm 60%. Viên Huyết Ngọc lắng dịu ánh sáng, mặt sông Nhà Bè trở lại màu phù sa bình thường. Đội lặn giảm áp 3 nấc và nổi lên an toàn lúc 13:45.",
        "Mở then xả áp Ngạc Khảm thành công; bình ổn hoàn toàn thủy triều đỏ và dòng xoáy ngầm ngã ba sông Nhà Bè; hoàn thành Payoff trọn vẹn FSH-026 và FSH-027, tiến triển FSH-028; hoàn tất nhiệm vụ thực địa dưới nước của Arc 1."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 44, 'loc_nha_be', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ vững vàng, trải nghiệm áp lực nước 5 bar và phát lực xoắn cơ học)",
        "Cơ bắp rã rời sau thời gian đáy 18 phút và giảm áp an toàn, màng tủy vững chắc, thể lực tiêu hao nhưng tinh thần cực kỳ tỉnh táo",
        json.dumps(["Mỏi cơ bắp bắp chân và vai nhẹ", "Màng nhĩ đã cân bằng áp suất bình thường"], ensure_ascii=False),
        json.dumps(["Bộ đồ lặn neoprene", "Bình khí Nitrox (còn 40% dung tích)", "Dao lặn & bay gạt kỹ thuật", "Điện thoại thông minh"], ensure_ascii=False),
        "Thanh thản, tự hào, cảm nhận sâu sắc giá trị của kỷ luật kỹ thuật và sự kết hợp giữa con người hiện đại với di sản tiền nhân"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 44, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (chìm vào giấc ngủ phục hồi sau khi hoàn tất hướng dẫn cơ học)",
        "Nguyên thần suy kiệt bước vào trạng thái ngủ say tĩnh dưỡng, không còn bị xáo động bởi xung lực bên ngoài",
        json.dumps(["Đạo cơ vỡ nát", "Nguyên thần ngủ say phục hồi"], ensure_ascii=False),
        json.dumps(["Thanh kiếm tàn Băng Phách Trảm Tuyết (ngủ say)"], ensure_ascii=False),
        "An lòng, tĩnh lặng, thừa nhận sự trưởng thành đáng tin cậy của Minh An"
    ))

    # 3.4 story_threads touch
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-001'
    """, ("Then cài xả áp Thủy Môn đã mở, nút nghẽn đáy sông được giải tỏa, dòng xoáy lắng dịu, cấu trúc vách đá được bảo tồn nguyên vẹn.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Minh An vượt qua thử thách lặn sâu 38m, phối hợp lực Luyện Cốt xoay then đồng ngàn năm thành công, củng cố cảnh giới sơ kỳ vững vàng.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-WLD-001'
    """, ("Chiến dịch khảo sát của tàu Đại Dương 09 và Cảng vụ Hàng hải hoàn thành xuất sắc nhiệm vụ bình ổn luồng hàng hải Soài Rạp.", now_iso))

    # 3.5 foreshadowing update
    cur.execute("""
    UPDATE foreshadowing_ledger SET status = 'PAID', payoff_chapter = 44 WHERE id = 'FSH-026'
    """)
    cur.execute("""
    UPDATE foreshadowing_ledger SET status = 'PAID', payoff_chapter = 44 WHERE id = 'FSH-027'
    """)
    cur.execute("""
    UPDATE foreshadowing_ledger SET status = 'ACTIVE' WHERE id = 'FSH-028'
    """)

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 44...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH44_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 44.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_044.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 44: Then Cài Trấn Thủy Và Dòng Chảy Hạ Lưu",
        chapter_num=44,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT SOẠN THẢO CHƯƠNG 44 THÀNH CÔNG ===")
    else:
        sys.exit(1)

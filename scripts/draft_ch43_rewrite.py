# -*- coding: utf-8 -*-
"""Script viết lại bản thảo Chương 43: Thủy Môn Cổ Phách Và Dấu Vết Vực Sâu Ngoại Giới."""

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
CH43_PATH = os.path.join(MANUSCRIPT_DIR, "ch_043.md")

CHAPTER_CONTENT = """---
chapter: 43
title: "Thủy Môn Cổ Phách Và Dấu Vết Vực Sâu Ngoại Giới"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Ngã ba sông Nhà Bè (độ sâu 40m), TP.HCM"
date: "2026-10-07"
word_count: 2850
---

# Chương 43: Thủy Môn Cổ Phách Và Dấu Vết Vực Sâu Ngoại Giới

Mười hai giờ bốn mươi phút trưa ngày mùng bảy tháng Mười năm 2026.

Tại tâm điểm ngã ba sông Nhà Bè — nơi dòng nước sông Sài Gòn và sông Đồng Nai cuộn trào hợp lưu trước khi tách thành hai luồng Soài Rạp và Lòng Tàu đổ ra biển Cần Giờ — con tàu khảo sát viễn thám `Đại Dương 09` đã buông bốn mỏ neo trọng tải lớn, ghìm mình vững chãi giữa những đợt sóng đỏ ngầu phù sa.

Thế nhưng, bầu không khí bao trùm mặt sông lúc này không hề mang vẻ yên ả của một ngày thu phương Nam.

Một màn sương mù xám bạc dày đặc bốc lên cuồn cuộn từ mặt nước, tỏa ra một mùi hương ngai ngái nồng đượm của khoáng thạch cổ xưa và lưu huỳnh đáy biển. Tầm nhìn của hoa tiêu trên đài chỉ huy bị bóp nghẹt xuống dưới năm mươi mét. Ánh nắng gắt gao ban trưa khi rọi qua màn sương quánh đặc ấy bỗng biến thành một thứ ánh sáng lờ nhờ màu chì ma quái.

Trong phòng điều hành tác chiến của tàu, không khí căng thẳng như một sợi dây đàn sắp đứt.

"Báo cáo Viện trưởng Nam, cụm cảm biến lượng tử đo trường biến thiên đáy sâu bắt đầu nhảy loạn xạ!" Kỹ sư Tuấn nhìn chằm chằm vào màn hình máy chủ, mồ hôi rịn ra trên trán: "Độ lệch từ trường khu vực ngã ba sông đã vượt ngưỡng bốn trăm nanoTesla, tăng gấp sáu lần mức bình thường! Nghiêm trọng hơn, mô hình quét sonar 3D đáy sông liên tục báo lỗi ma trận điểm ảnh — dường như có một trường lực vô hình đang bẻ cong cả sóng âm phản xạ!"

Tiến sĩ Trịnh Hoài Nam đứng bên bàn sa bàn số, hai tay chống chặt lên mép bàn, vẻ mặt ngưng trọng tột độ. Ông quay sang chú Phan Thanh Tùng:

"Chú Tùng, các bản dập văn tự cổ trên lưng rùa đá Thủy Trấn Thạch ở Thủ Thiêm có ghi nhận hiện tượng bẻ cong sóng âm và từ trường xoắn ốc như thế này không?"

Chú Tùng run rẩy lật từng trang tài liệu dập rập Hán Nôm màu mực nho, lắc đầu với đôi mắt trũng sâu:

"Không có... Cổ tịch thời Nguyễn và các ghi chép địa chí phương Nam chỉ nói rằng ngã ba sông Nhà Bè là nơi 'Giao long tụ hội, sóng đỏ trào dâng, đáy sông có cổng đá trấn giữ khí mạch'. Nhưng những gì đang hiển thị trên máy móc của chúng ta trưa nay... dường như không phải là hiện tượng thủy văn tự nhiên đơn thuần."

Đứng cạnh họ, trong bộ quân phục dã chiến của Viện Nghiên cứu Địa tầng và Năng lượng Nội sinh Đô thị, tôi không cần nhìn vào màn hình máy tính để biết chuyện gì đang xảy ra.

Nhờ thành tựu Luyện Cốt Hóa Tủy tầng hai — Cốt Tủy Thông Minh — đạt được đêm qua, hai trăm linh sáu mảnh xương trên toàn thân thể tôi đang run rẩy từng hồi đau buốt. Đó không phải là nỗi đau do va đập cơ học, mà là một cảm giác buốt giá xuyên thấu tủy sống, giống như có hàng ngàn mũi kim băng giá vô hình đang chọc thẳng vào các khớp xương.

Một luồng khí tức tịch diệt, tàn khốc và hoàn toàn xa lạ đang từ dưới độ sâu bốn mươi mét lòng bùn bốc lên cuồn cuộn.

*"Minh An..."*

Trong thức hải của tôi, thanh âm của Lâm Tịch bỗng vang lên. Nhưng khác hẳn với sự điềm đạm, lạnh lùng thường ngày của một nữ kiếm tiên viễn cổ, giọng nói của nàng lúc này ngập tràn một sự kinh hoàng chưa từng thấy:

*"Khí tức này... Không thể nào... Tại sao lại có dấu vết của bọn chúng ở một nơi phàm trần như thế này?!"*

"Lâm Tịch, rốt cuộc dưới đáy sông kia là cái gì?" Tôi lập tức truyền ý niệm gặng hỏi.

Hư ảnh của Lâm Tịch hiện ra trong tâm thức tôi, sắc mặt nàng trắng bệch không còn một giọt máu, đôi mắt nhìn chằm chằm về hướng hạ lưu với sự cảnh giác tột độ:

*"Đó không phải là năng lượng long mạch... Càng không phải là sự cố đứt gãy địa tầng phàm trần! Đó là **Hư Không Tha Hóa Khí**... Dấu vết của thế lực hủy diệt từng giáng xuống cõi Cố Thổ của ta năm xưa, xé rách chín tầng trời, biến hàng ngàn tông môn vĩ đại thành bình địa tro tàn!*

*Năm xưa, khi các bậc đại năng Khí Huyết Đạo liên thủ thiết lập đại trận phong ấn cõi đất này, họ đã dùng Thủy Môn để chặn đứng cửa biển phương Nam. Nhưng bây giờ... phong ấn dưới đáy sông đang rò rỉ! Lực lượng tha hóa từ vực sâu biển cả đang men theo vết nứt ngoài khơi âm thầm gặm nhấm cánh cổng ngầm!"*

Trái tim tôi đập thắt lại.

Vết rạn phong ấn viễn cổ! Lực lượng tha hóa từ biển sâu!

Những lời nói của Lâm Tịch như một quả bom sấm sét nổ tung trong tâm trí tôi, đập tan hoàn toàn những suy nghĩ ngây thơ trước đây. Hóa ra, những sự cố sụt lún ở Ba Son, rung chấn ở Thủ Thiêm hay thủy triều đỏ ở Nhà Bè không phải là những sự kiện ngẫu nhiên riêng lẻ của tự nhiên. Chúng là những dấu hiệu cảnh báo đầu tiên cho thấy chiếc lồng phong ấn bảo vệ cõi đất này suốt muôn vàn năm qua đang bước vào thời kỳ rạn nứt!

Và nếu cánh cổng Thủy Môn này sụp đổ, thứ tràn vào thành phố mười triệu dân không chỉ là nước sông ngập lụt, mà là sự tha hóa hủy diệt của chiều không gian bên ngoài!

"Báo cáo Giám đốc Minh An, buồng lặn áp lực cao titan đã được đưa vào vị trí cẩu!" Đại úy Trần Văn Hùng bước vào phòng điều hành, quân phục ướt đẫm hơi sương mặn: "Đội lặn đặc nhiệm gồm Lặn 01 đồng chí Dũng, Lặn 02 đồng chí Thành và tôi đã sẵn sàng. Nhưng theo quy chuẩn an toàn hàng hải, với độ lệch từ trường và dòng xoáy dị thường cấp độ bốn này, việc lặn xuống đáy sâu bốn mươi mét là cực kỳ nguy hiểm!"

Tôi quay người lại, ánh mắt kiên định nhìn thẳng vào Đại úy Hùng và Tiến sĩ Nam:

"Đại úy Hùng, anh ở lại boong tàu chỉ huy trung tâm điều phối và giám sát thông số sống. Tôi sẽ trực tiếp xuống đáy sông cùng đồng chí Dũng và đồng chí Thành."

"Cậu An, không thể mạo hiểm như vậy!" Tiến sĩ Nam giật mình can ngăn: "Cậu là Giám đốc Kỹ thuật Dữ liệu, là linh hồn phân tích toán học của toàn bộ Viện! Nếu xảy ra sự cố áp suất hay trượt lở đáy bùn..."

"Chính vì tôi hiểu rõ cấu trúc dữ liệu của Thủy Môn nhất nên tôi bắt buộc phải xuống," tôi ngắt lời ông, giọng nói bình thản nhưng chứa đựng một sức nặng không thể chối từ: "Thiết bị điện tử đã bị nhiễu loạn sóng âm, camera quang học dưới làn nước đỏ này tầm nhìn không quá một mét. Chỉ có trực giác định vị cơ học và khả năng cảm ứng trường lực của tôi mới có thể xác định được then chốt của công trình ngầm. Nếu chần chừ thêm một giờ nữa khi con nước ròng rút cạn, áp lực chênh lệch sẽ xé toạc toàn bộ chân đế đáy sông!"

Nhìn thấy ánh mắt sáng quắc, bất biến như bàn thạch của tôi, Tiến sĩ Nam lặng người đi một nhịp, rồi thở dài gật đầu:

"Được... Bảo trọng, Minh An! Toàn bộ nguồn lực của tàu `Đại Dương 09` sẽ hỗ trợ cậu đến cùng!"

Một giờ trưa.

Tôi cùng hai chiến sĩ người nhái dạn dày kinh nghiệm nhất của Đội Đặc nhiệm Hải quân bước vào khoang buồng lặn áp lực cao bằng hợp kim titan. 

Cánh cửa thép tròn dày hai mươi phân đóng sầm lại, tiếng van thủy lực khóa chặt vang lên những tiếng *cạch... cạch* đanh gọn. Chúng tôi mang trên mình bộ đồ lặn dã chiến chuyên dụng bằng cao su neoprene bọc sợi kevlar, đeo bình khí thở hỗn hợp Nitrox và đội chiếc mũ lặn áp lực cao có tích hợp đèn halogen công suất ba ngàn watt.

*Rắc... Rắc...*

Cần cẩu thủy lực trên boong tàu từ từ nhấc bổng khối lồng lặn nặng bốn tấn rời khỏi sàn tàu, thả dần xuống mặt nước đỏ ngầu của ngã ba sông Nhà Bè.

*Ùm!*

Bọt nước đỏ ngầu bắn tung tóe. Toàn bộ thế giới bên ngoài cửa kính quan sát lập tức chuyển sang một màu đỏ sẫm như máu loãng. 

Mười mét... Hai mươi mét... Ba mươi mét...

Chiếc lồng lặn hạ sâu dần vào lòng sông Soài Rạp. Áp suất thủy tĩnh bên ngoài tăng vọt theo từng mét độ sâu, đè nặng lên lớp vỏ hợp kim titan khiến thân lồng phát ra những tiếng cọt kẹt âm u rợn người. 

Khi đồng hồ đo độ sâu điểm con số ba mươi tám mét, chiếc lồng lặn chạm nhẹ vào lớp bùn nhão đáy sông.

"Lặn 01, Lặn 02, chuẩn bị xuất khoang!" Giọng tôi vang lên qua micro mũ lặn.

"Rõ!" Hai người lính đặc nhiệm hải quân dứt khoát kiểm tra lại dây cáp rốn bọc thép định vị và mở chốt cửa thoát hiểm đáy lồng.

Dòng nước lạnh buốt ập vào khoang ngập tới ngực. Chúng tôi bước chân ra khỏi lồng lặn, dẫm chân lên tầng trầm tích đáy sâu ngã ba sông Nhà Bè.

Dưới độ sâu gần bốn mươi mét, áp suất nước lên tới gần năm atmosphere ép chặt vào lồng ngực tôi. Nếu không có khung xương tủy Luyện Cốt sơ kỳ vững chắc nâng đỡ các cơ quan nội tạng và nhịp thở Tam Chu Thiên liên tục điều hòa áp lực máu, một người bình thường dù có mặc đồ lặn chuyên dụng cũng sẽ bị tức ngực, màng nhĩ đau buốt đến ngất lịm.

Tôi đưa tay bật ngọn đèn chiếu điểm cực mạnh gắn trên vai.

Luồng ánh sáng vàng đậm xé toạc màn nước đỏ quạch phù sa, rọi thẳng về phía trước.

Và ngay khoảnh khắc luồng sáng chạm tới đáy sâu, cả ba chúng tôi đều chết lặng vì kinh ngạc:

Cách vị trí lồng lặn chưa đầy mười mét, một vòm cổng đá khổng lồ sừng sững trồi lên khỏi lớp phù sa đáy sông!

Đó là một công trình kỳ vĩ được ghép từ hàng ngàn phiến đá thanh hoa màu xám đen, mỗi phiến đá nặng hàng chục tấn, được đẽo gọt vuông vức và khớp nối khít khao đến mức không thể nhét lọt một mũi dao. Vòm cổng cao hơn sáu mét, rộng gần mười mét, uốn lượn thành hình hai móng rồng khổng lồ cắm sâu vào lòng đất mẹ phương Nam. Trên bề mặt phiến đá, những đường vân phù điêu cổ xưa khắc họa hình tượng sông núi, sóng thần và những ký tự đạo văn viễn cổ chìm nổi dưới lớp trầm tích ngàn năm.

Đó chính là **Thủy Môn Cổ Phách** — chiếc then cài trấn thủy tối thượng của vùng châu thổ!

Thế nhưng, điều khiến toàn thân tôi lạnh toát không phải là sự đồ sộ của công trình ngầm, mà nằm ở cảnh tượng hãi hùng đang diễn ra ngay trên đỉnh vòm cổng đá:

Ngay giữa tâm vòm móng rồng, một khối cự thạch hình cầu có đường kính gần một mét — viên **Huyết Ngọc Trấn Ba** — đang lập lòe phát ra từng đợt ánh sáng đỏ rực tựa như máu tươi. Ánh sáng ấy không hề ấm áp, mà giật giãy từng hồi hỗn loạn như một trái tim đang đập những nhịp đập cuối cùng trong cơn hấp hối.

Và bao bọc quanh viên Huyết Ngọc cùng toàn bộ chân đế vòm đá...

Là hàng vạn **sợi tơ đen kịt u ám**!

Chúng mảnh như sợi tóc nhưng đặc quánh như hắc ín, không ngừng ngoe nguẩy, bò trườn như những xúc tu vô hình bò ra từ một khe nứt không gian đen ngòm nằm sâu dưới chân móng Thủy Môn. Mỗi nơi mà sợi tơ đen ấy bò qua, lớp đá thanh hoa ngàn năm tuổi liền phát ra những tiếng xèo xèo rợn tóc gáy, bề mặt đá bị gặm nhấm mục ruỗng, hóa thành những mảng cát đen rỉ sét trôi lơ lửng trong làn nước!

Cái lạnh tịch diệt mà tôi cảm nhận được từ trên boong tàu chính là phát ra từ những sợi tơ đen này!

*"Đúng là nó... Hư Không Tha Hóa!"* Tiếng Lâm Tịch thét lên trong tâm thức tôi, run rẩy và đau đớn tột cùng: *"Khe nứt phong ấn đáy biển ngoài khơi đã vỡ một góc! Luồng hắc khí tha hóa này đang muốn hủy diệt viên Huyết Ngọc Trấn Ba để xé toạc hoàn toàn lối vào đất liền! Viên ngọc đang dốc cạn năng lượng bản nguyên để chống cự, tạo ra dòng nước đỏ chu sa nhằm xua đuổi tà khí... Nhưng nó sắp không chống đỡ nổi nữa rồi!"*

"Báo cáo tàu điều hành... Chúng tôi nhìn thấy... nhìn thấy..." Giọng người lính đặc nhiệm mang mã hiệu Lặn 01 bên cạnh tôi bỗng lắp bắp qua bộ đàm vô tuyến, hơi thở của anh dồn dập bất thường: "Có... có cái gì đó màu đen... đang chuyển động quanh khối đá..."

"Lặn 01! Bình tĩnh! Lùi lại ngay!" Tôi quát lớn qua micro, đưa tay giật mạnh dây cáp hãm của anh.

Nhưng đã quá muộn.

Sự xuất hiện của luồng ánh sáng đèn halogen cực mạnh và sóng vô tuyến từ bộ đàm của chúng tôi dường như đã đánh động đến thực thể u ám dưới đáy sâu!

*Xì xì xì...*

Đám tơ đen quấn quanh viên Huyết Ngọc bỗng nhiên co giật dữ dội. 

Từ khe nứt đen ngòm dưới chân móng Thủy Môn, một luồng hắc khí cuồn cuộn trào ra như mực đen đổ vào nước, lập tức hòa vào dòng nước ngầm bốn mươi mét tạo thành một cơn lốc xoáy màu đen kịt hung hãn!

Dòng xoáy nước đen rít lên từng hồi gầm rú đinh tai nhức óc, cuốn phăng lớp bùn cát đáy sông, biến ngã ba sông Nhà Bè thành một địa ngục tối tăm không lối thoát!

*Keng!*

Một sợi tơ đen bay vụt qua làn nước, quẹt trúng cánh tay phải bọc giáp titan của Lặn 01.

Trong tích tắc, trước mắt tôi, lớp hợp kim titan chống ăn mòn biển sâu dày ba mi-li-mét bỗng nhiên xám xịt lại, nứt toác rồi rỉ sét mục nát như một mảnh sắt vụn ngâm trong axit đậm đặc hàng chục năm!

"Aaa!" Tiếng thét đau đớn của Lặn 01 vang lên qua tai nghe khi khí lạnh tha hóa ngấm qua lớp vải lót, đâm thẳng vào da thịt. Cảm biến sinh học trên mũ lặn của anh lập tức nhấp nháy đèn đỏ báo động: Nhịp tim tụt dốc không phanh từ tám mươi xuống còn bốn mươi nhịp trên phút!

"Đồng chí Thành! Đưa Dũng lùi về lồng lặn ngay lập tức! Bật van sưởi khẩn cấp!" Tôi gào lên qua bộ đàm, một tay đẩy mạnh người lính đặc nhiệm về phía cửa lồng titan.

"Còn cậu An thì sao?!" Lặn 02 hoảng hốt kêu lên giữa dòng nước xoáy đen ngòm đang cuộn trào dữ dội.

"Tôi bọc hậu! Đóng cửa lồng lại ngay!"

Tôi gạt phăng mọi sự chần chừ, bước một bước dài chắn ngang trước cửa lồng lặn.

Xung quanh tôi, dòng xoáy hắc khí đen ngòm đang bốc lên ngùn ngụt, bao vây lấy vòm cổng Thủy Môn và ép chặt lấy toàn bộ không gian đáy sông sâu bốn mươi mét. Viên Huyết Ngọc Trấn Ba trên đỉnh vòm phát ra những tia sáng đỏ rực cuối cùng trong tuyệt vọng, tiếng rạn nứt của đá khối cổ xưa vang lên răng rắc giữa màn nước đen kịt!

Đứng trước sự xâm thực tàn bạo của lực lượng tha hóa từ cõi vực sâu ngoài hành tinh, lần đầu tiên trong đời, tôi cảm nhận sâu sắc sự nhỏ bé, mong manh và bất lực của một phàm nhân bằng xương bằng thịt.

Nhưng sâu trong lồng ngực tôi, dòng máu Tam Chu Thiên bỗng nhiên sôi trào cuộn sóng, và hai trăm linh sáu mảnh xương tủy kiên định của tôi cất lên một tiếng ngân vang đầy kiêu hãnh giữa bóng tối ngàn trùng!
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 43 viết lại vào manuscript...")
    with open(CH43_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã cập nhật tệp: {CH43_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 43 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=43,
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
    VALUES (?, 'chapter', 'mini_arc_01_03', 43, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_043", "Chương 43: Thủy Môn Cổ Phách Và Dấu Vết Vực Sâu Ngoại Giới",
        "Tàu Đại Dương 09 buông neo tại ngã ba sông Nhà Bè lúc 12:40 trong màn sương mù xám bạc và từ trường hỗn loạn. Minh An cùng hai thợ lặn đặc nhiệm hải quân hạ lồng xuống độ sâu 40m đáy sông Soài Rạp. Họ phát hiện Thủy Môn Cổ Phách và viên Huyết Ngọc Trấn Ba đang bị quấn quanh bởi những sợi tơ hắc khí lạnh buốt — dấu vết của lực lượng Hư Không Tha Hóa từ rãnh biển sâu ngoài khơi Cần Giờ gặm nhấm phong ấn viễn cổ. Lâm Tịch kinh hoàng nhận ra kẻ thù diệt thế viễn cổ, hé lộ sự thật Trái Đất là Vị Diện Phong Ấn Tầng Thứ Sáu. Luồng hắc khí bị kích động bùng phát lốc xoáy đen ngầm, ăn mòn lớp giáp titan của thợ lặn Lặn 01. Minh An đẩy đồng đội về lồng an toàn, một mình đứng chặn trước dòng xoáy hắc ám để bảo vệ Thủy Môn.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 43, 1, '2026-10-07T13:15:00+07:00', 43, 'loc_nha_be', ?, ?, ?)
    """, (
        "EVT-CH043-01", "Khảo sát đáy sâu 40m Nhà Bè và phát hiện dấu vết Hư Không Tha Hóa xâm thực Thủy Môn",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "chú Tùng", "Lặn 01 Dũng", "Lặn 02 Thành"], ensure_ascii=False),
        "Trưa 07/10/2026 (~12:40 - 13:15). Tàu Đại Dương 09 ghi nhận dị thường từ trường và sóng âm tại ngã ba sông Nhà Bè. Minh An dẫn đầu đội lặn áp lực cao tiếp cận độ sâu 40m đáy sông Soài Rạp. Phát hiện Thủy Môn Cổ Phách và viên Huyết Ngọc Trấn Ba đang bị ăn mòn bởi hắc khí Hư Không Tha Hóa từ biển sâu tràn vào. Lâm Tịch xác nhận Trái Đất là vị diện phong ấn tầng thứ sáu đang bị rạn nứt. Luồng hắc khí kích động tạo xoáy nước đen, ăn mòn giáp titan của Lặn 01. Minh An yểm trợ đồng đội rút lui an toàn, một mình đối mặt hiểm nguy tột cùng.",
        "Phát hiện chấn động: Trái Đất là vị diện phong ấn tầng 6 và phong ấn đang bị xâm thực từ biển sâu; Lặn 01 bị thương do hắc khí; Minh An một mình đứng lại trước Thủy Môn đối mặt cơn lốc xoáy hắc ám."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 43, 'loc_nha_be', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ, Tam Chu Thiên vận khí chống cự áp suất nước 5 bar và khí lạnh tha hóa)",
        "Thể xác căng thẳng tột độ dưới áp lực nước 40m, xương tủy đau buốt do tiếp xúc khí tức Hư Không, khí huyết sôi trào bảo vệ tim mạch",
        json.dumps(["Khớp xương buốt nhức do khí lạnh tha hóa"], ensure_ascii=False),
        json.dumps(["Bộ đồ lặn neoprene bọc kevlar", "Bình khí Nitrox", "Mũ lặn áp lực cao đèn halogen", "Chiếc trâm ngọc cổ"], ensure_ascii=False),
        "Kinh hoàng trước bí mật phong ấn vị diện nhưng ý chí sắt đá, quyết tâm bảo vệ đồng đội và trật tự nhân gian"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 43, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (chấn động tột cùng khi chạm trán khí tức kẻ thù diệt thế Cửu U Vực Sâu)",
        "Nguyên thần rung chuyển, tàn lực bị kích động, ký ức phong ấn vị diện tầng 6 thức tỉnh một phần",
        json.dumps(["Đạo cơ vỡ nát", "Tàn hồn chấn động dữ dội"], ensure_ascii=False),
        json.dumps(["Bản thể kiếm tàn Băng Phách Trảm Tuyết"], ensure_ascii=False),
        "Kinh hãi, căm phẫn, lo lắng tột cùng cho an nguy của Minh An trước thế lực Hư Không Tha Hóa"
    ))

    # 3.4 story_threads
    # Mở story thread mới cho tầm vóc 3000 chương!
    cur.execute("""
    INSERT OR REPLACE INTO story_threads (thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter, status, current_state, known_info, hidden_info, reader_knowledge, last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at)
    VALUES (?, ?, ?, ?, 43, 500, 'ACTIVE', ?, ?, ?, ?, 43, 20, 'HIGH', 'CRITICAL', ?, ?)
    """, (
        "TH-MYS-003", "MYSTERY", "Sự Rạn Nứt Của Lưới Phong Ấn Trái Đất (Cực Tù Tầng 6)",
        "Trái Đất là vị diện phong ấn tầng thứ sáu do đại năng viễn cổ thiết lập để cách ly hoặc giam cầm một bí mật vũ trụ. Chu kỳ phong ấn vạn năm đang suy thoái, khiến các vết rạn xuất hiện dọc theo các rãnh biển sâu và long mạch toàn cầu, để lộ khe hở cho Hư Không Tha Hóa xâm nhập.",
        "Phát hiện dấu vết Hư Không Tha Hóa đầu tiên tại Thủy Môn Nhà Bè, xác nhận Trái Đất là vị diện phong ấn tầng thứ sáu.",
        "Minh An và Lâm Tịch đã chứng kiến hắc khí tha hóa ăn mòn Thủy Môn dưới đáy sông 40m.",
        "Nguyên nhân Trái Đất bị biến thành nhà tù phong ấn tầng 6 và thực thể bị phong ấn sâu trong lõi hành tinh là gì.",
        "Người đọc bắt đầu nhận ra quy mô thực sự của thế giới không chỉ gói gọn trong đô thị Sài Gòn mà gắn liền với vận mệnh vũ trụ.",
        now_iso, now_iso
    ))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 43, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-001'
    """, ("Thủy Môn Cổ Phách lộ diện là Trấn Hải Chi Môn bảo vệ cửa biển phương Nam, đang bị hắc khí Hư Không Tha Hóa tấn công.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 43, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Minh An đối mặt với áp lực nước 40m và khí tức tịch diệt của Hư Không, vận khí Tam Chu Thiên kiên cường trụ vững.", now_iso))

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 43...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH43_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 43.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_043.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 43: Thủy Môn Cổ Phách Và Dấu Vết Vực Sâu Ngoại Giới",
        chapter_num=43,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT VIẾT LẠI CHƯƠNG 43 THÀNH CÔNG ===")
    else:
        sys.exit(1)

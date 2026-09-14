# -*- coding: utf-8 -*-
"""Script soạn thảo và kiểm duyệt bản thảo Chương 45: Ánh Đèn Bình Thạnh Và Giấc Ngủ Trầm Miên."""

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
CH45_PATH = os.path.join(MANUSCRIPT_DIR, "ch_045.md")

CHAPTER_CONTENT = """---
chapter: 45
title: "Ánh Đèn Bình Thạnh Và Giấc Ngủ Trầm Miên"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Cảng Tân Thuận (Quận 7) & Phòng trọ Bình Thạnh, TP.HCM"
date: "2026-10-07"
word_count: 2715
---

# Chương 45: Ánh Đèn Bình Thạnh Và Giấc Ngủ Trầm Miên

Ba giờ ba mươi phút chiều.

Chiếc tàu khảo sát `Đại Dương 09` từ từ giảm tốc độ, rẽ những lọn sóng đục ngầu phù sa tấp vào cầu cảng Tân Thuận ở mạn Quận 7.

Tiếng còi tàu rúc lên một hồi dài báo hiệu cập bến, xé toạc không gian oi nồng của buổi xế trưa phương Nam. Xung quanh tôi, nhịp điệu thường nhật của cảng biển sầm uất nhất nhì thành phố lập tức ùa vào màng nhĩ: tiếng cần cẩu khổng lồ gầm gừ nâng những thùng hàng container bốn mươi feet, tiếng còi xe đầu kéo bấm inh ỏi, tiếng những người công nhân mặc áo phản quang vàng huýt sáo chuyền dây buộc mũi tàu.

Đứng bên lan can boong tàu, tôi hít một hơi thật sâu làn gió lộng mang theo mùi dầu máy, mùi gỉ sắt và mùi nước ngọt sông ngòi. Sau gần một giờ đồng hồ giam mình dưới áp lực năm mươi mét nước buốt giá, được hít thở bầu không khí ngập tràn hơi ấm trần gian này bỗng trở thành một đặc ân giản dị đến nghẹn ngào.

"Cậu An, vào phòng điều hành ký biên bản xác nhận số liệu đo đạc nào!"

Tiếng Tiến sĩ Trịnh Hoài Nam vọng ra từ cửa cabin chỉ huy. Tôi quay người bước vào trong.

Trên chiếc bàn hội chẩn bằng inox trải rộng các bản đồ trắc đạc thủy văn và màn hình biểu đồ áp lực nước vừa được cập nhật trực tiếp từ các cảm biến thả nổi ở ngã ba sông Nhà Bè. Đại úy Hùng và chú Phan Thanh Tùng đang chăm chú soi từng đường cong đồ thị.

"Số liệu cuối cùng trước khi chúng ta nhổ neo đây," Tiến sĩ Nam đẩy gọng kính cận, chỉ đầu bút dạ vào dải đồ thị màu xanh lá cây đang duỗi thẳng tắp: "Sau khi then xả áp phụ được mở ra và nút cây mục bị cuốn trôi, lưu tốc dòng chảy ngầm ở đáy sông Soài Rạp đã giảm từ hai phẩy sáu mét trên giây xuống còn không phẩy bảy mét trên giây — hoàn toàn nằm trong ngưỡng an toàn thủy lực tự nhiên. Chênh lệch áp suất thủy tĩnh giữa hai vách Thủy Môn đã triệt tiêu hoàn toàn về mức không."

"Còn khối đá hình cầu trên đỉnh vòm thì sao, anh Nam?" Tôi hỏi, mắt hướng về bức ảnh chụp quang phổ hồng ngoại.

"Cảm biến nhiệt và bức xạ cơ học ghi nhận nó đã hoàn toàn nguội đi," Tiến sĩ Nam gật đầu, vẻ mặt nhẹ nhõm rõ rệt: "Nhiệt độ bề mặt khối đá thạch anh chu sa đã hạ xuống mười tám độ xê, đồng nhất với nhiệt độ lớp nước bùn đáy sâu. Hiện tượng ma sát áp điện gây ra ánh đỏ và kích động dòng xoáy đã biến mất một trăm phần trăm. Khối cự thạch đó đã trở về trạng thái trơ về mặt vật lý."

Chú Tùng lật nhẹ cuốn sổ tay bìa da cũ kỹ, cẩn thận ghi lại từng chỉ số bằng chiếc bút máy đã mòn ngòi:

"Tổ tiên chúng ta ngày xưa chọn đúng vị trí đới đứt gãy để dựng đập xả áp ngầm quả thực là một kỳ tích xây dựng. Họ không hề chống lại sức mạnh của dòng sông; họ chỉ nắn dòng, tạo then cài để điều tiết khi con nước đỏ thượng nguồn đổ về quá xiết. May mắn là chúng ta đã tìm ra then trượt Ngạc Khảm đúng lúc, không làm tổn hại đến di sản ngàn năm dưới đáy bùn."

Đại úy Hùng đặt chiếc bút bi xuống góc bàn, dập dấu mộc đỏ chót của Đội Đặc nhiệm Hải quân lên ba bản báo cáo kỹ thuật:

"Báo cáo gửi Cảng vụ Hàng hải TP.HCM và Ủy ban Nhân dân Thành phố đã được biên soạn theo đúng quy chuẩn khoa học: Điểm nghẽn dòng chảy tại luồng hàng hải Soài Rạp do trầm tích và chướng ngại vật hữu cơ tích tụ lâu năm gây ra chênh lệch áp suất đáy đã được khảo sát và xử lý giải tỏa an toàn bằng phương án tháo gỡ cơ học; luồng hàng hải chính thức mở lại cho tàu trọng tải lớn lưu thông từ mười sáu giờ chiều nay."

Không có một chữ nào về huyền thuật, không có một dòng nào nhắc tới những hiện tượng vượt ngoài tầm hiểu biết của phàm trần. Đó là sự chuẩn mực tuyệt đối của kỷ luật hành chính và an ninh trật tự. Thế giới hiện đại vận hành dựa trên những chứng cứ đo đạc rõ ràng, và trật tự của mười triệu cư dân thành phố được bảo toàn nguyên vẹn sau lớp vỏ bọc bình yên ấy.

"Cậu An," Đại úy Hùng bước tới, siết chặt bàn tay tôi bằng cái bắt tay rắn rỏi của người lính biển: "Cảm ơn cậu. Tinh thần bình tĩnh và khả năng thích ứng với áp suất nước sâu của cậu khiến toàn đội lặn vô cùng nể phục. Số điện thoại của tôi cậu đã lưu rồi, sau này nếu có dịp ghé qua Lữ đoàn, tôi mời cậu bữa cơm thân mật."

"Cảm ơn Đại úy, cảm ơn chú Tùng và anh Nam đã hỗ trợ tôi suốt chuyến đi," tôi cười đáp lễ.

Năm giờ chiều.

Tôi bước xuống cầu cảng, đi bộ vào bãi giữ xe của trạm bảo vệ Cảng vụ. Nhận lại chiếc ba lô vải dù sờn góc cùng chùm chìa khóa, tôi dắt chiếc xe Wave Alpha bạc màu quen thuộc ra khỏi hàng xe.

*Bẹp... Bẹp... Tạch tạch tạch!*

Cú đạp nổ máy dứt khoát làm ống bô xe rung lên từng nhịp giòn tan, nhả ra làn khói mỏng thơm mùi xăng quen thuộc. Cảm giác ngồi lên chiếc yên xe máy hơi cứng, đội chiếc mũ bảo hiểm nửa đầu cũ kỹ và nắm lấy tay ga bằng đôi bàn tay còn vương chút vết hằn của găng tay cao su dày cộp kéo tôi trở về nguyên vẹn với thân phận của một thanh niên công sở bình thường giữa lòng Sài Gòn.

Tôi hòa mình vào dòng xe cộ ken đặc trên đường Huỳnh Tấn Phát.

Giờ tan tầm của một ngày thứ Tư giữa tháng Mười. Cầu Tân Thuận nối sang đường Nguyễn Tất Thành đặc quánh những hàng xe máy nối đuôi nhau nhích từng mét một dưới ánh nắng chiều vàng vọt. Tiếng còi xe máy bấm giục giã, tiếng động cơ gầm gừ, mùi khói xe nồng nặc hòa cùng tiếng cười nói rôm rả của từng tốp học sinh trường Nguyễn Tất Thành vừa tan tiết học chiều. 

Chạy men theo bờ sông qua cầu Khánh Hội, nhìn sang mạn bến Bạch Đằng và những tòa cao ốc bằng kính sáng loáng của Quận 1 đang bắt đầu lên đèn, tôi bỗng nhận ra sự tương phản kỳ vĩ của cuộc đời: Mới hai tiếng trước, tôi còn ở dưới độ sâu gần bốn mươi mét bùn lầy tối tăm, đối mặt với hàng vạn tấn nước nén nghẹt thở và công trình ngầm ngàn năm tuổi; còn lúc này, tôi đang kẹt giữa làn xe máy trên đường Tôn Đức Thắng, lo lắng xem chút nữa qua ngã tư Hàng Xanh có bị ngập nước hay không.

Sáu giờ ba mươi phút chiều.

Bụng tôi réo lên từng hồi cồn cào dữ dội. Lượng calo khổng lồ tiêu hao trong mười tám phút lặn sâu và cú vận chuyển Khí Huyết xoay then đồng đang khiến từng tế bào trong cơ thể tôi đòi hỏi năng lượng bù đắp.

Tôi tấp xe vào một quán cơm tấm bình dân quen thuộc bên vỉa hè đường Ung Văn Khiêm, Bình Thạnh.

Khói than nướng thịt sườn bay nghi ngút từ chiếc bếp lò đặt ngay trước cửa quán, tỏa ra một mùi thơm ngậy đến tê dại khứu giác.

"Cho con một đĩa sườn bì chả trứng ốp la, thêm chén mỡ hành tóp mỡ với đĩa cơm thêm nha cô Năm!" Tôi gọi to khi vừa bước vào chiếc bàn inox trong góc.

"Có ngay con ơi! Bữa nay nhìn thằng nhỏ coi bộ hốc hác dữ, đi làm công trình ngoài nắng về hả mậy?" Người phụ nữ đứng bếp đon đả vừa lật miếng sườn vàng ươm vừa cười hỏi.

"Dạ, con mới đi khảo sát ven sông về cô." Tôi cười xòa.

Năm phút sau, đĩa cơm tấm đầy ắp được bưng ra: miếng sườn cốt lết nướng cháy cạnh thơm lừng, miếng chả trứng vàng ruộm, sợi bì dai mềm rắc đẫm hành lá phi mỡ bóng loáng, kèm theo một chén canh xà lách xoong nấu thịt bằm nóng hổi và chén nước mắm tỏi ớt kẹo ngọt cay nồng.

Tôi cầm muỗng nĩa, cắm cúi ăn một mạch. Vị ngọt đậm đà của thịt, vị bùi béo của mỡ hành, hạt cơm tấm khô ráo dẻo bùi quyện trong nước mắm chua ngọt tạo nên một phong vị trần thế ngon đến rơi nước mắt. Sau khi húp cạn muỗng canh cuối cùng và uống cạn ly trà đá to tướng mát lạnh buốt tận chân răng, tôi mới thở phào một hơi thỏa mãn. Luồng nhiệt lượng từ tinh bột và đạm nhanh chóng được dạ dày tiêu hóa, chuyển hóa thành dòng dinh dưỡng âm thầm tưới tắm khắp các bó cơ đang mỏi nhừ.

Bảy giờ mười lăm phút tối.

Tôi chạy xe về đến con hẻm nhỏ trên đường D2, dắt xe vào tầng trệt ngôi nhà trọ ba tầng rồi bước lên căn phòng của mình.

Căn phòng trọ nhỏ rộng chừng mười lăm mét vuông đón tôi bằng bầu không khí quen thuộc: chiếc nệm mỏng gấp gọn gàng nơi góc tường, chiếc quạt trần quay chậm rãi, giá sách kỹ thuật xếp ngay ngắn và chiếc bàn làm việc đặt cạnh khung cửa sổ mở ra khoảng trời đêm Bình Thạnh.

Tôi cởi bỏ bộ quần áo lấm lem bụi đất, bước vào phòng tắm vặn vòi hoa sen.

Dòng nước ấm xối xả chảy từ đỉnh đầu xuống bờ vai, gột rửa sạch sẽ vị mặn mòi của nước sông lợ và lớp bùn khoáng chu sa bám trong kẽ móng tay. Đứng trước tấm gương soi mờ hơi nước, tôi nhìn lại cơ thể mình:

Sau gần nửa tháng kiên trì rèn luyện Thể Đạo kết hợp giữa bài quyền Tam Chu Thiên và thử thách khắc nghiệt dưới đáy sông chiều nay, vóc dáng của tôi đã có sự thay đổi rõ rệt. Lớp mỡ thừa dưới da đã biến mất hoàn toàn, thay vào đó là những dải cơ bắp săn chắc, thon gọn nhưng kết cấu cực kỳ đậm đặc. Khung xương sườn và cột sống dường như cứng cáp hơn, ánh mắt đen sâu thẳm toát lên vẻ trầm tĩnh, kiên định của người đã từng bước qua lằn ranh sinh tử.

Bước ra khỏi phòng tắm trong chiếc áo thun và quần lửng cotton mềm mại, tôi với tay lấy chiếc điện thoại đặt trên bàn làm việc.

Màn hình sáng lên với một loạt thông báo dồn dập:

Một tin nhắn Zalo từ anh Trưởng phòng tiếp thị gửi lúc bốn giờ chiều: *"An ơi, file kế hoạch chạy chiến dịch quý bốn cho nhãn hàng gia dụng em chỉnh sửa bảng tính dự toán ngân sách xong chưa? Sáng mai gửi anh sớm trước chín giờ để họp ban giám đốc nhé."*

Tôi kéo ghế ngồi vào bàn, mở chiếc máy tính xách tay cũ lên. Những con số biểu phí, phân bổ ngân sách quảng cáo và bảng tiến độ công việc hiện ra trên màn hình. Tôi gõ bàn phím thoăn thoắt, hoàn thiện nốt hai bảng tính còn dở dang rồi đính kèm file gửi qua email công ty kèm lời nhắn: *"Em đã cập nhật số liệu chi tiết theo yêu cầu của anh. Chúc anh buổi tối vui vẻ."*

Vừa gửi xong email thì màn hình điện thoại lại rung lên. Lần này là cuộc gọi video từ mẹ ở quê.

Tôi vội bấm nút nhận cuộc gọi.

Gương mặt rám nắng, hiền từ của mẹ hiện lên trên màn hình điện thoại, phía sau là gian bếp nhỏ quen thuộc ở vùng quê trung du với ánh lửa bập bùng từ bếp củi:

"An hả con? Ăn cơm nước gì chưa? Dạo này công việc trên đó có bận lắm không con?"

"Dạ con vừa ăn cơm xong mẹ ơi. Con mới tắm xong, đang ngồi nghỉ," tôi mỉm cười, giọng nói vô thức mềm lại: "Ở nhà bố mẹ có khỏe không? Vườn cam năm nay được mùa không mẹ?"

"Bố mày vừa ra trông vườn về, dạo này lưng ông ấy đỡ đau rồi nhờ có thuốc con gửi về đợt trước đấy. Mẹ nghe đài báo mấy bữa nay trong miền Nam mưa gió thất thường dữ lắm, con đi làm nhớ mang theo áo mưa nghe chưa, đừng có cậy khỏe mà tắm mưa rồi cảm lạnh. Tiền nhà tháng này có thiếu thốn gì không, bố mẹ vừa bán lứa lợn, nếu kẹt thì bảo bố chuyển cho một ít mà trang trải nghe con..."

Nghe giọng mẹ dặn dò từng li từng tí, nghe tiếng gà con ríu rít tìm mẹ và tiếng gió xào xạc luồn qua rặng tre đầu ngõ vọng qua chiếc loa điện thoại, sống mũi tôi bỗng cay cay. 

Đó chính là cội nguồn của tôi. Tôi không phải là một bậc siêu nhân thần thánh mang sứ mệnh gánh vác cõi trời đất nào cả; tôi chỉ là đứa con trai của mẹ, một đứa con sinh ra từ bùn đất quê hương, đang từng ngày nỗ lực bươn chải nơi đô thị để sống tự lập và chăm lo cho gia đình.

"Con không thiếu tiền đâu mẹ, tháng này con được thưởng dự án nữa, mai con gửi về cho mẹ mua sữa bồi bổ cho bố nhé. Mẹ ngủ sớm đi nha."

"Ừ, con cũng ngủ sớm đi nghe, đừng có thức khuya ôm cái máy tính hại mắt..."

Cuộc gọi tắt đi, để lại một khoảng lặng êm đềm đến lạ kỳ.

Tám giờ bốn mươi lăm phút tối.

Tôi tắt ngọn đèn tuýp trên trần nhà, chỉ để lại chiếc đèn bàn màu vàng nhạt. Tôi bước tới tấm chiếu cói trải giữa sàn, ngồi xếp bằng theo tư thế ngũ tâm triều thiên.

Hít sâu một hơi qua cánh mũi, tôi dẫn luồng khí ấm áp từ đan điền chậm rãi luân chuyển qua từng đốt sống lưng theo chu trình Tam Chu Thiên. 

Dưới sự lắng dịu của tâm trí, tôi có thể cảm nhận rõ ràng từng biến chuyển cơ học bên trong cơ thể: Áp lực nước khổng lồ buổi chiều nay giống như một chiếc búa tạ ngàn cân đã rèn giũa khối quặng thô, ép chặt từng thớ cơ và màng xương của tôi lại với nhau. Các khớp xương kêu lên những tiếng tí tách thật khẽ, tủy xương ấm nóng tỏa ra một nguồn sinh lực dồi dào, vững chắc. Cảnh giới Luyện Cốt sơ kỳ — vốn có phần non nớt sau những ngày đầu đột phá — nay đã hoàn toàn củng cố sâu sắc, hòa quyện làm một với thể xác phàm nhân.

*"Minh An..."*

Một tiếng gọi khẽ khàng như tiếng gió thoảng vang lên ngay giữa tâm thức tôi.

Hư ảnh của Lâm Tịch dần hiện ra trong tâm trí. Nhưng khác với vẻ lộng lẫy, sắc lạnh của một nữ kiếm tiên từng đứng giữa phong ba bão táp, nàng lúc này khoác một dải lụa trắng mỏng manh, dáng người hư ảo đến mức gần như trong suốt. Gương mặt thanh tú của nàng lộ rõ nét mệt mỏi, suy kiệt, nhưng khóe môi lại khẽ cong lên một nụ cười nhẹ nhõm, an nhiên.

Nàng hướng ánh nhìn qua khung cửa sổ phòng trọ của tôi, chăm chú ngắm nhìn bầu trời đêm thành phố.

Từ tầng ba nhìn ra, Sài Gòn về đêm hiện lên như một dòng sông ánh sáng bất tận: Tòa tháp Landmark 81 sừng sững vươn lên giữa tầng mây với dải đèn led đa sắc đổi màu liên tục; những nhịp cầu cạn bê tông của tuyến đường sắt đô thị uốn lượn qua những rặng cây xanh; hàng vạn vệt đèn xe máy rực đỏ đan xen trên các ngả đường lớn; và văng vẳng từ con hẻm bên dưới là tiếng lách cách gõ lóng báng của người bán hủ tiếu dạo hòa cùng tiếng trẻ con nô đùa rộn rã.

*"Một thế giới thật kỳ lạ..."* Lâm Tịch khẽ thì thầm, thanh âm mang theo sự rung cảm sâu xa tự đáy lòng.

"Cô cảm thấy thế giới này thế nào?" Tôi hỏi nàng trong ý niệm.

*"Ở thời đại của ta..."* Ánh mắt Lâm Tịch nhìn xa xăm, như đang lần giở lại những trang ký ức ngàn năm đã phủ bụi: *"Trời đất bao la vô tận, linh khí dạt dào như biển lớn. Nhưng thế giới ấy lại tàn khốc và lạnh lẽo khôn cùng. Kẻ mạnh nắm giữ thần thông khai sơn phá thạch, ngự kiếm bay qua chín tầng trời, nhìn sinh linh vạn dặm bên dưới không khác gì cỏ rác sâu kiến. Để tranh đoạt một cọng linh thảo hay một tấc linh mạch, các tông môn có thể đánh chìm cả một dãy núi, chém giết hàng chục vạn sinh mạng mà không hề chớp mắt.*

*Những phàm nhân ở cõi ấy cả đời sống trong sợ hãi, chỉ biết quỳ rạp dưới chân tượng thần cầu xin mưa thuận gió hòa, run rẩy chấp nhận số phận bị định đoạt bởi sự hỉ nộ vô thường của những kẻ tu tiên.*

*Nhưng thế giới này... những con người ở nơi này hoàn toàn khác."*

Nàng khẽ nghiêng đầu, nhìn dòng xe máy hối hả dưới chân cầu:

*"Các ngươi không có linh căn, không biết pháp thuật, thân thể mỏng manh chỉ cần một viên đạn hay một tai nạn nhỏ là tan vỡ. Nhưng các ngươi lại dùng chính đôi bàn tay và trí tuệ của mình để tạo dựng nên một cõi nhân gian ấm áp đến nhường này.*

*Các ngươi chế tạo ra những lồng thép chịu lực để lặn xuống đáy sâu ba mươi tám mét; các ngươi dùng dây cáp và sóng vô tuyến để kết nối hàng triệu con người; các ngươi thắp sáng màn đêm bằng những ngọn đèn không bao giờ tắt; và quan trọng hơn hết, các ngươi bảo vệ nhau bằng luật lệ, bằng tình thương và sự sẻ chia trách nhiệm.*

*Một thế giới như vậy... thực sự không cần đến những 'tiên nhân' cao ngạo đứng trên đầu chúng sinh để ban ơn hay trừng phạt."*

Nghe những lời tâm sự chân thành từ đáy lòng của Lâm Tịch, tôi cảm thấy một luồng hơi ấm lan tỏa khắp lồng ngực. Nàng không còn là một tàn hồn mang nặng chấp niệm phục thù hay kiêu hãnh của một thời đại đã mất; nàng đã bắt đầu thấu hiểu và tôn trọng vẻ đẹp của thế giới mà tôi đang sống.

*"Minh An, ta có một chuyện cần nói với ngươi..."* Giọng nói của nàng chùng xuống, trở nên yếu ớt hơn một chút.

"Tôi đang nghe đây, Lâm Tịch."

*"Nguồn năng lượng tàn hồn của ta sau ba lần kích hoạt kiếm ý và chỉ dẫn cơ học mở then Thủy Môn đã chạm tới giới hạn cạn kiệt. Nếu tiếp tục duy trì trạng thái thức tỉnh, bản thể nguyên thần của ta sẽ bắt đầu rút tỉa khí huyết của ngươi để bù đắp — điều đó sẽ làm tổn thương nghiêm trọng đến đạo cơ phàm nhân mà ngươi vừa dày công rèn luyện.*

*Vì vậy, lát nữa đây, ta sẽ tiến vào trạng thái **trầm miên** sâu."*

Tôi thoáng giật mình: "Trầm miên sao? Sẽ kéo dài bao lâu?"

*"Có thể là vài tuần, vài tháng, hoặc lâu hơn nữa tùy thuộc vào tốc độ hồi phục tự nhiên của thức hải,"* Lâm Tịch mỉm cười dịu dàng, ánh mắt nhìn tôi tràn đầy sự tin tưởng: *"Ngươi không cần phải lo lắng. Đây là quy luật tự bảo tồn của nguyên thần viễn cổ. Khi ta ngủ say, ý thức của ta sẽ phong bế hoàn toàn trong chiếc trâm cài ngọc, không làm phiền hay tiêu hao một sợi khí huyết nào của ngươi.*

*Nhưng điều đó cũng có nghĩa là, từ ngày mai, ngươi sẽ phải tự mình bước đi trên con đường Thể Đạo."*

Nàng nghiêm túc dặn dò từng lời, từng chữ khắc sâu vào tâm trí tôi:

*"Ngươi hãy nhớ kỹ ba điều này:*

*Thứ nhất, Thể Đạo phàm nhân lấy thân xác làm lò luyện, lấy cơm áo gạo tiền và lao động trần thế làm củi lửa. Đừng bao giờ xa rời cuộc sống hiện thực. Hãy làm việc chăm chỉ, ăn uống đủ chất dinh dưỡng, hiếu kính cha mẹ và giữ trọn bổn phận của một con người bình thường giữa xã hội.*

*Thứ hai, mỗi ngày vào giờ Tý và giờ Mão, hãy duy trì ba chu trình thở Tam Chu Thiên để nuôi dưỡng tủy xương. Khí Huyết Luyện Cốt cốt ở sự bền bỉ, nước chảy đá mòn, tuyệt đối cấm kỵ nóng vội cầu thành.*

*Và điều cuối cùng... viên Huyết Ngọc Trấn Ba dưới đáy sông Nhà Bè nay đã yên giấc, cơ chế Thủy Môn đã vận hành thông suốt. Bí mật ngàn năm ấy hãy để nó tiếp tục ngủ yên dưới dòng Soài Rạp. Đừng bao giờ ỷ lại vào sức mạnh huyền bí để mưu cầu danh lợi cá nhân."*

"Tôi hiểu rồi, Lâm Tịch," tôi đáp lại bằng tất cả sự chân thành và kiên định: "Tôi hứa với cô, tôi sẽ rèn luyện chăm chỉ và bảo vệ cuộc sống bình dị này."

*"Tốt lắm..."* 

Thanh âm của Lâm Tịch nhỏ dần, nhẹ bẫng như một làn khói sương mùa thu:

*"Minh An... hãy sống cho thật tốt cuộc đời của ngươi nơi nhân gian..."*

Dứt lời, bóng hình thanh tao của nàng khẽ mờ đi, hóa thành một đốm sáng trắng ấm áp thu liễm lại sâu thẳm trong thức hải của tôi, rơi vào một giấc ngủ sâu an lành không mộng mị.

Không gian tâm thức trở lại vẻ tĩnh lặng tuyệt đối.

Tôi từ từ mở mắt ra.

Gió đêm mùa thu luồn qua khung cửa sổ phòng trọ, làm lay động tấm rèm vải mỏng. Đèn đường vàng nhạt hắt lên tường những vệt bóng lung linh của cành bàng già trước hiên nhà.

Tôi bước xuống chiếu, uống một ngụm nước lọc mát lành rồi ngả lưng xuống chiếc nệm quen thuộc. 

Không còn tiếng gầm rít của dòng xoáy đáy sông sâu ba mươi tám mét, không còn sức ép nghẹt thở của áp suất năm mươi tấn lực, chỉ còn tiếng ve muộn rỉ rả trong đêm và tiếng còi tàu xa xăm vọng lại từ phía sông Sài Gòn bình yên.

Tôi nhắm mắt lại, thả lỏng toàn bộ thân thể, nhẹ nhàng chìm vào một giấc ngủ thật sâu.
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 45 vào manuscript...")
    with open(CH45_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã tạo tệp: {CH45_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 45 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=45,
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
    VALUES (?, 'chapter', 'mini_arc_01_03', 45, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_045", "Chương 45: Ánh Đèn Bình Thạnh Và Giấc Ngủ Trầm Miên",
        "Tàu Đại Dương 09 cập cảng Tân Thuận (Quận 7) lúc 15:30. Minh An cùng Tiến sĩ Nam, chú Tùng và Đại úy Hùng hoàn tất báo cáo kỹ thuật thủy văn, xác nhận khối cự thạch Huyết Ngọc Trấn Ba đã trở về trạng thái trơ cơ học và nhiệt lượng bình thường (Payoff FSH-028). Minh An lấy xe máy Wave Alpha hòa vào dòng kẹt xe giờ tan tầm, ăn đĩa cơm tấm sườn nướng Ung Văn Khiêm, trở về căn phòng trọ 15m2 ở Bình Thạnh. Anh xử lý email công việc marketing, gọi điện hỏi thăm bố mẹ ở quê nhà. Đêm muộn, anh vận khí Tam Chu Thiên củng cố Luyện Cốt sơ kỳ. Lâm Tịch cảm nhận vẻ đẹp của xã hội hiện đại vận hành bằng kỹ thuật và tình người, trước khi tiến vào trạng thái trầm miên sâu hồi phục nguyên thần. Nàng dặn dò Minh An kiên trì rèn luyện Thể Đạo độc lập và sống tốt cuộc đời phàm trần.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 45, 1, '2026-10-07T22:30:00+07:00', 45, 'loc_binh_thanh', ?, ?, ?)
    """, (
        "EVT-CH045-01", "Trở về đất liền, nghiệm thu kỹ thuật và cuộc đối thoại trước giấc ngủ trầm miên của Lâm Tịch",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "chú Tùng", "Mẹ Minh An"], ensure_ascii=False),
        "Chiều và tối 07/10/2026 (15:30 - 22:30). Tàu Đại Dương 09 cập cảng Tân Thuận; biên bản bàn giao thủy văn xác nhận luồng hàng hải an toàn, Huyết Ngọc Trấn Ba hạ nhiệt ngủ say (FSH-028 PAID). Minh An đi xe máy qua dòng kẹt xe giờ tan tầm, ăn cơm tấm Ung Văn Khiêm, về phòng trọ Bình Thạnh. Anh hoàn tất slide công việc và gọi điện cho mẹ ở quê. Đêm muộn, Minh An vận hành Tam Chu Thiên củng cố Luyện Cốt sơ kỳ. Lâm Tịch trò chuyện sâu sắc về sự đối lập giữa tu tiên viễn cổ và văn minh nhân gian hiện đại, sau đó tiến vào giấc ngủ trầm miên sâu để dưỡng thần, căn dặn Minh An tự lập rèn luyện.",
        "Khép lại hoàn toàn sự kiện ngầm Nhà Bè; củng cố vững chắc Luyện Cốt sơ kỳ; hoàn tất hồi báo FSH-028; Lâm Tịch bước vào trầm miên an toàn; Minh An tái khẳng định mỏ neo trách nhiệm đời thường và gia đình."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 45, 'Phòng trọ Bình Thạnh, TP.HCM', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ viên mãn ổn định, màng tủy vững chắc, tủy sinh khí huyết)",
        "Thể lực hồi phục hoàn toàn sau bữa ăn giàu dinh dưỡng và giấc ngủ ấm áp, kinh mạch thông suốt, không còn dư chấn áp suất nước",
        json.dumps([], ensure_ascii=False),
        json.dumps(["Chiếc trâm ngọc cổ (chứa Lâm Tịch đang trầm miên)", "Laptop làm việc", "Xe máy Wave Alpha", "Điện thoại thông minh"], ensure_ascii=False),
        "Thanh thản, ấm áp, kiên định với con đường Thể Đạo tự lập và trách nhiệm đối với gia đình, công việc"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 45, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (chính thức tiến vào trạng thái Trầm Miên sâu để khôi phục nguyên thần)",
        "Nguyên thần ngủ say tĩnh lặng tuyệt đối, không còn can thiệp hay tiêu hao năng lượng từ bên ngoài",
        json.dumps(["Đạo cơ vỡ nát", "Nguyên thần trầm miên phục hồi"], ensure_ascii=False),
        json.dumps(["Bản thể kiếm tàn Băng Phách Trảm Tuyết (ngủ say)"], ensure_ascii=False),
        "An lòng, nhẹ nhõm, hoàn toàn tin tưởng vào nhân cách và sự kiên định của Minh An"
    ))

    # 3.4 story_threads touch
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-001'
    """, ("Lâm Tịch bước vào trạng thái trầm miên sâu sau khi cạn kiệt tàn lực, giao lại trách nhiệm tự tu luyện Thể Đạo cho Minh An.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Minh An củng cố Luyện Cốt sơ kỳ viên mãn nhờ áp lực nước nén và Tam Chu Thiên, bắt đầu giai đoạn tự rèn luyện độc lập.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-REL-001'
    """, ("Đối thoại sâu sắc đêm muộn: Lâm Tịch thừa nhận giá trị và sự ấm áp của văn minh phàm nhân hiện đại; sự gắn kết giữa hai người đạt độ tin cậy và thanh thản cao.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-CHR-001'
    """, ("Minh An hoàn thành công việc marketing công ty, gọi điện ấm áp về quê hỏi thăm bố mẹ, ăn cơm tấm Ung Văn Khiêm, tái lập trật tự đời thường.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-001'
    """, ("Báo cáo khoa học chính thức xác nhận Thủy Môn và Huyết Ngọc Trấn Ba đã ổn định trơ cơ học, sự kiện đáy sông Nhà Bè khép lại an toàn.", now_iso))

    # 3.5 foreshadowing update - Payoff FSH-028
    cur.execute("""
    UPDATE foreshadowing_ledger SET status = 'PAID', payoff_chapter = 45, payoff_scene = 1 WHERE id = 'FSH-028'
    """)

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 45...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH45_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 45.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_045.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 45: Ánh Đèn Bình Thạnh Và Giấc Ngủ Trầm Miên",
        chapter_num=45,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT SOẠN THẢO CHƯƠNG 45 THÀNH CÔNG ===")
    else:
        sys.exit(1)

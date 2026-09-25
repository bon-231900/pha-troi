# -*- coding: utf-8 -*-
"""Draft Chapter 90 for Phá Trời Novel OS: Tiếng Sấm Đại Ngàn.
Prose length: ~3,750 words (standard: 3,200 - 4,500 words), zero meta-words, zero 'huyết mạch', severe grounding, deep pathos, geological realism, and preparation for Tây Nguyên expedition.
"""

import os
import sys
import json
import sqlite3
import re

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.emotion_dopamine_engine import EmotionDopamineEngine

CHAPTER_NUM = 90
CHAPTER_TITLE = "Tiếng Sấm Đại Ngàn"
DATE = "2026-11-01"
LOCATION = "Cù Lao Chợ Gạo, Tiền Giang & Viện Nghiên Cứu Địa Tầng, TP. Hồ Chí Minh"

ACT1 = '''Bốn giờ ba mươi phút sáng ngày mùng một tháng mười một.

Tiếng gà gáy le te từ các xóm ấp bên kia rạch dừa xé toạc màn sương sớm bảng lảng đang phủ trùm lên cù lao Chợ Gạo. Gió sông Tiền thổi qua rặng dừa xiêm mát rượi, mang theo hương thơm ngai ngái nồng nàn của đất bãi bồi sau con nước lớn ban đêm. Trên những tàu lá dừa nước chìa ra mép mương, từng giọt sương đọng long lanh tựa hạt ngọc, khẽ rơi tí tách xuống mặt nước phù sa phẳng lặng như gương.

Tôi thức dậy khi trời còn chưa rạng tỏ. Dưới ánh sáng le lói của ngọn đèn dầu hỏa đặt trên chiếc bàn gỗ tràm ngoài hiên, tôi xắn ống quần kaki lên quá đầu gối, xách đôi thùng thiếc đi ra mé rạch dừa sau nhà. 

Nước sông đang độ ròng sát đáy, phù sa lắng xuống để lộ làn nước trong vắt và mát lạnh đến tê buốt đầu ngón chân. Tôi bước xuống từng bậc đất nện trơn trượt, múc từng đôi nước gánh ngược lên bờ, đổ đầy vào ba chiếc lu da lươn lớn xếp sau chái bếp. Ba lu nước này mẹ có thể dùng để lắng phèn, có đủ nước ngọt sinh hoạt trong cả tuần tới mà không cần phải lom khom xách nặng. Sau đó, tôi cầm cây rựa bén đi một vòng quanh bờ rào dâm bụt, phạt sạch những nhánh gai dại cản lối đi, chặt bỏ những cành dừa khô rũ xuống mương nước. Tôi còn lấy dây kẽm và đinh mười chằng néo lại mấy tấm vách lá dừa trước hiên nhà cho thật chắc chắn, đề phòng những cơn gió lốc trái mùa thường thổi thốc vào bờ mỗi cữ triều rằm tháng mười.

Khi ánh bình minh vàng cam bắt đầu nhuộm đỏ mặt nước sông Tiền, mẹ tôi thức dậy.

Bước ra chái bếp, nhìn thấy ba lu nước đã đầy ắp tràn trề, khoảnh sân đất nện phong quang sạch bóng lá rụng và đống củi tràm khô được xếp ngay ngắn thành từng hàng cao ngang đầu người, đôi mắt đục mờ của mẹ rưng rưng niềm xúc động. Mẹ không nói nhiều, chỉ lẳng lặng đi nhóm bếp củi bằng những cọng lá dừa khô còn thơm mùi nắng trưa qua. 

Mẹ nấu cho tôi một nồi khoai mì luộc vừa mới đào ngoài góc liếp. Những củ khoai mì ruột trắng ngần, nứt vỏ bở tơi, được mẹ rưới lên một muỗng nước cốt dừa béo ngậy thắng với chút hành hoa, rắc thêm một nhúm muối mè giã nhuyễn thơm lừng.

Hai mẹ con ngồi bên chiếc bàn tre con ngoài hiên ăn bữa sáng đạm bạc. Hương vị ngọt bùi của khoai mì quê hòa cùng vị béo ngậy của nước cốt dừa và vị mặn mà của muối mè khiến từng miếng ăn trở nên ấm áp lạ kỳ.

"An này, công việc trên thành phố bận bịu, con cứ lo việc của con, đừng có bận tâm quá tới mẹ ở dưới này nghen," mẹ gắp củ khoai mì dẻo nhất bỏ vào chén tôi, giọng nói run run chan chứa tình thương: "Ở xóm cù lao này có thím Bảy với bà con chòm xóm tối lửa tắt đèn có nhau. Con đi làm ăn xa ngoài đường sá, đi công trình trèo đèo lội suối phải cẩn thận từng bước chân. Đừng có ham công tiếc việc quá mà bỏ bữa, nghe con."

"Dạ, con biết rồi mẹ. Cuối tháng này xong đợt khảo sát mới của Viện, con lại tranh thủ đón xe đò về thăm mẹ nữa."

Trước khi tôi bước chân ra ngõ, mẹ cẩn thận nhét vào ngăn đáy chiếc ba-lô của tôi một đòn bánh tét đậu xanh thịt mỡ mẹ tự tay gói từ hôm qua và một hũ mắm cá sặc thơm phức được bọc kỹ trong năm lớp bọc ni-lông buộc dây thun cẩn mật. Bàn tay gầy gò đầy những vết chai sạn và đường gân xanh của mẹ nắm chặt lấy bàn tay tôi, đưa chân tôi ra tận đầu cầu khỉ rồi đứng lặng nhìn theo.

Tôi khoác chiếc ba-lô vải dù lên vai, bước đi trên con đường đan rợp bóng dừa xiêm mát rượi. Khối Mộc Hoàng Lôi Tâm Thạch bọc kín trong lớp da nai rừng sấy khô được tôi cẩn thận giấu sâu dưới đáy ba-lô. Mỗi bước chân tôi bước đi trên con đường làng quê mẹ, khối đá bazan đen nhánh ấy dường như lại khẽ phát ra một nhịp rung chuyển ấm áp, tựa như một mạch đập ngầm của lòng đất đang giao hòa cùng dòng máu đang cuộn chảy trong cơ thể tôi.

Bảy giờ sáng, tôi đón chuyến xe đò tuyến Gò Công - Sài Gòn tại ngã ba huyện để quay trở lại thành phố.'''

ACT2 = '''Mười một giờ trưa cùng ngày.

Chiếc xe đò đưa tôi về tới bến xe Miền Tây sau gần bốn tiếng đồng hồ chạy giữa dòng xe cộ hối hả của quốc lộ. Sau khi ghé căn phòng trọ nhỏ trên đường Nơ Trang Long để cất đòn bánh tét của mẹ và lấy lại hai thanh Hắc Thiết Đoản Côn cùng Trấn Thủy Đoản Đao bọc kỹ trong bao bạt dứa, tôi bắt xe ôm chạy thẳng đến trụ sở Viện Nghiên cứu Địa tầng và Năng lượng Nội sinh Đô thị trên đường Mạc Đĩnh Chi, quận Nhất.

Vừa bước qua cánh cửa kính cách âm của tầng ba khu trung tâm dữ liệu, một bầu không khí khẩn trương, căng thẳng tột độ lập tức ập vào mắt tôi.

Trên dãy màn hình LED siêu rộng gắn dọc bức tường trung tâm, các đồ thị sóng địa chấn ba chiều đang liên tục nhấp nháy những dải màu đỏ rực báo động. Tiếng còi tín hiệu cảnh báo vang lên từng hồi ngắt quãng, hòa lẫn với tiếng gõ bàn phím lách cách của hàng chục chuyên viên kỹ thuật đang phân tích dữ liệu vi địa chấn truyền về từ mạng lưới trắc địa quốc gia.

Kỹ sư Tuấn — Tech Lead của đội kỹ thuật — đang cởi trần chiếc áo khoác đồng phục, hai mắt thâm quầng nhưng gương mặt lại hừng hực vẻ phấn khích tột cùng. Vừa thấy bóng tôi bước vào cửa, anh buông vội chiếc bút cảm ứng, lao tới túm lấy bả vai tôi lắc mạnh:

"Chú An! Trời đất ơi, chú mày về đúng lúc như một vị cứu tinh vậy! Anh gọi cho chú mày suốt từ chín giờ sáng mà máy toàn báo ngoài vùng phủ sóng!"

"Em ngồi xe đò qua mấy đoạn kênh rạch sóng yếu anh Tuấn," tôi kéo chiếc ghế ngồi xuống bên cạnh anh, đưa mắt nhìn lên biểu đồ sóng địa chấn đang giật cục dữ dội trên màn hình: "Có chuyện gì mà phòng dữ liệu báo động cấp độ hai vậy anh?"

Tuấn ghé sát lại gần tôi, hạ thấp giọng chỉ vào dải phổ tần số đang hiển thị:

"Từ bốn giờ ba mươi phút sáng nay, toàn bộ mười tám trạm quan trắc địa chấn ngầm sâu của chúng ta đặt dọc theo sườn nam Trường Sơn, đặc biệt là cụm trạm số 7 đặt quanh chân núi Chư Yang Sin thuộc địa phận tỉnh Đắk Lắk, liên tục thu được một chuỗi xung chấn cực kỳ dị thường!"

Nghe đến cái tên **Chư Yang Sin**, lồng ngực tôi bỗng khẽ thắt lại. Ba mươi ba đốt sống tủy ngọc sau lưng tôi hơi ấm lên một cách tự nhiên.

Tôi tập trung tinh thần nhìn vào các dải thông số kỹ thuật hiển thị trên màn hình.

"Tần số dao động cực thấp, chỉ dao động trong khoảng 0.08 Hertz đến 0.12 Hertz," Tuấn vừa chỉ ngón tay vào màn hình vừa phân tích: "Cứ đều đặn mười tám phút một lần, một đợt sóng xung chấn lại bùng phát từ độ sâu âm một ngàn hai trăm mét dưới lòng các vỉa đá bazan cổ. Đáng sợ nhất là luồng sóng này không phải là sóng nứt gãy kiến tạo thông thường. Nó mang theo một trường điện từ cực lớn, làm tê liệt toàn bộ la bàn từ tính và làm gián đoạn đường truyền vô tuyến của các trạm viễn thám trong bán kính hơn bốn mươi cây số! Toàn bộ các cảm biến địa từ tại trạm Lạc Dương và Krông Bông đều bị nhiễu loạn trắng xóa."

Đúng lúc đó, cánh cửa phòng họp chuyên gia mở toang.

Viện trưởng Trịnh Hoài Nam bước ra. Vị tiến sĩ địa chất kỳ cựu với mái tóc hoa râm và cặp kính lão dày cộp trông có vẻ tiều tụy vì đã thức trắng đêm qua. Trên tay ông đang ôm một tập hồ sơ tài liệu lưu trữ có dán nhãn niêm phong màu vàng ố đã ngả màu theo thời gian.

Nhìn thấy tôi, đôi mắt mệt mỏi của Viện trưởng Nam bỗng sáng bừng lên:

"Minh An! Cậu đã về rồi! Mau, vào phòng họp kín với tôi ngay, có tài liệu tối mật này tôi cần cậu thẩm định trực tiếp!"'''

ACT3 = '''Cánh cửa phòng họp chuyên gia dày dặn bằng hợp kim cách âm khép lại. Trên chiếc bàn hội nghị bằng kính cường lực, Viện trưởng Nam cẩn thận mở tập hồ sơ giấy ố vàng ra.

Đó là bản báo cáo trắc địa địa chất mang mã hiệu KH-96 do chính Viện trưởng Nam và một đoàn chuyên gia địa chất hàng đầu thực hiện vào mùa khô năm 1996 tại vùng rừng già Buôn Đôn và chân dãy Chư Yang Sin — đúng vào năm mà cha tôi đã đào được khối Mộc Hoàng Lôi Tâm Thạch!

Viện trưởng Nam đẩy cặp kính lão lên sống mũi, giọng nói trầm ấm nhưng đanh thép:

"Minh An, ba mươi năm trước, khi tôi còn là một nghiên cứu sinh trẻ theo chân các nhà khoa học Liên Xô khảo sát cấu trúc địa tầng Tây Nguyên, chúng tôi từng khoan thăm dò một lỗ khoan sâu tám trăm mét dưới thềm bazan Buôn Đôn. Khi mũi khoan chạm tới tầng đá biến chất cổ, thiết bị đo sóng siêu âm đã phát hiện một cấu trúc vòm rỗng hình bát giác khổng lồ ẩn sâu dưới lòng núi. Nhưng hồi đó kỹ thuật còn thô sơ, chúng tôi chỉ ghi nhận được hiện tượng từ trường dị thường phát ra âm thanh tựa như tiếng sấm rền rồi phải niêm phong dự án lại."

Ông chỉ tay vào màn hình phụ đang đồng bộ dữ liệu thời gian thực từ cao nguyên:

"Sáng nay, các phân tích vi chấn mới nhất của vệ tinh viễn thám cho thấy, cấu trúc vòm bát giác cổ dưới chân núi Chư Yang Sin đang bước vào chu kỳ kích hoạt năng lượng sau ba mươi năm ngủ say. Trường điện từ ngầm tăng vọt gấp năm mươi lần mức bình thường. Địa hình rừng núi nơi đó vô cùng hiểm trở, vách đá dựng đứng, vực sâu thăm thẳm và nhiều thung lũng sương mù dày đặc. Nếu hiện tượng này tiếp tục bộc phát mà không được đo đạc, kiểm soát và xác định nguyên nhân, nó có thể kích hoạt các đứt gãy bazan ngầm, đe dọa trực tiếp đến an toàn của các công trình thủy điện lớn trên dòng sông Sêrêpôk và cuộc sống của hàng vạn đồng bào các buôn làng quanh vùng đệm Vườn quốc gia!"

Viện trưởng Nam dừng lại, nhìn thẳng vào mắt tôi với tất cả sự kỳ vọng sâu sắc:

"Ban Chỉ đạo Khảo sát Địa chất Quốc gia và Bộ Khoa học Công nghệ đã ký quyết định hỏa tốc thành lập một Đoàn Khảo sát Trắc địa Đặc nhiệm. Nhiệm vụ của đoàn là lập tức lên đường đến Buôn Đôn và tiến sâu vào vùng lõi rừng già Chư Yang Sin, mang theo cụm thiết bị cảm biến quang học ma trận mới nhất để cắm ba mươi trạm quan trắc sâu, giải mã nguồn gốc của luồng xung lực địa chấn này."

Ông đặt bàn tay già nua nhưng ấm áp lên vai tôi:

"Kỹ thuật lọc nhiễu dữ liệu ma trận của cậu là số một của Viện ta. Chỉ có cậu mới đủ nhạy bén và thể lực để vận hành dàn thiết bị cảm biến sâu trong điều kiện rừng rậm hiểm trở của đại ngàn. Tôi muốn cậu trực tiếp đảm nhiệm vị trí Đội trưởng Đội Kỹ thuật Cảm biến và Dữ liệu Hiện trường của đoàn khảo sát này. Kỹ sư Tuấn sẽ đi cùng cậu để phụ trách hạ tầng trạm thu phát. Cậu nghĩ sao, Minh An?"

Lồng ngực tôi bừng lên một ngọn lửa nhiệt huyết mãnh liệt.

Mọi mắt xích của số phận như đang gắn kết lại thành một vòng tròn hoàn mỹ: từ khối Mộc Hoàng Lôi Tâm Thạch mà cha tôi cất giữ ba mươi năm trước, đến bí mật phong ấn lôi đình ngàn năm của đại ngàn Trường Sơn mà Lâm Tịch vừa hé lộ đêm qua, và giờ là nhiệm vụ khoa học chính thức của Viện Địa chất!

Tôi đứng nghiêm trang, ánh mắt kiên định tựa như bàn thạch:

"Báo cáo Viện trưởng, tôi nhận nhiệm vụ! Tôi và anh Tuấn sẽ chuẩn bị đầy đủ thiết bị và phương án kỹ thuật, sẵn sàng lên đường bất cứ lúc nào!"

"Tốt lắm!" Viện trưởng Nam mỉm cười hài lòng: "Bảy giờ sáng mai, đoàn xe dã chiến chuyên dụng của Viện sẽ xuất phát từ Sài Gòn, hành quân theo quốc lộ 14 hướng thẳng về cao nguyên Đắk Lắk. Hãy về chuẩn bị tư trang thật kỹ lưỡng!"'''

ACT4 = '''Tám giờ ba mươi phút tối.

Căn phòng trọ nhỏ trên đường Nơ Trang Long chìm trong sự tĩnh lặng quen thuộc. Tiếng còi xe từ phía đường lớn vọng lại ngắt quãng, hòa vào tiếng lá bàng rơi xào xạc ngoài khung cửa sổ mở hé.

Trên chiếc chiếu cói trải giữa sàn nhà, tôi cẩn thận bày ra ba món đồ vật: thanh Hắc Thiết Đoản Côn bằng thép nhíp Zil bát giác, thanh Trấn Thủy Đoản Đao bằng đồng nứt rạn chỉ vàng, và khối **Mộc Hoàng Lôi Tâm Thạch** màu đen nhánh vừa mang từ cù lao Chợ Gạo lên.

Khối đá bazan cổ sau khi được đưa về thành phố dường như càng trở nên linh động hơn. Dưới ánh sáng của bóng đèn huỳnh quang, những đường vân thớ gỗ ngàn năm ẩn sâu bên trong khối huyền thạch khẽ phát ra một làn lôi quang màu tím nhạt mờ ảo, mắt thường khó lòng nhận biết.

Tôi ngồi xếp bằng theo tư thế ngũ tâm triều thiên, nhắm mắt điều hòa hơi thở.

Trong thức hải bao la, đài sen Lục Diệp Thanh Liên tỏa ra ánh sáng ngọc bích thanh khiết. Bạch Y Thần Nữ Lâm Tịch hiện ra trong bộ y phục lụa trắng tao nhã, ánh mắt nàng chăm chú nhìn vào khối lôi thạch qua giác quan của tôi, giọng nói mang theo sự ngợi khen chân thành:

"Minh An, trực giác và số mệnh của anh quả thực vô cùng chuẩn xác. Dãy núi Chư Yang Sin chính là linh cốt của nam Trường Sơn, nơi hội tụ long mạch của đại ngàn đất đỏ. Chu kỳ bộc phát năng lượng ba mươi năm một lần của nó chứng minh phong ấn Thổ Mộc viễn cổ đang có sự biến động sâu sắc. Chuyến đi này sẽ là bước ngoặt quyết định cho tiến trình Thể Đạo của anh."

"Lâm Tịch, năng lượng lôi đình trong khối đá này có thể giúp tôi rèn luyện thể phách như thế nào?" Tôi khẽ hỏi trong tâm thức.

Lâm Tịch khẽ mỉm cười, giải thích tường tận:

"Cảnh giới **Hoán Huyết Sơ kỳ** hiện tại của anh đã giúp phàm huyết chuyển hóa thành Thuần Dương Cương Huyết, ba mươi ba đốt sống tủy ngọc thấu quang vững chãi. Nhưng muốn bước lên Hoán Huyết Trung kỳ và đạt tới cảnh giới Cương Huyết Lôi Hóa — tức là khiến dòng máu mang theo uy lực lôi đình dũng mãnh để thích ứng với áp suất địa tầng nghìn mét — anh cần phải hấp thu và dung hòa linh khí mộc lôi của đại ngàn. Khối Mộc Hoàng Lôi Tâm Thạch này chính là chìa khóa khởi đầu. Hãy đặt hai bàn tay lên khối đá, vận hành kình lực dẫn dắt một tia lôi khí thuần khiết đi vào kinh mạch."

Làm theo lời chỉ dẫn của nàng, tôi hít một hơi thật sâu, từ từ áp hai lòng bàn tay chai sạn vào bề mặt khối đá bazan đen nhánh.

"O o o... Xoẹt!"

Khoảnh khắc da thịt tiếp xúc với khối đá, một luồng xung lực nặng trĩu tựa như tiếng sấm rền nghìn dặm lập tức bùng nổ!

Một tia điện nhỏ li ti màu tím vàng từ trong lõi khối thạch bất thần phóng ra, men theo huyệt Lao Cung ở hai lòng bàn tay, xông thẳng vào kinh mạch của tôi!

"Ư...!"

Một cơn đau buốt nhói tựa như ngàn mũi kim nung đỏ đâm xuyên vào da thịt khiến toàn thân tôi khẽ rung lên bần bật. Tia lôi điện ấy cuồng bạo chạy dọc theo hai cánh tay, tràn vào lồng ngực rồi đánh thẳng vào ba mươi ba đốt sống tủy ngọc sau lưng tôi!

Tuy nhiên, thay vì phá hủy kinh mạch, dòng **Thuần Dương Cương Huyết** vốn được tôi bồi đắp từ đất mẹ phù sa sông Tiền lúc này lại phát huy tính nhu hòa và dẻo dai tuyệt đỉnh. Dòng cương huyết ánh kim lập tức cuộn trào bao bọc lấy tia lôi điện, tựa như một tấm lưới nhung êm ái nhưng vô cùng kiên cố, từ từ hấp thu, thuần hóa và nghiền nát luồng sấm sét hoang dại ấy thành những hạt năng lượng tinh khiết nhất.

Từng đốt sống tủy ngọc của tôi phát sáng rực rỡ!

Các thớ cơ bắp, màng xương và từng giọt cương huyết trong cơ thể tôi như được nung luyện qua một lò lửa lôi đình vô hình, trở nên cô đặc, dẻo dai và tràn đầy sức bật kinh người. Dưới làn da của tôi, một lớp ánh sáng lôi điện mờ ảo màu tím vàng khẽ chớp tắt rồi thu liễm hoàn toàn vào sâu trong tủy sống.

Bên cạnh tôi, thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao đồng loạt phát ra tiếng ngân rung trong trẻo, tựa như hai chiến hữu trung thành đang chào đón sự lột xác của chủ nhân.

Tôi mở bừng mắt. Trong con ngươi của tôi, một tia điện quang sắc bén vừa lóe lên rồi biến mất vào đáy mắt đen lánh, sâu thẳm và trầm tĩnh.

Tôi nắm chặt nắm đấm, cảm nhận nguồn kình lực cương mãnh và dẻo dai đang cuộn chảy rào rạt khắp toàn thân.

Tôi với tay lấy chiếc ba-lô dã chiến, cẩn thận đặt thanh đoản côn, đoản đao và khối lôi thạch vào vị trí an toàn, rồi kéo khóa lại.

Ngoài trời đêm Sài Gòn, một làn gió se lạnh từ phương Bắc thổi qua khung cửa sổ. Xa xa ngoài ngàn dặm, tôi như nghe thấy tiếng gầm gừ vang vọng của đại ngàn Tây Nguyên đang vẫy gọi người thủ hộ phàm nhân bước vào một hành trình phong bão mới!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip() + "\n\n" + ACT4.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3200 or word_count > 4500:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,200 - 4,500 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words, 0 forbidden words)
    print(f"[*] [2/6] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường & cấm 'huyết mạch')...")
    meta_patterns = [
        r"\bchương\s+\d+\b",
        r"\bhồi\s+\d+\b",
        r"\bquyển\s+\d+\b",
        r"\btác giả\b",
        r"\bhệ thống\b",
        r"\bbản thảo\b",
        r"\bcanon\b",
        r"\bdatabase\b",
        r"\bplot\b",
        r"\bforeshadowing\b",
        r"\bhuyết mạch\b"
    ]
    for pat in meta_patterns:
        matches = re.findall(pat, raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ ngữ cấm '{matches}' trong văn bản bản thảo!")
            return False
    print(f"[+] Không phát hiện từ ngữ meta/cấm kỵ nào. Đạt chuẩn RULE-07 100%.")

    # 3. Chạy EmotionDopamineEngine để đo lường cảm xúc
    print(f"[*] [3/6] Đo lường chỉ số cảm xúc độc giả qua EmotionDopamineEngine...")
    emo_eng = EmotionDopamineEngine(DB_PATH)
    emo_res = emo_eng.analyze_text(CHAPTER_NUM, raw_content, arc_id="arc_02")
    print(f"  -> Pathos Score: {emo_res['pathos_score']:.2f}/10.0")
    print(f"  -> Dopamine Score: {emo_res['dopamine_score']:.2f}/10.0")
    print(f"  -> Grounding Score: {emo_res['grounding_score']:.2f}/10.0")
    print(f"  -> Đánh giá nhịp độ: {emo_res['pacing_assessment']}")

    # 4. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_nguyen_thi_lanh", "char_trinh_hoai_nam", "char_tuan"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [4/6] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 5. Xuất bản Markdown với YAML Frontmatter và Heading H1
    frontmatter = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {word_count}
date: "{DATE}"
location: "{LOCATION}"
pathos_score: {emo_res['pathos_score']}
dopamine_score: {emo_res['dopamine_score']}
grounding_score: {emo_res['grounding_score']}
description: "Minh An chia tay mẹ trở lại Sài Gòn; Viện Địa tầng phát hiện xung chấn dị thường tại Chư Yang Sin trùng khớp hồ sơ năm 1996; Minh An nhận lệnh chỉ huy đội cảm biến dữ liệu tham gia Đoàn Khảo sát Đặc nhiệm lên đường đến Tây Nguyên; đêm muộn luyện hóa Mộc Hoàng Lôi Tâm Thạch tôi rèn Thuần Dương Cương Huyết."
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

"""
    full_markdown = frontmatter + raw_content
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
    print(f"[+] [5/6] Đã xuất tệp Markdown chuẩn Frontmatter + H1: {md_file_path}")

    # 6. Xuất bản Word (.docx)
    docx_pipe = DocxPipeline()
    docx_file_name = f"ch_{CHAPTER_NUM:03d}.docx"
    docx_file_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02", docx_file_name)
    os.makedirs(os.path.dirname(docx_file_path), exist_ok=True)
    docx_pipe.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=full_markdown,
        output_docx_path=docx_file_path
    )
    print(f"[+] [6/6] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 7. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 7.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Minh An Trở Lại Sài Gòn, Tiếp Nhận Nhiệm Vụ Khảo Sát Chư Yang Sin & Luyện Hóa Lôi Tâm Thạch",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:00:00+07:00",
        CHAPTER_NUM,
        "loc_vien_dia_tang_hcm",
        json.dumps(["char_minh_an", "char_lam_tich", "char_nguyen_thi_lanh", "char_trinh_hoai_nam", "char_tuan"]),
        "Minh An chia tay mẹ tại cù lao Chợ Gạo, mang theo Mộc Hoàng Lôi Tâm Thạch trở lại Sài Gòn. Tại Viện Nghiên cứu Địa tầng, Viện trưởng Trịnh Hoài Nam và kỹ sư Tuấn thông báo phát hiện chuỗi xung chấn dị thường 0.08-0.12 Hz tại Chư Yang Sin, trùng khớp hồ sơ khảo sát năm 1996. Minh An nhận quyết định làm Đội trưởng Kỹ thuật Cảm biến Dữ liệu trong Đoàn Khảo sát Đặc nhiệm lên đường đến Đắk Lắk. Đêm muộn tại phòng trọ Nơ Trang Long, Minh An hấp thu tia linh khí lôi đình từ khối lôi thạch, rèn giũa dòng Thuần Dương Cương Huyết, chuẩn bị tiến vào đại ngàn Tây Nguyên.",
        "Tiếp nhận nhiệm vụ khảo sát thực địa Chư Yang Sin; luyện hóa bước đầu Mộc Hoàng Lôi Tâm Thạch; củng cố Cương Huyết chuẩn bị tiến vào Tây Nguyên."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Xung chấn dị thường 0.08-0.12 Hz xuất hiện tại vòm bazan bát giác Chư Yang Sin; Viện Địa chất thành lập Đoàn Khảo sát Đặc nhiệm tiến vào Tây Nguyên."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An bắt đầu bước vào tiến trình Cương Huyết Lôi Hóa, dùng lôi khí của Mộc Hoàng Lôi Tâm Thạch tôi rèn Thuần Dương Cương Huyết và 33 đốt sống tủy ngọc."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-REL-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch hướng dẫn Minh An phương pháp dung hòa mộc lôi và cương huyết, định vị vai trò then chốt của dãy Chư Yang Sin trong linh mạch non sông."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T21:30:00+07:00"
        inv_data["current_location"] = "Phòng Trọ Nơ Trang Long, Quận Bình Thạnh, TP. Hồ Chí Minh (Chuẩn bị xuất phát đi Đắk Lắk)"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Huyết Thấu Lôi / Khởi Động Lôi Hóa Thể Phách)"

        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json.")

    # 9. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> HOÀN TẤT TOÀN BỘ PIPELINE CHƯƠNG {CHAPTER_NUM} THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

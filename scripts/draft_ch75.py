# -*- coding: utf-8 -*-
"""Draft Chapter 75 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, severe physical and tactical realism, everyday warmth, and multi-tier foreshadowing."""

import os
import sys
import json
import sqlite3
import re

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.canon_engine import CanonEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine

CHAPTER_NUM = 75
CHAPTER_TITLE = "Hải Uyên Tỏa Long"
DATE = "2026-10-23"
LOCATION = "Rãnh Nứt Cực Tù Hải Uyên (-1.200m) & Boong Tàu HQ-268 (Vịnh Gành Rái)"

ACT1 = '''Sáu giờ bốn mươi phút tối.

Tại đáy rãnh nứt Cực Tù Hải Uyên ở độ sâu một ngàn hai trăm mét dưới mực nước biển, cái lạnh hai độ C cùng bóng tối vĩnh cửu bao bọc lấy thềm đá ngọc thạch. Xác con U Minh Quỷ Sa đầu đàn chìm dần vào khe nứt sâu thẳm, dòng máu đen tanh nồng bị dòng xoáy ngầm cuốn phăng đi. Bên cạnh đó, cỗ tàu lặn cơ giới *Kình Uyên 01* nặng hai mươi tấn nằm nghiêng ngả, đuôi tàu bị xé toạc, cụm chân vịt gãy rời và các mạch điện cao áp đã tắt ngấm sau cú va đập kinh hoàng.

Tôi đứng vững hai chân trên thềm đá ngọc thạch cổ xưa, ngước nhìn kỳ quan sừng sững trước mắt.

*Hải Uyên Tỏa Long Trụ*!

Cây cột đá ngọc bích sừng sững vươn cao hơn ba mươi mét giữa lòng đại dương sâu thẳm, to lớn tựa ngọn tháp ngọc thạch chống đỡ thềm lục địa phương Nam. Toàn thân cột đá được chế tác từ ngọc bích viễn cổ màu xanh thẫm, bên trong lập lòe những đường vân sáng tựa hàng ngàn tinh cầu đang dịch chuyển. Quanh thân cột, chín sợi xích thần long đúc bằng hoàng kim cổ đại to bằng thân cây cổ thụ quấn chặt từ đỉnh tháp xuống chân đế. Trên từng mắt xích hoàng kim, vô số cổ văn phù triện tỏa ra vầng hào quang màu vàng ấm áp, tạo thành một lồng ánh sáng hình vòm đường kính năm mươi mét đẩy lùi hoàn toàn bóng đen quánh đặc của vực sâu.

Nhưng khi bước tới gần chân đế cột đá, sắc mặt tôi chợt ngưng trọng.

Dưới chân bệ trụ bazan, mũi khoan kim cương đường kính một mét của tàu lặn *Kình Uyên 01* trước khi bị vô hiệu hóa đã kịp khoét sâu vào lòng đá hơn hai mét. Mũi khoan tà đạo đã cày nát một mảng phù triện trấn áp, làm lộ ra một khe nứt địa chất đen ngòm.

Từ khe nứt ấy, từng đợt bọt khí màu đen thẫm mang theo mùi lưu huỳnh nồng nặc và âm trọc khí buốt giá đang cuồn cuộn trào ra!

Đó là luồng hàn sát âm trọc tích tụ nơi đáy vực hàng ngàn năm. Khí trọc tràn ra tới đâu, lớp ngọc thạch xung quanh lập tức bị ăn mòn loang lổ, biến thành màu xám tro tử khí. Nếu để khe nứt này tiếp tục rò rỉ, dòng trọc khí đáy biển sẽ men theo các dòng hải lưu ngầm tràn lên vịnh Gành Rái, phá hủy sinh thái rừng ngập mặn Cần Giờ và làm đảo lộn hoàn toàn trục cân bằng thủy mạch của mạng lưới Thủy Môn Thập Nhị Tiêu!

*"Minh An, mũi khoan kim cương của tàu lặn đã chạm vào mạch ngầm phong tỏa chân trụ!"* Tiếng nói của Lâm Tịch khẽ vang lên từ thức hải, thanh âm nàng mang theo vẻ nghiêm cẩn hiếm thấy. *"Chín sợi xích thần long hoàng kim đang rung lắc dữ dội vì mất đi điểm tựa địa tầng. Phải phong tỏa miệng nứt ngay lập tức, nếu không phản lực từ áp lực nước một trăm hai mươi át-mốt-phe sẽ bẻ gãy một góc bệ móng!"*

"Phong tỏa bằng cách nào?" Tôi truyền niệm hỏi nhanh. "Dưới áp lực nước một triệu ký-lô-gam trên mỗi mét vuông này, bê-tông công nghiệp hay kim loại thông thường đều sẽ bị ép vỡ vụn trong chớp mắt!"

*"Dùng Thuần Dương Cương Huyết và Trấn Thủy Đoản Đao!"* Lâm Tịch chỉ dẫn mạch lạc. *"Đoản đao mang bản tính của đồng thau trấn thủy, kết hợp cùng nhiệt lượng của Cương Huyết sẽ tạo ra hỏa kình nung chảy các tinh thể bazan và ngọc vụn, ép chúng kết tinh trở lại thành thạch anh khóa miệng vực!"*

"Được!"

Tôi không chút chần chừ. Toàn thân tôi nhức nhối sau trận kịch chiến với tàu lặn, ba mươi ba đốt sống lưng vừa mới trải qua quá trình nén ép tôi luyện vẫn còn âm ỉ sốt bỏng. Nhưng trách nhiệm bảo vệ long mạch duyên hải không cho phép tôi do dự.

Tôi bước nhanh tới sát miệng nứt bazan. Tay trái tôi rút thanh Trấn Thủy Đoản Đao rỉ xanh, cắm phập lưỡi đao thẳng vào tâm điểm khe nứt đang sủi bọt khí đen kịt!

"Keng!"

Lưỡi đao cổ thụy vừa chạm vào đá ngầm, luồng âm trọc buốt giá lập tức men theo thân đao truyền ngược vào cánh tay tôi, biến lớp da thịt thành màu lam tím tái. Cái lạnh thấu xương dường như muốn làm đông cứng mọi kinh mạch!

"Mở cho ta!"

Tôi gầm lên một tiếng trầm đục trong lồng ngực. Thức thứ tám *Hoán Huyết Hóa Cương* bùng nổ đến cực hạn!

Trái tim tôi đập rộn rã với tần số mạnh mẽ, tống xuất từng đợt Cương Huyết Thuần Dương màu đồng thau chảy tràn vào cánh tay trái. Dòng máu nóng bỏng rực lửa ép ngược luồng âm trọc ra ngoài, men theo rãnh lưỡi đao rót thẳng vào sâu trong lòng đất đá bazan nứt nẻ!

Đồng thời, tay phải tôi giáng một chưởng Thể Đạo nén kình lực *Kính Phách Phản Chấn* nện mạnh vào chuôi đao!

"Xèo xèo xèo... ẦM!"

Nhiệt lượng cực đại của Thuần Dương Cương Huyết kết hợp cùng kình lực Thể Đạo va chạm dữ dội với khối nước biển hai độ C dưới đáy vực, tạo nên một hiện tượng nhiệt động lực học kỳ vĩ. Các mảnh vụn bazan và bụi kim cương bị nung chảy đỏ rực, sau đó bị áp suất thủy tĩnh một trăm hai mươi át-mốt-phe nén chặt tức thì thành một khối ngọc thạch cứng tựa kim cương, bịt kín hoàn toàn khe nứt rò rỉ!

Dòng khí đen ngắt lịm. Vùng nước xung quanh chân đế cột đá lấy lại vẻ trong trẻo lam ngọc ban đầu.

Đúng lúc ấy, kỳ tích xuất hiện!

"U u u... Ô N G !"

Một tiếng ngân vang trầm hùng tựa tiếng rồng ngâm từ thời viễn cổ bất thần rung chuyển khắp lòng rãnh nứt Cực Tù Hải Uyên! Thân trụ *Hải Uyên Tỏa Long Trụ* bừng sáng chói lọi, chín sợi xích thần long hoàng kim đồng loạt phát xuất những chuỗi ký tự kim quang uốn lượn bay lượn trên không trung dưới nước, hòa nhập vào ba mươi ba đốt sống của tôi tựa như một sự công nhận thiêng liêng.

Tại vị trí trung tâm bệ đá nơi tôi vừa phong tỏa, một luồng ánh sáng hoàng kim rực rỡ ngưng tụ lại, đẩy lên một vật phẩm cổ xưa:

Đó là một khối ngọc tỷ vuông vức cỡ bàn tay đúc bằng ngọc bích đáy biển, bốn phía chạm khắc hình chín con rồng vàng uốn lượn ôm lấy một viên minh châu màu lam thẫm. Mặt dưới ngọc tỷ khắc bốn chữ triện cổ: *Tỏa Long Huyền Tỷ*!

Đây chính là Trận Nhãn thứ bảy của Thủy Môn Thập Nhị Tiêu!

Tôi cẩn thận cầm lấy Tỏa Long Huyền Tỷ, cất gọn vào túi nhung cách nước bên trong ngực áo dã chiến. Luồng năng lượng ấm áp từ ngọc tỷ lan tỏa, lập tức xoa dịu những thương tổn trên các khớp xương sau trận huyết chiến.

Chưa dừng lại ở đó, tôi bơi qua xác cỗ tàu lặn *Kình Uyên 01*. Bằng sức mạnh Luyện Cốt Hậu kỳ, tôi dùng Hắc Thiết Đoản Côn bẩy bung nắp khoang điều khiển chống nước của tàu địch. Bên trong buồng lái ngập nước, cụm ổ cứng quang học chứa dữ liệu hải đồ tác chiến và định vị vệ tinh của Tập đoàn Cửu Long Thiên Hải vẫn còn nguyên vẹn.

Tôi tháo rời chiếc ổ cứng quân sự bọc titan ra khỏi giá đỡ, buộc chặt sau lưng cùng chiếc máy phát tín hiệu âm học của Tuấn.

Mọi mục tiêu dưới đáy biển ngàn mét đã hoàn thành trọn vẹn!'''

ACT2 = '''Bảy giờ mười lăm phút tối.

Tại đài chỉ huy Tàu Tuần Tra Cao Tốc HQ-268 trên mặt vịnh Gành Rái, bầu không khí căng thẳng đến nghẹt thở. Đã gần hai tiếng đồng hồ trôi qua kể từ khi bóng dáng Minh An biến mất dưới làn nước đen thẳm ngoài phao số không.

Kỹ sư Tuấn ngồi dán mắt vào màn hình hiển thị thủy âm sonar thụ động. Mồ hôi ướt đẫm trán anh dù gió biển đêm thổi lồng lộng.

"Thuyền trưởng! Cụm sonar vừa ghi nhận những chấn động âm học cực lớn ở độ sâu hơn một ngàn mét cách đây ba mươi phút!" Tuấn lo lắng báo cáo. "Có tiếng nổ của dòng điện cao áp, sau đó là xung lực chấn động của khối đá sụp đổ. Suốt hai mươi phút qua, tín hiệu định vị ngầm của Minh An hoàn toàn im lặng!"

Đại úy Lê Đình Hùng đứng cạnh bàn hải đồ điện tử, bàn tay người thuyền trưởng siết chặt lan can thép đến trắng bệch các khớp ngón:

"Độ sâu một ngàn hai trăm mét... Áp lực nước ấy có thể bóp bẹp một vỏ tàu ngầm thông thường. Liệu cậu ấy có gặp nạn trước hỏa lực của tàu lặn Cửu Long?"

Đúng lúc sự âu lo dâng lên tột độ, chiếc loa máy thu thủy âm bỗng phát ra chuỗi âm thanh thanh thoát:

"Tích... Tích... Tò... Tí... Tích!"

Ba xung âm ngắn, một xung âm dài, lặp lại ba lần chuẩn xác theo bảng mã quy ước quân sự!

Trên màn hình trắc diện âm học ba chiều, một chấm sáng màu xanh ngọc bích rực rỡ xuất hiện ở độ sâu tám trăm mét, đang di chuyển thẳng đứng lên phía trên với vận tốc ổn định hai mét mỗi giây!

"Tín hiệu an toàn! Mã 0-7-PASS!" Tuấn nhảy bật khỏi ghế chỉ huy, hét lớn trong sự vỡ òa phấn khích. "Minh An còn sống! Cậu ấy đang nổi lên! Cậu ấy đã thành công!"

Toàn thể kíp trực trên đài chỉ huy HQ-268 đồng loạt thở phào nhẹ nhõm, những nụ cười rạng rỡ nở trên gương mặt dạn dày sóng gió của các chiến sĩ hải quân.

"Bật toàn bộ đèn pha công suất lớn rọi xuống mặt biển mạn hữu!" Thuyền trưởng Lê Đình Hùng hạ lệnh dõng dạc, ánh mắt ngập tràn sự khâm phục. "Chuẩn bị thang dây cứu sinh và tổ quân y tiếp đón đồng chí An!"

Dưới lòng đại dương sâu thẳm, hành trình trồi lên của tôi là một kỳ tích sinh học.

Một thợ lặn thương mại nếu xuống sâu hàng trăm mét, khi trở lên mặt nước bắt buộc phải nằm trong buồng giải áp suốt nhiều ngày đêm để khử khí ni-tơ trong máu, tránh nguy cơ thuyên tắc mạch máu gây tử vong. Nhưng với tôi, dòng Thuần Dương Cương Huyết lưu chuyển với tốc độ gấp ba lần bình thường đã tự động phân tách và bài tiết các bọt khí siêu nhỏ qua từng lỗ chân lông.

Ở trạm dừng sáu trăm mét, nhiệt độ nước ấm dần lên mười độ C.

Ở trạm dừng ba trăm mét, ánh sáng đèn pha tuần tra từ mặt nước bắt đầu rọi xuống mờ ảo tựa những dải lụa bạc xuyên qua màn đêm.

Và khi đồng hồ đo độ sâu chỉ về con số không mét, mặt nước vịnh Gành Rái bỗng rẽ ra thành hai làn sóng trắng xóa!

"ÀO!"

Tôi đạp mạnh dòng nước, toàn thân phóng vút lên không trung hơn ba mét tựa một mũi tên lam ngọc, rồi nhẹ nhàng đáp chân xuống sàn boong thép chống trượt của tàu tuần tra HQ-268!

Bọt nước biển bắn tung tóe dưới ánh đèn pha sáng rực. Tôi đứng thẳng người, rũ bỏ làn nước mặn chát bám trên mái tóc. Dù quần áo dã chiến rách nhiều mảng, bả vai và cánh tay rướm những vệt máu bầm, nhưng thần sắc tôi sáng quắc, sống lưng thẳng tắp như ngọn thương thép.

"Minh An!" Tuấn lao tới ôm chầm lấy tôi, giọng nghẹn ngào. "Cậu làm được rồi! Cậu thực sự quay về từ cõi chết!"

Thuyền trưởng Lê Đình Hùng cùng tổ y sĩ vội vã chạy đến. Nhìn thấy thanh Hắc Thiết Đoản Côn bọc da bò sau lưng tôi và chiếc ổ cứng titan dính rong rêu đáy biển, người thuyền trưởng dạn dày trận mạc đứng nghiêm chào theo điều lệnh quân đội:

"Chào mừng Giám Đốc An trở về an toàn! Thủy thủ đoàn HQ-268 vinh dự được đồng hành cùng đồng chí!"

Cùng lúc đó, từ đài quan sát phía mũi tàu, một chiến sĩ cảnh giới báo cáo vang dội qua bộ đàm:

"Báo cáo Thuyền trưởng! Tàu mẹ *Thiên Hải 09* năm ngàn tấn của địch ở ngoài phao số không phát hiện tàu lặn mất tích, radar của chúng vừa quét thấy biên đội tàu Cảnh sát biển Vùng 3 của ta đang tiến tới đón lõng. Chúng đã kéo neo, quay mũi tàu tháo chạy hết tốc lực về phía hải phận quốc tế!"

"Không cần truy đuổi vào vùng biển giáp ranh," Thuyền trưởng Hùng mỉm cười kiên định. "Nhiệm vụ cốt lõi của chúng ta tại hải phận Cần Giờ đã toàn thắng. Cửa ngõ phương Nam vẫn vững như bàn thạch!"'''

ACT3 = '''Tám giờ ba mươi phút tối.

Sóng biển đêm vỗ dập dồn vào mạn tàu HQ-268 đang thả neo giữ vị trí chốt chặn tại vùng biển êm gần khu dự trữ sinh quyển Rừng Sác. Trên bầu trời đêm, những đám mây giông đã tan biến, để lộ dải ngân hà lấp lánh muôn ngàn ánh sao phản chiếu xuống mặt nước lung linh.

Trong phòng y tế của tàu, trung úy y sĩ quân y đang nhìn chằm chằm vào máy đo huyết áp điện tử và máy điện tim với vẻ mặt không thể tin nổi.

"Huyết áp một trăm hai mươi trên tám mươi, nhịp tim bốn mươi nhịp một phút, nồng độ ô-xy trong máu đạt chín mươi chín phần trăm... Không hề có dấu hiệu ngộ độc ni-tơ hay phù phổi áp lực!" Viên y sĩ lắc đầu kinh ngạc nhìn tôi. "Thưa anh An, nếu không tận mắt thấy anh nhảy từ dưới đáy biển lên boong tàu, tôi sẽ nghĩ anh vừa bước ra từ một phòng tập thể thao cao cấp. Cấu trúc sinh lý của anh dường như đã vượt xa mọi tiêu chuẩn y học hiện đại!"

Tôi mỉm cười, cảm ơn người y sĩ rồi mặc lại chiếc áo phông đen khô ráo do anh em thủy thủ đoàn cho mượn. Trong túi áo trong ngực trái, chiếc trâm ngọc của Lâm Tịch vẫn tỏa ra hơi ấm dịu dàng xoa dịu tâm thức tôi.

Bước ra khu vực bàn ăn nhỏ cạnh boong sau của tàu, mùi thơm nồng nàn của thức ăn lập tức đánh thức cơn đói cồn cào trong dạ dày tôi.

Trên chiếc bàn gỗ cố định, anh nuôi của tàu vừa bưng ra hai tô mì tôm trứng nóng hổi nghi ngút khói. Sợi mì vàng óng ngập trong nước dùng cay nồng rắc đầy hành hoa xắt nhỏ và tiêu đen Phú Quốc thơm lừng, bên trên là hai quả trứng chần lòng đào béo ngậy. Kèm theo đó là một đĩa cá cơm khô Cần Giờ chiên giòn rụm màu cánh gián và một ấm cà phê phin bằng nhôm đang tí tách nhỏ từng giọt đen nhánh đậm đà.

"Ăn đi Minh An!" Tuấn đẩy tô mì về phía tôi, đôi mắt anh lấp lánh niềm vui. "Đặc sản tàu hải quân đấy! Mì tôm trứng và cá cơm khô giữa biển đêm Sài Gòn, bảo đảm ngon hơn mọi nhà hàng năm sao trên đường Nguyễn Huệ!"

Tôi ngồi xuống chiếc ghế sắt, bưng tô mì tôm húp một ngụm nước súp nóng hổi. Vị cay ấm của ớt hiểm và tiêu đen lan tỏa khắp vòm họng, xua tan nốt những tàn dư lạnh giá của vùng biển sâu ngàn mét. Cắn một miếng cá cơm giòn rụm đậm đà vị mặn của muối biển, tôi cảm nhận được sự ấm áp, bình dị và chân thực của đời sống trần gian.

Đây chính là cuộc sống mà tôi muốn bảo vệ.

Không phải vì danh vọng hay hư ảo quyền lực, mà là để những con người bình thường trên mảnh đất này — những người lính biển kiên trung, những người bạn đồng hành chí cốt như Tuấn, và hàng triệu người dân Sài Gòn — có thể an yên đón nhận những sớm mai bình dị.

"Tít... tít."

Chiếc điện thoại bọc túi chống nước của tôi trên bàn bỗng rung lên. Màn hình sáng lên với dòng thông báo tin nhắn từ mẹ ở quê gửi lúc chập tối:

*"An à, mẹ xem thời tiết thấy ngoài biển Nam Bộ đang có giông gió. Con đi công tác khảo sát thực địa ở Cần Giờ có bị mưa ướt không? Nhớ ăn uống đầy đủ nghe con, đừng có tiết kiệm tiền ăn mà thức khuya làm dữ liệu. Khi nào xong việc về phòng trọ bên Nơ Trang Long thì gọi cho mẹ hay."*

Nhìn những dòng chữ mộc mạc của mẹ, nơi khóe mắt tôi chợt cay cay. Một cảm giác bình yên sâu lắng dâng trào trong lồng ngực. Tôi nhẹ nhàng bấm phím nhắn lại:

*"Con xong việc rồi mẹ ơi, biển êm lắm. Tối nay con ăn cơm ngon với anh em kỹ sư. Mẹ ngủ sớm đi nhé, cuối tuần con gọi về cho mẹ."*

Tuấn ngồi đối diện, vừa nhâm nhi ly cà phê phin đắng đót vừa cắm chiếc ổ cứng quân sự bọc titan thu được từ tàu lặn địch vào chiếc máy tính xách tay chuyên dụng của Viện Địa tầng.

Các dòng mã nhị phân màu xanh lá cây chạy vun vút trên màn hình. Với trình độ kỹ sư viễn thông thượng thừa, chỉ sau mười phút, Tuấn đã bẻ khóa thành công phân vùng dữ liệu tối mật của Tập đoàn Cửu Long Thiên Hải.

"Minh An, nhìn vào đây!" Tuấn hạ thấp giọng, chỉ tay vào tấm bản đồ trắc địa đa phổ hiện lên trên màn hình. "Những kẻ tà đạo không chỉ nhắm vào lưu vực sông ngòi Sài Gòn và cửa biển Cần Giờ!"

Trên màn hình, mạng lưới Thủy Môn Thập Nhị Tiêu hiển thị bảy điểm sáng màu vàng tượng trưng cho bảy cọc tiêu đã được hóa giải an toàn. Nhưng từ điểm sáng thứ bảy tại Cực Tù Hải Uyên, một đường đứt gãy địa chất ngầm màu đỏ rực kéo dài ngược lên hướng đông bắc, xuyên qua thềm lục địa, đâm thẳng vào khối đá granite cổ xưa của vùng núi rừng Đông Nam Bộ!

Tại điểm giao nhau giữa các nếp đứt gãy, tọa độ của cọc tiêu thứ tám nhấp nháy liên tục:

*Đỉnh Núi Chứa Chan — Thềm Đá Cổ Thần Quy (Đồng Nai)*!

"Cọc tiêu thứ tám không nằm dưới sông nước, mà được chôn sâu dưới lòng đá granite của dãy núi cổ sót lại từ kỷ đệ tứ!" Tuấn thì thầm kinh ngạc. "Cửu Long Thiên Hải đã điều động chi nhánh nội địa của chúng tiếp cận khu vực này từ một tuần trước!"

Cùng lúc đó, trong thức hải tôi, đài sen ngọc bích của Lâm Tịch khẽ xoay tròn. Vạt áo trắng thanh khiết của nàng lay động trong làn sương mờ ảo.

*"Núi Chứa Chan..."* Giọng nói của Lâm Tịch vang lên, trong trẻo tựa tiếng chuông bạc nhưng ẩn chứa một thoáng bồi hồi từ ngàn năm trước. *"Nơi ấy từng có dấu tích của một người quen cũ... Một trận nhãn phong tỏa bằng kiếm ý viễn cổ. Hành trình tiếp theo của ngươi sẽ không còn đơn thuần là chiến đấu với sức nước, mà là bước vào lãnh địa của đá và kiếm."*

Tôi nhìn ra màn đêm biển cả mênh mông, nơi ngọn hải đăng Cần Giờ phía xa xa đang quét những luồng sáng kiên định vào không gian. Gió biển đêm lùa qua mái tóc, mang theo hơi thở của đất trời phương Nam.

Bảy cọc tiêu đã an định. Nhưng bức tranh toàn cảnh của đại phong ấn đang từng bước mở rộng ra ngoài phạm vi sông ngòi đô thị.

Tôi hít một hơi gió biển trong lành, ánh mắt rực sáng niềm tin kiên định. Dù thử thách phía trước là núi cao hay vực sâu, Thể Đạo phàm nhân này cũng sẽ vững bước tiến lên, phá vỡ mọi mưu toan đen tối để bảo vệ mảnh đất quê hương.'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/5] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3300 or word_count > 3700:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,300 - 3,650 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words)
    print(f"[*] [2/5] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường)...")
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
        r"\bforeshadowing\b"
    ]
    for pat in meta_patterns:
        matches = re.findall(pat, raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ ngữ meta '{matches}' trong văn bản bản thảo!")
            return False
    print(f"[+] Không phát hiện từ ngữ meta nào. Đạt chuẩn RULE-07 100%.")

    # 3. Đăng ký thực thể mới vào novel_os.db
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'artifact_toa_long_huyen_ty',
        'Tỏa Long Huyền Tỷ',
        'item',
        json.dumps(['Trận Nhãn thứ bảy', 'Hải Uyên Long Tỉ', 'Ngọc Tỷ Chín Rồng'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'material': 'Deep sea jade & archaic gold dragons', 'function': 'Trận nhãn cốt lõi của Hải Uyên Tỏa Long Trụ, trấn áp âm trọc Cực Tù'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'loc_nui_chua_chan',
        'Đỉnh Núi Chứa Chan (Đồng Nai)',
        'location',
        json.dumps(['Núi Chứa Chan', 'Gia Lào', 'Thềm Đá Cổ Thần Quy'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'elevation': '837m', 'terrain': 'Khối đá granite cổ kỷ đệ tứ', 'significance': 'Vị trí cọc tiêu thứ tám Thủy Môn Thập Nhị Tiêu'}, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

    # 4. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_tuan", "char_lam_tich", "char_le_dinh_hung"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [3/5] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 5. Xuất bản Markdown với YAML Frontmatter và Heading H1
    frontmatter = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {word_count}
date: "{DATE}"
location: "{LOCATION}"
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

"""
    full_markdown = frontmatter + raw_content
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
    print(f"[+] [4/5] Đã xuất tệp Markdown chuẩn Frontmatter + H1: {md_file_path}")

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
    print(f"[+] [5/5] Đã xuất tệp Word (.docx): {docx_file_path}")

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
        "Hàn Gắn Phong Ấn Hải Uyên & Khải Hoàn Trên Boong Tàu HQ-268",
        CHAPTER_NUM,
        1,
        f"{DATE}T20:30:00+07:00",
        CHAPTER_NUM,
        "loc_cuc_tu_hai_uyen",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_le_dinh_hung"]),
        "Minh An dùng Thuần Dương Cương Huyết và Trấn Thủy Đoản Đao phong tỏa khe nứt bazan rò rỉ âm trọc khí dưới chân Hải Uyên Tỏa Long Trụ. Nhận được sự công nhận từ 9 sợi xích thần long hoàng kim và thu đắc Trận Nhãn thứ bảy Tỏa Long Huyền Tỷ cùng ổ cứng dữ liệu tàu Kình Uyên 01. Minh An giảm áp sinh học thành công, đạp sóng trở về tàu tuần tra HQ-268. Tàu mẹ Thiên Hải 09 của Cửu Long Thiên Hải tháo chạy. Trên boong tàu đêm ấm áp, Minh An thưởng thức tô mì tôm trứng nóng hổi, nhận tin nhắn từ mẹ và giải mã tọa độ cọc tiêu thứ tám tại Núi Chứa Chan (Đồng Nai).",
        "Phong tỏa hoàn tất cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ; thu đắc Tỏa Long Huyền Tỷ; giải mã tọa độ cọc tiêu thứ tám tại Núi Chứa Chan (Đồng Nai)."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An phong tỏa thành công cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ, đoạt Tỏa Long Huyền Tỷ và giải mã tọa độ cọc tiêu thứ tám tại thềm đá Núi Chứa Chan (Đồng Nai)."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T20:30:00+07:00"
        inv_data["current_location"] = "Tàu Tuần Tra Cao Tốc HQ-268 (Vịnh Gành Rái / Cần Giờ)"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ (Cương Huyết Thuần Dương)"
        
        # Thêm Tỏa Long Huyền Tỷ vào inventory nếu chưa có
        existing_names = [it.get("name") for it in inv_data.get("core_weapons_and_artifacts", [])]
        if "Tỏa Long Huyền Tỷ (Trận Nhãn Thủy Môn Tiêu số 7)" not in existing_names:
            inv_data.setdefault("core_weapons_and_artifacts", []).append({
                "name": "Tỏa Long Huyền Tỷ (Trận Nhãn Thủy Môn Tiêu số 7)",
                "type": "Cổ ngọc tỷ trận nhãn / Thần vật trấn hải",
                "location": "Túi nhung cách nước trong ngực áo dã chiến",
                "condition": "Nguyên vẹn 100%, ngọc bích chạm chín rồng hoàng kim ngậm minh châu lam thẫm",
                "durability": "100/100",
                "function": "Trận nhãn cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ; trấn áp âm trọc Cực Tù, điều hòa phong ba đại dương và xoa dịu thương tổn xương cốt"
            })
            
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json với Tỏa Long Huyền Tỷ.")

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

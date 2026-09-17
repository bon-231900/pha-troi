# -*- coding: utf-8 -*-
"""Draft Chapter 72 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 72
CHAPTER_TITLE = "Hoán Huyết Hóa Cương"
LOCATION = "Phòng thí nghiệm ngầm B2 & Tầng thượng Viện Địa tầng Đô thị (TP.HCM)"
DATE = "2026-10-23"

ACT1 = '''Mười giờ ba mươi phút đêm ngày hai mươi hai tháng Mười.

Phòng thí nghiệm bảo mật B2 của Viện Địa tầng Đô thị — sâu hai mươi mét dưới lòng đất Quận 1 — rền vang tiếng rè rè của máy phân tích phổ quang và máy quét từ trường cao tần. Vừa rời giếng ngầm Ba Son, mùi khét của dầm thép đứt và hàn khí buốt giá đáy nước bốn mươi hai mét dường như vẫn còn vương trên áo dã chiến của tôi.

Kỹ sư Tuấn tựa lưng vào ghế xoay, tay cầm tách cà phê nguội ngắt, mắt dán chặt bảng điều khiển. Trên vách kính cường lực phía trước, sơ đồ mạng lưới thủy văn thành phố Hồ Chí Minh sáng rực dưới ánh đèn huỳnh quang xanh dịu.

Bỗng nhiên, chiếc còi báo động vi chấn trên bàn làm việc phát ra tiếng bíp dài trong trẻo tựa tiếng chuông khánh đồng cổ.

"Minh An, nhìn màn hình giám sát này!" Tuấn đặt vội tách cà phê xuống, tròng kính cận phản chiếu những dải sóng dao động đang đồng loạt vẽ nên những đường cong hoàn mỹ. "Toàn bộ sáu trạm quan trắc địa chấn ngầm dọc lưu vực sông Sài Gòn vừa ghi nhận hiện tượng chưa từng xuất hiện trong lịch sử đo đạc của Viện ta!"

Tôi bước nhanh lại gần bàn làm việc, ngưng thần quan sát biểu đồ địa tầng.

Trên màn hình kỹ thuật số, sáu điểm nút địa lý xung yếu lần lượt phát sáng rực rỡ: Ngã ba Nhà Bè, rạch Lò Gốm, bến Phú Định, Mũi Đèn Đỏ, mố đá Cầu Mống, và ụ tàu Ba Son. Sáu điểm nút cùng phát xuất tần số dao động đồng nhất 0.12 Héc — đúng bằng nhịp tim của lõi đất mẹ tôi từng cảm nhận tại Cầu Mống.

Từ sáu điểm sáng hoàng kim, những đường chỉ năng lượng vàng đồng đan bện vào nhau, tạo thành đồ án Lục Giác Trấn Thủy khổng lồ ôm trọn trung tâm đô thị và bán đảo Thủ Thiêm. Luồng âm sát địa tầng làm đục nước và sạt lở bờ kè suốt nhiều tháng qua đã hoàn toàn bị long khí thuần khiết ép lui.

"Sáu cọc tiêu tiền tuyến đã liên kết trọn vẹn thành một thể thống nhất," tôi siết nhẹ nắm tay, cảm nhận sự an định của mạch đất dưới chân. "Tiền nhân đã tính toán chu toàn từng bước để bảo bọc dòng sông này suốt ngàn năm."

"Nhưng nguy cơ vẫn chưa dừng lại ở đó," giọng nói trầm hùng mang vẻ uy nghiêm vang lên từ phía cửa thép phòng thí nghiệm.

Cửa cách âm mở ra, Viện trưởng Trịnh Hoài Nam bước vào trong chiếc áo khoác dã chiến xám sẫm đượm sương đêm. Dưới cánh tay ông là cặp tài liệu da đen dán niêm phong đỏ thẫm: *Hồ sơ chuyên án đặc biệt — Cục Cảnh sát Giao thông Đường thủy & Bộ Tư lệnh Vùng 2 Hải quân*.

"Viện trưởng!" Tôi và Tuấn đồng loạt đứng nghiêm chào.

Viện trưởng Nam gật đầu, vỗ nhẹ vai tôi, ánh mắt chan chứa niềm tự hào:

"Hai cậu đã làm nên kỳ tích tại ụ tàu Ba Son. Nhưng báo cáo thẩm vấn nhanh từ tổ tuần tra đặc nhiệm đường thủy gửi sang cách đây ba mươi phút cho thấy, quân cờ chúng ta vừa triệt phá chỉ là góc của tảng băng trôi."

Ông mở cặp tài liệu, rút ra những bức ảnh trinh sát hồng ngoại chụp lúc chạng vạng ngoài cửa biển:

"Tên Hắc Lân Thiết Vệ bị thương tháo chạy trên ca-nô cao tốc đã không kịp thoát ra hải phận quốc tế. Ca-nô của gã bị tàu tuần tra Hải quân ép dạt vào rạn đá cù lao Cần Giờ. Dù gã nhảy xuống biển tẩu thoát, nhưng lực lượng chức năng đã thu giữ được thiết bị định vị vệ tinh và tài liệu mã hóa. Bọn chúng trực thuộc nhánh vũ trang viễn dương của tổ chức Cửu Long Thiên Hải."

Tôi nhìn vào bức ảnh trinh sát. Giữa màn đêm kịt ngoài phao số không thuộc vịnh Gành Rái, bóng một con tàu khổng lồ dài hơn một trăm ba mươi mét đang thả neo sừng sững.

"Con tàu này đăng ký danh nghĩa tàu khảo sát địa chấn dầu khí đa quốc gia mang tên *Thiên Hải 09*," Viện trưởng Nam trầm giọng, chỉ tay vào tọa độ rãnh nứt ngoài khơi Cần Giờ. "Thực chất, đó là căn cứ di động của bọn chúng, trang bị cần cẩu siêu trọng và thiết bị lặn biển sâu không người lái. Mục tiêu cuối cùng của chúng là dùng tà trận Cửu U Thôn Thiên mở toang đại phong ấn đáy biển sâu ngàn mét ngoài thềm lục địa!"

Tôi đứng thẳng người, cất giọng đanh thép:

"Báo cáo Viện trưởng, với cương vị Giám Đốc Kỹ Thuật Dữ Liệu của Viện Địa tầng, tôi xin cam đoan: Dù kẻ địch có đem tàu chiến hay phương tiện cơ giới hiện đại đến đâu, chừng nào mạng lưới dữ liệu địa chấn và cọc tiêu tiền tuyến của chúng ta còn đứng vững, âm mưu của chúng nhất định sẽ bị chặn đứng."

Viện trưởng Nam nhìn tôi, mỉm cười tin cậy:

"Tôi tin cậu, Minh An. Bây giờ, chúng ta cần giải mã toàn bộ những gì thu được từ tên Thiết Vệ trước khi trời sáng."'''

ACT2 = '''Mười một giờ bốn mươi lăm phút đêm.

Chiếc bàn kim loại chuyên dụng chống rung giữa phòng B2 được dọn sạch. Tôi cẩn thận đặt hai món chiến lợi phẩm đoạt được từ Hắc Lân Thiết Vệ lên mặt bàn: Chiếc hộp đồng cổ vân mai rùa thu từ hầm Cầu Mống và tấm bản đồ da dê cổ sẫm màu lấy từ người tên Thiết Vệ tại Ba Son.

Bên cạnh đó, chiếc lệnh bài huyền thiết nặng một cân rưỡi mang số hiệu *Thiết Vệ Tam* cũng được đặt dưới máy quét hiển vi điện tử.

Tuấn khởi động cụm đèn chiếu tử ngoại và máy quét huỳnh quang tia X. Những chùm sáng xanh lam và tím sẫm quét chầm chậm qua từng thớ da dê ngả màu nâu đất. Trên màn hình máy tính dã chiến, các lớp bụi bẩn, vết máu khô và lớp mực ngụy trang dần dần được bóc tách bằng thuật toán xử lý hình ảnh quang phổ.

"Kỳ diệu thật..." Tuấn thốt lên, ngón tay phóng to từng phân vùng ảnh quét. "Minh An, tấm bản đồ da dê này không phải bản vẽ địa lý thông thường. Đây là sơ đồ trận pháp hải trình kết hợp phép chiếu thiên văn cổ đại!"

Tôi ghé sát mắt nhìn những đường nét màu đỏ máu hiện lên trên màn hình.

Bản đồ thể hiện rõ ràng toàn bộ dòng chảy uốn lượn của sông Sài Gòn, sông Đồng Nai, đổ dồn về ngã ba Nhà Bè rồi phân nhánh qua rừng ngập mặn Cần Giờ trước khi lao thẳng ra vịnh Gành Rái. Sáu cọc tiêu tiền tuyến trên đất liền — nơi tôi đã từng bước đặt chân qua — được vẽ thành sáu vòng tròn nhỏ bằng đồng thau, mang tên gọi *Lục Môn Tỏa Thủy*.

Nhưng điểm đáng sợ nhất nằm ở ngoài khơi xa, cách mũi Cần Giờ hơn hai mươi hải lý về phía Đông Nam.

Nơi thềm lục địa đột ngột sụt lún thành rãnh nứt vực thẳm sâu hơn một ngàn hai trăm mét dưới mực nước biển, tấm bản đồ khắc họa một vòng xoáy chín tầng màu đen thẫm, kèm theo bốn chữ cổ khắc chìm: *Cực Tù Hải Uyên*.

"Đáy biển sâu một ngàn hai trăm mét..." Tuấn nuốt nước bọt, trán lấm tấm mồ hôi dù nhiệt độ phòng duy trì ở mức hai mươi độ C. "Minh An, ở độ sâu đó, áp suất thủy tĩnh lên tới hơn một trăm hai mươi át-mốt-phe, tương đương mỗi xăng-ti-mét vuông bề mặt cơ thể phải chịu sức nặng hơn một trăm hai mươi ký! Ngay cả tàu ngầm quân sự lặn xuống độ sâu đó cũng có nguy cơ bị bẹp rúm tựa vỏ lon rỗng!"

"Không chỉ có áp suất," tôi trầm ngâm chỉ vào những ký tự cổ khắc quanh vòng xoáy Cực Tù Hải Uyên. "Ghi chép địa chất cổ cho thấy đây là nơi phong ấn tầng thứ sáu của Cực Tù Lục Trọng Giới — nơi tiền nhân giam giữ những thực thể tà đạo viễn cổ từ hai triệu rưỡi năm trước. Sáu cọc tiêu Ba Son, Cầu Mống, Nhà Bè chỉ là chốt khóa ngoài để giữ cho long mạch nước ngọt không bị nhiễm tà khí biển mặn. Trận nhãn cốt lõi thực sự nằm dưới vực sâu ngàn mét ấy."

"Còn đây là thời gian hành động của bọn chúng," Tuấn trỏ chuột vào góc dưới tấm da dê, nơi có đồ án bảy ngôi sao Bắc Đẩu thẳng hàng với trăng tròn và ký hiệu triều cường cực đại. "Chu kỳ Thất Tinh Quy Vị trùng khớp chính xác với đợt triều cường rằm tháng Chín âm lịch... Tức là chỉ còn đúng sáu ngày nữa tính từ hôm nay!"

Sáu ngày.

Khoảng thời gian ngắn ngủi tựa cái chớp mắt. Trong sáu ngày đó, Cửu Long Thiên Hải với con tàu siêu trọng *Thiên Hải 09* và đội ngũ người nhái tinh nhuệ sẽ dùng thiết bị cơ giới biển sâu tấn công vào phong ấn rãnh nứt Cần Giờ. Nếu phong ấn bị xé toạc, nước biển dâng cao kết hợp tà khí viễn cổ sẽ nhấn chìm toàn bộ đồng bằng Nam Bộ trong biển bùn đen độc hại.

Muốn ngăn chặn thảm họa đó, tôi không thể chỉ đứng trên bờ quan sát dữ liệu. Tôi phải đích thân lặn xuống vực thẳm biển sâu, đối diện với áp lực ngàn cân của biển cả và nanh vuốt kẻ thù.

Nhưng thân thể phàm nhân, dù đã luyện đến Luyện Cốt trung kỳ đỉnh phong, liệu có thể chống chọi nổi áp suất một trăm hai mươi át-mốt-phe dưới đáy đại dương đen kịt?

Trong thâm tâm tôi, câu hỏi lớn tựa tảng đá ngàn cân đè nặng lên từng nhịp thở.'''

ACT3 = '''Một giờ ba mươi phút sáng ngày hai mươi ba tháng Mười.

Tôi bước vào gian phòng tĩnh tọa cách âm nằm ở góc sâu nhất tầng hầm B2. Cánh cửa thép dày mười lăm phân khép lại, ngăn cách hoàn toàn mọi âm thanh cơ giới và tín hiệu vô tuyến bên ngoài. Không gian chìm vào tĩnh mịch tuyệt đối, chỉ còn lại tiếng hít thở trầm lắng và tiếng máu chảy róc rách trong huyết quản tôi.

Tôi ngồi xếp bằng trên tấm đệm cói, đặt thanh Hắc Thiết Đoản Côn nằm ngang trên hai đầu gối, thanh Trấn Thủy Đoản Đao gác bên cạnh.

Nhắm mắt lại, ý niệm của tôi chìm sâu vào thức hải.

Bên trong không gian tinh thần bao la, đóa sen ngọc bích tỏa ánh hào quang hoàng kim ấm áp — nguồn năng lượng đất trời thuần khiết tôi hấp thu từ cọc đồng Thủy Môn Chấn Tiêu tại đáy giếng Ba Son.

Lâm Tịch ngồi tĩnh tọa nơi tâm đài sen, tà áo lụa trắng khẽ lay động. Sắc mặt nàng bớt đi vài phần nhợt nhạt, dung nhan thanh tú tuyệt trần toát lên vẻ trang nghiêm. Đôi mắt phượng trong veo khẽ mở ra, nhìn thẳng vào tâm thức tôi:

*"Minh An, sáu cọc tiêu tiền tuyến đã an định, nanh rồng phương Nam đã được tháo bỏ xiềng xích. Ngươi làm rất tốt. Nhưng hải đồ mai rùa đã chỉ rõ, cửa ải Cực Tù Hải Uyên ngoài khơi Cần Giờ mới là thử thách sinh tử thật sự của ngươi trên con đường Thể Đạo."*

"Ta hiểu, thưa nàng," tôi khẽ đáp lời. "Dưới độ sâu một ngàn hai trăm mét, áp lực nước khổng lồ gấp ba mươi lần giếng Ba Son. Dù khung xương của ta đã cứng tựa kim thạch nhờ Ngọc Tủy Quy Nhất, nhưng lục phủ ngũ tạng và mạch máu phàm nhân vẫn không thể chịu nổi sức ép khủng khiếp ấy."

Lâm Tịch khẽ gật đầu, giọng thanh lãnh tựa tiếng chuông ngân:

*"Đúng vậy. Khung xương chỉ là giàn giáo nâng đỡ cơ thể. Dòng máu mới là cội nguồn sinh mệnh, là chiếc cầu nối luân chuyển dưỡng khí đến từng thớ thịt. Nếu máu của ngươi vẫn chỉ là phàm huyết loãng yếu, áp suất biển sâu sẽ lập tức ép vỡ mao mạch, làm đông máu trong lồng ngực chỉ trong chớp mắt. Muốn đạp sóng ngàn trượng, bước chân xuống vực thẳm đại dương, ngươi buộc phải đột phá Thức thứ tám của Đoán Cốt Thập Nhị Thức — Hoán Huyết Hóa Cương!"*

"Hoán Huyết Hóa Cương..." Tôi lặp lại bốn chữ ấy, lồng ngực dâng lên luồng nhiệt khí cuộn trào.

*"Hoán Huyết, chính là mượn ngọc tủy làm lò luyện, mượn kiếm khí hàn băng của Thanh Long làm búa nện, tôi luyện từng giọt phàm huyết thành Cương Huyết!"* Lâm Tịch cất giọng đanh gọn, từng lời khắc sâu vào tâm trí tôi. *"Cương Huyết cô đọng tựa đồng thau lỏng, nặng gấp ba lần máu thường, giữ dưỡng khí vượt trội gấp mười lần. Khi Cương Huyết vận hành, nó tạo ra áp lực thủy tĩnh nội sinh đối kháng hoàn hảo với áp suất ngoại giới, giúp ngươi tự do hô hấp và vận kình dưới đáy biển sâu ngàn trượng!"*

"Xin nàng chỉ dẫn phương pháp vận chuyển!" Tôi kiên định đáp.

*"Hãy dẫn dắt giọt ngọc tủy hoàng kim nơi đốt sống thứ ba mươi ba tan chảy, rót thẳng vào tâm thất trái! Hãy chuẩn bị tinh thần, quá trình thay máu đau đớn tựa như lấy nước sôi rưới vào tủy xương, một khi bắt đầu thì không thể dừng lại!"*

Tôi hít sâu một hơi, nhắm nghiền hai mắt, tâm trí quy về một mối.

"Bắt đầu!"

Kình lực Thể Đạo trong cơ thể tôi gầm thét cuộn trào. Dọc ba mươi ba đốt xương sống, dòng tủy ngọc lấp lánh bừng sáng. Tại đốt sống cuối cùng, giọt ngọc tủy vàng óng ánh ngưng tụ sau trận chiến Ba Son bắt đầu phát nổ.

"Oanh!"

Cơn đau đớn kịch liệt tựa ngàn mũi kim nung đỏ đâm xuyên qua tủy sống bùng phát. Tôi cắn chặt răng đến bật máu tươi nơi khóe môi, toàn thân run rẩy trên tấm đệm cói. Nhưng ý chí sắt đá của người tu luyện Thể Đạo không cho phép tôi lùi bước.

Giọt tủy ngọc hoàng kim hòa tan, chảy tràn vào buồng tim.

Ngay khoảnh khắc ấy, kiếm khí hàn băng của *Thanh Long Lân Kiếm* nơi đốt sống ngực thứ bảy đồng thời phóng thích từng đợt sương lạnh phỉ thúy, bao bọc lấy tim mạch ngăn nhiệt lượng cực hạn thiêu rụi phàm thể.

Âm dương giao hòa, băng hỏa đồng quy!

Trái tim tôi đập dồn dập tựa trống trận: "Thình... thình... thình!" Mỗi nhịp đập là một lần ngọn lửa kình khí thiêu đốt tạp chất trong dòng máu. Tế bào máu cũ kỹ bị nghiền nát, thay thế bằng những hạt tinh thể huyết dịch đỏ ánh vàng óng ánh, đặc quánh tựa dung nham kim loại.

Từ trái tim, dòng máu mới — Cương Huyết — cuồn cuộn chảy qua động mạch chủ, tỏa đi khắp cơ thể. Đi đến đâu, các mạch máu lại phát ra tiếng rên siết trầm đục, thành mạch dày lên gấp đôi, dẻo dai và co giãn tựa những sợi cáp cao su bọc thép.

Cơn đau đớn dần nhường chỗ cho cảm giác khoan khoái, no đủ chưa từng có.

Toàn bộ ba mươi ba đốt xương sống phát ra tiếng rền vang giòn tan như ngọc vỡ. Lớp màng bảo vệ xương cốt dày thêm một tấc, óng ánh sắc phỉ thúy và hoàng kim. Khí tức trong cơ thể tôi liên tục thăng hoa, phá vỡ bức tường bình cảnh vô hình.

Luyện Cốt Hậu kỳ!

Tôi đã chính thức bước trọn vẹn cả hai chân vào cảnh giới Luyện Cốt Hậu kỳ, hoàn thành mỹ mãn Thức thứ tám — Hoán Huyết Hóa Cương!'''

ACT4 = '''Năm giờ ba mươi phút sáng ngày hai mươi ba tháng Mười.

Tôi từ từ mở mắt ra.

Tia sáng màu đồng thau lướt qua con ngươi đen lánh rồi thu liễm vào sâu đáy mắt. Hơi thở tôi ấm áp, tinh khiết, mang theo hương thơm thanh nhã của ngọc tủy.

Tôi cúi nhìn đôi bàn tay mình. Làn da ngăm đen rắn rỏi nay ẩn hiện lớp ánh kim mờ nhạt dưới ánh đèn. Dưới cổ tay, các mạch máu lớn đập chậm rãi: Chỉ ba mươi hai nhịp trong một phút. Mỗi nhịp đập vững chãi tựa tiếng búa nện xuống đe thép, bơm dòng Cương Huyết cuồn cuộn sức mạnh đi khắp châu thân.

Tôi đứng dậy, bước từng bước khoan thai ra khỏi phòng tĩnh tọa. Cánh cửa thép mở ra, tiếng bước chân nhẹ tựa lông hồng nhưng mỗi lần chạm đất, mặt sàn lại phát ra tiếng cộng hưởng trầm đục vững vàng.

Bên ngoài bàn làm việc, Tuấn và Viện trưởng Nam vẫn thức trắng theo dõi dữ liệu trinh sát. Nghe tiếng động, cả hai đồng loạt quay đầu lại.

Chiếc bút bi trên tay Tuấn rơi "tách" xuống bàn. Anh mở to hai mắt, nhìn tôi ngỡ ngàng:

"Minh An... Em... Em vừa trải qua chuyện gì vậy? Khí tức quanh người em... sao lại vững chãi đến mức này?"

Viện trưởng Nam cũng sững sờ. Là chuyên gia đầu ngành địa chất từng tiếp xúc nhiều năng lượng địa tầng, ông nhận ra ngay sự biến chuyển bản chất toát ra từ từng thớ thịt của tôi. Mắt ông sáng rực tia hy vọng:

"Đột phá rồi sao, Minh An?"

"Báo cáo Viện trưởng," tôi đứng thẳng người, giọng nói trầm ấm có sức xuyên thấu lạ thường. "Giám Đốc Kỹ Thuật Dữ Liệu Nguyễn Minh An đã củng cố xong thể trạng. Thể chất của tôi hiện tại đã hoàn toàn thích ứng với môi trường áp suất cực hạn của đáy biển sâu. Tôi đã sẵn sàng cho nhiệm vụ Cần Giờ."

Viện trưởng Nam bước tới, nắm chặt cánh tay tôi. Cảm nhận được sự vững chãi tựa thép nguội toát ra từ tôi, ông khẽ run lên vì xúc động:

"Tốt! Quá tốt! Đây là mệnh lệnh công tác đặc biệt vừa được phê duyệt lúc bốn giờ sáng từ cấp trên."

Ông trao cho tôi tập hồ sơ có dấu mộc đỏ tươi:

"Viện ta phối hợp cùng Bộ Tư lệnh Vùng 2 Hải quân thành lập Tổ Khảo sát Thủy văn Địa tầng Biển sâu. Tàu tuần tra cao tốc chuyên dụng Hải quân số hiệu HQ-268 đã neo sẵn tại Cát Lái, sẵn sàng đưa tổ công tác tiến thẳng về vùng biển Cần Giờ. Cậu Tuấn phụ trách trạm điều khiển sonar và viễn thám, còn cậu An sẽ là mũi nhọn trực tiếp thâm nhập thực địa."

"Rõ!" Tôi và Tuấn đồng thanh đáp, giọng dõng dạc kiên định.

Sáu giờ mười lăm phút sáng.

Tôi bước lên sân thượng tầng mười hai của Viện Địa tầng Đô thị.

Gió sớm từ sông Sài Gòn ùa tới lồng lộng, thổi bay làn tóc mai. Bầu trời phương Đông ửng lên những vệt rạng đông cam vàng rực rỡ xua tan màn đêm. Phía bên kia sông, những tòa cao ốc vươn mình kiêu hãnh trong nắng sớm. Dưới chân cầu, dòng người bắt đầu đổ ra đường hối hả mưu sinh, tiếng còi xe rộn rã đón chào ngày mới bình yên.

Tôi đứng tựa lan can thép, hít căng lồng ngực bầu không khí trong lành. Bên hông, thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao nằm trong bao da, phát ra tiếng ngân nga khe khẽ hòa cùng nhịp đập Cương Huyết.

Trong thức hải, Lâm Tịch xuất hiện bên cạnh tôi, tà áo trắng bay bay theo làn gió tinh thần. Nàng nhìn về phía Đông Nam xa xôi — nơi dòng sông Sài Gòn hòa vào biển mẹ mênh mông:

*"Minh An, đại dương bao la, sóng gió ngập trời. Cực Tù Lục Trọng Giới tầng thứ sáu đã ngủ yên hai triệu rưỡi năm, nay sắp đến ngày thức giấc. Ngươi đã chuẩn bị xong chưa?"*

Tôi nhìn về phía chân trời xa xăm nơi cửa biển Cần Giờ mờ ảo trong sương sớm, khóe môi khẽ nhếch lên nụ cười điềm đạm nhưng ngập tràn hào khí:

"Sóng to gió lớn càng hay. Đôi chân này của tôi sinh ra là để đạp bằng mọi phong ba."'''

def run_pipeline():
    print(f"=== BẮT ĐẦU CHU TRÌNH SÁNG TÁC & KIỂM TOÁN CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    
    # 1. Ghép nối bản thảo
    raw_content = f"{ACT1}\n\n{ACT2}\n\n{ACT3}\n\n{ACT4}"
    word_count = len(raw_content.split())
    print(f"[+] [1/5] Soạn thảo hoàn tất: {word_count:,} từ (Mục tiêu: 3.300 - 3.650 từ).")
    if word_count < 3300 or word_count > 3650:
        print(f"[-] Cảnh báo: Độ dài từ {word_count} chưa nằm trong khoảng tối ưu 3.300 - 3.650 từ!")
        return False

    # 2. Kiểm tra cấm chữ "hồi" và meta-words theo RULE-07
    forbidden_words = [
        "chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện",
        "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"
    ]
    
    found_violations = []
    
    # Quét chữ "hồi" dưới mọi hình thức
    hoi_matches = re.findall(r'\b\w*hồi\w*\b', raw_content, re.IGNORECASE)
    if hoi_matches:
        found_violations.append(f"Chứa biến thể chữ 'hồi': {set(hoi_matches)}")

    # Quét các meta-words khác
    for fw in forbidden_words:
        if fw == "hồi":
            continue
        m = re.findall(rf'\b{fw}\b', raw_content, re.IGNORECASE)
        if m:
            found_violations.append(f"Chứa meta-word '{fw}': {len(m)} lần")

    if found_violations:
        print(f"[-] [LỖI RULE-07] Phát hiện vi phạm từ cấm:")
        for v in found_violations:
            print(f"    * {v}")
        return False
    print(f"[+] [2/5] RULE-07 đạt chuẩn tuyệt đối: 0 meta-words, 0 chữ 'hồi'.")

    # 3. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_tuan", "char_lam_tich", "char_trinh_hoai_nam"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [3/5] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 4. Xuất bản Markdown với YAML Frontmatter và Heading H1
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

    # 5. Xuất bản Word (.docx)
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

    # 6. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 6.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Lục Trụ Quy Nguyên & Đột Phá Hoán Huyết Hóa Cương",
        CHAPTER_NUM,
        1,
        f"{DATE}T06:00:00+07:00",
        CHAPTER_NUM,
        "loc_vien_dia_tang_b2",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"]),
        "Trở về phòng thí nghiệm ngầm B2 sau sự kiện Ba Son, Minh An và Tuấn ghi nhận 6 cọc tiêu tiền tuyến đồng loạt cộng hưởng tần số 0.12 Hz hình thành Lục Giác Trấn Thủy Đồ. Viện trưởng Nam cung cấp tin tình báo về tàu khảo sát Thiên Hải 09 của Cửu Long Thiên Hải ngoài khơi Cần Giờ. Phân tích hải đồ mai rùa và bản đồ da dê phát hiện đại phong ấn Cực Tù Hải Uyên sâu hơn 1200m ngoài khơi Vịnh Gành Rái sắp mở vào rằm tháng Chín. Lâm Tịch truyền thụ Thức thứ tám Hoán Huyết Hóa Cương. Minh An tôi luyện dòng máu thành Cương Huyết chịu áp lực biển sâu, chính thức đột phá Luyện Cốt Hậu kỳ và nhận lệnh thành lập Tổ Khảo sát Biển sâu xuất quân.",
        "Minh An đột phá Luyện Cốt Hậu kỳ, nắm vững Hoán Huyết Hóa Cương; giải mã thành công hải đồ Cần Giờ; thành lập Tổ Khảo sát Thủy văn Địa tầng Biển sâu phối hợp Tàu tuần tra Hải quân HQ-268 chuẩn bị xuất kích."
    ))

    # 6.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        status = 'RESOLVED',
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-003'
    """, (
        CHAPTER_NUM,
        "Minh An chính thức mở khóa và luyện thành Thức thứ tám Hoán Huyết Hóa Cương, biến phàm huyết thành Cương Huyết thích ứng biển sâu ngàn mét, đột phá Luyện Cốt Hậu kỳ."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An đạt cảnh giới Luyện Cốt Hậu kỳ sau khi luyện thành Hoán Huyết Hóa Cương, thể chất kim thạch và mạch máu dẻo dai chịu áp suất 120 atm."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 7. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T06:30:00+07:00"
        inv_data["current_location"] = "Phòng thí nghiệm ngầm B2 Viện Địa tầng Đô thị (Quận 1, TP.HCM)"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ (Hoán Huyết Hóa Cương)"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json.")

    # 8. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> HOÀN TẤT TOÀN BỘ PIPELINE CHƯƠNG {CHAPTER_NUM} THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

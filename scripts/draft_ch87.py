# -*- coding: utf-8 -*-
"""Draft Chapter 87 for Phá Trời Novel OS with ~3,500+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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
from system.engines.emotion_dopamine_engine import EmotionDopamineEngine

CHAPTER_NUM = 87
CHAPTER_TITLE = "Huyết Chiến Thanh Đa"
DATE = "2026-10-29"
LOCATION = "Viện Khảo Sát Địa Chất & Bán Đảo Thanh Đa, Sông Sài Gòn"

ACT1 = '''Ba giờ ba mươi phút chiều ngày hai mươi chín tháng mười.

Bầu trời Sài Gòn sau buổi trưa oi nồng bỗng chốc sẫm màu lại bởi những dải mây giông xám xịt từ phía rừng ngập mặn Cần Giờ cuồn cuộn kéo về. Gió bắt đầu thốc mạnh qua những ngọn xà cừ cổ thụ dọc đường Hoàng Hoa Thám thuộc quận Bình Thạnh, cuốn theo từng đám lá khô xoay tít trên mặt đường nhựa.

Sau khi nghiền nát chiếc bộ đàm mã hóa của toán lính bắn tỉa tại bờ kè Thanh Đa, tôi biết thời gian của mình chỉ còn tính bằng từng phút.

Tạ Lôi — kẻ đứng đầu bộ phận tác chiến đặc biệt của Tập đoàn Cửu Long Thiên Hải tại thành phố Hồ Chí Minh — trong cơn hoảng loạn và điên cuồng khi biết bốn tay súng tinh nhuệ bị vô hiệu hóa, đã lập tức hạ lệnh cho toán đột nhập số 3 tiến đánh Viện Khảo sát Địa chất Nam Bộ. Mục tiêu của chúng không chỉ là cướp đoạt toàn bộ các mẫu lõi khoáng vật bazan độc bản mà tôi đã dày công thu thập suốt những tháng ngày bôn ba nơi duyên hải, mà còn muốn biến nơi đây thành một biển máu để uy hiếp tinh thần tôi.

Tại Viện Địa chất ấy, có Giáo sư già Trần Văn Định — người thầy đã từng kiên nhẫn cầm tay chỉ cho tôi từng thớ đá phiến, từng lớp đứt gãy kiến tạo thuở tôi còn là một cậu sinh viên nghèo ngơ ngác bước chân vào ngành địa chất.

Tôi không cho phép bất kỳ kẻ nào vấy bẩn lên mái trường và những người thầy đáng kính ấy!

Không bắt xe ôm hay bất kỳ phương tiện giao thông nào, tôi chọn cách di chuyển thuần túy bằng thể lực của một võ giả Thể Đạo đã bước vào **Hoán Huyết Sơ kỳ**.

Thân hình tôi lướt đi thoăn thoắt trong những con hẻm ngoằn ngoèo chằng chịt của khu dân cư Bình Thạnh. Với tốc độ hơn bốn mươi cây số một giờ nhưng từng bước chân chạm đất của tôi lại êm ái tựa như một chiếc bóng. Dòng Thuần Dương Cương Huyết ánh kim cuộn chảy nhịp nhàng qua từng bó cơ bắp săn chắc, giúp nhịp tim của tôi duy trì ở mức ổn định tuyệt đối mà không hề phát ra một tiếng thở dốc.

Mười lăm phút sau, tôi đã áp sát bờ tường rào rêu phong phía sau khuôn viên Viện Khảo sát Địa chất.

Tòa nhà ba tầng quét vôi vàng cổ kính xây dựng từ thời Pháp nằm tĩnh lặng dưới những tán cây bàng rợp bóng. Chiều muộn, phần lớn cán bộ và nhân viên nghiên cứu đã tan sở về nhà, chỉ còn lại vài ô cửa sổ trên tầng hai vẫn sáng đèn.

Khứu giác và thính giác siêu phàm của Hoán Huyết kỳ lập tức phát huy tác dụng tối đa.

Tôi ngửi thấy mùi dầu máy bôi trơn chuyên dụng của kìm cộng lực thủy lực, mùi nhựa cháy khét lẹt của thiết bị phá khóa điện tử và nhịp thở dồn dập của năm kẻ lạ mặt đang lén lút tiếp cận cầu thang thoát hiểm phía sau dãy nhà thí nghiệm.

Chúng gồm năm tên, đều mặc đồng phục công nhân viễn thông màu xanh đậm, đeo ba-lô kỹ thuật nhưng bên hông lại giấu súng ngắn giảm thanh và bình xịt hơi cay nén áp suất cao.

"Toán đột nhập số 3," tôi thầm nhủ, ánh mắt lóe lên một tia sát khí lạnh buốt.

Tôi khẽ nhún chân, thân hình như một cánh én lướt qua hàng rào dây thép gai cao hơn ba mét mà không làm rung rinh dù chỉ một chiếc lá bàng.

Tại hành lang tầng hai, cánh cửa gỗ dẫn vào phòng lưu trữ mẫu lõi địa chất độc bản đã bị phá vỡ niêm phong. Bên trong phòng làm việc liền kề, Giáo sư Trần Văn Định tuổi ngoài sáu mươi với mái tóc bạc phơ đang ngồi bất động trên chiếc ghế xoay, gương mặt nhợt nhạt vì hoảng sợ khi bị một gã tà tu lực lưỡng kề mũi dao bấm sắc lạnh ngay sát động mạch cổ.

"Lão già, mật mã mở két sắt lưu trữ mẫu đá khoan Cực Tù ở đâu? Đọc nhanh không tao rạch nát cổ họng!" tên tà tu gằn giọng đe dọa bằng một thanh âm khàn đục nồng nặc mùi thuốc lá rẻ tiền.

Bốn tên còn lại đang dùng kìm thủy lực phá chốt chiếc tủ thép bảo mật đựng các ống mẫu địa tầng ngầm mà tôi đã gửi về từ vịnh Gành Rái và cồn Trấn Ba.

Dù đôi bàn tay gầy gò run rẩy vì sức ép tàn nhẫn, Giáo sư Định vẫn cắn chặt môi, ánh mắt kiên định ngước nhìn tên cướp:

"Đó là tài sản khoa học quốc gia... là công sức mồ hôi của các thế hệ nghiên cứu... Các người... đừng hòng lấy được..."

"Mày muốn chết!" Tên tà tu trừng mắt hung hãn, lưỡi dao bấm khẽ ấn sâu vào da thịt, rỉ ra một vệt máu tươi.

Ngay trong tích tắc sinh tử ngàn cân treo sợi tóc ấy, một luồng kình phong buốt giá bỗng nhiên thổi thốc qua khung cửa sổ đang mở toang.

*XOẸT!*

Tôi không dùng vũ khí. Giữa một căn phòng thí nghiệm đầy ắp những dụng cụ đo đạc thủy tinh tinh xảo và tài liệu giấy tờ quý giá, một đòn chấn động quá mức có thể hủy hoại toàn bộ công trình nghiên cứu của người thầy già.

Áp dụng tuyệt kỹ **Cương Khí Ly Thể**, ngón tay trỏ của tôi búng mạnh vào thinh không!

Một viên kình lực vô hình xé gió bắn thẳng vào khớp cổ tay của gã đang cầm dao.

*RẮC!*

Xương cổ tay của tên tà tu lập tức trật khớp, gãy gập sang một bên. Con dao bấm văng ra khỏi tay hắn, cắm phập xuống sàn gỗ mà không kịp chạm sâu thêm một mi-li-mét nào vào cổ vị giáo sư.

Trước khi tên tà tu kịp há mồm rú lên vì đau đớn, thân ảnh của tôi đã lướt tới như một tia chớp. Lòng bàn tay tôi áp nhẹ lên ngực hắn, một luồng Kính Kình thuần thục đánh thẳng vào hạch thần kinh tim khiến hắn nghẹt thở ngất lịm, ngã gục xuống sàn mà không phát ra bất kỳ tiếng động lớn nào.

Bốn tên còn lại giật mình quay phắt lại, tay vội vàng thò vào vạt áo rút súng ngắn giảm thanh.

Nhưng tốc độ của phàm nhân cầm súng trước mặt một võ giả Hoán Huyết Sơ kỳ chẳng khác nào những chuyển động chậm chạp của loài rùa.

*VÚT! VÚT! VÚT!*

Thanh **Hắc Thiết Đoản Côn** bát giác vung lên giữa không trung, vẽ nên ba đường tròn hoàn mỹ màu đen nhánh pha vệt chu sa đỏ rực. Kình lực trên thân côn không đập vỡ xương thịt của chúng, mà chuẩn xác gõ thẳng vào ba khẩu súng ngắn, làm gãy đôi cụm cò súng và vặn xoắn nòng kim loại thành những khối sắt vụn méo mó.

Chỉ trong vòng chưa đầy ba giây, ba cú điểm côn tiếp theo giáng thẳng vào các huyệt đạo yếu hại trên bả vai và gáy của ba tên tà tu, khiến chúng ngã lăn ra sàn bất tỉnh nhân sự.

Tên cuối cùng — kẻ cầm đầu toán đột nhập — kinh hãi lùi giật lùi về phía góc tường, run rẩy móc ra một quả lựu đạn gây choáng định giật chốt tự sát.

Tôi bước tới một bước, chân phải khẽ hất nhẹ chiếc ghế gỗ. Chiếc ghế trượt trên mặt sàn với tốc độ kinh người, tông thẳng vào ngực hắn, ép chặt hắn vào bức tường bê tông. Bàn tay tôi vươn ra tước lấy quả lựu đạn, đồng thời bẻ gãy khớp ngón tay của hắn trong sự lạnh lùng tuyệt đối.

Căn phòng lưu trữ mẫu đá hoàn toàn trở lại vẻ tĩnh lặng.

Giáo sư Trần Văn Định ôm lấy lồng ngực thở dốc, đôi mắt mờ đục nhìn bóng người thanh niên mặc chiếc áo dã chiến bạc màu đứng trước mặt mình. Phải mất một lúc lâu, thầy mới nhận ra gương mặt quen thuộc từng gắn bó suốt bốn năm đại học:

"Minh An... Là em thật sao Minh An? Em... em làm sao làm được những chuyện này..."

Tôi cúi người đỡ người thầy già ngồi lại ngay ngắn trên ghế, rút chiếc khăn tay sạch nhẹ nhàng lau đi vệt máu nơi cổ thầy:

"Thầy bình tĩnh lại, mọi chuyện đã an toàn rồi ạ. Bọn chúng là tay sai của một thế lực ngầm muốn phá hoại các nghiên cứu địa chất của nước ta. Em vừa đi khảo sát thực địa ở miền Tây về kịp lúc."

Tôi lấy chiếc điện thoại tác chiến thu giữ từ toán lính, bấm gửi tin nhắn khẩn cấp kèm theo định vị tọa độ và danh sách bắt giữ năm tên tà tu cho số máy bảo mật của lực lượng an ninh đặc nhiệm thuộc Bộ Chỉ huy Biên phòng — kênh liên lạc mà Đại úy Phan Thế Dũng đã bàn giao cho tôi tại Cà Mau. Với bằng chứng quả tang này, toàn bộ toán đột nhập sẽ bị cơ quan chức năng tiếp quản trong vòng mười lăm phút tới.

"Thầy ở yên đây, lực lượng bảo vệ đặc nhiệm sẽ đến tiếp quản ngay bây giờ," tôi nắm lấy đôi bàn tay gầy gò của thầy, trầm giọng dặn dò. "Các mẫu lõi đá này em xin phép mang theo chiếc ống số 9 — mẫu đá bazan ngầm của thềm lục địa Sài Gòn. Đêm nay, em phải dùng nó để hoàn tất nhiệm vụ cuối cùng."

Giáo sư Định nhìn sâu vào mắt tôi, dường như cảm nhận được gánh nặng thiêng liêng đè nặng trên vai người học trò cũ:

"Minh An... Thầy không biết em đang gánh vác điều gì to lớn, nhưng hãy nhớ: đất đá của quê hương này chứa đựng linh hồn của tổ tiên hàng triệu năm. Hãy giữ gìn nó bình yên, em nhé!"

"Em nhớ rồi, thưa thầy!"

Tôi cúi đầu chào thầy một lần cuối rồi ôm chiếc ống mẫu địa tầng số 9 nhảy qua khung cửa sổ, hòa mình vào màn mưa giông bắt đầu trút xuống trắng xóa thành phố.'''

ACT2 = '''Bảy giờ ba mươi phút tối.

Trận mưa giông nhiệt đới cuối mùa trút nước xối xả xuống lưu vực sông Sài Gòn, tạo nên một tấm màn nước mù mịt che khuất toàn bộ tầm nhìn đô thị.

Những tia sét xé toạc bầu trời đêm đen đặc, rọi sáng khúc uốn móng ngựa quanh co của bán đảo Thanh Đa. Bên kia bờ Thảo Điền, những tòa cao ốc chọc trời hoa lệ nhấp nháy ánh đèn led mờ ảo qua làn mưa dầy đặc. Mặt sông Sài Gòn bình thường phẳng lặng nay cuộn sóng hung hãn, từng đợt sóng đục ngầu phù sa đập ầm ầm vào bờ kè bê tông nứt nẻ.

Giữa khúc sông rộng hơn ba trăm mét ấy, bốn chiếc sà lan hút cát khổng lồ mang số hiệu vận tải ngụy trang của Cửu Long Thiên Hải đang thả neo cố định thành một trận địa hình tứ giác hoàn hảo.

Tiếng động cơ diesel hạng nặng của bốn chiếc sà lan nổ rền vang, át cả tiếng sấm chớp trên trời cao.

Nhưng sâu bên dưới khoang máy của chúng, những cột khói màu tím đen mang theo mùi hôi thối nồng nặc của bùn đáy vực sâu đang không ngừng bốc lên ngùn ngụt. Bốn cụm máy phát xung điện từ tần số cực thấp kết hợp với những khối trận bàn huyết thạch tà thuật đang phóng thích hàng vạn xung chấn năng lượng tiêu cực thẳng xuống đáy sông.

Dưới độ sâu âm ba mươi mét, lớp bùn sét cổ xưa đang bị xé toạc từng mảng lớn. Chín sợi xích huyền thiết khổng lồ neo giữ ngọn **Cổ Tháp Thần Hoang** đang rung lắc dữ dội, bốn mắt xích ở hướng đông nam đã bị tà khí ăn mòn đến mức xuất hiện những vết rạn nứt li ti!

"Minh An, không thể chần chừ thêm nữa," thanh âm của Lâm Tịch vang lên từ thức hải, mang theo sự cảnh báo đanh thép. "Bốn sà lan này đang tạo thành trận thế Tứ Hung Đoạt Mạch. Nếu không phá hủy các cụm máy phát xung trong vòng ba mươi phút, mắt xích số bốn sẽ gãy gập, giải phóng toàn bộ năng lượng nén của đáy sông!"

Tôi đứng trên mỏm đất hoang ngập cỏ dại sát mép nước, cởi chiếc áo khoác dã chiến để lộ lồng ngực trần cuồn cuộn gân cốt.

Dưới làn mưa lạnh buốt quất rát mặt, ba mươi ba đốt sống tủy ngọc sau lưng tôi bừng sáng rực rỡ, tỏa ra một vầng hào quang ấm áp mang sắc vàng kim pha ánh lam ngọc thấu suốt qua làn da. Dòng Thuần Dương Cương Huyết bừng cháy như dung nham trong huyết quản, đẩy nhiệt độ cơ thể tôi lên mức tối ưu, biến nước mưa rơi xuống da thịt thành từng làn hơi nước trắng mỏng bốc lên nghi ngút.

Bên hông trái, thanh **Trấn Thủy Đoản Đao** bằng đồng rỉ xanh lam đang khẽ rung lên những nhịp reo vui khi ngửi thấy mùi sóng nước địa mạch. Tay phải tôi nắm chặt **Hắc Thiết Đoản Côn** bát giác.

Tôi hít sâu một hơi, vận chuyển khẩu quyết **Quy Tức Cùng Cực** rồi phóng mình lao thẳng xuống dòng sông Sài Gòn đang cuộn sóng dữ!

*TỎM!*

Mặt nước rẽ ra làm hai, nuốt trọn bóng hình tôi vào lòng sông sâu thẳm.

Dưới làn nước phù sa đen ngòm chảy xiết, tầm nhìn của một người bình thường gần như bằng không. Nhưng với năng lực Tâm Nhãn của Hoán Huyết Sơ kỳ, thế giới dưới đáy sông hiện ra trước mắt tôi rõ ràng đến từng chi tiết vi mô.

Tôi thấy rõ những sợi cáp thép ngầm to bằng bắp đùi nối từ đáy bốn chiếc sà lan cắm sâu xuống lòng bùn sét. Tôi thấy rõ từng luồng xung chấn điện từ màu tím đen đang cuồn cuộn phóng xuống ngọn cổ tháp chín tầng mờ ảo dưới đáy vực.

Như một con kình ngư Thuần Dương xé nước bơi ngược dòng, tôi áp sát vào đáy chiếc sà lan số 1 ở mạn tây nam.

Tôi trồi lên khỏi mặt nước ngay cạnh bục neo xích sau lái của sà lan số 1, hai bàn tay bám chặt vào mép vỏ thép rỉ sét rồi đu mình nhảy vọt lên boong tàu.

Trên boong sà lan trơn trượt đầy bùn đất, sáu tên tà tu mặc áo mưa đen đang vận hành cụm máy phát xung điện từ. Nhìn thấy một thanh niên lưng trần phát sáng bỗng nhiên từ dưới đáy sông nhảy vọt lên, chúng kinh hãi rú lên những tiếng kêu thất thanh:

"Kẻ xâm nhập! Là thằng ranh Nguyễn Minh An!"

"Bắn chết nó!"

Chúng rút dao găm và dùi cui điện xông tới điên cuồng.

Nhưng câu trả lời của tôi chỉ là một đường côn quét ngang đầy uy lực!

*OÀNG!*

Thanh Hắc Thiết Đoản Côn phát ra một luồng **Kính Kình** chấn động cực hạn. Không khí ẩm ướt trên boong tàu bỗng chốc bị nén lại thành một vòng sóng xung kích hình bán nguyệt, hất tung toàn bộ sáu tên tà tu văng ra xa hơn mười mét, rơi tõm xuống dòng sông chảy xiết!

Không dừng lại một phần mười giây, tôi xoay người tung một cú đập thẳng từ trên cao xuống:

*RẦM!*

Đoản côn nện chuẩn xác vào lõi khối đá huyết thạch đang phát sáng tím đen trên bệ máy. Kình lực Thuần Dương bộc phát nghiền nát khối huyết thạch thành hàng ngàn mảnh vụn nhỏ, đồng thời làm nổ tung toàn bộ bảng mạch điện tử của cụm máy phát xung trên chiếc sà lan thứ nhất.

Ngọn lửa điện xẹt ra le lói rồi tắt ngấm trong làn mưa tầm tã. Luồng hắc khí đầu tiên nối xuống đáy sông lập tức đứt đoạn!

Tôi nhảy vọt qua khoảng không gian mười mét giữa hai con tàu, tiếp đất hoàn hảo trên mũi chiếc sà lan số 2.

Tại đây, chúng đã có sự phòng bị.

Một gã đàn ông lực lưỡng với khuôn mặt chằng chịt những vết sẹo rết bò — một trong hai đại hộ pháp tà đạo của Cửu Long Thiên Hải — đang đứng chờ sẵn. Hai bàn tay gã gắn đôi móng vuốt thép năm ngón dài nửa thước, sắc lẹm và tẩm chất độc Huyết Thiềm màu xanh lục bốc khói cay nồng.

"Nguyễn Minh An! Mày dám phá hỏng đại sự của Tạ tổng quản, nộp mạng đi!"

Gã hộ pháp gầm lên như một con thú dữ, thân hình to lớn lao vút qua màn mưa, đôi Huyết Trảo xé gió bổ thẳng vào ngực tôi với tốc độ kinh hồn, mang theo luồng âm phong tanh tưởi!

Trong thời khắc ấy, tôi không lùi lại nửa bước.

Tay trái tôi rút thanh **Trấn Thủy Đoản Đao** ra khỏi vỏ bọc da bò.

*KENG!*

Một tiếng va chạm kim loại đanh thép vang lên chấn động màng nhĩ!

Lưỡi đao thanh đồng rỉ lam ngọc của Trấn Thủy Đoản Đao bừng sáng những đường chỉ vàng kim rực rỡ. Khi chất độc Huyết Thiềm chạm vào thân đao thanh đồng cổ xưa, nó lập tức bị địa khí Thuần Dương thiêu rụi thành một làn khói trắng vô hại.

Kình lực từ Đoán Cốt Thập Nhị Thức của tôi truyền thẳng qua cán đao, bẻ gãy ngọt xớt năm chiếc móng vuốt thép của gã hộ pháp!

Gã hộ pháp trố mắt kinh hoàng khi nhìn thấy đôi vuốt thép gia truyền bị chém đứt như cọng rạ. Nhưng hắn chưa kịp lùi lại thì cán Hắc Thiết Đoản Côn trên tay phải của tôi đã thúc thẳng vào hõm ngực hắn.

*HỰ!*

Cú thúc mang theo luồng kình lực Cương Khí Ly Thể đánh bay gã hộ pháp nặng hơn một tạ trượt dài trên mặt sàn thép, đập gãy lan can sà lan rồi nằm bất động, miệng ọc ra một ngụm máu bầm.

Tôi vung đoản đao chém đứt toàn bộ đường dây dẫn và đập nát khối huyết thạch trên sà lan số 2.

Hai trong số bốn luồng hắc khí đã bị tiêu diệt hoàn toàn!'''

ACT3 = '''Tám giờ mười lăm phút tối.

Khi chiếc sà lan số 3 bị tôi vô hiệu hóa sau một loạt những đòn cận chiến dứt khoát và lạnh lùng, toàn bộ sự chú ý của trận chiến dồn về chiếc sà lan số 4 — con tàu chỉ huy lớn nhất neo đậu ngay tại tâm điểm khúc sông Thanh Đa.

Mưa bão lúc này đã đạt tới đỉnh điểm cuồng nộ. Sóng sông Sài Gòn chồm lên cao hơn hai mét, quất từng đợt bọt nước trắng xóa vào thân tàu sắt rỉ sét.

Trên boong chiếc sà lan chỉ huy rộng hàng trăm mét vuông, hàng chục ngọn đuốc phòng bão cắm trên cọc sắt đang bập bùng cháy đỏ rực dưới mưa gió.

Và ở mũi tàu, đứng sừng sững giữa màn mưa là một bóng người cao gầy mặc áo măng tô đen ướt đẫm.

Đó chính là Tạ Lôi!

Gương mặt gã hốc hác, đôi mắt sâu hoắm vằn đỏ những tia máu điên dại. Trên tay phải của gã, thanh **U Minh Huyết Đao** — một thanh đao cổ dài bốn thước rỉ sét loang lổ những vệt máu thâm sì — đang tỏa ra những làn sương khói tím đen ma quái, phát ra những tiếng rít u u như tiếng khóc than của ngàn vạn oan hồn chìm dưới đáy sông.

Nhìn thấy tôi bước lên boong tàu với hai món binh khí trong tay, thân thể rực sáng hoàng kim giữa đêm mưa bão, Tạ Lôi không hề tỏ ra kinh ngạc mà ngược lại, gã ngửa mặt lên trời cười rộ lên một tràng cười the the, man dại:

"Ha ha ha! Nguyễn Minh An! Mày giỏi lắm! Một thằng nhóc kỹ thuật viên quèn không có lấy một mẩu linh căn, vậy mà dám một thân một mình bẻ gãy mười hai cọc Thủy Môn của Cửu Long Thiên Hải chúng tao, lại còn dám mò về tận sào huyệt Sài Gòn này!"

Tôi dừng bước cách gã mười bước chân, Trấn Thủy Đoản Đao chĩa xéo xuống mặt sàn thép, giọng nói lạnh lùng vang lên át cả tiếng sóng gầm:

"Tạ Lôi, bốn chiếc sà lan của ngươi đã bị phế ba chiếc. Toán bắn tỉa ở Nơ Trang Long và toán đột nhập ở Viện Địa chất đều đã sa lưới. Giang sơn Nam Bộ này không phải là nơi cho lũ tà tu các ngươi làm càn. Hãy buông đao chịu trói, đối diện với pháp luật và sự phán xét của đất trời!"

"Buông đao? Đầu hàng?" Tạ Lôi trừng mắt, khóe miệng giật giật đầy ác hiểm. "Mày nghĩ tao là thằng ngu như Tạ Bách Xuyên sao? Mày nghĩ tao không chuẩn bị đường lùi cho canh bạc cuối cùng này sao?!"

Gã giơ tay trái lên.

Trong lòng bàn tay gã là một chiếc hộp điều khiển màu đen nhánh gắn một khối huyết thạch đỏ lòm như con mắt quỷ. Chiếc hộp nối với một bó dây cáp thép to dày, cắm thẳng từ boong tàu xuyên qua đáy sông, dẫn thẳng xuống mắt xích chủ lực số chín của ngọn Cổ Tháp Thần Hoang!

"Mày có biết tao đã đặt cái gì dưới mắt xích số chín không?" Tạ Lôi gầm lên điên cuồng, nước mưa chảy ròng ròng trên gương mặt biến dạng vì thù hận. "Một khối **Huyết Thần Bạo Liệt Trận** tích tụ toàn bộ uế khí của mười hai cọc Thủy Môn bị đánh vỡ! Chỉ cần tao ấn chiếc nút này, toàn bộ khối năng lượng tà thuật sẽ nổ tung, giật đứt mắt xích chủ lực!"

Gã chỉ tay về phía bờ bán đảo Thanh Đa và thành phố rực rỡ ánh đèn phía xa:

"Khi mắt xích chủ lực gãy vụn, toàn bộ thềm phù sa của bán đảo Thanh Đa này sẽ sụp đổ hoàn toàn trong vòng năm phút! Hàng triệu tấn đất đá sẽ đổ sập xuống lòng sông, tạo ra một trận đại hồng thủy nuốt chửng hàng chục ngàn người dân Sài Gòn, đồng thời xé toạc phong ấn Tầng Thứ Sáu! Tao có chết cũng phải kéo theo cả thành phố này chôn cùng!"

Sự tàn độc và điên cuồng của Tạ Lôi đã vượt xa mọi giới hạn của loài người.

Gã không còn là một kẻ tranh đoạt lợi ích thông thường, mà đã hoàn toàn trở thành một con quỷ dữ muốn hủy diệt thế gian trong cơn tuyệt vọng!

"Minh An!"

Trong thức hải của tôi, đóa sen Lục Diệp Thanh Liên bỗng xoay chuyển cực hạn. Hình ảnh Lâm Tịch hiện ra với đôi mắt ngập tràn kiếm ý sương lam buốt giá:

"Tôi sẽ dùng toàn bộ kiếm niệm vừa phục hồi để phong tỏa thần thức của hắn trong một phần mười cái chớp mắt! Anh phải dùng tốc độ nhanh nhất của Hoán Huyết kỳ, chém đứt ngòi nổ trước khi hắn kịp truyền tín hiệu xung điện!"

"Được!" Tôi gầm lên trong tâm thức.

Ngay khoảnh khắc ngón tay cái của Tạ Lôi bắt đầu ấn xuống chiếc nút kích nổ màu đỏ máu:

*ONG!*

Từ giữa trán tôi, một luồng kiếm ý băng phách vô hình trong suốt xé toạc màn mưa đêm, bắn thẳng vào mi tâm của Tạ Lôi!

Thần thức của Tạ Lôi như bị một tảng băng vạn năm đâm xuyên qua, toàn bộ kinh mạch và phản xạ cơ bắp của gã lập tức đình trệ trong một phần mười giây ngắn ngủi!

Đó chính là khoảng thời gian định mệnh!

Ba mươi ba đốt sống tủy ngọc sau lưng tôi bùng nổ toàn bộ sức mạnh của Hoán Huyết Sơ kỳ. Tôi đạp mạnh chân xuống sàn thép, kình lực bộc phát làm lõm sâu một hố tròn đường kính nửa mét.

Thân hình tôi phóng vút qua không trung tựa như một đạo lôi điện hoàng kim!

Thanh **Trấn Thủy Đoản Đao** trong tay tôi chém ra một đường cong hoàn mỹ mang theo toàn bộ Thuần Dương Cương Huyết!

*XOẸT!*

Lưỡi đao sắc bén chém đứt lìa cánh tay trái của Tạ Lôi ngay sát khớp khuỷu tay! Chiếc hộp điều khiển kích nổ rơi văng ra ngoài không trung.

Không để chiếc hộp kịp rơi xuống nước, thanh **Hắc Thiết Đoản Côn** trên tay phải tôi đã quét ngang một đường Kính Kình chuẩn xác, đập nát khối điều khiển tà thuật thành tro bụi lơ lửng giữa màn mưa giông!

*A A A!*

Tiếng thét đau đớn xé ruột xé gan của Tạ Lôi vang vọng khắp mặt sông. Thanh U Minh Huyết Đao trên tay phải gã vụt rơi xuống sàn boong, bị tôi vung chân đá văng chìm sâu xuống đáy nước phù sa.

Gã trùm tác chiến ngầm ngã quỵ xuống mặt sàn thép trơn trượt, ôm lấy cánh tay cụt máu phun xối xả, đôi mắt tràn ngập sự kinh hoàng và tuyệt vọng tột cùng khi nhìn lên người thanh niên đứng sừng sững trước mặt:

"Mày... Mày không phải là người... Làm sao một phàm nhân lại có thể nhanh đến mức này..."

Tôi không trả lời. Tôi rút một đoạn xích thép chịu lực trên vách tàu, quấn chặt lấy người Tạ Lôi rồi khóa chặt gã vào cột trụ chính của chiếc sà lan. Toàn bộ kinh mạch tà công trong cơ thể gã đã bị kiếm ý của Lâm Tịch và kình lực Hoán Huyết của tôi đánh phế hoàn toàn.

Dưới độ sâu âm ba mươi mét dưới lòng sông Sài Gòn, khi mối đe dọa cuối cùng bị dập tắt, ngọn **Cổ Tháp Thần Hoang** chín tầng bỗng rung lên một nhịp chuông ngân trầm hùng, vang vọng khắp cõi u minh.

Chín sợi xích huyền thiết lấy lại sự tĩnh lặng ngàn đời, ghim chặt vào nền đá bazan thềm lục địa.

Một luồng linh quang màu hoàng kim ấm áp từ đỉnh cổ tháp phóng thẳng lên mặt nước, lan tỏa thành những gợn sóng ánh sáng êm đềm đẩy lùi toàn bộ âm trọc khí tím đen độc hại trên sông.

Cơn mưa giông nhiệt đới dần ngớt hạt.

Mây đen tan biến, nhường chỗ cho những vì sao lấp lánh xuất hiện trên bầu trời đêm Sài Gòn.

Phía chân trời đông, những vệt sáng hồng cam đầu tiên của buổi bình minh bắt đầu ló dạng, chiếu rọi lên những nhịp cầu Bình Lợi, cầu Sài Gòn và những tòa nhà chọc trời đang thức giấc trong sự bình yên trọn vẹn.

Tôi đứng trên mũi chiếc sà lan, hít một hơi sâu luồng gió sớm mát lành mang theo hương phù sa nồng nàn của dòng sông quê hương.

Sau lưng tôi, tà khí đã hoàn toàn bị quét sạch.

Bão ngầm Sài Gòn đã tan. Và tôi biết, mình đã giữ trọn vẹn lời hứa bảo vệ mảnh đất phương Nam này bằng chính đôi bàn tay và dòng máu của một phàm nhân!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3000 or word_count > 5500:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,000 - 5,000 từ)")

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
        active_characters=["char_minh_an", "char_lam_tich"],
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
description: "Minh An giải cứu Viện Địa chất, đột kích 4 sà lan tà thuật trên sông Sài Gòn và quyết chiến chém cụt tay Tạ Lôi, bảo vệ vẹn toàn bán đảo Thanh Đa."
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
        "Giải Cứu Viện Địa Chất, Đột Kích Bốn Sà Lan Tà Thuật & Trảm Tạ Lôi Tại Bán Đảo Thanh Đa",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:00:00+07:00",
        CHAPTER_NUM,
        "loc_ban_dao_thanh_da",
        json.dumps(["char_minh_an", "char_lam_tich", "char_ta_loi"]),
        "Minh An thần tốc giải cứu Giáo sư Trần Văn Định tại Viện Khảo sát Địa chất Nam Bộ, vô hiệu hóa 5 tên tà tu và bảo vệ trọn vẹn các mẫu lõi khoáng vật. Đêm xuống trong cơn mưa giông nhiệt đới dữ dội, Minh An bơi lặn sông Sài Gòn, dùng Kính Kình và Trấn Thủy Đoản Đao phá nát 3 cụm sà lan tà thuật. Tại sà lan số 4, đối đầu Tạ Lôi cầm U Minh Huyết Đao định tự bạo Huyết Thần Trận phá hủy mắt xích chủ lực ngọn Cổ Tháp Thần Hoang. Lâm Tịch xuất chiêu Băng Phách Kiếm Ý đóng băng thần thức Tạ Lôi, Minh An chém đứt lìa cánh tay cầm ngòi nổ của Tạ Lôi, bắt sống kẻ cầm đầu và bảo vệ trọn vẹn bình yên bán đảo Thanh Đa.",
        "Tiêu diệt toàn bộ mạng lưới tác chiến ngầm Cửu Long Thiên Hải tại Sài Gòn; bắt sống Tạ Lôi; bảo vệ an định tuyệt đối Cổ Tháp Thần Hoang 9 tầng; khép lại thắng lợi rực rỡ Hồi 2."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch phóng xuất Băng Phách Kiếm Ý sắc lạnh đóng băng thần thức Tạ Lôi trong tích tắc định mệnh, phối hợp hoàn hảo cùng đao pháp Thuần Dương của Minh An."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An thể hiện đỉnh cao Hoán Huyết Sơ kỳ: bơi lặn ngược dòng lũ sông Sài Gòn, Kính Kình phá nát kim loại và đá huyết thạch, Trấn Thủy Đoản Đao chém đứt móng vuốt thép độc."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Mắt xích chủ lực số chín của Cổ Tháp Thần Hoang được bảo vệ an định tuyệt đối; linh quang hoàng kim lan tỏa khắp dòng sông Sài Gòn, thanh lọc hoàn toàn âm trọc khí."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An cứu thoát Giáo sư Trần Văn Định, thu hồi mẫu đá thềm lục địa số 9, bắt sống trùm tác chiến Tạ Lôi, kết thúc mối họa Cửu Long Thiên Hải tại Sài Gòn."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T21:00:00+07:00"
        inv_data["current_location"] = "Mũi Sà Lan Chỉ Huy, Bán Đảo Thanh Đa, Sông Sài Gòn"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Huyết Ánh Kim / Cốt Tủy Thấu Quang / Cương Khí Ly Thể)"

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

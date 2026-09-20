# -*- coding: utf-8 -*-
"""Draft Chapter 78 for Phá Trời Novel OS with ~4,000+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 78
CHAPTER_TITLE = "Khí Quán Chứa Chan"
DATE = "2026-10-24"
LOCATION = "Thềm Đá Cổ Thần Quy & Rừng Núi Chứa Chan (Xuân Lộc, Đồng Nai)"

ACT1 = '''Hai giờ mười lăm phút chiều ngày hai mươi tư tháng mười.

Từ trên gờ đá granite cao hơn bốn mét so với mặt bằng công trường, tôi búng người lao xuống như một cánh chim ưng vồ mồi.

Toàn bộ ba mươi ba đốt sống lưng của tôi phát xuất một chuỗi âm thanh lách cách giòn giã tựa ngọc thạch va đập. Thuần Dương Cương Huyết cuộn trào bỏng rát từ tim dồn thẳng xuống cánh tay phải. Thanh Hắc Thiết Đoản Côn nặng hơn ba ký hai vẽ nên một đường cung màu đen nhánh ánh chu sa đỏ rực giữa tầng không, xé gió giáng thẳng xuống đỉnh đầu tên tà tu Tạ Lôi!

"Kẻ nào?!"

Tạ Lôi gầm lên một tiếng kinh thiên động địa. Phản xạ của một gã cựu thủ lĩnh lính đánh thuê dạn dày hàng trăm trận cận chiến sinh tử tại vùng Tam Giác Vàng lập tức phát huy tác dụng.

Hắn không hề nao núng lùi bước. Bàn tay trái hộ bối lang yêu siết chặt chuôi thanh đại đao hợp kim đen nhánh nặng hai mươi ký, vung ngược từ dưới lên trên đón đỡ đòn giáng thế của tôi!

*KEEENG!*

Một tiếng va chạm chói tai như tiếng cồng đồng nổ tung giữa không trung.

Sóng xung kích từ cú va đập kim thạch tàn khốc quét ra xung quanh, thổi bạt những lớp bụi đá và lá khô trên mặt thềm đá hoa cương. Sức nặng của thanh đại đao kết hợp với kình lực Thiết Cốt tà môn của Tạ Lôi quả thực hung hãn vô song, truyền một luồng chấn động tê dại ngược trở lại cổ tay tôi.

Nhưng tôi không hề cứng đối cứng để chịu trận.

Ngay tại thời khắc hai khối kim loại chạm nhau, tôi lập tức vận chuyển tuyệt kỹ Kính Kình — uốn cong cổ tay, triệt tiêu bốn mươi phần trăm phản lực chấn động, rồi mượn chính sáu mươi phần trăm kình lực dội ngược của Tạ Lôi để lộn một vòng tròn hoàn hảo trên không trung.

Chân phải tôi vung ra như một ngọn roi thép, nhằm thẳng vào cổ tay phải của Tạ Lôi — nơi hắn đang cầm chiếc máy kích nổ vô tuyến!

*BỐP!*

Cú đá chuẩn xác đến từng mi-li-mét trúng ngay huyệt đạo cổ tay Tạ Lôi. Lực chấn mạnh đến mức khiến ngón tay cái của hắn bật khỏi nút kích hoạt màu đỏ. Chiếc máy kích nổ vô tuyến văng ra khỏi tay hắn, bay vút qua mép vực sâu thăm thẳm rồi rơi thẳng xuống đáy vực rậm rạp sương mù bên dưới!

"Khốn kiếp! Mày muốn chết!"

Tạ Lôi thấy chiếc máy kích nổ bị đá văng thì điên cuồng gầm rống. Hắn buông tay khỏi nẹp lưng, rút phắt khẩu súng phóng lựu M79 báng cưa nòng ngắn giắt bên hông, nhằm thẳng vào lồng ngực tôi ở cự ly chưa đầy ba mét mà bóp cò!

*OÀNG!*

Một quả đạn nổ mảnh bốn mươi mi-li-mét phụt ra khỏi nòng súng kèm theo quầng lửa màu cam rực rỡ.

Ở cự ly cận chiến ngặt nghèo này, một người bình thường chắc chắn sẽ bị xé thành từng mảnh vụn. Nhưng ngay khoảnh khắc ngón tay Tạ Lôi khẽ siết cò, các giác quan sắc bén của Luyện Cốt Hậu kỳ đã giúp tôi đọc trước hướng nòng súng.

Tôi không nhảy lùi ra sau — bởi phía sau là vách vực trống trải. Tôi ngả rạp người sát mặt đất, chân trái làm trụ, cả thân thể trượt dài trên sườn đá granite dốc sáu mươi độ như một mũi tên xé gió.

Quả đạn M79 bay sượt qua vai áo tôi chừng một gang tay, đâm thẳng vào khối cự thạch phía sau và phát nổ kinh hoàng.

*ÙNG!*

Đất đá văng tung tóe, khói thuốc súng khét lẹt bao trùm không gian. Hàng chục mảnh kim loại sắc bén văng ra như mưa rào, găm thẳng vào chiếc ba lô dã chiến và rạch toạc lớp áo khoác gió bên bả vai trái của tôi. Một vệt máu đỏ tươi rỉ ra, nhưng lớp màng cơ bắp cuộn chặt tựa thép nguội bên dưới da tôi đã tự động siết lại, chặn đứng mảnh kim loại cắm sâu vào tủy sống.

"Bắn! Bắn chết nó cho tao!" Tạ Lôi vừa lùi lại vừa quát tháo đám thuộc hạ.

Bốn tên lính đánh thuê gác cửa lập tức giương súng tiểu liên báng gấp, những nòng súng đen ngòm khạc lửa xối xả về phía tôi:

*Tằng tằng tằng tằng!*

Những làn đạn chì chín mi-li-mét đan thành một tấm lưới tử thần rít lên xé toạc màn sương mù sườn núi.

Nấp sau một mỏm đá hoa cương nhô cao, tôi hít sâu một hơi, vận hành tuyệt kỹ Quy Tức Quyết kết hợp với nhịp đập chậm rãi bốn mươi lần một phút của trái tim. Trong mắt tôi lúc này, đường đi của từng viên đạn dường như chậm lại một nửa.

Tôi không dùng súng, không dùng vũ khí tầm xa. Phàm nhân tu Thể Đạo lấy chính nhục thân làm chiến trường!

Chờ cho loạt đạn tiểu liên vừa ngắt nhịp để thay băng đạn, tôi đạp mạnh chân vào vách đá, thân hình vọt ra như một bóng ma đen nhánh. Lợi dụng những góc chết của địa hình đá tai mèo lởm chởm, tôi áp sát tên lính đánh thuê đầu tiên chỉ trong ba phần mười giây.

Không cần vung côn, bàn tay trái tôi xòe ra như chiếc kìm thép, chộp thẳng vào nòng khẩu tiểu liên vừa nóng rực, bẻ gập nòng súng sang một bên. Đồng thời, ngón trỏ và ngón giữa tay phải tôi điểm thẳng vào hõm vai của hắn.

Kình lực Luyện Cốt thẩm thấu qua thớ thịt, khóa chặt huyệt đạo khiến toàn thân gã lính đánh thuê tê liệt, ngã gục xuống sàn đá mà không kịp kêu lên một tiếng.

Tên thứ hai hoảng hốt rút dùi cùi điện định lao vào thì thanh Hắc Thiết Đoản Côn trong tay tôi đã quét ngang một đường tròn êm ái. Đầu côn bọc da bò đập trúng khớp xương bánh chè của hắn, triệt tiêu hoàn toàn khả năng đứng vững.

Chưa đầy mười giây đồng hồ, bốn tên lính đánh thuê trang bị vũ khí nóng hiện đại đã bị tôi dùng bộ pháp Thể Đạo và mưu mẹo cận chiến tước bỏ hoàn toàn khả năng tác chiến, nằm rên rỉ trên mặt đá.

Hiện trường thềm đá lúc này chỉ còn lại tôi và Tạ Lôi — kẻ mang biệt danh Lôi Báo của vùng Tam Giác Vàng!'''

ACT2 = '''Gió chiều trên đỉnh Chứa Chan thổi thốc qua khe vực, mang theo mùi thuốc súng khét lẹt hòa lẫn với hơi nóng bỏng rát của đá hoa cương bị nung dưới nắng gắt.

Tạ Lôi vứt bỏ khẩu súng M79 đã hết đạn sang một bên, hai tay nắm chặt chuôi thanh đại đao hợp kim đen nhánh.

Đôi mắt hắn đỏ ngầu như mắt lợn rừng bị thương, gân máu nổi chằng chịt trên tròng trắng. Toàn bộ lớp da xám xịt ánh kim loại trên ngực hắn bắt đầu phồng rộp lên, những đường gân xanh đen nổi gồ ghề như những con trăn nhỏ bò ngoằn ngoèo dưới lớp biểu bì.

"Một thằng nhóc phàm nhân ranh con mà dám phá hỏng đại sự của Cửu Long Thiên Hải tao!" Tạ Lôi gầm gừ, giọng nói trầm đục như tiếng kim loại cọ xát vào đá tảng. "Mày nghĩ đá văng được máy kích nổ là cứu được cọc tiêu này sao? Mười sáu khối C4 kia đều có gắn kíp nổ áp suất cơ học dự phòng! Chỉ cần tao chém gãy chân mày, tao sẽ tự tay dùng gót chân đạp nổ tung cái thềm đá chết tiệt này!"

*VÙ!*

Không để tôi kịp đáp lời, Tạ Lôi đạp mạnh hai chân xuống mặt đá. Phiến đá granite hoa cương dưới chân hắn lập tức nứt toác thành hình mạng nhện. Thân hình đồ sộ cao gần một mét chín của hắn lao vút tới như một cỗ xe tăng bánh xích, thanh đại đao hai mươi ký chém xuống một nhát bạt sơn cửu đỉnh!

Nhát chém mang theo luồng tà khí Thiết Cốt tanh nồng, tạo ra một tiếng rít xé toạc không khí.

Tôi vội lách người né sang phải. Lưỡi đao chém hụt, đâm thẳng vào một khối đá hoa cương nặng hơn năm tấn cạnh thềm đá.

*RẮC!*

Khối đá hoa cương cứng cấp tám thang Mohs bị thanh đại đao chém vỡ toang làm đôi như một quả dưa hấu! Những mảnh đá vụn sắc lẹm bắn tung tóe găm vào vách đá xung quanh.

Sức mạnh cận chiến của Thiết Cốt tà môn quả thực hung hãn đến mức rợn người. Nếu tôi dại dột dùng Hắc Thiết Đoản Côn chặn trực diện nhát chém này, kình lực va đập sẽ tạo ra chấn động cực lớn truyền thẳng xuống chân bệ đỡ thềm đá — nơi mười sáu khối bộc phá C4 đang chực chờ kích nổ theo áp suất va đập!

"Không thể đánh cứng đối cứng ở đây!" Tôi thầm nhủ, mồ hôi lạnh chảy ròng ròng sau gáy.

Muốn thắng Tạ Lôi mà không làm nổ tung thềm đá Thần Quy, tôi chỉ có một con đường duy nhất: **Dùng trí để dẫn dụ hắn vào tử huyệt!**

Tôi giả vờ hụt hơi, lùi liền ba bước về phía mép vực của Thềm Đá Cổ Thần Quy — nơi vết chém Kiếm Ngân ngàn năm của Bạch Viên Kiếm Tôn đang dao động không ngừng.

"Chạy đi đâu con chuột nhắt!" Tạ Lôi tưởng tôi đã kiệt sức, cười man dại sải bước đuổi theo, đại đao trong tay múa tít thành một vòng tròn đen đặc quánh kình lực tà đạo.

Từng bước lùi của tôi đều được tính toán chính xác theo góc độ phong thủy và địa chất. Càng tiến gần về phía vết chém Kiếm Ngân, luồng Vô Ngân Kiếm Khí vô hình càng trở nên dày đặc, sắc bén đến mức làm da mặt tôi rát buốt như bị hàng ngàn mũi kim châm.

Đúng lúc này, trong thức hải tôi, đài sen ngọc bích bỗng rung chuyển dữ dội.

Bóng hình Lâm Tịch hiện lên giữa quầng sáng trắng thanh khiết. Nàng khoác bộ váy cổ phong phiêu dật, nhưng gương mặt nàng lúc này tái nhợt không còn một giọt máu. Để giúp tôi cảm nhận được nhịp điệu của kiếm khí giữa chiến trường hỗn loạn, nàng đang phải cưỡng ép xuất thần niệm chống lại áp chế tàn khốc của quy tắc Trái Đất.

*"Minh An... cẩn thận..."* Tiếng nói của Lâm Tịch vang lên, yếu ớt và đứt quãng chưa từng có. *"Đài sen của ta... đang bị hàn sát phong ấn chấn động... Ta chỉ có thể định vị tần số kiếm khí cho ngươi một lần duy nhất..."*

"Lâm Tịch! Đừng ép bản thân quá mức!" Tôi truyền niệm kêu lên, trong lòng dâng lên một nỗi xót xa đau đớn đến tột cùng.

Tôi nhìn thấy rõ ràng trên cánh sen ngọc bích nơi nàng tĩnh tọa, một vết nứt li ti màu xám tro vừa xuất hiện. Mỗi một lần nàng thi triển thần niệm vì tôi, tàn hồn của nàng lại tiêu hao thêm một phần. Nỗi đau ấy so với vết thương thể xác do đạn bắn còn đau đớn gấp trăm ngàn lần!

*"Đừng bận tâm về ta... Hãy tập trung!"* Lâm Tịch cắn răng truyền âm, ngón tay ngọc chỉ thẳng về phía khoảng không trước mặt vết chém: *"Hướng ba giờ... cách vết chém ba tấc... nhịp kiếm thứ bảy! Đó là nơi Vô Ngân Kiếm Khí giao thoa tạo thành khoảng trống phản chấn! 'Dĩ Thể Vi Kiếm' — hãy lấy ba mươi ba đốt sống lưng làm vỏ, hút kiếm khí vào đoản côn!"*

Lời chỉ dẫn của Lâm Tịch vừa dứt, Tạ Lôi đã gầm thét lao tới mép vực.

Thanh đại đao hợp kim của hắn giơ cao quá đầu, dồn toàn bộ kình lực Thiết Cốt tà môn chém xuống một đòn quyết định nhằm băm tôi thành hai nửa:

"Chết đi cho tao!"

Ngay tại khoảnh khắc ngàn cân treo sợi tóc ấy, tôi không lùi nữa.

Tôi bước chéo một bước về hướng ba giờ, đúng ba tấc cạnh vết chém Kiếm Ngân. Toàn bộ ba mươi ba đốt sống ngọc thạch đồng thau trong lồng ngực tôi mở toang mọi kinh mạch, dòng Thuần Dương Cương Huyết cuộn trào bỏng rát như dung nham núi lửa.

Một luồng Vô Ngân Kiếm Khí sắc lạnh vô hình từ vết chém trên vách đá như tìm được chốn dung thân đồng điệu, lập tức tràn vào thân thể tôi!

Kiếm khí lạnh buốt xuyên qua từng thớ thịt, cắt rách chiếc áo dã chiến trên ngực tôi thành từng mảnh vụn. Cảm giác đau đớn như bị dao lam cứa vào từng tế bào khiến tôi muốn gào thét. Nhưng tôi cắn chặt môi đến bật máu, giữ vững bản tâm phàm nhân kiên định, không để kiếm khí xé nát tâm mạch mà dùng chính kình lực Luyện Cốt Hậu kỳ dẫn dắt toàn bộ luồng kiếm khí ấy rót thẳng vào thanh Hắc Thiết Đoản Côn!

Thanh đoản côn đen nhánh bỗng phát ra một tiếng kiếm reo trong trẻo, vang dội thấu tận mây xanh!

Một vệt kiếm mang màu bạch ngọc sắc lẹm dài hơn một trượng bọc quanh thân côn, phát xuất luồng uy áp cổ xưa của Bạch Viên Kiếm Tôn ngàn năm trước!

"Dĩ Thể Vi Kiếm, Khí Quán Cửu Tiêu!"

Tôi hét lớn một tiếng, vung thanh Hắc Thiết Đoản Côn chém ngang một nhát tuyệt mỹ!

*XOẸT!*

Một âm thanh thanh thoát, ngọt ngào vang lên giữa không trung.

Thanh đại đao hợp kim nặng hai mươi ký của Tạ Lôi bị vệt kiếm mang vô hình chém đứt ngọt xớt như một khúc mía non! Nửa trên của lưỡi đao văng thẳng lên trời, xoay tít rồi cắm ngập vào vách đá phía sau.

Đạo kiếm mang không hề dừng lại. Nó lướt qua lồng ngực của Tạ Lôi, chém toạc lớp da Thiết Cốt xám xịt kim loại của hắn.

*PHỤT!*

Một vệt máu đen tanh tưởi phun ra xối xả. Toàn bộ mạng lưới gân cốt tà môn trên ngực Tạ Lôi bị kiếm khí thuần khiết của tiền nhân phá tan nát. Kình lực phản chấn khủng khiếp đánh bạt thân hình đồ sộ gần một trăm ký của hắn bay ngược ra sau hơn mười mét, đập mạnh vào vách đá hoa cương rồi ngã sụp xuống như một đống bùn nhão!'''

ACT3 = '''Ba giờ mười lăm phút chiều.

Bụi đá và khói thuốc súng trên Thềm Đá Cổ Thần Quy dần dần lắng xuống theo ngọn gió rừng đại ngàn.

Tạ Lôi nằm sõng soài trên vách đá, miệng không ngừng ộc ra từng ngụm máu đen bầm tím. Thanh đại đao gãy đôi nằm chỏng chơ bên cạnh. Lớp da màu xám xịt ánh kim loại trên người hắn đã hoàn toàn biến mất, thay vào đó là một màu trắng bệch thảm hại của kẻ vừa bị phế sạch toàn bộ công phu tà đạo.

Đôi mắt hắn trợn trừng nhìn tôi, tràn đầy sự kinh hoàng và không thể tin nổi:

"Mày... mày rốt cuộc là quái vật gì? Một thằng kỹ sư trần tục hai mươi lăm tuổi... tại sao lại có thể điều khiển được kiếm khí của Bạch Viên Kiếm Tôn? Dĩ Thể Vi Kiếm... đó là tuyệt kỹ thất truyền ngàn năm của bậc đại năng Thể Kiếm Song Tu... tại sao mày lại biết?"

Tôi không thèm trả lời những câu hỏi điên loạn của hắn.

Hạ thanh Hắc Thiết Đoản Côn xuống, tôi lập tức lao nhanh về phía bốn góc chân móng của thềm đá Thần Quy.

Thời gian không còn nhiều!

Dùng thanh Trấn Thủy Đoản Đao sắc bén, tôi cẩn thận cắt rời từng sợi dây điện kích nổ và tháo rời toàn bộ mười sáu khối bộc phá dẻo C4 quân dụng ra khỏi các hốc nứt địa tầng. Từng khối thuốc nổ dẻo màu xám tro nặng trịch được tôi gom lại, đặt sâu vào một hốc đá tự nhiên cách xa thềm đá hơn năm mươi mét để bảo đảm an toàn tuyệt đối.

Khi khối bộc phá cuối cùng được gỡ bỏ, một sự chuyển hóa kỳ diệu bỗng diễn ra ngay trước mắt tôi.

*ÙNG... ÙNG...*

Thềm Đá Cổ Thần Quy khẽ phát ra một tiếng rền rĩ trầm đục, trang nghiêm tựa như tiếng thở phào nhẹ nhõm của một vị thần khổng lồ sau hàng thế kỷ bị giam cầm.

Vết chém Kiếm Ngân dài ba mươi trượng trên lưng thềm đá bỗng tỏa ra một làn quang hoa màu lam ngọc dịu dàng. Những luồng Vô Ngân Kiếm Khí sắc bén hung hãn trước đó dần dần thu liễm, hòa nhập hoàn toàn vào cấu trúc đá granite kỷ đệ tứ, tạo thành một màng phong tỏa vô hình vững chắc tựa bàn thạch.

Dưới đáy vực sâu thăm thẳm, tiếng gầm gừ đục ngầu của mạch ác long thạch sát bị ép lùi sâu vào lòng đất, hoàn toàn im bặt.

Cọc tiêu thứ tám Thần Quy Thạch đã an định tuyệt đối!

Tôi đứng tựa lưng vào vách đá, thở dốc từng cơn. Toàn thân tôi đau nhức như bị bẻ gãy từng chiếc xương sườn. Chiếc áo dã chiến rách nát tả tơi, vết thương do mảnh đạn trên vai trái vẫn đang rỉ máu, thấm đỏ một mảng áo phông sẫm màu.

Nhưng điều khiến tim tôi thắt lại không phải là vết thương thể xác.

Trong thức hải tôi, đài sen ngọc bích của Lâm Tịch lúc này đã thu nhỏ lại chỉ còn bằng một bàn tay. Quầng sáng trắng bao quanh nàng mờ nhạt đến mức gần như trong suốt. Vết nứt màu xám tro trên cánh sen vẫn nằm đó, như một vết sẹo vĩnh viễn nhắc nhở tôi về cái giá mà nàng vừa phải trả để cứu mạng tôi.

"Lâm Tịch... cô có sao không?" Tôi truyền niệm khẽ gọi, thanh âm nghẹn ngào nơi cuống họng.

Phải mất một hồi lâu, tiếng nói của nàng mới vang lên, thì thào tựa như một cơn gió thoảng qua kẽ lá:

*"Ta... không sao... Chỉ là tàn hồn tiêu hao quá độ, cần phải ngủ say một thời gian dài để tĩnh dưỡng..."*

Nàng dừng lại một chút, dường như đang cố gắng gom góp từng chút thần niệm cuối cùng:

*"Minh An... ngươi đã làm rất tốt. Ngươi đã lấy thân làm kiếm, lĩnh ngộ được bản tâm của Thể Đạo... Nhưng ngươi hãy nhớ lời ta... từ nay về sau, nếu không phải thời khắc sinh tử tuyệt vọng, chớ có tùy tiện vận dụng Dĩ Thể Vi Kiếm... Mỗi lần kiếm khí cổ xưa nhập thể, nó sẽ gọt giũa xương tủy ngươi, nhưng cũng đồng thời mài mòn đi từng chút cảm giác trần thế của ngươi..."*

"Tôi nhớ rồi. Cô hãy nghỉ ngơi đi, đừng nói nữa." Tôi cắn chặt môi, cố ngăn không cho giọt nước mắt trào ra nơi khóe mi.

Bóng hình Lâm Tịch khẽ gật đầu rồi tan biến vào trung tâm đài sen, chìm sâu vào giấc ngủ tĩnh dưỡng miên man.

Tôi mở mắt ra, nhìn về phía Tạ Lôi đang nằm thoi thóp dưới chân vách đá.

Thấy tôi tiến lại gần, Tạ Lôi ho sặc sụa ra máu, trên gương mặt đầy sẹo bỗng nở một nụ cười tàn độc, méo mó:

"Mày tưởng mày bảo vệ được cọc tiêu này là mày thắng rồi sao, thằng nhóc?"

Hắn ngước đôi mắt vằn vện tia máu nhìn tôi, thều thào từng lời độc địa:

"Mày nghĩ Tập đoàn Cửu Long Thiên Hải chỉ là một công ty khoáng sản tầm thường sao? Bọn tao đã nắm rõ toàn bộ lý lịch của mày từ cái đêm ở Ba Son rồi! Nguyễn Minh An, hai mươi lăm tuổi, nhân viên hợp đồng của Viện Địa tầng... Quê quán ở một huyện cù lao nghèo mạn Tiền Giang, có một bà mẹ già bán rau ngoài chợ huyện sống thui thủi một mình..."

Nghe đến hai chữ "mẹ già", lồng ngực tôi bỗng nhói buốt như bị một mũi dao nhọn đâm xuyên qua tim!

Bàn tay tôi siết chặt thanh Hắc Thiết Đoản Côn đến mức các khớp xương kêu răng rắc, đốt sống lưng run rẩy kịch liệt.

Tạ Lôi nhìn thấy phản ứng của tôi thì càng cười khoái trá, tiếng cười the the như tiếng quạ kêu đêm:

"Mày cản đường đại nghiệp khai thông long mạch của các ngài... Mày nghĩ người thân của mày sẽ yên ổn được sao? Khi các ngài ở tổng bộ phái Chân Thân đại năng xuống, không chỉ cái mạng cùi của mày, mà cả cái xóm nghèo của mẹ mày, cả cái cơ quan của thằng bạn thân mày... tất cả sẽ bị nghiền nát thành tro bụi!"

"Câm mồm!"

Tôi quát lên một tiếng trầm đục, vung tay điểm một chỉ vào huyệt câm của Tạ Lôi, khiến hắn nghẹn họng ú ớ không thể phát ra tiếng cười ma quái ấy được nữa.

Tôi dùng dây dù quân dụng trói chặt Tạ Lôi và bốn tên thuộc hạ lại thành một xâu, kéo chúng vào bóng râm của lán chỉ huy dã chiến, bên cạnh là toàn bộ số vũ khí nóng, súng phóng lựu M79 và mười sáu khối bộc phá C4 đã bị vô hiệu hóa.

Từ phía chân núi xa xăm, tiếng còi hụ xe đặc chủng của Công an huyện Xuân Lộc và lực lượng kiểm lâm bắt đầu vang lên dồn dập, xé toạc sự tĩnh lặng của buổi chiều tà. Những đợt rung chấn và tiếng súng nổ trước đó đã đánh động toàn bộ lực lượng an ninh địa phương.

Tôi biết mình không thể ở lại đây để bị thẩm vấn hay lộ diện trước ống kính truyền thông. Thân phận của tôi phải được giấu kín trong bóng tối.

Tôi khoác chiếc ba lô dã chiến nặng trịch lên vai, kéo chiếc mũ lưỡi trai sụp xuống che khuất nửa gương mặt đầy bụi đá và vệt máu khô, rồi lặng lẽ xoay người bước nhanh vào màn rừng le rậm rạp phía sườn tây.

Bốn giờ ba mươi phút chiều.

Tôi đứng trên một mỏm đá cheo leo ở độ cao bảy trăm mét, phóng tầm mắt nhìn về phía chân trời xa xăm.

Ánh hoàng hôn màu đỏ ối như máu đang buông xuống nhuộm đỏ cả một vùng trời miền Đông Nam Bộ. Gió chiều thổi lồng lộng, làm tung bay vạt áo rách bươm của tôi.

Phía xa xăm kia, qua khỏi những cánh rừng cao su bạt ngàn của Đồng Nai, là ánh đèn lung linh của Sài Gòn — nơi có căn phòng trọ nhỏ bé trên đường Nơ Trang Long, có những quán cơm tấm thơm mùi khói than và những ly cà phê sữa đá ngọt ngào.

Và xa hơn nữa về phía tây nam, là xóm quê thanh bình ven sông Tiền — nơi người mẹ già tóc bạc của tôi vẫn đang ngóng trông từng chuyến xe đò cuối tuần, mong đứa con trai trở về ăn bữa cơm canh cua đồng ấm áp.

Lời đe dọa của Tạ Lôi vẫn văng vẳng bên tai tôi như một bản án nghiệt ngã.

Lần đầu tiên kể từ ngày bước chân vào con đường Thể Đạo, tôi cảm nhận được một nỗi bi thương và bất lực sâu sắc đến nghẹn thở.

Tôi có thể đấm vỡ đá hoa cương, có thể dùng thân làm kiếm chém đứt đại đao hợp kim, nhưng tôi không thể bảo vệ mẹ bằng cách mang bà theo bên mình giữa những trận huyết chiến đạn bom tàn khốc. Càng mạnh mẽ, chiếc bóng thù hằn phía sau tôi càng lớn, và những người tôi yêu thương nhất lại càng dễ trở thành mục tiêu bị tàn sát.

"Mẹ ơi... con xin lỗi..." Tôi thì thầm trong gió, nước mắt lặng lẽ lăn dài trên gò má rám nắng đầy bụi đá.

Con đường phía trước của tôi đã không còn lối rẽ êm đềm nào nữa.

Để bảo vệ mẹ, bảo vệ Tuấn, bảo vệ những người bình dị vô tội của thành phố này, tôi sẽ phải nuốt trọn mọi đắng cay vào lòng, tự mình buông bỏ những mối liên lạc trần thế, chấp nhận trở thành một kẻ cô độc bước đi trong màn đêm vô tận.

Đại cục trường thiên của "Phá Trời" giờ đây mới thực sự bắt đầu bằng những vết sẹo rớm máu trong tâm hồn!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3000 or word_count > 5500:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,000 - 5,000 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words)
    print(f"[*] [2/6] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường)...")
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
        active_characters=["char_minh_an", "char_lam_tich", "char_ta_loi"],
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
        "Huyết Chiến Thần Quy Thạch, Dĩ Thể Vi Kiếm & Nỗi Đau Cô Độc",
        CHAPTER_NUM,
        1,
        f"{DATE}T16:30:00+07:00",
        CHAPTER_NUM,
        "loc_them_da_than_quy",
        json.dumps(["char_minh_an", "char_lam_tich", "char_ta_loi"]),
        "Minh An xuất kích đá văng kíp nổ vô tuyến của Tạ Lôi, né tránh đạn M79 và vô hiệu hóa toán lính đánh thuê. Dẫn dụ Tạ Lôi vào vùng Kiếm Ngân Thần Quy Thạch. Nhờ sự hỗ trợ xuất thần niệm của Lâm Tịch khiến đài sen của nàng rạn nứt thêm một vệt xám tro, Minh An ngộ ra Dĩ Thể Vi Kiếm, dung nạp Vô Ngân Kiếm Khí chém gãy đại đao hợp kim và phế sạch Thiết Cốt tà môn của Tạ Lôi. Tháo gỡ an toàn 16 khối C4, an định cọc tiêu thứ tám. Tạ Lôi tiết lộ Cửu Long Thiên Hải đã điều tra lý lịch người mẹ già ở quê của Minh An. Minh An bàn giao hiện trường cho công an huyện Xuân Lộc, lặng lẽ rút lui vào rừng già, đối diện với nỗi đau bất lực và sự chia cách thầm lặng để bảo vệ người thân.",
        "Cọc tiêu thứ tám Thần Quy Thạch an định hoàn toàn; Tạ Lôi bị bắt; Lâm Tịch tàn hồn suy kiệt ngủ say; Minh An nhận thức gánh nặng bi thương của kẻ thủ hộ cô độc."
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
        "Cọc tiêu thứ tám Thần Quy Thạch tại Núi Chứa Chan (Đồng Nai) đã được an định hoàn toàn; 8/12 cọc tiêu Thủy Môn đã giải quyết."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An lĩnh ngộ thành công Dĩ Thể Vi Kiếm, dung nạp Vô Ngân Kiếm Khí vào 33 đốt sống ngọc thạch và Hắc Thiết Đoản Côn; thể phách đạt tới giới hạn Luyện Cốt Hậu kỳ."
    ))

    # Đăng ký tuyến truyện bi thương TH-TRG-001 nếu chưa có
    cur.execute("""
    INSERT OR REPLACE INTO story_threads (
        thread_id, thread_type, title, description, origin_chapter, target_resolution_chapter,
        status, current_state, known_info, hidden_info, reader_knowledge,
        last_touched_chapter, revisit_window_chapters, urgency, importance, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (
        "TH-TRG-001", "CHARACTER_ARC", "Bi Kịch Của Kẻ Thủ Hộ & Sự Chia Cách Thầm Lặng",
        "Gánh nặng cô độc của Minh An: buộc phải giữ khoảng cách và xa lánh mẹ già cùng bạn bè để bảo vệ họ khỏi sự trả thù của Cửu Long Thiên Hải; đối mặt với sự suy kiệt tàn hồn của Lâm Tịch.",
        78, 300, "ACTIVE",
        "Minh An nhận lời đe dọa từ Tạ Lôi về người mẹ già ở quê; Lâm Tịch rạn nứt đài sen chìm vào ngủ say; Minh An rơi nước mắt chấp nhận con đường cô độc.",
        "Minh An biết kẻ địch đã lần ra danh tính người thân ở quê.",
        "Cửu Long Thiên Hải đang bí mật cử phân đà thám thính khu vực Tiền Giang và Bình Thạnh.",
        "Độc giả cảm nhận sâu sắc nỗi đau hy sinh thầm lặng của người con hiếu thảo nhưng phải đứng ngoài khung cửa sổ dưới mưa.",
        78, 10, "HIGH", "CORE"
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T16:30:00+07:00"
        inv_data["current_location"] = "Rừng Già Sườn Tây Núi Chứa Chan, Đồng Nai"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ Cực Cảnh (33 Đốt Sống Ngọc Thạch / Dĩ Thể Vi Kiếm)"
        
        # Cập nhật tình trạng Trâm Ngọc Lâm Tịch
        for itm in inv_data.get("core_weapons_and_artifacts", []):
            if "Lâm Tịch" in itm.get("name", ""):
                itm["condition"] = "Xuất hiện vết rạn xám tro mới, đài sen thu nhỏ, Lâm Tịch rơi vào ngủ say sâu"
                itm["durability"] = "80/100"

        # Thêm kỹ năng mới Dĩ Thể Vi Kiếm
        skills = inv_data.get("core_skills", [])
        if not any(s.get("name") == "Dĩ Thể Vi Kiếm (Vô Ngân Kiếm Ý)" for s in skills):
            skills.append({
                "name": "Dĩ Thể Vi Kiếm (Vô Ngân Kiếm Ý)",
                "type": "Thể Kiếm Song Tu / Dung hợp kiếm ý cổ",
                "stage": "Sơ ngộ (Lấy 33 đốt sống ngọc thạch làm vỏ kiếm, dẫn kiếm khí vào Hắc Thiết Đoản Côn chém đứt hợp kim)"
            })
        inv_data["core_skills"] = skills

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

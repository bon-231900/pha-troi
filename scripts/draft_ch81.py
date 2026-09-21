# -*- coding: utf-8 -*-
"""Draft Chapter 81 for Phá Trời Novel OS with ~4,000+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 81
CHAPTER_TITLE = "Trấn Ba Thạch Quy"
DATE = "2026-10-25"
LOCATION = "Cồn Trấn Ba & Cổ Miếu Trấn Ba (Sông Tiền, Tiền Giang)"

ACT1 = '''Năm giờ bốn mươi phút chiều ngày hai mươi lăm tháng mười.

Mưa giăng mờ mịt trên dòng sông Tiền cuộn sóng. Hoàng hôn miền Tây tắt hẳn, nhường chỗ cho màn đêm u tối buốt lạnh tràn ngập khắp một vùng sông nước mênh mông.

Tôi đứng dưới bóng một rặng bần ngập mặn ven bến đò ngang, kéo chiếc nón tai bèo sụp xuống che khuất nửa gương mặt phong trần. Dưới chân tôi, một chiếc xuồng ba lá cũ kỹ bằng gỗ sao không gắn máy đang dập dềnh theo từng đợt sóng phù sa đỏ quạch.

Tôi cởi bỏ chiếc bao tải dứa ngụy trang, rút thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao giắt chặt vào thắt lưng da bên trong chiếc áo bà ba màu xanh đen.

Khác với những chuyến tác chiến trước đây, lần này trong thức hải của tôi không còn tiếng nói chỉ dẫn quen thuộc của Lâm Tịch. Đài sen ngọc bích vẫn thu nhỏ lại bằng lòng bàn tay, chìm sâu trong giấc ngủ tĩnh dưỡng miên man. Nhưng thay vì hoang mang, lồng ngực tôi lúc này lại tràn ngập một sự tĩnh lặng kiên định tột cùng.

Ba mươi ba đốt sống lưng tủy ngọc của tôi khẽ rung động nhịp nhàng. Cảnh giới Luyện Cốt Hậu kỳ Cùng Cực mang lại cho tôi một cảm giác thấu triệt kỳ diệu về nhục thân và thế giới tự nhiên xung quanh.

Tôi bước xuống xuồng ba lá, cầm lấy chiếc dầm gỗ mun.

Không cần nổ máy, không cần động cơ, tôi vận chuyển tuyệt kỹ Kính Kình của Thể Đạo truyền thẳng xuống cổ tay và lưỡi dầm. Mỗi nhát chèo của tôi cắm sâu vào dòng nước cuộn trào đều êm ru không một tiếng động, nhưng kình lực đẩy chiếc xuồng lao đi vun vút tựa một mũi tên đen xé toạc màn mưa đêm.

Mục tiêu của tôi nằm cách bờ gần một cây số về phía hạ lưu: **Cồn Trấn Ba**.

Đó là một cồn cát nổi hình đầu rùa khổng lồ đã tồn tại hàng trăm năm giữa dòng sông Tiền, bốn bề bao bọc bởi những vạt bần ngập mặn và lau sậy rậm rạp cao quá đầu người.

Theo những tài liệu khảo sát địa tầng cổ mà tôi từng tiếp cận tại cơ quan, từ đầu thế kỷ mười chín, các bậc tiền nhân triều Nguyễn đã chọn doi đất cao nhất của cồn cát này để xây dựng **Cổ Miếu Trấn Ba** nhằm trấn áp thủy quái và bình ổn sóng gió cho các đoàn thuyền buôn phương Nam. Nhưng trong lăng kính của Thủ Hộ Nhất Mạch, nơi đây chính là nơi đặt **cọc tiêu thứ chín** của mạng lưới Thủy Môn Thập Nhị Tiêu!

Khi chiếc xuồng của tôi áp sát mép bãi bồi phía đông bắc Cồn Trấn Ba, tiếng máy nổ cơ giới trầm đục từ phía đỉnh cồn bắt đầu dội vào màng nhĩ tôi.

Những luồng ánh sáng đèn pha công suất lớn màu vàng rực quét loang loáng qua những ngọn cây bần, soi rõ một chiếc sà-lan mini bọc thép và hai chiếc ca-nô cao tốc đang neo chặt vào chân kè đá của cổ miếu.

Tôi lướt xuồng vào sâu trong một lùm cây bần ngập nước, dùng dây dù buộc chặt mũi xuồng vào gốc cây rồi nhẹ nhàng trườn lên bãi cát ẩm ướt.

Ẩn mình sau những khóm lau sậy rậm rạp, tôi quan sát toàn cảnh hiện trường.

Khoảng sân gạch rêu phong trước Cổ Miếu Trấn Ba lúc này đã bị hơn mười gã đàn ông lực lưỡng chiếm giữ. Chúng mặc đồng phục bảo hộ lao động màu xám tro của Tập đoàn Cửu Long Thiên Hải, mang theo gậy điện, xà beng hợp kim và máy cắt đá cao tần.

Ở trung tâm khoảng sân, ngay trước bậc tam cấp của ngôi miếu cổ, một khối cự thạch đen nhánh sừng sững hiện ra dưới ánh đèn pha rực rỡ.

Đó chính là pho tượng rùa đá ngàn năm: **Trấn Ba Thạch Quy**!

Tượng rùa đá nguyên khối dài hơn ba mét, toàn thân khắc đầy những hoa văn hình sóng nước và ký tự cổ của tiền nhân phương Nam. Trên lưng rùa cõng một tấm bia sa thạch cổ kính cao hai mét rưỡi. Dưới bụng của pho tượng rùa đá là một khe nứt địa tầng tự nhiên ăn sâu vào lòng móng đá bazan đáy sông — nơi luồng từ trường 0.12 Hz đang phát xuất từng đợt sóng xung kích vô hình dội ngược lên không gian!

Đứng cạnh pho tượng rùa đá là một gã đàn ông trung niên vạm vỡ, cao gần một mét tám, cởi trần để lộ phần thân trên cuồn cuộn cơ bắp màu xám xịt ánh kim loại.

Hắn chính là **Trần Bảy**, biệt danh **Bảy Thép** — thủ lĩnh phân đà miền Tây của Cửu Long Thiên Hải, một kẻ nổi danh tàn độc với môn công phu Thiết Bì tà đạo!

Trên tay Trần Bảy cầm một chiếc la bàn phong thủy bằng đồng đen đang xoay tít. Hắn nhìn chằm chằm vào khe nứt dưới bụng rùa đá, gầm gừ ra lệnh cho đám thuộc hạ:

"Mau dựng giàn kích thủy lực lên! Lão Lôi bên Chứa Chan bị sa lưới rồi, tổng bộ vừa phát lệnh khẩn cấp yêu cầu chúng ta phải phá vỡ liên kết cọc tiêu thứ chín này trước nửa đêm! Chỉ cần dùng mũi khoan kim cương kết hợp trận bàn phong tỏa bẻ gãy mai rùa đá, mạch trọc khí dưới đáy sông Tiền sẽ bùng nổ, cuốn trôi toàn bộ mạng lưới đê kè cù lao!"

Nghe những lời độc địa ấy, lồng ngực tôi bốc lên một ngọn lửa phẫn nộ ngút trời.

Chúng không chỉ muốn phá hủy cọc tiêu của tiền nhân, mà còn toan tính dìm hàng vạn người dân vô tội của quê hương tôi vào thảm cảnh ngập lụt sạt lở!

Bàn tay tôi siết chặt chuôi Hắc Thiết Đoản Côn. Khí huyết sôi trào, ba mươi ba đốt sống lưng tủy ngọc mở toang kinh mạch, sẵn sàng cho một trận huyết chiến rực lửa giữa màn mưa sông nước!'''

ACT2 = '''Sáu giờ mười lăm phút tối.

Gió sông Tiền thổi thốc qua Cồn Trấn Ba, mang theo những đợt mưa rào quất rát rạt vào mái ngói âm dương rêu phong của ngôi miếu cổ.

Hai tên công nhân của Cửu Long Thiên Hải đang hì hục khiêng chiếc đầu mũi khoan thủy lực nặng hơn tám mươi ký tiến lại gần khe nứt dưới mai rùa đá Trấn Ba.

Ngay tại thời khắc then chốt ấy, tôi không do dự thêm một phần nghìn giây nào nữa.

Đạp mạnh chân vào cồn cát ẩm ướt, kình lực Luyện Cốt Hậu kỳ Cùng Cực bộc phát toàn diện!

Thân hình tôi vọt ra khỏi rặng lau sậy như một bóng ma đen nhánh xé toạc màn mưa. Thanh Hắc Thiết Đoản Côn trong tay tôi vẽ nên một đường cung tròn đen nhánh ánh chu sa đỏ rực, xé gió quét ngang một đòn sấm sét!

*BỐP! BỐP!*

Hai tiếng va đập giòn giã vang lên nối tiếp nhau.

Đầu côn bọc da bò đập chuẩn xác vào khớp khuỷu tay của hai tên công nhân khiêng máy khoan. Kình lực Thuần Dương xuyên thấu qua lớp cơ bắp khiến hai cánh tay của chúng tê dại hoàn toàn, buông rơi chiếc đầu khoan thủy lực xuống sàn gạch cổ phát ra một tiếng *RẦM* chấn động.

"Kẻ nào?!"

Trần Bảy giật mình quay phắt lại. Ánh mắt hắn lóe lên tia hung quang dữ tợn như một con thú dữ săn mồi giữa đêm đen.

Nhìn thấy một thanh niên trẻ tuổi mặc áo bà ba thô kệch, cầm thanh đoản côn đen nhánh đứng sừng sững chắn trước bệ đá Thần Quy, Trần Bảy gằn giọng cười khẩy:

"Hóa ra là mày! Thằng kỹ sư trần tục Nguyễn Minh An! Mày dám một mình mò ra tận cồn cát này nộp mạng sao?"

Hắn không hề nói thêm nửa lời vô ích. Với bản tính của một kẻ tà tu dạn dày thực chiến, Trần Bảy vung hai cánh tay xám xịt ánh kim loại, rút phắt đôi đoản chùy bằng thép đúc nặng mỗi chiếc mười lăm ký giắt sau lưng, lao vút tới như một cỗ xe tăng bọc thép!

*VÙ!*

Cặp thiết chùy mang theo tiếng gió rít kinh hồn bạt vía, giáng thẳng xuống đầu và ngực tôi!

Kình lực Thiết Bì tà môn của Trần Bảy quả thực thô bạo và hung hãn tột cùng. Sức nặng của đôi thiết chùy kết hợp với quán tính lao tới đủ sức đập nát một khối bê tông cốt thép trong chớp mắt.

Nhưng tôi không hề nao núng lùi bước.

Tôi không đối đầu cứng nhắc bằng cách giơ côn đỡ trực diện. Trong lăng kính của Thể Đạo, sự cứng cỏi của Luyện Cốt Hậu kỳ Cùng Cực không phải là sự bất động vô tri của sắt đá, mà là sự dẻo dai linh hoạt tựa dòng phù sa sông nước!

Ngay khi ngọn thiết chùy bên phải vừa lao tới cách lồng ngực tôi nửa gang tay, tôi vận hành bộ pháp Du Thân Bộ, nghiêng người né sang một góc ba mươi độ.

Ngọn chùy chém hụt, đập sầm xuống mặt sân gạch cổ, làm vỡ toang một mảng gạch tàu nứt toác thành hình mạng nhện!

Chớp lấy khoảnh khắc trọng tâm của Trần Bảy bị nghiêng về phía trước, thân hình tôi xoay tròn nửa vòng trên một gót chân, mượn chính luồng gió cuốn của ngọn chùy địch để gia tăng tốc độ cho đòn phản công.

Thanh Hắc Thiết Đoản Côn trong tay tôi rung lên một tiếng ngân trong trẻo, mang theo toàn bộ kình lực tích tụ từ ba mươi ba đốt sống tủy ngọc, giáng thẳng vào khớp cổ tay phải của hắn!

*KENG!*

Một tiếng va chạm chói tai như tiếng cồng đồng nổ tung giữa màn đêm.

Lớp da màu xám xịt Thiết Bì trên cổ tay Trần Bảy bị kình lực Thuần Dương phá vỡ một mảng lớn. Cơn chấn động khủng khiếp khiến các ngón tay thô ráp của hắn run rẩy dữ dội, chiếc thiết chùy bên phải văng tuột khỏi tay, rơi cắm ngập xuống bãi cát ven bờ!

"Thằng khốn kiếp!"

Trần Bảy gầm lên một tiếng điên dại. Đôi mắt hắn đỏ ngầu tơ máu. Hắn vứt bỏ luôn chiếc thiết chùy còn lại, hai bàn tay xòe ra thành hình ưng trảo, toàn bộ lớp da trên ngực và cổ hắn nổi gồ ghề những đường gân xanh đen tà ác.

Hắn dồn toàn bộ tà khí Thiết Bì vào hai cánh tay, chộp thẳng vào yết hầu và thái dương tôi nhằm xé nát đầu tôi thành từng mảnh vụn!

"Chết đi cho tao!"

Đối mặt với đòn liều mạng tàn độc của đối thủ, ánh mắt tôi vẫn lạnh lùng và tĩnh lặng như mặt hồ đóng băng.

Tôi hít sâu một hơi, vận hành Quy Tức Cùng Cực. Nhịp tim tôi chậm lại ba mươi lăm nhịp một phút, nhưng dòng Thuần Dương Cương Huyết trong lồng ngực lại cuộn trào bỏng rát như dung nham núi lửa.

Tôi bước chéo một bước về phía trước, hạ thấp trọng tâm, luồn thẳng vào khoảng trống nách trái của Trần Bảy.

"Thể Đạo Phá Cương — Kình Quán Ngọc Tủy!"

Tôi hét lớn một tiếng trầm đục, hữu quyền siết chặt như một thỏi thép nguội tôi trong lò rèn, đấm thẳng vào huyệt Đản Trung ngay giữa lồng ngực hắn!

*ÙNG!*

Một tiếng nổ trầm đục vang lên tựa như tiếng sấm sét nổ tung trong lòng đất.

Kình lực Thuần Dương thuần khiết của ba mươi ba đốt sống tủy ngọc bộc phát toàn diện, xuyên thấu qua lớp cơ bắp dày cộm, phá tan nát toàn bộ mạng lưới gân cốt Thiết Bì tà môn của Trần Bảy!

*PHỤT!*

Trần Bảy há hốc mồm phun ra một ngụm máu đen bầm tím. Đôi mắt hắn trợn trừng kinh hãi, không thể tin nổi lớp Thiết Bì tu luyện hơn hai mươi năm của mình lại bị một phàm nhân dùng một đấm phá tan tành!

Kình lực phản chấn cực đại đánh bạt thân hình nặng gần một trăm ký của hắn bay ngược ra sau hơn bảy mét, đập mạnh vào bức tường gạch cổ của miếu rồi ngã sụp xuống như một bao tải trấu rách!

Đám thuộc hạ xung quanh nhìn thấy thủ lĩnh Thiết Bì bất bại bị hạ gục chỉ sau vài hiệp đấu thì kinh hoàng bạt vía.

Mấy tên định rút vũ khí lao vào thì thanh Hắc Thiết Đoản Côn trong tay tôi đã quét ngang thành một vòng tròn rực lửa. Đầu côn điểm liên hoàn vào các huyệt đạo trọng yếu, đánh gãy sức kháng cự của bốn tên hung hãn nhất chỉ trong vòng mười giây. Những tên còn lại hoảng loạn vứt bỏ xà beng và máy móc, nhảy xuống ca-nô cao tốc nổ máy tháo chạy thảm hại về phía hạ lưu sông Tiền!

Hiện trường sân miếu lúc này chỉ còn lại tiếng mưa rơi rả rích và tiếng rên rỉ bất lực của Trần Bảy đang nằm sõng soài dưới chân tường đá.'''

ACT3 = '''Tám giờ tối.

Màn mưa trên Cồn Trấn Ba dần dần ngớt hạt. Gió sông Tiền thổi lồng lộng qua những tán bần ngập mặn, mang theo hơi thở mát lạnh của đất trời sau cơn giông tố.

Trần Bảy nằm tựa lưng vào tường miếu, miệng không ngừng ộc ra từng ngụm máu bầm. Lớp da màu xám xịt kim loại trên người hắn đã hoàn toàn nhạt màu, lộ ra làn da trắng bệch tiều tụy của kẻ vừa bị phế sạch toàn bộ công phu tà đạo.

Đôi mắt hắn nhìn tôi chằm chằm, tràn đầy sự sợ hãi và thảng thốt:

"Mày... mày không dùng bùa chú, không dùng pháp bảo... Tại sao một phàm nhân nhục nhãn lại có thể sở hữu kình lực Thuần Dương kinh khủng đến mức nghiền nát Thiết Bì của tao? Mày rốt cuộc là truyền nhân của môn phái nào?"

Tôi không buồn trả lời câu hỏi vô nghĩa của hắn.

Tôi dùng dây thừng dù quân dụng trói chặt Trần Bảy cùng bốn tên tay sai bị tê liệt lại thành một xâu, kéo chúng vào một gian nhà kho cất giữ ngư cụ của miếu cổ để bảo đảm an toàn.

Sau đó, tôi tịch thu chiếc máy tính bảng quân sự chuyên dụng và toàn bộ điện thoại liên lạc của Trần Bảy.

Bước lại trước bậc tam cấp của Cổ Miếu Trấn Ba, tôi đứng đối diện với pho tượng **Trấn Ba Thạch Quy**.

Pho tượng rùa đá ngàn năm cõng tấm bia sa thạch rêu phong vẫn đứng sừng sững ở đó. Nhưng dưới bụng rùa đá, khe nứt địa tầng tự nhiên đang bốc lên từng làn khói xám mờ mịt mang theo mùi tanh nồng của âm trọc khí — tàn dư của trận bàn phong tỏa tà môn mà đám người Trần Bảy vừa kích hoạt.

Dưới đáy sâu của dòng sông Tiền, tiếng gầm gừ đục ngầu của mạch nước ngầm đang dao động dữ dội, khiến cả cồn cát khẽ rung chuyển từng cơn.

Thời gian không thể chần chừ!

Tôi tra thanh Hắc Thiết Đoản Côn vào nẹp lưng, rút thanh **Trấn Thủy Đoản Đao** đen nhánh ánh vân thép damascus ra khỏi bao da.

Ngồi xếp bằng trước mai rùa đá, tôi nhắm mắt vận hành Quy Tức Cùng Cực.

Ba mươi ba đốt sống lưng tủy ngọc của tôi phát xuất một chuỗi âm thanh giòn giã tựa ngọc thạch va đập. Từ sâu trong cuống tim, dòng Thuần Dương Cương Huyết sôi trào, dồn thẳng xuống đầu ngón tay trỏ bàn tay phải.

Tôi rạch nhẹ đầu ngón tay, điểm ba giọt máu tươi đỏ thẫm ánh kim sắc lên rãnh hoa văn cổ trên đỉnh đầu rùa đá Trấn Ba, đồng thời cắm thẳng mũi Trấn Thủy Đoản Đao vào trung tâm khe nứt địa tầng!

*ÙNG... ÙNG...*

Một luồng quang hoa màu hoàng kim rực rỡ bỗng bùng nổ từ lưng pho tượng rùa đá!

Dòng Thuần Dương Cương Huyết của tôi tựa như một ngọn lửa thiêu đốt toàn bộ âm trọc khí tích tụ trong lòng đá. Dưới mũi Trấn Thủy Đoản Đao, cấu trúc sa thạch cổ xưa của tấm bia đá trên lưng rùa bắt đầu tỏa ra những đường vân ánh sáng màu lam ngọc tuyệt mỹ, vẽ nên đồ hình Thủy Môn Thập Nhị Tiêu cổ xưa của tiền nhân phương Nam.

Từng luồng kình lực trấn thủy uy nghiêm tràn xuống đáy sâu của dòng sông Tiền.

Những xoáy nước ngầm hung hãn dưới lòng sông dần dần dịu lại, hòa quyện hoàn toàn vào dòng chảy phù sa màu mỡ. Pho tượng rùa đá khẽ phát ra một tiếng thở rền trầm hùng như một vị hộ thần viễn cổ vừa được đánh thức sau hàng thế kỷ say ngủ.

Màng phong ấn ánh lam ngọc bọc kín toàn bộ Cồn Trấn Ba rồi từ từ thu liễm, chìm sâu vào lòng mạch địa tầng sông nước.

**Cọc tiêu thứ chín — Trấn Ba Thạch Quy — đã chính thức an định tuyệt đối!**

Chín trên mười hai cọc tiêu của mạng lưới Thủy Môn Thập Nhị Tiêu phương Nam đã được phong tỏa vững chắc tựa bàn thạch!

Tôi rút thanh Trấn Thủy Đoản Đao ra, lau sạch vết máu rồi tra vào bao da. Toàn thân tôi tuy thấm mệt sau một ngày dài bôn ba và huyết chiến, nhưng tinh thần lại sảng khoái và thanh thản chưa từng có.

Tôi mở chiếc máy tính bảng quân sự của Trần Bảy ra, nhập chuỗi khóa giải mã cơ bản của các kỹ sư địa chất.

Màn hình kỹ thuật số sáng lên, hiển thị một tấm bản đồ trắc địa vệ tinh bao trùm toàn bộ dải đất phương Nam.

Trên bản đồ, chín cọc tiêu đã chuyển sang màu xanh lục an định. Nhưng ở góc phía nam của bản đồ, ba điểm nút màu đỏ thẫm nhấp nháy liên tục cùng các thông số địa chấn nguy cấp:

* **Cọc tiêu thứ mười**: Rừng ngập mặn Cần Giờ & Cửa biển Soài Rạp.
* **Cọc tiêu thứ mười một**: Cửa biển Ba Lai & Cổ Chiên (Bến Tre - Trà Vinh).
* **Cọc tiêu thứ mười hai (Trận Nhãn Tối Cao)**: Vùng đầm lầy U Minh Hạ & Mũi Cà Mau!

Ba cọc tiêu cuối cùng này chính là "Cửa Biển Tam Môn" — then cài then chốt nhất khóa chặt toàn bộ dòng khí huyết đại dương của Trái Đất!

Tôi sao lưu toàn bộ tập dữ liệu tọa độ vào chiếc thẻ nhớ bảo mật, rồi dùng kìm phá hủy hoàn toàn bo mạch của chiếc máy tính bảng.

Sau đó, tôi dùng điện thoại vệ tinh nặc danh gửi một thông điệp tọa độ ngắn gọn cho Đồn Biên phòng Cửa khẩu Cảng Tiền Giang và Lực lượng Cảnh sát Giao thông đường thủy:

*"Cồn Trấn Ba: Bắt giữ nhóm đối tượng mang danh nghĩa doanh nghiệp tàng trữ vũ khí và thiết bị thăm dò khoáng sản trái phép xâm hại di tích cổ. Đề nghị tiếp quản hiện trường."*

Làm xong mọi việc, tôi khoác chiếc ba lô dã chiến lên vai, bước ra khỏi sân miếu cổ.

Chín giờ ba mươi phút đêm.

Mưa đã tạnh hẳn. Bầu trời đêm trên dòng sông Tiền quang đãng, để lộ những vì sao lấp lánh như dát bạc trên nền nhung đen thẫm.

Tôi đứng trên doi cát đầu mũi Cồn Trấn Ba, phóng tầm mắt nhìn về bờ cù lao xa xa.

Phía bên kia bờ sông, ánh đèn vàng ấm áp từ những căn nhà lá ven rạch Cây Me vẫn đang tỏa sáng êm đềm giữa màn đêm tĩnh lặng. Ở nơi đó, người mẹ già tóc bạc của tôi đang chìm vào giấc ngủ yên bình trong căn nhà tranh đơn sơ, không còn phải lo sợ trước nanh vu tộc tà ác của kẻ thù.

Cơn gió sông Tiền thổi lồng lộng làm tung bay tà áo bà ba của tôi, mang theo hương thơm nồng nàn của đất phù sa và hoa bưởi nở muộn.

Tôi mỉm cười, một nụ cười nhẹ nhõm và thanh thản hiếm hoi kể từ ngày bước chân vào con đường Thể Đạo cô độc.

Mẹ tôi đã bình yên. Quê hương tôi đã an định.

Và chặng đường phía trước của một kẻ thủ hộ phàm nhân — hướng về ba cọc tiêu tối hậu nơi biển trời phương Nam — đang vẫy gọi tôi bằng những ngọn sóng cuộn trào của bình minh rạng rỡ!'''

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
        "Huyết Chiến Cổ Miếu, Đả Bại Thiết Bì & An Định Cọc Tiêu Thứ Chín Trấn Ba Thạch Quy",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:30:00+07:00",
        CHAPTER_NUM,
        "loc_con_tran_ba_song_tien",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An chèo xuồng ba lá trong đêm mưa vượt sóng sông Tiền tiếp cận Cồn Trấn Ba. Phát hiện Trần Bảy (Bảy Thép) và nhóm tà tu Cửu Long Thiên Hải đang dùng máy cắt đá và trận bàn tà đạo mưu toan phá hủy Trấn Ba Thạch Quy. Minh An xuất kích bằng Hắc Thiết Đoản Côn và kình lực Thuần Dương Luyện Cốt Hậu kỳ Cùng Cực, phá vỡ công phu Thiết Bì của Trần Bảy, chế ngự toán tay sai. Dùng Thuần Dương Cương Huyết và Trấn Thủy Đoản Đao thanh tẩy tà khí ô trọc, an định hoàn toàn cọc tiêu thứ chín Thần Quy Trấn Ba (9/12 cọc tiêu). Giải mã bản đồ trắc địa thu được của địch, xác định tọa độ 3 cọc tiêu cuối cùng tại Cửa Biển Tam Môn.",
        "Cọc tiêu thứ chín Trấn Ba Thạch Quy an định tuyệt đối; Trần Bảy bị phế tà công và bắt giữ; 9/12 cọc tiêu Thủy Môn hoàn tất; giải mã tọa độ 3 cọc tiêu cuối cùng."
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
        "Cọc tiêu thứ chín Trấn Ba Thạch Quy tại sông Tiền đã an định tuyệt đối; 9/12 cọc tiêu Thủy Môn đã giải quyết; giải mã tọa độ 3 cọc tiêu cuối cùng tại Cửa Biển Tam Môn."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An vận dụng hoàn hảo Luyện Cốt Hậu kỳ Cùng Cực phá tan Thiết Bì tà công; thể phách vững như bàn thạch sẵn sàng cho giai đoạn Hoán Huyết."
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
        inv_data["current_location"] = "Cồn Trấn Ba, Sông Tiền, Tỉnh Tiền Giang"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ Cùng Cực (33 Đốt Sống Ngọc Tủy Viên Mãn / Chuẩn Bị Hoán Huyết)"

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

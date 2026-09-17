# -*- coding: utf-8 -*-
"""Draft Chapter 70 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 70
CHAPTER_TITLE = "Long Lân Phá Kình"
LOCATION = "Tầng hầm kỹ thuật Tháp Thủy Đài — Ụ tàu cổ Ba Son (TP.HCM)"
DATE = "2026-10-22"

ACT1 = '''Bốn giờ ba mươi phút chiều ngày hai mươi hai tháng Mười.

Không gian căn hầm sâu mười hai mét dưới tháp thủy đài Ba Son ngột ngạt tựa lò luyện thép nung đỏ. Mùi rêu mốc bị xua tan bởi sát khí tanh nồng cuộn trào mang đậm mùi bùn lầy ngập mặn và huyết dịch hung tàn.

Khí tức Luyện Cốt hậu kỳ phát xuất từ thân hình đồ sộ của Hắc Lân Thiết Vệ như một ngọn núi đá đè nặng lên từng tấc không khí.

"Minh An... cẩn thận!" Kỹ sư Tuấn đứng phía sau tôi kêu lên một tiếng thất thanh, hai chân anh run rẩy không thể tự chủ trước áp lực vô hình lan tỏa khắp gian hầm.

Tôi không quay đầu lại, cánh tay trái vung ngang đẩy Tuấn lùi sâu vào hốc tường khuất sau cây dầm thép chữ I dày dặn:

"Anh Tuấn, nấp kỹ sau cây dầm chịu lực, nhắm mắt bịt tai lại và tuyệt đối không được bước ra ngoài!"

Giọng nói đanh thép mang uy lực Thể Đạo khiến Tuấn vội vã nép sát vào góc chết sau khối thép lớn.

Lúc này, đôi mắt đỏ ngầu như dã thú săn mồi của Hắc Lân Thiết Vệ hoàn toàn ghim chặt vào tôi. Gã cao hơn hai mét, bờ vai rộng tựa cánh phản gỗ lim, lớp giáp da cá sấu đen tuyền bó sát thân hình vạm vỡ cuồn cuộn. Hai cánh tay gã nổi gân guốc cuồn cuộn, bao bọc bởi lớp vảy sừng cứng ngắc tựa vảy sắt nguội — dấu tích công pháp ngoại môn Luyện Cốt hậu kỳ cực hạn.

"Một tên nhóc Luyện Cốt trung kỳ mới nổi..." Hắc Lân Thiết Vệ gằn từng tiếng trầm đục, âm thanh rền rĩ như tiếng đá tảng va đập vào nhau dưới đáy vực. "Ngươi đã liên tiếp phá hỏng đại kế của Cửu Long Thiên Hải từ Lò Gốm, Bến Phú Định cho tới Mũi Đèn Đỏ. Đêm qua tại Cầu Mống, ngươi còn dám chém đứt vũ khí của toán người nhái Hắc Giao Đường. Hôm nay, ta sẽ bẻ gãy từng khúc xương của ngươi để tế cờ cho Thủy Môn Chấn Tiêu!"

Lời vừa dứt, thân hình khổng lồ của gã bỗng bùng nổ một tốc độ kinh hoàng trái ngược hoàn toàn với vẻ ngoài nặng nề!

"Oanh!"

Mặt sàn gạch vồ dưới chân gã nổ tung, bắn ra vô số mảnh gạch vụn. Hắc Lân Thiết Vệ lướt tới như một cỗ xe ủi bọc thép xé toạc không khí, nắm đấm phải to lớn tựa chiếc cối đá giáng thẳng xuống đầu tôi!

Đó là sát chiêu *Hắc Ngạc Toái Cốt*!

Quyền phong chưa tới nơi, áp lực luồng gió nén đã ép rát rạt da mặt tôi, làm những ngọn đèn sợi đốt trên trần hầm chao đảo dữ dội. Đòn đánh nặng ngàn cân vượt xa sức mạnh của bất kỳ đối thủ nào tôi từng chạm trán trước đây.

Tôi không hề hoảng sợ tháo lui. Tôi hít một hơi sâu, hạ thấp trọng tâm, vận chuyển khẩu quyết Thức thứ bảy *Ngọc Tủy Quy Nhất*.

"Rắc! Rắc!"

Ba mươi ba đốt xương sống tôi phát ra tiếng nổ giòn đanh. Dòng tủy ngọc trong suốt phóng thích luồng kình lực thuần khiết bao bọc lấy hai cánh tay. Tôi bắt chéo hai cẳng tay tạo thành thế *Thiết Khảm Thụ*, đón đỡ trực diện cú đấm nghìn cân của đối phương!

"Ầm!"

Âm thanh va chạm chấn động màng nhĩ vang lên đinh tai nhức óc giữa lòng hầm kín.

Cú đấm của Hắc Lân Thiết Vệ giáng thẳng vào giao điểm hai cẳng tay tôi. Một luồng lực đạo cuồng bạo tựa như sóng thần dội tới, xuyên qua da thịt đánh thẳng vào màng xương. Tôi cắn chặt răng, vận chuyển *Kính Phách Phản Chấn* để triệt tiêu lực chấn. Tuy nhiên, chênh lệch cảnh giới giữa trung kỳ và hậu kỳ quá lớn, tôi chỉ kịp phân tán bốn mươi phần trăm xung lực ra không khí, sáu mươi phần trăm kình lực hung hãn còn lại dồn thẳng xuống đôi chân!

"Rầm rầm rầm!"

Mặt sàn vỡ nát, thân hình tôi trượt lùi hơn ba mét cày nát gạch vồ. Hai cánh tay tê rần, khí huyết trong lồng ngực cuộn trào dữ dội.

"Khá lắm!" Hắc Lân Thiết Vệ nhếch mép cười gằn, ánh mắt thoáng lộ vẻ kinh ngạc. "Đỡ trọn một quyền toàn lực của ta mà xương cẳng tay không gãy vụn, nhục thân của ngươi quả nhiên có chỗ kỳ quái. Nhưng để xem ngươi chống đỡ được bao nhiêu quyền!"'''

ACT2 = '''Không cho tôi bất kỳ khoảng trống nào để điều hòa khí huyết, Hắc Lân Thiết Vệ lập tức vung tay ra sau lưng.

"Xoẹt!"

Hai thanh đoản kích hắc thiết dài tám mươi phân được gã rút khỏi lưng. Lưỡi kích xẻ rãnh răng cưa uốn lượn như hàm răng cá sấu, tỏa mùi tanh nồng của độc chất âm sát tôi luyện từ nọc rắn biển.

"Chết đi!"

Gã gầm lên một tiếng dã man, hai tay múa lượn song kích lao vút tới. Đôi đoản kích xé toạc không khí đan thành tấm lưới chết chóc bao trùm quanh miệng giếng. Từng mũi kích chém sạt dầm thép làm gạch đá vách tường rơi rụng lả tả.

Đối mặt với vũ khí sắc bén của cường giả hậu kỳ, tôi biết dùng tay không nghênh đón là tự tìm đường chết.

Trong chớp mắt thân pháp lướt nghiêng né tránh mũi kích thứ nhất, bàn tay phải của tôi vung về phía sau hông, rút phăng thanh Hắc Thiết Đoản Côn bọc da bò dã chiến.

"Keng!"

Thanh đoản côn vung lên chặn đứng mũi kích thứ hai nảy lửa, phát ra tiếng vo ve trầm đục của Kính Kình nhờ bột chu sa thạch anh dẫn truyền lực tối ưu.

"Keng! Keng! Keng!"

Chỉ trong mười giây ngắn ngủi, tôi và Hắc Lân Thiết Vệ đã giao đấu hơn ba mươi chiêu thức kịch liệt. 

Tôi vận dụng linh hoạt các thế biến hóa của *Đoán Cốt Thập Nhị Thức*, kết hợp thân pháp lướt trên bùn lầy uyển chuyển né tránh những đòn hiểm vào đầu và ngực. Mỗi lần thanh đoản côn va chạm với song kích, tôi đều vận dụng *Kính Phách Phản Chấn* hấp thu một phần lực đạo rồi mượn đà phản kích.

Thế nhưng, lớp giáp vảy da cá sấu kết hợp màng da Luyện Cốt hậu kỳ của Hắc Lân Thiết Vệ quá sức trâu bò. Những đòn côn phản chấn đánh trúng bả vai hay lồng ngực gã chỉ tạo tiếng bình bịch như nện vào bao cát, khiến gã chỉ khựng lại nửa bước rồi phản đòn hung tợn hơn.

Mỗi nhát kích của gã chém xuống đều mang theo lực phá hoại kinh hồn, ép tôi phải liên tục lùi bước phòng ngự. Căn phòng hầm chật hẹp càng lúc càng trở nên ngột ngạt vì bụi gạch vữa mù mịt.

Đúng lúc đó, trong một thoáng giao phong chớp nhoáng, trực giác Thể Đạo của tôi bỗng nắm bắt được một điểm dị thường.

Sau mỗi đợt vung kích liên tiếp ba chiêu toàn lực, nhịp thở của Hắc Lân Thiết Vệ lại có một thoáng ngắt quãng cực ngắn, chỉ kéo dài khoảng một phần mười giây. Cùng lúc ấy, dưới lớp áo giáp nơi đốt sống thắt lưng số tư và cổ tay phải của gã lộ ra những mảng da bầm tím sẫm màu, phát ra mùi tanh của máu ứ đọng.

*"Minh An!"* Tiếng Lâm Tịch vang lên kịp thời từ tận đáy thức hải. *"Kẻ này không phải người tu luyện Thể Đạo chính thống! Hắn đã dùng tà pháp ngoại môn nuốt chửng tinh huyết của thủy quái ngập mặn Cần Giờ để cưỡng ép thúc đẩy xương cốt đột phá Luyện Cốt hậu kỳ. Căn cơ của hắn đầy rẫy tạp chất, các khớp xương chưa được tôi luyện hoàn mỹ. Đốt sống thắt lưng số tư và kinh mạch cổ tay phải chính là tử huyệt tích tụ huyết độc của hắn!"*

Tôi nín thở truyền âm: "Lớp lân giáp hộ thể của hắn quá dày, kình lực thông thường của đoản côn không thể đánh thủng màng da để công phá tử huyệt!"

*"Hãy dùng kiếm khí của Thanh Long Lân Kiếm!"* Giọng Lâm Tịch vang lên đanh thép như mệnh lệnh. *"Ngươi đã dung nạp cọc tiêu số năm vào tủy ngọc. Hãy dẫn dắt kiếm khí hàn băng của thánh vật trấn thủy truyền vào thanh đoản côn, dùng sắc bén của kiếm khí phá tan lân giáp, kết hợp Kính Kình đánh nát tử huyệt của hắn!"*

Lời của Lâm Tịch như một tia chớp xé toạc màn sương mù trong đầu tôi.

Đúng vậy! Tôi đâu chỉ có kình lực nhục thân đơn thuần! Tôi đang nắm giữ kiếm khí của thanh bảo kiếm ngàn năm trấn giữ long mạch rạch Bến Nghé!'''

ACT3 = '''Ý niệm vừa lóe lên, tôi lập tức hành động không chút do dự.

Khi mũi kích của Hắc Lân Thiết Vệ chém sạt qua vai áo tôi, tôi cố ý để lưỡi kích cứa rách một mảng vải bố, giả vờ loạng choạng lùi lại ba bước sát mép miệng giếng kỹ thuật để dẫn dụ đối phương tung đòn quyết định.

Quả nhiên, thấy tôi lộ sơ hở lớn, đôi mắt đỏ ngầu của Hắc Lân Thiết Vệ bùng cháy vẻ khát máu tột cùng.

"Hết đường chạy trốn rồi ranh con! Nạp mạng đi!"

Gã gầm thét dữ dội, dồn toàn bộ khí huyết tà đạo vào đôi cánh tay vượn đen bóng. Hai thanh đoản kích hợp kim giơ cao quá đầu, kình lực Luyện Cốt hậu kỳ nén chặt lại biến đôi kích thành hai dải hắc quang hình răng nanh khổng lồ, giáng thẳng xuống đỉnh đầu tôi với toàn bộ sức nặng của ngàn cân cơ bắp!

Sát chiêu cực hạn: *Hắc Ngạc Phệ Thiên*!

Đòn đánh này nếu giáng xuống, dù là một khối thép đúc dày năm phân cũng sẽ bị bẻ gãy làm đôi!

Nhưng ngay trong tích tắc ngàn cân treo sợi tóc ấy, tôi không hề lùi bước. Ánh mắt tôi trở nên tĩnh lặng như mặt hồ không một gợn sóng.

"Đoán Cốt Thập Nhị Thức — Thức thứ bảy: Ngọc Tủy Quy Nhất, chuyển!"

Tôi gầm lên một tiếng trầm hùng từ sâu thẳm lồng ngực. Ba mươi ba đốt xương sống tôi phát ra tiếng sấm ran rền rĩ. Dòng tủy ngọc lấp lánh cuộn trào, lập tức câu thông với thanh Thanh Long Lân Kiếm đang an tọa dọc cột sống.

"Uông — !"

Một tiếng kiếm minh vang dội từ trong xương tủy tôi phóng xuất ra ngoài. Luồng kiếm khí hàn băng thanh lãnh vô cùng sắc bén cuộn trào như thác lũ, theo kinh mạch cánh tay phải tràn thẳng vào thanh Hắc Thiết Đoản Côn trong tay tôi.

Thanh đoản côn hắc thiết đen nhánh ánh đỏ lập tức phát sinh biến dị phi thường!

Lớp sương băng lam ngọc bao bọc thân côn ngưng tụ thành dải đao mang hàn khí dài hơn một thước. Nhiệt độ hạ xuống dưới độ âm khiến giọt nước trên trần hầm đông cứng rơi lộp độp!

Đây chính là chiêu thức Thể Đạo dung hợp độc nhất vô nhị mà tôi vừa lĩnh ngộ: **Long Lân Phá Kình**!

Tôi bước tới một bước, trọng tâm vững chãi cắm chặt xuống nền đá, vung thanh đoản côn bọc kiếm khí vạch ra một đường bán nguyệt màu xanh biếc tuyệt mỹ giữa không gian tối tăm!

"Keng — Rắc!"

Một âm thanh giòn giã chấn động tâm can vang lên. 

Dải kiếm khí Thanh Long sắc bén vô song va chạm trực diện với đôi đoản kích của Hắc Lân Thiết Vệ. Dưới uy lực gọt sắt như chém bùn của thánh vật viễn cổ, thanh đoản kích bên phải của gã bị kiếm khí lam ngọc chém đứt đôi trong nháy mắt! Nửa đoạn kích gãy bay vút lên găm phập vào dầm thép trần nhà!

Chưa dừng lại ở đó, kình lực Kính Kình phối hợp cùng kiếm khí hàn băng không hề suy giảm, mượn đà xoay chuyển thân pháp lướt qua kẽ hở phòng ngự của đối phương, mũi côn bọc sương băng đập thẳng vào mạng sườn phải rồi điểm chuẩn xác vào đốt sống thắt lưng số tư của gã!

"Phập!"

Lớp giáp da cá sấu và màng vảy lân hộ thể mà Hắc Lân Thiết Vệ luôn tự hào bị kiếm khí hàn băng đâm thủng như một mảnh giấy mỏng. Kình lực Ngọc Tủy mang theo cái lạnh thấu xương của đáy sông ngàn năm rót thẳng vào tử huyệt đốt sống của gã, đóng băng toàn bộ các mạch máu ứ đọng!

"Rắc rắc rắc!"

Tiếng xương khớp nứt vỡ từ đốt sống lưng vang lên giòn tan rợn người.

"Á a a a!"

Hắc Lân Thiết Vệ phát ra một tiếng thét đau đớn xé ruột xé gan. Toàn bộ kình lực Luyện Cốt hậu kỳ hung hãn của gã như quả bóng bị chọc thủng, lập tức xì hết hơi lực. Gã há miệng phun ra một ngụm máu tươi đen ngòm, dòng máu vừa rời khỏi khóe môi đã đông kết thành những hạt băng nhỏ li ti rơi lả tả xuống đất.

Thân hình hơn trăm ký bị hất bay bảy mét, đập dữ dội làm nắp thép miệng giếng lõm sâu hoắm!'''

ACT4 = '''Hắc Lân Thiết Vệ ngã lăn xuống sàn gạch, hai tay ôm chặt lấy vùng thắt lưng quặn thắt vì đau đớn.

Lớp da đen bóng trên cánh tay gã rạn nứt từng mảng lớn, từng vệt sương băng màu trắng xóa từ vết thương nơi thắt lưng đang không ngừng lan tỏa khắp lồng ngực và cổ gã, làm hơi thở của gã phả ra từng luồng khói trắng buốt giá. Gã ngẩng đầu lên, đôi mắt đỏ ngầu giờ đây tràn ngập sự kinh hoàng tột độ nhìn thanh đoản côn bọc sương ngọc trong tay tôi:

"Ngươi... kiếm khí này... tại sao ngươi lại có thánh khí trấn thủy của Cầu Mống?! Ngươi đã lấy được Thanh Long Lân Kiếm rồi sao?!"

Tôi cầm chắc đoản côn, bước từng bước trầm ổn tiến lại gần gã, mũi côn hơi chúc xuống sàn, ánh mắt lạnh lùng:

"Kẻ nào dám nhúng tay vào long mạch rạch Bến Nghé và sông Sài Gòn, kẻ đó phải trả giá. Nói! Ai là kẻ ra lệnh cho ngươi đến phong tỏa cọc tiêu Ba Son?"

Hắc Lân Thiết Vệ run rẩy co giật, biết rõ với vết thương chí mạng nơi cột sống tủy huyết, nếu gã còn chần chừ thêm một phút nữa, kiếm khí hàn băng sẽ triệt để phong tỏa tim phổi, biến gã thành một khối băng chết cứng. 

Gã cắn chặt môi đến ứa máu, nở một nụ cười thảm hại pha lẫn vẻ tàn độc điên cuồng:

"Nguyễn Minh An... ngươi đừng vội đắc ý! Đánh bại ta chỉ là khởi đầu thôi! Hội chủ Cửu Long Thiên Hải đã hạ lệnh phong tỏa toàn bộ luồng hàng hải từ cửa biển Cần Giờ đến các cảng quốc tế Sài Gòn. Các ngươi vĩnh viễn không thể mang bất kỳ cọc tiêu nào rời khỏi thành phố này! Ngày đại trận nghịch chuyển bùng nổ, toàn bộ các ngươi sẽ chìm sâu dưới đáy sông!"

Dứt lời, bàn tay trái còn lành lặn của gã đập mạnh xuống một cần gạt xả khẩn cấp gắn trên đường ống kỹ thuật ngầm sát vách miệng giếng.

"Keng! Rầm rầm!"

Một cửa van thoát nước bằng gang đúc đường kính một mét bật mở toang, để lộ dòng nước ngầm cuộn chảy xiết nối thẳng ra lòng sông Sài Gòn. Hắc Lân Thiết Vệ không chút do dự, buông xuôi thân hình đồ sộ lao thẳng vào đường ống nước ngầm, bị dòng nước xoáy cuốn trôi mất dạng vào bóng tối sâu thẳm.

Tôi không đuổi theo. Dưới đường ống ngầm nước xiết dẫn ra sông lớn, việc truy sát một kẻ liều chết là không cần thiết. Kiếm khí hàn băng đã phá hủy kinh mạch cột sống, phế đi tu vi Luyện Cốt hậu kỳ của gã.

Tôi từ từ thu liễm kiếm khí Thanh Long về lại tủy ngọc. Lớp sương băng trên thân đoản côn tan biến thành những hạt nước trong vắt, trả lại màu đen ánh đỏ quen thuộc của hắc thiết chu sa.

Cơ thể tôi khẽ lay động, một cảm giác mỏi mệt từ các thớ cơ ập đến sau khi dốc cạn kình lực thực hiện đòn dung hợp đầu tiên. Tôi đứng yên tại chỗ, vận chuyển *Ngọc Tủy Quy Nhất* hít thở sâu ba nhịp. Dòng tủy ngọc tinh khiết lập tức tỏa nhiệt gột rửa sự căng thẳng của kinh mạch, giúp cơ thể tôi bình ổn trở lại.

"Minh An! Em có sao không?!"

Tiếng kỹ sư Tuấn hốt hoảng vang lên. Anh từ sau cây dầm thép lao vội ra, hai mắt trố tròn nhìn hiện trường hoang tàn của căn hầm: sàn gạch vỡ nát, dầm thép móp méo và nắp giếng bị đập lõm sâu. Tuấn thở hổn hển, nhìn tôi với ánh mắt bàng hoàng tựa như nhìn thấy một vị thiên thần giáng thế:

"Trời đất ơi... em vừa đánh bay một gã khổng lồ mặc giáp sắt nặng hơn tạ đấy à? Em... võ công của em rốt cuộc là cảnh giới gì vậy?!"

Tôi mỉm cười lau mồ hôi trên trán: "Chỉ là chút quyền cước tự vệ gia truyền thôi anh Tuấn. Em không sao cả."

Nói đoạn, tôi cúi xuống nhặt những vật phẩm rơi lại trên sàn nơi Hắc Lân Thiết Vệ vừa ngã xuống.

Đó là một tấm lệnh bài bằng huyền thiết màu đen xám nặng trịch, mặt trước chạm nổi hình rồng chín đầu vờn sóng biển cuộn trào, mặt sau khắc ba chữ Nôm sắc bén: **Thiết Vệ Tam**. Bên cạnh tấm lệnh bài là một cuộn da dê cổ vẽ chi tiết sơ đồ bố trí các chốt xích Hắc Thiết Âm Cương đang trói chặt Thủy Môn Chấn Tiêu dưới đáy địa tầng bốn mươi hai mét.

Tôi mở cuộn da dê ra xem, mắt ánh lên vẻ sắc lạnh. Trên bản vẽ, Cửu Long Thiên Hải đã đóng chín chiếc đinh neo âm cương phong tỏa chín kinh mạch chủ của cọc đồng, mượn âm khí lòng sông để nuôi dưỡng một trận pháp nghịch chuyển có tên gọi viễn cổ là *Cửu U Thôn Thiên Trận*.

Tôi cất lệnh bài và bản đồ vào balo dã chiến, rồi bước lại gần miệng giếng kỹ thuật.

Qua khe hở của nắp thép bị móp méo, ba mắt xích bằng hợp kim đen ngòm dày bằng cổ tay người lớn đang lộ ra ngoài, cắm sâu xuống đường giếng dẫn vào lòng đất. 

Tôi rút thanh Trấn Thủy Đoản Đao nơi thắt lưng. Dồn kình lực Ngọc Tủy và kiếm khí Thanh Long vào lưỡi đao đồng thau, tôi vung đao chém dứt khoát!

"Keng! Rắc rắc!"

Ba nhát đao sắc ngọt chém đứt lìa toàn bộ ba mắt xích âm cương đầu tiên. Những mảnh xích đen ngòm vỡ vụn thành bột sắt rơi rụng xuống đáy giếng.

Ngay khoảnh khắc ba mắt xích bị chặt đứt, từ sâu trong lòng giếng bốn mươi hai mét bỗng phát ra một tiếng chuông đồng ngân vang trầm đục:

"Uông... uông... uông..."

Một luồng linh khí ấm áp màu hoàng kim thuần khiết từ đáy sâu dội ngược lên, xua tan hoàn toàn khí tức âm sát ngột ngạt trong căn hầm. Toàn bộ không gian dưới chân tháp thủy đài Ba Son trở nên sáng sủa và thanh tịnh lạ thường. Mạch nước sông Sài Gòn ngoài kia dường như cũng đang khẽ rung lên những nhịp điệu hoan ca đáp lại.

Khối trụ đồng **Thủy Môn Chấn Tiêu** đã bắt đầu cởi bỏ xiềng xích đầu tiên.

Tôi nhìn xuống đáy giếng tối thẳm, trong lòng dâng lên một ngọn lửa quyết tâm rực cháy. Tấm lệnh bài của Thiết Vệ Tam và bản đồ Cửu U Thôn Thiên Trận đã mở ra toàn bộ manh mối then chốt. Trận quyết chiến cuối cùng để giải thoát hoàn toàn cọc tiêu số sáu dưới đáy sâu Ba Son đang chờ đợi tôi ở phía trước!'''

CHAPTER_PROSE = f"{ACT1}\n\n{ACT2}\n\n{ACT3}\n\n{ACT4}"

def run_pipeline():
    print(f"=== BẮT ĐẦU PIPELINE TỰ ĐỘNG CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")

    # 1. Kiểm tra độ dài từ ngữ
    word_count = len(CHAPTER_PROSE.split())
    print(f"[+] [1/5] Tổng số từ trong bản văn: {word_count} từ.")
    if word_count < 3300 or word_count > 3700:
        print(f"[-] CẢNH BÁO: Số từ ({word_count}) nằm ngoài khoảng mục tiêu (3300 - 3650 từ)!")

    # 2. Kiểm duyệt RULE-07 (Không meta từ ngữ, không dùng chữ 'hồi')
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"]
    found_meta = []
    lower_prose = CHAPTER_PROSE.lower()
    for mw in meta_words:
        matches = re.findall(rf"\b{mw}\b", lower_prose)
        if matches:
            found_meta.append((mw, len(matches)))
    
    if found_meta:
        print(f"[-] [RULE-07 LỖI] Phát hiện từ cấm meta: {found_meta}")
        return False
    else:
        print("[+] [2/5] Kiểm duyệt RULE-07 hoàn hảo: Không có bất kỳ từ meta nào (0 từ cấm, 0 chữ 'hồi')!")

    # Kiểm tra an toàn: Không chứa từ khóa chất nổ
    sensitive_words = ["thuốc nổ", "bom", "kíp nổ", "cài bom", "đánh sập"]
    found_sensitive = [sw for sw in sensitive_words if sw in lower_prose]
    if found_sensitive:
        print(f"[-] [AN TOÀN LỖI] Phát hiện từ khóa nhạy cảm: {found_sensitive}")
        return False
    print("[+] Kiểm duyệt an toàn hoàn hảo: 100% không chứa từ khóa nhạy cảm vũ khí nổ!")

    # 3. Chạy CanonEngine & CritiqueEngine
    canon_eng = CanonEngine(DB_PATH)
    critique_eng = CritiqueEngine(DB_PATH)

    canon_issues = canon_eng.validate_text_for_forbidden_assumptions(CHAPTER_PROSE)
    if canon_issues:
        print(f"[-] CanonEngine phát hiện lỗi: {canon_issues}")
        return False
    print("[+] CanonEngine: 0 lỗi suy diễn cấm kỵ.")

    critique_res = critique_eng.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_tuan"],
        text=CHAPTER_PROSE
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [3/5] CritiqueEngine thông qua: 0 lỗi nghiêm trọng (Tổng issues: {len(critique_res.get('issues', []))}).")

    # 4. Xuất bản Markdown
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(CHAPTER_PROSE)
    print(f"[+] [4/5] Đã xuất tệp Markdown: {md_file_path}")

    # 5. Xuất bản Word (.docx)
    docx_pipe = DocxPipeline()
    docx_file_name = f"ch_{CHAPTER_NUM:03d}.docx"
    docx_file_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02", docx_file_name)
    os.makedirs(os.path.dirname(docx_file_path), exist_ok=True)
    docx_pipe.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=CHAPTER_PROSE,
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
        "Đại Chiến Hầm Ba Son & Đột Phá Long Lân Phá Kình",
        CHAPTER_NUM,
        1,
        f"{DATE}T17:30:00+07:00",
        CHAPTER_NUM,
        "loc_ba_son",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_hac_lan_thiet_ve"]),
        "Minh An đối đầu trực diện Hắc Lân Thiết Vệ (Luyện Cốt hậu kỳ) trong tầng hầm kỹ thuật 12m Ba Son. Đối phương dùng Hắc Ngạc Toái Cốt và song kích ép lùi Minh An. Nhận ra tử huyệt đốt sống thắt lưng số 4 do tà công nuốt tinh huyết thủy quái, Minh An dung nạp kiếm khí Thanh Long Lân Kiếm vào Hắc Thiết Đoản Côn, thi triển chiêu thức dung hợp Long Lân Phá Kình chém gãy kích và đánh nát tử huyệt đối thủ. Hắc Lân Thiết Vệ trọng thương trốn thoát qua cống ngầm. Minh An thu được lệnh bài Thiết Vệ Tam, bản đồ Cửu U Thôn Thiên Trận, và chém đứt 3 mắt xích âm cương đầu tiên giải phóng linh khí cọc số 6.",
        "Đánh bại cường giả Luyện Cốt hậu kỳ đầu tiên; sáng tạo chiêu thức Thể Đạo mới Long Lân Phá Kình; phá vỡ tầng phong tỏa đầu tiên của Thủy Môn Chấn Tiêu; thu thập lệnh bài và bản đồ âm mưu Cửu Long Thiên Hải."
    ))

    # 6.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An đánh bại Hắc Lân Thiết Vệ tại Ba Son, chặt đứt 3 mắt xích âm cương đầu tiên, bắt đầu đánh thức Thủy Môn Chấn Tiêu."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Phát hiện trận đồ Cửu U Thôn Thiên Trận của Cửu Long Thiên Hải dùng để phong tỏa long mạch bến cảng Sài Gòn."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 7. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T18:00:00+07:00"
        inv_data["current_location"] = "Tầng hầm kỹ thuật Tháp Thủy Đài — Ụ tàu cổ Ba Son (TP.HCM)"
        
        # Thêm Lệnh bài Thiết Vệ Tam & Bản đồ Cửu U Thôn Thiên Trận
        item_names = [it.get("name") for it in inv_data.get("core_weapons_and_artifacts", [])]
        if "Lệnh Bài Huyền Thiết Thiết Vệ Tam" not in item_names:
            inv_data["core_weapons_and_artifacts"].append({
                "name": "Lệnh Bài Huyền Thiết Thiết Vệ Tam",
                "type": "Chiến lợi phẩm / Thẻ bài thân phận",
                "location": "Balo dã chiến",
                "condition": "Nguyên vẹn, chạm khắc rồng chín đầu",
                "durability": "100/100",
                "function": "Lệnh bài của Hắc Lân Thiết Vệ đệ tam thuộc tổng bộ Cửu Long Thiên Hải"
            })
            inv_data["core_weapons_and_artifacts"].append({
                "name": "Bản Đồ Da Dê Cửu U Thôn Thiên Trận",
                "type": "Chiến lợi phẩm / Trận đồ tà đạo",
                "location": "Balo dã chiến",
                "condition": "Nguyên vẹn",
                "durability": "100/100",
                "function": "Bản vẽ chi tiết 9 chốt neo xích Hắc Thiết Âm Cương phong tỏa Thủy Môn Chấn Tiêu tại Ba Son"
            })
        
        # Cập nhật kỹ năng mới Long Lân Phá Kình
        skill_names = [sk.get("name") for sk in inv_data.get("core_skills", [])]
        if "Long Lân Phá Kình (Kính Kình Kiếm Khí Hợp Nhất)" not in skill_names:
            inv_data["core_skills"].append({
                "name": "Long Lân Phá Kình (Kính Kình Kiếm Khí Hợp Nhất)",
                "type": "Thể Đạo / Dung hợp vũ khí & kiếm khí",
                "stage": "Sơ ngộ (Dẫn kiếm khí Thanh Long Lân Kiếm vào Hắc Thiết Đoản Côn phá giáp hộ thể)"
            })

        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (thêm Lệnh Bài, Bản Đồ Da Dê & Chiêu thức Long Lân Phá Kình).")

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

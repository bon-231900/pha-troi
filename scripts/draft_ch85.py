# -*- coding: utf-8 -*-
"""Draft Chapter 85 for Phá Trời Novel OS with ~3,600+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 85
CHAPTER_TITLE = "Huyết Khí Quy Nguyên"
DATE = "2026-10-28"
LOCATION = "Mốc Tọa Độ Quốc Gia GPS 0001 & Bến Tàu Năm Căn, Cà Mau"

ACT1 = '''Năm giờ ba mươi phút sáng ngày hai mươi tám tháng mười.

Bình minh trên Đất Mũi Cà Mau buông xuống bãi bồi phù sa một dải ánh sáng vàng cam rực rỡ, tinh khôi và thanh khiết lạ thường.

Gió biển sớm mai từ hai vùng đại dương — biển Đông ngầu đỏ phù sa màu mỡ và vịnh Thái Lan xanh ngắt một màu lam ngọc sâu thẳm — giao thoa thổi về lồng lộng, mang theo vị mặn nồng nàn của biển khơi hòa quyện với hương thơm ngai ngái của bùn non và lá đước mục rữa. Từng đàn chim hải âu trắng muốt chao lượn rộn rã trên nền trời lam biếc, ríu rít gọi bầy đón chào một ngày mới an lành.

Tôi ngồi khoanh chân xếp bằng theo thế ngũ tâm triều thiên trên một mỏm đá bazan nhô cao sát mép nước, ngay cạnh mốc tọa độ quốc gia GPS 0001 — nơi đặt hình tượng con tàu no gió vươn mình ra biển lớn.

Đêm qua, sau khi khối thạch anh bazan Trấn Hải Thần Sa được kích hoạt và toàn bộ mười hai cọc tiêu Thủy Môn đồng loạt an định, một sự bình yên tuyệt đối đã bao trùm lấy khắp dải đất phương Nam. Cơn sóng triều hung hãn từng chồm lên đòi nuốt chửng dải rừng phòng hộ nay đã lùi xa, nhường chỗ cho con nước ròng êm đềm vỗ về chân rừng ngập mặn.

Chiếc tàu nghiên cứu đại dương cải trang của Cửu Long Thiên Hải cùng toàn bộ bốn chiếc bè nổi thép đã bị vô hiệu hóa hoàn toàn. Toán lính đánh thuê tinh nhuệ bị tước sạch vũ khí, bị giam giữ nghiêm ngặt trong khoang tàu dưới sự áp giải của lực lượng an ninh biên phòng đường biển, sau khi tôi bí mật gửi tín hiệu tọa độ khẩn cấp bằng mật mã điều hướng quốc gia.

Tạ Bách Xuyên — kẻ mang danh phó tổng giám đốc an ninh đặc nhiệm từng ngông nghênh coi trời bằng vung — giờ đây chỉ là một kẻ bại trận bị trật khớp vai và chấn thương kinh mạch, đang chờ ngày đối diện với sự trừng phạt nghiêm minh của pháp luật.

Nhưng trong khoảnh khắc tĩnh lặng thiêng liêng này, tôi không nghĩ nhiều về kẻ thù.

Tôi nhắm mắt lại, đắm mình vào sự chuyển hóa kỳ diệu đang diễn ra bên trong từng tế bào của cơ thể.

Ký ức của những ngày đầu tiên dấn thân vào con đường chông gai bỗng ùa về rõ mồn một trong tâm trí tôi. Tôi nhớ lại buổi chiều mưa tầm tã bên ngã tư Hàng Xanh ở quận Bình Thạnh, nơi tôi — một thanh niên kỹ thuật viên địa chất bình thường với mức lương còm cõi và gánh nặng cơm áo gạo tiền — lần đầu tiên nhặt được mảnh tàn hồn cô độc của Lâm Tịch rơi rụng từ thinh không. Tôi nhớ lại những đêm thức trắng trên căn gác trọ nhỏ đường Ung Văn Khiêm, cắn răng chịu đựng những cơn đau xé thịt rách da khi tự mình nắn chỉnh từng khớp xương, rèn giũa ba mươi ba đốt sống tủy theo khẩu quyết Thể Đạo phàm nhân.

Từ chỗ một phàm nhân yếu ớt không có linh căn, chỉ biết nương tựa vào sự kiên trì và lòng can đảm, tôi đã đi qua biết bao trận huyết chiến sinh tử. Từ ngọn núi Chứa Chan đầy hiểm họa, qua chùa Hang Châu Đốc, cồn Trấn Ba sóng vỗ, cho tới đáy sâu Soài Rạp và mũi biển Cà Mau này.

Và giờ đây, một cảnh giới hoàn toàn mới đã chính thức định hình: **Hoán Huyết Sơ kỳ**!

Đó là một sự lột xác toàn diện từ tận gốc rễ sinh học. Ba mươi ba đốt sống lưng của tôi lúc này sáng lấp lánh như ngọc thạch liên hoa thấu quang. Không còn cảm giác thô cứng, nặng nề của khung xương phàm trần, toàn bộ khung xương của tôi giờ đây dẻo dai và bền bỉ tựa như những thanh hợp kim tinh luyện trong lò luyện ngàn độ. Từng khớp xương liên kết chặt chẽ với nhau, có thể co giãn vi mô để phân tán mọi lực va đập khủng khiếp nhất.

Đặc biệt nhất chính là dòng máu mới đang cuộn trào bên trong huyết quản.

Từng giọt Thuần Dương Cương Huyết mang sắc đỏ thẫm ánh lên kim quang ấm áp, chuyển động tuần hoàn nhịp nhàng theo từng nhịp đập chậm rãi của trái tim. Dưới sự vận hành của quy tức cùng cực, nhịp tim của tôi duy trì ở mức bốn mươi nhịp một phút nhưng mỗi lần co bóp đều đẩy đi một khối lượng năng lượng khổng lồ, nuôi dưỡng hàng triệu mao mạch li ti dưới da.

Làn da của tôi sau khi bài tiết toàn bộ tạp chất vi mô đã trở nên mịn màng, dẻo dai như da thuộc ngàn năm. Một vết xước do mảnh kim loại sắc nhọn cứa phải trên bắp tay đêm qua giờ đây đã tự động khép miệng, bong lớp vảy mỏng và tái tạo làn da mới hoàn toàn mà không để lại bất kỳ vết sẹo nào.

Tôi khẽ giơ bàn tay phải ra trước mặt, vận chuyển một luồng cương huyết từ tâm thất dồn về lòng bàn tay.

Không cần chạm vào bề mặt phiến đá bazan cách đó nửa thước, một làn sóng kình lực vô hình ấm áp tựa luồng nhiệt phong bỗng bắn ra từ lòng bàn tay tôi!

*XOẸT!*

Mặt đá bazan cứng như thép lập tức lõm xuống một vết tròn sâu nửa tấc, nhẵn thín như được mài giũa bằng mũi khoan kim cương! Đó chính là dấu hiệu của "Cương Khí Ly Thể" — khả năng phóng kình lực cách không mà chỉ những bậc đại tông sư Thể Đạo đạt tới cảnh giới hoán chuyển máu thịt mới có thể làm được.

Các giác quan của tôi mở rộng đến mức độ kinh ngạc.

Ngồi trên mỏm đá, dù nhắm nghiền hai mắt, tôi vẫn có thể nghe rõ tiếng những chú cá thòi lòi quẫy đuôi nhảy tanh tách trên bãi bùn cách xa ba mươi mét, nghe được từng đợt sóng ngầm luồn lách qua chùm rễ đước dưới đáy nước sâu mười mét. Xa hơn nữa, tôi nghe thấy tiếng máy đuôi tôm nổ phành phạch của những chiếc ghe cào xóm Mũi bắt đầu ra khơi, tiếng cười nói giòn tan của những người ngư dân chân chất khi kéo lên những mẻ lưới đầy ắp tôm cá tươi rói.

Đó chính là sức mạnh chân thật của Thể Đạo phàm nhân: không mượn linh khí trời đất để ngưng tụ pháp lực ảo ảnh, mà đánh thức tiềm năng vô tận vốn ngủ yên bên trong chính xương thịt và dòng máu của con người.'''

ACT2 = '''Tám giờ sáng.

Nắng sớm bắt đầu rải những vệt vàng óng ả lên tán rừng đước Năm Căn bạt ngàn.

Tôi đứng dậy, vươn vai hít một hơi thật sâu. Không khí trong lành mặn mòi nơi rốn biển tràn ngập lồng ngực, mang lại một cảm giác sảng khoái và tự do chưa từng có trong suốt những tháng ngày bôn ba gian khổ.

Bỗng nhiên, trong thức hải của tôi, một làn sóng năng lượng ấm áp khẽ lay động.

Đài sen ngọc bích vốn lơ lửng giữa làn sương mờ tĩnh lặng bỗng tỏa ra muôn ngàn tia sáng màu lam ngọc lung linh. Từng cánh sen hé nở nhịp nhàng, để lộ một bóng hình thiếu nữ thanh tú, hư ảo nhưng vô cùng rõ nét đang ngồi khoanh chân giữa nhụy hoa.

Lâm Tịch đã thực sự thức tỉnh!

Không còn là những ý niệm thì thầm đứt quãng trong cơn mê muội, nguyên thần của nàng lúc này đã ngưng tụ lại một cách vững chắc. Chiếc áo lụa trắng thanh tao bay phấp phới trong thức hải, mái tóc đen dài xõa ngang vai, đôi mắt trong veo như làn nước mùa thu đang chăm chú nhìn tôi với vẻ kinh ngạc và xúc động khôn nguôi.

"Minh An..."

Thanh âm trong trẻo như tiếng chuông ngọc của nàng vang vọng khắp tâm trí tôi, làm tan biến mọi mệt mỏi sau chuỗi ngày bôn ba nơi đầu sóng ngọn gió.

"Lâm Tịch, cô đã hoàn toàn bình phục rồi sao?" Tôi mừng rỡ hỏi dồn trong tâm thức.

Lâm Tịch khẽ mỉm cười, một nụ cười hiếm hoi mang theo sự ấm áp chân thành xua tan vẻ lạnh lùng băng giá thường ngày:

"Nguyên thần của tôi đã hồi phục được sáu phần nhờ luồng địa khí thanh khiết vô biên mà anh thu thập từ mười hai cọc tiêu Thủy Môn. Vết nứt trên bản mệnh đài sen đã liền lại, không còn nguy cơ tiêu tán nữa."

Nàng ngước mắt nhìn quanh thức hải của tôi, nơi những dải sáng vàng óng của Thuần Dương Cương Huyết đang lưu chuyển tuần hoàn như những dải ngân hà thu nhỏ:

"Nhưng điều làm tôi kinh ngạc nhất chính là anh... Nguyễn Minh An, anh đã làm được một điều mà ngay cả các tu sĩ thượng giới ở kỷ nguyên trước cũng phải nghiêng mình thán phục. Anh đã dùng chính thể phách phàm nhân, bước từng bước kiên định qua Luyện Cốt rồi đột phá Hoán Huyết, bảo vệ trọn vẹn mạch phong ấn của cả một vùng đất rộng lớn."

Tôi đưa mắt nhìn ra biển trời bao la của Đất Mũi, khẽ lắc đầu:

"Tôi không nghĩ mình làm được điều gì phi thường. Tôi chỉ là một người con của mảnh đất này. Nhìn thấy quê hương bị đe dọa, nhìn thấy mẹ già và những người dân lam lũ có thể mất đi mái nhà yên ấm, tôi không thể khoanh tay đứng nhìn. Sức mạnh này không phải do tôi tự sáng tạo ra, mà là do chính đất mẹ phương Nam đã nâng đỡ, che chở cho tôi."

Lâm Tịch lặng đi một thoáng, ánh mắt nàng ánh lên niềm xúc cảm sâu lắng:

"Chính vì tấm lòng trong sáng và ý chí kiên định ấy, địa khí đất trời mới chịu quy phục và hòa nhập vào dòng máu của anh. Ở thượng giới xa xưa, người ta mải mê tranh đoạt linh đan diệu dược, chém giết lẫn nhau để tìm kiếm trường sinh bất tử, nhưng lại quên mất rằng cội nguồn của sức mạnh chân chính chính là sự gắn kết với mảnh đất nuôi dưỡng mình."

Nàng ngập ngừng giây lát rồi khẽ nói, giọng nói nhẹ như gió thoảng nhưng đong đầy tình cảm chân thật:

"Cảm ơn anh, Minh An. Cảm ơn anh vì đã luôn giữ trọn lời hứa, không bao giờ bỏ rơi tôi giữa những thời khắc đen tối nhất."

"Chúng ta là bạn đồng hành cùng chung hoạn nạn, cùng chia sẻ một sinh mệnh, đừng nói lời cảm ơn khách sáo," tôi mỉm cười đáp lại.

Nét mặt nàng bỗng trở nên nghiêm nghị, đôi mày thanh tú hơi nhíu lại:

"Minh An, giờ đây khi anh đã bước vào Hoán Huyết Sơ kỳ và mười hai cọc tiêu Thủy Môn đã an định, tôi có thể giải thích cho anh rõ hơn về bí mật thực sự của thế giới này. Mảnh đất Trái Đất nơi anh đang sống không đơn thuần là một hành tinh bình thường. Trong vũ trụ bao la, nơi đây được gọi là **Cực Tù Lục Trọng Giới** — nhà tù giam giữ sáu tầng phong ấn tối cổ do các bậc chí tôn Thần Hoang giới thiết lập từ hàng triệu năm trước."

"Sáu tầng phong ấn?" Tôi kinh ngạc hỏi.

"Đúng vậy," Lâm Tịch gật đầu. "Mười hai cọc Thủy Môn ngoài duyên hải phương Nam thực chất chỉ là chiếc then cài bảo vệ bên ngoài của Tầng Thứ Sáu. Trung tâm thực sự của tầng phong ấn này nằm ngay dưới lòng sông Sài Gòn — nơi ẩn giấu **Đại Trận Thần Hoang** và ngọn cổ tháp phong ấn bí mật. Cửu Long Thiên Hải muốn phá hủy mười hai cọc Thủy Môn cốt để làm lệch hướng dòng chảy năng lượng, ép lõi phong ấn dưới lòng sông Sài Gòn phải trồi lên sớm hơn dự kiến. Giờ đây khi mười hai cọc tiêu đã an định, âm mưu đường biển của chúng đã thất bại hoàn toàn. Nhưng điều đó cũng đồng nghĩa với việc: chúng sẽ dồn toàn bộ lực lượng tà tu còn lại về đại bản doanh Sài Gòn để tung ra đòn liều chết cuối cùng!"'''

ACT3 = '''Mười giờ ba mươi phút trưa.

Tôi có mặt tại một quán cà phê nhỏ lợp mái lá dừa ven bến tàu Năm Căn, thưởng thức ly cà phê đen đá đậm đà mang đậm hương vị miệt vườn sông nước Cà Mau.

Bên ngoài, dòng sông Cửa Lớn cuồn cuộn chảy trôi với dòng nước đỏ nặng phù sa, từng chiếc xuồng máy đuôi tôm chở đầy ắp hàng hóa xuôi ngược nhộn nhịp. Cuộc sống thanh bình, êm ả của người dân nơi đây dường như chưa từng hay biết về cơn bão ngầm suýt chút nữa đã hủy diệt toàn bộ vùng đất này đêm qua.

Tôi lấy chiếc điện thoại di động cũ ra khỏi túi, bấm gọi vào một số máy quen thuộc.

Chuông reo vài hồi thì đầu dây bên kia bắt máy, giọng nói hiền từ, ấm áp của mẹ tôi vang lên giữa tiếng gà gáy trưa ở cù lao Tiền Giang:

"An đó hả con? Mấy bữa nay đi công tác ngoài biển sóng gió dữ hôn con? Ăn uống có đàng hoàng không?"

Nghe tiếng mẹ, sống mũi tôi bỗng cay cay. Mọi căng thẳng, mệt mỏi và hiểm nguy nơi đáy biển sâu dường như tan biến không còn dấu vết:

"Dạ con khỏe lắm mẹ. Công việc khảo sát ngoài này xong xuôi hết rồi, con đang chuẩn bị lên xe về lại Sài Gòn. Mẹ ở nhà nhớ giữ gìn sức khỏe nghe mẹ."

"Ừ, con ráng giữ gìn sức khỏe. Chừng nào rảnh thì ghé về cù lao mẹ đổ bánh xèo cho ăn nghen con..."

"Dạ, con nhớ rồi mẹ."

Tắt điện thoại, tôi hít một hơi thật sâu để lấy lại sự bình tĩnh thép. Sự bình yên của mẹ, của gia đình và của hàng triệu con người lương thiện chính là lý do duy nhất để tôi tiếp tục tiến bước.

Chiếc máy tính bảng thu giữ từ Tạ Bách Xuyên đặt trên bàn gỗ, màn hình hiển thị toàn bộ dữ liệu mật đã được giải mã thành công sau khi kết nối với khóa bảo mật do chính tay lão khai nhận dưới sự áp giải của cơ quan an ninh biên phòng.

Những tập tin tuyệt mật mở ra trước mắt tôi hé lộ toàn bộ quy mô của chiến dịch "Đoạt Mạch" do hội đồng quản trị Tập đoàn Cửu Long Thiên Hải vạch ra từ nhiều năm trước.

Cửu Long Thiên Hải không đơn thuần là một tập đoàn tài chính hàng hải thông thường. Đứng sau chúng là một nhóm tà tu biến chất trốn chạy từ các rạn nứt không gian hải ngoại, kết hợp với các thế lực ngầm thèm khát nguồn năng lượng khổng lồ bị phong ấn dưới lòng đất Sài Gòn suốt hai phẩy năm triệu năm qua.

Khi toàn bộ mười hai cọc tiêu Thủy Môn phương Nam bị tôi an định, âm mưu làm sụp lở thềm địa tầng duyên hải của chúng đã hoàn toàn phá sản.

Bị dồn vào chân tường, bức điện tín mật phát đi từ đại bản doanh hải ngoại lúc bốn giờ sáng nay đã ra lệnh:

Toàn bộ các chi nhánh ngầm của Cửu Long Thiên Hải tại thành phố Hồ Chí Minh phải lập tức chuyển sang giai đoạn khẩn cấp. Mục tiêu tiếp theo của chúng là kích hoạt lõi phong ấn trung tâm nằm ngay tại ngã ba sông Sài Gòn và bán đảo Thanh Đa — nơi ngọn cổ tháp phong ấn bí mật đang ngủ yên!

Đặc biệt, trong danh sách các mục tiêu theo dõi trọng điểm của chúng tại Sài Gòn, tôi nhìn thấy hình ảnh viện nghiên cứu địa chất nơi tôi từng làm việc, và cả hình ảnh khu nhà trọ cũ kỹ của tôi trên đường Nơ Trang Long!

Bàn tay tôi vô thức siết chặt chiếc ly thủy tinh, kình lực Hoán Huyết khiến mặt nước cà phê gợn lên từng vòng sóng nhỏ.

Chúng muốn nhắm vào những nơi chốn thân thuộc nhất của tôi để uy hiếp tinh thần!

Trên chiếc ghế gỗ bên cạnh, một ông lão cựu chiến binh tuổi ngoài bảy mươi mặc bộ bà ba sẫm màu, tay cầm chiếc nón tai bèo cũ kỹ, đang ngồi nhìn ra dòng sông Cửa Lớn. Thấy tôi chăm chú nhìn ra bến tàu, ông cụ khẽ cười, giọng khàn khàn đặc sệt chất Nam Bộ:

"Chú em đi công tác về thành phố hả? Rừng đước xứ này ngó vậy chớ thiêng liêng lắm chú em ơi. Hồi chiến tranh bom đạn dập tơi bời, vậy mà cây đước vẫn bám rễ sâu dưới bùn non, chở che cho bộ đội mình qua bao mùa giặc giã. Đất này bom đạn không khuất phục nổi, người xứ này cũng hổng có ai chịu cúi đầu đâu!"

Lời nói mộc mạc của ông lão cựu chiến binh như một ngọn lửa ấm áp truyền thẳng vào tim tôi.

"Dạ, cháu hiểu thưa bác," tôi kính cẩn đáp lời. "Người đi trước đã giữ đất bằng máu xương, thế hệ chúng cháu nhất định sẽ không để mảnh đất này bị kẻ xấu chà đạp."

Tôi đứng dậy, để lại tiền nước trên bàn rồi khoác chiếc ba-lô bước nhanh ra bến xe khách Năm Căn.

Nhìn lại dải đất Cực Nam một lần cuối, những rặng đước xanh ngắt kiên cường vẫy chào trong gió biển lồng lộng. Mảnh đất này đã trao cho tôi sức mạnh của Thuần Dương Cương Huyết, trao cho tôi niềm tin bất diệt của người thủ hộ phàm nhân.

Tôi bước lên chuyến xe khách ngược dòng về phương Bắc.

Phía trước tôi, Sài Gòn đang chờ đợi. Những ngọn gió giông bão táp của số phận đang dần hội tụ trên bầu trời thành phố, và tôi đã sẵn sàng nghênh đón tất cả!'''

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
description: "Minh An củng cố Hoán Huyết Sơ kỳ tại Đất Mũi, Lâm Tịch hồi phục nguyên thần hé lộ bí mật Đại Trận Thần Hoang, chuẩn bị ngược dòng trở về Sài Gòn đối đầu tổng bộ."
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
        "Bình Minh Đất Mũi, Củng Cố Hoán Huyết Sơ Kỳ, Lâm Tịch Thức Tỉnh & Lên Xe Ngược Dòng Về Sài Gòn",
        CHAPTER_NUM,
        1,
        f"{DATE}T11:00:00+07:00",
        CHAPTER_NUM,
        "loc_dat_mui_ca_mau",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An tĩnh tọa bên mốc GPS 0001 Đất Mũi Cà Mau, củng cố hoàn hảo cảnh giới Hoán Huyết Sơ kỳ, các giác quan mở rộng và cơ thể tự hồi phục vết thương phi thường. Lâm Tịch chính thức thức tỉnh sáu phần nguyên thần, đối thoại sâu sắc và hé lộ việc 12 cọc tiêu an định đã vô tình kích hoạt thế cờ cuối cùng của Đại Trận Thần Hoang tại Sài Gòn. Trích xuất tài liệu mật từ máy tính Tạ Bách Xuyên, phát hiện tổng bộ Cửu Long Thiên Hải rục rịch nhắm vào viện nghiên cứu và nhà trọ tại Sài Gòn. Minh An lên xe khách Năm Căn ngược dòng về Sài Gòn nghênh chiến.",
        "Củng cố vững chắc Hoán Huyết Sơ kỳ; Lâm Tịch hồi phục nguyên thần; giải mã toàn bộ hồ sơ mật Cửu Long Thiên Hải; Minh An lên đường trở lại Sài Gòn mở ra cao trào cuối Hồi 2."
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
        "Lâm Tịch hồi phục sáu phần nguyên thần, thức tỉnh hoàn toàn trong đài sen ngọc bích, chia sẻ tầm nhìn về Đại Trận Thần Hoang và gắn kết tri kỷ với Minh An."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An củng cố hoàn hảo cảnh giới Hoán Huyết Sơ kỳ, xương ngọc thấu quang, Thuần Dương Cương Huyết mang ánh kim, thính giác thị giác mở rộng cực hạn."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "12 cọc tiêu Thủy Môn đã an định trọn vẹn; tiêu điểm chuyển dịch về ngã ba sông Sài Gòn và bán đảo Thanh Đa — nơi Đại Trận Thần Hoang sắp sửa mở ra."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An gọi điện cho mẹ ở cù lao Tiền Giang, nhận diện nguy cơ tổng bộ Cửu Long Thiên Hải nhắm vào nhà trọ Nơ Trang Long và viện nghiên cứu địa chất tại Sài Gòn."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T11:00:00+07:00"
        inv_data["current_location"] = "Bến Xe Khách Năm Căn, Cà Mau (Đang di chuyển về TP.HCM)"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Huyết Ánh Kim / Cốt Tủy Thấu Quang / Tự Phục Hồi Phi Thường)"

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

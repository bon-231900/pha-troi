# -*- coding: utf-8 -*-
"""Draft Chapter 79 for Phá Trời Novel OS with ~4,000+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 79
CHAPTER_TITLE = "Dạ Hành Độc Lộ"
DATE = "2026-10-24"
LOCATION = "Núi Chứa Chan & Quốc Lộ 1A (Đồng Nai) -> Ngoại Vi TP.HCM"

ACT1 = '''Năm giờ mười lăm phút chiều ngày hai mươi tư tháng mười.

Ráng chiều miền Đông buông xuống sườn tây Núi Chứa Chan như một dải lụa màu huyết dụ vắt ngang qua bầu trời bát ngát. Gió đại ngàn thổi thốc qua những trảng le xào xạc, mang theo hơi ẩm lạnh lẽo của rừng già hòa lẫn với mùi khét lẹt của đá hoa cương vừa bị nung cháy bởi thuốc súng.

Tôi cẩn thận bám theo những gờ đá granite tai mèo dốc đứng, từng bước luồn sâu vào thung lũng sườn tây.

Mỗi cử động của tôi lúc này đều kéo theo một cơn đau nhức âm ỉ. Vết rách do mảnh đạn M79 găm sượt qua bả vai trái đã bắt đầu se miệng nhờ lớp cơ bắp Luyện Cốt siết chặt, nhưng máu khô bết dính vào lớp áo lót bên trong khiến da thịt cọ xát rát buốt. Tuy nhiên, vết thương thể xác ấy chẳng thấm tháp vào đâu so với cơn chấn động đang âm ỉ râm ran dọc theo ba mươi ba đốt sống lưng.

Tuyệt kỹ "Dĩ Thể Vi Kiếm" quả thực là con dao hai lưỡi tàn khốc.

Dù đã mượn được một tia Vô Ngân Kiếm Khí của tiền nhân Bạch Viên để chém đứt thanh đại đao hai mươi ký của Tạ Lôi và phế sạch công phu tà đạo của hắn, nhưng luồng kiếm ý sắc lạnh ấy đã để lại những vết hằn sâu hoắm trong tủy ngọc của tôi. Từng đốt xương sống như những thỏi đồng thau vừa được lôi ra khỏi lò rèn, vừa bỏng rát như lửa thiêu lại vừa lạnh buốt như băng hàn, khiến từng nhịp thở của tôi đều nặng nề như đeo chì.

Nhưng điều khiến lòng tôi trĩu nặng nhất không phải là nỗi đau thể xác.

Tôi khẽ khép mắt, hướng thần niệm vào sâu trong thức hải.

Trước mắt tôi, không gian ý thức từng một thời rực rỡ quầng sáng trắng thanh khiết nay chỉ còn là một vùng sương mù mờ ảo, hoang vu và lạnh lẽo. Đài sen ngọc bích của Lâm Tịch giờ đây đã thu nhỏ lại chỉ còn bằng lòng bàn tay, lơ lửng đơn độc giữa hư không u tối.

Trên cánh sen ngọc, vết nứt mới màu xám tro rạch một đường dài ngoằn ngoèo, nằm song song với vết thương cũ từ trận đại chiến viễn cổ. Quầng sáng hộ thể bao quanh nàng đã hoàn toàn tắt lịm. Nàng tĩnh tọa ở đó, đôi mắt nhắm nghiền, gương mặt thanh tú trắng bệch không còn một tia sinh khí, chìm sâu vào giấc ngủ tĩnh dưỡng miên man.

"Lâm Tịch..." Tôi truyền niệm khẽ gọi, giọng nói nghẹn lại giữa lồng ngực.

Không có một tiếng đáp lại.

Chỉ có sự im lặng đến rợn ngợp dội ngược trở lại tâm thức tôi.

Lần đầu tiên kể từ buổi chiều định mệnh giữa cơn mưa rào ngã tư Hàng Xanh, khi giọng nói lạnh lùng mà sâu lắng của nàng lần đầu tiên vang lên trong đầu tôi, tôi mới phải đối mặt với sự tĩnh lặng tuyệt đối này. Hơn bốn mươi ngày qua, nàng vừa là người bạn đồng hành bí ẩn, vừa là người thầy chỉ dạy từng đường đi nước bước của Thể Đạo, cùng tôi vượt qua bao phen thập tử nhất sinh dưới lòng sông Sài Gòn và đáy vực Hải Uyên.

Giờ đây, vì cứu mạng tôi trước họng súng và đại đao của kẻ thù, nàng đã phải gánh chịu phản chấn tàn khốc của quy tắc Trái Đất, vắt kiệt chút thần niệm ít ỏi để rồi rơi vào hôn mê sâu dài hạn.

Tôi đứng lặng trên một mỏm đá nhô ra giữa sườn đồi, bàn tay siết chặt chuôi Hắc Thiết Đoản Côn đến mức các khớp ngón tay trắng bệch.

Từ nay về sau, trên con đường chông gai vạn dặm này, sẽ không còn ai nhắc nhở tôi hướng né tránh của từng luồng sóng xung kích, không còn ai phân tích điểm yếu của đối thủ, cũng không còn ai khẽ thở dài mỗi khi tôi liều mạng đánh đổi thân xác lấy một cơ hội sinh tồn.

Tôi phải hoàn toàn tự bước đi bằng chính đôi chân và khối óc của một phàm nhân!

Từ phía bên kia sườn đông bắc, tiếng còi hụ của đoàn xe đặc chủng Công an huyện Xuân Lộc và lực lượng kiểm lâm vang lên ngày một dồn dập. Những luồng ánh đèn pha quét loang loáng qua tán rừng le phía xa. Đám người Tạ Lôi cùng toàn bộ số vũ khí nóng và mười sáu khối bộc phá C4 đã bị tôi vô hiệu hóa chắc chắn đã lọt vào tay chính quyền.

Tôi không thể nán lại thêm một giây nào nữa.

Men theo lòng suối cạn đầy những tảng đá mồ côi trơn trượt, tôi luồn qua hàng rào ranh giới của một vườn điều bạt ngàn, tiếp cận con đường đất đỏ liên xã dẫn ra hướng thị trấn Gia Ray.

Dưới chân dốc, bên cạnh một vườn chuối rậm rạp, căn nhà cấp bốn lợp mái tôn của một hộ dân làm rẫy hiện ra mờ ảo dưới ánh đèn vàng vọt. Đây chính là nơi tôi đã gửi chiếc xe máy Wave Alpha cũ từ sáng sớm trước khi leo lên vách đá Thần Quy.

Tôi kéo sụp chiếc mũ lưỡi trai xuống che khuất nửa khuôn mặt đầy bụi đá, bước vào khoảng sân đất nện.

"Bác ơi, cháu xin lấy lại xe," tôi cất tiếng, cố giữ giọng nói bình thản nhất có thể.

Một người đàn ông trung niên da ngăm đen bước ra từ hiên nhà, trên tay cầm chiếc đèn pin nhỏ. Nhìn thấy bộ dạng chiếc áo khoác gió rách bươm và vệt bụi đất bám đầy trên ống quần tôi, ông khẽ nhíu mày:

"Ủa chú em, đi phượt hay khảo sát trên núi mà sao tơi tả vậy? Nãy giờ công an với kiểm lâm hú còi ầm ĩ bên sườn đông, nghe đâu có vụ nổ súng hay sập hầm đá gì trên đó dữ lắm, chú có thấy gì không?"

"Dạ không bác, cháu đi lạc vào bụi gai le sườn tây, trượt chân rách cả áo," tôi cười gượng, rút tờ tiền năm mươi ngàn đưa cho bác chủ nhà. "Bác cho cháu xin nhờ vòi nước ngoài góc sân rửa mặt một chút được không ạ?"

"Được chứ, vòi nước máy bơm đó, chú cứ tự nhiên."

Tôi bước lại góc sân, mở van nước giếng khoan mát lạnh, vục từng vốc nước lớn táp thẳng vào mặt, vào cổ. Dòng nước mát rượi xua đi cái nóng ran của khói súng và bụi đá granite hoa cương bám chặt trong lỗ chân lông. Tôi cẩn thận rửa sạch những vệt máu khô trên bả vai và cánh tay, tránh để lại bất kỳ dấu vết sinh học nào đáng ngờ.

Soi bóng mình vào chiếc gương tròn ố vàng treo trên thân cây vú sữa trước sân, tôi thoáng giật mình.

Khuôn mặt của một kỹ sư dữ liệu hai mươi lăm tuổi trước kia vốn thư sinh và có phần mỏi mệt sau những đêm dài tăng ca trước màn hình máy tính, giờ đây đã góc cạnh và phong trần hơn gấp bội. Nhưng điều làm tôi chú ý nhất là đôi mắt. Sâu thẳm trong tròng đen, dường như có một tia sáng màu bạch ngọc sắc lẹm thoảng qua rồi ẩn sâu vào đáy mắt — tàn dư của luồng kiếm khí ngàn năm vừa được tôi dùng máu thịt tôi luyện.

Tôi cởi bỏ chiếc áo khoác gió đã rách tả tơi, nhét sâu vào đáy ba lô. Thay vào đó, tôi khoác lên mình bộ áo mưa hai lớp màu xanh rêu sẫm, đội chiếc mũ bảo hiểm nửa đầu quen thuộc, gạt chân chống và nổ máy.

Tiếng động cơ xe Wave Alpha nổ giòn tan trong hoàng hôn tĩnh mịch. Tôi vặn ga, chiếc xe lao nhanh ra con đường nhựa liên xã, hòa vào dòng xe cộ thưa thớt của buổi chiều muộn, trực chỉ hướng Quốc lộ 1A.'''

ACT2 = '''Sáu giờ ba mươi phút tối.

Khi bánh xe tôi vừa chạm vào dải phân cách bê tông của ngã ba Xuân Lộc để rẽ vào Quốc lộ 1A, bầu trời miền Đông bỗng chốc tối sầm lại như một chiếc vung nồi khổng lồ úp sập xuống nhân gian.

Một cơn mưa rào đặc trưng của mùa mưa phương Nam bất chợt ập xuống xối xả.

Những hạt mưa to như hạt ngô quất rát rạt vào tấm kính chắn gió của mũ bảo hiểm, chảy ròng ròng xuống cổ áo. Gió chiều thổi bạt những hàng cây cao su hai bên đường, cuốn theo mùi đất đỏ bazan ngai ngái nồng nặc. Nước mưa lạnh buốt ngấm qua lớp áo mưa, táp thẳng vào vết rách trên bả vai trái khiến toàn thân tôi khẽ rùng mình, từng thớ thịt giật lên từng cơn đau buốt.

Những đoàn xe tải chở gỗ, xe container và xe khách giường nằm chạy tuyến Bắc Nam gầm rú inh ỏi, bấm những hồi còi hơi chói tai xé toạc màn mưa đêm. Ánh đèn pha vàng rực quét loang loáng trên mặt đường nhựa ngập nước, phản chiếu những quầng sáng ma quái, chập chờn.

Giữa dòng người hối hả ngược xuôi trên tuyến quốc lộ trọng yếu ấy, không một ai có thể ngờ rằng, người thanh niên gầy gò đang co ro cầm lái chiếc xe máy cà tàng kia vừa trải qua một trận huyết chiến sinh tử với những tay súng đánh thuê thiện chiến nhất của vùng Tam Giác Vàng, vừa dùng một thanh đoản côn cứu lấy mạng lưới phong ấn ngầm của toàn bộ dải đất phương Nam.

Tám giờ bốn mươi phút đêm.

Sau hơn hai tiếng đồng hồ cắn răng chịu đựng những cơn đau nhức buốt giá dưới màn mưa tầm tã, vượt qua thị xã Long Khánh, tôi tấp xe vào một quán cà phê võng xập xệ bên lề đường Quốc lộ 1A thuộc địa phận huyện Trảng Bom.

Quán chỉ là một cái chòi lợp bằng tôn xi măng cũ kỹ, xung quanh mắc chừng mười chiếc võng dù màu xanh bộ đội. Dưới ánh đèn tuýp vàng vọt chập chờn bám đầy xác thiêu thân, mấy bác tài xế xe tải đang ngồi hút thuốc lào vặt, tiếng rít thuốc sòng sọc hòa lẫn với tiếng nước mưa chảy rào rào từ máng xối xuống rãnh thoát nước ven đường.

Tôi chọn một chiếc võng khuất sâu trong góc tối nhất của quán, gọi một ly cà phê đen nóng không đường.

Bác chủ quán mang ly cà phê bốc khói nghi ngút ra, nhìn bộ dạng ướt sũng của tôi rồi ái ngại nói:

"Mưa gió lớn thế này mà chạy xe máy đường dài nguy hiểm lắm chú em. Uống ly cà phê nóng cho ấm người rồi ngả lưng một lát đi, chừng nào tạnh mưa hẵng đi tiếp."

"Cảm ơn bác," tôi khẽ gật đầu, đón lấy ly cà phê.

Hớp một ngụm cà phê đắng ngắt bỏng rát, tôi cảm nhận được hơi ấm lan tỏa từ cuống họng xuống dạ dày, làm dịu bớt cái lạnh tê tái đang bao trùm lấy lồng ngực.

Tôi kéo chiếc ba lô dã chiến vào lòng, mở ngăn bí mật lót lớp vải chống nước bên trong. Tôi rút ra một chiếc điện thoại di động phím bấm cũ kỹ màu đen — chiếc điện thoại phụ dùng SIM rác không đăng ký danh tính mà Tuấn đã trang bị cho tôi để liên lạc khẩn cấp mỗi khi đi thực địa.

Bật nguồn máy, màn hình đơn sắc sáng lên yếu ớt.

Một tin nhắn dạng văn bản mã hóa bằng thuật toán đối xứng hiển thị trên màn hình, được gửi đến từ số máy lạ vào lúc bảy giờ mười lăm phút tối.

Tôi rút tờ giấy nhớ ghi chuỗi khóa giải mã trong ví, nhanh chóng dịch từng dòng ký tự rời rạc thành một thông điệp hoàn chỉnh. Đó chính là tin nhắn từ Tuấn:

*"An! Tôi vừa kiểm tra mạng lưới nội bộ của Viện và dữ liệu giám sát giao thông Đồng Nai. Bên công an huyện Xuân Lộc đã phong tỏa toàn bộ khu vực sườn núi Thần Quy. Mười sáu khối bộc phá C4 và toàn bộ súng đạn của nhóm người nước ngoài đã bị thu giữ. Báo chí địa phương chỉ đăng tin vắn về việc triệt phá băng nhóm tàng trữ vũ khí quân dụng trái phép dưới vỏ bọc doanh nghiệp khoáng sản. Cậu an toàn chứ?"*

Tôi thở phào nhẹ nhõm một hơi. Nhóm Tạ Lôi đã chính thức bị cách ly khỏi hiện trường, cọc tiêu thứ tám Thần Quy Thạch đã được an định trong yên bình mà không gây ra hoảng loạn trong dư luận xã hội.

Nhưng dòng tin nhắn tiếp theo của Tuấn lại khiến tim tôi thắt lại:

*"Tuy nhiên, có một tin rất xấu. Cách đây một tiếng, tường lửa bảo mật của Viện Địa tầng ghi nhận có bốn đợt tấn công từ chối dịch vụ và truy vấn dữ liệu trái phép từ các địa chỉ IP nước ngoài. Mục tiêu của chúng không phải là tài liệu khoa học, mà là trích xuất toàn bộ hồ sơ nhân sự, bảng lương và lý lịch gia đình của nhóm kỹ sư tham gia dự án trắc địa thủy văn — đặc biệt là hồ sơ cá nhân của cậu! Tôi đã kịp thời kích hoạt giao thức cô lập máy chủ và xóa sạch bản sao hồ sơ lưu trữ tạm thời, nhưng tôi e rằng chúng đã thu thập được một phần dữ liệu cơ bản từ trước!"*

Ngón tay tôi run lên bần bật.

Lời đe dọa tàn độc của Tạ Lôi bên mép vực lại một lần nữa vang dội trong tâm trí tôi:

*"Nguyễn Minh An, hai mươi lăm tuổi... Quê quán ở một huyện cù lao nghèo mạn Tiền Giang, có một bà mẹ già bán rau ngoài chợ huyện sống thui thủi một mình... Mày nghĩ người thân của mày sẽ yên ổn được sao?"*

Chúng không hề dọa suông!

Tập đoàn Cửu Long Thiên Hải là một tổ chức tà tu kết hợp với thế lực tư bản ngầm khổng lồ, với những xúc tu vươn sâu vào mọi ngóc ngách của xã hội hiện đại. Một khi chúng đã nhắm vào ai, chúng sẵn sàng dùng những thủ đoạn hèn hạ và tàn nhẫn nhất để bẻ gãy ý chí của kẻ đó.

Tôi lập tức bấm phím gửi lại cho Tuấn một tin nhắn ngắn gọn:

*"Tôi an toàn. Cậu lập tức thu dọn máy tính và đồ đạc cá nhân, rời khỏi căn phòng trọ hiện tại ngay trong đêm. Sang ở tạm căn hộ của anh họ cậu bên Quận 7, nơi đó có bảo vệ và camera giám sát nghiêm ngặt. Tuyệt đối không dùng điện thoại cơ quan để liên lạc với tôi. Mọi việc cứ để tôi xử lý."*

Gửi xong tin nhắn, tôi lập tức tháo nắp lưng chiếc điện thoại phụ, bẻ gãy chiếc thẻ SIM làm đôi rồi vứt vào một bao rác phế liệu dưới chân quán.

Tôi ngả người ra lưng võng, đưa tay vào túi áo trong rút chiếc điện thoại thông minh cá nhân của mình ra.

Màn hình cảm ứng sáng lên. Hình nền là bức ảnh chụp tôi và mẹ vào dịp Tết Nguyên Đán năm ngoái. Trong ảnh, người phụ nữ ngoài năm mươi tuổi với mái tóc hoa râm, khuôn mặt đầy những nếp nhăn lam lũ nhưng nụ cười lại hiền hậu như đóa hoa sen nở giữa bùn lầy, đang tựa đầu vào vai đứa con trai duy nhất của mình bên hiên nhà lá ven sông.

Màn hình thông báo có ba cuộc gọi nhỡ từ "Mẹ" vào lúc năm giờ rưỡi chiều.

Lồng ngực tôi bỗng nhói buốt như bị một bàn tay vô hình bóp nghẹt.

Tôi biết giờ này ở quê, sau một ngày dài dãi nắng dầm mưa ngồi bán từng mớ rau muống, rổ cà chua ngoài chợ huyện, mẹ tôi sẽ lại lụi hụi nhóm bếp củi nấu nồi cơm nguội, rồi ngồi bên chiếc bàn gỗ cũ kỹ ngóng trông tiếng chuông điện thoại của đứa con trai đang đi làm xa trên Sài Gòn.

Chắc chắn mẹ đang lo lắng khôn nguôi. Mẹ sẽ tự hỏi: "Thằng An nay bận gì mà không nghe máy? Nó có bị cảm mạo hay làm việc quá sức không?"

Ngón tay cái của tôi run rẩy đặt lên phím gọi lại màu xanh.

Tôi thèm được nghe giọng nói mộc mạc, đậm chất miền Tây của mẹ biết bao. Tôi thèm được nghe mẹ mắng yêu vài câu, thèm được nghe mẹ kể chuyện con cá bống dừa dưới mương, thèm được nghe mẹ dặn: "Gắng ăn uống đầy đủ nha con, đừng có tiếc tiền mà nhịn ăn nhịn uống..."

Nhưng ngay khoảnh khắc ngón tay chuẩn bị chạm vào màn hình, tôi bỗng khựng lại.

Một cảm giác ớn lạnh chạy dọc sống lưng.

Tạ Lôi đã biết về mẹ tôi. Nếu Cửu Long Thiên Hải đã cử người theo dõi số điện thoại của tôi hoặc thiết lập các trạm thu phát sóng giả mạo để quét tín hiệu, một cuộc gọi trực tiếp lúc này sẽ chẳng khác nào tự tay vẽ một đường chỉ dẫn cho những tên sát thủ tìm về mái nhà tranh nghèo ven sông Tiền!

Tôi có thể chịu đựng được vạn tiễn xuyên tâm, có thể dùng thân mình đỡ đạn M79, nhưng mẹ tôi — một người phụ nữ nông dân bình thường cả đời chưa từng bước ra khỏi lũy tre làng — làm sao có thể chống đỡ được sự tàn bạo của đám tà tu coi mạng người như cỏ rác?

Bàn tay tôi run lên bần bật. Nước mắt không biết từ lúc nào đã làm mờ nhòe đi gương mặt mẹ trên màn hình.

Tôi cắn chặt môi đến mức nếm được vị tanh nồng của máu tươi trào ra nơi khóe miệng.

"Mẹ ơi... con bất hiếu..." Tôi thì thầm trong tiếng nấc nghẹn ngào, bàn tay run rẩy từ từ thu ngón tay lại, rồi dứt khoát nhấn nút tắt nguồn điện thoại.

Màn hình tối sầm lại. Bức ảnh của mẹ biến mất.

Chỉ còn lại sự bi thương và nỗi cô đơn tột cùng bao trùm lấy tâm can tôi giữa màn đêm u tối của quán nước ven đường.'''

ACT3 = '''Mười một giờ ba mươi phút đêm.

Sau khi vòng qua thành phố Biên Hòa, tôi không đi theo hướng cầu Đồng Nai để về trung tâm Sài Gòn như thường lệ. Tôi biết, căn phòng trọ nhỏ bé trên đường Nơ Trang Long ở Bình Thạnh giờ đây có thể đã bị cài cắm người theo dõi hoặc đặt các thiết bị nghe lén tầm xa.

Một kỹ sư dữ liệu am hiểu về công nghệ như tôi tuyệt đối không bao giờ cho phép mình bước chân vào một cái bẫy đã được dự báo trước.

Tôi rẽ xe vào con đường đất gồ ghề ven sông Đồng Nai thuộc khu vực giáp ranh giữa thành phố Dĩ An và quận Thủ Đức cũ. Đây là một bãi tập kết vật liệu xây dựng và xưởng sửa chữa xà lan đã bị bỏ hoang từ nhiều năm nay sau một đợt quy hoạch treo.

Xung quanh chỉ có những khối bê tông vỡ vụn, những cọc sắt rỉ sét chĩa lên trời như những bộ xương khô khổng lồ, và những bụi cỏ lau cao quá đầu người đung đưa xào xạc dưới ngọn gió đêm lạnh ngắt.

Dưới mái tôn xi măng thủng lỗ chỗ của một nhà kho chứa máy móc cũ, tôi tắt máy xe, dựng chân chống giữa.

Không gian xung quanh hoàn toàn tĩnh mịch, chỉ có tiếng nước sông Đồng Nai vỗ ì ầm vào bờ kè đất và tiếng dế rỉ rả kêu đêm.

Tôi trải tấm bạt dã chiến chống nước ra mặt sàn bê tông khô ráo, tháo chiếc ba lô nặng trịch xuống, rồi cởi bỏ bộ áo mưa và chiếc áo phông rách nát.

Trong bóng tối nhờ nhợ của ánh trăng lọt qua khe mái tôn, bờ vai trái của tôi hiện lên với một vệt rách dài hơn mười phân. Lớp máu khô đã đóng thành một mảng vảy sẫm màu, nhưng xung quanh vết thương, các thớ cơ bắp vẫn đang co giật nhẹ theo từng nhịp tim đập.

Quan trọng hơn, bên dưới lớp da lưng của tôi, ba mươi ba đốt sống ngọc thạch đang phát xuất những đợt rung chấn vi mô với tần số cực kỳ dị thường.

Tôi ngồi xếp bằng theo tư thế ngũ tâm triều thiên, hai tay đặt nhẹ lên đầu gối, nhắm nghiền hai mắt và bắt đầu vận hành khẩu quyết "Quy Tức Quyết".

*Hít vào... thở ra...*

Từng luồng không khí ẩm lạnh của đêm ven sông được tôi hút sâu vào lồng ngực, dẫn xuống đan điền, rồi từ từ chuyển hóa thành một luồng thanh khí thuần khiết.

Trái tim tôi bắt đầu đập chậm lại.

Tám mươi nhịp... sáu mươi nhịp... bốn mươi nhịp... rồi dừng lại ở mức ba mươi lăm nhịp một phút.

Nhịp tim chậm đến mức nếu một bác sĩ dùng ống nghe đặt vào ngực tôi lúc này, họ sẽ nghĩ rằng người thanh niên này đang cận kề cái chết lâm sàng. Nhưng trong lăng kính của Thể Đạo, đó lại là trạng thái "Quy Tức Cùng Cực" — nơi mọi nguồn năng lượng của cơ thể được thu gom về hạch tâm, chuẩn bị cho một đợt bộc phát tôi luyện toàn diện.

*ÙNG... ÙNG...*

Từ sâu trong cuống tim tôi, dòng Thuần Dương Cương Huyết bắt đầu sôi sục trở lại.

Từng giọt máu đỏ thẫm ánh kim sắc như những dòng dung nham nóng hổi cuộn trào chảy qua các động mạch chủ, rồi phân nhánh tràn vào ba mươi ba đốt sống lưng.

Ngay khoảnh khắc Cương Huyết chạm vào cấu trúc xương sống, những tia Vô Ngân Kiếm Khí còn sót lại từ ban chiều lập tức phản ứng dữ dội!

Hàng ngàn tia kiếm mang màu bạch ngọc li ti như những hạt bụi phát sáng bắt đầu xoay tròn điên cuồng, cắt cứa vào từng thớ tủy xương. Một cơn đau xé ruột xé gan ập đến, dữ dội gấp mười lần những đòn tra tấn tàn khốc nhất trần gian. Cảm giác như có hàng vạn mũi kim thép nung đỏ đang đâm xuyên qua tủy ngọc, gọt giũa từng tế bào xương sống của tôi.

Toàn thân tôi run rẩy kịch liệt. Mồ hôi túa ra như suối, ướt đẫm tấm bạt dã chiến bên dưới, rồi bốc hơi ngùn ngụt thành từng làn khói trắng mỏng manh trong không khí đêm lạnh giá.

Tôi nghiến chặt hai hàm răng đến mức rỉ máu, giữ vững một tia thanh minh duy nhất trong tâm thức:

"Không được gục ngã! Thân thể là vỏ kiếm, ý chí là mũi kiếm! Lấy máu thịt phàm nhân trui rèn ngọc tủy!"

Tôi không dùng kình lực để chống đối hay xua đuổi luồng kiếm khí ấy. Nhớ lại lời dặn của Lâm Tịch trước khi nàng chìm vào giấc ngủ sâu, tôi chủ động mở rộng từng khe hở trong ba mươi ba đốt sống, dùng chính dòng Thuần Dương Cương Huyết bỏng rát của mình để bao bọc, thẩm thấu và đồng hóa từng tia kiếm mang cổ xưa.

Thời gian chầm chậm trôi qua giữa đêm trường hoang vắng.

Một giờ sáng... hai giờ sáng... rồi ba giờ sáng ngày hai mươi lăm tháng mười.

Khi giọt sương đêm cuối cùng rơi xuống mái tôn cũ kỹ phát ra một tiếng tách thanh mảnh, một sự chuyển hóa long trời lở đất bỗng bùng nổ bên trong cơ thể tôi.

*KENG!*

Một tiếng kiếm reo trong trẻo, trang nghiêm vang vọng từ sâu trong lồng ngực tôi, chấn động đến mức làm rung chuyển cả những hạt bụi trên sàn bê tông xung quanh.

Ba mươi ba đốt sống lưng của tôi đồng loạt tỏa ra một làn quang hoa màu bạch ngọc ánh đồng thau rực rỡ. Toàn bộ tàn dư của Vô Ngân Kiếm Khí đã hoàn toàn hòa tan vào tủy ngọc, biến cấu trúc xương sống của tôi thành một thể thống nhất vững chắc tựa kim cương bất hoại!

Vết rách do mảnh đạn trên vai trái khẽ giật giật, lớp vảy máu khô tự động bong tróc ra, để lại một làn da mới hồng hào, săn chắc như chưa từng chịu bất kỳ tổn thương nào.

Cảnh giới Luyện Cốt Hậu kỳ của tôi đã chính thức viên mãn, chạm tới đỉnh cao Cùng Cực — chỉ còn cách ngưỡng cửa Hoán Huyết một bước chân duy nhất!

Tôi từ từ mở mắt ra.

Trong bóng tối dày đặc của nhà kho bỏ hoang, tầm nhìn của tôi rõ ràng như ban ngày. Tôi có thể nhìn thấy từng đường vân rỉ sét trên cây xà bần cách xa hai mươi mét, có thể nghe thấy tiếng một con cá quẫy đuôi dưới mặt nước sông Đồng Nai cách đó hàng trăm thước.

Nhưng cùng lúc đó, tôi cũng cảm nhận được một sự thay đổi đáng sợ bên trong tâm hồn mình.

Xúc giác của tôi trở nên trầm tĩnh lạ thường. Nhịp tim tôi đập bình thản đến mức lạnh lùng. Những cảm xúc đau đớn, xót xa, phẫn nộ vừa dày vò tôi vài tiếng trước dường như đã bị một lớp màng kiếm khí vô hình đóng băng lại, chìm sâu vào đáy lòng.

Lời cảnh báo yếu ớt của Lâm Tịch một lần nữa vang vọng bên tai tôi như một tiếng chuông cảnh tỉnh:

*"Mỗi lần kiếm khí cổ xưa nhập thể, nó sẽ gọt giũa xương tủy ngươi, nhưng cũng đồng thời mài mòn đi từng chút cảm giác trần thế của ngươi..."*

Tôi cúi đầu nhìn vào hai bàn tay thô ráp đầy những vết chai sần của mình, rồi tự nắm chặt lại thành nắm đấm.

"Không... Mình không thể để bản thân bị biến thành một cỗ máy chiến đấu vô cảm!" Tôi tự nhủ với chính mình, thanh âm trầm đục vang lên giữa bóng đêm. "Mình là Nguyễn Minh An. Mình là một kỹ sư phàm nhân hai mươi lăm tuổi của đất Sài Gòn này. Mình tu luyện Thể Đạo là để bảo vệ mẹ, bảo vệ Tuấn, bảo vệ những người bình dị vô tội, chứ không phải để trở thành một kẻ tu đạo máu lạnh đứng trên đỉnh cao cô độc!"

Tôi hít sâu một hơi, để ngọn gió sông mát lành phả vào mặt, khơi gợi lại từng ký ức ấm áp về nụ cười của mẹ, về những bát cơm tấm nóng hổi bên hẻm Nơ Trang Long, về những buổi chiều ngồi uống trà đá ngắm dòng xe cộ qua cầu Sài Gòn.

Tia hàn quang sắc lạnh trong mắt tôi dần dần thu liễm, trả lại đôi mắt đen láy, kiên định và chan chứa tình người của một phàm nhân chân chính.

Tôi đứng dậy, khoác chiếc ba lô dã chiến lên vai.

Phía chân trời đằng đông, qua khỏi những rặng dừa nước ven sông Đồng Nai, một vệt rạng đông màu hồng nhạt bắt đầu hé lộ, xua tan màn đêm u tối.

Tôi phóng tầm mắt nhìn về phía Tây Nam — nơi dòng sông Tiền hiền hòa đang chở nặng phù sa nuôi dưỡng những cù lao xanh mướt của quê hương.

Một kế hoạch tác chiến rõ ràng đã định hình trong đầu tôi:

Tôi sẽ không trốn chạy, cũng không manh động đối đầu trực diện với tổng bộ Cửu Long Thiên Hải khi chưa chuẩn bị đầy đủ. Tôi sẽ bí mật xuôi về miền Tây bằng con đường sông nước, âm thầm thiết lập một mạng lưới bảo vệ kiên cố xung quanh mẹ tôi mà không làm kinh động đến cuộc sống bình yên của bà. Đồng thời, tôi sẽ điều tra xem liệu mạng lưới Thủy Môn Thập Nhị Tiêu ở vùng đồng bằng châu thổ sông Cửu Long còn những cọc tiêu nào đang bị bàn tay hắc ám của kẻ thù dòm ngó.

Chiếc Wave Alpha lại nổ máy, đưa tôi rời khỏi bãi hoang ven sông, bắt đầu một chặng đường dạ hành mới đầy cam go và thử thách!'''

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
        "Dạ Hành Độc Lộ, Mưa Đêm Quốc Lộ & Trui Rèn Ngọc Tủy",
        CHAPTER_NUM,
        1,
        f"{DATE}T23:30:00+07:00",
        CHAPTER_NUM,
        "loc_ven_song_dong_nai",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An rút lui khỏi Núi Chứa Chan, lấy lại xe máy tại nhà dân và hòa vào dòng xe Quốc lộ 1A. Đối mặt với sự im lặng tuyệt đối của Lâm Tịch khi nàng chìm vào trầm miên sâu trong thức hải rạn nứt. Trong cơn mưa đêm Trảng Bom, Minh An nhận tin báo từ Tuấn về việc Cửu Long Thiên Hải tấn công hệ thống dữ liệu Viện Địa tầng để truy tìm thân nhân, đồng thời cắn răng nuốt nước mắt không gọi điện cho người mẹ già ở cù lao Tiền Giang để bảo vệ an toàn cho bà. Dừng chân tại bãi xưởng bỏ hoang ven sông Đồng Nai lúc nửa đêm, Minh An vận hành Quy Tức Quyết và Thuần Dương Cương Huyết tôi luyện tủy ngọc, thuần hóa toàn bộ tàn dư Vô Ngân Kiếm Khí, đạt cảnh giới Luyện Cốt Hậu kỳ Cùng Cực. Nhận thức sâu sắc nguy cơ bị kiếm khí mài mòn nhân tính, Minh An giữ vững bản tâm phàm nhân và hướng tầm mắt về miền Tây Nam mở ra hành trình bảo vệ thầm lặng.",
        "Thể phách Minh An đạt Luyện Cốt Hậu kỳ Cùng Cực; tàn dư kiếm khí hòa tan vào tủy ngọc; Tuấn sơ tán an toàn sang Quận 7; Minh An quyết định bí mật xuôi về Tiền Giang thiết lập mạng lưới phòng thủ bảo vệ mẹ già."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-TRG-001'
    """, (
        CHAPTER_NUM,
        "Minh An nuốt nước mắt không gọi điện cho mẹ ở Tiền Giang để tránh để lộ vị trí; Tuấn sơ tán sang Quận 7; Minh An chấp nhận gánh nặng cô độc của kẻ thủ hộ."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An thuần hóa Vô Ngân Kiếm Khí trong ba mươi ba đốt sống lưng, tủy ngọc viên mãn đạt Luyện Cốt Hậu kỳ Cùng Cực; đứng trước ngưỡng cửa Hoán Huyết."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch chìm sâu vào trầm miên dài hạn với đài sen rạn nứt xám tro; Minh An hoàn toàn tự lực cánh sinh trong mọi quyết định sinh tử."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T23:30:00+07:00"
        inv_data["current_location"] = "Khu Bến Bãi Hoang Ven Sông Đồng Nai, Dĩ An - Thủ Đức"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ Cùng Cực (33 Đốt Sống Ngọc Tủy Viên Mãn / Chuẩn Bị Hoán Huyết)"
        
        # Cập nhật tình trạng Trâm Ngọc Lâm Tịch
        for itm in inv_data.get("core_weapons_and_artifacts", []):
            if "Lâm Tịch" in itm.get("name", ""):
                itm["condition"] = "Đài sen thu nhỏ bằng bàn tay, vết rạn xám tro kéo dài, Lâm Tịch rơi vào trầm miên sâu dài hạn"
                itm["durability"] = "75/100"

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

# -*- coding: utf-8 -*-
"""Draft Chapter 91 for Phá Trời Novel OS: Bụi Đỏ Đại Ngàn.
Prose length: ~3,800 words (standard: 3,200 - 4,500 words), zero meta-words, zero 'huyết mạch', severe grounding, geological realism, Tây Nguyên folklore, and Chư Yang Sin approach.
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

CHAPTER_NUM = 91
CHAPTER_TITLE = "Bụi Đỏ Đại Ngàn"
DATE = "2026-11-02"
LOCATION = "Quốc Lộ 14, Buôn Đôn & Cửa Ngõ Vườn Quốc Gia Chư Yang Sin, Tỉnh Đắk Lắk"

ACT1 = '''Sáu giờ sáng ngày mùng hai tháng mười một.

Bầu trời thành phố còn chưa tan hết hơi sương ẩm ướt của một sớm đầu đông. Trước cổng Viện Nghiên cứu Địa tầng trên đường Mạc Đĩnh Chi, ba chiếc xe bán tải chuyên dụng hai cầu loại dã chiến màu xanh rêu đã nổ máy cầm chừng từ lâu, tiếng động cơ dầu rền vang giòn giã.

Trên nóc mỗi chiếc xe đều được lắp đặt giàn thép chịu lực chở đầy các hòm nhôm chống sốc chứa cọc cảm biến vi địa chấn sâu, bình ắc-quy dự phòng dung lượng cao và chảo thu phát vệ tinh di động. Hai bên sườn xe dán logo phản quang màu cam nổi bật của Đoàn Khảo sát Trắc địa Quốc gia.

Tôi khoác lên mình bộ trang phục dã chiến vải dù màu xanh rêu bền chắc, chân xỏ đôi ủng cổ cao chuyên dụng đi rừng bằng cao su non đúc nguyên khối có gai bám chống trơn trượt. Chiếc ba-lô quân dụng nặng hơn hai mươi ký sau lưng tôi được sắp xếp vô cùng gọn gàng. Ngoài tư trang cá nhân, đòn bánh tét đậu xanh thịt mỡ và hũ mắm cá sặc của mẹ, bên trong ba-lô là hai thanh vũ khí tùy thân bọc kín vải dù: Hắc Thiết Đoản Côn và Trấn Thủy Đoản Đao. Nằm sâu ở đáy ba-lô, khối Mộc Hoàng Lôi Tâm Thạch bọc nhiều lớp da nai rừng sấy khô vẫn tỏa ra một luồng nhiệt lượng ấm áp, như một lò sưởi vô hình sưởi ấm vùng thắt lưng của tôi.

Kỹ sư Tuấn bước từ trong sảnh lớn ra, tay xách chiếc va-li hợp kim chứa máy tính phân tích ma trận dữ liệu thời gian thực. Anh mặc chiếc áo gi-lê kỹ thuật nhiều túi, đội chiếc mũ tai bèo phong trần, nhìn thấy tôi liền toe toét cười:

"Chào Đội trưởng An! Tối qua ngủ nghê thế nào? Nhìn thần sắc chú mày sáng sủa, tinh anh dữ nghen, hai con mắt sáng quắc như đèn pha vậy!"

"Em ngủ ngon lắm anh Tuấn. Trang thiết bị đo đạc vi chấn đã kiểm tra thông số lần cuối chưa anh?"

"Chuẩn chỉ từng con ốc rồi chú mày! Ba mươi đầu dò cảm biến quang học ngầm sâu đã nạp đầy năng lượng, cáp truyền dẫn bọc sợi kevlar chống chuột cắn và chống nước áp lực cao đã chuẩn bị sẵn ba ngàn mét. Lần này vào rừng sâu Chư Yang Sin, dù có mưa rừng gió rét cỡ nào cũng bảo đảm truyền dữ liệu về tổng bộ thông suốt từng giây!"

Đúng sáu giờ ba mươi phút, Viện trưởng Trịnh Hoài Nam bước ra. Ông mặc bộ đồ dã chiến bạc màu của người lính trinh sát địa chất năm xưa, mái tóc hoa râm bay trong gió sớm, ánh mắt tràn đầy vẻ quyết đoán:

"Tất cả các tổ kiểm tra lại tần số bộ đàm nội bộ. Đoàn xe xuất phát!"

Ba chiếc xe bán tải từ từ lăn bánh, rẽ qua đường Đinh Tiên Hoàng rồi hòa vào dòng xe cộ ban mai, vượt cầu Bình Triệu để tiến vào Quốc lộ 13, sau đó nhập vào tuyến Quốc lộ 14 — con đường thiên lý huyền thoại chạy dọc sống lưng Trường Sơn Tây.

Chiếc xe chở tôi, Tuấn và Viện trưởng Nam dẫn đầu đoàn. Bác tài xế trạc ngoài bốn mươi tuổi, một tay lái dạn dày kinh nghiệm từng nhiều năm chở các đoàn khảo sát địa chất băng đèo vượt suối, giữ tốc độ ổn định bảy mươi cây số một giờ.

Rời khỏi vùng phụ cận Bình Dương, con đường bắt đầu lướt qua những cánh rừng cao su bạt ngàn của tỉnh Bình Phước. Từng hàng cây cao su thẳng tắp đang mùa thay lá, những tán lá màu vàng cam và đỏ ối rụng đầy hai bên vệ đường tạo nên một khung cảnh trầm mặc, tĩnh lặng.

Qua khỏi ngã ba Đồng Xoài, địa hình bắt đầu dâng cao rõ rệt. Những con dốc thoai thoải nhường chỗ cho những khúc cua tay áo uốn lượn men theo sườn đồi dốc đứng. Đất thịt phù sa màu xám xịt của vùng hạ lưu hoàn toàn biến mất, thay vào đó là màu đỏ rực rỡ, nồng nàn của đất đỏ bazan Tây Nguyên.

Bụi đỏ bazan mịn như nhung bốc lên theo từng vòng bánh xe lăn, bám một lớp mỏng lên kính chắn gió và thành xe.

Tôi hạ khung cửa kính xuống một nửa, hít sâu một hơi luồng không khí cao nguyên bắt đầu trở nên loãng dần và se lạnh. Gió đại ngàn thổi qua những rặng thông và đồi cà phê bạt ngàn, xộc vào khoang ngực tôi một luồng sinh khí thơm mùi nhựa cây, mùi đất đỏ nung dưới nắng và hương hoa dã quỳ nở vàng rực rỡ dọc hai bên sườn đồi.

Dưới làn da của tôi, dòng Thuần Dương Cương Huyết sơ kỳ sau một đêm hấp thu tia lôi khí từ khối Mộc Tâm bỗng khẽ rạo rực. Ba mươi ba đốt sống tủy ngọc thấu suốt một dải ánh sáng ấm áp, tự động điều chỉnh nhịp tuần hoàn để thích ứng với sự thay đổi của độ cao và áp suất khí quyển. Toàn thân tôi không hề có một chút cảm giác mệt mỏi hay say xe, trái lại, các khớp xương và thớ cơ càng lúc càng trở nên dẻo dai, sung mãn lạ thường.'''

ACT2 = '''Mười hai giờ ba mươi phút trưa.

Đoàn xe vượt qua địa phận thị xã Gia Nghĩa của tỉnh Đắk Nông, tiến thẳng vào cao nguyên Đắk Lắk và dừng lại ăn trưa tại một quán ăn nhỏ của đồng bào ven quốc lộ, cách thành phố Buôn Ma Thuột chừng ba mươi cây số.

Không gian xung quanh ngập tràn hương vị phóng khoáng của đất đỏ đại ngàn.

Bữa trưa dã chiến được dọn ra trên những chiếc mẹt tre lót lá chuối tươi: cơm lam nướng trong ống nứa nếp nương thơm dẻo quánh, một con gà đồi nướng than hoa vàng ươm da giòn rụm chấm với muối ớt rừng giã lá é xanh mướt cay xè, đĩa đọt mây xào lòng gà giòn sần sật, và một tô canh cà đắng nấu cá suối đậm đà phong vị bản địa.

Viện trưởng Nam rót cho mỗi người một ly trà xanh hái từ đồi chè cổ Cầu Đất, mỉm cười nói:

"Ăn no vào các cậu, nạp đầy năng lượng đi. Từ Buôn Ma Thuột rẽ vào Buôn Đôn và tiến vào chân núi Chư Yang Sin đường sá gập ghềnh đá hộc dữ lắm, chiều nay chúng ta sẽ phải lội bộ khảo sát địa hình thực địa nhiều đấy."

Tôi bẻ một khúc cơm lam nóng hổi chấm vào đĩa muối ớt rừng, nhai chậm rãi. Vị bùi dẻo của nếp nương hòa quyện với vị cay nồng của ớt hiểm và vị mặn mà của muối hột bùng nổ trong khoang miệng.

Ăn xong bữa trưa, trong lúc các đồng nghiệp ngồi thưởng thức tách cà phê Robusta đen đặc sánh thơm lừng của vùng đất Buôn Ma Thuột, tôi một mình bước ra khoảng sân đất trống phía sau quán ăn.

Tôi tháo đôi ủng dã chiến, để đôi bàn chân trần dẫm trực tiếp lên lớp đất đỏ bazan mịn màng dưới bóng râm của một cây kơ-nia cổ thụ tỏa bóng xum xuê.

Khoảnh khắc lòng bàn chân tiếp xúc với mặt đất đỏ, một cảm giác kỳ diệu khó tả lập tức truyền thẳng lên dọc sống lưng tôi.

Đất đỏ bazan nơi đây được hình thành từ những dòng nham thạch núi lửa phun trào từ hàng triệu năm trước. Nó khô ráo, xốp mịn, giàu khoáng chất sắt, titan và tích tụ một nguồn từ trường tự nhiên vô cùng mãnh liệt. Khác hẳn với đất bùn phù sa mềm mại, bao dung và ẩm ướt của cù lao sông Tiền, địa khí của đất đỏ Tây Nguyên cương mãnh, nóng bỏng và ẩn chứa một nguồn nhiệt lượng nội sinh dồi dào tựa như một đống than hồng đang âm ỉ cháy sâu dưới đáy vực.

Hai lòng bàn chân tôi bấm chặt vào đất đỏ, huyệt Dũng Tuyền mở rộng.

Dưới sự kích thích của từ trường bazan, dòng **Thuần Dương Cương Huyết** trong cơ thể tôi tự động tăng tốc tuần hoàn. Những hạt năng lượng lôi điện tím vàng vốn được tôi thuần hóa đêm qua trong tủy sống khẽ chớp sáng, tựa như tìm thấy một mảnh đất màu mỡ để bén rễ sinh sôi. Dòng máu mang theo kình lực cương mãnh chảy rào rạt qua từng nhánh kinh mạch, khiến làn da đồng thau của tôi ửng lên một lớp hồng hào tràn đầy sinh lực.

Trong thức hải bao la, Bạch Y Thần Nữ Lâm Tịch ngự trên đài sen Lục Diệp Thanh Liên, đôi mắt trong veo ngước nhìn ra thế giới bên ngoài qua giác quan của tôi. Nàng khẽ gật đầu, truyền âm thanh tao:

"Mảnh đất này quả thực phi thường. Dãy Trường Sơn hùng vĩ này chính là bộ xương sống của non sông đất nước anh. Đất đỏ bazan giàu khoáng chất kim loại và từ tính chính là lớp vỏ bọc bảo hộ hoàn hảo nhất cho các mạch ngầm viễn cổ. Thể Đạo của anh lấy Thuần Dương làm gốc, khi đặt chân lên vùng đất lửa cổ xưa này sẽ như rồng gặp mây, hổ thêm cánh. Hãy tận dụng chuyến đi này để rèn giũa cốt tủy đến độ thuần khiết nhất."

"Tôi hiểu rồi, Lâm Tịch. Càng đi xa, tôi càng thấy đất nước mình ẩn chứa những điều kỳ diệu vượt xa trí tưởng tượng của phàm nhân." Tôi đáp lại bằng một nụ cười điềm đạm.

Hai giờ chiều, tiếng còi xe của bác tài vang lên giục giã. Tôi xỏ chân vào đôi ủng, khoác ba-lô bước lên xe tiếp tục hành trình hướng về Buôn Đôn.'''

ACT3 = '''Bốn giờ ba mươi phút chiều.

Rời Quốc lộ 14, đoàn xe rẽ vào tỉnh lộ 1 chạy ngoằn ngoèo qua những cánh rừng khộp rụng lá đặc trưng của vùng Buôn Đôn. Khung cảnh hai bên đường mở ra với những nếp nhà dài bằng gỗ cà chít truyền thống của đồng bào Ê Đê, sàn nhà cao lêu nghêu dựng trên những thân cột gỗ lim to bằng hai người ôm để chống thú dữ.

Dòng sông Sêrêpôk huyền thoại hiện ra trước mắt chúng tôi.

Mặt nước sông màu đỏ gạch cuộn trào sóng dữ, rẽ qua những ghềnh đá bazan đen nhánh lởm chởm. Đây là con sông kỳ lạ nhất phương Nam — dòng sông chảy ngược dòng về hướng tây để đổ sang đất bạn Campuchia trước khi hòa vào dòng Mê Kông vĩ đại.

Đoàn xe vượt qua cây cầu treo bắc qua dòng sông cuộn sóng, men theo con đường đất đỏ gồ ghề đầy đá tảng lổn nhổn để tiến thẳng về phía Trạm Kiểm lâm số 4 — trạm gác tiền tiêu nằm ngay tại vùng đệm giáp ranh vùng lõi Vườn Quốc gia Chư Yang Sin.

Dãy núi Chư Yang Sin sừng sững hiện ra nơi chân trời phía đông nam.

Đỉnh núi cao nhất cao hơn hai ngàn bốn trăm mét chìm ngập trong những dải mây mù xám bạc cuồn cuộn. Những vách đá hoa cương và đá bazan dựng đứng tựa như bức tường thành khổng lồ của tạo hóa, ngăn cách dải đồng bằng duyên hải miền Trung với cao nguyên đất đỏ lộng gió.

Tại sân trạm kiểm lâm, một chiếc xe bán tải chuyên dụng của Hạt Kiểm lâm Krông Bông đã chờ sẵn.

Người bước ra đón đoàn là Trạm phó trạm kiểm lâm — một người đàn ông Ê Đê trạc ngoài năm mươi tuổi tên là Y Krông. Ông có vóc dáng vạm vỡ, nước da ngăm đen bóng bẩy như gỗ mun, hai bắp tay gân guốc cuồn cuộn và đôi mắt sáng quắc như chim ưng săn mồi.

Viện trưởng Nam bước xuống xe, vừa nhìn thấy Y Krông liền bước nhanh tới, hai người đàn ông ôm chầm lấy nhau mừng rỡ:

"Y Krông! Ba mươi năm rồi mới gặp lại cậu! Vẫn khỏe mạnh, rắn rỏi như cây kơ-nia giữa rừng già thế này à!"

"Bác Nam! Già làng trong buôn bảo hôm nay chim chơ-rao hót trên mái nhà sàn là có khách quý phương xa tới, không ngờ là bác!" Y Krông cười lớn, tiếng cười sảng khoái vang vọng cả góc rừng: "Nghe tin Viện Địa chất khẩn cấp cử đoàn lên khảo sát núi Mẹ Chư Yang Sin, già làng cử tôi ra đón các bác vào nhà sàn uống ché rượu cần ngay!"

Trong lúc mọi người đang bốc dỡ các hòm thiết bị từ thùng xe xuống sân trạm, tôi bước tới giúp khiêng một thùng cảm biến nặng hơn sáu mươi ký. Thấy tôi một tay nhấc bổng chiếc hòm kim loại nặng trịch nhẹ nhàng như không, đôi mắt sắc sảo của Y Krông khẽ nhíu lại kinh ngạc.

Khi tôi móc chiếc bật lửa Zippo vỏ đồng ra khỏi túi để châm mồi lửa giúp một anh kiểm lâm nhóm bếp đun nước sôi, ánh mắt Y Krông bỗng dán chặt vào những vết xước dăm đặc trưng và dòng chữ khắc mờ dưới đáy bật lửa.

Người đàn ông Ê Đê bỗng sững sờ, giọng ông run lên lạc đi:

"Cậu thanh niên... Chiếc bật lửa này... Có phải của thợ mộc Nguyễn Văn Hùng năm xưa không?"

Tôi giật mình, ngước nhìn Y Krông:

"Dạ đúng, đó là cha của cháu. Bác từng quen biết cha cháu sao?"

Y Krông bước tới, hai bàn tay thô ráp của ông nắm chặt lấy bờ vai tôi, đôi mắt ngấn lệ xúc động:

"Trời đất ơi! Cậu là con trai của anh Hùng thợ mộc! Năm 1996, cha cậu cùng bác Sáu Kiên từng ở lại nhà sàn của gia đình tôi suốt sáu tháng trời để làm nhà rông và đục mộng xà lim cho buôn làng! Hồi đó tôi mới là một chàng trai mười tám tuổi theo cha cậu đi rừng vác gỗ. Cha cậu là người thợ mộc giỏi nhất, trầm tính nhất và tốt bụng nhất mà buôn làng tôi từng gặp!"

Cuộc hội ngộ bất ngờ giữa đại ngàn khiến toàn bộ không khí của đoàn khảo sát như lắng đọng lại trong sự ấm áp thiêng liêng của tình người.

Y Krông kéo tôi ngồi xuống bậc thang nhà sàn, giọng ông trầm xuống đầy vẻ huyền bí:

"An này, cha cậu năm xưa cùng bác Sáu Kiên đào được khối đá lạ dưới chân núi Mẹ, người trong buôn ai cũng biết. Người Ê Đê chúng tôi từ ngàn đời nay đều tin rằng, trong lòng dãy Chư Yang Sin có Thần Sấm Yang Lôi ngự trị. Ba ngày nay, rừng già bỗng biến động dữ dội. Những đàn voi rừng ngoài thung lũng Ea Súp tự nhiên bỏ rừng sâu chạy dạt về hạ nguồn, chim chóc bay tán loạn không dám đậu trên các ngọn cây cao. Đêm nào dưới lòng đất sâu cũng vọng lên những âm thanh ầm ầm tựa như tiếng trống trận của tổ tiên. Các già làng đang rất lo lắng. Chuyến đi này của các cậu, thần linh đại ngàn dường như đã sắp đặt sẵn để con trai của người thợ mộc năm xưa trở về giải mã bí mật của núi Mẹ!"'''

ACT4 = '''Tám giờ ba mươi phút tối.

Màn đêm buông xuống đen đặc như mực trên cánh rừng già Chư Yang Sin. Gió đại ngàn thổi qua các khe núi đá hú lên từng hồi rùng rợn, mang theo cái lạnh buốt xương của vùng núi cao hơn ngàn mét. Giữa sân trạm kiểm lâm, một đống lửa lớn bằng gỗ trắc khô đang bùng cháy bập bùng, tỏa ra những tàn lửa đỏ rực bay lên trời đêm đầy sao.

Bên trong gian phòng làm việc dã chiến của trạm kiểm lâm, tôi và kỹ sư Tuấn đang cặm cụi lắp ráp cụm trạm thu phát cảm biến ma trận số 1.

Mũi cọc cảm biến titan dài ba mét đã được tôi dùng đôi tay trần đóng ngập sâu vào lòng đất đỏ bazan cứng như đá ở góc sân trạm mà không cần dùng đến búa máy. Dây cáp quang học bọc sợi kevlar được nối thẳng vào máy tính chủ dã chiến đặt trên bàn gỗ.

"Tít... Tít... Rè..."

Màn hình máy tính bỗng chớp sáng dữ dội. Biểu đồ sóng vi chấn ba chiều lập tức nhảy vọt lên những dải biên độ sắc nhọn!

"Chú An! Nhìn này!" Tuấn ghé mắt sát vào màn hình, giọng nói nghẹn lại vì phấn khích: "Ở đây tín hiệu vi chấn rõ nét gấp mười lần so với lúc chúng ta đo ở Sài Gòn! Tần số đúng 0.10 Hertz, chu kỳ xung lực phát ra đều đặn mười tám phút một lần! Điểm phát xung lực nằm chính xác tại tọa độ đỉnh Chư Yang Sin, cách chúng ta mười lăm cây số đường chim bay xuyên qua vùng lõi rừng rậm!"

Tôi chăm chú quan sát đồ thị sóng.

Đúng lúc đó, từ bên trong chiếc ba-lô dã chiến đặt cạnh chân tôi, khối **Mộc Hoàng Lôi Tâm Thạch** bỗng rung lên bần bật!

Một luồng sóng xung chấn cực kỳ trầm thấp từ khối đá đen nhánh phát ra, truyền thẳng qua lớp vải dù, đập vào mắt cá chân tôi. Tần số dao động của khối lôi thạch vừa vặn trùng khớp một trăm phần trăm với dải sóng 0.10 Hertz đang nhảy múa trên màn hình máy tính của Tuấn!

Cùng lúc đó, thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao đặt trong bao bạt dứa cũng phát ra những tiếng ngân rung nhè nhẹ tựa như tiếng gió rít qua rặng thông.

Trong thức hải, Lâm Tịch xuất hiện trên Lục Diệp Thanh Liên, giọng nàng vang lên đầy vẻ cảnh giác:

"Minh An, trận nhãn Thổ Mộc dưới chân đỉnh Chư Yang Sin đang phản hồi lại khối lôi thạch của anh. Vùng lõi rừng già phía trước không chỉ có địa hình hiểm trở, mà trường điện từ của trận nhãn đang làm biến đổi sinh thái của khu rừng. Cây cối, độc trùng và dã thú nơi đó có thể đã bị lôi khí kích thích trở nên hung dữ dị thường. Ngày mai khi tiến sâu vào rừng, anh phải luôn giữ cho dòng Thuần Dương Cương Huyết vận hành ở trạng thái sẵn sàng chiến đấu."

"Tôi hiểu rồi, Lâm Tịch. Tôi đã sẵn sàng." Tôi điềm tĩnh đáp lại trong tâm thức.

Tôi bước ra lan can nhà sàn, đứng đón luồng gió lạnh buốt từ đại ngàn thổi tới.

Trước mắt tôi, dãy núi Chư Yang Sin sừng sững tựa như một con cự long thời tiền sử đang nằm phủ phục trong bóng đêm dày đặc. Những vách đá đen thẫm mờ ảo dưới ánh trăng mờ, thỉnh thoảng trên những tầng mây bao quanh đỉnh núi lại lóe lên những tia chớp lân tinh không tiếng động — dấu hiệu của lôi đình địa tầng đang cuộn trào tích tụ.

Tôi siết chặt nắm tay, cảm nhận nguồn kình lực dũng mãnh của Hoán Huyết Sơ kỳ đang cuộn chảy rào rạt trong từng thớ cơ bắp.

Ngày mai, cuộc hành quân xuyên rừng già tiến vào tâm bão lôi đình sẽ chính thức bắt đầu!'''

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
        active_characters=["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"],
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
description: "Đoàn khảo sát xuất phát theo Quốc lộ 14 tiến vào cao nguyên Đắk Lắk; Minh An giao hòa thể phách cùng đất đỏ bazan giàu từ tính; cuộc gặp gỡ xúc động với già Y Krông tại Buôn Đôn hé lộ ký ức người cha năm 1996; đêm đầu tiên tại cửa rừng Chư Yang Sin ghi nhận sóng vi chấn 0.10 Hz trùng khớp Mộc Hoàng Lôi Tâm Thạch."
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
        "Đoàn Khảo Sát Tiến Vào Buôn Đôn, Gặp Già Y Krông & Ghi Nhận Xung Chấn Chư Yang Sin",
        CHAPTER_NUM,
        1,
        f"{DATE}T20:30:00+07:00",
        CHAPTER_NUM,
        "loc_tram_kiem_lam_chu_yang_sin",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"]),
        "Đoàn khảo sát xuất phát theo Quốc lộ 14 tiến vào cao nguyên Đắk Lắk. Minh An giao hòa thể phách cùng đất đỏ bazan giàu từ tính, củng cố Thuần Dương Cương Huyết. Chiều cùng ngày đến Trạm Kiểm lâm số 4 Buôn Đôn, gặp Trạm phó Y Krông — người từng theo cha Minh An học việc làm mộc năm 1996, được nghe truyền thuyết Thần Sấm Chư Yang Sin và sự biến động của đàn voi rừng. Đêm muộn lắp ráp trạm cảm biến số 1, bắt được sóng vi chấn 0.10 Hz dội về từ đỉnh núi Chư Yang Sin trùng khớp hoàn toàn với nhịp rung của khối Mộc Hoàng Lôi Tâm Thạch.",
        "Đoàn khảo sát đến tiền trạm an toàn; Minh An kết nối mối duyên cũ của cha tại Buôn Đôn; xác nhận tọa độ xung chấn Chư Yang Sin."
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
        "Đoàn khảo sát cắm chốt tại Trạm Kiểm lâm Chư Yang Sin, bắt sóng vi chấn 0.10 Hz trùng khớp khối Mộc Tâm, chuẩn bị tiến sâu vào vùng lõi rừng già."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Thể Đạo Hoán Huyết sơ kỳ của Minh An dung hợp mãnh liệt cùng từ trường đất đỏ bazan Tây Nguyên, Thuần Dương Cương Huyết đạt độ dẻo dai và dũng mãnh mới."
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
        inv_data["current_location"] = "Trạm Kiểm Lâm Số 4, Vùng Đệm Vườn Quốc Gia Chư Yang Sin, Tỉnh Đắk Lắk"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Thể Đạo Giao Hòa Đất Đỏ Bazan / Khí Huyết Lôi Hóa Nhập Môn)"

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

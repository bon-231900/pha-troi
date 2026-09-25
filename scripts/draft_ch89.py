# -*- coding: utf-8 -*-
"""Draft Chapter 89 for Phá Trời Novel OS: Khói Bếp Cù Lao.
Prose length: ~4,150 words (standard: 3,200 - 4,500 words), zero meta-words, zero 'huyết mạch', severe grounding, deep pathos, mortal body cultivation harmony, and Tây Nguyên foreshadowing.
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

CHAPTER_NUM = 89
CHAPTER_TITLE = "Khói Bếp Cù Lao"
DATE = "2026-10-31"
LOCATION = "Cù Lao Ven Sông Tiền, Huyện Chợ Gạo, Tỉnh Tiền Giang"

ACT1 = '''Năm giờ ba mươi phút sáng ngày ba mươi mốt tháng mười.

Màn sương sớm bảng lảng còn đọng trên những tán cây sao đen dọc đại lộ Võ Văn Kiệt. Không khí ban mai se lạnh, thoang thoảng mùi hương cà phê vợt thơm lừng từ những chiếc xe đẩy nhỏ nép bên góc đường của các cô chú lao động nghèo.

Tôi mặc chiếc áo sơ mi bạc màu, quần kaki sờn gối và đôi dép quai hậu cũ. Trên lưng chỉ là chiếc ba lô vải dù nhỏ gọn. Hắc Thiết Đoản Côn và Trấn Thủy Đoản Đao nặng trịch sát khí đã được tôi cẩn thận bọc vải dù dệt thô, khóa kỹ trên chiếc giá gỗ trong phòng trọ Nơ Trang Long. Trở về với mẹ hiền, tôi không muốn mang theo bất kỳ thứ binh khí tanh mùi kim khí nào. Trong ba lô lúc này chỉ có hai bộ quần áo thường ngày, hai hộp trà lài búp sen, ba lọ cao xoa bóp thảo dược giúp mẹ làm dịu đi những cơn đau nhức xương khớp mỗi khi trở trời, cùng chiếc bật lửa Zippo vỏ đồng đã mòn nhẵn góc cạnh của cha tôi để lại.

Rời con hẻm nhỏ Bình Thạnh, tôi đón chuyến xe buýt sớm chạy thẳng về bến xe Miền Tây.

Khu bến xe buổi sớm nhộn nhịp một cách thân thương. Tiếng còi xe đò bấm inh ỏi, tiếng người lơ xe đon đả gọi khách về các tỉnh miền Tây: Mỹ Tho, Bến Tre, Gò Công, Trà Vinh... Những sọt mây chất đầy thanh long đỏ rực, cần xé bưởi da xanh và buồng dừa tươi tỏa ra mùi hương cây trái miệt vườn ngọt ngào, đậm đà phù sa.

Tôi bước lên chiếc xe đò ba mươi chỗ tuyến Sài Gòn đi Chợ Gạo. Bác tài xế trạc ngoài năm mươi, khuôn mặt vuông chữ điền đen sạm vì nắng gió đường dài, nhìn thấy tôi liền gật đầu cười niềm nở:

"Về miệt Chợ Gạo hả chú em? Ngồi băng ghế thứ tư bên cửa sổ cho thoáng gió nghen, xe chạy liền bây giờ đây!"

Tôi kéo chiếc ba lô ôm vào lòng, ngồi xuống chiếc ghế da đã nứt rạn theo năm tháng. Chiếc xe đò từ từ chuyển bánh, lướt qua những đại lộ rồi bon bon tiến vào dải quốc lộ hướng về cửa ngõ miền Tây.

Hai bên đường, cảnh sắc thành thị dần nhường chỗ cho những mảng xanh bát ngát của đồng bằng sông Cửu Long. Vừa qua khỏi địa phận Bến Lức, con sông Vàm Cỏ Đông hiện ra phẳng lặng dưới ánh nắng ban mai, mặt nước màu xanh biếc hòa lẫn với những dải lục bình tím ngát trôi bồng bềnh xuôi dòng.

Những cánh đồng lúa đang vào vụ gặt trải dài tít tắp đến tận chân trời. Mùi rơm rạ mới thơm nồng ngai ngái bốc lên từ những thửa ruộng vừa gặt xong, quyện chặt với làn gió mát lành thổi qua khung cửa kính mở toang, ùa vào lồng ngực tôi một luồng sinh khí thanh khiết.

Dưới làn da của tôi, ba mươi ba đốt sống tủy ngọc thấu suốt một dải ánh sáng ấm áp.

Dòng Thuần Dương Cương Huyết sơ kỳ không hề sôi trào cuồng bạo như lúc tôi tử chiến với đám tà tu ngoài cửa biển hay trên bán đảo Thanh Đa, mà chảy trôi chậm rãi, nhu hòa tựa như dòng phù sa bồi đắp cho bờ bãi châu thổ. Sau những trận huyết chiến khốc liệt, đây là lần đầu tiên tôi cảm nhận được sự lắng đọng hoàn mỹ nhất của thể xác. Từng nhịp đập của trái tim tôi hòa cùng nhịp bánh xe lăn trên mặt đường, hòa vào tiếng gió thổi qua cánh đồng rơm rạ, nhẹ nhõm và an yên đến lạ kỳ.

Người ngồi bên cạnh tôi là một cụ già tóc bạc phơ mặc áo bà ba nâu gụ, dưới chân cụ là chiếc làn cói đựng vài con cá tai tượng và nải chuối sứ vàng ươm. Thấy tôi chăm chú nhìn ra đồng lúa, cụ già nở nụ cười móm mém:

"Chú em đi làm ăn trên Sài Gòn lâu ngày mới có dịp về thăm quê hả?"

"Dạ thưa ông, cháu làm việc trên thành phố, mấy tháng nay bận bịu công trình ngoài xa nên chưa về được. Bữa nay rảnh việc, cháu tranh thủ về thăm mẹ ở cù lao."

"Ờ, phải vậy chớ chú em! Làm gì thì làm, có tiền bạc bao nhiêu cũng không bằng bữa cơm quây quần bên mẹ cha dưới mái nhà lá quê mình. Miệt Chợ Gạo đợt này trúng mùa dưa hấu với thanh long dữ lắm, phù sa đầu nguồn đổ về đỏ ngầu sông, cây trái ngọt lịm hà!"

Tiếng trò chuyện mộc mạc của ông cụ, tiếng radio trên xe đò đang phát khúc Nam Xuân réo rắt... Tất cả như dòng suối trong lành gột rửa mọi bụi bặm và hiểm nguy ra khỏi tâm trí tôi.'''

ACT2 = '''Tám giờ bốn mươi phút sáng.

Chiếc xe đò tấp vào ngã ba đường nhựa nhỏ rợp bóng mát thuộc huyện Chợ Gạo. Tôi cảm ơn bác tài xế rồi nhảy xuống vệ đường đất đỏ, hít một hơi thật sâu luồng không khí đượm nồng vị phù sa và hương dừa nước.

Từ ngã ba này, tôi rẽ vào con đường đan nhỏ dài hơn hai cây số dẫn ra bến đò sang cù lao. Con đường làng uốn lượn dưới những rặng dừa xiêm trĩu quả soi bóng xuống mặt nước rạch êm đềm. Hai bên bờ, những vạt dừa nước mọc chồm ra mép bùn, từng chùm lá xòe rộng che rợp ánh nắng sớm. Vài chú chim bìm bịp cất tiếng kêu trầm đục báo hiệu con nước ròng đang cạn đáy. Một chiếc ghe tam bản chở đầy bông điên điển vàng rực lướt qua, đuôi tôm khuấy động tạo thành những vệt sóng trắng vỗ ì oạp vào chân bờ.

Tôi bước nhanh trên con đường đan quen thuộc. Từng bờ cây, bụi cỏ, chiếc cầu khỉ bắc qua mương vườn nhỏ đều in đậm trong ký ức tuổi thơ nghèo khó nhưng êm đềm của tôi. Nơi đây cha từng dắt tay tôi đi câu cá, mẹ từng gánh đôi quang gánh trĩu nặng rau quả ra chợ từ lúc gà gáy le te để chắt chiu từng đồng nuôi tôi ăn học nên người.

Đi hết con đường đan, trước mắt tôi hiện ra bờ rào dâm bụt trổ hoa đỏ thắm, bao bọc lấy khoảng sân đất nện rợp bóng giàn hoa thiên lý.

Phía sau rào dâm bụt là ngôi nhà lá ba gian vách ván mộc mạc, mái lợp lá dừa nước đã ngả màu xám bạc theo nắng mưa.

Dưới chái bếp nhỏ, làn khói lam nhạt nhòa đang bảng lảng bay lên, hòa cùng mùi thơm của rơm mục và lá khô un bếp. Bên chiếc bàn tre con đặt cạnh khạp nước mưa ngoài sân, mẹ tôi — bà cụ Nguyễn Thị Lành, mái tóc đã bạc hoa râm — đang cặm cụi ngồi lựa từng bó rau muống xanh non, cẩn thận nhặt bỏ lá úa rồi buộc lại bằng cọng rơm vàng.

Nhìn dáng mẹ còng lưng bên rổ rau, tấm lưng gầy rung lên nhè nhẹ theo từng động tác tỉ mẩn, sống mũi tôi cay xè, nơi sâu kín nhất trong lồng ngực trào dâng cảm xúc xót xa khôn xiết.

Người mẹ hiền hậu ấy cả đời chỉ biết đến ruộng vườn, dãi nắng dầm mưa ngoài chợ huyện để đổi lấy bữa cơm đạm bạc cho con. Mẹ nào hay biết đứa con trai độc nhất đêm qua vừa bước qua cửa tử, dùng đôi tay trần nghiền nát âm mưu tà thuật kinh hoàng để giữ lại sự bình yên cho mảnh đất này.

Tôi bước nhẹ qua chiếc cổng rào tre, cất tiếng gọi nghẹn ngào:

"Mẹ ơi! Con về rồi nè mẹ!"

Bà cụ giật mình, cọng rau trên tay khẽ rơi xuống rổ. Mẹ ngước đôi mắt đã đục mờ vì sương gió nhìn về phía cổng, chiếc khăn rằn rơi xuống, mẹ run rẩy đứng bật dậy, bước những bước lập cập:

"Trời ơi... An! Thằng An con tôi về thiệt rồi!"

Tôi bước vội tới, ôm chầm lấy thân hình gầy guộc của mẹ vào lòng. Mùi mồ hôi vất vả, mùi khói bếp lá dừa và hơi ấm dịu dàng của mẹ xộc vào cánh mũi, làm tan biến mọi mỏi mệt tích tụ suốt bao tháng ngày rèn luyện gian khổ.

Bàn tay mẹ gầy gò nổi đầy gân xanh run rẩy vỗ nhẹ lên lưng tôi, rồi đưa lên vuốt ve đôi gò má phong trần. Đôi mắt mẹ rưng rưng những giọt lệ mừng vui:

"Con tôi... Sao đợt này nhìn đen đi, gầy hơn chút đỉnh nhưng cái tướng coi bộ rắn rỏi, cứng cáp dữ vậy con? Mấy tuần nay nghe đài báo biển động sóng to, mẹ ở nhà thắp nhang bàn thờ vái lạy ông bà tổ tiên ngày đêm phù hộ cho con đi công tác ngoài khơi được bình an vô sự..."

"Dạ con khỏe lắm mẹ ơi, sóng gió ngoài biển chẳng nhằm nhò gì với con đâu. Mẹ coi nè, con rắn chắc như cột nhà vậy đó!" Tôi cười rạng rỡ, gồng cánh tay săn chắc cho mẹ nắn thử.

Mẹ tôi quệt vội giọt nước mắt lăn trên khóe mi, kéo tay tôi vào nhà:

"Vào nhà uống miếng nước mưa cho mát ruột con! Sáng sớm nay thím Bảy vừa mang qua cho mẹ con cá lóc đồng bự tổ chảng, nặng gần ký rưỡi, mẹ giữ lại trong lu nước sau hè. Để mẹ đi nhóm bếp nướng trui cho con ăn liền!"

Mẹ tôi ra sau vườn ôm vào đống rơm vàng còn thơm nắng. Con cá lóc đồng tươi roi rói được xiên dọc sống lưng bằng thanh tre, cắm ngược đầu xuống đất rồi phủ kín rơm châm lửa. Ngọn lửa rơm bùng lên nghi ngút thơm lừng. Khi tro tàn lụi xuống, mẹ gạt lớp tro xám, cạo sạch lớp vảy cháy sém bên ngoài, để lộ những thớ thịt cá trắng ngần bốc khói ngào ngạt, ứa mỡ béo ngậy.

Bữa trưa dọn ra trên chiếc bàn tre con ngoài hiên: đĩa cá lóc đồng nướng trui vàng rộm; rổ rau đắng đất mọc hoang giòn rụm, đọt choại non tơ, lá cách; đĩa bánh tráng phơi sương; cùng chén nước mắm me dầm ớt hiểm cay xè đậm đà. Cạnh đó là tô canh chua bông súng đỏ nấu cá linh non rắc ngò om thơm ngát.

"Ăn đi con, cá lóc đồng cuốn rau đắng đất chấm mắm me là hết sẩy đó!" Mẹ gắp miếng thịt ngon nhất bỏ vào chén tôi, mắt chan chứa yêu thương.

Tôi cuốn miếng cá lóc nóng hổi cùng rau đắng đất vào bánh tráng, chấm ngập chén mắm me. Vị ngọt đậm của thịt cá nướng rơm quyện cùng vị đắng thanh của rau đắng đất, chua ngọt cay nồng của mắm me bùng nổ nơi đầu lưỡi. Đó là hương vị quê hương nuôi dưỡng dòng máu tôi từ thuở ấu thơ. Ăn bữa cơm mộc mạc bên mẹ hiền, tôi cảm nhận niềm hạnh phúc viên mãn mà không cảnh giới tu chân nào sánh được.'''

ACT3 = '''Một giờ ba mươi phút chiều.

Nắng trưa đổ dài trên những liếp vườn cây ăn trái quanh nhà. Gió sông Tiền thổi lồng lộng qua rặng dừa, xua tan cái oi ả nhiệt đới.

Sau khi ép mẹ nằm nghỉ trưa trên phản gỗ, tôi xắn quần quá gối, cởi trần để lộ thân hình vạm vỡ như đúc bằng đồng thau rồi bước ra vườn sau. Vườn mẹ rộng hai công đất trồng dừa xiêm, sầu riêng và liếp chanh. Mấy tháng mẹ đau yếu, cỏ dại mọc lúp xúp, rãnh mương phù sa bị bồi lắng tắc nghẽn.

Tôi cầm chiếc cuốc sắt cũ của cha để lại, bước xuống mé mương bắt đầu nạo vét bùn.

Từng nhát cuốc cắm sâu vào lòng đất sét phù sa đặc quánh. Với người tu luyện Thể Đạo Hoán Huyết Sơ kỳ, đây là một hình thức rèn luyện và giao hòa tuyệt mỹ. Tôi không vận Cương Khí cuồng bạo mà điều hòa hơi thở theo chu thiên tự nhiên. Mỗi nhát cuốc bổ xuống, cơ bắp co giãn nhịp nhàng, bàn chân trần bấm chặt vào bùn mát, truyền phản lực nhu hòa dọc ba mươi ba đốt sống tủy ngọc. Mồ hôi túa ra như tắm, kéo theo những tàn dư sát khí từ các trận huyết chiến ngoài biển sâu bài tiết ra ngoài, hòa tan vào lòng đất mẹ.

Đây là sự tĩnh lặng tột cùng của Thể Đạo phàm nhân. Nó không bắt nguồn từ mật thất bế quan xa hoa, mà từ sức lao động nguyên thủy khi hòa mình vào thiên nhiên, giúp Thuần Dương Cương Huyết được bồi đắp tính nhu hòa của đất phù sa.

Trong thức hải, Lục Diệp Thanh Liên khẽ lay động. Bạch Y Thần Nữ Lâm Tịch ngự trên đài sen, im lặng dõi theo tôi suốt hai giờ đồng hồ. Nàng khẽ truyền âm:

"Minh An... Thật kỳ diệu."

Tôi dừng tay, lấy khăn rằn lau mồ hôi trán, mỉm cười:

"Cô thấy kỳ diệu ở điểm nào, Lâm Tịch?"

Giọng nàng trầm tư:

"Ở thượng giới, tu sĩ luôn coi phàm nhân như cỏ rác, xem lao động cày cấy là thấp hèn. Họ bế quan trăm năm nhưng tâm hồn ngày càng lạnh lẽo, xa rời vạn vật, để rồi gục ngã trước tâm ma thiên kiếp. Nhưng anh thì khác. Vừa trải qua đại chiến dời non lấp bể, trở về bên mẹ già, anh lại thản nhiên cuốc đất dọn mương. Dòng máu trong người anh không kiêu ngạo, mà đang hút địa khí bình dị bồi đắp cốt tủy. Đây mới thực sự là Đạo... một đạo lộ vững vàng tựa bàn thạch."

"Thể Đạo rốt cuộc là công cụ để bảo vệ những điều bình dị này," tôi điềm tĩnh đáp. "Nếu tu luyện để thành kẻ vô cảm, quên đi cội nguồn và mẹ hiền, thì sức mạnh ấy có khác gì loài dã thú."

Lâm Tịch mỉm cười, mắt sáng lấp lánh: "Được đồng hành cùng anh là cơ duyên lớn nhất trong đời tu hành của tôi."

Sau khi nạo vét xong mương rãnh, tôi gánh nước phù sa tưới đẫm gốc sầu riêng đang hé nụ, rồi chẻ đống củi tràm khô xếp ngay ngắn dưới chái bếp. Mẹ thức dậy bước ra vườn, nhìn thành quả của con trai mà đôi mắt ánh lên niềm tự hào khôn xiết.'''

ACT4 = '''Tám giờ tối.

Đêm rằm tháng mười âm lịch, vầng trăng tròn vành vạnh như chiếc đĩa bạc khổng lồ nhô lên khỏi rặng dừa nước, tỏa ánh sáng vằng vặc xuống khắp xóm cù lao thanh bình.

Không gian tĩnh mịch, chỉ có tiếng gió đêm xào xạc luồn qua tàu lá dừa, tiếng cá quẫy đuôi dưới rạch và tiếng dế mèn rỉ rả. Dưới hiên nhà, đống trấu và lá dừa khô được mẹ tôi un từ chập tối đang âm ỉ tỏa ra những làn khói thơm dịu nhẹ để xua đuổi muỗi rừng.

Sau một ngày dài vui vầy bên con trai, mẹ tôi đã chìm vào giấc ngủ sâu thanh thản trên chiếc phản gỗ trong nhà.

Tôi nhẹ nhàng khép cánh cửa buồng, thắp ngọn đèn dầu hỏa nhỏ đặt lên chiếc bàn gỗ tràm cũ kỹ ngoài hiên — nơi thuở sinh thời, cha tôi vẫn thường ngồi uống trà ngắm trăng sau mỗi chuyến đi làm thợ rừng, thợ mộc trở về. Ngọn lửa vàng cam lung linh soi rõ từng đường vân gỗ mộc mạc đã nhẵn bóng theo năm tháng.

Tôi lấy chiếc bật lửa Zippo vỏ đồng của cha ra khỏi túi quần, đặt cạnh chiếc đèn dầu. Cạnh đó là chiếc xe đạp Thống Nhất khung sắt cũ kỹ màu xanh rêu cha để lại từ hơn hai mươi năm trước. Ban chiều, tôi đã dành nửa tiếng tra dầu mỡ vào từng mắt xích, siết lại ốc vít và lau sạch vết rỉ sét bám trên vành xe, khiến chiếc xe lại sẵn sàng bon bon trên đường làng.

Ngồi một mình giữa đêm trăng tĩnh lặng, trong lòng tôi dâng lên những hồi ức xa xăm về người cha trầm lặng, ít nói nhưng có đôi bàn tay tài hoa phi thường.

Thuở ấy, cha quanh năm bôn ba làm nghề thợ mộc, thợ rừng trên vùng đất đỏ cao nguyên Tây Nguyên, đặc biệt là vùng rừng già Buôn Đôn giáp ranh dãy Chư Yang Sin hùng vĩ. Cha từng cùng bác Sáu Kiên — người bạn kết nghĩa sinh tử mà sau này mở lò rèn ở Hóc Môn giúp tôi rèn thanh Hắc Thiết Đoản Côn — lặn lội qua biết bao cánh rừng đại ngàn để tìm kiếm những thân gỗ lim, gỗ gõ cổ thụ ngàn năm.

Bỗng nhiên, ánh mắt tôi hướng về góc tối dưới gầm phản gỗ trong nhà. Nơi đó có một chiếc rương gỗ lim cũ kỹ dài khoảng năm tấc, bốn góc bọc đai sắt đã hoen rỉ. Đó là chiếc rương đồ nghề duy nhất của cha được bác Sáu Kiên mang từ Buôn Đôn về trao lại cho mẹ con tôi sau ngày cha qua đời. Bao năm qua, mẹ tôi vẫn gìn giữ chiếc rương ấy như một kỷ vật thiêng liêng.

Tôi đứng dậy, cẩn thận nhấc chiếc rương gỗ lim nặng trịch đặt lên mặt bàn tràm. Cạy nhẹ then cài bằng đồng phủ lớp teng xanh cổ kính, nắp rương từ từ mở ra.

Bên trong rương là những dụng cụ mộc quen thuộc: vài chiếc đục mộc cán gỗ trau chuốt tỉ mỉ, chiếc bào tay bằng gỗ cẩm lai nhẵn bóng, cuộn dây thước đo bằng da bò thuộc thủ công và chiếc cưa tay mini thép gió. Mùi dầu tràm và mùi gỗ lim cổ thụ lập tức phảng phất thơm nồng.

Nhưng ở đáy rương, dưới lớp vải nhung màu đỏ sẫm đã mục nát, có một vật thể lạ được bọc kín bằng nhiều lớp da nai rừng sấy khô, buộc chặt bằng sợi dây gai rừng bện ba sợi vô cùng cẩn mật.

Tôi cẩn thận tháo từng nút thắt dây gai, gỡ lớp da nai dày cộp ra. Một vật thể bằng đá đen nhánh, dài chừng một gang tay, hình khối bát giác thon dài hiện ra dưới ánh đèn dầu le lói!

Kích thước chỉ bằng một bắp ngô nhỏ nhưng trọng lượng của nó phải hơn mười ký, nặng và chắc hơn bất kỳ loại đá bazan thông thường nào tôi từng kiểm định tại Viện Địa chất. Mặt ngoài đen bóng như huyền thạch, nhưng bên trong lại lấp lánh những đường vân thớ gỗ cổ xưa uốn lượn tựa như vòng đời sinh trưởng của một thân đại thụ ngàn năm tuổi đã bị hóa thạch hoàn toàn dưới áp suất địa tầng cực lớn.

Đó là một khối **Hóa Thạch Mộc Tâm Bazan** tuyệt mỹ!

Bên dưới khối mộc tâm là mảnh giấy da trắc địa lâm nghiệp đã ố vàng, mép giấy sờn rách, ghi chép những dòng chữ viết tay nắn nót bằng mực tàu của cha tôi vào mùa khô năm 1996:

*"Tháng Ba năm 1996 — Rừng sâu Buôn Đôn, chân núi Chư Yang Sin.*
*Đào được khúc Mộc Tâm này ở độ sâu mười hai mét dưới tầng đá bazan cổ cùng anh Sáu Kiên. Khúc gỗ hóa thạch phát ra tiếng ngân như sấm rền mỗi khi trời sắp đổ mưa giông lớn. Các già làng Ê Đê bảo đây là Lõi Cây Thần Sấm ngàn năm trấn giữ mạch đá ngầm của dãy núi Mẹ. Địa tầng nơi đây rung chuyển theo chu kỳ lạ lùng, âm thanh dưới lòng đất vọng lên như tiếng trống trận viễn cổ... Cất giữ lại làm kỷ niệm đời thợ rừng."*

Khoảnh khắc bàn tay tôi chạm vào khối Hóa Thạch Mộc Tâm Bazan, một sự cố chấn động bất ngờ xảy ra!

Từ sâu trong lõi khối đá đen nhánh, một luồng sóng xung chấn mang theo uy lực nặng trĩu tựa như tiếng sấm rền nghìn dặm bỗng phát ra tần số dao động cực kỳ trầm thấp. Tần số dao động ấy vừa vặn trùng khớp với nhịp tim và chu thiên vận hành của dòng **Thuần Dương Cương Huyết** trong cơ thể tôi!

Ba mươi ba đốt sống tủy ngọc sau lưng tôi đồng loạt phát sáng ấm áp, tự động sinh ra lực cộng hưởng mãnh liệt. Dòng cương huyết ánh kim trong kinh mạch tôi khẽ rung lên rộn rã, tựa như gặp lại người bạn cố tri thất lạc muôn trùng năm tháng. Đồng thời, từ chiếc ba lô nơi góc phòng, thanh Trấn Thủy Đoản Đao dù bọc kín vải dù cũng khẽ phát ra tiếng đao minh trong trẻo, hưởng ứng với tiếng sấm rền của khối mộc tâm!

Trong thức hải, Bạch Y Thần Nữ Lâm Tịch đột ngột xuất hiện trên đài sen Lục Diệp Thanh Liên. Khuôn mặt thanh tú tràn đầy vẻ kinh ngạc tột độ, đôi mắt dán chặt vào khối đá đen nhánh trên tay tôi qua thần niệm:

"Trời ơi... Minh An! Đây chính là **Mộc Hoàng Lôi Tâm Thạch** — hạch tâm linh mộc tích tụ lôi kiếp và địa khí ngàn năm của đại ngàn Trường Sơn!"

Thanh âm của Lâm Tịch run lên vì chấn động:

"Tôi từng nói với anh, mười hai cọc Thủy Môn ngoài biển lớn phương Nam chỉ là mạng lưới phong tỏa thủy đạo duyên hải. Để duy trì sự cân bằng của toàn bộ đại trận phong ấn non sông này, nơi thượng nguồn các con sông lớn, sâu trong lòng các rặng núi lửa bazan cổ của đại ngàn Tây Nguyên ắt phải có những trận nhãn Thổ - Mộc tương sinh để trấn áp lôi đình vực sâu! Tiếng trống trận ngầm dưới chân núi Chư Yang Sin mà cha anh nhắc tới ba mươi năm trước chính là dấu hiệu của một trận nhãn cổ xưa đang ngủ say! Mảnh đất non sông này dường như đã âm thầm an bài số mệnh từ đời trước, để hôm nay khối Mộc Tâm này rơi vào tay một phàm nhân tu luyện Thể Đạo như anh!"

Gió đêm sông Tiền thổi qua hiên nhà, làm ngọn lửa đèn dầu khẽ chao nghiêng.

Tôi nâng khối Hóa Thạch Mộc Tâm Bazan nặng trịch trên đôi bàn tay chai sạn của mình, lòng ngực cuộn trào cảm xúc thiêng liêng khó tả.

Từ người cha thợ mộc bôn ba nơi đại ngàn Buôn Đôn năm xưa, đến người mẹ hiền nhặt từng cọng rau muống nơi cù lao Chợ Gạo hôm nay, và hành trình Thể Đạo đầy gian truân mà tôi đang bước đi... Tất cả như hòa quyện vào làm một dòng chảy bất tận của số phận.

Bão ngầm phương Nam đã lắng xuống, nhưng tôi biết, một chân trời mới hùng vĩ và bí ẩn hơn đang vẫy gọi tôi hướng về phía đại ngàn đất đỏ Tây Nguyên cao ngút ngàn mây gió!'''

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
        active_characters=["char_minh_an", "char_lam_tich", "char_nguyen_thi_lanh"],
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
description: "Minh An bắt xe đò về thăm mẹ tại cù lao Chợ Gạo, Tiền Giang; thưởng thức cá lóc nướng trui rau đắng đất, lao động cuốc đất bồi vườn giao hòa Thể Đạo cùng đất mẹ; đêm trăng phát hiện khối Hóa Thạch Mộc Tâm Bazan Buôn Đôn trong chiếc rương cũ của người cha thợ mộc."
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
        "Minh An Về Cù Lao Chợ Gạo Thăm Mẹ, Thể Đạo Hòa Điền Viên & Manh Mối Mộc Hoàng Lôi Tâm Thạch Buôn Đôn",
        CHAPTER_NUM,
        1,
        f"{DATE}T12:00:00+07:00",
        CHAPTER_NUM,
        "loc_nha_me_cho_gao_tien_giang",
        json.dumps(["char_minh_an", "char_lam_tich", "char_nguyen_thi_lanh"]),
        "Minh An rời Sài Gòn trên chuyến xe đò sớm về thăm mẹ già Nguyễn Thị Lành tại cù lao Chợ Gạo, Tiền Giang. Hai mẹ con sum vầy bên bữa cơm cá lóc đồng nướng trui rơm, rau đắng đất mắm me. Buổi chiều, Minh An cuốc đất bồi vườn, chẻ củi tràm, gột rửa sát khí, đạt cảnh giới Thể Đạo giao hòa cùng đất mẹ phù sa khiến Lâm Tịch xúc động sâu sắc. Đêm trăng rằm, Minh An mở chiếc rương gỗ cũ của người cha thợ mộc Buôn Đôn, phát hiện khối Hóa Thạch Mộc Tâm Bazan (Mộc Hoàng Lôi Tâm Thạch) cùng ghi chép địa chấn Chư Yang Sin năm 1996, mở ra manh mối cho hành trình hướng về đại ngàn Tây Nguyên.",
        "Sum vầy tình mẫu tử; củng cố Thể Đạo Hoán Huyết sơ kỳ trong lao động phàm trần; phát hiện di vật Mộc Hoàng Lôi Tâm Thạch của người cha Tây Nguyên."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An về tận nhà lá cù lao Chợ Gạo Tiền Giang, ăn bữa cơm ấm áp bên mẹ già Nguyễn Thị Lành, cuốc đất tỉa vườn hoàn thành ước nguyện phàm nhân."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Thể Đạo Hoán Huyết sơ kỳ của Minh An đạt trạng thái cân bằng tuyệt mỹ nhờ lao động phàm trần, dòng Thuần Dương Cương Huyết giao hòa cùng đất mẹ phù sa."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-REL-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch xúc động chứng kiến đạo lý Thể Đạo phàm nhân gắn liền với tình mẫu tử và lao động chân chính, sự gắn kết tri kỷ với Minh An ngày càng sâu sắc."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Phát hiện khối Mộc Hoàng Lôi Tâm Thạch và ghi chép năm 1996 của người cha thợ mộc tại Buôn Đôn, mở ra manh mối mạng lưới phong ấn đại ngàn Tây Nguyên."
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
        inv_data["current_location"] = "Nhà Mẹ, Cù Lao Ven Sông Tiền, Huyện Chợ Gạo, Tỉnh Tiền Giang"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Thể Đạo Giao Hòa Phù Sa / Thuần Dương Cương Huyết Ôn Nhuận)"
        
        # Thêm Mộc Hoàng Lôi Tâm Thạch vào inventory
        special_items = inv_data.get("special_items", [])
        has_item = any(item.get("name") == "Mộc Hoàng Lôi Tâm Thạch" for item in special_items)
        if not has_item:
            special_items.append({
                "id": "item_moc_hoang_loi_tam_thach",
                "name": "Mộc Hoàng Lôi Tâm Thạch",
                "type": "Hóa Thạch Mộc Tâm Bazan Ngàn Năm",
                "origin": "Rừng già Buôn Đôn, Chân núi Chư Yang Sin (Di vật của cha Minh An năm 1996)",
                "properties": "Phát ra lôi âm trầm đục cộng hưởng cùng Thuần Dương Cương Huyết; mắt xích Thổ Mộc linh mạch Tây Nguyên"
            })
            inv_data["special_items"] = special_items

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

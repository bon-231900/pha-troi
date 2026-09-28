# -*- coding: utf-8 -*-
"""Draft Chapter 94 for Phá Trời Novel OS: Đáy Vạc Chư Yang Sin.
Prose length: ~3,800 words (standard: 3,200 - 4,500 words), zero meta-words, zero 'huyết mạch', severe grounding, geological realism, Tây Nguyên folklore, and Chư Yang Sin primeval forest depth.
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

CHAPTER_NUM = 94
CHAPTER_TITLE = "Đáy Vạc Chư Yang Sin"
DATE = "2026-11-03"
LOCATION = "Ống Dung Nham Số 3 & Đáy Vạc Núi Lửa Chư Yang Sin, Huyện Krông Bông, Tỉnh Đắk Lắk"

ACT1 = '''Lời truyền âm của Lâm Tịch vừa dứt, không gian giữa màn sương mù đặc quánh bỗng như đông cứng lại.

Tôi đứng lặng bên mép đá bazan nứt toác, các ngón tay siết chặt lấy bức ảnh đen trắng đã ố vàng theo năm tháng. Dưới ánh sáng vàng vọt hắt ra từ ngọn đèn bão dã chiến, gương mặt cha tôi ba mươi năm trước hiện lên rõ mồn một. Vẫn là nụ cười hiền hậu, vầng trán cao và đôi bàn tay gân guốc thô ráp từng bao năm cầm cưa, cầm bào nơi chái bếp nghèo ven sông Tiền.

Từ thuở ấu thơ cho đến ngày ông nhắm mắt xuôi tay trên chiếc giường tre ọp ẹp ở cù lao, cha chưa từng nhắc một lời về võ thuật, chưa từng khoe khoang nửa câu về những chuyến đi rừng rúng động đất trời. Ông chỉ dạy tôi cách dùng búa cho chuẩn, cách mài lưỡi đục cho bén, và cách đặt từng bước chân vững chãi như một sợi dây dọi cắm thẳng xuống đất mẹ phù sa.

Vậy mà đêm nay, giữa chốn rừng thiêng nước độc Chư Yang Sin, tôi lại tìm thấy chiếc cọc mốc địa chất khắc tên ông, cùng một đồ án triện cổ trùng khớp với thanh Trấn Thủy Đoản Đao gia bảo.

"Lâm Tịch..." Tôi khẽ cất lời trong thức hải, ngực áo phập phồng theo từng nhịp thở nặng nề: "Cô vừa bảo cha tôi không phải phàm nhân?"

Bạch Y Thần Nữ ngồi xếp bằng trên đài sen Lục Diệp Thanh Liên, tà áo lụa trắng buông lơi phủ kín những cánh sen ngọc thấu quang. Đôi mắt phượng của nàng nhìn vào bức ảnh cũ thông qua giác quan của tôi, ánh mắt lộ vẻ đăm chiêu sâu thẳm:

"Không phải người tu đạo tầm thường, mà là một bậc Thể Đạo đại tông sư ẩn mình giữa nhân gian. Nét chữ khắc trên cọc đá hoa cương kia không dùng búa tạ nện vào đục sắt, mà dùng ngón tay dẫn truyền cương khí ngưng tụ trên mũi thép tự chế mà vạch thành. Lực đạo thấu sâu ba phân, nét đá trơn nhẵn không hề vỡ vụn rìa ngoài. Chỉ có kẻ rèn tủy đến cảnh giới đại thành, biến da thịt thành đồng thau, mới có thể để lại dấu tích như vậy."

Nàng dừng lại một nhịp, giọng nói trầm xuống như tiếng đàn cổ vang vọng từ thung lũng xa xăm:

"Người đời thường nghĩ kẻ mạnh phải đứng trên đỉnh cao vạn trượng để muôn người bái vọng. Nhưng trên mảnh đất này, những người thực sự gánh vác non sông lại chọn cách vùi mình vào bùn đất, sống cuộc đời một người thợ mộc, một lão thợ rèn, âm thầm dùng máu thịt phàm nhân để neo giữ từng mạch đất phong ấn. Cha của anh đã dùng ba mươi năm bình yên còn lại của đời mình để chờ anh lớn khôn."

Già Y Dăm bên cạnh tôi khẽ thở dài, bàn tay đen bóng sờ lên chuỗi nanh heo rừng trên ngực:

"Lâm Tịch nói không sai đâu cậu trai. Năm chín sáu, lúc đoàn khảo sát gặp lũ quét cuốn sập cầu treo, một tảng đá hộc nặng cả tấn lăn từ sườn núi xuống chực đè nát chiếc xe chở máy móc. Chính mắt tao thấy cha mày bước tới, một vai ghìm chặt tảng đá, hai chân cắm sâu vào đất sét bazan nửa mét, cứu sống mười mấy mạng người. Đêm đó, cha mày chỉ bảo tao: 'Y Dăm, chuyện này sống để bụng chết mang theo. Tao chỉ là một thằng thợ mộc qua đường thôi.'"

Tôi cẩn thận gấp bức ảnh lại, nhét vào túi áo ngực ngay cạnh chiếc bật lửa Zippo vỏ đồng của cha. Hơi ấm của kim loại áp sát vào da thịt, truyền vào tim tôi một dòng nhiệt lượng vững chãi đến lạ lùng.

Tôi trải tấm bản đồ vẽ tay trên giấy can dầu ra mặt phẳng của cọc đá.

Tấm bản đồ đã ố vàng vì thời gian nhưng từng đường mực tàu đen nhánh vẫn sắc sảo vô cùng. Cha tôi đã dùng bút vẽ trắc địa khoanh tròn một đường nét đứt khúc, chú thích rõ ràng: *Đường hầm đứt gãy số 3 — Ống dẫn dung nham bazan cổ đại*. Tuyến đường này chạy ngầm xuyên qua lòng sườn núi phía nam, luồn lách qua các túi khí độc và đới đá sụt lở, dẫn thẳng vào tâm chấn miệng núi lửa Chư Yang Sin nằm ở độ cao một ngàn bốn trăm mét so với mực nước biển.

Gió núi rít qua khe nứt địa tầng vừa sạt lở, thổi tung những tàn tro lưu huỳnh bay lả tả.

Dưới lòng đất, những xung động hạ âm trầm đục lại dội lên từng đợt dồn dập. Tần số dao động 0.08 Hertz quét qua mặt đất khiến lớp sỏi vụn nhảy múa lách tách trên phiến đá.

"Không còn nhiều thời gian nữa," tôi nhìn già Y Dăm, ánh mắt kiên định: "Họng núi lửa đang giãn nở nhanh hơn dự kiến. Trước giờ Tý đêm nay, cháu phải đưa Mộc Tâm vào an vị tại đáy vạc."

"Đi!" Người thợ săn già không hề do dự, giắt chiếc xà-gạc vào thắt lưng da, tay cầm chắc chiếc gậy le: "Tao đã hứa với cha mày ba mươi năm trước, đêm nay dù có gãy xương tàn phế, già này cũng phải đưa mày tới cửa hang vạc lửa!"'''

ACT2 = '''Khe nứt địa tầng vừa mở ra sau trận sạt lở tựa như một vết chém khổng lồ ăn sâu vào sườn núi Chư Yang Sin.

Hai chúng tôi lách người qua vách đá hẹp, trượt xuống một triền dốc ngổn ngang đá dăm và rễ cây cháy xém. Càng đi xuống sâu, ánh sáng mờ ảo của bầu trời đêm cao nguyên hoàn toàn biến mất, nhường chỗ cho bóng tối đen đặc quánh như mực tàu. 

Tôi bật chiếc đèn pin dã chiến chuyên dụng gắn trên mũ bảo hộ. Luồng ánh sáng trắng cắt ngang màn sương mù lưu huỳnh, soi rọi một cảnh tượng địa chất kỳ vĩ đến ngạt thở.

Trước mắt chúng tôi là một đường hầm hình vòm khổng lồ, cao hơn bốn mét và rộng chừng sáu mét. Vách hầm không phải là đất đá vụn bở, mà được cấu tạo từ hàng ngàn cột đá bazan hình lăng trụ lục giác dựng đứng san sát nhau, đều tăm tắp tựa như tổ của một loài ong khổng lồ thời tiền sử. Đây chính là một ống dẫn dung nham hóa thạch — dấu tích của dòng nham thạch nóng chảy hàng ngàn độ từng cuồn cuộn chảy qua đây từ kỷ Đệ Tứ, trước khi lớp vỏ ngoài nguội lạnh và để lại một đường ống ngầm rỗng ruột xuyên thẳng vào tim ngọn núi.

Không khí bên trong đường hầm vô cùng ngột ngạt.

Càng tiến sâu theo độ dốc thoai thoải của ống dung nham, nhiệt độ môi trường càng tăng lên vùn vụt. Từ cái lạnh mười bốn độ C của sương đêm bên ngoài, nhiệt độ trong lòng hang đã vọt lên hơn bốn mươi lăm độ C. Hơi ẩm quánh lại, nồng nặc mùi khí sunfua dioxit và hydro sunfua cay xè xộc thẳng vào mũi.

Bên mép vách đá bazan lục giác, một dòng suối ngầm nhỏ đang sôi lục bục, phả ra những làn khói trắng xóa bốc mùi khoáng chất nồng nặc.

Dưới sự vận hành nhịp nhàng của dòng Thuần Dương Cương Huyết, ba mươi ba đốt sống tủy lưng của tôi ấm ran lên, tự động phóng thích ra một lớp Cương Khí mỏng như lụa bao bọc lấy phế nang và làn da. Khí độc và nhiệt lượng gay gắt khi chạm vào màng khí huyết của tôi lập tức bị tản mát ra ngoài, không thể xâm nhập vào lục phủ ngũ tạng.

Thế nhưng, già Y Dăm thì không thể chịu đựng được lâu như vậy.

Dù đã dùng một mảnh khăn thổ cẩm tẩm nước suối lạnh bịt kín mũi miệng, tiếng thở của người thợ săn già mỗi lúc một nặng nhọc, đứt quãng. Gương mặt khắc khổ của ông đỏ bừng lên vì nhiệt độ ngột ngạt, hai bên thái dương giật giật từng cơn, bước chân bắt đầu lảo đảo trên nền đá trơn trượt.

Đi được gần một cây số, đến một ngã ba nơi ống dung nham mở rộng thành một vòm hang lớn có nhiều đàn dơi cổ quạ bay loạn xạ, già Y Dăm bỗng ngã quỵ xuống một mỏm đá bazan, ho sặc sụa từng tràng dữ dội.

"Khụ... khụ... khụ..."

Một búng đờm đen sẫm lẫn bụi than lưu huỳnh bắn ra khỏi kẽ khăn.

Tôi vội vàng buông chiếc ba-lô xuống, bước tới đỡ lấy bả vai gầy guộc của ông lão. Bàn tay phải của tôi đặt nhẹ lên huyệt Phế Du sau lưng già Y Dăm, nhẹ nhàng truyền một luồng kình lực ấm áp vào kinh mạch, xoa dịu cơn co thắt dữ dội của lồng ngực.

"Già Dăm! Thở chậm lại, đừng hít sâu!" Tôi trầm giọng dặn dò.

Sau vài nhịp dẫn truyền kình lực, hơi thở của già Y Dăm dần dần ổn định trở lại. Ông ngẩng khuôn mặt nhợt nhạt đầm đìa mồ hôi lên nhìn tôi, đôi mắt già nua ánh lên vẻ bất lực xót xa:

"Cậu An... phổi của tao... phổi của tao bị thán khí thiêu đốt rồi. Năm chín sáu tao trẻ khỏe, theo cha mày tới được đây là phải dừng bước... Đằng trước là Vạc Lửa, nơi họng núi lửa thông thẳng xuống túi mắc-ma ngầm. Nhiệt độ ở đó đủ nung chảy cả chì... Người trần mắt thịt vào đó, chỉ ba bước chân là cháy rụi cuống họng mà chết ngạt."

Người thợ săn già run rẩy tháo chuỗi vòng cổ có chiếc nanh heo rừng khổng lồ ra, ấn mạnh vào lòng bàn tay tôi:

"Cầm lấy cái này... Chiếc nanh ở giữa năm xưa cha mày từng dùng tủy ngọc tôi luyện qua. Nó có thể giúp mày cảm ứng được vị trí của mạch đá an vị. Mày phải đi một mình thôi, cậu trai họ Nguyễn."

Tôi nhìn quanh vòm hang. Ở góc phía đông của hang dơi, một khe nứt tự nhiên ăn thông lên sườn núi phía trên đang hút một luồng gió mát lành từ bên ngoài vào, tạo thành một vùng đệm không khí tương đối trong lành và an toàn.

Tôi dìu già Y Dăm ngồi dựa lưng vào vách đá cạnh khe thông gió, lấy bình nước khoáng dã chiến và gói lương khô trong ba-lô ra đặt vào tay ông:

"Già ngồi yên ở đây tịnh dưỡng. Khe gió này rất an toàn, đàn dơi tụ tập ở đây chứng tỏ không khí không có độc tính chết người. Cháu để lại cho già chiếc đèn bão và hai cây pháo sáng cứu hộ. Sau khi an vị Mộc Tâm, cháu sẽ quay lại đón già ra ngoài."

Già Y Dăm nắm chặt bàn tay tôi, giọng nói khàn đặc run rẩy:

"Cẩn thận nghe con... Miệng vạc lửa Chư Yang Sin không dung thứ cho kẻ yếu đuối đâu."

Tôi gật đầu thật mạnh, siết chặt quai đeo ba-lô, siết lại dây buộc của thanh Trấn Thủy Đoản Đao và Hắc Thiết Đoản Côn. 

Rút khối Mộc Hoàng Lôi Tâm Thạch ra khỏi lớp da nai bọc ngoài, tôi ôm trọn khối gỗ hóa thạch đen nhánh vào trước lồng ngực. Sức nóng từ tảng đá và sức nóng từ ngọn lửa địa tầng hòa quyện vào nhau, thúc giục tôi cất những bước chân đơn độc tiến thẳng vào lòng chảo hỏa ngục.'''

ACT3 = '''Càng rời xa trạm nghỉ hang dơi, không gian xung quanh càng biến chuyển thành một lò nung khổng lồ.

Vách đá bazan lục giác hai bên đường hầm lúc này không còn màu đen xám thông thường, mà bị nhiệt độ cực cao nung đỏ ửng như những thanh sắt vừa rút ra khỏi bễ lò rèn. Không khí rít lên từng cơn ghê rợn qua các kẽ đá, mang theo luồng nhiệt lượng bỏng rát lên tới hơn sáu mươi độ C. 

Dưới chân tôi, mặt đất rung chuyển không ngừng. Những tiếng ùng oàng trầm đục từ đáy sâu dội lên nghe như tiếng gầm của một đàn quái thú bị giam cầm dưới chín tầng địa ngục.

Tôi cắn chặt quai hàm, vận chuyển Thuần Dương Cương Huyết đến mức tối đa. 

Từng giọt mồ hôi vừa túa ra trên trán tôi lập tức bốc hơi thành những làn khói trắng mỏng. Nhưng ba mươi ba đốt sống tủy lưng của tôi vẫn tỏa ra một luồng hàn quang thanh khiết, ngưng kết thành lớp phòng hộ vững chắc che chở cho trái tim và hệ thần kinh. Đôi chân trần bên trong đôi ủng cao su chịu nhiệt bám chắc lấy từng gờ đá, tiến bước vững chãi như một chiếc cọc sắt cắm xuống bùn lầy.

Vượt qua khúc quanh cuối cùng của ống dung nham số 3, tầm mắt tôi đột ngột mở rộng ra một không gian ngầm khổng lồ khiến tôi sững sờ chết lặng.

Đó là Đáy Vạc Chư Yang Sin.

Một lòng chảo núi lửa cổ đại hình elip nằm sâu hàng trăm mét dưới lòng đất, rộng lớn tựa như một sân vận động mái vòm thiên nhiên. Trên trần hang cao vút, hàng ngàn khối thạch nhũ bazan nhọn hoắt rủ xuống như những thanh gươm của tử thần.

Dưới đáy lòng chảo, một hồ khoáng chất ngầm đang sôi sùng sục. Nước hồ không phải màu xanh trong mà đỏ quạch như máu hòa lẫn với bùn khoáng kim loại nóng chảy, liên tục bốc lên những bong bóng khổng lồ to bằng chiếc nón lá rồi nổ tung thành những cột hơi nước áp lực cao rít lên chói tai.

Mặt đất của lòng chảo bị xé toạc thành hàng chục vết nứt chằng chịt, để lộ ra những mạch dung nham đỏ rực đang cuồn cuộn dâng trào từ tầng sâu của vỏ Trái Đất.

Ở chính giữa hồ khoáng chất sôi sùng sục ấy, sừng sững một gò đá bazan hình bát giác tự nhiên nhô cao khỏi mặt nước chừng ba mét. Trên đỉnh gò đá bát giác, một khe nứt thẳng đứng sâu hun hút có hình thù và kích thước trùng khớp hoàn hảo với khối Mộc Hoàng Lôi Tâm Thạch trên tay tôi!

"Trận nhãn Mộc Hạch!" Lâm Tịch cất tiếng, thanh âm mang theo sự cảnh báo tột độ: "Minh An, vòm đá đáy vạc đang sụt lún! Túi dung nham bên dưới đang bị lực từ trường cưỡng bức đẩy lên! Nếu trong vòng ba phút nữa không cắm Mộc Tâm vào trấn áp trận nhãn, toàn bộ đáy vạc sẽ nổ tung, hàng triệu khối nham thạch sẽ xé toạc sườn núi Krông Bông!"

*Răng... rắc... ầm!*

Đúng lúc đó, một đợt sóng vi địa chấn cực mạnh đánh thẳng vào lòng chảo.

Cây cầu đá bazan tự nhiên duy nhất nối từ mép cửa hang ra gò đá bát giác bỗng gãy đôi thành ba đoạn, đổ ụp xuống hồ nước khoáng sôi sùng sục, làm bắn lên những làn sóng nhiệt bỏng rát cao cả chục mét.

Khoảng cách từ mép hang ra đến gò đá bát giác lúc này là hơn mười lăm mét mặt nước sôi bỏng!

Người bình thường đối mặt với khoảng cách ấy, cùng sức nóng thiêu đốt da thịt, chắc chắn chỉ có con đường tuyệt vọng.

Nhưng tôi là Nguyễn Minh An. Một phàm nhân khổ tu Thể Đạo đã tôi luyện gân cốt qua hàng ngàn lần rách da nát thịt nơi sóng gió cù lao.

Tôi không hề do dự nửa giây.

Hai chân tôi lùi lại ba bước lấy đà, trọng tâm cơ thể hạ thấp xuống mức cực hạn. Dòng Thuần Dương Cương Huyết trong cơ thể tôi sôi trào dữ dội, ba mươi ba đốt sống tủy ngọc bừng sáng một dải ánh vàng rực rỡ xuyên qua lớp áo dã chiến sờn rách.

"Lên!"

Tôi gầm lên một tiếng trầm hùng, hai bàn chân đạp mạnh lên mỏm đá bờ vực.

Rầm!

Phiến đá bazan dày nửa mét dưới chân tôi nứt toác thành hàng trăm mảnh vụn trước phản lực kinh hoàng. Toàn bộ thân hình tôi bay vút lên không trung tựa như một mũi tên xé gió, lướt ngang qua hồ nước khoáng sôi sùng sục.

Hơi nóng hàng trăm độ táp thẳng vào mặt tôi, làm cháy xém những sợi tóc mai và làm rát bỏng làn da trần. Nhưng luồng Cương Khí Ly Thể phóng thích ra từ lỗ chân lông đã tạo thành một bức bình phong vô hình đẩy dạt luồng khí nóng sang hai bên.

Bịch!

Bàn chân tôi đáp chuẩn xác xuống gờ đá trơn trượt của gò bát giác. Lực quán tính khiến tôi trượt dài nửa bước, mũi ủng chỉ cách hồ nước sôi vài phân, nhưng cơ đùi và cơ hông của tôi lập tức siết chặt lại, ghìm cứng cơ thể đứng vững như bàn thạch.

Trước mắt tôi, khe nứt trận nhãn đang phát ra những tiếng rít the thé của địa lôi bị kìm nén.

Tôi nâng khối Mộc Hoàng Lôi Tâm Thạch nặng hơn mười ký lên bằng cả hai tay. Cơ bắp trên hai cánh tay cuộn lên như rễ cây cổ thụ, gân xanh nổi cộm chằng chịt.

Dưới sự kích thích của từ trường đáy vạc, những đường vân sấm sét màu hoàng kim trong khối lôi thạch bỗng bừng sáng chói lọi, cộng hưởng mãnh liệt với ba mươi ba đốt tủy ngọc sau lưng tôi.

"Trấn!"

Tôi dồn toàn bộ kình lực của Thuần Dương Cương Huyết sơ kỳ, cắm thẳng mũi nhọn của khối Mộc Hoàng Lôi Tâm Thạch vào khe nứt bazan trên đỉnh bệ đá!

Oành!

Một tiếng nổ chấn động tựa như thiên lôi giáng thế bùng nổ giữa lòng hang ngầm.

Một luồng lôi điện màu lục kim rực rỡ từ khối Mộc Tâm bắn vọt lên trần hang cao vút, rồi tựa như một mạng lưới rễ cây phát sáng khổng lồ lan tỏa khắp vách đá bazan của đáy vạc. 

Lôi đình đi tới đâu, mặt hồ nước khoáng sôi sục lập tức phẳng lặng tới đó. Những mạch dung nham đỏ rực đang trào dâng bỗng chốc ngưng tụ lại, nguội dần và chuyển sang màu tro xám an định. Đợt sóng hạ âm 0.08 Hertz bị triệt tiêu hoàn toàn, trả lại cho lòng đất mẹ Chư Yang Sin một sự tĩnh mịch bình hòa kỳ diệu.

Tôi buông tay khỏi khối đá, thở dốc từng cơn, lồng ngực phập phồng sau cú dồn lực sinh tử.

Khối Mộc Hoàng Lôi Tâm Thạch lúc này đã hòa làm một với gò đá bazan, tỏa ra làn ánh sáng xanh ngọc dịu dàng ấm áp, tựa như một trái tim vĩnh cửu đang đập nhịp nhàng cùng mạch sống của đại ngàn Tây Nguyên.

Nhưng đúng vào khoảnh khắc ánh chớp lôi điện lục kim vừa quét qua đáy hồ khoáng chất vừa nguội lạnh, một cảnh tượng rợn người bất thần đập vào mắt tôi.

Dưới lớp bùn khoáng bazan mỏng manh vừa lắng xuống đáy hồ cạn, cách chân gò đá bát giác chừng năm bước chân, một vòng tròn hợp kim cơ quan khổng lồ đường kính hơn mười mét lộ ra lấp lánh ánh kim loại màu xám lạnh.

Trên bề mặt của vòng tròn cơ quan ấy, không phải là những hoa văn cổ xưa của tiền nhân muôn năm trước.

Mà là những ký hiệu số tọa độ được dập bằng máy đột kim loại công nghiệp hiện đại, sắc nét và sáng bóng không hề có một vết rỉ sét, kèm theo một dòng mã số la-tinh khắc chìm mới toanh:

*PROJECT EARTH-SEAL // SECTOR 04 - CHU YANG SIN // ANCHOR CORE V.2026*'''

def run_pipeline():
    print(f"[*] Bắt đầu Pipeline tự động hóa xuất bản Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Độ dài thân bài: {word_count} từ (Yêu cầu: 3.200 - 4.500 từ).")
    if word_count < 3000:
        print(f"[-] Cảnh báo: Độ dài chương hơi ngắn ({word_count} từ). Cần mở rộng chi tiết văn học!")

    # 1. Kiểm tra từ cấm tuyệt đối (RULE-07 & RULE 3)
    meta_words = ["chương", "hồi", "quyển", "tác giả", "hệ thống", "bản thảo", "canon", "database", "plot", "foreshadowing"]
    for mw in meta_words:
        matches = re.findall(rf"\b{mw}\b", raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ meta '{mw}' trong thân bài!")
            return False
            
    if "huyết mạch" in raw_content.lower():
        print("[-] VI PHẠM RULE 3: Phát hiện từ cấm 'huyết mạch' trong thân bài!")
        return False
    print("[+] [2/6] Kiểm tra từ cấm tối cao: 0 meta-words, 0 'huyết mạch'.")

    # 2. Đo lường cảm xúc & nhịp độ
    emo_engine = EmotionDopamineEngine(DB_PATH)
    emo_res = emo_engine.analyze_text(CHAPTER_NUM, raw_content, arc_id="arc_02")
    print(f"[+] [3/6] Chỉ số Cảm xúc & Dopamine:")
    print(f"    - Pathos Score    : {emo_res['pathos_score']:.2f}")
    print(f"    - Dopamine Score  : {emo_res['dopamine_score']:.2f}")
    print(f"    - Grounding Score : {emo_res['grounding_score']:.2f}")

    # 2.5 Đảm bảo thực thể nhân vật hợp lệ trong DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        "char_gia_y_dam",
        "Già Y Dăm",
        "character",
        json.dumps(["Y Dăm", "Già Y Dăm"], ensure_ascii=False),
        "ALIVE",
        json.dumps({"role": "Thợ săn Ê Đê dẫn đường Vườn Quốc gia Chư Yang Sin", "age": 62}, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

    # 3. Tự phản biện bằng CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_gia_y_dam"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        for ci in critical_issues:
            print("   ->", ci)
        return False
    print(f"[+] [4/6] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 4. Xuất bản Markdown
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
description: "Minh An cùng già Y Dăm tiến sâu vào ống dung nham bazan số 3; già Y Dăm kiệt sức vì thán khí ở trạm dừng chân an toàn; Minh An một mình vượt qua lòng chảo địa nhiệt cực đoan của Đáy Vạc Chư Yang Sin; vận dụng Thuần Dương Cương Huyết nhảy vọt qua hồ khoáng sôi và cắm Mộc Hoàng Lôi Tâm Thạch an vị trận nhãn, dập tắt nguy cơ phun trào; phát hiện vòng tròn cơ quan kim loại mang ký hiệu công nghiệp hiện đại dưới đáy hồ cạn."
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
    print(f"[+] [6/6] Đã xuất tệp Word (.docx): {docx_file_path}")

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
        "Minh An An Vị Mộc Tâm Đáy Vạc Chư Yang Sin & Phát Hiện Vòng Tròn Cơ Quan Hiện Đại",
        CHAPTER_NUM,
        1,
        f"{DATE}T05:00:00+07:00",
        CHAPTER_NUM,
        "loc_day_vac_chu_yang_sin",
        json.dumps(["char_minh_an", "char_lam_tich", "char_gia_y_dam"]),
        "Minh An thấu hiểu sự hi sinh và cốt cách Thể Đạo của cha; cùng già Y Dăm thâm nhập ống dung nham số 3; bố trí già Y Dăm tịnh dưỡng tại Hang Dơi an toàn; một mình băng qua hỏa ngục Đáy Vạc Chư Yang Sin với nhiệt độ hơn 60 độ C; vận dụng Thuần Dương Cương Huyết nhảy vọt qua hồ khoáng sôi và cắm Mộc Hoàng Lôi Tâm Thạch an vị trận nhãn Mộc Hạch, dập tắt nguy cơ phun trào; phát hiện vòng tròn hợp kim hiện đại PROJECT EARTH-SEAL 2026 dưới đáy hồ khoáng cạn.",
        "An vị thành công Mộc Hoàng Lôi Tâm Thạch; giải tỏa nguy cơ đứt gãy núi lửa Chư Yang Sin; mở ra bí mật chấn động về vòng tròn cơ quan công nghệ hiện đại can thiệp vào phong ấn."
    ))

    # 6.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Minh An an vị thành công Mộc Hoàng Lôi Tâm Thạch vào trận nhãn Đáy Vạc Chư Yang Sin; phát hiện dấu vết cơ quan công nghiệp hiện đại tại lòng chảo núi lửa."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Thuần Dương Cương Huyết của Minh An chịu đựng thành công nhiệt lượng cực hạn của hồ khoáng magma; Thể Đạo phàm nhân bộc phát sức bật 15 mét qua miệng vạc sôi."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-003'
    """, (
        CHAPTER_NUM,
        "Bí mật vòng tròn hợp kim PROJECT EARTH-SEAL 2026 dưới đáy vạc Chư Yang Sin hé lộ sự can thiệp của khoa học công nghệ hiện đại vào lưới phong ấn địa cầu."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 7. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T05:30:00+07:00"
        inv_data["current_location"] = "Đáy Vạc Núi Lửa Cổ Đại Chư Yang Sin, Huyện Krông Bông, Tỉnh Đắk Lắk"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Kháng Ngự Địa Nhiệt Cực Hạn / Thể Phách Tôi Luyện Dung Nham)"

        # Cập nhật trạng thái của Mộc Hoàng Lôi Tâm Thạch: Đã an vị vào trận nhãn
        artifacts = inv_data.get("core_weapons_and_artifacts", [])
        for art in artifacts:
            if "Mộc Hoàng Lôi Tâm Thạch" in art.get("name", ""):
                art["location"] = "Đã an vị vào Trận Nhãn Bệ Bát Giác Bazan tại Đáy Vạc Chư Yang Sin"
                art["condition"] = "Đang kích hoạt hòa nhập vào mạch địa lôi non sông"

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

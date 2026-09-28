# -*- coding: utf-8 -*-
"""Draft Chapter 93 for Phá Trời Novel OS: Lôi Chấn Vực Thần Sấm.
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

CHAPTER_NUM = 93
CHAPTER_TITLE = "Lôi Chấn Vực Thần Sấm"
DATE = "2026-11-03"
LOCATION = "Vực Thần Sấm, Vùng Lõi Rừng Nguyên Sinh Chư Yang Sin, Huyện Krông Bông, Tỉnh Đắk Lắk"

ACT1 = '''Ngón tay tôi bấu chặt vào chuôi gỗ bọc đồng của thanh Trấn Thủy Đoản Đao, mũi chân ghìm sâu xuống khe nứt của tảng đá bazan phủ đầy rêu ướt.

Mảnh kính khoáng chịu lực của chiếc la bàn quân sự vỡ vụn cấn vào lớp da thuộc bọc cổ tay trái, nhói buốt. Nhưng cái đau thể xác ấy chẳng thấm vào đâu so với luồng áp bách đang tỏa ra từ chạc ba của cây chò chỉ ngàn năm tuổi sừng sững trong màn sương mù dày đặc.

Hai đốm sáng đỏ rực như than hồng không hề chớp. Đó không phải là ảo ảnh của lân tinh bốc lên từ thảm lá mục, mà là ánh nhìn của một dã thú săn mồi thượng thặng nơi chốn rừng thiêng nước độc.

"Đừng nhúc nhích, cậu trai..." Già Y Dăm rít khẽ qua kẽ răng, bàn tay gầy gò nổi đầy gân xanh siết chặt cán xà-gạc bằng gỗ trắc, hạ thấp người xuống sau một thân le rừng gãy gập. "Là Sơn Miêu Mắt Máu. Thứ thú dữ ăn sỏi đá, uống nước suối ngậm sắt của họng núi lửa Chư Yang Sin mà lớn lên."

Gió đêm từ đáy vực sâu bốc lên từng cơn ràn rạt, mang theo hơi ẩm ngai ngái của rêu phong, nồng nặc mùi lưu huỳnh và mùi tanh tưởi của thú ăn thịt. Dưới ánh sáng vàng yếu ớt hắt ra từ đốm than trên tẩu thuốc của người thợ săn già, hình thù của sinh vật trên cành cây dần dần hiện rõ.

Đó là một con hắc báo khổng lồ. 

Toàn thân nó dài hơn hai mét tính từ mũi đến gốc đuôi, lớp lông đen mượt như than đá kíp-lê nhưng dưới ánh nhìn sắc bén của tôi, từng sợi lông cứng như thép non bám đầy bụi quặng bazan màu nâu thẫm. Dọc theo sống lưng gồ ghề của con thú, một bờm lông dựng đứng đang rung rinh nhè nhẹ, thỉnh thoảng lại lóe lên những tia tĩnh điện li ti màu xanh tím lách tách. Khác với loài báo hoa mai thông thường ở miền duyên hải châu thổ, hộp sọ của con thú này bè rộng, khung xương vai gồ lên cuồn cuộn tựa như hai khối đá tảng ghép lại. Bốn bàn chân nó to bè như miệng bát ăn cơm, những chiếc móng vuốt màu hổ phách cắm phập vào vỏ cây chò chỉ dày nửa gang tay mà không gây ra lấy một tiếng động nhỏ.

Từ trong lồng ngực vạm vỡ của nó, một luồng âm ba trầm đục phát ra, rung bần bật với tần số cực thấp.

*Gừ... ừ... ừ...*

Âm thanh đó không giống tiếng gầm đe dọa thông thường của loài hổ báo săn mồi, mà như tiếng cọ xát của hai phiến đá mài ngập dưới đáy nước xiết. Tần số dao động ấy đánh thẳng vào màng nhĩ, len lỏi qua các thớ thịt, kích thích trực tiếp vào khối Mộc Hoàng Lôi Tâm Thạch đang buộc chặt sau lưng tôi.

Dưới lớp vải bố dày và da nai bọc ngoài, khối lôi thạch nặng hơn mười ký bỗng nóng ran lên. Những vân sấm sét màu hoàng kim trong lõi đá rung lên từng nhịp, hòa cùng nhịp đập của quả tim tôi.

Con hắc thú ngửi thấy mùi vị quen thuộc ấy.

Đôi mắt đỏ quạch của nó từ từ co rút đồng tử lại, hướng thẳng vào chiếc ba-lô dã chiến trên lưng tôi. Nó không phải đói ăn, mà là bị kích động bởi dòng địa lôi ngầm đang sôi sục dưới chân núi, cùng mùi hương của khúc gỗ hóa thạch đã phong kín ba mươi năm nay vừa trở lại cố thổ.

"Nó canh giữ miệng hang sụt dưới họng Thần Sấm," già Y Dăm thì thào, hơi thở phả ra làn khói trắng mỏng trong cái lạnh thấu xương của sương đêm: "Năm chín sáu, lúc cha mày bổ xà-băng xuống hốc đá nhấc khúc Mộc Tâm lên, con thú này còn là một con mèo rừng lông xám lấm lem, bị sét đánh xém nửa bên tai nằm thoi thóp trong kẹt đá. Cha mày không nỡ giết, còn lấy rượu thuốc xoa bóp rồi vứt cho nó nửa tảng thịt nai khô. Không ngờ ba chục năm sau, nó đã ăn gió nuốt sét mà lớn thành quái thú chốn rừng thẳm."

"Nó nhận ra hơi thở của khúc đá," tôi đáp khẽ, hai chân hơi chùng xuống, cơ bắp toàn thân thả lỏng theo yếu chỉ của Thể Đạo.

Dưới làn da đồng hun, ba mươi ba đốt sống tủy ngọc của tôi khẽ phát ra hơi ấm dịu dàng. Dòng Thuần Dương Cương Huyết sơ kỳ bắt đầu luân chuyển với tốc độ gấp ba lần bình thường, đẩy lùi toàn bộ cảm giác lạnh buốt của sương rừng và sự tê dại do từ trường hạ âm gây ra.

Trong thức hải, Lâm Tịch lặng lẽ đứng trên đài sen Lục Diệp Thanh Liên. Tà áo trắng của nàng lay động giữa màn sương lam hư ảo. Giọng truyền âm của nàng vang lên trong đầu tôi, mang theo sự sắc lạnh và cẩn trọng vốn có:

"Minh An, con thú này đã hấp thu địa từ bazan qua hàng chục năm, cốt cách của nó cứng chắc chẳng khác nào thép rèn nguội. Nhưng trong gân cốt nó chứa đầy khí độc lưu huỳnh tích tụ từ miệng núi lửa đang nứt toác. Đừng dùng lưỡi bén chém vỡ nội tạng nó, khí độc phát tán sẽ làm nhiễm bẩn đới thực bì cổ thụ xung quanh, dẫn dắt lôi hỏa bùng phát sớm hơn."

"Tôi hiểu."

Vừa dứt câu đáp trong ý nghĩ, chạc ba cây chò chỉ bỗng rung chuyển dữ dội.

Con hắc thú co chân lấy đà. Lớp vỏ cây cổ thụ nứt toác thành những mảnh vụn bay tung tóe giữa màn sương. Một bóng đen khổng lồ tựa như tảng thiên thạch xé toạc màn đêm lao thẳng xuống đầu tôi, mang theo một luồng gió rít lạnh buốt thấu xương.'''

ACT2 = '''Cú vồ từ độ cao hơn hai mươi mét tạo ra một áp lực không khí nặng nề tựa như một bức tường đá đổ ụp xuống.

Nếu là một người bình thường hoặc một thợ săn thiếu kinh nghiệm, phản xạ tự nhiên sẽ là lăn sang hai bên để né tránh. Nhưng ở bờ vực đá trơn trượt ngổn ngang rêu mục này, chỉ cần bước hụt nửa bước là sẽ rơi thẳng xuống dòng suối ngầm cuồn cuộn đá ngầm bên dưới.

Tôi không lùi.

Chân trái tôi bước trượt về phía trước nửa bước, đế ủng cao su non cắm chặt vào kẽ đá bazan, hai đầu gối chùng xuống khóa chặt hạ bàn. Bàn tay phải tôi rút thanh Trấn Thủy Đoản Đao ra khỏi bao da bên hông. 

Lưỡi đao bằng đồng cổ rạn nứt những đường chỉ vàng sẫm màu vung lên một góc bốn mươi lăm độ, không dùng mũi nhọn đâm thẳng mà dùng sống đao dày dặn đón đỡ cú vồ ngàn cân.

Keng!

Một tiếng kim loại va đập chói tai vang lên giữa rừng già.

Móng vuốt trước của con hắc thú quẹt ngang qua sống đao đồng thau, làm bắn ra một chùm tia lửa vàng rực sáng lòa giữa màn đêm ẩm ướt. Sức nặng hơn hai trăm ký cộng với gia tốc rơi tự do dồn ép thẳng xuống hai cánh tay tôi. Cổ tay tôi rung lên bần bật, nhưng ba mươi ba đốt sống lưng lập tức liên kết thành một trục thẳng tắp, truyền toàn bộ lực va đập khủng khiếp ấy xuống hai bàn chân rồi ghim thẳng vào lòng khối đá bazan kiên cố.

Phiến đá dưới chân tôi nứt toác ra một đường dài ba tấc, nhưng thân hình tôi vẫn vững như bàn thạch.

Con thú săn mồi trượt vuột qua đầu tôi, đáp xuống mỏm đá phía sau với một cú xoay người cực kỳ uyển chuyển. Chiếc đuôi dài như roi sắt quất mạnh vào một bụi le rừng, làm gãy gục hàng chục thân cây to bằng bắp tay người lớn kêu rôm rốp.

Đôi mắt đỏ như máu của nó lóe lên sự kinh ngạc tột độ. Nó không ngờ một sinh linh hai chân nhỏ bé lại có thể dùng sức mạnh thuần túy của thân xác để đón đỡ trọn vẹn cú vồ sở trường của nó.

"Hây!" 

Già Y Dăm từ bên sườn đá hét lớn một tiếng, cánh tay gân guốc ném phắt chiếc tẩu thuốc đang đỏ rực than hồng thẳng vào mắt trái của con thú. Đồng thời, lưỡi xà-gạc bằng thép rèn thủ công trên tay già quét ngang một đường sắc lẹm, chém đứt đám dây leo chằng chịt quấn quanh chân sau của nó để cản đường rút lui.

Đốm than hồng nổ lách tách trước mắt khiến con hắc thú lùi lại nửa nhịp, nhe hàm răng nanh trắng ởn dài bằng ngón tay trỏ gầm lên một tiếng giận dữ.

Tận dụng khoảnh khắc ngưng trệ của đối phương, tôi buông tay trái ra sau lưng, rút thanh Hắc Thiết Đoản Côn ra khỏi đai đeo.

Thanh thép nhíp xe Zil nặng hơn ba ký bát giác nằm gọn trong lòng bàn tay tôi. Lớp da bò quấn chuôi đã thấm đẫm mồ hôi ấm áp. Những rãnh khía chu sa đỏ thẫm trên thân côn như bừng tỉnh dưới sự kích thích của dòng Thuần Dương Cương Huyết đang cuộn trào trong kinh mạch.

Con thú gầm lên một tiếng xé lòng, hai chân sau đạp mạnh lên vách đá phóng tới. Lần này, nó há to chiếc mồm đỏ lòm tanh tưởi, nhắm thẳng vào cuống họng tôi cắn xuống, hai chiếc móng trước xòe rộng như hai chiếc bồ cào thép chực xé toạc lồng ngực đối thủ.

Tôi không hề hoảng loạn. 

Trong trạng thái tĩnh lặng của Thể Đạo Hoán Huyết, từng chuyển động của con thú dường như chậm lại nửa nhịp trong tầm mắt tôi. Tôi nhìn thấy rõ từng thớ cơ bắp cuồn cuộn dưới lớp lông đen bóng, nhìn thấy làn hơi lưu huỳnh nóng rực bốc ra từ khóe miệng nó, và cả những tia tĩnh điện li ti đang chạy dọc theo móng vuốt.

Tôi hít một hơi không khí ẩm ướt của rừng già, cơ hoành siết chặt lại.

Nội kình từ đan điền bốc lên, chạy dọc theo tủy sống, ba mươi ba đốt tủy ngọc thấu quang phát ra luồng nhiệt lượng ấm áp. Dòng Cương Huyết mang theo sắc vàng ánh kim róc rách chảy qua các nhánh mạch máu lớn nhỏ, truyền thẳng vào hai cánh tay.

Thay vì né tránh, tôi bước chéo một bước hình chữ Đinh, nghiêng người né qua đường cắn chết người của con thú trong đường tơ kẽ tóc. 

Bàn tay phải cầm Hắc Thiết Đoản Côn xoay tròn nửa vòng, mượn chính quán tính lao tới của đối phương, tôi dồn toàn bộ kình lực của cơ ngực, eo và vai vào một đòn vung ngang chuẩn xác.

Cương Khí Ly Thể!

Kình lực vô hình phóng ra khỏi đầu thanh đoản côn chừng ba đốt ngón tay, tạo nên một tiếng rít xé gió tựa như tiếng búa tạ xé rách không gian.

Bốp!

Đầu côn bọc chu sa giáng thẳng vào khớp xương bả vai dày cộm của con hắc thú.

Một tiếng rạn nứt trầm đục vang lên bên dưới lớp da dầy. Kình lực Thuần Dương cương mãnh xuyên thấu qua lớp mỡ và cơ bắp, đánh tan toàn bộ lớp tĩnh điện màu xanh tím đang bao bọc quanh cơ thể con thú, đồng thời chấn động thẳng vào kinh lạc điều khiển chi trước của nó.

Con hắc thú nặng hai trăm ký bị cú đánh tống bổng sang ngang, đập mạnh vào vách đá bazan dựng đứng rồi trượt dài xuống nền đất ẩm ướt.

Nó lồm cồm bò dậy, chân trước bên phải hơi run rẩy, không thể đặt hoàn toàn trọng lượng xuống đất. Nó nhìn tôi bằng đôi mắt tràn ngập vẻ kiêng dè và sợ hãi, hàm răng nhe ra thở phì phò những làn khói xám nồng mùi khoáng vật nung nóng.

Tôi thu côn về ngang ngực, không hề thừa thế xông lên dồn nó vào chỗ chết.

Tôi hạ thấp trọng tâm, đưa bàn tay trái trần trụi chạm nhẹ vào lớp vải bọc của khối Mộc Hoàng Lôi Tâm Thạch sau lưng, rồi ấn thẳng lòng bàn tay xuống mặt phiến đá bazan ẩm ướt dưới chân.

Thuần Dương Cương Huyết trong cơ thể tôi bắt đầu dao động cùng tần số với khối đá cổ đại. 

Một luồng xung lực êm dịu, ấm áp mang theo hơi thở của đất mẹ bazan và lôi đình đã được thuần hóa từ từ lan tỏa qua lòng bàn tay tôi, truyền vào lòng phiến đá, tạo thành những gợn sóng từ trường bình hòa quét qua khoảng đất trống giữa tôi và con thú.

Mùi khét lẹt của tĩnh điện trong không khí dần dần tan biến.

Con hắc thú khịt khịt mũi. Khi cảm nhận được làn sóng từ trường ấm áp quen thuộc ấy — thứ năng lượng từng cứu mạng nó trong kẹt đá ba mươi năm trước khi nó còn là một con thú non côi cút — ánh mắt đỏ ngầu man dại của nó dần dần dịu lại, chuyển sang màu vàng sẫm thuần khiết của loài báo hoang.

Nó cúi thấp đầu, áp sát mũi xuống mặt đất hít hà hơi ấm lan tỏa từ bàn tay tôi, rồi khẽ phát ra một tiếng gầm gừ êm ái như tiếng mèo rừng sưởi nắng.

Con thú quay đầu nhìn già Y Dăm, rồi lại nhìn tôi một lần cuối, trước khi tập tễnh phóng mình vào bụi rậm le rừng rậm rạp, biến mất tăm vào bóng đêm thăm thẳm của sườn núi phía tây.'''

ACT3 = '''Tiếng xào xạc của lá le khô xa dần rồi hoàn toàn chìm vào màn đêm tịch mịch.

Tôi từ từ đứng thẳng người dậy, thở ra một hơi dài màu sương trắng. Cánh tay phải vẫn còn hơi tê rần vì lực phản chấn của cú va chạm ban nãy, nhưng dòng Cương Huyết tuần hoàn êm dịu đã nhanh chóng làm tan đi sự mỏi mệt trong các khớp xương.

"Mày... mày đánh gãy được kình lực của Lôi Thú mà không cần một giọt máu chảy..." Già Y Dăm bước tới, đôi mắt mở to nhìn tôi trân trối, ngực phập phồng sau cơn nghẹt thở: "Thần Đất trên đỉnh Chư Yang Sin chứng giám, tao đi rừng hơn bốn mươi năm nay, chưa từng thấy người Kinh nào có gân cốt và sức mạnh tay không ghê gớm đến bực này. Cậu An, mày thực sự là cốt cách của dòng giống người mở cõi!"

"Cháu chỉ mượn thế đánh lui nó thôi già," tôi vừa nói vừa cài lại thanh Hắc Thiết Đoản Côn vào đai ba-lô: "Con thú đó có linh tính, nó chỉ phát điên vì áp suất lòng đất trào lên. Giết nó đi thì mạch rừng này sẽ mất đi một kẻ giữ cửa."

Lời tôi vừa dứt, một tiếng rền rĩ quái dị bỗng nhiên dội lên từ sâu thẳm dưới lòng đất đá bazan.

*Ù... ù... ùng...*

Lần này, không phải là rung chấn nhẹ thông thường. 

Mặt đất dưới chân chúng tôi rung lắc dữ dội theo chiều thẳng đứng tựa như có một chiếc đe khổng lồ vừa nện sầm xuống tầng đá móng cách mặt đất ba cây số. Những tảng đá hộc to bằng gian nhà nằm chênh vênh bên sườn đèo bắt đầu lăn ầm ầm xuống vực sâu, kéo theo hàng ngàn khối đất đá và cây cối đổ gãy rào rào.

Một đợt sóng hạ âm với biên độ cực mạnh quét qua, khiến không khí quanh chúng tôi rít lên ken két.

"Cẩn thận sạt lở!" Già Y Dăm hét lên, kéo tôi nép sát vào một hàm ếch đá hoa cương nhô ra bên vách núi.

Trước mắt chúng tôi, toàn bộ sườn đồi phủ đầy cây dương xỉ cổ thụ của vách đá phía đông Vực Thần Sấm bỗng nứt toác ra một vệt dài hơn ba mươi mét. Từng mảng đá bazan phong hóa hàng triệu năm trượt thẳng xuống lòng suối cạn, bốc lên những đám bụi đất đỏ mù mịt hòa lẫn với hơi nước sương mù tạo thành một màn sương đặc quánh như cháo.

Khi bụi đá dần lắng xuống sau cơn địa chấn kinh hoàng, một cảnh tượng kỳ dị mở ra ngay trước mắt chúng tôi.

Vết sạt lở đã xé toạc lớp đất mặt và rễ cây cổ thụ, để lộ ra một khe nứt địa tầng sâu hun hút đâm chéo vào lòng núi Chư Yang Sin. Từ trong khe nứt ấy, những luồng khí nóng hầm hập mang theo mùi lưu huỳnh và hơi nước bốc lên nghi ngút, tạo thành những cột khói trắng mờ ảo cuộn tròn trong đêm lạnh.

Trên các ngọn cây dương xỉ và cành le gãy gục quanh miệng vực, những quầng sáng lân tinh màu xanh lam nhạt lập tức bùng cháy le lói — hiện tượng lửa thánh Elmo sinh ra khi từ trường tĩnh điện trong không khí đạt tới ngưỡng bão hòa cực hạn.

Nhưng điều khiến tim tôi thắt lại không phải là khe nứt địa chất đang bốc khói.

Ở ngay mép đá bazan bị xé toạc, cách chỗ chúng tôi đứng chừng bảy bước chân, một khối đá hoa cương màu xám trắng nhân tạo lộ ra giữa tầng tầng lớp lớp đá núi lửa màu nâu đen.

Đó là một chiếc cọc mốc địa chất bằng đá granite được đẽo gọt vuông vức, bốn góc cạnh đã mòn vẹt vì rêu phong và thời gian. Chiếc cọc đá cắm sâu vào lòng khe nứt, quanh thân cọc được gia cố bằng những sợi dây cáp đồng thau to bằng ngón tay cái bện chặt, néo chặt vào các mấu neo thép chôn sâu trong đá gốc.

Tôi bước lại gần, quỳ một gối xuống lớp đá vụn nóng rẫy, dùng mu bàn tay gạt đi lớp rêu phong bám dày trên bề mặt cọc đá hoa cương.

Dưới lớp rêu mục màu tro, những ký tự khắc chìm bằng đục sắt hiện ra rõ mồn một dưới ánh đèn bão:

*ĐOÀN KHẢO SÁT ĐỊA TẦNG TÂY NGUYÊN — 11/1996*
*MỐC ĐỊA CHẤN TẦNG SÂU SỐ 04 — CAO ĐỘ 1.420M*
*NGUYỄN VĂN HÙNG — TRỊNH HOÀI NAM*

Phía dưới dòng chữ hành chính kỹ thuật ấy, người khắc dường như đã lén dùng một mũi khoan hợp kim tự chế để khắc thêm một đồ án bí mật: một biểu tượng hình đóa sen ba cánh lồng trong một vòng tròn bát giác — hoa văn giống hệt với chiếc triện cổ khắc trên chuôi thanh Trấn Thủy Đoản Đao của tôi!

Và bên dưới hoa văn triện cổ là một dòng chữ viết tắt nguệch ngoạc:

*"Mộc Hạch trấn trụ, địa lôi tiềm tàng. Ba mươi năm sau nứt họng, chờ con trai về an vị."*

Ngón tay tôi run lên nhè nhẹ khi chạm vào từng nét đục thô ráp của cha mình. Ký ức tuổi thơ nghèo khó nơi chái bếp cù lao sông Tiền, hình ảnh người cha với đôi bàn tay chai sạn vì đục đẽo gỗ đá bỗng chốc ùa về, sống động và chân thực đến nhói lòng. Cha tôi ba mươi năm trước không chỉ đơn thuần là một thợ mộc hay thợ trắc địa theo đoàn khảo sát, mà ông đã cùng Viện trưởng Nam tính toán chuẩn xác chu kỳ hoạt động ngầm của miệng núi lửa Chư Yang Sin đến từng mốc thời gian!

"Trời đất ơi..." Già Y Dăm run rẩy quỳ xuống bên cạnh tôi, đôi bàn tay đen bóng sờ lên chiếc cọc đá hoa cương: "Đúng là cọc mốc của anh Hùng năm ấy rồi! Năm chín sáu, chính tay tao vác cái cọc đá nặng bảy chục ký này từ chân dốc lên đây cho cha mày đóng neo. Cha mày bảo đây là cái đinh giữ vía cho mạch núi, không có nó thì trận nứt đất năm đó đã xé toang cả thung lũng Krông Bông..."

Ánh mắt tôi bỗng chú ý đến một khe hở nhỏ phía sau bệ móng của cọc đá.

Nằm sâu trong hốc đá bazan được chèn chặt bằng một lớp nhựa đường chống thấm, một ống kim loại hình trụ bằng hợp kim nhôm dã chiến dài khoảng hai gang tay đang nằm im lìm. Nắp ống được hàn kín bằng một lớp thiếc dày, bên ngoài dán một dải băng keo vải màu xanh quân đội đã ngả sang màu vàng ố.

Tôi rút con dao găm nhỏ bên hông, cẩn thận nạy lớp thiếc niêm phong quanh nắp ống nhôm.

Chiếc nắp bật mở với một tiếng xì nhẹ của không khí bị nén kín suốt ba thập kỷ. 

Bên trong ống nhôm là một cuốn sổ tay trắc địa bọc bìa da màu nâu đã sờn rách các góc, cùng một tấm bản đồ vẽ tay trên giấy can dầu chống ẩm. Từng đường nét mực tàu đen nhánh thể hiện chi tiết sơ đồ đứt gãy địa tầng của vùng lõi Chư Yang Sin, dẫn thẳng từ mép vực Thần Sấm này vào tận họng núi lửa cổ đại ẩn sâu dưới đỉnh núi cao nhất.

Kẹp giữa trang đầu của cuốn sổ tay là một bức ảnh đen trắng nhỏ chụp ba người đàn ông: Viện trưởng Trịnh Hoài Nam thời trẻ mặc áo lính, già Y Dăm ngực trần đóng khố cầm xà-gạc, và cha tôi — người đàn ông có nụ cười hiền hậu, vầng trán rộng và ánh mắt kiên định, trên tay đang ôm khúc Mộc Hoàng Lôi Tâm Thạch vừa khai quật.

Phía sau bức ảnh, nét chữ bút chì thân thương của cha tôi viết vội:

*"Nếu con cầm được cuốn sổ này, nghĩa là con đã vượt qua được thử thách của Vực Thần Sấm và dòng máu trong người con đã thức tỉnh. Hãy mang Mộc Tâm đi theo đường hầm đứt gãy số 3 trên bản đồ, cắm thẳng vào khe đá bazan dưới đáy miệng núi lửa trước giờ Tý. Trận nhãn này không chỉ cứu lấy đại ngàn Tây Nguyên, mà còn là mắt xích đầu tiên bảo vệ linh mạch toàn cõi non sông."*

Trong thức hải bao la, Bạch Y Thần Nữ Lâm Tịch ngự trên đài sen Lục Diệp Thanh Liên bỗng mở bừng đôi mắt trong veo. 

Làn sương lam quanh người nàng khẽ xao động một nhịp chưa từng có, thanh âm truyền âm của nàng vang lên bên tai tôi, trầm lắng và chấn động:

"Minh An... Cha của anh không phải là một phàm nhân bình thường."'''

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
description: "Minh An đối mặt Hắc Báo Lôi Thú nơi Vực Thần Sấm, vận dụng Thể Đạo Hoán Huyết và Cương Khí Ly Thể ghìm chặt thú dữ mà không sát sinh; đợt sụt lún địa tầng xé toạc sườn đèo lộ ra chiếc cọc mốc địa chất hoa cương 1996 của người cha cùng ống nhôm chứa bản đồ bí mật đứt gãy dẫn vào miệng núi lửa Chư Yang Sin."
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
        "Minh An Thu Phục Lôi Thú Vực Thần Sấm & Khám Phá Cọc Mốc Bí Mật 1996",
        CHAPTER_NUM,
        1,
        f"{DATE}T03:30:00+07:00",
        CHAPTER_NUM,
        "loc_vuc_than_sam_chu_yang_sin",
        json.dumps(["char_minh_an", "char_lam_tich", "char_gia_y_dam"]),
        "Minh An giáp mặt Hắc Báo Lôi Thú tại Vực Thần Sấm; vận dụng Hoán Huyết Sơ kỳ, Hắc Thiết Đoản Côn và Cương Khí Ly Thể đỡ đòn, dùng từ trường êm dịu của Mộc Hoàng Lôi Tâm Thạch cảm hóa thú dữ. Đợt sụt lún địa tầng tiếp theo xé toạc vách đá lộ ra cọc mốc hoa cương năm 1996 do người cha và Viện trưởng Nam cắm neo cùng ống nhôm chứa bản đồ đứt gãy dẫn vào miệng núi lửa Chư Yang Sin. Lâm Tịch thốt lên nghi vấn về thân thế người cha.",
        "Thu phục Lôi Thú mở đường vào vùng lõi; giải mã cọc mốc địa chất 1996; sở hữu bản đồ bí mật đứt gãy số 3 tiến vào họng núi lửa Chư Yang Sin."
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
        "Minh An tìm thấy cọc mốc địa tầng 1996 của cha và bản đồ hầm đứt gãy số 3 dẫn vào miệng núi lửa Chư Yang Sin."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Hoán Huyết Sơ kỳ và Cương Khí Ly Thể thực chiến hiệu quả trước lôi thú; vận dụng thuần thục từ trường địa chấn hòa hợp với Mộc Hoàng Lôi Tâm Thạch."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 7. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T04:15:00+07:00"
        inv_data["current_location"] = "Vực Thần Sấm & Vách Đá Sạt Lở Vùng Lõi Chư Yang Sin, Huyện Krông Bông, Tỉnh Đắk Lắk"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Khí Ly Thể Thuần Thục / Hòa Hợp Mộc Hoàng Lôi Thạch)"

        # Thêm item mới vào inventory nếu chưa có
        has_notebook = any("Sổ Tay Trắc Địa" in item.get("name", "") for item in inv_data.get("core_weapons_and_artifacts", []))
        if not has_notebook:
            inv_data.setdefault("core_weapons_and_artifacts", []).append({
                "name": "Sổ Tay Trắc Địa & Bản Đồ Đứt Gãy 1996",
                "type": "Di vật của cha / Bản đồ khảo sát địa tầng",
                "location": "Túi trong ba-lô dã chiến",
                "condition": "Nguyên vẹn trong ống nhôm dã chiến, giấy can dầu mực tàu",
                "durability": "95/100",
                "function": "Dẫn đường qua hầm đứt gãy số 3 thâm nhập miệng núi lửa Chư Yang Sin; ghi chép chu kỳ địa chấn 30 năm"
            })

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

# -*- coding: utf-8 -*-
"""Draft Chapter 95 for Phá Trời Novel OS: Mã Khóa 2026.
Prose length: ~3,800 words (standard: 3,200 - 4,500 words), zero meta-words, zero 'huyết mạch',
severe grounding, geological realism, Tây Nguyên folklore, and Chư Yang Sin primeval forest depth.
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

CHAPTER_NUM = 95
CHAPTER_TITLE = "Mã Khóa 2026"
DATE = "2026-11-03"
LOCATION = "Đáy Vạc Núi Lửa Chư Yang Sin & Hang Dơi Ống Dung Nham Số 3, Huyện Krông Bông, Tỉnh Đắk Lắk"

ACT1 = '''Hơi nóng lưu huỳnh từng cuộn bốc lên nghi ngút ban nãy bỗng chốc loãng dần theo làn gió ngầm hút ngược lên trần hang. 

Tôi đứng chôn chân trên đỉnh gò bát giác, hai bàn tay thô ráp vẫn còn vương những vụn đá lấp lánh của khối Mộc Hoàng Lôi Tâm Thạch. Toàn thân tôi ướt đẫm mồ hôi, lớp áo bảo hộ lao động dính chặt vào lồng ngực đang phập phồng sau cú dồn lực sinh tử. Dưới chân tôi, khối lôi thạch vừa được cắm ngập vào khe nứt bazan tỏa ra từng gợn sóng lục kim ấm áp, tựa như một trái tim khổng lồ đang đập những nhịp khoan thai, xoa dịu cơn co giật địa tầng của lòng núi lửa Chư Yang Sin.

Thế nhưng, đôi mắt tôi không tài nào rời khỏi khoảng đáy hồ khoáng vừa rút cạn nước.

Cách chân gò đá bát giác chừng năm bước chân, lớp bùn khoáng xám tro trôi tuột theo những rãnh thoát ngầm, phơi bày một vòng tròn hợp kim khổng lồ có đường kính ngót nghét mười mét. 

Đó là một khối cơ quan cơ khí tráng lệ và lạnh lẽo đến sững sờ. 

Nó nằm ôm trọn lấy phần chân đế của gò đá bazan, phẳng lì như một vành đai bánh răng công nghiệp được đúc bằng hợp kim titan-niken chống ăn mòn cực hạn. Dưới ánh sáng lục kim dịu dàng từ khối lôi thạch rọi xuống, bề mặt kim loại không hề có một vảy rỉ sét nào, chỉ ánh lên sắc xám bạc lỳ lợm của loại thép chịu nhiệt chuyên dùng trong kỹ thuật khoan thăm dò đáy biển sâu. 

Xung quanh vành đai cơ quan ấy là ba mươi sáu bu-lông lục giác cỡ lớn, mỗi chiếc to bằng bắp tay người lớn, cắm sâu vào vỉa đá móng bằng phương pháp nêm nở thủy lực. 

Và ngay trên tấm biển tên bằng thép không gỉ dày hai phân gắn chặt vào thân vòng tròn, từng nét chữ dập nổi bằng máy đột công nghiệp hiện đại hiện lên rõ mồn một, sắc cạnh và sạch sẽ đến mức đối nghịch hoàn toàn với khung cảnh hoang sơ ngàn năm của lòng chảo núi lửa:

*PROJECT EARTH-SEAL // SECTOR 04 - CHU YANG SIN // ANCHOR CORE V.2026*

Dự án Earth-Seal. Phân khu số 4 — Chư Yang Sin. Cụm neo hạch tâm phiên bản 2026.

Làn không khí ẩm lạnh thốc vào khoang mũi buốt rát, lồng ngực tôi thắt lại. 

Năm 2026 chính là năm nay! 

Giữa một vùng rừng nguyên sinh rậm rạp bậc nhất Tây Nguyên, nơi ngay cả những thợ săn thiện nghệ người Ê Đê như già Y Dăm cũng chỉ dám lần theo dấu vết thú rừng ven sườn ngoài, làm sao có thể tồn tại một công trình cơ khí ngầm quy mô khủng khiếp đến thế này? Ai đã vận chuyển hàng chục tấn hợp kim chịu nhiệt cùng dàn máy ép thủy lực vào sâu dưới lòng ống dung nham số 3 mà không để lại bất kỳ dấu vết nào trên mặt đất?

Tôi thận trọng bước từng bước chậm rãi từ đỉnh gò đá xuống đáy lòng chảo. Đôi ủng cao su dẫm lên lớp bùn khoáng bazan phát ra những tiếng lép bép ẩm ướt. Nhiệt độ của lớp đá dưới chân đã hạ từ sáu mươi độ xuống chỉ còn âm ấm như mặt đường nhựa sau cơn mưa rào, không còn nguy cơ làm nổ tung đế giày bảo hộ.

Tôi quỳ một chân xuống mặt bùn, đưa bàn tay trần chạm vào bề mặt vòng tròn hợp kim.'''

ACT2 = '''Lớp thép mát lạnh truyền qua da thịt, mang lại một cảm giác chân thực đến gai người. 

Tôi miết đầu ngón tay dọc theo đường rãnh tiện ren của chiếc bu-lông lục giác gần nhất. Đầu ngón tay tôi bỗng khựng lại.

Là một người lớn lên bên cạnh xưởng mộc của cha ở cù lao Tiền Giang, từng nhiều năm theo cha cưa từng thớ gỗ mù u, mài từng lưỡi đục thép nhíp xe Zil, tôi quá đỗi quen thuộc với cảm giác của những đường gia công cơ khí chính xác. Trên bề mặt của chiếc bu-lông hợp kim siêu cứng này, mép vát cạnh không phải là đường cắt vát hoàn toàn trơn tuột của máy tiện CNC hiện đại điều khiển bằng máy tính. 

Ở phần chân ren ăn sâu vào đá bazan, có một góc lượn vát nghiêng ba mươi độ được sửa lại bằng tay. Nét giũa mịn như lụa, tì đè với một lực đạo đều đặn đến mức hoàn mỹ, chỉ để lại những đường vân xước tế vi hình bán nguyệt — kiểu vát ren thoát phoi thủ công đặc trưng mà ngày xưa cha tôi vẫn hay làm mỗi khi chế tạo các chốt mộng thép gia cố cho thuyền gỗ vượt sóng lớn.

Tôi run rẩy đưa ngón tay chạm vào một ký hiệu nhỏ xíu được đóng chìm bằng đục thép ở góc dưới tấm biển tên.

Một chữ "H" hoa lồng trong một hình tròn nhỏ, bên cạnh là một hình triện vuông tí hon bằng hạt đậu xanh.

Đó là dấu triện của cha tôi — Nguyễn Văn Hùng!

"Cha..." 

Cổ họng tôi khô khốc, một tiếng gọi nghẹn ngào bật ra giữa không gian tĩnh lặng của đáy vạc.

Bức ảnh chụp đoàn khảo sát ba mươi năm trước mà tôi cất trong túi áo ngực bỗng nóng bừng lên. Ba mươi năm trước, năm 1996, cha tôi đã cùng các nhà khoa học của Viện Khảo sát Địa chất đặt chân đến cánh rừng này. Họ đã khảo sát vết đứt gãy, đã đo đạc những chấn động sâu trong lòng đất. Nhưng công trình này lại mang số hiệu phiên bản 2026! 

Điều đó có nghĩa là gì? Bản thiết kế và những linh kiện cốt lõi này đã được cha tôi cùng các bậc tiền bối chế tác, rồi sau đó được các thế hệ kỹ sư thực địa tiếp nối, hoàn thiện và bí mật lắp đặt vào trận nhãn này theo chu kỳ địa chấn được dự báo chính xác cho năm nay?

Trong thức hải của tôi, tà áo lụa trắng của Lâm Tịch khẽ lay động trên đài sen Lục Diệp Thanh Liên. Đôi mắt phượng của nàng nhìn xuyên qua tâm thức tôi, chăm chú quan sát vòng tròn hợp kim khổng lồ dưới chân:

— Thật phi thường...

Thanh âm truyền âm của nàng trầm lắng, chứa đựng một sự kinh ngạc chưa từng có:

— Ta từng nghĩ phàm nhân thời nay chỉ biết dựa dẫm vào máy móc thô kệch bên ngoài mà quên mất đạo lý hòa hợp với trời đất. Nhưng kẻ tạo ra vòng tròn kim loại này đã dùng tri thức thạch học và cơ khí trần gian để mô phỏng lại đúng thế trận 'Cửu Cung Khóa Địa' của viễn cổ. Ba mươi sáu chiếc chốt thép kia cắm đúng vào ba mươi sáu huyệt đạo lưu chuyển địa khí của lòng vạc. Chúng không hề phá hủy long mạch, mà dùng chính trọng lực và sức căng của hợp kim để neo giữ lớp vỏ đá nứt nẻ, ngăn không cho dung nham trào dâng. 

Nàng khẽ thở dài một tiếng, ánh mắt nhìn tôi tràn đầy vẻ dịu dàng thấu hiểu:

— Cha của anh và những người đồng hành của ông ấy không chỉ là những người thợ. Họ là những người gác cổng thầm lặng của trần gian. Họ biết rõ sức mạnh của đá cổ có giới hạn, nên đã dùng chính bàn tay và trí tuệ phàm nhân để dựng nên một bộ khung thép, chờ đợi ngày anh mang khối Mộc Tâm này đến khép kín mắt trận.'''

ACT3 = '''Lời nói của Lâm Tịch như một dòng nước mát rót thẳng vào tâm can, làm tan biến mọi nỗi hoang mang trong lòng tôi.

Tôi đứng thẳng dậy, soi đèn pin bão dọc theo thân vành đai hợp kim. 

Tại góc hướng chính bắc của vòng tròn — đối diện thẳng với vách đá dựng đứng của ống dẫn dung nham số 3 — tôi phát hiện một chiếc hộp cơ khí hình trụ tròn bằng kim loại dày cộp, kích thước cỡ bằng chiếc cặp lồng cơm dã chiến. Chiếc hộp được gắn chặt vào khung thân bằng bốn chốt khóa bật cơ học, bên ngoài bọc một lớp gioăng cao su chịu nhiệt màu cam đã ngả màu vì khói lưu huỳnh.

Tôi ngồi xổm xuống, gạt bốn chốt khóa. 

*Tách! Tách! Tách! Tách!*

Những tiếng bật tanh tách khô khốc vang lên giòn giã giữa lòng hang. Nắp hộp kim loại bật mở, một làn khí ni-tơ bảo quản xì nhẹ ra ngoài mang theo mùi dầu máy công nghiệp quen thuộc.

Bên trong khoang chứa chống sốc lót đệm cao su xốp, không có vàng bạc hay bảo vật thần bí. 

Chỉ có hai vật dụng bình dị được đặt ngay ngắn: một thiết bị ghi chép địa chấn cơ học dạng trống quay dùng dây cót cơ khí bằng thạch anh, và một cuốn sổ nhật ký thực địa bọc bìa vải dầu màu xanh ô-liu đã cũ mòn bốn góc.

Bàn tay tôi run run nhấc cuốn sổ bìa vải dầu lên. Trên trang bìa cứng, dòng chữ viết tay bằng mực dạ dầu màu đen vẫn còn đậm nét:

*NHẬT KÝ THEO DÕI ĐỊA CHẤN ĐỚI ĐỨT GÃY SỐ 4 — CHƯ YANG SIN*
*Đội Khảo sát Địa chất Chuyên đề Sâu // Trạm Quan trắc Cơ động*

Tôi cẩn thận lật từng trang giấy can dày cộp chống ẩm.

Trang đầu tiên ghi lại những thông số trắc địa từ tháng Mười năm 1996, với nét chữ chân phương, phóng khoáng của cố Viện trưởng Trần Minh Nam và chữ ký xác nhận của thợ kỹ thuật chính: *Nguyễn Văn Hùng*. Họ đã ghi chép chi tiết về cấu trúc ống dung nham bazan, về các túi khí thán khí nguy hiểm và dự báo về một chu kỳ bộc phát địa nhiệt kéo dài đúng ba mươi năm.

Nhưng khi tôi lật đến những trang cuối cùng, ngày tháng ghi trên góc trang giấy khiến tim tôi đập thình thịch:

*Ngày 18 tháng 8 năm 2026.*

Đó là những dòng ghi chép mới toanh, chỉ cách thời điểm hiện tại chưa đầy ba tháng!

Nét chữ lần này thanh mảnh hơn, viết bằng bút bi xanh của một kỹ sư trẻ thuộc thế hệ chúng tôi. Nhật ký ghi nhận đội công tác đã hoàn tất việc hiệu chỉnh ba mươi sáu cụm neo thủy lực Anchor Core V.2026 tại đáy vạc Chư Yang Sin theo đúng đồ án lưu trữ năm 1996 của cha tôi. Cấu trúc vành đai hợp kim chịu lực ổn định ở mức nhiệt độ 280 độ C.

Tuy nhiên, phần cảnh báo bên dưới lại được gạch chân hai lần mực đỏ:

Tần số dao động hạ âm 0.08 Hertz dưới lòng ống dẫn dung nham đang có dấu hiệu khuếch đại theo cấp số nhân. Vòng tròn cơ học chỉ có thể neo giữ cấu trúc đá mẹ trong giới hạn chịu tải tối đa chín mươi ngày. Nếu sau tiết Sương Giáng mà dao động không giảm, áp lực magma sẽ bẻ gãy toàn bộ bu-lông neo, gây phun trào dây chuyền dọc theo mạng lưới đứt gãy Nam Trung Bộ.

Phía dưới cùng là dòng ghi chú đặc biệt bằng nét chì của Viện trưởng:

Mọi thông số khoa học đã đạt tới hạn của kỹ thuật cơ khí phàm trần. Chiếc khóa này đã sẵn sàng. Phần còn lại... chỉ còn biết trông cậy vào người giữ thanh Trấn Thủy Đoản Đao và khối Mộc Tâm từ phương Nam trở về...'''

ACT4 = '''Đọc đến dòng chữ cuối cùng, sống mũi tôi cay xè, những ngón tay siết chặt lấy mép cuốn sổ bọc vải dầu.

Hóa ra là như vậy.

Không hề có một sự tình cờ nào trong hành trình gian nan này. Những người thầy, những người cha, những thế hệ kỹ sư địa chất đi trước đã dùng cả cuộc đời và trí tuệ của họ để âm thầm chống đỡ cho sự bình yên của non sông này. Họ đo đạc từng milimét dịch chuyển của lòng đất, họ dùng mồ hôi và sắt thép để chế tạo nên chiếc cùm khóa cơ học này, kiên nhẫn chờ đợi hạt giống mà họ gieo xuống ba mươi năm trước nảy mầm.

Tôi nâng thanh Trấn Thủy Đoản Đao đeo bên hông lên. Lớp vỏ bao bằng đồng thau nứt rạn ánh chỉ vàng áp sát vào lòng bàn tay tôi ấm áp.

Dưới đáy hộp kim loại, cạnh vị trí đặt cuốn sổ, có một rãnh tra then cơ học hình chữ nhật dài đúng một gang tay, được khoét sâu vào trục van thủy lực trung tâm của vòng tròn hợp kim. Kích thước và đồ án triện cổ trên miệng rãnh tra then ấy trùng khớp tuyệt đối với lưỡi thanh đoản đao gia bảo của cha tôi.

"Đến lúc rồi." Tôi lẩm bẩm một mình, ánh mắt kiên định nhìn vào trục van trung tâm.

Tôi bước tới trước rãnh tra then, nắm chặt chuôi Trấn Thủy Đoản Đao, chậm rãi tra lưỡi dao đồng vào khe cơ khí.

*Cạch!*

Một tiếng khớp then kim loại vang lên giòn tan, chuẩn xác đến từng phần mười milimét. 

Tôi nín thở điều hòa nhịp tim đang đập dồn dập trong lồng ngực, thúc giục Thuần Dương Cương Huyết vừa thức tỉnh trong cơ thể. Ba mươi ba đốt sống tủy ngọc sau lưng tôi nóng bừng lên, một dòng nhiệt lượng thuần dương ấm áp từ đan điền cuộn trào qua các kinh mạch cánh tay, rót thẳng vào chuôi dao.

"Mở mạch khóa địa!"

Tôi gầm nhẹ một tiếng, hai cánh tay gồng cứng như sắt nguội, xoay mạnh chuôi Trấn Thủy Đoản Đao theo chiều kim đồng hồ một góc chín mươi độ!

Rắc... rắc... keng!

Tiếng bánh răng hợp kim chuyển động trầm đục vang lên từ sâu dưới đáy lòng chảo. Ba mươi sáu chiếc bu-lông nêm nở thủy lực xung quanh vòng tròn đồng loạt siết chặt lại, kéo căng toàn bộ mạng lưới cáp thép chịu lực ngầm dưới lòng đất. 

Cùng lúc đó, khối Mộc Hoàng Lôi Tâm Thạch trên đỉnh gò bát giác bỗng phóng thích ra một làn sương mù màu xanh ngọc bích, tràn xuống bao phủ lấy toàn bộ vòng tròn kim loại. Năng lượng địa lôi cổ xưa và cơ cấu kỹ thuật hiện đại của con người chạm vào nhau, không hề bài xích mà hòa quyện làm một. Từng đường rãnh ren, từng con ốc vít của cỗ máy phàm trần được dòng lôi điện màu lục kim tôi luyện, ánh lên một lớp màng bảo hộ trong suốt như thủy tinh.

Một tiếng thở phào nhẹ nhõm như thể cả quả núi khổng lồ vừa trút bỏ được gánh nặng ngàn năm lan tỏa khắp không gian. 

Mặt đất dưới chân tôi hoàn toàn phẳng lặng. Tiếng rít the thé của địa lôi tắt ngấm. Mùi khét lẹt biến mất, chỉ còn lại làn gió núi mát rượi từ các khe thông gió tự nhiên thổi lùa qua vòm đá, mang theo hương thơm ngai ngái của rêu rừng và hoa dại đầu nguồn.'''

ACT5 = '''Tôi cẩn thận cất cuốn sổ nhật ký thực địa vào sâu trong ngăn chống nước của ba lô, rút thanh Trấn Thủy Đoản Đao tra lại vào bao rồi cúi đầu vái tạ khối Mộc Tâm và gò đá bát giác một lạy.

Nhiệm vụ tại Đáy Vạc Chư Yang Sin đã hoàn thành trọn vẹn. 

Tôi xoay người, bám vào những gờ đá bazan nguội lạnh men theo lối mòn trèo ngược trở lên cửa vòm ống dung nham số 3. Quãng đường rút lui nhẹ nhàng hơn lúc tiến vào rất nhiều; khí độc đã tan bớt, nhiệt độ trong đường hầm hạ xuống mức mát mẻ dễ chịu.

Nửa tiếng sau, ánh sáng vàng ấm áp của ngọn đèn bão dã chiến hiện ra nơi khúc quanh của Hang Dơi.

Già Y Dăm đang ngồi tựa lưng vào vách đá, tay nắm chặt cây nỏ săn bóng loáng, đầu gật gù trong cơn mệt mỏi. Nghe thấy tiếng bước chân ủng cao su dẫm trên đá dăm lạo xạo, ông già giật thót người choàng tỉnh, mũi tên nỏ lập tức giương lên trong bóng tối. Nhưng khi nhận ra bóng dáng quen thuộc của tôi bước ra từ cửa hầm, đôi mắt đục mờ của người thợ săn già bỗng chốc ứa nước mắt.

— Ơi An... Mày... mày còn sống về được rồi!

Già buông cây nỏ, lập cập bước tới nắm chặt lấy hai bả vai tôi, bàn tay đen nhẻm run rẩy sờ khắp ngực áo để kiểm tra thương tích:

— Tao ở ngoài này nghe tiếng sấm nổ đùng đùng trong ruột núi, tưởng đâu vạc lửa vỡ tung rồi chứ! Mà sao tự nhiên... gió trên trần hang nó thổi mát rượi thế này? Tiếng con cọp gầm dưới đất cũng nín bặt rồi?

Tôi mỉm cười, đưa tay đỡ lấy già Y Dăm ngồi xuống tảng đá phẳng:

— Dạ, yên ổn hết rồi già. Mạch lửa dưới vạc đã nguội, đá Chư Yang Sin ngủ yên rồi, buôn làng mình từ nay không sợ động đất nứt nhà nữa đâu.

Già Y Dăm ngửa mặt lên vòm hang đá, chắp hai tay trước ngực lẩm bẩm những lời tạ ơn thần rừng Yang hùng vĩ bằng tiếng Ê Đê. Đoạn, già với lấy ống nứa đựng nước ngô rang treo bên hông, mở nắp đưa cho tôi:

— Uống miếng nước cho lại sức đi con. Uống đi, nước ngô già rang từ rẫy nhà tao đó, ngọt lắm.

Tôi đón lấy ống nứa, uống một ngụm lớn. Vị ngọt thanh của ngô nương hòa cùng mùi khói củi lan tỏa nơi đầu lưỡi, xua tan đi tất cả những mệt mỏi rã rời sau một đêm sinh tử dưới lòng đất. 

Hai bác cháu thu dọn đồ đạc, dập tắt ngọn đèn bão rồi lần theo lối cửa hang dơi bước ra ngoài sườn núi.

Khi chúng tôi bước qua khỏi vòm cây rậm rạp che kín miệng hang, một luồng ánh sáng ban mai tinh khôi ùa tới, rọi thẳng vào gương mặt phong trần của tôi.

Mặt trời đã bắt đầu nhô lên khỏi rặng núi phía đông. Những tia nắng vàng như rót mật xuyên qua biển mây bồng bềnh phủ trắng các thung lũng Krông Bông, dát một lớp viền vàng rực rỡ lên những tán cây pơ-mu cổ thụ ngàn năm tuổi. Đại ngàn Chư Yang Sin thức giấc trong tiếng chim hót véo von và tiếng suối reo róc rách xa xa.

Tôi đứng trên mỏm đá cao nhìn ngắm non sông gấm vóc trải dài dưới chân, trong lòng dâng lên một niềm thanh thản vô bờ.

Đột nhiên, từ chiếc máy bộ đàm trắc địa tầm xa đeo bên hông ba lô của tôi, một chuỗi âm thanh rè rè vang lên, phá tan sự tĩnh lặng của buổi sớm mai.

*Tít... tít... rẹt...*

Một tín hiệu xung mã Morse địa chấn vang lên đứt quãng, kèm theo một giọng nói quen thuộc của kỹ sư trực trạm viễn thám vang lên qua làn sóng ngắn:

— *Trạm kiểm định gọi tổ khảo sát Chư Yang Sin... Minh An có nghe rõ không? Vừa ghi nhận dao động tại Sector 04 đã về mức 0 tuyệt đối... Nhưng đới đứt gãy ven biển Sector 05 — khu vực rạn nứt đá bazan đảo Hòn Yến vừa phát tín hiệu cộng hưởng khẩn cấp... Nhắc lại, Sector 05 đang chờ lệnh tiếp cận...*

Tôi nhìn già Y Dăm, rồi nhìn về phía dải mây hồng rực rỡ nơi chân trời đông nam.

Hành trình của một người thợ phàm nhân đi vá lại vết nứt non sông vẫn chưa dừng lại ở cánh rừng già này.'''

raw_content = f"""{ACT1}

{ACT2}

{ACT3}

{ACT4}

{ACT5}"""

def run_pipeline():
    print(f"=== KHỞI CHẠY PIPELINE SÁNG TÁC & KIỂM DUYỆT CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    
    # 1. Kiểm tra dung lượng từ
    word_count = len(raw_content.split())
    print(f"[+] [1/6] Độ dài văn xuôi: {word_count} từ (Chuẩn mực: 3.200 - 4.500 từ).")
    if word_count < 3200 or word_count > 4500:
        print(f"[CẢNH BÁO] Độ dài nằm ngoài khoảng chuẩn mực: {word_count} từ!")
    
    # 2. Kiểm tra từ cấm và quy tắc RULE-07
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

    # 3. Đo lường cảm xúc & nhịp độ
    emo_engine = EmotionDopamineEngine(DB_PATH)
    emo_res = emo_engine.analyze_text(CHAPTER_NUM, raw_content, arc_id="arc_02")
    print(f"[+] [3/6] Chỉ số Cảm xúc & Dopamine:")
    print(f"    - Pathos Score    : {emo_res['pathos_score']:.2f}")
    print(f"    - Dopamine Score  : {emo_res['dopamine_score']:.2f}")
    print(f"    - Grounding Score : {emo_res['grounding_score']:.2f}")

    # 4. Tự phản biện bằng CritiqueEngine
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

    # 5. Xuất bản Markdown
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
description: "Minh An khám phá vòng tròn hợp kim khổng lồ PROJECT EARTH-SEAL 2026 dưới đáy vạc Chư Yang Sin; phát hiện dấu triện và nét gia công cơ khí tài hoa của người cha Nguyễn Văn Hùng; mở hộp bảo mật đọc nhật ký thực địa ba mươi năm của các thế hệ kỹ sư địa chất; vận dụng Trấn Thủy Đoản Đao và Thuần Dương Cương Huyết khóa chốt thủy lực, khép lại nguy cơ thảm họa núi lửa; cùng già Y Dăm đón bình minh đại ngàn trước khi nhận tín hiệu điều hướng về Sector 05 duyên hải."
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

    # 6. Xuất Word (.docx)
    word_arc_dir = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02")
    os.makedirs(word_arc_dir, exist_ok=True)
    docx_file_path = os.path.join(word_arc_dir, f"ch_{CHAPTER_NUM:03d}.docx")
    
    dp = DocxPipeline()
    dp.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=full_markdown,
        output_docx_path=docx_file_path
    )
    print(f"[+] [6/6] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 7. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Mã Khóa Cơ Quan 2026 Đáy Vạc Chư Yang Sin & Bước Tiếp Theo Hướng Duyên Hải",
        CHAPTER_NUM,
        1,
        f"{DATE}T06:30:00+07:00",
        CHAPTER_NUM,
        "loc_day_vac_chu_yang_sin",
        json.dumps(["char_minh_an", "char_lam_tich", "char_gia_y_dam"]),
        "Minh An khám phá vòng tròn hợp kim khổng lồ PROJECT EARTH-SEAL 2026 dưới đáy vạc Chư Yang Sin; phát hiện dấu triện và kỹ thuật vát ren thủ công của cha Nguyễn Văn Hùng; mở hộp kim loại đọc nhật ký trắc địa ba mươi năm của các thế hệ kỹ sư địa chất; tra Trấn Thủy Đoản Đao mở chốt khóa thủy lực, kết hợp cùng Mộc Hoàng Lôi Tâm Thạch bình ổn hoàn toàn đứt gãy núi lửa Chư Yang Sin; hội ngộ già Y Dăm và nhận tín hiệu bộ đàm khẩn về Sector 05 Hòn Yến.",
        "Bình ổn tuyệt đối hỏa ngục Chư Yang Sin; tri ân tâm huyết thế hệ cha ông; mở ra hướng đi tiếp theo tại Sector 05 duyên hải Nam Trung Bộ."
    ))

    # Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Vòng tròn hợp kim Earth-Seal 2026 tại Chư Yang Sin được khóa chốt thành công; mạch địa chấn Tây Nguyên hoàn toàn ổn định."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An kết hợp Thuần Dương Cương Huyết với cơ cấu cơ khí chính xác; thể đạo phàm nhân dung hợp hoàn mỹ cùng kỹ nghệ gia truyền của người cha."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-003'
    """, (
        CHAPTER_NUM,
        "Nhật ký trắc địa ba mươi năm xác nhận sự liên kết giữa Viện Khảo sát Địa chất và đồ án cứu non sông; tín hiệu khẩn hướng về Sector 05 Hòn Yến."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T06:45:00+07:00"
        inv_data["current_location"] = "Sườn Đông Núi Lửa Chư Yang Sin, Huyện Krông Bông, Tỉnh Đắk Lắk"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Khí Dung Hợp Thần Binh & Cơ Quan Khóa Địa)"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json.")

    # 9. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> SÁNG TÁC & KIỂM DUYỆT CHƯƠNG {CHAPTER_NUM} HOÀN TẤT THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

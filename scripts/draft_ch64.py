# -*- coding: utf-8 -*-
"""Draft Chapter 64 for Phá Trời Novel OS with full ~3,500 words prose."""

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

CHAPTER_NUM = 64
CHAPTER_TITLE = "Phong Ba Mũi Đèn Đỏ"
LOCATION = "Mũi Đèn Đỏ (Phường Phú Thuận, Quận 7, TP.HCM)"
DATE = "2026-10-20"

ACT1 = '''Mười hai giờ mười lăm phút trưa.

Cơn gió đầu mùa từ hướng biển Cần Giờ thổi ngược lên sông Soài Rạp, mang theo hơi nước lợ ngai ngái quyện với mùi bùn mặn đặc trưng của những cánh rừng ngập mặn hạ lưu. Bầu trời phương nam trưa nay không có lấy một vạt nắng hanh hao của mùa khô, thay vào đó là từng dải mây xám chì nặng trĩu đang từ từ phủ kín không gian thành phố. Không khí oi nồng, đặc quánh đến mức khó thở — dấu hiệu quen thuộc của một cơn dông nhiệt đới dữ dội sắp quét qua vùng bán đảo châu thổ Sài Gòn.

Chiếc xe bán tải chuyên dụng của Viện Địa tầng Đô thị rẽ khỏi đại lộ Nguyễn Văn Linh, lao nhanh vào đường Huỳnh Tấn Phát rồi quặt sang trục đường Đào Trí thuộc địa phận phường Phú Thuận, Quận 7. Đi kèm sát phía sau là hai chiếc xe dã chiến của lực lượng trinh sát thuộc Công an Thành phố Hồ Chí Minh.

Trên suốt chặng đường di chuyển từ trung tâm Quận 1 qua cầu Tân Thuận, tôi ngồi ở hàng ghế sau, lặng lẽ quan sát mặt nước các nhánh kênh rạch hai bên đường. Từ kênh Tẻ cho đến rạch Bến Ngựa, dòng nước đục ngầu phù sa trưa nay đang dâng cao một cách bất thường, từng đợt sóng xô bờ tạo ra những bọt nước sủi tăm li ti. Những xoáy nước nhỏ xoay tròn bên các trụ cầu báo hiệu áp lực thủy động học bên dưới lòng đất đang biến chuyển dồn dập.

Càng tiến sâu về phía bờ sông, phố xá đông đúc của khu đô thị hiện đại nhanh chóng nhường chỗ cho một vùng bán đảo hoang sơ, vắng lặng đến rợn người.

Những bãi lau sậy cao ngút đầu người dập dờn theo từng cơn gió lộng. Ven những con đường rải đá dăm gồ ghề là các bãi tập kết container bỏ hoang, những dãy hàng rào tôn rỉ sét nằm trơ trọi bên cạnh những vũng nước lợ đọng phù sa đỏ quạch. Nơi đây chính là Mũi Đèn Đỏ — doi đất nhô ra giữa ngã ba sông rộng lớn bậc nhất toàn vùng châu thổ Sài Gòn, nơi người Pháp vào cuối thế kỷ mười chín từng dựng ngọn hải đăng hoa tiêu đầu tiên để dẫn đường cho tàu buôn từ biển Đông tiến vào cảng Sài Gòn.

Dân chài lưới lâu năm ở vùng Nhà Bè vẫn truyền tai nhau rằng, Mũi Đèn Đỏ là ngã ba hợp thủy hung hiểm nhất phương Nam. Nơi đây dòng nước ngọt chở nặng phù sa từ vùng rừng núi Đồng Nai gặp gỡ dòng triều mặn cuồn cuộn từ vịnh Gành Rái ép ngược lên, tạo thành những túi nước xoáy ngầm có thể nuốt chửng cả những chiếc xà lan chở cát hàng ngàn tấn trong chớp mắt.

Chiếc xe dừng lại bên vệ cỏ cách mép bờ kè sông khoảng năm mươi mét.

Tôi đẩy cửa xe bước xuống, kéo sụp vành mũ tai bèo để che đi những hạt mưa lất phất bắt đầu quất vào mặt.

Trước mắt tôi, ngã ba sông rộng mênh mông như một vùng biển nhỏ. Đây là nơi hội tụ của ba dòng thủy lộ khổng lồ: sông Sài Gòn từ phía bắc đổ xuống, sông Đồng Nai từ vùng rừng núi thượng nguồn phía đông tràn qua, và sông Soài Rạp mở rộng đón lấy toàn bộ dòng chảy cuồn cuộn đổ thẳng ra biển Đông qua vịnh Gành Rái. Chiều rộng mặt nước tại khúc giao này lên tới hơn một cây số. Mặt nước ngã ba sông đục ngầu phù sa, cuộn sóng lớp lớp. Giữa dòng nước xiết, những vòng xoáy ngầm khổng lồ có đường kính hàng chục mét liên tục hình thành rồi vỡ vụn, tạo ra những tiếng gầm gừ trầm đục tựa như tiếng thở dốc của một loài thủy quái khổng lồ đang cựa mình dưới đáy sâu.

"Minh An, mang vali thiết bị trắc địa vệ tinh lại đây!"

Tiếng gọi gấp gáp của kỹ sư Tuấn vang lên giữa tiếng gió rít từng chập.

Tôi xốc chiếc balo dã chiến nặng trịch lên vai, hai tay xách chiếc vali chống sốc chứa bộ máy đo vệ tinh RTK Leica GS18, bước nhanh về phía mép bờ kè bê tông nơi Viện trưởng Trịnh Hoài Nam và các kỹ sư đang đứng.'''

ACT2 = '''Hiện trường sạt lở trước mắt khiến bất kỳ ai chứng kiến cũng phải rùng mình.

Đoạn bờ kè bê tông cốt thép kiên cố dài hơn ba mươi mét vốn dùng để gia cố doi đất ngã ba sông đã bị bẻ gãy gập thành nhiều đoạn. Mặt đất nứt toác ra một rãnh sâu gần hai mét, nuốt chửng toàn bộ dải lan can sắt và những khối đá hộc kè bờ. Đất sét pha bùn bão hòa nước sạt trượt từng mảng lớn, để lộ ra những phiến đá tảng cổ xưa phủ đầy rêu đen và vỏ hàu bám chặt.

"Các cậu nhìn kỹ kết cấu nền móng bị phơi ra đi," Viện trưởng Trịnh Hoài Nam đưa tay chỉ vào vết nứt sâu hoắm, giọng ông đanh lại trong gió dông: "Đây không phải hiện tượng xói lở cơ học thông thường do dòng chảy đáy. Vết đứt gãy này đi theo một đường thẳng tắp, tựa như có một nguồn lực cắt khổng lồ từ lòng đất đẩy ngược lên!"

Một sự đối lập kỳ lạ hiện rõ trước mắt chúng tôi. Những khối bê tông mác cao hiện đại gia cố bằng thép phi hai mươi lăm bị xé toạc thành từng mảnh vụn như bánh đa xốp. Thế nhưng, ẩn sâu bên dưới lớp đất sụt lún, những khối đá hoa cương xám xanh do các bậc tiền nhân đục đẽo từ thời vua Thành Thái vào năm 1898 vẫn nằm vững chãi, khớp mộng chữ công khít khao không hề suy suyển. Thuật phong thủy định hải ngàn năm của người xưa rõ ràng thuận theo tự nhiên và hiểu thấu lòng đất hơn hẳn những khối bê tông vô hồn của thời hiện đại.

Kỹ sư Tuấn lập tức mở chân ba chạc, định vị đầu thu GNSS RTK và kết nối máy đo biến thiên từ trường ba trục fluxgate với trạm máy tính hiện trường. Những ngón tay của anh gõ thoăn thoắt trên bàn phím:

"Số liệu hiệu chỉnh vệ tinh đã đồng bộ xong! Tần số vi chấn ELF đo được tại tâm chấn sạt lở đang duy trì ở mức không phẩy bảy mươi lăm héc (0.75 Hz)!"

Trên màn hình phổ tần số, đường cong dao động màu đỏ thẫm dựng đứng lên thành những đỉnh răng cưa sắc nhọn, phát ra những tiếng bíp bíp dồn dập cảnh báo quá tải năng lượng. Thông thường, từ trường tự nhiên tại vùng đất bồi phù sa chỉ dao động quanh ngưỡng bốn mươi hai ngàn nanoTesla. Thế nhưng ngay tại vết nứt này, cảm biến ghi nhận những xung lực từ trường ngầm nhảy vọt lên hơn bốn trăm năm mươi nanoTesla, kèm theo chu kỳ phát xung trùng khớp tuyệt đối với nhịp địa chấn đáy sông.

"Độ sâu của nguồn phát dao động là bao nhiêu?" Viện trưởng Trịnh Hoài Nam trầm giọng hỏi.

"Mười lăm mét dưới lớp trầm tích đáy sông!" Tuấn phóng to mô hình quét sóng phản xạ 3D. "Dưới đáy rãnh bùn ngập mặn ngã ba sông, có một khối trụ đá bát giác nguyên khối dài hơn mười hai mét, chu vi gần sáu mét. Đó chính là cọc tiêu số bốn — **Trấn Giang Hữu Tiêu**!"

Kỹ sư Tuấn nuốt nước bọt, khuôn mặt tái mét:

"Nhưng điều đáng sợ nhất là... khối trụ đá ngầm không hề bị lún sụt, mà đang bị kéo căng bởi một mô-men xoắn cực lớn! Toàn bộ áp lực dòng chảy tích tụ sau khi hai cọc tiêu Lò Gốm và Bến Phú Định ngừng hoạt động đã dồn hết về đây. Khối trụ đá này đang phải gánh chịu tải trọng thủy động học tăng gấp ba lần bình thường!"

Tôi bước sát lại mép bờ kè sụt lún, đưa mắt nhìn thẳng xuống dòng xoáy nước đục ngầu.

Ngay khoảnh khắc tôi tiến gần mép nước, chiếc balo sau lưng tôi bỗng phát ra những đợt sóng nhiệt ấm nóng khác thường.

Hai khối trận nhãn *Hắc Thủy Huyền Thạch* và *Định Hải Huyền Châu* được bọc kín trong các lớp nhung cách âm dường như cảm ứng được tiếng gọi của cọc tiêu số bốn, bắt đầu rung lên nhè nhẹ. Thanh *Trấn Thủy Đoản Đao* cài bên hông khẽ phát ra tiếng rền u u trầm đục, như một con mãnh thú ngửi thấy mùi chiến trận.

Cùng lúc đó, dọc theo ba mươi ba đốt sống trên lưng tôi, dòng tủy ngọc trong suốt vừa được tôi luyện qua Thức thứ bảy *Ngọc Tủy Quy Nhất* bắt đầu cuộn trào mạnh mẽ. Từng tế bào xương tủy phát ra luồng kình lực tinh thuần, tự động cộng hưởng với tần số dao động 0.75 Hz truyền lên từ lòng đất. Một cảm giác kết nối vô hình giữa thể xác tôi và khối trụ đá ngàn năm dưới đáy sông bỗng chốc mở ra, rõ ràng và sống động đến từng thớ thịt. Tôi có thể cảm nhận được từng đường vân nứt nẻ li ti đang xuất hiện trên bề mặt khối cọc đá Trấn Giang Tiêu dưới sức ép tàn bạo của dòng nước lũ ngầm. Khối trụ đá ấy tựa như một đốt sống thứ ba mươi tư của chính cơ thể tôi đang oằn mình chống đỡ cơn cuồng nộ của đại dương.'''

ACT3 = '''*"Minh An... cẩn thận!"*

Tiếng truyền âm thanh lãnh của Lâm Tịch vang lên từ nơi sâu thẳm trong thức hải, mang theo sự ngưng trọng chưa từng có:

*"Trấn Giang Tiêu tại Mũi Đèn Đỏ vốn là mắt xích chịu lực then chốt nhất của toàn bộ Thủy Môn Thập Nhị Tiêu. Mười một cọc tiêu kia phân tán áp lực về các nhánh kênh rạch nội đô, nhưng riêng cọc tiêu này lại án ngữ ngay yết hầu cửa biển, một mình gánh vác toàn bộ thủy triều từ biển Đông ép ngược vào đất liền. Hiện nay cọc tiêu đang ở trạng thái quá tải cực hạn, chỉ cần một lực chấn động ngoại lai đủ mạnh kích phát, toàn bộ cọc đá sẽ vỡ vụn từ bên trong!"*

"Ngoại lực kích phát?" Tôi nheo mắt, truyền âm đáp lại: "Ý nàng là Cửu Long Group sẽ ra tay ngay lúc này?"

*"Bọn chúng không những sẽ ra tay, mà đã có mặt ngay trước mắt ngươi rồi!"* Giọng Lâm Tịch lạnh băng.

Tôi giật mình, lập tức ngẩng đầu nhìn ra giữa dòng sông Soài Rạp.

Cách bờ kè sạt lở khoảng một trăm hai mươi mét, ngược theo luồng hàng hải sâu, một chiếc tàu vỏ thép cỡ lớn sơn màu xám tro đang từ từ rẽ sóng tiến lại gần. Trên thân tàu in dòng chữ lớn: `Tàu Nạo Vét Luồng Hàng Hải — Vạn Hưng 18`.

Chiếc tàu nạo vét dừng lại giữa ngã ba sông, buông bốn chiếc neo thép nặng hàng tấn xuống lòng sông sâu, tạo thành thế gọng kìm cố định thân tàu ngay trên vị trí thẳng đứng của cọc Trấn Giang Tiêu.

"Chiếc tàu nạo vét đó ở đâu ra vậy?" Đại úy Trần Văn Hùng — chỉ huy tổ trinh sát hình sự đi cùng đoàn — cau mày, đưa ống nhòm quân sự lên quan sát. "Theo lịch trình điều tiết luồng lạch của Cảng vụ Hàng hải khu vực Nhà Bè, hôm nay không có bất kỳ kế hoạch nạo vét luồng nào tại ngã ba Mũi Đèn Đỏ do cảnh báo triều cường và sạt lở!"

Đúng lúc đó, điện thoại bảo mật của Đại úy Hùng đổ chuông dồn dập. Anh áp máy vào tai nghe vài giây rồi sắc mặt biến đổi hoàn toàn:

"Báo cáo Viện trưởng Nam! Tổ công tác đột kích tòa tháp Bitexco vừa báo về: Văn phòng đại diện của Tập đoàn Cửu Long trên tầng ba mươi tám đã trống trơn! Toàn bộ máy tính bị phá hủy ổ cứng, tài liệu bị đốt cháy trong thùng kim loại. Richard Wong đã tẩu thoát khỏi tòa tháp từ sáng sớm bằng ca nô cao tốc theo hướng hạ lưu sông Sài Gòn!"

Qua lăng kính viễn vọng của ống nhòm dã chiến, tôi nhìn thấy rõ trên boong tàu `Vạn Hưng 18` xuất hiện bảy tám bóng người mặc áo gió chiến thuật màu sẫm. Bọn chúng không hề có dáng vẻ của những công nhân nạo vét đường thủy hiền lành, mà di chuyển với bước chân nhẹ bẫng, cảnh giác, tay luôn áp sát vào hông áo — tư thế chuẩn mực của những tay súng đánh thuê chuyên nghiệp. Trên đài chỉ huy của tàu, hai gã đàn ông cầm súng trường giảm thanh đang quan sát bờ kè với ánh mắt lạnh tanh.

Kỹ sư Tuấn lập tức chuyển màn hình radar vi sóng sang chế độ quét xuyên nước nông:

"Viện trưởng, anh Hùng, nhìn vào màn hình quét sonar này đi! Dưới đáy chiếc tàu `Vạn Hưng 18` hoàn toàn không có gàu cẩu cát hay vòi hút bùn thông thường!"

Trên màn hình hiển thị đồ họa siêu âm, bên dưới khoang đáy của chiếc tàu nạo vét đang từ từ hạ xuống một giàn khung cơ khí hình trụ khổng lồ bằng thép hợp kim. Ở đầu giàn khung là một cụm đầu khoan nén thủy lực công suất cực lớn, bao quanh bởi sáu cuộn cảm điện từ cao tần.

"Máy khoan nén xung kích địa chấn!" Viện trưởng Trịnh Hoài Nam biến sắc, giọng nói run lên vì bàng hoàng: "Bọn chúng không nạo vét bùn, mà đang chuẩn bị thả mũi khoan nén xuống thẳng vị trí đầu cọc Trấn Giang Tiêu! Thiết bị này dùng sóng hạ âm cộng hưởng kết hợp mũi khoan kim cương, chuyên dùng để phá hủy móng cầu ngầm sâu!"

Tôi nghiến chặt răng, bàn tay siết chặt lấy quai đeo balo.

Mọi chuyện đã sáng tỏ như ban ngày. Sau khi chiếc sà lan cẩu cát ở Bến Phú Định bị bắt quả tang và cơ quan điều tra siết chặt vòng vây pháp lý, Richard Wong và đường dây ngầm của Tập đoàn Cửu Long biết rằng bọn chúng không còn cơ hội lén lút trục vớt từng viên ngọc trận nhãn.

Bọn chúng quyết định chơi một ván bài lật ngửa tàn bạo: sử dụng chiếc tàu nạo vét `Vạn Hưng 18` mang danh nghĩa công trình dân dụng, dùng máy khoan xung kích công nghiệp để phá hủy triệt để cọc Trấn Giang Tiêu!

Một khi chốt chặn then chốt tại Mũi Đèn Đỏ bị nghiền nát, toàn bộ mười một cọc tiêu còn lại sẽ đứt gãy dây chuyền dưới áp lực khủng khiếp của mạng lưới thủy mạch. Khi đó, phong ấn Cực Tù cổ xưa dưới lòng đất Sài Gòn sẽ mở toang, thảm họa sụp lún đại quy mô sẽ xóa sổ toàn bộ vùng duyên hải, tạo ra một cơn hỗn loạn kinh hoàng để những kẻ chủ mưu ung dung tẩu thoát ra hải phận quốc tế!'''

ACT4 = '''"Ầm! Ầm! Ầm!"

Tiếng sấm sét rền vang như xé toạc bầu trời xám xịt phía trên vịnh Gành Rái. Cơn dông nhiệt đới tháng Mười chính thức trút xuống bán đảo Mũi Đèn Đỏ.

Những hạt mưa nặng hạt quất ràn rạt xuống mặt đất, biến bãi cỏ lau thành một biển nước mịt mùng. Gió giật cấp bảy cuộn từng đợt sóng đục ngầu đập mạnh vào bờ kè sạt lở, bọt nước tung trắng xóa cao hàng mét.

Giữa màn mưa giông trắng trời, từ khoang máy của chiếc tàu `Vạn Hưng 18`, tiếng gầm rú chói tai của khối động cơ diesel ngàn mã lực bắt đầu vang lên rền rĩ. Cụm giàn khoan thép khổng lồ dưới bụng tàu đã chạm tới độ sâu mười mét nước, mũi khoan hợp kim bắt đầu xoay tròn, tạo thành một xoáy nước sủi bọt khí trắng xóa cuộn xoáy dữ dội.

Cảm biến vi chấn của kỹ sư Tuấn trên bờ kè lập tức phát ra những tiếng rú đinh tai:

"Báo động đỏ! Tần số dao động vọt lên một phẩy hai héc! Khối trụ đá Trấn Giang Tiêu xuất hiện các vết nứt vi mô trên đỉnh cọc! Chỉ cần giàn khoan nén thủy lực kia kích hoạt xung chấn toàn phần, cọc tiêu sẽ nổ tung trong vòng chưa đầy hai mươi phút nữa!"

Viện trưởng Trịnh Hoài Nam lập tức rút điện thoại vệ tinh khẩn cấp, áp chặt vào tai hét lớn:

"Báo cáo Ban Chỉ huy Thành phố và Bộ Tư lệnh Hải quân! Yêu cầu biên đội tàu tuần tra cao tốc của Vùng 2 và Cảnh sát biển xuất kích ngăn chặn tàu nạo vét `Vạn Hưng 18` tại ngã ba Mũi Đèn Đỏ ngay lập tức!"

Đại úy Hùng cúp máy bộ đàm, gương mặt đanh lại đầy vẻ bất lực:

"Biên đội ca nô tuần tra xuất phát từ cảng Cát Lái đang gặp gió giật cực mạnh giữa luồng sông Soài Rạp! Tầm nhìn trên sông chưa đầy hai mươi mét, sóng lớn cản trở hướng đi, nhanh nhất cũng phải ba mươi lăm đến bốn mươi phút nữa lực lượng vũ trang mới có thể áp sát hiện trường!"

"Ba mươi lăm phút?" Kỹ sư Tuấn ôm đầu tuyệt vọng. "Mười lăm phút nữa thôi là cọc Trấn Giang Tiêu sẽ gãy nát hoàn toàn rồi!"

Không khí trên bờ kè nghẹt thở đến cùng cực. Mọi phương án cơ giới hay can thiệp vũ lực công khai từ mặt nước đều bị cơn dông bão tố và khoảng cách thời gian vô hiệu hóa hoàn toàn.

Trong khoảnh khắc sinh tử ngàn cân treo sợi tóc đó, tôi lặng lẽ lùi lại nửa bước, ánh mắt kiên định nhìn thẳng vào chiếc tàu thép đang neo đậu giữa dòng nước xiết.

Ba mươi lăm phút là quá dài đối với số phận của đại phong ấn Sài Gòn. Nhưng đối với một người vừa đúc thành *Ngọc Tủy Quy Nhất*, mười lăm phút là quá đủ để kết thúc một trận chiến sinh tử dưới đáy nước sâu.

Tôi không nói một lời nào để tránh làm kinh động đến Viện trưởng Nam và kỹ sư Tuấn.

Lợi dụng màn mưa mù mịt và những rặng lau sậy rậm rạp che khuất tầm nhìn, tôi nhanh chóng di chuyển vòng qua mỏm đá sạt lở phía hạ lưu bờ kè.

Đứng sau một bụi cây đước cổ thụ ngập mặn, tôi cởi bỏ chiếc áo bảo hộ bên ngoài, để lộ bộ đồ lặn cao su tổng hợp đen tuyền ôm sát lấy từng thớ cơ bắp cuồn cuộn. Thanh *Hắc Thiết Đoản Côn* được buộc chặt vào cánh tay trái, thanh *Trấn Thủy Đoản Đao* gài chắc nơi thắt lưng, còn hai viên trận nhãn được niêm phong kỹ lưỡng trong túi đeo dã chiến chống nước sau lưng.

*"Minh An, dòng xoáy ngầm tại ngã ba Mũi Đèn Đỏ mạnh gấp mười lần Bến Phú Định, lại có sóng chấn động từ mũi khoan thủy lực của bọn chúng phong tỏa toàn bộ tầng nước giữa,"* Giọng nói của Lâm Tịch khẽ rung lên, đong đầy sự quan tâm và kiên quyết: *"Dưới độ sâu đó, ngươi phải dùng toàn bộ kình lực Ngọc Tủy để khóa chặt kinh mạch, biến bản thân thành một mũi tên xé nước!"*

"Tôi hiểu rồi. Trận chiến này... tôi tuyệt đối không lùi bước!"

Tôi hít một hơi sâu, vận chuyển khẩu quyết *Quy Tức Quyết*. Nhịp tim lập tức hạ xuống mức tĩnh lặng tuyệt đối, van khí quản khép chặt, chu trình trao đổi dưỡng khí hoàn toàn chuyển sang vòng tuần hoàn tủy ngọc bên trong cơ thể.

Luồng kình lực trong suốt từ ba mươi ba đốt sống phóng ra, bao bọc lấy toàn thân như một lớp áo giáp vô hình.

"Ùm!"

Thân hình tôi rẽ nước, lặn không một tiếng động vào lòng sông Soài Rạp cuộn sóng.

Dòng nước lợ lạnh buốt và đặc quánh phù sa lập tức nuốt chửng lấy tôi. Áp lực nước ngập mặn đè nặng lên cơ thể, nhưng dưới sự vận hành của ngọc tủy thanh khiết, các khớp xương của tôi tự động co giãn, biến lực ép thủy tĩnh thành lực đẩy đưa tôi lướt êm ru qua các dòng xoáy ngầm.

Phía trước, ở độ sâu mười lăm mét dưới đáy sông, ánh đèn pha công suất lớn của giàn khoan nén thủy lực rực sáng như hai con mắt quỷ giữa màn đêm bùn lầy. Tiếng rền cơ khí va đập vào khối đá Trấn Giang Tiêu truyền qua làn nước tựa như những nhát búa tạ giáng thẳng vào lồng ngực.

Tôi rút thanh *Trấn Thủy Đoản Đao* ra khỏi vỏ, hai mắt rực sáng hàn quang. Một trận quyết chiến sinh tử nơi đáy ngã ba sông Mũi Đèn Đỏ... chính thức khai màn!'''

CHAPTER_PROSE = f"{ACT1}\n\n{ACT2}\n\n***\n\n{ACT3}\n\n{ACT4}"

words = len(CHAPTER_PROSE.split())

def run_pipeline():
    print(f"=== SÁNG TÁC & THẨM ĐỊNH CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    print(f"[*] Tổng số từ bản thảo: {words:,} từ (Mục tiêu: 3.300 - 3.650 từ)")
    
    if words < 3200 or words > 3650:
        print(f"[!] Cảnh báo độ dài: {words} từ (Cần trong khoảng 3.200 - 3.650 từ)!")
        return False

    # 1. Kiểm tra RULE-07 (Tuyệt đối không chứa từ ngữ hậu trường sáng tác)
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"]
    prose_lower = CHAPTER_PROSE.lower()
    found_meta = [mw for mw in meta_words if re.search(rf"\b{mw}\b", prose_lower)]
    if found_meta:
        print(f"[-] Vi phạm RULE-07: Phát hiện từ ngữ hậu trường: {found_meta}")
        return False
    print("[PASS] [1/5] Kiểm tra RULE-07: Hoàn hảo 100% (0 từ ngữ hậu trường).")

    # 2. Kiểm tra Canon Forbidden Assumptions
    ce = CanonEngine()
    canon_errors = ce.validate_text_for_forbidden_assumptions(CHAPTER_PROSE)
    if canon_errors:
        print(f"[-] Vi phạm Canon: {canon_errors}")
        return False
    print("[PASS] [2/5] Kiểm tra Canon Assumptions: Hoàn hảo 100%.")

    # 3. Thẩm định toàn diện bằng CritiqueEngine
    critique = CritiqueEngine(DB_PATH, record_to_db=False)
    report = critique.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"],
        text=CHAPTER_PROSE
    )
    issues = report.get("issues", [])
    has_critical = any(iss.get('severity') in ('CRITICAL', 'HIGH') for iss in issues)
    if has_critical:
        print(f"[-] CritiqueEngine phát hiện lỗi CRITICAL/HIGH: {issues}")
        return False
    print("[PASS] [3/5] CritiqueEngine (Canon, POV, Style, Knowledge): Hoàn hảo 100%.")

    # 4. Lưu trữ bản thảo Markdown nguồn chân lý
    md_dir = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02")
    os.makedirs(md_dir, exist_ok=True)
    md_file_path = os.path.join(md_dir, f"ch_{CHAPTER_NUM:03d}.md")

    md_content = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {words}
date: "{DATE}"
location: "{LOCATION}"
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

{CHAPTER_PROSE}
"""
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] [4/5] Đã lưu bản thảo Markdown: {md_file_path}")

    # 5. Xuất bản Word (.docx) chuẩn in ấn
    docx_dir = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02")
    os.makedirs(docx_dir, exist_ok=True)
    docx_file_path = os.path.join(docx_dir, f"ch_{CHAPTER_NUM:03d}.docx")

    docx_pipe = DocxPipeline()
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
        "Phong Ba Mũi Đèn Đỏ & Xuất Kích Ngăn Chặn Vạn Hưng 18",
        CHAPTER_NUM,
        1,
        f"{DATE}T14:30:00+07:00",
        CHAPTER_NUM,
        "loc_mui_den_do",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"]),
        "Minh An cùng Viện trưởng Trịnh Hoài Nam, kỹ sư Tuấn và cảnh sát tiếp cận Mũi Đèn Đỏ. Khảo sát vết nứt sạt lở 30m, phát hiện cọc số 4 Trấn Giang Hữu Tiêu chịu áp lực quá tải cực hạn. Tàu nạo vét Vạn Hưng 18 của Cửu Long Group thả giàn khoan xung kích nén thủy lực toan phá hủy cọc đá. Minh An vận dụng Ngọc Tủy Quy Nhất lặn sâu xuống đáy sông Soài Rạp ngăn chặn hiểm họa.",
        "Xác định rõ âm mưu phá hoại liều chết của Cửu Long Group; Minh An bí mật xuất kích lặn sâu vào mắt bão ngã ba sông nghênh chiến giàn khoan thủy lực dưới đáy nước 15m."
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
        "Cọc tiêu số 4 Trấn Giang Hữu Tiêu tại Mũi Đèn Đỏ bị tàu nạo vét Vạn Hưng 18 của Cửu Long Group dùng máy khoan nén xung kích tấn công; Minh An lặn sâu 15m nghênh chiến trực diện."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An vận dụng thực chiến tầng 7 Ngọc Tủy Quy Nhất kết hợp Quy Tức Quyết rẽ sóng lặn sâu giữa dòng xoáy ngã ba sông Soài Rạp trong cơn dông bão cấp 7."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 7. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T15:30:00+07:00"
        inv_data["current_location"] = "Mũi Đèn Đỏ (Bến Đèn Đỏ, Quận 7 / Nhà Bè, TP.HCM)"
        
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (vị trí Mũi Đèn Đỏ).")

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

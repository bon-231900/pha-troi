# -*- coding: utf-8 -*-
"""Draft Chapter 68 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 68
CHAPTER_TITLE = "Thanh Long Lân Kiếm"
LOCATION = "Lòng rạch Bến Nghé — Chân mố Cầu Mống (TP.HCM)"
DATE = "2026-10-22"

ACT1 = '''Mười một giờ đêm ngày hai mươi mốt tháng Mười.

Gió đêm từ hướng sông Sài Gòn thổi thốc vào lòng rạch Bến Nghé, mang theo hơi nước ẩm mặn quyện lẫn mùi bùn non đặc trưng của vùng châu thổ. Dọc đôi bờ Võ Văn Kiệt và Bến Vân Đồn, dòng xe cộ đã thưa thớt. Ánh đèn vàng hắt xuống mặt kênh phẳng lặng, rọi bóng vòm thép cong của Cầu Mống in thẫm trên nền nước tối sẫm. Nhưng phía sau vẻ tĩnh lặng của trung tâm phố thị, bầu không khí dưới chân mố cầu phía Quận 4 lại ngột ngạt và căng thẳng vô cùng.

Trên chiếc xà lan kỹ thuật của Viện Địa tầng neo sát bờ kè đá hoa cương, ánh đèn màn hình máy tính dã chiến hắt lên gương mặt đăm chiêu của kỹ sư Tuấn. Anh đeo tai nghe chuyên dụng, hai ngón tay gõ nhịp liên tục lên bàn phím, đôi lông mày nhíu chặt lại sau tròng kính cận:

"Minh An, tín hiệu sóng âm phản xạ tầng sâu từ ba mươi tám mét dưới đáy bùn đang biến thiên cực kỳ quái dị. Các cảm biến áp điện cắm quanh bốn trụ cầu vừa ghi nhận một dải xung chấn tần số một trăm bốn mươi kilo-Hertz. Tần số này hoàn toàn không phải dao động địa chấn tự nhiên hay tiếng ồn cơ giới của xà lan nạo vét."

Tôi mặc bộ đồ lặn dã chiến màu đen tuyền bằng cao su tổng hợp cách nhiệt, bên hông cài chắc thanh Trấn Thủy Đoản Đao bọc kín trong bao da chống thấm, lưng mang hai bình dưỡng khí nén áp suất cao. Nghe Tuấn nói, tôi bước lại gần nhìn vào đồ thị phổ:

"Anh Tuấn, đồ thị này có điểm gì khác thường?"

Tuấn trỏ ngón tay vào chuỗi đỉnh sóng nhấp nhô có chu kỳ lặp lại chính xác đến từng phần nghìn giây:

"Đây là tín hiệu điều khiển kỹ thuật số mã hóa tầm xa. Có ít nhất bốn nguồn phát sóng siêu âm công suất lớn đang được gắn trực tiếp vào các khe nứt của khối thạch đài cổ dưới chân mố cầu. Chúng phát ra xung lực dao động cưỡng bức nhằm làm rạn nứt cấu trúc tinh thể đá bazan. Nếu bọn chúng đồng loạt kích hoạt bộ dao động cực hạn vào lúc các xe tải nặng thử tải lăn bánh lên cầu trưa mai, toàn bộ chân mố cầu phía Quận 4 sẽ lập tức nứt vỡ từ bên trong bởi hiện tượng cộng hưởng cơ học!"

Tôi siết chặt nắm tay, từng khớp ngón tay phát ra tiếng kêu giòn đanh. Đúng như Lâm Tịch đã cảnh báo, tàn dư Cửu Long Thiên Hải sau thất bại ở Mũi Đèn Đỏ đã âm thầm cài đặt trận bàn cộng hưởng siêu âm dưới tầng bùn sâu nhằm bẻ gãy long mạch rạch Bến Nghé ngay tại yết hầu Cầu Mống.

"Bác Trịnh Hoài Nam đã liên hệ với lực lượng tuần tra đường thủy chưa anh?" Tôi hỏi.

"Đã phong tỏa toàn bộ luồng lạch trong bán kính năm trăm mét từ ngã ba sông Sài Gòn vào rạch Bến Nghé," Tuấn gật đầu, giọng đanh lại. "Hai ca-nô tuần tra đang chốt chặn hai đầu kênh. Nhưng ở độ sâu gần bốn chục mét dưới đáy bùn đen đặc, áp lực nước cực lớn, người thường không thể lặn xuống xử lý."

"Việc đó để em lo," tôi đáp dứt khoát.

Trong thức hải, hoa sen ngọc bích chậm rãi xoay chuyển. Lâm Tịch ngồi tĩnh tọa trên đài sen, thanh âm trong trẻo như tiếng ngọc khánh vang vọng bên tai tôi:

*"Minh An, cọc tiêu số năm Thanh Long Lân Kiếm là một thanh bảo kiếm viễn cổ mang tính Thủy cực thịnh. Trận bàn cộng hưởng của kẻ thù đang mượn chính nguồn năng lượng âm hàn của kiếm để khuếch đại xung chấn phá hoại. Ngươi phải lặn xuống, vô hiệu hóa các trục neo xung chấn trước, sau đó mới dùng kình lực Thể Đạo tháo gỡ thanh kiếm khỏi mắt trận. Một khi kiếm rời trận nhãn mà mạch nước chưa được an định, toàn bộ áp lực địa tầng tích tụ hàng ngàn năm sẽ trào ngược lên như vòi rồng."*

"Ta hiểu rồi," tôi thầm đáp lại Lâm Tịch.

Tôi kiểm tra lại van thở, kéo kính lặn chuyên dụng che kín mặt, rồi bước ra mạn xà lan. Nước rạch Bến Nghé đen ngòm, lững lờ trôi dưới ánh trăng mờ nhạt. Tôi khẽ hít một hơi sâu, vận chuyển khẩu quyết Thức thứ bảy *Ngọc Tủy Quy Nhất*. Dòng tủy ngọc trong xương tủy lập tức tỏa ra luồng nhiệt lượng ấm áp lan tỏa khắp tứ chi, xua tan cái lạnh buốt của đêm thu.

"Bõm!"

Tôi thả mình xuống dòng nước tối thẫm, lặn sâu vào lòng rạch Bến Nghé.'''

ACT2 = '''Làn nước đen ngòm lạnh buốt lập tức ôm trọn lấy thân thể tôi.

Áp lực dòng chảy mùa triều cường cuộn xiết, đẩy những lớp bùn lỏng và tạp chất trôi dạt đập vào kính lặn. Tầm nhìn nhanh chóng sụt giảm xuống mức gần như mù mịt. Nếu là một thợ lặn bình thường, với bóng tối đặc quánh và độ đục của đáy rạch Bến Nghé, việc định hướng sẽ hoàn toàn phụ thuộc vào dây tiêu và la bàn từ tính.

Thế nhưng, la bàn từ tính lúc này lại xoay tròn vô định do từ trường biến dạng dưới đáy sâu.

Tôi không hề hoang mang. Tôi nhắm mắt lại, khép kín ngũ quan phàm trần và kích hoạt trực giác Thể Đạo. Khi dòng tủy ngọc trong cột sống bắt nhịp đồng bộ với dao động không phẩy mười hai Hertz dội lên từ lòng đất mẹ, cả không gian ngầm dưới đáy sông bỗng hiện rõ mồn một trong tâm trí tôi như một bức đồ họa lập thể ba chiều. Từng dòng xoáy ngầm cuộn chảy, từng khe nứt trên mố đá hoa cương của Cầu Mống, và cả khối thạch đài bazan cổ xưa nằm sâu dưới ba mươi tám mét đáy bùn đều hiện lên rành mạch.

Tôi bơi lặn xuống theo thân mố cầu trụ số hai.

Đến độ sâu mười lăm mét, lớp nước bắt đầu chuyển sang một tầng nhiệt độ dị thường. Hàn khí buốt giá xuyên qua lớp cao su dày của bộ đồ lặn, mang theo mùi khoáng thạch cổ. Đây chính là hàn sát từ Thanh Long Tả Tiêu.

Đột nhiên, linh giác tôi rung lên một tiếng chuông cảnh báo sắc lẹm!

Từ phía bên phải mố cầu, một luồng nước ngầm bị rẽ ra với tốc độ cực nhanh. Một bóng đen thon dài lướt tới như một con thủy quái săn mồi giữa màn đêm.

"Vút!"

Một mũi lao thép phi tiêu ngầm xé toạc làn nước đen, lao thẳng vào chấn thủy lồng ngực tôi!

Tôi không chút nao núng. Thân hình tôi uốn cong nhẹ nhàng giữa dòng nước theo thế *Long Đằng Phách Lãng*, né tránh mũi lao thép chỉ trong đường tơ kẽ tóc. Mũi lao cắm phập vào mố đá hoa cương phía sau, làm đá vụn bắn tung tóe dưới đáy nước.

Tôi mở mắt nhìn về hướng luồng nước vừa dao động. Nhờ ánh huỳnh quang lân tinh phát ra từ tủy ngọc, tôi thấy rõ ba bóng người nhái trang bị đồ lặn chuyên nghiệp màu xám tro, mang mặt nạ thở tuần hoàn khép kín không sủi bọt khí. Trên vai áo bọn chúng thêu phù hiệu chim ưng xanh ngọc quắp đầu rồng bằng chỉ kim tuyến — ấn ký của toán người nhái Hắc Giao Đường Ma Cao trực thuộc Cửu Long Thiên Hải!

Bọn chúng đã mai phục sẵn dưới chân mố cầu từ nhiều giờ trước để canh giữ trận bàn cộng hưởng!

Nhận thấy đòn bắn lén không trúng đích, tên người nhái dẫn đầu lập tức vung tay ra hiệu. Hai tên bơi kèm hai bên lập tức rút ra hai thanh đoản đao ngầm bằng hợp kim vonfram chống gỉ, đạp chân vịt lao vút tới giáp công tôi từ hai mạn sườn. Đao quang xé toạc bóng tối, mang theo lực đạo cuồn cuộn của những kẻ đạt cảnh giới Luyện Cốt sơ kỳ.

Tôi bình thản lơ lửng giữa dòng nước xoáy, hai tay buông lỏng tự nhiên.

Khi lưỡi đao của tên bên trái chỉ còn cách cổ họng tôi gang tấc, tôi đột ngột phát lực. Thức thứ bảy *Ngọc Tủy Quy Nhất* bùng nổ trong tích tắc!

"Keng!"

Tôi không rút vũ khí, mà dùng sống cẳng tay bọc kình khí tủy ngọc gạt phăng mũi đao của đối phương. Kình lực Thể Đạo cô đọng cứng cáp như kim cương va chạm vào thanh đao hợp kim, phát ra một âm thanh trầm đục lan truyền qua môi trường nước. Kình lực chấn động làm cánh tay đối phương run rẩy, thanh đao tuột khỏi tay chìm xuống bùn.

Không để hắn kịp ổn định tư thế, tôi bước tới một bước giữa làn nước xiết, chưởng phong áp sát ngực hắn đánh ra một chiêu *Kính Phách Phản Chấn*.

"Ầm!"

Một luồng sóng xung kích vô hình khuếch tán dưới nước. Tên người nhái bị chấn bay xa hơn năm mét, va đập mạnh vào thân mố cầu đá, bình dưỡng khí sau lưng rạn nứt sủi bọt trắng xóa. Hắn ngất lịm, buông xuôi thân hình trôi dạt theo dòng nước ngầm.

Hai tên còn lại kinh hãi tột độ khi chứng kiến sức mạnh nhục thân kinh người của một đối thủ không mang vũ khí hạng nặng. Tên cầm súng bắn lao vội vàng nạp lại mũi tên tiếp theo, nhưng tốc độ của hắn làm sao sánh kịp với kình phong Thể Đạo!

Tôi lướt tới như một tia chớp dưới lòng sông sâu. Bàn tay phải tôi vung lên, thanh Trấn Thủy Đoản Đao nơi thắt lưng tuốt khỏi vỏ. Một dải hào quang hoàng kim đồng thau rực rỡ bừng sáng giữa đáy nước đen ngòm, xé toạc bóng tối của rạch Bến Nghé!

"Xoẹt!"

Lưỡi đoản đao rỉ sét cổ xưa chém đứt đôi khẩu súng phóng lao khí nén và chém rách ống dẫn khí của tên thứ hai. Dưới uy áp Thể Đạo Luyện Cốt trung kỳ, hai tên tàn dư lập tức mất hết sức chiến đấu, ôm ngực ngoi vội lên mặt nước tháo chạy.

Tôi không đuổi theo những kẻ bại trận. Trọng trách cấp bách lúc này nằm ở ba mươi tám mét dưới đáy bùn sét!'''

ACT3 = '''Tôi quay người, cắm đầu lặn thẳng xuống đáy bùn sâu.

Vượt qua tầng bùn nhão phù sa dày hơn mười mét, tôi chạm đến tầng sét cứng cổ xưa của địa tầng Sài Gòn. Ở độ sâu ba mươi tám mét, áp lực thủy tĩnh đè nặng lên màng nhĩ và lồng ngực tựa như có cả một cỗ máy nghiền khổng lồ ép xuống. Nếu không có kình khí tủy ngọc bảo vệ nội tạng, thợ lặn bình thường sẽ bị tổn thương phổi nghiêm trọng.

Trước mắt tôi hiện ra một cảnh tượng tráng lệ đến ngạt thở.

Nằm sâu dưới phù sa là đàn tế đá bazan hình tròn rộng chừng mười sáu mét, được gọt đẽo vuông vức. Bề mặt đá bazan phủ rêu phong, lộ rõ hoa văn mặt trời nhiều tia rực rỡ và những cánh chim lạc dang rộng đôi cánh — minh văn thiêng liêng của văn minh Đông Sơn thời dựng nước Văn Lang!

Bốn góc đàn tế đá cổ bị đục khoét bởi các mũi khoan kỹ thuật hiện đại.

Bốn khối kim loại hình trụ xám đen được gắn chặt vào các khe nứt then chốt của đàn tế bằng bulong titan. Đèn led trên thân khối trụ nhấp nháy đỏ dồn dập, phát sóng siêu âm làm rung chuyển tầng sét đáy sông, khiến những vết nứt dài ngoằn ngoèo lan dần về phía trung tâm đàn tế!

"Đây chính là bốn trục neo của trận bàn cộng hưởng siêu âm!" Tôi thầm nhủ.

Thời gian không còn nhiều. Đèn tín hiệu trên thiết bị đã chuyển sang nhịp nhấp nháy màu đỏ tươi với tần suất hai lần mỗi giây, báo hiệu tiến trình kích xung chấn sắp đạt đến ngưỡng cực hạn.

Tôi lập tức bơi tới khối trụ kim loại đầu tiên. Vung thanh Trấn Thủy Đoản Đao, tôi dồn toàn bộ kình lực Thể Đạo vào mũi đao, nhắm chuẩn xác vào các chốt liên kết cơ khí và cáp tín hiệu bằng sợi quang thủy tinh.

"Keng! Keng! Phập!"

Lưỡi đoản đao đồng thau cổ xưa dưới sự gia trì của kình lực Ngọc Tủy sắc bén hơn bất kỳ lưỡi cưa plasma hiện đại nào. Tôi vung đao dứt khoát, chặt đứt toàn bộ bốn ngàm kẹp titan và đường dây dẫn xung điện của khối trụ thứ nhất. Chiếc máy siêu âm rung lên một tiếng rạn vỡ rồi tắt ngấm đèn led, rơi rụng xuống lớp bùn sét.

Không dừng lại một giây, tôi thoăn thoắt di chuyển sang vị trí thứ hai, thứ ba rồi thứ tư.

Bằng những nhát chém chuẩn xác kết hợp lực tay ngàn cân, tôi lần lượt vô hiệu hóa toàn bộ bốn trục neo cộng hưởng. Âm thanh rít gào của sóng siêu âm biến mất, trả lại sự yên bình cho đáy rạch ngàn năm.

Nhưng đúng lúc cỗ máy cuối cùng ngừng hoạt động, một biến động dữ dội khác lại bùng phát!

Thiếu đi lực dao động cưỡng bức của sóng siêu âm kiềm tỏa, luồng khí tức ngầm bị nén chặt suốt nhiều ngày qua dưới tâm đàn tế đột ngột mất thăng bằng. Mặt sàn đá bazan rung chuyển dữ dội. Từ một khe nứt lớn ngay chính giữa đàn tế, một cột sáng màu xanh ngọc bích rực rỡ bắn thẳng lên trời, nhuộm sáng cả vùng nước đáy sông u tối!

Trong cột sáng xanh biếc ấy, một thanh cổ kiếm cắm sâu ngập nửa thân kiếm vào nanh đá bazan đang rung lên từng nhịp, phát ra tiếng kiếm minh ngân vang trầm hùng như tiếng rồng gầm thét xé tan đáy nước!

Đó chính là cọc tiêu số năm: **Thanh Long Lân Kiếm**!'''

ACT4 = '''Tôi nín thở bơi lại gần tâm đàn tế.

Thanh kiếm dài chừng một mét mốt, toàn thân toát lên sắc xanh lục biếc của ngọc phỉ thúy thượng hạng, trong suốt không chút tì vết. Dọc hai bên thân kiếm, những đường vân tự nhiên uốn lượn xếp tầng tầng lớp lớp tựa như hàng vạn chiếc vảy rồng lấp lánh dưới đáy nước. Sống kiếm dày dặn, khắc chìm một hàng triện văn cổ xưa hình ngọn lửa và mặt trời — tương đồng với ký tự linh phù khắc trên mặt Trống Đồng Ngọc Lũ trong tài liệu khảo cổ của Viện!

Luồng hàn khí tỏa ra từ thân kiếm buốt giá đến mức làm nước xung quanh đông kết thành những hạt tinh thể băng nhỏ li ti lơ lửng giữa dòng nước mặn.

*"Minh An, cẩn thận!"* Tiếng Lâm Tịch vang lên từ thức hải, mang theo sự nhắc nhở trang trọng. *"Thanh Long Lân Kiếm này đã trấn giữ nanh long mạch ngã ba kênh Bến Nghé suốt hai ngàn năm qua, hấp thu vô lượng thủy sát và linh khí sông ngòi. Kiếm phách của nó vô cùng kiêu hãnh. Nếu ngươi dùng sức phàm cưỡng ép nhổ kiếm, kiếm khí phản phệ sẽ đóng băng toàn bộ kinh mạch và lục phủ ngũ tạng trong nháy mắt!"*

"Vậy phải làm thế nào để thu phục được kiếm phách?" Tôi truyền âm hỏi.

*"Lấy huyết dịch làm cầu nối, dùng tủy ngọc làm lò luyện! Ngươi hãy rạch đầu ngón tay, nhỏ một giọt tinh huyết chứa kình lực Ngọc Tủy Quy Nhất lên chuôi kiếm, sau đó dẫn dắt kiếm khí dung hòa vào nhịp đập của cột sống!"*

Tôi gật đầu hiểu ý. Không chần chừ, tôi tháo găng tay lặn bên phải. Dưới đáy nước buốt giá, tôi vận kình ép giọt máu tươi đỏ thắm rỉ ra từ ngón trỏ. Giọt máu không bị dòng nước cuốn trôi, ngưng đọng tròn trịa như hạt hồng ngọc nhờ kình lực Thể Đạo bao bọc.

Tôi đưa bàn tay phải áp thẳng lên chuôi kiếm ngọc vảy rồng!

"Xoẹt!"

Khoảnh khắc giọt tinh huyết chạm vào vân vảy rồng trên chuôi kiếm, toàn bộ thanh cổ kiếm bỗng rực sáng rạng ngời!

Một luồng hàn khí tinh thuần tựa như băng tuyết ngàn năm từ thân kiếm cuồn cuộn tràn qua lòng bàn tay, xông thẳng vào kinh mạch cánh tay phải rồi lao thẳng vào cột sống tôi. Cảm giác buốt giá khiến toàn thân run rẩy, lớp da bên ngoài phủ tầng sương trắng mỏng.

"Đoán Cốt Thập Nhị Thức — Thức thứ bảy: Ngọc Tủy Quy Nhất, chuyển!"

Tôi gầm lên một tiếng trầm đục trong lồng ngực. Từng đốt xương sống tôi phát ra tiếng nổ giòn tan như sấm sét. Dòng tủy ngọc trong suốt lập tức trỗi dậy cuộn trào, nghênh đón luồng kiếm khí hàn băng mãnh liệt. Hai luồng năng lượng bản nguyên va chạm dữ dội, rồi nhanh chóng quấn quýt lấy nhau, dung hòa từng tấc một.

Trong khoảnh khắc kiếm khí và tủy ngọc hợp nhất, một luồng xung cảm tâm linh vô cùng kỳ vĩ bỗng tràn ngập tâm trí tôi.

Trước mắt tôi không còn là đáy rạch Bến Nghé tăm tối, mà là một khung cảnh viễn cổ hoang sơ ngập tràn ánh sáng hỗn mang. Tôi nhìn thấy giữa đất trời bao la vô tận, chín cây trụ đá khổng lồ chống đỡ vòm trời, và vô số bậc đại năng thời thái cổ đang dốc cạn sinh lực để phong ấn một cự ma thái cổ dưới vực sâu thăm thẳm. Thanh Long Lân Kiếm khi ấy chính là một trong những thanh kiếm then chốt cắm trên đại trận Cửu Châu Phong Thiên!

Khí tức viễn cổ này làm linh hồn tôi rung động sâu sắc. Tủy ngọc trong xương dường như được thanh tẩy thêm một tầng tinh khiết mới, trở nên trong vắt và vững chãi.

"Rút!"

Tôi nắm chặt chuôi kiếm, cánh tay phải gân guốc phát lực nhấc bổng lên!

"Keng — uông!"

Một tiếng kiếm ngân vang dội thấu đáy sông. Thanh Long Lân Kiếm rời khỏi nanh đá bazan ngàn năm, hóa thành một đạo thanh quang xanh biếc thu nhỏ lại, thuận theo lòng bàn tay tôi chui vào trong cơ thể, an tọa ngay ngắn bên cạnh cột sống tủy ngọc!

Ngay khi thanh kiếm được thu phục, lòng rạch Bến Nghé bỗng chốc trở nên êm ả lạ kỳ. Vòng xoáy ám triều tan biến hoàn toàn, mạch đất ngầm được an định vững chắc. Dưới đáy hốc đá nơi cọc tiêu vừa được rút lên, một chiếc hộp bằng đồng thau nhỏ phủ kín hoa văn mai rùa cổ xưa lộ ra.

Tôi cúi xuống nhặt chiếc hộp đồng cất vào túi bảo hộ ngực áo, rồi đạp chân vịt bơi ngược lên mặt nước.

Hai giờ sáng.

Mặt nước rạch Bến Nghé rẽ sóng, tôi trồi lên sát mạn xà lan của Viện Địa tầng. Kỹ sư Tuấn và hai chiến sĩ tuần tra đường thủy vội vàng đỡ tôi lên sàn tàu.

"Thế nào rồi Minh An? Các chỉ số vi chấn trên màn hình vừa đột ngột trở về trạng thái phẳng lặng tuyệt đối!" Tuấn thở phào nhẹ nhõm, ánh mắt tràn đầy thán phục.

Tôi tháo kính lặn, mỉm cười đón lấy chiếc khăn bông ấm từ tay Tuấn: "Toàn bộ thiết bị cộng hưởng ngầm đã bị vô hiệu hóa. Móng Cầu Mống đã an toàn tuyệt đối cho buổi thử tải ngày mai."

Nói đoạn, tôi mở chiếc hộp đồng vừa nhặt được dưới đáy sâu. Bên trong là một tấm da rùa cổ khắc họa đồ thủy đạo Sài Gòn xưa. Trên tấm da rùa, một điểm sáng màu đỏ son được đánh dấu rất rõ tại vị trí ụ tàu cổ và thủy đài ngầm của xưởng đóng tàu Ba Son — nơi cọc tiêu số sáu mang tên **Thủy Môn Chấn Tiêu** đang ẩn mình chờ đợi.'''

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
        "Lặn Sâu Rạch Bến Nghé & Thu Phục Thanh Long Lân Kiếm",
        CHAPTER_NUM,
        1,
        f"{DATE}T02:00:00+07:00",
        CHAPTER_NUM,
        "loc_cau_mong",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan"]),
        "Minh An lặn sâu xuống lòng rạch Bến Nghé, đối đầu toán sát thủ người nhái Hắc Giao Đường thuộc Cửu Long Thiên Hải. Vô hiệu hóa 4 trục neo phát sóng cộng hưởng siêu âm phá mạch đá móng Cầu Mống. Tiếp cận đàn tế đá Đông Sơn cổ sâu 38m, dùng tinh huyết và kình lực Thể Đạo dung nạp bảo kiếm Thanh Long Lân Kiếm (cọc số 5). Phát hiện hộp đồng chứa hải đồ cổ dẫn tới cọc số 6 Thủy Môn Chấn Tiêu tại xưởng Ba Son.",
        "Móng Cầu Mống an định tuyệt đối; vô hiệu hóa toàn bộ trận bàn phá hoại ngầm; thu phục thành công cọc tiêu số 5 Thanh Long Lân Kiếm; thu thập manh mối cọc tiêu số 6 Ba Son."
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
        "Minh An thu phục thành công cọc tiêu số 5 Thanh Long Lân Kiếm tại Cầu Mống; tìm thấy hải đồ chỉ tới cọc số 6 Thủy Môn Chấn Tiêu tại xưởng Ba Son."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Đàn tế đá Đông Sơn cổ dưới đáy rạch Bến Nghé được chứng thực; hoa văn mặt trời và chim lạc trên chuôi kiếm Thanh Long liên kết với đại trận Cửu Châu Phong Thiên thượng cổ."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 7. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T02:30:00+07:00"
        inv_data["current_location"] = "Ngã ba Rạch Bến Nghé — Cầu Mống (TP.HCM)"
        
        # Thêm Thanh Long Lân Kiếm vào core_weapons_and_artifacts nếu chưa có
        item_names = [it.get("name") for it in inv_data.get("core_weapons_and_artifacts", [])]
        if "Thanh Long Lân Kiếm (Trận Nhãn Thủy Môn Tiêu số 5)" not in item_names:
            inv_data["core_weapons_and_artifacts"].append({
                "name": "Thanh Long Lân Kiếm (Trận Nhãn Thủy Môn Tiêu số 5)",
                "type": "Cổ kiếm trận nhãn / Cổ khí trấn thủy",
                "location": "Dung nạp trong khí hải tủy ngọc dọc cột sống",
                "condition": "Nguyên vẹn 100%, ngọc phỉ thúy vảy rồng xanh biếc, kiếm khí hàn băng",
                "durability": "100/100",
                "function": "Trận nhãn cọc tiêu Thanh Long Tả Tiêu (Cầu Mống); trấn áp thủy sát lưu vực Bến Nghé, phụ trợ kình lực Thể Đạo tôi luyện tủy ngọc và phát xuất hàn băng kiếm khí"
            })
            # Thêm hộp đồng cổ
            inv_data["core_weapons_and_artifacts"].append({
                "name": "Hộp Đồng Cổ Vân Mai Rùa (Chứa Hải Đồ Ba Son)",
                "type": "Vật phẩm cốt truyện / Di vật Đông Sơn",
                "location": "Túi bảo hộ ngực áo dã chiến",
                "condition": "Nguyên vẹn",
                "durability": "100/100",
                "function": "Chứa hải đồ da rùa chỉ dẫn vị trí cọc tiêu số 6 Thủy Môn Chấn Tiêu tại xưởng Ba Son"
            })

        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (thêm Thanh Long Lân Kiếm & Hộp Đồng Cổ).")

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

# -*- coding: utf-8 -*-
"""
NovelOS — Modul Quản Lý & Xuất Bản Các Trang SEO & Lore Vệ Tinh Cho Phá Trời
Bao gồm:
1. /phat-troi-la-truyen-gi/ (Cẩm nang toàn diện bộ truyện)
2. /truyen-tu-tien-viet-nam-sai-gon/ (Bài phân tích chuyên sâu tu tiên bản địa)
3. /do-thi-tu-chan-la-gi/ (Giải mã thể loại đô thị tu chân)
4. /the-dao/ (Hồ sơ Lore: Thể Đạo phàm nhân)
5. /nguyen-minh-an/ (Hồ sơ Lore: Nhân vật Nguyễn Minh An)
"""

import json
from datetime import datetime

SEO_PAGES = [
    {
        "slug": "phat-troi-la-truyen-gi",
        "title": "Phá Trời Là Truyện Gì? Cẩm Nang Toàn Diện Về Tiểu Thuyết Đô Thị Tu Chân Sài Gòn 2026",
        "meta_title": "Phá Trời Là Truyện Gì? Cẩm Nang Đô Thị Tu Chân | phatroi.com",
        "meta_desc": "Tìm hiểu về Phá Trời: tiểu thuyết đô thị tu chân TP.HCM 2026 của tác giả An Bình. Bối cảnh Sài Gòn, nhân vật Minh An, Lâm Tịch và Thể Đạo phàm nhân.",
        "keywords": "Phá Trời là truyện gì, tiểu thuyết Phá Trời, Phá Toái Thần Hoang, đô thị tu chân Sài Gòn, Nguyễn Minh An, Lâm Tịch, Thể Đạo, tác giả An Bình, truyện tiên hiệp Việt Nam",
        "category": "CẨM NANG TÁC PHẨM",
        "read_mins": 7,
        "date": "2026-10-01",
        "content_html": """
<p class="lead-p">
  <strong>Phá Trời</strong> (tên đầy đủ: <em>Phá Toái Thần Hoang</em>) là bộ trường thiên tiểu thuyết đô thị tu chân hiện đại của tác giả <strong>An Bình</strong>, lấy bối cảnh chính xác tại <strong>Thành phố Hồ Chí Minh năm 2026</strong>. Tác phẩm kể về hành trình của <strong>Nguyễn Minh An</strong> — một nhân viên văn phòng 25 tuổi bình thường — vô tình bước vào thế giới tu chân khi phong ấn đại địa cổ xưa ngủ vùi 2,5 triệu năm dưới lòng sông Sài Gòn bắt đầu thức giấc.
</p>

<h2>1. Thông Tin Tổng Quan Tác Phẩm</h2>
<div class="info-table-box">
  <table class="data-table">
    <tbody>
      <tr><td><strong>Tên tác phẩm:</strong></td><td>Phá Trời (Phá Toái Thần Hoang)</td></tr>
      <tr><td><strong>Tác giả:</strong></td><td>An Bình</td></tr>
      <tr><td><strong>Thể loại:</strong></td><td>Đô thị tu chân, Huyền huyễn hiện đại, Thể thuật, Triết luận</td></tr>
      <tr><td><strong>Bối cảnh chính:</strong></td><td>TP. Hồ Chí Minh (Sài Gòn), Việt Nam — Năm 2026</td></tr>
      <tr><td><strong>Quy mô hiện tại:</strong></td><td>78+ chương (~226.500+ từ), đang phát hành liên tục</td></tr>
      <tr><td><strong>Nền tảng đọc chính thức:</strong></td><td><a href="https://phatroi.com/">phatroi.com</a> (Đọc miễn phí, hỗ trợ PWA offline 24/7)</td></tr>
    </tbody>
  </table>
</div>

<h2>2. Bối Cảnh Độc Nhất: Khi Sài Gòn Trở Thành Tâm Điểm Của Cổ Giới</h2>
<p>
  Khác biệt hoàn toàn với các tác phẩm tiên hiệp Trung Quốc mượn bối cảnh cổ trang xa lạ, <em>Phá Trời</em> đặt từng bước chân nhân vật ngay trên các địa danh quen thuộc của Sài Gòn đời thực:
</p>
<ul>
  <li><strong>Ngã tư Hàng Xanh & Đường Ung Văn Khiêm (Bình Thạnh):</strong> Nơi bắt đầu câu chuyện với những cơn mưa rào tháng 10 đặc trưng, căn phòng trọ mái tôn ngột ngạt và tiếng còi xe máy giờ tan tầm.</li>
  <li><strong>Lòng sông Sài Gòn & Bán đảo Thanh Đa:</strong> Dưới lớp phù sa ngầm hàng trăm mét không chỉ là địa tầng địa chất thông thường, mà là một trận pháp phong ấn đại địa đã tồn tại hơn 2,5 triệu năm trước khi nhân loại hiện đại hình thành.</li>
  <li><strong>Bến Bạch Đằng, Cầu Ba Son & Hầm Thủ Thiêm:</strong> Những công trình biểu tượng của thế kỷ 21 trở thành ranh giới giao thoa mong manh giữa nhịp sống đô thị nhộn nhịp và các dòng chảy linh mạch cổ đang rạn nứt.</li>
  <li><strong>Khu phố cổ Quận 5 & Kênh Tàu Hủ:</strong> Những võ đường cổ truyền, tiệm thuốc bắc hàng trăm năm tuổi ẩn chứa các manh mối về những người tu đạo phàm trần đã âm thầm bảo vệ mảnh đất này qua nhiều thế kỷ.</li>
</ul>

<h2>3. Nhân Vật Chính Nguyễn Minh An: Phàm Nhân Không Hệ Thống</h2>
<p>
  Nhân vật chính <strong>Nguyễn Minh An</strong> được xây dựng hoàn toàn đối lập với hình mẫu nhân vật "tiên hiệp mì ăn liền":
</p>
<blockquote>
  “Hắn không có linh căn thượng phẩm, không có hệ thống điểm số nhảy số trước mắt, và càng không phải là đại năng chuyển thế mang theo ký ức bá đạo. Hắn chỉ là một người phàm 25 tuổi, ban ngày chen chúc trên chiếc xe máy cũ qua cầu Sài Gòn để kịp giờ chấm công, ban đêm đối diện với những cơn đau xé rách xương tủy khi huyết mạch thức giấc.”
</blockquote>
<p>
  Minh An đại diện cho ý chí quật cường của một con người bình dị. Khi bị cuốn vào cơn lốc giữa các thế lực siêu nhiên cổ xưa và nguy cơ đại địa sụp đổ, vũ khí duy nhất hắn sở hữu là ý chí sắt đá và <strong>Thể Đạo</strong> — con đường tu luyện nhục thân thuần túy.
</p>

<h2>4. Thể Đạo: Con Đường Tu Luyện Đột Phá Mạt Pháp</h2>
<p>
  Trong thế giới của <em>Phá Trời</em>, Trái Đất là vùng đất mạt pháp — nơi linh khí trời đất đã cạn kiệt suốt hàng triệu năm. Các pháp môn tu luyện linh căn truyền thống đều trở nên vô dụng. Để sinh tồn và chiến đấu, Minh An phải dấn thân vào <strong>Thể Đạo</strong>:
</p>
<ul>
  <li><strong>Lấy Thể Vi Bản:</strong> Không cầu xin linh khí bên ngoài, mà khai mở tiềm năng vô tận ẩn sâu trong từng tế bào, gân cốt và huyết dịch của chính cơ thể người.</li>
  <li><strong>Cái giá của sức mạnh:</strong> Mỗi bước đột phá Thể Đạo đòi hỏi người tu luyện phải tôi luyện nhục thân qua đau đớn cùng cực, rèn luyện ý chí trước sự ma sát khốc liệt của khí huyết.</li>
  <li><strong>Kháng Linh Tự Nhiên:</strong> Khi đạt đến cảnh giới nhất định, nhục thân Thể Đạo có khả năng miễn nhiễm và xé rách các đòn tấn công pháp thuật, biến người tu thành một cỗ chiến xa bất bại ở cự ly cận chiến.</li>
</ul>

<h2>5. Bí Ẩn Lâm Tịch: Linh Hồn Cổ Triệu Năm Trong Thức Hải</h2>
<p>
  Đồng hành cùng Minh An trong hành trình là <strong>Lâm Tịch</strong> — một thực thể thần bí thức tỉnh bên trong thức hải của hắn. Nàng không phải là một "cụ già trong nhẫn" toàn năng ban phát bảo vật, mà là một mảnh tàn hồn mang theo ký ức bi tráng về cuộc đại chiến viễn cổ và phong ấn Trái Đất.
</p>
<p>
  Mối quan hệ giữa Minh An và Lâm Tịch phát triển theo nhịp điệu chậm rãi, sâu sắc (Slow Burn), dựa trên sự thấu hiểu, tôn trọng và cùng nhau tìm kiếm sự thật về nguồn gốc vũ trụ.
</p>

<h2>6. Hướng Dẫn Đọc & Theo Dõi Tác Phẩm</h2>
<p>
  Hiện tại, <em>Phá Trời</em> đã xuất bản trọn vẹn <strong>78 chương</strong> đầu tiên (tương đương Quyển I và nửa đầu Quyển II). Tác phẩm được phát hành miễn phí và chính thức tại website:
</p>
<div class="cta-box">
  <h3>Bắt Đầu Đọc Phá Trời Ngay Hôm Nay</h3>
  <p>Trải nghiệm giao diện đọc tinh tế, không quảng cáo, tối ưu cho điện thoại và máy tính.</p>
  <div class="cta-actions">
    <a href="/chuong-1/" class="btn-cta-primary">Đọc Từ Chương 1 →</a>
    <a href="/the-dao/" class="btn-cta-secondary">Tìm Hiểu Thể Đạo</a>
  </div>
</div>
"""
    },
    {
        "slug": "truyen-tu-tien-viet-nam-sai-gon",
        "title": "Truyện Tu Tiên Việt Nam Lấy Bối Cảnh Sài Gòn: Khi Huyền Huyễn Giao Thoa Đời Thực",
        "meta_title": "Truyện Tu Tiên Việt Nam Sài Gòn: Phá Trời | phatroi.com",
        "meta_desc": "Khám phá làn sóng truyện tu tiên Việt Nam hiện đại. Phân tích sự độc đáo của Phá Trời khi đưa ngã tư Hàng Xanh, sông Sài Gòn vào tiểu thuyết huyền ảo.",
        "keywords": "truyện tu tiên Việt Nam, tu tiên Sài Gòn, đô thị tu chân Việt Nam, tiểu thuyết huyền huyễn TP.HCM, truyện tiên hiệp Việt Nam hiện đại, Phá Trời Sài Gòn",
        "category": "PHÂN TÍCH VĂN HỌC",
        "read_mins": 6,
        "date": "2026-10-05",
        "content_html": """
<p class="lead-p">
  Trong suốt hơn hai thập kỷ qua, độc giả yêu thích thể loại tiên hiệp, huyền huyễn tại Việt Nam chủ yếu tiếp cận các tác phẩm dịch hoặc phóng tác từ văn học mạng Trung Quốc. Những bối cảnh quen thuộc như núi Côn Lôn, sông Hoàng Hà hay các tông môn cổ trang đã trở thành lối mòn. Sự xuất hiện của <strong>Phá Trời</strong> — bộ tiểu thuyết đô thị tu chân lấy bối cảnh trực tiếp tại <strong>TP. Hồ Chí Minh năm 2026</strong> — đang đánh dấu một bước chuyển mình mạnh mẽ cho dòng văn học huyền ảo bản địa.
</p>

<h2>1. Nỗi Khát Khao Một Thế Giới Tu Tiên "Rất Việt Nam"</h2>
<p>
  Người đọc Việt Nam luôn mong muốn tìm thấy những câu chuyện mà nhân vật sống trong không gian gần gũi với mình: uống cà phê cóc ven đường, chạy xe máy dưới cơn mưa ngập đường Ung Văn Khiêm, ngắm nhìn sông Sài Gòn lấp lánh ánh đèn đêm từ cầu Ba Son.
</p>
<p>
  Khi những địa danh thân thuộc đó không chỉ là phông nền đời thường mà ẩn giấu những bí mật kinh thiên động địa — một đại địa phong ấn 2,5 triệu năm, những dòng linh mạch ngầm cổ xưa, những võ đường bí truyền giữa lòng Chợ Lớn — cảm giác ngỡ ngàng và thích thú của người đọc tăng lên gấp bội.
</p>

<h2>2. Sài Gòn: Vùng Đất Hoàn Hảo Cho Đô Thị Huyền Ảo</h2>
<p>
  Tại sao tác giả An Bình lại chọn Sài Gòn mà không phải một thành phố nào khác?
</p>
<ul>
  <li><strong>Sự Tương Phản Gay Gắt:</strong> Sài Gòn là nơi giao thoa mãnh liệt giữa hiện đại và truyền thống, giữa những tòa nhà chọc trời kính sáng loáng ở Quận 1 và những con hẻm ngoằn ngoèo rêu phong ở Quận 5. Đây là mảnh đất màu mỡ để gieo mầm ý tưởng: một thế giới tu chân cổ xưa đang âm thầm vận hành song song dưới chân những cư dân hiện đại bận rộn.</li>
  <li><strong>Hệ Thống Sông Ngòi Chằng Chịt:</strong> Sông Sài Gòn, kênh Nhiêu Lộc - Thị Nghè, kênh Tàu Hủ, bán đảo Thanh Đa... tạo nên mạng lưới thủy mạch tự nhiên kỳ vĩ. Trong <em>Phá Trời</em>, mạng lưới thủy văn này chính là sơ đồ phong ấn vĩ đại được tiền nhân thiết lập từ thời hồng hoang.</li>
  <li><strong>Nhịp Sống Đô Thị Thật:</strong> Nhân vật trong truyện không phải là những kẻ xa rời thực tế. Họ phải trả tiền trọ, lo lắng công việc văn phòng, đối mặt với áp lực mưu sinh trước khi gánh vác sứ mệnh cứu vãn càn khôn.</li>
</ul>

<h2>3. Vượt Qua Định Kiến "Truyện Tu Tiên Việt Nam Kém Sức Hút"</h2>
<p>
  Nhiều độc giả từng có định kiến rằng tiểu thuyết kỳ ảo do người Việt viết thường thiếu tính logic hoặc sao chép rập khuôn. <em>Phá Trời</em> đã chứng minh điều ngược lại thông qua:
</p>
<blockquote>
  “Một hệ thống thế giới quan khép kín, logic tu luyện nhất quán (Thể Đạo dựa trên khí huyết và sinh học cơ thể), văn phong tiếng Việt trau chuốt, giàu sức gợi hình và không lạm dụng từ Hán Việt thừa thãi.”
</blockquote>

<h2>4. Lời Kết</h2>
<p>
  <em>Phá Trời</em> không chỉ là một cuốn tiểu thuyết giải trí, mà còn là nỗ lực khẳng định rằng: tác giả Việt Nam hoàn toàn có thể xây dựng những vũ trụ kỳ ảo đồ sộ, hấp dẫn và đậm đà bản sắc riêng.
</p>
<div class="cta-box">
  <h3>Khám Phá Sài Gòn Huyền Ảo Cùng Phá Trời</h3>
  <p>Hãy bước chân vào Chương 1 để cảm nhận một Sài Gòn hoàn toàn khác biệt dưới ngòi bút của tác giả An Bình.</p>
  <div class="cta-actions">
    <a href="/chuong-1/" class="btn-cta-primary">Đọc Ngay Chương 1 →</a>
    <a href="/nguyen-minh-an/" class="btn-cta-secondary">Xem Hồ Sơ Minh An</a>
  </div>
</div>
"""
    },
    {
        "slug": "do-thi-tu-chan-la-gi",
        "title": "Truyện Đô Thị Tu Chân Là Gì? Giải Mã Sức Hút Của Thể Loại Tu Tiên Hiện Đại",
        "meta_title": "Đô Thị Tu Chân Là Gì? Cẩm Nang Tu Tiên | phatroi.com",
        "meta_desc": "Đô thị tu chân là gì? Tìm hiểu nguồn gốc, đặc điểm và sự cách tân của thể loại tu tiên hiện đại qua tiểu thuyết đô thị tu chân Phá Trời — TP.HCM 2026.",
        "keywords": "đô thị tu chân là gì, truyện đô thị tu tiên, urban cultivation, thể loại đô thị tu chân, tu tiên hiện đại, đặc điểm đô thị tu chân, Phá Trời",
        "category": "KIẾN THỨC THỂ LOẠI",
        "read_mins": 5,
        "date": "2026-10-10",
        "content_html": """
<p class="lead-p">
  <strong>Đô thị tu chân</strong> (tiếng Anh: <em>Urban Cultivation</em> hay <em>Modern Xianxia</em>) là một phân nhánh đặc sắc của văn học mạng phương Đông, kết hợp giữa yếu tố <strong>tu tiên, luyện khí, trường sinh</strong> cổ điển với <strong>bối cảnh xã hội hiện đại</strong> (thành phố, công nghệ, đời sống đương đại).
</p>

<h2>1. Nguồn Gốc & Sự Phát Triển Của Đô Thị Tu Chân</h2>
<p>
  Ban đầu, các tiểu thuyết tu tiên kinh điển (như <em>Phàm Nhân Tu Tiên</em>, <em>Tiên Nghịch</em>) chủ yếu đặt bối cảnh trong các đại lục giả tưởng thời cổ đại. Tuy nhiên, sự tò mò của độc giả ngày càng lớn: <em>"Điều gì sẽ xảy ra nếu một người có khả năng phi thiên độn địa sống giữa một thành phố hiện đại với súng đạn, internet và cao ốc?"</em>
</p>
<p>
  Từ câu hỏi đó, thể loại đô thị tu chân ra đời và nhanh chóng chiếm lĩnh thị trường văn học mạng suốt một thập kỷ qua.
</p>

<h2>2. Những Mô-Típ Quen Thuộc & Điểm Bão Hòa Của Thể Loại</h2>
<p>
  Trong giai đoạn phát triển ban đầu, dòng truyện này thường mắc phải các công thức rập khuôn:
</p>
<ul>
  <li><strong>Mô-típ "Trọng sinh vả mặt":</strong> Tiên đế chuyển sinh vào người bình thường, liên tục bị khinh thường rồi dùng sức mạnh đè bẹp đối thủ một cách vô lý.</li>
  <li><strong>Hệ thống hack điểm (System):</strong> Nhân vật không cần nỗ lực, chỉ cần hoàn thành nhiệm vụ của bảng giao diện là tăng cấp vù vù.</li>
  <li><strong>Phá vỡ cân bằng hiện thực:</strong> Tác giả thường bỏ qua các quy luật vật lý, luật pháp xã hội và đạo đức cơ bản, khiến câu chuyện mất đi tính thuyết phục.</li>
</ul>

<h2>3. Cuộc Cách Tân Trong "Phá Trời": Đô Thị Tu Chân Hiện Thực & Triết Luận</h2>
<p>
  Nhận thức rõ sự bão hòa của các mô-típ cũ, <strong>Phá Trời</strong> đã lựa chọn một hướng đi hoàn toàn mới:
</p>
<ol>
  <li><strong>Nói KHÔNG với hệ thống hack:</strong> Nguyễn Minh An phải tự mình nỗ lực qua từng giọt mồ hôi và máu để khai phá Thể Đạo. Không có phần thưởng miễn phí từ trên trời rơi xuống.</li>
  <li><strong>Bảo tồn tính chân thực của đô thị:</strong> Xã hội TP.HCM 2026 được miêu tả chân thực, sống động với đầy đủ các mối quan hệ xã hội, gia đình, công việc văn phòng và những trăn trở của người trẻ.</li>
  <li><strong>Hệ thống sức mạnh có cái giá rõ ràng:</strong> Sức mạnh không đến từ việc hít thở không khí mà đòi hỏi sự tiêu hao sinh mệnh, ma sát khí huyết và sự giác ngộ về bản ngã.</li>
</ol>

<h2>4. Kết Luận</h2>
<p>
  Đô thị tu chân đang bước vào kỷ nguyên mới — nơi những câu chuyện có chiều sâu, tính nhân văn và bối cảnh bản địa thực thụ lên ngôi. <em>Phá Trời</em> chính là minh chứng rõ nét cho sự trưởng thành vượt bậc này.
</p>
<div class="cta-box">
  <h3>Trải Nghiệm Thể Loại Đô Thị Tu Chân Mới Nhất</h3>
  <p>Đọc ngay 78 chương tiểu thuyết Phá Trời hoàn toàn miễn phí tại phatroi.com.</p>
  <div class="cta-actions">
    <a href="/chuong-1/" class="btn-cta-primary">Bắt Đầu Chương 1 →</a>
    <a href="/phat-troi-la-truyen-gi/" class="btn-cta-secondary">Tổng Quan Bộ Truyện</a>
  </div>
</div>
"""
    },
    {
        "slug": "the-dao",
        "title": "Thể Đạo Trong Phá Trời: Con Đường Tu Luyện Nhục Thân Của Phàm Nhân",
        "meta_title": "Thể Đạo Trong Phá Trời: Tu Luyện Nhục Thân | phatroi.com",
        "meta_desc": "Giải mã Thể Đạo trong Phá Trời: con đường tu luyện nhục thân và khí huyết phàm nhân không cần linh căn giữa thời mạt pháp tại TP.HCM 2026. Tác giả An Bình.",
        "keywords": "Thể Đạo Phá Trời, tu luyện nhục thân, Thể Đạo là gì, khí huyết đạo, Nguyễn Minh An Thể Đạo, mạt pháp tu chân, hệ thống tu luyện Phá Trời",
        "category": "HỒ SƠ LORE & HỆ THỐNG",
        "read_mins": 5,
        "date": "2026-10-02",
        "content_html": """
<p class="lead-p">
  Trong vũ trụ <strong>Phá Trời</strong>, <strong>Thể Đạo</strong> không đơn thuần là các bài tập thể lực hay rèn luyện cơ bắp thông thường. Đây là một đại đạo tu hành cổ xưa độc lập, lấy bản thân cơ thể phàm nhân làm lò luyện, lấy khí huyết làm củi lửa để đốt cháy và phá vỡ các gông cùm gien di truyền của nhân loại.
</p>

<h2>1. Tại Sao Lại Là Thể Đạo?</h2>
<p>
  Trái Đất bước vào kỷ nguyên mạt pháp từ hàng triệu năm trước. Nồng độ linh khí tự nhiên trong khí quyển gần như bằng không. Những ai cố gắng tu luyện theo con đường truyền thống (Linh Căn - Tụ Khí - Trúc Cơ) đều phải chuốc lấy thất bại vì không có nguồn linh năng để hấp thụ.
</p>
<p>
  Trong nghịch cảnh đó, <strong>Thể Đạo</strong> là con đường khả thi duy nhất:
</p>
<blockquote>
  “Trời đất không cho linh khí, thì phàm nhân tự tìm kiếm sức mạnh trong chính 60 ngàn tỷ tế bào của mình. Cơ thể con người chính là vũ trụ thu nhỏ hoàn hảo nhất.”
</blockquote>

<h2>2. Các Giai Đoạn Tiến Hóa Của Thể Đạo</h2>
<ul>
  <li><strong>Giai đoạn 1 — Khí Huyết Lạc Mạch:</strong> Đánh thức dòng chảy khí huyết ngủ sâu trong các mao mạch phụ, gia tăng mật độ xương và sức bền cơ bắp lên gấp 5–10 lần người bình thường.</li>
  <li><strong>Giai đoạn 2 — Cốt Tủy Lôi Âm:</strong> Tiếng gầm của tủy xương như sấm rền khi vận chuyển huyết dịch, đào thải toàn bộ tạp chất tế bào, hình thành lớp màng bảo vệ vô hình trên bề mặt da.</li>
  <li><strong>Giai đoạn 3 — Thể Hồn Hợp Nhất:</strong> Nhục thân đạt đến độ thuần khiết tuyệt đối, có khả năng khóa chặt sinh cơ và kháng lại các đòn xâm thực tinh thần từ thức hải.</li>
</ul>

<h2>3. Mối Quan Hệ Với Phong Ấn Sài Gòn</h2>
<p>
  Theo những phát hiện của Minh An tính đến Chương 78, đại phong ấn dưới đáy sông Sài Gòn được xây dựng bằng cùng một loại quy tắc với Thể Đạo cổ xưa. Điều này lý giải vì sao cơ thể hắn có thể cộng hưởng và mở khóa phong ấn mà không bị cắn trả tử vong.
</p>

<div class="cta-box">
  <h3>Theo Chân Minh An Khám Phá Thể Đạo</h3>
  <p>Chứng kiến từng bước rèn luyện nhục thân đầy gian khổ nhưng phi thường trong Phá Trời.</p>
  <div class="cta-actions">
    <a href="/chuong-1/" class="btn-cta-primary">Đọc Từ Chương 1 →</a>
    <a href="/nguyen-minh-an/" class="btn-cta-secondary">Hồ Sơ Minh An</a>
  </div>
</div>
"""
    },
    {
        "slug": "nguyen-minh-an",
        "title": "Hồ Sơ Nguyễn Minh An: Nhân Viên Văn Phòng 25 Tuổi Và Đại Địa Phong Ấn Sài Gòn",
        "meta_title": "Hồ Sơ Nguyễn Minh An — Phàm Nhân Thể Đạo | phatroi.com",
        "meta_desc": "Hồ sơ chi tiết về Nguyễn Minh An: 25 tuổi, nhân viên văn phòng tại TP.HCM, người thức tỉnh Thể Đạo phàm nhân dưới phong ấn 2,5 triệu năm của sông Sài Gòn.",
        "keywords": "Nguyễn Minh An, nhân vật Minh An Phá Trời, hồ sơ Nguyễn Minh An, nhân vật chính Phá Trời, tiểu sử Minh An, Thể Đạo Minh An",
        "category": "HỒ SƠ NHÂN VẬT",
        "read_mins": 5,
        "date": "2026-10-03",
        "content_html": """
<p class="lead-p">
  <strong>Nguyễn Minh An</strong> là nhân vật chính của trường thiên tiểu thuyết đô thị tu chân <strong>Phá Trời</strong>. Một thanh niên 25 tuổi mang đầy đủ những nét đặc trưng của thế hệ trẻ Sài Gòn hiện đại: kiên trì, thực tế, sống có trách nhiệm nhưng ẩn chứa bên trong là một ý chí bất khuất trước nghịch cảnh.
</p>

<h2>1. Thông Tin Cơ Bản</h2>
<div class="info-table-box">
  <table class="data-table">
    <tbody>
      <tr><td><strong>Họ và tên:</strong></td><td>Nguyễn Minh An</td></tr>
      <tr><td><strong>Tuổi:</strong></td><td>25 tuổi (Sinh năm 2001, mốc truyện 2026)</td></tr>
      <tr><td><strong>Nơi cư trú:</strong></td><td>Phòng trọ đường Ung Văn Khiêm, P. 25, Q. Bình Thạnh, TP.HCM</td></tr>
      <tr><td><strong>Nghề nghiệp:</strong></td><td>Nhân viên văn phòng / Thiết kế dữ liệu</td></tr>
      <tr><td><strong>Đạo đồ tu luyện:</strong></td><td>Thể Đạo (Không linh căn, không pháp môn)</td></tr>
      <tr><td><strong>Tình trạng hiện tại:</strong></td><td>Đã kích hoạt Khí Huyết Lạc Mạch, cộng sinh cùng tàn hồn Lâm Tịch</td></tr>
    </tbody>
  </table>
</div>

<h2>2. Tính Cách & Triết Lý Sống</h2>
<p>
  Minh An không phải là kẻ háo danh hay khao khát quyền lực thống trị. Mục tiêu ban đầu của hắn rất đỗi bình thường: kiếm đủ tiền trang trải cuộc sống, chăm lo cho người thân và có một chỗ đứng yên bình tại thành phố này.
</p>
<p>
  Tuy nhiên, khi biến cố ập đến và phát hiện bản thân là mắt xích quan trọng nhất của đại phong ấn sông Sài Gòn, hắn không hề trốn chạy. Thái độ đối mặt với khó khăn của Minh An mang đậm tính cách người miền Nam: điềm tĩnh, dám làm dám chịu và kiên cường tới cùng.
</p>

<h2>3. Bước Ngoặt Định Mệnh</h2>
<p>
  Cơn mưa rào đêm tháng 10 năm 2026 tại ngã tư Hàng Xanh đã thay đổi hoàn toàn cuộc đời Minh An. Hiện tượng địa chấn ngầm kích hoạt dòng ký ức viễn cổ ngủ sâu trong gien di truyền, mở ra cánh cổng thức hải và đánh thức Lâm Tịch — người đã ngủ vùi 2,5 triệu năm.
</p>

<div class="cta-box">
  <h3>Đồng Hành Cùng Minh An Từ Bước Chân Đầu Tiên</h3>
  <p>Đón đọc hành trình đầy kịch tính của Nguyễn Minh An tại phatroi.com.</p>
  <div class="cta-actions">
    <a href="/chuong-1/" class="btn-cta-primary">Đọc Chương 1 Ngay →</a>
    <a href="/phat-troi-la-truyen-gi/" class="btn-cta-secondary">Về Trang Chủ Phá Trời</a>
  </div>
</div>
"""
    }
]

def render_seo_page_html(article, shared_css, site_url, ga_measurement_id, total_chapters):
    slug = article["slug"]
    title = article["title"]
    meta_title = article["meta_title"]
    meta_desc = article["meta_desc"]
    keywords = article["keywords"]
    category = article["category"]
    read_mins = article["read_mins"]
    date_str = article["date"]
    content_html = article["content_html"]
    canonical_url = f"{site_url}/{slug}/"
    
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="google-site-verification" content="495lr0EokjP3LLADeovb1t_ecOikpcbgyO_mW9m8e00">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <title>{meta_title}</title>
  
  <meta name="title" content="{meta_title}">
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="An Bình">
  
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{site_url}/assets/hero_horizontal.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{meta_title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{site_url}/assets/hero_horizontal.jpg">

  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/assets/logo.webp" type="image/webp">
  <link rel="apple-touch-icon" href="/assets/logo.webp">
  <meta name="theme-color" content="#07090e">

  <!-- Anti-FOUC Early Theme Execution -->
  <script>
    (function() {{
      try {{
        var t = localStorage.getItem('pha_troi_theme') || 'theme-peaceful-dark';
        document.documentElement.className = t;
      }} catch(e) {{}}
    }})();
  </script>

  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga_measurement_id}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga_measurement_id}', {{
      page_title: '{title}',
      page_path: '/{slug}/'
    }});
  </script>

  <!-- Structured Data JSON-LD (Article & Breadcrumb) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Trang Chủ",
            "item": "{site_url}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{title}",
            "item": "{canonical_url}"
          }}
        ]
      }},
      {{
        "@type": "Article",
        "headline": "{title}",
        "description": "{meta_desc}",
        "url": "{canonical_url}",
        "inLanguage": "vi",
        "datePublished": "{date_str}",
        "dateModified": "{date_str}",
        "author": {{
          "@type": "Person",
          "name": "An Bình",
          "url": "{site_url}/"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "Phá Trời",
          "logo": {{
            "@type": "ImageObject",
            "url": "{site_url}/assets/logo.webp"
          }}
        }},
        "mainEntityOfPage": {{
          "@type": "WebPage",
          "@id": "{canonical_url}"
        }}
      }}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/assets/seo.css">
</head>
<body class="theme-peaceful-dark is-seo-page">

  <div id="progressBarContainer"><div id="progressBar"></div></div>

  <!-- HEADER -->
  <header id="topHeader">
    <div class="header-left">
      <a href="/" class="btn-brand" title="Trở về Trang Chủ Phá Trời">
        <picture>
          <source srcset="/assets/logo.webp" type="image/webp">
          <img src="/assets/logo.jpg" class="nav-logo" alt="Phá Trời">
        </picture>
        <span class="nav-brand-text">PHÁ TRỜI</span>
        <span class="nav-live-badge"><span class="dot-live"></span> {total_chapters} CHƯƠNG</span>
      </a>
    </div>

    <div class="header-center">
      <span class="header-title">{title}</span>
    </div>

    <div class="header-right">
      <a href="/chuong-1/" class="btn-top-nav next" style="text-decoration:none; padding:6px 14px; font-size:12.5px;">
        <span>Đọc Chương 1 →</span>
      </a>
      <button class="btn-icon" id="btnQuickTheme" title="Chuyển Giao Diện Sáng / Tối" aria-label="Chuyển giao diện sáng tối">
        <svg id="iconMoon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>
    </div>
  </header>

  <!-- MAIN ARTICLE -->
  <main class="seo-page-container">
    <nav class="breadcrumb-nav" aria-label="Breadcrumb">
      <a href="/">Trang Chủ</a>
      <span class="breadcrumb-sep">/</span>
      <span>{category}</span>
      <span class="breadcrumb-sep">/</span>
      <span style="color:var(--gold-primary);">{title}</span>
    </nav>

    <article class="article-header">
      <div class="article-category">{category}</div>
      <h1 class="article-h1">{title}</h1>
      <div class="article-meta">
        <span>Tác giả: <strong>An Bình</strong></span>
        <span>·</span>
        <span>Thời gian đọc: ~{read_mins} phút</span>
        <span>·</span>
        <span>Cập nhật: {date_str}</span>
        <span>·</span>
        <a href="/" style="color:var(--gold-primary);">phatroi.com</a>
      </div>
    </article>

    <div class="article-body">
      {content_html}
    </div>

    <footer class="site-footer">
      <div class="footer-title">PHÁ TRỜI — PHÁ TOÁI THẦN HOANG</div>
      <div class="footer-sub">Trường thiên tiểu thuyết đô thị tu chân Sài Gòn 2026 • Tác giả: An Bình</div>
      <div class="footer-copy">Bản quyền nội dung thuộc về tác giả An Bình © 2026. Mọi quyền được bảo lưu.</div>
    </footer>
  </main>

  <script>
    // Quick Theme Switcher
    const btnTheme = document.getElementById('btnQuickTheme');
    if (btnTheme) {{
      btnTheme.onclick = () => {{
        const htmlEl = document.documentElement;
        const cur = htmlEl.className;
        const next = (cur === 'theme-peaceful-dark' || cur === 'theme-saigon-night' || !cur) ? 'theme-gentle-light' : 'theme-peaceful-dark';
        htmlEl.className = next;
        try {{ localStorage.setItem('pha_troi_theme', next); }} catch(e) {{}}
      }};
    }}

    // Reading Scroll Progress
    const progressBar = document.getElementById('progressBar');
    window.addEventListener('scroll', () => {{
      const curY = window.scrollY;
      const totalH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = totalH > 0 ? Math.min(100, Math.max(0, Math.round((curY / totalH) * 100))) : 0;
      if (progressBar) progressBar.style.width = pct + '%';
    }}, {{ passive: true }});
  </script>
</body>
</html>"""

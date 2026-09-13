# -*- coding: utf-8 -*-
import sys
import io

# Set UTF-8 standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from system.engines.coauthor_engine import CoAuthorEngine

ch17_prose = """# CHƯƠNG 17: ÁNH ĐÈN BÊN DÒNG KÊNH

Bảy giờ tối ngày thứ Bảy, mười chín tháng Chín.

Phố xá Bình Thạnh lên đèn, nhuộm một màu vàng cam ấm áp lên những dòng xe cộ hối hả qua lại trên cầu Thị Nghè. Dưới lòng kênh Nhiêu Lộc, mặt nước lăn tăn gợn sóng phản chiếu những vệt đèn màu của dãy quán cà phê và quán ăn ven đường Hoàng Sa, Trường Sa.

Tôi trở về căn phòng trọ nhỏ trên đường Nơ Trang Long sau một buổi sáng đong đầy những cảm xúc khó tả tại võ quán của ông Ba Khiêm. Mở cánh cửa sổ nhỏ nhìn ra phía khoảng trời đêm lấp lánh ánh đèn đô hội, làn gió mát từ bờ kênh thổi vào mang theo hơi ẩm dịu lành, xua tan đi cái oi ả còn sót lại của ngày nắng gắt.

Tôi bật chiếc đèn bàn màu vàng nhạt, ngồi xuống bàn làm việc. 

Trên mặt bàn gỗ cũ kỹ, bên cạnh chiếc laptop làm việc hàng ngày, tôi mở một cuốn sổ tay bìa da nhỏ. Cầm cây bút bi trên tay, tôi cẩn thận phác thảo lại những đường nét chính của đồ hình kinh mạch mà tôi đã ghi nhớ từng chi tiết trong cuốn `Nam Phương Quyền Kinh` lúc sáng.

Từng nét vẽ hiện lên sống động: dòng khí huyết cuộn chảy từ đan điền, men theo xương cụt, vượt qua đốt sống lưng thứ bảy rồi hướng thẳng lên đỉnh đầu. 

Khi ngắm nhìn đồ hình do chính tay mình vẽ lại, tôi không khỏi trầm ngâm. Hàng trăm năm trước, khi súng đạn phương Tây chưa tràn tới và khoa học công nghệ chưa định hình thế giới, những bậc tiền nhân trần thế nơi mảnh đất phương Nam này đã bằng trực giác phi thường và sự bền bỉ của ý chí mà chạm tới bờ cõi của Thể Đạo. Họ không có máy móc lượng tử, không có cảm biến nhiệt độ phân giải cao, nhưng họ có sự thấu hiểu sâu sắc đối với từng thớ thịt, từng khớp xương của chính mình.

"Ngươi đang nghĩ về vị võ sư già đó?" 

Giọng nói êm ả của Lâm Tịch khẽ vang lên trong cõi sâu thức hải. Chiếc kén khí huyết sinh học ấm áp khẽ rung rinh, tựa như một đóm lửa nhỏ che chắn cho tàn niệm mong manh của nàng giữa đêm tĩnh mịch.

"Đúng vậy," tôi khẽ đáp lại bằng ý niệm, đặt cây bút bi xuống mặt bàn. "Tôi nghĩ về sự kiên định của con người. Cả đời ông Ba Khiêm không mưu cầu xưng bá võ lâm, không mở lò võ kiếm tiền, chỉ lặng lẽ gìn giữ một cuốn sách rách và dạy lũ trẻ con trong xóm cách thở sâu, đứng vững. Đó là một vẻ đẹp rất đỗi bình dị của trần gian."

Trong thức hải, bóng dáng thiếu nữ áo choàng xám bạc khẽ chớp mắt. Nàng tựa lưng vào vách kén khí huyết, ánh mắt nhìn vào khoảng không vô định, giọng nói thoảng qua một chút ngậm ngùi:

"Ở thế giới trước kia của ta... nơi chư thiên bao la với hàng vạn tinh cầu lấp lánh, người tu luyện nhiều như cát sông Hằng. Nhưng phần lớn bọn họ đều bị cuốn vào vòng xoáy tranh đoạt tài nguyên, chém giết lẫn nhau để giành giật từng viên linh đan, từng mảnh bảo địa, sẵn sàng san bằng cả một đại lục chỉ vì một pháp bảo vô tri. Hiếm có ai chịu ngồi lại dưới hiên nhà, uống một tuần trà và ngắm nhìn những đứa trẻ tập bước đi đầu tiên như vị lão nhân kia."

Nàng ngưng lại một chút, thanh âm bỗng trở nên dịu dàng hơn:

"Ngươi cũng rất giống ông ấy. Ngươi có sức mạnh vượt xa người thường, nhưng trong tâm ngươi chưa từng khởi lên ý niệm coi thường đồng loại, cũng chưa từng muốn dùng nó để tranh đoạt danh lợi phù phiếm."

Tôi mỉm cười, nhìn ra ánh đèn lấp lánh ngoài khung cửa sổ:

"Vì tôi hiểu rõ mình là ai. Tôi sinh ra là một con người phàm trần, lớn lên từ những bữa cơm gia đình đạm bạc, từng trải qua cảm giác mệt mỏi sau những ngày làm thêm kiệt sức. Sức mạnh này không phải để tôi đứng trên kẻ khác, mà là để tôi có thể tự chủ cuộc đời mình, và bảo vệ những người tôi yêu quý khỏi những biến cố bất ngờ."

"Một tâm thái vững chãi," Lâm Tịch khẽ gật đầu, trong giọng nói toát lên sự thán phục chân thành. "Chính tâm thái đó mới là đạo cơ vững chắc nhất để ngươi đi xa trên con đường Thể Đạo. Hãy bắt đầu điều tức đi, ta cảm nhận thấy dòng máu của ngươi sau khi hấp thu kinh nghiệm thôi thủ sáng nay đang cuộn trào rất mãnh liệt."

Chín giờ ba mươi phút tối.

Tôi tắt đèn bàn, chỉ để lại ngọn đèn ngủ le lói ở góc phòng. Ngồi xếp bằng trên tấm đệm cói quen thuộc, tôi khép nhẹ hai mi mắt, thả lỏng toàn bộ cơ bắp từ vai, gáy cho tới các đầu ngón chân.

Áp dụng phương pháp điều hòa hơi thở phối hợp thính kình mà ông Ba Khiêm chỉ dạy, tôi hít vào một hơi thật sâu bằng mũi, đưa không khí mát lành xuống tận đáy phổi, ép cơ hoành hạ thấp. 

*Thình... thịch... thình... thịch...*

Nhịp tim tôi chậm dần, đều đặn ở mức năm mươi lăm nhịp mỗi phút. Dòng khí huyết ấm áp trong lồng ngực bắt đầu chuyển động, tựa như một dòng phù sa đỏ thắm bắt đầu cuộc hành trình tuần hoàn.

Khí huyết cuộn trào xuống xương cụt, tích tụ thành một luồng nhiệt năng dồi dào rồi bắn vọt lên trên theo trục tủy sống. Khi dòng máu lướt qua đốt sống lưng thứ bảy — nơi chiếc then cài đầu tiên đã bị phá nứt đêm trước — nó chảy qua êm ru, trơn tru như thuyền xuôi dòng nước lớn, không hề gặp phải một chút trở lực nào.

Thế nhưng, khi dòng khí huyết dồi dào ấy tiếp tục dâng cao qua vùng bả vai, tiến thẳng về phía cổ áo thì bất ngờ khựng lại!

*Ầm!*

Một cảm giác nghẽn tắc sắc lạnh đột ngột xuất hiện ngay tại đốt sống cổ thứ ba — vị trí huyệt Đại Chùy nằm giữa hai bờ vai.

Nó không phải là sự tắc nghẽn của mạch máu sinh học thông thường, mà là một lớp màng ngăn vô hình, cứng chắc và lạnh lẽo tựa như một khối đá vôi ngàn năm hóa thạch nằm sâu trong tủy sống. Dòng máu nóng hổi dội thẳng vào lớp màng ấy, lập tức dội ngược trở lại, tạo nên một cơn đau nhức âm ỉ lan dọc từ chân gáy lên thái dương.

Hơi thở tôi khẽ ngưng trệ, hai bên thái dương giật giật từng cơn. 

"Đừng hoảng loạn," tiếng nhắc nhở sắc bén nhưng điềm tĩnh của Lâm Tịch lập tức vang lên bên tai tôi. "Đó chính là then cài phong ấn thứ hai: huyệt Đại Chùy!"

Tôi cắn chặt răng, duy trì tư thế ngồi thẳng lưng, dùng ý niệm giữ vững dòng tuần hoàn không để nó bị tán loạn:

"Then cài thứ hai sao?"

"Đúng vậy," Lâm Tịch giải thích cặn kẽ. "Trên thể phách con người tại Cố Thổ, chín chiếc then cài phong ấn viễn cổ được bố trí dọc theo trục thiên địa của cơ thể. Then cài đốt sống thứ bảy ở thắt lưng là 'Khí Huyết Hạ Bàn', cai quản sức bật cơ bắp và độ thăng bằng của hạ thể. Còn chiếc then cài Đại Chùy tại đốt sống cổ này chính là rào cản ngăn cách giữa thân thể và não bộ — gọi là 'Khí Huyết Thấu Não'."

Nàng dừng lại một nhịp rồi tiếp tục:

"Khi then cài Đại Chùy bị khóa kín, dòng máu giàu dưỡng chất và năng lượng sinh học không thể dâng lên nuôi dưỡng trọn vẹn các tế bào thần kinh đại não. Con người phàm trần vì thế mà tư duy nhanh mệt mỏi, phản xạ bị giới hạn bởi tốc độ truyền dẫn hóa học thông thường. Nếu ngươi phá vỡ được chiếc then cài này, dòng khí huyết sẽ thấu suốt lên đỉnh Bách Hội, mở ra vòng Nhị Chu Thiên trọn vẹn, giác quan và năng lực phản xạ của ngươi sẽ thăng hoa lên một tầm cao hoàn toàn mới."

Tôi lắng nghe từng lời của Lâm Tịch, cảm nhận rõ rệt sự va đập nhịp nhàng của dòng máu ấm áp lên khối đá vôi vô hình tại đốt sống cổ. Cảm giác căng tức, buốt lạnh nơi chân gáy kéo dài dai dẳng, tựa như có hàng ngàn mũi kim châm li ti đang gõ vào xương tủy.

Nhớ lại bài học sáng nay của ông Ba Khiêm về việc "Dưỡng khí bồi tủy, không nôn nóng cưỡng cầu", tôi không cố chấp dồn ép khí huyết tông mạnh vào then cài để tránh gây tổn thương cho các dây thần kinh nhạy cảm nơi tủy sống. Thay vào đó, tôi khẽ chùng vai, uốn nhẹ các đốt sống cổ, điều phối dòng máu nóng chảy chậm rãi, bao bọc lấy khối màng đá vôi, dùng nhiệt năng sinh học kiên trì mài giũa, thẩm thấu từng chút một.

Trong cõi sâu thức hải, chứng kiến sự điềm đạm và kiên nhẫn phi thường của tôi, hình bóng thiếu nữ của Lâm Tịch khẽ cử động.

Vạt áo choàng xám bạc của nàng khẽ lay động trong làn sương mỏng. Từ vạt áo ấy, một đóm tàn vũ lấp lánh ánh xám tro — một tia sinh cơ thuần khiết kết tinh từ tàn niệm nguyên thủy của nàng — nhẹ nhàng tách ra, bay xuyên qua màng kén khí huyết rồi hòa tan vào dòng máu ấm áp đang chảy quanh vùng cổ của tôi.

*Xèo...*

Một luồng ấm áp kỳ diệu bỗng nhiên lan tỏa khắp đốt sống cổ thứ ba. 

Cơn đau buốt âm ỉ tức thì dịu đi phân nửa. Lớp màng đá vôi cứng ngắc kia dưới sự tác động đồng thời của dòng máu nóng và tia sinh cơ xám bạc bỗng nhiên khẽ phát ra một tiếng rạn nứt cực nhỏ, tựa như một vết rạn chân chim vừa xuất hiện trên mặt tảng băng dày.

Tôi thở phào nhẹ nhõm, thu hồi khí huyết trở về đan điền, chầm chậm mở mắt ra.

Mười một giờ ba mươi phút đêm.

Đồng hồ trên tường nhích từng tích tắc đều đặn. Toàn thân tôi tuy toát một lớp mồ hôi mỏng nhưng tinh thần lại vô cùng sảng khoái và tỉnh táo. Cổ họng tôi ngọt ngào, vùng gáy ấm áp lạ thường, và vết nứt nhỏ tại huyệt Đại Chùy cho tôi biết rằng cánh cửa bước vào cảnh giới Nhị Chu Thiên đã không còn xa nữa.

Đứng dậy bước ra ban công, gió đêm từ dòng kênh Nhiêu Lộc lồng lộng thổi qua vạt áo tôi. Thành phố Sài Gòn đã dần chìm vào giấc ngủ muộn, những ánh đèn cao ốc xa xa mờ ảo trong làn sương đêm.

Tôi hít một hơi thật sâu lồng ngực, hướng ánh mắt kiên định về phía màn đêm thăm thẳm. Đêm mai, khi khí huyết tích tụ đến đỉnh điểm, tôi sẽ chính thức khai mở chiếc then cài Đại Chùy này."""

def main():
    print("--- KHỞI CHẠY QUY TRÌNH VIẾT CHƯƠNG 17 ---")
    engine = CoAuthorEngine()
    result = engine.write_next_chapter(
        target_chapter_num=17,
        pov="Nguyễn Minh An (Ngôi thứ nhất)",
        custom_draft_prose=ch17_prose
    )
    print("Kết quả pipeline:", result["success"])
    print("Đường dẫn Markdown:", result["md_path"])
    print("Đường dẫn Word DOCX:", result["docx_path"])
    print("Tổng số từ:", result["word_count"])
    print("Kiểm duyệt (Audit Passed):", result["critique"]["passed"])
    if not result["critique"]["passed"]:
        print("Danh sách cảnh báo:", result["critique"]["issues"])
    print("Hoàn tất!")

if __name__ == "__main__":
    main()

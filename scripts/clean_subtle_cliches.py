# -*- coding: utf-8 -*-
import os

replacements = [
    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01\ch_007.md",
     "Chị Mai hoàn toàn sững sờ, đồng tử co rút lại vì hoảng loạn, không kịp có bất kỳ phản xạ né tránh nào.",
     "Chị Mai hoàn toàn sững sờ, mặt cắt không còn hạt máu vì hoảng loạn, không kịp có bất kỳ phản xạ né tránh nào."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01\ch_011.md",
     "Đồng tử tôi khẽ co lại, nhưng nhịp tim và nét mặt vẫn giữ được sự bình thản tuyệt đối.",
     "Sống lưng tôi khẽ lạnh đi, nhưng nhịp thở và nét mặt vẫn giữ được sự bình thản tuyệt đối."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01\ch_034.md",
     "Lâm Tịch khẽ đưa ngón tay thanh mảnh chạm vào vết tích vừa hé lộ, khóe môi khẽ cong lên một nụ cười hiếm hoi:",
     "Lâm Tịch đưa ngón tay chạm vào vết tích vừa hé lộ, khẽ mỉm cười:"),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01\ch_044.md",
     "Nghe những lời cảnh báo rợn người ấy, khóe môi tôi dưới lớp mặt nạ lặn bỗng khẽ nhếch lên một nụ cười kiêu hãnh.",
     "Nghe những lời cảnh báo rợn người ấy, tôi chỉ nghiến chặt quai hàm dưới lớp mặt nạ lặn, ánh mắt không hề chùn bước."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_048.md",
     "Tôi nhìn màn hình nứt góc một lúc lâu, khóe môi khẽ cong lên một nụ cười ấm áp.",
     "Tôi nhìn màn hình nứt góc một lúc lâu, trong lòng ấm lại."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_052.md",
     "ánh mắt tên trùm phế liệu thoáng chốc lóe lên một tia độc địa tàn nhẫn.",
     "ánh mắt tên trùm phế liệu đanh lại, lạnh lùng và tàn nhẫn."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_053.md",
     "Tôi nhìn đứa bé, khóe môi khẽ nhếch lên một nụ cười mệt mỏi nhưng ấm áp.",
     "Tôi nhìn đứa bé, gượng cười mệt mỏi nhưng ấm áp."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_058.md",
     "Nghe đến đây, đồng tử mắt tôi khẽ co lại.",
     "Nghe đến đây, tôi khựng người lại một nhịp."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_059.md",
     "Tôi đứng lặng giữa xưởng tôn tối om, ánh mắt lóe lên tia sáng tính toán sắc sảo của một kỹ sư trắc địa.",
     "Tôi đứng lặng giữa xưởng tôn tối om, đầu óc tính toán nhanh như một chiếc máy trắc địa."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_060.md",
     "Tôi thở phào nhẹ nhõm, khóe môi khẽ nhếch lên một nụ cười kín đáo.",
     "Tôi thở phào nhẹ nhõm, lòng trút đi được một gánh nặng lớn."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_060.md",
     "Trong đáy mắt Lâm Tịch lóe lên một tia dao động tán thưởng mờ nhạt. Nàng khẽ nghiêng đầu:",
     "Lâm Tịch khẽ nghiêng đầu nhìn tôi, trong ánh mắt thoáng vẻ tán thưởng:"),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_073.md",
     "ánh mắt anh khẽ lóe lên một tia ngạc nhiên kín đáo.",
     "ánh mắt anh thoáng vẻ ngạc nhiên kín đáo."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_080.md",
     "khóe môi khẽ nhếch lên.",
     "khóe môi gợn một nụ cười gằn."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_081.md",
     "Ánh mắt hắn lóe lên tia hung quang dữ tợn như một con thú dữ săn mồi giữa đêm đen.",
     "Đôi mắt vằn đỏ của hắn đục ngầu dữ tợn như một con thú dữ săn mồi giữa đêm đen."),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_086.md",
     '"Cửu Long Thiên Hải đã bắt đầu ra tay rồi," tôi thầm nhủ trong lòng, ánh mắt chợt lóe lên một tia sắc lạnh.',
     '"Cửu Long Thiên Hải đã bắt đầu ra tay rồi," tôi thầm nhủ, ánh mắt đanh lại sắc lạnh.'),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_086.md",
     "Tôi nhìn ra dòng sông Sài Gòn đang cuộn sóng phù sa dưới ánh nắng trưa rực rỡ, khóe môi khẽ nhếch lên một nụ cười ngạo nghễ của người thủ hộ phàm nhân:",
     "Tôi nhìn ra dòng sông Sài Gòn đang cuộn sóng phù sa dưới ánh nắng trưa rực rỡ, lòng thanh thản tựa như mặt nước:"),

    (r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_02\ch_087.md",
     '"Toán đột nhập số 3," tôi thầm nhủ, ánh mắt lóe lên một tia sát khí lạnh buốt.',
     '"Toán đột nhập số 3," tôi thầm nhủ, toàn thân căng cứng như dây cung.')
]

count = 0
for path, old, new in replacements:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if old in content:
            content = content.replace(old, new)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print(f"Replaced in {os.path.basename(path)}")
        else:
            print(f"NOT FOUND in {os.path.basename(path)}: {old[:40]}...")

print(f"Total replaced: {count}/{len(replacements)}")

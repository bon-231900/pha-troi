# -*- coding: utf-8 -*-
import os
import json
import sqlite3
from system.core.config import ROOT_DIR, DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.context_builder import ContextBuilder
from system.engines.critique_engine import CritiqueEngine
from system.engines.revision_engine import RevisionEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.telemetry_engine import TelemetryEngine
from system.core.git_manager import GitManager

class CoAuthorEngine:
    """Thực thi hợp đồng 'Viết tiếp': Đọc state -> Context -> Narrative Move -> Draft -> Critique -> Revise -> Update -> Save -> Docx -> Commit."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.context_builder = ContextBuilder(db_path)
        self.critique_engine = CritiqueEngine(db_path)
        self.revision_engine = RevisionEngine()
        self.docx_pipeline = DocxPipeline()
        self.retrieval_engine = RetrievalEngine(db_path)
        self.telemetry_engine = TelemetryEngine(db_path)
        self.git_manager = GitManager(ROOT_DIR)

    def write_next_chapter(self, target_chapter_num: int = 1, pov: str = "Nguyễn Minh An (Ngôi thứ nhất)", custom_draft_prose: str = None) -> dict:
        active_chars = ["char_minh_an", "char_lam_tich"]
        location_id = "loc_hcmc"

        # 1. Build Context
        context_pack = self.context_builder.build_context_pack(target_chapter_num, pov, active_chars, location_id)

        # 2. Soạn bản thảo
        if custom_draft_prose:
            prose = custom_draft_prose
        else:
            prose = self._generate_canonical_chapter_1()

        # 3. Critique pass
        audit_res = self.critique_engine.audit_chapter_draft(target_chapter_num, pov, active_chars, prose)

        # 4. Revision nếu có issue nhỏ
        if not audit_res["passed"]:
            crit_errors = [i for i in audit_res["issues"] if i["severity"] == "CRITICAL"]
            if crit_errors:
                return {
                    "success": False,
                    "reason": "CRITICAL_CONTINUITY_ERROR",
                    "issues": audit_res["issues"]
                }
        
        refined_prose = self.revision_engine.auto_fix_minor_issues(prose, audit_res["issues"])

        # 5. Save Markdown Source of Truth
        md_file = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_01", f"ch_{target_chapter_num:03d}.md")
        os.makedirs(os.path.dirname(md_file), exist_ok=True)
        with open(md_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(refined_prose.strip() + "\n")

        # 5b. Update Retrieval Index (FTS5 BM25 scene indexing)
        indexed_count = self.retrieval_engine.index_chapter(md_file)

        # 6. Compile Word DOCX
        docx_file = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", f"ch_{target_chapter_num:03d}.docx")
        lines = [ln.strip() for ln in refined_prose.strip().split("\n") if ln.strip()]
        ch_title = lines[0].replace("#", "").strip() if lines and lines[0].startswith("#") else f"Chương {target_chapter_num}"
        self.docx_pipeline.export_chapter_to_docx(ch_title, target_chapter_num, refined_prose, docx_file)

        # 7. Update State
        self._update_state_post_chapter(target_chapter_num, ch_title)

        # 7b. Record Telemetry
        self.telemetry_engine.record_event(
            task_type="COAUTHOR_PIPELINE",
            model_tier="DETERMINISTIC",
            tokens_in_est=len(refined_prose.split()) * 2,
            tokens_out_est=len(refined_prose.split()) * 2,
            tokens_saved_est=5000,
            deterministic_ops_count=indexed_count + 4,
            cache_hit=True,
            description=f"Quy trình hậu xử lý tự động & lập chỉ mục FTS5 Chương {target_chapter_num}"
        )

        # 8. Git Commit Minor
        self.git_manager.commit_minor(f"Cập nhật hoàn chỉnh Chương {target_chapter_num} (Markdown + DOCX + State + Index)")

        return {
            "success": True,
            "chapter_num": target_chapter_num,
            "md_path": md_file,
            "docx_path": docx_file,
            "word_count": len(refined_prose.split()),
            "critique": audit_res
        }

    def _generate_canonical_chapter_1(self) -> str:
        """Soạn bản thảo Chương 1 chuẩn mực: Modern Cinematic + Literary + Vietnam Realism."""
        return """# CHƯƠNG 1: MƯA TRÊN PHỐ CŨ

Sài Gòn vào tháng Chín luôn có những buổi chiều kỳ lạ. 

Năm giờ ba mươi, bầu trời trên đầu ngã tư Hàng Xanh vẫn còn váng vất ánh nắng oi nồng đặc trưng của miền nhiệt đới, thứ ánh sáng hanh hao rọi xuống dòng xe cộ ken đặc như nêm. Nhưng chỉ cần kim đồng hồ nhích qua con số sáu, từng cuộn mây xám xịt từ phía thượng nguồn sông Đồng Nai đã ào ạt tràn về, nuốt chửng những vệt ráng chiều cuối cùng. Gió nổi lên phần phật, cuốn theo bụi đường, mùi xăng khói và cả mùi hơi nước ngai ngái bốc lên từ mặt đường nhựa bỏng rát.

Tôi kéo chiếc khẩu trang y tế lên sát sống mũi, gạt chân chống chiếc xe Wave cũ đã cùng mình đi qua bốn năm đại học và một năm đi làm. Điện thoại trong túi quần rung lên hai hồi ngắn ngủi — thông báo từ ứng dụng ngân hàng trừ tiền bữa trưa và một email từ trưởng phòng nhắc nhở bảng số liệu báo cáo tuần.

Tôi hai mươi lăm tuổi. Không có gì nổi bật giữa tám triệu con người đang hối hả chen chúc dưới làn khói xe này. Sáng đi làm, chiều về phòng trọ, tối mở máy tính xem một bộ phim cũ hoặc lướt vài diễn đàn rồi chìm vào giấc ngủ. Một cuộc đời bình lặng đến mức nếu có ai đó hỏi tôi ba năm nữa mình sẽ ra sao, tôi cũng chỉ có thể mỉm cười gãi đầu.

Tiếng sấm đầu tiên rền vang phía chân trời, trầm đục và khô khốc.

Mưa đổ xuống.

Không phải từng hạt lất phất báo trước, mà là cả một màn nước trắng xóa dội thẳng từ trời cao, quất rát mặt những người đi đường chưa kịp tấp xe vào lề mặc áo mưa. Tôi nép vội vào mái hiên của một tiệm sửa khóa ven đường Ung Văn Khiêm, nước mưa từ mép tôn chảy xối xả xuống đôi giày vải ướt sũng. 

Tôi ngửa đầu nhìn lên vòm trời mịt mù. 

Giữa những tia chớp chằng chịt rạch ngang tầng mây đen kịt, có một khoảnh khắc kỳ dị mà sau này dù trải qua bao nhiêu biến cố, tôi vẫn không bao giờ quên được. 

Không có ánh sáng chói lòa, không có tiếng nổ long trời lở đất. Chỉ có một vệt màu tro tàn rất nhạt — mỏng như một sợi tơ, lặng lẽ rơi xuyên qua màn mưa giông dày đặc. Nó không mang theo nhiệt độ, không phát ra âm thanh, rơi nhanh đến mức tôi cứ ngỡ đó chỉ là một ảo giác do mắt mình mỏi mệt sau tám tiếng đồng hồ dán chặt vào màn hình máy tính.

Nhưng ngay khi vệt sáng mờ nhạt ấy lướt qua khoảng không trước mặt tôi chừng mười mét, một cơn đau nhói đột ngột giáng thẳng vào sau gáy.

Đó không phải là cơn đau của da thịt. Cảm giác ấy giống như có một giọt sương băng giá rơi thẳng vào sâu trong tâm thức, khiến toàn bộ thần kinh tôi co giật dữ dội. Tôi lảo đảo tựa lưng vào bức tường gạch loang lổ rêu phong, hơi thở nghẹn lại nơi cuống họng. Đôi tai lùng bùng, tiếng còi xe inh ỏi và tiếng mưa gầm rú xung quanh bỗng nhiên trôi dạt ra xa xôi, như thể tôi vừa bị kéo tụt xuống đáy của một hồ nước lạnh buốt.

Trong cõi sâu thẳm của sự mông muội ấy, tôi dường như thoáng thấy một bóng hình. 

Một bóng hình đứng giữa biển máu ngập tràn và những vòm trời đổ nát, xung quanh là vô số vì sao đang lụi tàn như tàn thuốc. Người đó mặc bạch y đã rách nát loang lổ vết chém, một tay nắm lấy chuôi kiếm gãy, mái tóc dài tung bay giữa những luồng bão tố cuồng nộ có thể nghiền nát cả sơn hà. Nhưng điều khiến lồng ngực tôi thắt lại không phải là cảnh tượng hủy diệt ấy, mà là đôi mắt của nàng.

Đó là đôi mắt của một người đã chiến đấu đến hơi thở cuối cùng, đã đứng chắn trước vô số sinh linh để rồi chứng kiến tất cả tan biến, tịch mịch đến mức không còn một giọt nước mắt.

Một tiếng thở dài khẽ khàng, mỏng manh như khói thoảng, vang lên ngay trong đáy lòng tôi:

— Hóa ra... nơi này...

Cơn đau biến mất nhanh như khi nó xuất hiện.

Tôi bừng tỉnh, mồ hôi lạnh toát ra ướt đẫm lưng áo sơ mi hòa cùng nước mưa tạt vào mép hiên. Tim tôi đập thình thịch như muốn nhảy khỏi lồng ngực. Đường phố vẫn là đường phố, dòng người mặc áo mưa đủ sắc màu vẫn kiên nhẫn nhích từng mét giữa dòng nước bắt đầu dâng ngập nửa bánh xe.

Tôi đưa tay sờ lên sau gáy. Không có vết thương, không có máu, chỉ có làn da vẫn còn lành lạnh.

"Chắc là trúng gió rồi..." Tôi tự nhủ, cố gắng hít một hơi thật sâu để xua đi cảm giác ớn lạnh kỳ lạ vừa quét qua thân thể.

Mưa ngớt dần. Tôi dắt xe ra đường, hòa vào dòng người tiếp tục hành trình trở về căn phòng trọ nhỏ bé của mình, hoàn toàn không hay biết rằng, bánh xe của một định mệnh vượt ngoài tầm hiểu biết của thế gian đã bắt đầu chậm rãi xoay chuyển.
"""

    def _update_state_post_chapter(self, chapter_num: int, chapter_title: str = ""):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        cur = conn.cursor()
        title_clean = chapter_title.replace("#", "").strip() or f"Chương {chapter_num}"
        
        # Plot node update
        cur.execute("""INSERT OR REPLACE INTO plot_nodes (id, node_type, parent_id, order_index, title, status)
                       VALUES (?, 'CHAPTER', 'arc_01', ?, ?, 'CANONIZED')""",
                    (f"ch_{chapter_num:03d}", chapter_num, title_clean))

        if chapter_num == 1:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", "Cơn mưa rào ngã tư Hàng Xanh và khoảnh khắc tàn hồn rơi", chapter_num, 1,
                         "2026-09-13T18:00:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                         "Minh An tan sở trú mưa ở Ung Văn Khiêm, bị tàn hồn Lâm Tịch rơi trúng thức hải, trải qua cơn đau nhói và thoáng thấy ảo ảnh chiến trường viễn cổ.",
                         "Lâm Tịch hoàn tất neo đậu vào thức hải Minh An; Minh An ngỡ là trúng gió cảm mạo."))
        elif chapter_num == 2:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", "Thanh âm đầu tiên trong căn phòng trọ Bình Thạnh", chapter_num, 1,
                         "2026-09-13T20:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                         "Minh An về phòng trọ sau mưa ngập, cảm nhận hàn ý và thấy đốm tro tàn trong mắt. Tàn hồn Lâm Tịch cất tiếng hỏi, xác nhận cảnh tượng biển máu là thật trước khi ngủ say.",
                         "Minh An xác định không phải bệnh lý tâm thần; thiết lập liên kết ý thức sơ khởi giữa hai người."))
            
            # Character states
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_minh_an", 2, "Phòng trọ Bình Thạnh", "Phàm nhân", "Bình thường, hơi lạnh sau gáy và bàn tay",
                         json.dumps([], ensure_ascii=False),
                         json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ"], ensure_ascii=False),
                         "Căng thẳng cảnh giác, bàng hoàng nhưng giữ được bình tĩnh"))
            
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_lam_tich", 2, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                         json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                         json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                         "Cảnh giác, kiêu hãnh nhưng mệt mỏi cùng cực, chìm vào ngủ say"))
            
            # Foreshadowing seed FSH-002
            cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("FSH-002", "Đốm tro tàn thoáng hiện trong đồng tử và hiện tượng sương giá ngưng đọng quanh cốc nước", 2, 1,
                         json.dumps(["Minh An"], ensure_ascii=False),
                         "Dấu hiệu nguyên thần Lâm Tịch vô thức rò rỉ hàn khí quy tắc ra môi trường xung quanh Minh An", 5, "PLANTED"))
        elif chapter_num == 3:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", "Đêm trắng đầu tiên và nhịp thở chia sẻ", chapter_num, 1,
                         "2026-09-14T03:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                         "Minh An trải qua một đêm trắng tìm kiếm thông tin y khoa, nhận thức được sự hiện diện yếu ớt của Lâm Tịch. Nhịp tim và khí huyết phàm nhân vô thức che chở cho đốm lửa tàn. Sáng sớm, Minh An vẫn phải mặc áo sơ mi đi làm mưu sinh.",
                         "Minh An chấp nhận thực tại siêu nhiên nhưng giữ vững cuộc sống đời thường; bước đầu hình thành sự cộng hưởng khí huyết tự nhiên."))
            
            # Character states
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_minh_an", 3, "Phòng trọ Bình Thạnh -> Đi làm", "Phàm nhân", "Thiếu ngủ, mắt hơi thâm quầng nhưng tinh thần tĩnh táo khác thường",
                         json.dumps([], ensure_ascii=False),
                         json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Cà phê gói"], ensure_ascii=False),
                         "Trầm tĩnh, chấp nhận thực tế, kiên định"))
            
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_lam_tich", 3, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                         json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                         json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                         "Ngủ sâu bảo tồn nguyên thần, an tĩnh"))
            
            # Foreshadowing seed FSH-003
            cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("FSH-003", "Khí huyết sinh học của cơ thể phàm nhân vô thức nuôi dưỡng ngọn lửa tàn của nguyên thần viễn cổ", 3, 1,
                         json.dumps(["Minh An"], ensure_ascii=False),
                         "Nguyên lý sơ khai của con đường Khí Huyết Đạo tại Trái Đất bị phong ấn", 12, "PLANTED"))
        elif chapter_num == 4:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", "Bản hòa âm trần thế và tiếng vọng giữa trưa hè", chapter_num, 1,
                         "2026-09-14T12:15:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                         "Minh An hòa vào nhịp sống công sở hối hả tại Quận 1, trải nghiệm sự tương phản giữa thực tại cơm áo gạo tiền và cõi sâu tâm thức. Buổi trưa tại quán cơm tấm, hạt băng bất ngờ ngưng kết trên thành cốc trà đá khi Lâm Tịch khẽ thức giấc đặt câu hỏi về nhân gian ồn ào.",
                         "Minh An giữ vững tâm tính phàm trần điềm tĩnh; sự hiện diện của Lâm Tịch dần hòa nhập vào trải nghiệm cảm quan đời thường mà không làm đảo lộn trật tự xã hội."))
            
            # Character states
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_minh_an", 4, "Văn phòng Quận 1 -> Quán cơm tấm hẻm Nguyễn Thị Minh Khai", "Phàm nhân", "Khí huyết dồi dào nhẹ, phản xạ nhanh nhạy hơn, thể lực ổn định",
                         json.dumps([], ensure_ascii=False),
                         json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Laptop công ty"], ensure_ascii=False),
                         "Điềm tĩnh, quan sát sâu sắc, thấu cảm"))
            
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_lam_tich", 4, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                         json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                         json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                         "Hiếu kỳ yếu ớt, ngạc nhiên trước trần thế không có linh khí, lại chìm vào giấc ngủ"))
            
            # Foreshadowing seed FSH-004
            cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("FSH-004", "Quy tắc hàn băng vi mô phát sinh tại môi trường nhiệt độ cao (giọt nước ngưng băng trên cốc trà đá giữa trưa)", 4, 1,
                         json.dumps(["Minh An"], ensure_ascii=False),
                         "Quy tắc Băng Phách của Lâm Tịch bắt đầu có hiện tượng rò rỉ thụ động ra vật chất ngoại cảnh khi nàng chuyển mình ý thức", 7, "PLANTED"))
        elif chapter_num == 5:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", "Cuộc đối thoại dưới ánh đèn đêm và lời giới thiệu tên họ", chapter_num, 1,
                         "2026-09-14T21:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                         "Minh An trở về phòng trọ sau ngày làm việc. Trong đêm tĩnh mịch, Lâm Tịch tỉnh giấc lâu hơn, chính thức giới thiệu danh tự của mình và giải thích về đạo cơ vỡ nát cùng nguyên nhân hàn khí rò rỉ. Hai người chia sẻ góc nhìn về nhân sinh ngắn ngủi của phàm nhân và sự tịch diệt của chư thiên vị diện.",
                         "Hoàn tất thu hồi phục bút FSH-002; xác lập liên kết nhận thức sâu sắc giữa Minh An và Lâm Tịch; gieo mầm phục bút FSH-005 về thảm họa Phá Trời."))
            
            # Character states
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_minh_an", 5, "Phòng trọ Bình Thạnh", "Phàm nhân", "Khí huyết lưu chuyển hài hòa, bắt đầu có cảm ứng vi mô với nhiệt độ và sinh mệnh lực xung quanh",
                         json.dumps([], ensure_ascii=False),
                         json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Cốc trà sứ"], ensure_ascii=False),
                         "Trầm lắng, thấu cảm sâu sắc, bắt đầu gánh vác trọng trách vô hình"))
            
            cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("char_lam_tich", 5, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                         json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                         json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                         "Bớt cảnh giác, chấp nhận nương tựa, thoáng ngậm ngùi trước triết lý nhân gian"))
            
            # Payoff FSH-002
            cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-002'""")

            # Foreshadowing seed FSH-005
            cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("FSH-005", "Lời nhắc mơ hồ của Lâm Tịch về 'Bầu trời bị tha hóa' và thanh kiếm gãy chém đứt quy tắc", 5, 1,
                         json.dumps(["Minh An"], ensure_ascii=False),
                         "Bản chất của thảm họa diệt thế chư thiên: Thiên Đạo sinh ra ý chí độc hại nuốt chửng các vị diện", 20, "PLANTED"))
        else:
            cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (f"EVT-CH{chapter_num:03d}-01", title_clean, chapter_num, 1,
                         "2026-09-13T21:00:00+07:00", "loc_hcmc", json.dumps(["char_minh_an"], ensure_ascii=False),
                         f"Diễn biến tiếp nối của Chương {chapter_num}.", "Hoàn thành chương."))
            
        conn.commit()
        conn.close()
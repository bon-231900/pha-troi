# -*- coding: utf-8 -*-
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try: sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

import argparse
import json
from system.core.lock import verify_novel_lock
from system.engines.coauthor_engine import CoAuthorEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.canon_engine import CanonEngine
from system.engines.character_engine import CharacterEngine
from system.engines.world_engine import WorldEngine
from system.engines.timeline_engine import TimelineEngine
from system.engines.foreshadowing_engine import ForeshadowingEngine
from system.engines.proposal_manager import ProposalManager
from system.engines.test_runner import run_all_narrative_tests
from system.engines.telemetry_engine import TelemetryEngine
from system.engines.retrieval_engine import RetrievalEngine

def main():
    verify_novel_lock()
    parser = argparse.ArgumentParser(
        prog="NovelOS",
        description="NOVEL OS — HỆ ĐIỀU HÀNH SÁNG TÁC TIỂU THUYẾT 'PHÁ TRỜI'",
        epilog="Chuyên dụng cho tiểu thuyết trường thiên 2.000+ chương. Quyền tối cao thuộc về Author."
    )
    subparsers = parser.add_subparsers(dest="command", help="Danh sách lệnh vận hành hệ thống")

    p_write = subparsers.add_parser("viet-tiep", aliases=["write-next"], help="Tự động viết tiếp chương mới theo đúng Canon và Continuity")
    p_write.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="Số thứ tự chương cần sáng tác (mặc định: 1)")
    p_write.add_argument("--pov", type=str, default="Nguyễn Minh An (Ngôi thứ nhất)", help="Góc nhìn người kể (POV)")

    p_rewrite = subparsers.add_parser("viet-lai", aliases=["rewrite"], help="Soạn lại chương theo định hướng mới")
    p_rewrite.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="Số thứ tự chương cần viết lại")

    subparsers.add_parser("kiem-tra", aliases=["audit", "check"], help="Kiểm tra toàn diện tính nhất quán, Canon, Dòng thời gian và Logic tự sự")

    p_export = subparsers.add_parser("xuat-word", aliases=["export-word"], help="Biên dịch bản thảo ra định dạng Word (.docx) chuẩn in ấn")
    p_export.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="Chương cần xuất")

    subparsers.add_parser("canon", help="Tra cứu toàn bộ danh mục quy tắc, tiền đề và thiết lập Canon đã khóa")
    subparsers.add_parser("nhan-vat", aliases=["characters"], help="Tra cứu hồ sơ, thể trạng, thương tổn, cảnh giới và túi đồ nhân vật")
    subparsers.add_parser("thoi-gian", aliases=["timeline"], help="Xem dòng thời gian các sự kiện tuyệt đối và tương đối")
    subparsers.add_parser("the-gioi", aliases=["world"], help="Xem phân tầng thế giới (Cosmology) và bản đồ các vị diện")
    subparsers.add_parser("phuc-but", aliases=["foreshadowing"], help="Xem sổ cái phục bút và các hạt mầm Chekhov's Gun")
    subparsers.add_parser("de-xuat", aliases=["proposals"], help="Xem danh sách đề xuất thay đổi Canon đang chờ Author duyệt")

    p_app = subparsers.add_parser("duyet", aliases=["approve"], help="Phê duyệt đề xuất thay đổi Canon")
    p_app.add_argument("id", type=str, help="Mã định danh đề xuất (Proposal ID)")

    p_rej = subparsers.add_parser("tu-choi", aliases=["reject"], help="Từ chối đề xuất thay đổi Canon")
    p_rej.add_argument("id", type=str, help="Mã định danh đề xuất (Proposal ID)")

    subparsers.add_parser("kiem-thu", aliases=["test"], help="Chạy bộ kiểm thử tự động 21 tình huống narrative logic")
    subparsers.add_parser("tiet-kiem", aliases=["telemetry", "token-metrics"], help="Báo cáo viễn trắc đo lường mức độ tiết kiệm token và thao tác tất định")

    p_search = subparsers.add_parser("tim-kiem", aliases=["search", "memory-search"], help="Tra cứu ký ức, tình tiết, nhân vật và Canon siêu tốc bằng FTS5 BM25")
    p_search.add_argument("query", type=str, help="Từ khóa hoặc ngữ cảnh cần tìm kiếm")
    p_search.add_argument("--type", type=str, default=None, help="Loại tài liệu: chapter_scene, canon_rule, character_profile, research_cache")
    p_search.add_argument("--limit", type=int, default=5, help="Số lượng kết quả tối đa (mặc định: 5)")

    subparsers.add_parser("studio", aliases=["serve"], help="Khởi động giao diện Novel OS Web Studio trực quan")

    args = parser.parse_args()

    if args.command in ["viet-tiep", "write-next"]:
        print(f"[*] Đang kích hoạt chu trình 'Viết tiếp' cho Chương {args.chapter}...")
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter, pov=args.pov)
        if res["success"]:
            print(f"[+] SÁNG TÁC THÀNH CÔNG CHƯƠNG {res['chapter_num']}!")
            print(f"    - Tệp Markdown gốc: {res['md_path']}")
            print(f"    - Tệp Word in ấn:  {res['docx_path']}")
            print(f"    - Tổng số từ:      {res['word_count']} từ")
            print(f"    - Tự phản biện:    {res['critique']['total_issues']} lưu ý nhỏ (Hệ thống đã tự chuẩn hóa).")
        else:
            print(f"[-] Không thể hoàn tất chương: {res['reason']}")
            for iss in res.get("issues", []):
                print(f"    ! [{iss['severity']}] {iss['category']}: {iss['description']}")

    elif args.command in ["kiem-tra", "audit", "check"]:
        print("[*] Đang thực hiện kiểm tra toàn diện: Canon, Nhận thức nhân vật, Dòng thời gian và Logic vũ trụ...")
        tests = run_all_narrative_tests()
        if tests["passed"]:
            print(f"[+] HỆ THỐNG TOÀN VẸN TUYỆT ĐỐI! Đã vượt qua toàn bộ {tests['total']} bài kiểm thử logic tự sự.")
        else:
            print(f"[-] PHÁT HIỆN LỖI LOGIC: {tests['failures']} trường hợp vi phạm, {tests['errors']} lỗi hệ thống.")
            print(tests["output"])

    elif args.command in ["xuat-word", "export-word"]:
        print(f"[*] Đang xuất file Word cho Chương {args.chapter}...")
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter)
        print(f"[+] ĐÃ XUẤT THÀNH CÔNG TỆP WORD: {res['docx_path']}")

    elif args.command == "canon":
        c_eng = CanonEngine()
        entries = c_eng.list_all_canon()
        print(f"=== DANH MỤC THIẾT LẬP CANON ({len(entries)} mục) ===")
        for e in entries:
            print(f"- [{e['level']}] {e['title']} (Mã: {e['key']})")
            print(f"  Nội dung: {e['content']}\n")

    elif args.command in ["nhan-vat", "characters"]:
        char_eng = CharacterEngine()
        for cid in ["char_minh_an", "char_lam_tich"]:
            c = char_eng.get_character(cid)
            st = c.get("latest_state", {})
            print(f"=== {c['name']} (Mã: {c['id']}) ===")
            print(f"  Trạng thái sống:    {c['status']}")
            print(f"  Cảnh giới tu luyện: {st.get('cultivation_realm')}")
            print(f"  Vị trí hiện tại:    {st.get('location_id')}")
            print(f"  Trạng thái tâm lý:  {st.get('emotional_state')}")
            print(f"  Thương tích:        {', '.join(st.get('injuries', [])) if st.get('injuries') else 'Không có'}")
            print(f"  Túi đồ mang theo:   {', '.join(st.get('inventory', [])) if st.get('inventory') else 'Rỗng'}\n")

    elif args.command in ["thoi-gian", "timeline"]:
        t_eng = TimelineEngine()
        evts = t_eng.get_events()
        print(f"=== DÒNG THỜI GIAN CÁC SỰ KIỆN ({len(evts)} sự kiện) ===")
        for e in evts:
            print(f"- [{e['absolute_time']}] Chương {e['chapter_num']}: {e['title']}")
            print(f"  Nhân vật tham gia: {', '.join(e['participants'])}")
            print(f"  Tóm tắt diễn biến: {e['summary']}")
            print(f"  Kết quả sự kiện:   {e['outcome']}\n")

    elif args.command in ["the-gioi", "world"]:
        w_eng = WorldEngine()
        nodes = w_eng.list_nodes()
        print(f"=== PHÂN TẦNG VŨ TRỤ (COSMOLOGY) & BẢN ĐỒ VỊ DIỆN ===")
        for n in nodes:
            print(f"[Tầng {n['rank']}: {n['rank_name']}] {n['name']}")
            print(f"  Hệ thống tu luyện: {n['cultivation_system']}")
            print(f"  Trạng thái:        {n['status']}")
            print(f"  Mô tả:             {n['description']}\n")

    elif args.command in ["phuc-but", "foreshadowing"]:
        f_eng = ForeshadowingEngine()
        seeds = f_eng.list_seeds()
        print(f"=== SỔ CÁI PHỤC BÚT & CHEKHOV'S GUN ({len(seeds)} hạt mầm) ===")
        for s in seeds:
            print(f"- [{s['status']}] Mã: {s['id']} (Gieo ở Chương {s['planted_chapter']})")
            print(f"  Hạt mầm:         {s['seed_description']}")
            print(f"  Bản chất thật:   {s['actual_meaning']}")
            print(f"  Dự kiến thu hồi: Chương {s['payoff_chapter'] or 'Chưa xác định'}\n")

    elif args.command in ["de-xuat", "proposals"]:
        p_mgr = ProposalManager()
        props = p_mgr.list_proposals()
        print(f"=== DANH SÁCH ĐỀ XUẤT CANON ({len(props)} đề xuất) ===")
        if not props:
            print("Hiện tại không có đề xuất nào cần phê duyệt. Mọi quy tắc Canon đều đang ở trạng thái khóa bảo vệ.\n")
        for p in props:
            print(f"- [{p['status']}] {p['title']} (Mã: {p['id']})")
            print(f"  Chi tiết: {p['description']}")
            print(f"  Mức độ rủi ro: {p['risk']}\n")

    elif args.command in ["duyet", "approve"]:
        p_mgr = ProposalManager()
        p_mgr.approve_proposal(args.id)
        print(f"[+] ĐÃ PHÊ DUYỆT ĐỀ XUẤT: {args.id}")

    elif args.command in ["tu-choi", "reject"]:
        p_mgr = ProposalManager()
        p_mgr.reject_proposal(args.id)
        print(f"[+] ĐÃ TỪ CHỐI ĐỀ XUẤT: {args.id}")

    elif args.command in ["kiem-thu", "test"]:
        res = run_all_narrative_tests()
        print(res["output"])
        print(f"Kết quả kiểm thử: {'ĐẠT CHUẨN' if res['passed'] else 'THẤT BẠI'} (Tổng cộng {res['total']} bài kiểm tra)")

    elif args.command in ["tiet-kiem", "telemetry", "token-metrics"]:
        t_eng = TelemetryEngine()
        metrics = t_eng.get_summary_metrics()
        print("=== BÁO CÁO VIỄN TRẮC & TỐI ƯU HÓA TOKEN (NOVEL OS TELEMETRY) ===")
        print(f"  Tổng sự kiện ghi nhận:          {metrics['total_events']:,}")
        print(f"  Tổng token gửi LLM (ước tính):  {metrics['total_tokens_in']:,}")
        print(f"  Tổng token tiết kiệm được:      {metrics['total_tokens_saved']:,}")
        print(f"  Tỷ lệ nén / tiết kiệm:          {metrics['compression_percentage']}%")
        print(f"  Thao tác tất định bằng mã:      {metrics['deterministic_ops_count']:,} lần")
        print(f"  Tỷ lệ Cache Hit:                {metrics['cache_hit_ratio']}%")
        print("\n--- Chi tiết theo nhóm tác vụ ---")
        for brk in metrics.get("breakdown", []):
            print(f"  - [{brk['task_type']} / {brk['model_tier']}]: {brk['count']} lần | Tiết kiệm: {brk['saved']:,} tokens | Tất định: {brk['ops']:,} ops")
        print()

    elif args.command in ["tim-kiem", "search", "memory-search"]:
        r_eng = RetrievalEngine()
        doc_types = [args.type] if getattr(args, 'type', None) else None
        results = r_eng.search(args.query, doc_types=doc_types, top_k=args.limit)
        print(f"=== KẾT QUẢ TÌM KIẾM TRÍ NHỚ (FTS5 BM25) CHO: '{args.query}' ===")
        if not results:
            print("  Không tìm thấy kết quả phù hợp.\n")
        else:
            for idx, res in enumerate(results, 1):
                print(f"{idx}. [{res['doc_type']}] {res['title']} (Điểm phù hợp: {res['score']:.2f})")
                print(f"   Thẻ: {res['tags']}")
                print(f"   Nội dung: {res['content'][:250]}...\n")

    elif args.command in ["studio", "serve"]:
        from system.web.app import run_server
        run_server()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
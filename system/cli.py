import sys

# Kh?i t?o m? h?a UTF-8 cho console ti?ng Vi?t
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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

def main():
    verify_novel_lock()
    parser = argparse.ArgumentParser(
        prog="NovelOS",
        description="NOVEL OS ? H? ?I?U H?NH S?NG T?C TI?U THUY?T 'PH? TR?I'",
        epilog="Chuy?n d?ng cho ti?u thuy?t tr??ng thi?n 2.000+ ch??ng. Quy?n t?i cao thu?c v? Author."
    )
    subparsers = parser.add_subparsers(dest="command", help="Danh s?ch l?nh v?n h?nh h? th?ng")

    # viet-tiep (write-next)
    p_write = subparsers.add_parser("viet-tiep", aliases=["write-next"], help="T? ??ng vi?t ti?p ch??ng m?i theo ??ng Canon v? Continuity")
    p_write.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="S? th? t? ch??ng c?n s?ng t?c (m?c ??nh: 1)")
    p_write.add_argument("--pov", type=str, default="Nguy?n Minh An (Ng?i th? nh?t)", help="G?c nh?n ng??i k? (POV)")

    # viet-lai (rewrite)
    p_rewrite = subparsers.add_parser("viet-lai", aliases=["rewrite"], help="So?n l?i ch??ng theo ??nh h??ng m?i")
    p_rewrite.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="S? th? t? ch??ng c?n vi?t l?i")

    # kiem-tra (audit)
    subparsers.add_parser("kiem-tra", aliases=["audit", "check"], help="Ki?m tra to?n di?n t?nh nh?t qu?n, Canon, D?ng th?i gian v? Logic t? s?")

    # xuat-word (export-word)
    p_export = subparsers.add_parser("xuat-word", aliases=["export-word"], help="Bi?n d?ch b?n th?o ra ??nh d?ng Word (.docx) chu?n in ?n")
    p_export.add_argument("--chuong", "--chapter", type=int, default=1, dest="chapter", help="Ch??ng c?n xu?t")

    # canon
    subparsers.add_parser("canon", help="Tra c?u to?n b? danh m?c quy t?c, ti?n ?? v? thi?t l?p Canon ?? kh?a")

    # nhan-vat (characters)
    subparsers.add_parser("nhan-vat", aliases=["characters"], help="Tra c?u h? s?, th? tr?ng, th??ng t?n, c?nh gi?i v? t?i ?? nh?n v?t")

    # thoi-gian (timeline)
    subparsers.add_parser("thoi-gian", aliases=["timeline"], help="Xem d?ng th?i gian c?c s? ki?n tuy?t ??i v? t??ng ??i")

    # the-gioi (world)
    subparsers.add_parser("the-gioi", aliases=["world"], help="Xem ph?n t?ng th? gi?i (Cosmology) v? b?n ?? c?c v? di?n")

    # phuc-but (foreshadowing)
    subparsers.add_parser("phuc-but", aliases=["foreshadowing"], help="Xem s? c?i ph?c b?t v? c?c h?t m?m Chekhov's Gun")

    # de-xuat (proposals)
    subparsers.add_parser("de-xuat", aliases=["proposals"], help="Xem danh s?ch ?? xu?t thay ??i Canon ?ang ch? Author duy?t")

    # duyet (approve)
    p_app = subparsers.add_parser("duyet", aliases=["approve"], help="Ph? duy?t ?? xu?t thay ??i Canon")
    p_app.add_argument("id", type=str, help="M? ??nh danh ?? xu?t (Proposal ID)")

    # tu-choi (reject)
    p_rej = subparsers.add_parser("tu-choi", aliases=["reject"], help="T? ch?i ?? xu?t thay ??i Canon")
    p_rej.add_argument("id", type=str, help="M? ??nh danh ?? xu?t (Proposal ID)")

    # kiem-thu (test)
    subparsers.add_parser("kiem-thu", aliases=["test"], help="Ch?y b? ki?m th? t? ??ng 21 t?nh hu?ng narrative logic")

    # studio (serve)
    subparsers.add_parser("studio", aliases=["serve"], help="Kh?i ??ng giao di?n Novel OS Web Studio tr?c quan")

    args = parser.parse_args()

    if args.command in ["viet-tiep", "write-next"]:
        print(f"[*] ?ang k?ch ho?t chu tr?nh 'Vi?t ti?p' cho Ch??ng {args.chapter}...")
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter, pov=args.pov)
        if res["success"]:
            print(f"[+] S?NG T?C TH?NH C?NG CH??NG {res['chapter_num']}!")
            print(f"    - T?p Markdown g?c: {res['md_path']}")
            print(f"    - T?p Word in ?n:  {res['docx_path']}")
            print(f"    - T?ng s? t?:      {res['word_count']} t?")
            print(f"    - T? ph?n bi?n:    {res['critique']['total_issues']} l?u ? nh? (H? th?ng ?? t? chu?n h?a).")
        else:
            print(f"[-] Kh?ng th? ho?n t?t ch??ng: {res['reason']}")
            for iss in res.get("issues", []):
                print(f"    ! [{iss['severity']}] {iss['category']}: {iss['description']}")

    elif args.command in ["kiem-tra", "audit", "check"]:
        print("[*] ?ang th?c hi?n ki?m tra to?n di?n: Canon, Nh?n th?c nh?n v?t, D?ng th?i gian v? Logic v? tr?...")
        tests = run_all_narrative_tests()
        if tests["passed"]:
            print(f"[+] H? TH?NG TO?N V?N TUY?T ??I! ?? v??t qua to?n b? {tests['total']} b?i ki?m th? logic t? s?.")
        else:
            print(f"[-] PH?T HI?N L?I LOGIC: {tests['failures']} tr??ng h?p vi ph?m, {tests['errors']} l?i h? th?ng.")
            print(tests["output"])

    elif args.command in ["xuat-word", "export-word"]:
        print(f"[*] ?ang xu?t file Word cho Ch??ng {args.chapter}...")
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter)
        print(f"[+] ?? XU?T TH?NH C?NG T?P WORD: {res['docx_path']}")

    elif args.command == "canon":
        c_eng = CanonEngine()
        entries = c_eng.list_all_canon()
        print(f"=== DANH M?C THI?T L?P CANON ({len(entries)} m?c) ===")
        for e in entries:
            print(f"? [{e['level']}] {e['title']} (M?: {e['key']})")
            print(f"  N?i dung: {e['content']}\\n")

    elif args.command in ["nhan-vat", "characters"]:
        char_eng = CharacterEngine()
        for cid in ["char_minh_an", "char_lam_tich"]:
            c = char_eng.get_character(cid)
            st = c.get("latest_state", {})
            print(f"=== {c['name']} (M?: {c['id']}) ===")
            print(f"  Tr?ng th?i s?ng: {c['status']}")
            print(f"  C?nh gi?i tu luy?n: {st.get('cultivation_realm')}")
            print(f"  V? tr? hi?n t?i:   {st.get('location_id')}")
            print(f"  Tr?ng th?i t?m l?: {st.get('emotional_state')}")
            print(f"  Th??ng t?ch:       {', '.join(st.get('injuries', [])) if st.get('injuries') else 'Kh?ng c?'}")
            print(f"  T?i ?? mang theo:  {', '.join(st.get('inventory', [])) if st.get('inventory') else 'R?ng'}\\n")

    elif args.command in ["thoi-gian", "timeline"]:
        t_eng = TimelineEngine()
        evts = t_eng.get_events()
        print(f"=== D?NG TH?I GIAN C?C S? KI?N ({len(evts)} s? ki?n) ===")
        for e in evts:
            print(f"? [{e['absolute_time']}] Ch??ng {e['chapter_num']}: {e['title']}")
            print(f"  Nh?n v?t: {', '.join(e['participants'])}")
            print(f"  Di?n bi?n: {e['summary']}")
            print(f"  K?t qu?:   {e['outcome']}\\n")

    elif args.command in ["the-gioi", "world"]:
        w_eng = WorldEngine()
        nodes = w_eng.list_nodes()
        print(f"=== PH?N T?NG V? TR? (COSMOLOGY) & B?N ?? V? DI?N ===")
        for n in nodes:
            print(f"[T?ng {n['rank']}: {n['rank_name']}] {n['name']}")
            print(f"  H? th?ng tu luy?n: {n['cultivation_system']}")
            print(f"  Tr?ng th?i:        {n['status']}")
            print(f"  M? t?:             {n['description']}\\n")

    elif args.command in ["phuc-but", "foreshadowing"]:
        f_eng = ForeshadowingEngine()
        seeds = f_eng.list_seeds()
        print(f"=== S? C?I PH?C B?T & CHEKHOV'S GUN ({len(seeds)} h?t m?m) ===")
        for s in seeds:
            print(f"? [{s['status']}] M?: {s['id']} (Gieo ? Ch??ng {s['planted_chapter']})")
            print(f"  H?t m?m:        {s['seed_description']}")
            print(f"  B?n ch?t th?t:  {s['actual_meaning']}")
            print(f"  D? ki?n thu h?i: Ch??ng {s['payoff_chapter'] or 'Ch?a x?c ??nh'}\\n")

    elif args.command in ["de-xuat", "proposals"]:
        p_mgr = ProposalManager()
        props = p_mgr.list_proposals()
        print(f"=== DANH S?CH ?? XU?T CANON ({len(props)} ?? xu?t) ===")
        if not props:
            print("Hi?n t?i kh?ng c? ?? xu?t n?o c?n ph? duy?t. M?i quy t?c Canon ??u ?ang ? tr?ng th?i kh?a b?o v?.\\n")
        for p in props:
            print(f"? [{p['status']}] {p['title']} (M?: {p['id']})")
            print(f"  Chi ti?t: {p['description']}")
            print(f"  M?c ?? r?i ro: {p['risk']}\\n")

    elif args.command in ["duyet", "approve"]:
        p_mgr = ProposalManager()
        p_mgr.approve_proposal(args.id)
        print(f"[+] ?? PH? DUY?T ?? XU?T: {args.id}")

    elif args.command in ["tu-choi", "reject"]:
        p_mgr = ProposalManager()
        p_mgr.reject_proposal(args.id)
        print(f"[+] ?? T? CH?I ?? XU?T: {args.id}")

    elif args.command in ["kiem-thu", "test"]:
        res = run_all_narrative_tests()
        print(res["output"])
        print(f"K?t qu? ki?m th?: {'??T CHU?N' if res['passed'] else 'TH?T B?I'} (T?ng c?ng {res['total']} b?i ki?m tra)")

    elif args.command in ["studio", "serve"]:
        from system.web.app import run_server
        run_server()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

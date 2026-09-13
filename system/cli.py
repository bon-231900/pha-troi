import argparse
import sys
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
    parser = argparse.ArgumentParser(description="Novel OS ? H? ?i?u H?nh S?ng T?c Ti?u Thuy?t Ph? Tr?i")
    subparsers = parser.add_subparsers(dest="command", help="L?nh v?n h?nh")

    # write-next
    p_write = subparsers.add_parser("write-next", help="Vi?t ti?p ch??ng ti?p theo t? ??ng")
    p_write.add_argument("--chapter", type=int, default=1, help="S? th? t? ch??ng")
    p_write.add_argument("--pov", type=str, default="Nguy?n Minh An (First Person)", help="G?c nh?n (POV)")

    # rewrite
    p_rewrite = subparsers.add_parser("rewrite", help="Vi?t l?i ch??ng theo ch? ??nh")
    p_rewrite.add_argument("--chapter", type=int, default=1, help="S? th? t? ch??ng")

    # audit / check
    p_audit = subparsers.add_parser("audit", help="Ki?m tra t?nh li?n t?c, canon v? logic t? s?")

    # export-word
    p_export = subparsers.add_parser("export-word", help="Xu?t b?n th?o ra ??nh d?ng Word (.docx)")
    p_export.add_argument("--chapter", type=int, default=1, help="Ch??ng c?n xu?t (ho?c xu?t c? quy?n)")

    # canon
    subparsers.add_parser("canon", help="Xem danh s?ch lu?t v? s? ki?n Canon")

    # characters
    subparsers.add_parser("characters", help="Xem danh s?ch tr?ng th?i nh?n v?t")

    # timeline
    subparsers.add_parser("timeline", help="Xem d?ng th?i gian c?c s? ki?n")

    # world
    subparsers.add_parser("world", help="Xem ?? th? ph?n t?ng th? gi?i & cosmology")

    # foreshadowing
    subparsers.add_parser("foreshadowing", help="Xem danh m?c ph?c b?t Chekhov's Gun")

    # proposals
    subparsers.add_parser("proposals", help="Xem danh s?ch ?? xu?t thay ??i canon")

    # approve / reject
    p_app = subparsers.add_parser("approve", help="Ph? duy?t ?? xu?t")
    p_app.add_argument("id", type=str, help="Proposal ID")

    p_rej = subparsers.add_parser("reject", help="T? ch?i ?? xu?t")
    p_rej.add_argument("id", type=str, help="Proposal ID")

    # test
    subparsers.add_parser("test", help="Ch?y b? ki?m th? 21 narrative tests")

    # serve
    subparsers.add_parser("serve", help="Kh?i ??ng Novel OS Web Studio c?c b?")

    args = parser.parse_args()

    if args.command == "write-next":
        print(f"[*] ?ang th?c thi h?p ??ng 'Vi?t ti?p' cho Ch??ng {args.chapter}...")
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter, pov=args.pov)
        if res["success"]:
            print(f"[+] Vi?t th?nh c?ng Ch??ng {res['chapter_num']}!")
            print(f"    - Markdown: {res['md_path']}")
            print(f"    - Word: {res['docx_path']}")
            print(f"    - S? t?: {res['word_count']}")
            print(f"    - Critique: {res['critique']['total_issues']} c?nh b?o nh? (?? t? ??ng x? l?).")
        else:
            print(f"[-] L?i khi vi?t ti?p: {res['reason']}")
            for iss in res.get("issues", []):
                print(f"    ! [{iss['severity']}] {iss['category']}: {iss['description']}")

    elif args.command == "audit":
        print("[*] ?ang ki?m tra to?n di?n Canon, Timeline, Knowledge v? Nh?n v?t...")
        tests = run_all_narrative_tests()
        if tests["passed"]:
            print(f"[+] H? TH?NG TO?N V?N TUY?T ??I: V??t qua to?n b? {tests['total']} ki?m th? logic!")
        else:
            print(f"[-] PH?T HI?N L?I: {tests['failures']} th?t b?i, {tests['errors']} l?i.")
            print(tests["output"])

    elif args.command == "export-word":
        coauthor = CoAuthorEngine()
        res = coauthor.write_next_chapter(target_chapter_num=args.chapter)
        print(f"[+] ?? xu?t file Word: {res['docx_path']}")

    elif args.command == "canon":
        c_eng = CanonEngine()
        entries = c_eng.list_all_canon()
        print(f"=== DANH M?C CANON ({len(entries)} m?c) ===")
        for e in entries:
            print(f"- [{e['level']}] {e['title']} ({e['key']}): {e['content']}")

    elif args.command == "characters":
        char_eng = CharacterEngine()
        for cid in ["char_minh_an", "char_lam_tich"]:
            c = char_eng.get_character(cid)
            st = c.get("latest_state", {})
            print(f"=== {c['name']} ({c['id']}) ===")
            print(f"  Tr?ng th?i: {c['status']}")
            print(f"  C?nh gi?i: {st.get('cultivation_realm')}")
            print(f"  V? tr?: {st.get('location_id')}")
            print(f"  T?m l?: {st.get('emotional_state')}")
            print(f"  Th??ng t?ch: {st.get('injuries')}")
            print(f"  T?i ??: {st.get('inventory')}")

    elif args.command == "timeline":
        t_eng = TimelineEngine()
        evts = t_eng.get_events()
        print(f"=== D?NG TH?I GIAN ({len(evts)} s? ki?n) ===")
        for e in evts:
            print(f"- [{e['absolute_time']}] Ch.{e['chapter_num']}: {e['title']} -> {e['summary']}")

    elif args.command == "world":
        w_eng = WorldEngine()
        nodes = w_eng.list_nodes()
        print(f"=== C?U TR?C COSMOLOGY & B?N ?? TH? GI?I ===")
        for n in nodes:
            print(f"[{n['rank']}] {n['name']} ({n['rank_name']}) | H? th?ng: {n['cultivation_system']} | Tr?ng th?i: {n['status']}")

    elif args.command == "foreshadowing":
        f_eng = ForeshadowingEngine()
        seeds = f_eng.list_seeds()
        print(f"=== CHEKHOV'S GUN & PH?C B?T ({len(seeds)} h?t m?m) ===")
        for s in seeds:
            print(f"- [{s['status']}] (ID: {s['id']}) Ch.{s['planted_chapter']} -> Payoff Ch.{s['payoff_chapter']}: {s['seed_description']}")

    elif args.command == "proposals":
        p_mgr = ProposalManager()
        props = p_mgr.list_proposals()
        print(f"=== DANH S?CH ?? XU?T CANON ({len(props)} ?? xu?t) ===")
        for p in props:
            print(f"- [{p['status']}] (ID: {p['id']}) {p['title']}: {p['description']}")

    elif args.command == "approve":
        p_mgr = ProposalManager()
        p_mgr.approve_proposal(args.id)
        print(f"[+] ?? ph? duy?t ?? xu?t {args.id}.")

    elif args.command == "reject":
        p_mgr = ProposalManager()
        p_mgr.reject_proposal(args.id)
        print(f"[+] ?? t? ch?i ?? xu?t {args.id}.")

    elif args.command == "test":
        res = run_all_narrative_tests()
        print(res["output"])
        print(f"K?t qu?: {res['passed']} (T?ng c?ng {res['total']} tests)")

    elif args.command == "serve":
        from system.web.app import run_server
        run_server()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

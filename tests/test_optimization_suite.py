# -*- coding: utf-8 -*-
import unittest
import os
import sys
import json
import sqlite3

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

from system.core.config import DB_PATH, ROOT_DIR, MANUSCRIPT_MD_DIR
from system.core.router import TaskRouter, TaskTier
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.telemetry_engine import TelemetryEngine
from system.engines.context_builder import ContextBuilder
from system.engines.critique_engine import CritiqueEngine
from system.engines.research_vault import ResearchVault
from tests.test_base import IsolatedDatabaseTestCase

class TestOptimizationSuite(IsolatedDatabaseTestCase):
    def setUp(self):
        super().setUp()
        self.router = TaskRouter()
        self.retrieval = RetrievalEngine(self.db_path)
        self.telemetry = TelemetryEngine(self.db_path)
        self.context_builder = ContextBuilder(self.db_path)
        self.critique = CritiqueEngine(self.db_path)
        self.vault = ResearchVault(self.db_path)

    def test_01_task_router_tier_classification(self):
        self.assertEqual(TaskRouter.classify('continuity_audit'), TaskTier.DETERMINISTIC)
        self.assertTrue(TaskRouter.is_deterministic('continuity_audit'))
        self.assertFalse(TaskRouter.requires_llm('continuity_audit'))

        self.assertEqual(TaskRouter.classify('fts5_search'), TaskTier.DETERMINISTIC)
        self.assertTrue(TaskRouter.is_deterministic('fts5_search'))

        self.assertEqual(TaskRouter.classify('docx_export'), TaskTier.MECHANICAL)
        self.assertTrue(TaskRouter.is_deterministic('docx_export'))

        self.assertEqual(TaskRouter.classify('macro_plot_planning'), TaskTier.HIGH_REASONING)
        self.assertTrue(TaskRouter.requires_llm('macro_plot_planning'))

        self.assertEqual(TaskRouter.classify('chapter_writing'), TaskTier.CRITICAL_CREATIVE)
        profile = TaskRouter.get_routing_profile('chapter_writing')
        self.assertEqual(profile['recommended_model'], 'pro')
        self.assertEqual(profile['token_cost_policy'], 'QUALITY_FIRST')

    def test_02_fts5_bm25_retrieval_accuracy(self):
        results = self.retrieval.search('Ung Van Khiem', doc_types=['chapter_scene'], top_k=3)
        self.assertGreater(len(results), 0)
        self.assertGreater(results[0]['score'], 0)

        lore_results = self.retrieval.search('Đạo cơ', doc_types=['canon'], top_k=2)
        self.assertGreater(len(lore_results), 0)
        self.assertEqual(lore_results[0]['doc_type'], 'canon')

    def test_03_incremental_indexing_dirty_checking(self):
        test_ch = os.path.join(MANUSCRIPT_MD_DIR, 'volume_01', 'arc_01', 'ch_001.md')
        if os.path.exists(test_ch):
            count_1 = self.retrieval.index_chapter(test_ch)
            count_2 = self.retrieval.index_chapter(test_ch)
            self.assertEqual(count_2, 0)

    def test_04_adaptive_context_pack_compression(self):
        pack = self.context_builder.build_context_pack(
            chapter_num=4,
            pov='Nguyễn Minh An (Ngôi thứ nhất)',
            active_characters=['char_minh_an', 'char_lam_tich'],
            location_id='loc_hcmc',
            scene_objective='Minh An đi làm buổi sáng trong trạng thái thiếu ngủ'
        )
        self.assertIn('style_constraints', pack)
        self.assertIn('character_states', pack)
        self.assertIn('epistemic_knowledge', pack)
        self.assertIn('active_foreshadowing', pack)
        self.assertIn('recent_events', pack)
        self.assertIn('relevant_past_excerpts', pack)

        pack_text = json.dumps(pack, ensure_ascii=False)
        word_count = len(pack_text.split())
        self.assertLess(word_count, 2500)

    def test_05_deterministic_critique_continuity_audits(self):
        audit_typo = self.critique.audit_chapter_draft(1, 'Minh An', ['char_minh_an'], 'Minh Ánh đi làm tại cơ quan')
        has_typo_issue = any('Minh Ánh' in i['description'] for i in audit_typo['issues'])
        self.assertTrue(has_typo_issue)

        audit_inv = self.critique.audit_chapter_draft(1, 'Minh An', ['char_lam_tich'], 'Lâm Tịch cầm Thần kiếm nguyên vẹn')
        has_inv_issue = any('vật phẩm' in i['category'].lower() or 'kiếm' in i['description'].lower() for i in audit_inv['issues'])
        self.assertTrue(has_inv_issue)

    def test_06_research_vault_caching_and_deduplication(self):
        topic = 'Sai Gon ngap nuoc Ung Van Khiem 2026'
        self.vault.add_research_item(
            item_id='RS-TEST-01',
            topic=topic,
            source='Khao sat do thi',
            date='2026-09-13',
            summary='Ung Van Khiem ngap nuoc sau con mua rao thang 9.'
        )
        cached = self.vault.find_cached_research(topic)
        self.assertGreater(len(cached), 0)
        self.assertIn('ngap nuoc', cached[0]['summary'])

    def test_07_telemetry_engine_accounting(self):
        self.telemetry.record_event(
            task_type='UNIT_TEST_OPTIMIZATION',
            model_tier='DETERMINISTIC',
            tokens_in_est=100,
            tokens_out_est=0,
            tokens_saved_est=5000,
            deterministic_ops_count=10,
            cache_hit=True,
            description='Kiem thu telemetry'
        )
        stats = self.telemetry.get_summary_stats()
        self.assertGreaterEqual(stats['total_events'], 1)
        self.assertGreaterEqual(stats['total_tokens_saved'], 5000)
        self.assertGreater(stats['compression_rate_percent'], 50.0)
        self.assertGreaterEqual(stats['total_deterministic_ops'], 10)

if __name__ == '__main__':
    unittest.main()

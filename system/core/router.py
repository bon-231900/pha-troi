# -*- coding: utf-8 -*-
from enum import Enum

class TaskTier(str, Enum):
    CRITICAL_CREATIVE = "CRITICAL_CREATIVE"       # Sáng tác văn xuôi, nhịp điệu, cảm xúc (Mô hình cao nhất)
    HIGH_REASONING = "HIGH_REASONING"             # Lập dàn ý vĩ mô, phê duyệt đề xuất Canon lớn
    STRUCTURED_REASONING = "STRUCTURED_REASONING" # Giải quyết xung đột continuity mập mờ
    MECHANICAL = "MECHANICAL"                     # Xuất file Word, commit Git, định dạng Markdown
    DETERMINISTIC = "DETERMINISTIC"               # Tìm kiếm FTS5, kiểm tra nhân vật, kiểm tra mốc thời gian

TASK_ROUTING_MAP = {
    "chapter_writing": TaskTier.CRITICAL_CREATIVE,
    "chapter_rewrite": TaskTier.CRITICAL_CREATIVE,
    "scene_expansion": TaskTier.CRITICAL_CREATIVE,

    "macro_plot_planning": TaskTier.HIGH_REASONING,
    "canon_proposal_evaluation": TaskTier.HIGH_REASONING,
    "world_expansion_proposal": TaskTier.HIGH_REASONING,

    "ambiguous_continuity_resolution": TaskTier.STRUCTURED_REASONING,
    "complex_dialogue_refinement": TaskTier.STRUCTURED_REASONING,

    "docx_export": TaskTier.MECHANICAL,
    "git_commit": TaskTier.MECHANICAL,
    "markdown_cleaning": TaskTier.MECHANICAL,

    "continuity_audit": TaskTier.DETERMINISTIC,
    "fts5_search": TaskTier.DETERMINISTIC,
    "entity_lookup": TaskTier.DETERMINISTIC,
    "knowledge_check": TaskTier.DETERMINISTIC,
    "timeline_monotonicity": TaskTier.DETERMINISTIC,
    "inventory_check": TaskTier.DETERMINISTIC,
    "telemetry_record": TaskTier.DETERMINISTIC,
    "research_cache_lookup": TaskTier.DETERMINISTIC
}

class TaskRouter:
    """Bộ điều phối tác vụ và mô hình thông minh.
    Đảm bảo 100% các tác vụ cơ học/tra cứu chạy bằng code địa phương (0 token),
    và chỉ dành tài nguyên mô hình cao cấp nhất cho sáng tác văn học nghệ thuật.
    """

    @staticmethod
    def classify(task_name: str) -> TaskTier:
        return TASK_ROUTING_MAP.get(task_name.lower(), TaskTier.STRUCTURED_REASONING)

    @staticmethod
    def requires_llm(task_name: str) -> bool:
        tier = TaskRouter.classify(task_name)
        return tier in (TaskTier.CRITICAL_CREATIVE, TaskTier.HIGH_REASONING, TaskTier.STRUCTURED_REASONING)

    @staticmethod
    def is_deterministic(task_name: str) -> bool:
        tier = TaskRouter.classify(task_name)
        return tier in (TaskTier.DETERMINISTIC, TaskTier.MECHANICAL)

    @staticmethod
    def get_routing_profile(task_name: str) -> dict:
        tier = TaskRouter.classify(task_name)
        return {
            "task_name": task_name,
            "tier": tier.value,
            "requires_llm": TaskRouter.requires_llm(task_name),
            "recommended_model": "pro" if tier == TaskTier.CRITICAL_CREATIVE else ("flash" if tier == TaskTier.HIGH_REASONING else "flash_lite"),
            "token_cost_policy": "MAXIMUM_SAVINGS" if tier in (TaskTier.DETERMINISTIC, TaskTier.MECHANICAL) else "QUALITY_FIRST"
        }


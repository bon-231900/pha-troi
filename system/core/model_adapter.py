# -*- coding: utf-8 -*-
"""
Novel OS — Model Adapter Interface & Configuration Layer (system/core/model_adapter.py)
Trừu tượng hóa nhà cung cấp mô hình ngôn ngữ (LLM Provider Abstraction).
Tách biệt hoàn toàn tầng logic tự sự khỏi tên gọi cụ thể của từng model (pro, flash, gpt-4o, claude-3.5).
"""
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class ModelRequest:
    task_name: str
    tier: str
    prompt: str
    system_instruction: Optional[str] = ""
    temperature: float = 0.7
    max_tokens: int = 4000
    metadata: Dict = field(default_factory=dict)

@dataclass
class ModelResponse:
    content: str
    model_name: str
    provider_name: str
    tokens_in: int = 0
    tokens_out: int = 0
    finish_reason: str = "stop"

class ModelConfig:
    """Cấu hình ánh xạ Tier sang Model Name thông qua biến môi trường hoặc giá trị mặc định."""
    DEFAULT_MAPPINGS = {
        "CRITICAL_CREATIVE": os.getenv("NOVEL_MODEL_CREATIVE", "pro"),
        "HIGH_REASONING": os.getenv("NOVEL_MODEL_REASONING", "flash"),
        "STRUCTURED_REASONING": os.getenv("NOVEL_MODEL_STRUCTURED", "flash"),
        "DETERMINISTIC": "local-deterministic-engine",
        "MECHANICAL": "local-mechanical-engine"
    }

    @classmethod
    def get_model_for_tier(cls, tier: str) -> str:
        return cls.DEFAULT_MAPPINGS.get(tier, "default-tier")

class BaseModelProvider(ABC):
    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        pass

class MockDeterministicProvider(BaseModelProvider):
    """Provider mặc định chạy cục bộ, an toàn tuyệt đối, dùng cho kiểm thử và fallback ngoại tuyến."""
    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content=f"[DETERMINISTIC_MOCK_PROSE for {request.task_name}]",
            model_name=ModelConfig.get_model_for_tier(request.tier),
            provider_name="mock_deterministic",
            tokens_in=len(request.prompt.split()),
            tokens_out=50
        )

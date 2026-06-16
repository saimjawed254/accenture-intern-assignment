"""Shared diagnosis schema for the Week 2 LLM-only flow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FailureType(str, Enum):
    """Supported failure categories returned by the LLM."""

    DEPENDENCY = "dependency_error"
    TEST = "test_failure"
    CONFIG = "config_issue"
    OOM = "oom_error"
    NETWORK = "network_timeout"
    PERMISSION = "permission_denied"
    SECRET = "missing_secret"
    COMPILE = "compile_error"
    DISK = "disk_full"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class FailureDiagnosis:
    """Structured diagnosis payload returned to the CLI."""

    failure_type: FailureType
    confidence: str
    matched_pattern: str
    evidence: str
    root_cause: str
    fix_steps: tuple[str, ...]
    suggested_fix: str
    source: str = "gemini"
    raw_model_output: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize the diagnosis to JSON-friendly data."""

        return {
            "failure_type": self.failure_type.value,
            "confidence": self.confidence,
            "matched_pattern": self.matched_pattern,
            "evidence": self.evidence,
            "root_cause": self.root_cause,
            "fix_steps": list(self.fix_steps),
            "suggested_fix": self.suggested_fix,
            "source": self.source,
            "raw_model_output": self.raw_model_output,
        }
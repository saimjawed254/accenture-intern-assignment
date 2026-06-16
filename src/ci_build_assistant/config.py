"""Configuration loading for the Gemini-backed Week 2 flow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True, slots=True)
class GeminiSettings:
    """Runtime settings for Gemini access."""

    api_key: str | None
    model: str
    temperature: float
    timeout_seconds: float
    max_output_tokens: int


def load_settings(project_root: Path | None = None) -> GeminiSettings:
    """Load settings from `.env` and the current process environment."""

    root = project_root or Path.cwd()
    dotenv_path = root / ".env"
    _load_dotenv_file(dotenv_path)

    return GeminiSettings(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        temperature=_coerce_float(os.getenv("GEMINI_TEMPERATURE"), default=0.2),
        timeout_seconds=_coerce_float(os.getenv("GEMINI_TIMEOUT_SECONDS"), default=30.0),
        max_output_tokens=_coerce_int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS"), default=1024),
    )


def _load_dotenv_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _coerce_float(value: str | None, *, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def _coerce_int(value: str | None, *, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default
# AI-Powered CI/CD Build Assistant

Week 2 of the CI/CD build assistant is now wired for Gemini-backed structured diagnosis only.

## Current Status

- CLI accepts any log file path and reads build logs from disk.
- Gemini integration is the only analysis path when `GEMINI_API_KEY` is available.
- The CLI prints structured JSON diagnosis output followed by the raw log body.
- If the Gemini request fails or the JSON is invalid, the CLI prints the reason to `stderr` and exits non-zero.

## Runtime Files

The pushable runtime surface is intentionally small:

- `assistant.py` - CLI entrypoint
- `src/ci_build_assistant/parser.py` - log parsing
- `src/ci_build_assistant/schema.py` - shared diagnosis types
- `src/ci_build_assistant/config.py` - `.env` and environment loading
- `src/ci_build_assistant/prompts.py` - Gemini prompt templates
- `src/ci_build_assistant/llm_client.py` - Gemini REST client
- `src/ci_build_assistant/analysis.py` - orchestration and JSON parsing
- `src/ci_build_assistant/__init__.py` - package exports

The archived Week 1 classifier is stored under `unwanted/` for reference and is not part of the active runtime path.

Non-essential artifacts were moved into the ignored `unwanted/` folder.

## Environment Variables

Add these to your `.env` file at the repo root:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.2
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_OUTPUT_TOKENS=1024
```

If `GEMINI_API_KEY` is missing, the assistant exits with a clear configuration error.

## How To Run

```powershell
python assistant.py "C:\path\to\your\build.log"
```

## Output Shape

By default, the CLI prints a beautiful, emoji-enriched terminal report dashboard featuring:
- Log stats (character count, line count) and model name.
- Status badges for confidence level (🟢 HIGH, 🟡 MEDIUM, 🔴 UNCERTAIN).
- Sectioned details for **Failure Category**, **Root Cause**, **Evidence**, **Suggested Fix**, and numbered **Step-by-Step Recovery Actions**.
- The raw build log contents at the end.

If you specify the `--json` option, the CLI outputs a structured JSON diagnosis object (ideal for automation/integrations):
```powershell
python assistant.py "C:\path\to\your\build.log" --json
```

## Week 2 Status

- **Completed**: Gemini client with `.env` support.
- **Completed**: Structured JSON diagnosis contract.
- **Completed**: Direct Gemini-only diagnosis with explicit error reporting.
- **Completed**: Prompt templates and response parsing.
- **Completed**: Expanded failure coverage to 10 distinct categories.
- **Completed**: Redesigned CLI with user-friendly human-readable dashboard and `--json` fallback.
- **Completed**: Established offline-compatible unit/CLI test suites using mocks in `tests/`.
- **Next**: Start Week 3 to build the agentic loop (Reasoning & Action).
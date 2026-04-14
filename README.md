# moodle-agent-guardrails

An agent evaluation framework and guardrails layer for a multi-agent Moodle data extraction system. Built before the Argus coordination architecture — an early implementation of per-role access control and systematic agent performance evaluation.

## What This Is

The Moodle Calendar Sync project used five specialized OpenAI Agents SDK agents to extract course data, announcements, activities, and calendar events from a university Moodle instance. This repo contains the evaluation and safety layer: code for measuring how well each agent performed, and a guardrails module that gates what each agent is permitted to access.

The evaluation framework (`agent_evaluator.py`) was built because agent outputs weren't reliable enough to trust without measurement. Rather than doing spot-checks, the evaluator quantifies completeness, accuracy, and efficiency per agent — producing structured reports that make failure modes visible.

## Components

### `agent_evaluator.py` — Agent Performance Evaluator

Evaluates five agent types: `calendar_agent`, `course_agent`, `announcement_agent`, `activity_agent`, `triage_agent`.

**Metrics per agent:**
- **Completeness** (40% weight): `min(1.0, actual_count / expected_count)` — did the agent find everything?
- **Accuracy** (40% weight): item-level name matching between expected and actual output
- **Efficiency** (20% weight): items extracted per second, normalized against a 10 items/s baseline
- **Overall score**: weighted composite (0–1)

**Reports:** Timestamped JSON files with per-agent metrics, summary statistics, and text recommendations (`"agent X needs significant improvement"` / `"performing excellently"`).

```python
evaluator = AgentEvaluator()
evaluator.evaluate_agent_performance(
    "course_agent",
    expected_data=expected_courses,
    actual_data=extracted_courses,
    execution_time=3.2
)
report = evaluator.generate_evaluation_report()
evaluator.print_report_summary(report)
```

### `moodle_guardrails.py` — Access Control Layer

Guardrails that gate agent tool access by role. Each agent type is permitted a specific subset of Moodle data access tools — a `calendar_agent` cannot call course-extraction tools, and vice versa. Prevents agents from operating outside their defined scope.

### `moodle_tools.py` — Agent Tool Definitions

Tool definitions for the OpenAI Agents SDK. Includes structured schemas for Moodle data extraction operations, used by the agents to query course data, announcements, and calendar events.

## Architecture Context

This system used the OpenAI Agents SDK with five specialized agents running in a pipeline:

```
Moodle LMS
    │
    ├── course_agent      (extracts enrolled courses)
    ├── announcement_agent (extracts course announcements)
    ├── activity_agent    (extracts assignments + deadlines)
    ├── calendar_agent    (extracts calendar events)
    └── triage_agent      (routes and deduplicates)
         │
         └── Google Calendar API (writes events)
```

Each agent operated with constrained tool access (guardrails) and was evaluated independently after each extraction run.

## Why This Predates Argus

This system was built in January–March 2025, before the Argus coordination architecture. The patterns that emerged here — per-agent role constraints, systematic performance measurement, structured evaluation reports — directly informed the design of the Argus coordination layer's agent identity and audit systems.

The key lesson: agent outputs are not reliable without measurement infrastructure. The evaluator was not an afterthought; it was built because the first runs produced inconsistent results and there was no other way to know *which* agent was failing or *how badly*.

## Stack

- Python 3.11+
- OpenAI Agents SDK
- Playwright (browser automation for Moodle login)
- Google Calendar API

## Setup

```bash
pip install -r requirements.txt
```

Required environment variables (not committed — see `.env.example`):
```
OPENAI_API_KEY=
MOODLE_URL=
MOODLE_USERNAME=
MOODLE_PASSWORD=
GOOGLE_CREDENTIALS_PATH=
```

## Running Evaluations

```bash
# Run evaluation in mock mode (no real Moodle/Google credentials needed)
MOCK_LOGIN=true MOCK_CALENDAR_EVENTS=true python agent_evaluator.py

# Run full test suite
pytest tests/
```

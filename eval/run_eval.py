"""
Run the eval over eval_cases.json and print a pass-rate table.

STARTER skeleton. Fill in the TODOs, then:

    python eval/run_eval.py

Approach: send each case's input through your ChatService, then score the
output. LLM-as-judge is fine — give a judge model a clear rubric and ask for
a pass/fail (or 1–5). Keep the test set FIXED so you can compare changes.
"""

from __future__ import annotations

import json
import os
import sys

# Make the parent dir importable so we can reuse the backend.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_service import ChatService  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load_cases() -> list[dict]:
    with open(os.path.join(HERE, "eval_cases.json")) as f:
        return json.load(f)["cases"]


def judge(case: dict, answer: str) -> bool:
    """Return True if `answer` passes for `case`.

    TODO: implement. A good default is LLM-as-judge — call a model with a
    rubric like: "Given the question, the expected answer, and the actual
    answer, reply PASS or FAIL." Return True on PASS.
    """
    raise NotImplementedError("TODO: implement the judge")


def run_variant(label: str) -> None:
    cases = load_cases()
    service = ChatService()  # TODO: vary config per variant if comparing two
    passed = 0
    for case in cases:
        service.reset()
        answer = service.send(case["input"])
        ok = judge(case, answer)
        passed += int(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] case {case['id']}")
    total = len(cases)
    rate = (passed / total * 100) if total else 0
    print(f"\n{label}: {passed}/{total} passed ({rate:.0f}%)")


if __name__ == "__main__":
    # TODO: run at least two variants (different prompt/model/settings) and
    # paste the resulting pass-rate table into eval_results.md.
    run_variant("variant-A")

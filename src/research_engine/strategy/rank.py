"""Rank hypotheses with existing ExpectedResearchValue × FailureLearningValue."""

from __future__ import annotations

from typing import TYPE_CHECKING

from research_engine.diagnosis.corpus import ResearchCorpus
from research_engine.diagnosis.selection import score_candidate
from research_engine.diagnosis.types import CandidateSketch
from research_engine.memory.types import NoveltyStatus
from research_engine.strategy.types import ResearchHypothesis

if TYPE_CHECKING:
    from research_engine.memory.store import ResearchMemory


def rank_hypothesis(
    hypothesis: ResearchHypothesis,
    memory: ResearchMemory | None = None,
    corpus: ResearchCorpus | None = None,
) -> ResearchHypothesis:
    sketch = CandidateSketch(
        name=hypothesis.target or hypothesis.id,
        prior_art_classified=bool(hypothesis.prior_art_matches)
        or hypothesis.novelty_status is NoveltyStatus.KNOWN_REDISCOVERY,
        experimental_cost=1.0 if not hypothesis.candidate_attack_chain else float(
            len(hypothesis.candidate_attack_chain)
        ),
        claimed_capabilities=(),
        lean_certifiable=hypothesis.current_status.value == "LEAN_CERTIFIED",
    )
    report = score_candidate(sketch, corpus if corpus is not None else ResearchCorpus(), memory)
    from dataclasses import replace

    return replace(
        hypothesis,
        expected_value=report.value,
        failure_learning_value=report.failure_learning_value,
    )


def rank_hypotheses(
    hypotheses: tuple[ResearchHypothesis, ...] | list[ResearchHypothesis],
    memory: ResearchMemory | None = None,
    corpus: ResearchCorpus | None = None,
) -> tuple[ResearchHypothesis, ...]:
    ranked = tuple(rank_hypothesis(item, memory, corpus) for item in hypotheses)
    return tuple(sorted(ranked, key=lambda item: item.expected_value, reverse=True))

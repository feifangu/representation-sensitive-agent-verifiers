"""Forced-answer conditional likelihood scoring for causal language models."""

from __future__ import annotations

import math
from typing import Any

SUCCESS = "SUCCESS"
FAILURE = "FAILURE"


def verifier_messages(task_text: str, rendered_trajectory: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are an outcome verifier. Judge only whether the agent completed the given "
                "task using evidence in the trajectory. Do not reward confidence, style, or claims "
                "unsupported by tool observations. Your answer is exactly SUCCESS or FAILURE."
            ),
        },
        {
            "role": "user",
            "content": f"TASK\n{task_text}\n\nTRAJECTORY\n{rendered_trajectory}\n\nVERDICT",
        },
    ]


def normalized_success_score(success_loglik: float, failure_loglik: float) -> float:
    """Stable two-candidate normalization."""
    m = max(success_loglik, failure_loglik)
    success = math.exp(success_loglik - m)
    failure = math.exp(failure_loglik - m)
    return success / (success + failure)


def _answer_loglik(model: Any, tokenizer: Any, prompt_ids: Any, answer: str) -> float:
    """Teacher-force an answer plus EOS and sum its conditional token log-likelihood."""
    import torch

    answer_ids = tokenizer.encode(answer, add_special_tokens=False)
    if tokenizer.eos_token_id is not None:
        answer_ids = answer_ids + [tokenizer.eos_token_id]
    if not answer_ids:
        raise ValueError(f"answer tokenized to empty sequence: {answer!r}")
    continuation = torch.tensor([answer_ids], device=prompt_ids.device, dtype=prompt_ids.dtype)
    input_ids = torch.cat([prompt_ids, continuation], dim=1)
    with torch.inference_mode():
        logits = model(input_ids=input_ids).logits.float()
    start = prompt_ids.shape[1] - 1
    token_logits = logits[:, start : start + len(answer_ids), :]
    targets = continuation
    log_probs = torch.log_softmax(token_logits, dim=-1)
    return float(log_probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1).sum().item())


def score_messages(
    model: Any,
    tokenizer: Any,
    messages: list[dict[str, str]],
    chat_template_kwargs: dict[str, Any] | None = None,
    max_context_tokens: int = 0,
) -> dict[str, Any]:
    prompt_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt",
        **(chat_template_kwargs or {}),
    ).to(model.device)
    answer_lengths = [
        len(tokenizer.encode(answer, add_special_tokens=False)) + int(tokenizer.eos_token_id is not None)
        for answer in (SUCCESS, FAILURE)
    ]
    if max_context_tokens and prompt_ids.shape[1] + max(answer_lengths) > max_context_tokens:
        raise RuntimeError(
            f"context overflow: prompt={prompt_ids.shape[1]}, continuation={max(answer_lengths)}, "
            f"limit={max_context_tokens}"
        )
    success_ll = _answer_loglik(model, tokenizer, prompt_ids, SUCCESS)
    failure_ll = _answer_loglik(model, tokenizer, prompt_ids, FAILURE)
    return {
        "success_loglik": success_ll,
        "failure_loglik": failure_ll,
        "success_score": normalized_success_score(success_ll, failure_ll),
        "prompt_tokens": int(prompt_ids.shape[1]),
        "success_token_ids": tokenizer.encode(SUCCESS, add_special_tokens=False),
        "failure_token_ids": tokenizer.encode(FAILURE, add_special_tokens=False),
    }

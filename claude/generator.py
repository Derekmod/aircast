import os
import functools
from dataclasses import dataclass
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


@functools.lru_cache
def get_claude_key() -> str:
    return os.environ["CLAUDE_KEY"]


@dataclass
class Turn:
    user_message: str
    assistant_message: str | None


@dataclass
class Trajectory:
    # system_message
    turns: list[Turn]


def generate(
    trajectory: Trajectory,
    max_tokens_to_sample: int = 500,
    # TODO: inference params
) -> str:
    anthropic = Anthropic(
        api_key=get_claude_key(),
    )

    prompt = ""
    for turn_idx, turn in enumerate(trajectory.turns):
        prompt += f"{HUMAN_PROMPT} {turn.user_message}"
        if turn.assistant_message is not None:
            if turn_idx == len(trajectory.turns) - 1:
                raise ValueError("Cannot generate human messages!")
            prompt += f"{AI_PROMPT} {turn.assistant_message}"
        else:
            assert turn_idx == len(trajectory.turns) - 1
            prompt += f"{AI_PROMPT}"

    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=max_tokens_to_sample,
        prompt=prompt,
    )

    return completion.completion.lstrip()

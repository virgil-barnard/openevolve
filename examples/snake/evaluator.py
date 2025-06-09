"""
Evaluation entry-point for OpenEvolve.

OpenEvolve will import this module and call evaluate(program_path, config),
where program_path is the path to the candidate npc_player.py after patching
in the LLM-generated EVOLVE code.

We run N episodes with different seeds and return average score & length.
"""

import importlib.util
import statistics
from pathlib import Path
import sys
import os

# Ensure local modules like `game` and `player_base` can be imported when this
# file is loaded dynamically via ``importlib``. OpenEvolve loads the evaluation
# function using ``spec_from_file_location`` which does not automatically add
# the file's directory to ``sys.path``.
sys.path.insert(0, os.path.dirname(__file__))

from game import Game
from player_base import PlayerBase

EPISODES = 5   # increase for harder eval

def _load_player(candidate_file: Path) -> PlayerBase:
    spec = importlib.util.spec_from_file_location("npc_player", candidate_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EvolvedPlayer()

def evaluate(candidate_file, config=None):
    scores, lengths = [], []
    for seed in range(EPISODES):
        player = _load_player(Path(candidate_file))
        g = Game(rows=12, cols=12, max_steps=200)
        score, steps = g.play(player, seed=seed)
        scores.append(score)
        lengths.append(steps)

    return {
        "avg_score": statistics.mean(scores),
        "avg_steps": statistics.mean(lengths),
    }

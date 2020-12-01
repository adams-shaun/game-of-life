#!/usr/bin/python
"""Simple CLI util for executing game of life runs."""

import json
import enum
import argparse
import typing
import random

import life_lib


class RuleType(enum.Enum):
    classic = 'classic'
    highlife = 'highlife'

    @staticmethod
    def values():
        return [o.value for o in RuleType]


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", help="Number of rows in the grid",
                        type=int, default=25)
    parser.add_argument("-c", help="Number of columns in the grid",
                        type=int, default=25)
    parser.add_argument("-n", help="Number of steps to simulate",
                        type=int, default=100)
    parser.add_argument("-t", help="Game of life rules variant",
                        type=RuleType, choices=RuleType)
    parser.add_argument("--percent", help="Percentage of initial tiles with life.",
                        type=int, default=50)
    parser.add_argument('--infile', nargs='?',
                        help="JSON file of program inputs",
                        type=argparse.FileType('r'))

    args = parser.parse_args()

    return args


def make_random_distribution(height: int,
                             width: int,
                             percent_full: int,) -> typing.List[typing.Tuple[int, int]]:
    """This isn't perfect, just choose alive/dead on a per cell basis.
    Doesn't enforce actual distribution percentage, but given large enough board should be close.
    """
    alive_cells = []

    for y_idx in range(height):
        for x_idx in range(width):
            if random.random() < percent_full / 100:
                alive_cells.append((y_idx, x_idx))

    return alive_cells


def make_engine() -> life_lib.GameRunner:
    args = parse_args()

    input_data = dict()
    if args.infile:
        # with open(args.infile.buffer, 'r') as f:
        input_data = json.load(args.infile.buffer)

    height = input_data.get('height', None) or args.r
    width = input_data.get('width', None) or args.c
    num_steps = input_data.get('num_steps', None) or args.n
    initial_dist = input_data.get('initial_distribution', None) or make_random_distribution(height, width, args.percent)
    rules = life_lib.HighLifeRules if args.t == RuleType.highlife.value else life_lib.ClassicRules

    return life_lib.GameRunner(height, width, num_steps, initial_dist, rule_engine=rules)


if __name__ == '__main__':
    engine = make_engine()
    engine.execute()

"""
Solver for the secret santa problem:

Given a set of participants S_0...S_i

And a set of rules where participant S_i cannot give a gift to S_j

Determine the secret santa assignments for the participants.
"""

from dataclasses import dataclass
from json import load
from pathlib import Path
from typing import List, Tuple

from z3 import *


@dataclass
class SecretSantaConfig:
    """
    The rules of the secret santa problem (imported from json)

    Attributes:
        participants: The participants of the secret santa problem by name
        rules: The rules of the secret santa problem (by indices in participants list)
        assignments: The resultant assignments from the solution
    """

    participants: List[str]
    rules: List[List[int]]


class SecretSantaSolver:
    def __init__(self, rulefile: Path) -> None:
        """
        Initialize the secret santa solver with the rules from the given file

        :param rulefile: The path to the rules file
        """
        with rulefile.open("r") as f:
            self.config = SecretSantaConfig(**load(f))
            assert (
                len(self.config.participants) % 2 == 0
            ), "Number of participants must be even"

    def count_equals(self, elements: List[Int], equalto: Int) -> Int:
        """
        Get the count of elments in the list that are equal to the given element

        :param elements: The list of elements to count
        :param equalto: The element to count
        """
        return Sum(
            list(map(lambda i: If(elements[i] == equalto, 1, 0), range(len(elements))))
        )

    def solve(self) -> List[Tuple[str, str]]:
        """
        Solve the secret santa problem

        :return: The assignments of the participants
        """
        solver = Solver()
        num_groups = len(self.config.participants) // 2
        assignments = list(map(lambda g: Int(f"group_{g}"), range(num_groups)))

        for i in range(num_groups):
            solver.add(assignments[i] == i)

        participant_vars = list(map(lambda p: Int(p), self.config.participants))

        # Participants must be equal to one of the assigned pairs
        for participant in participant_vars:
            solver.add(Or(list(map(lambda a: participant == a, assignments))))

        # Each pair cannot have more than 2 participants equal to it
        for i, assignment in enumerate(assignments):
            solver.add(self.count_equals(participant_vars, assignment) == 2)

        # Apply the pairing rules
        for rule in self.config.rules:
            solver.add(
                participant_vars[self.config.participants.index(rule[0])]
                != participant_vars[self.config.participants.index(rule[1])]
            )

        if solver.check() == sat:
            model = solver.model()
            participant_assignments = list(
                map(lambda p: (p, model[p].as_long()), participant_vars)
            )
            final_assignments = []
            for assignment in assignments:
                final_assignments.append(
                    tuple(
                        map(
                            lambda p: str(p[0]),
                            filter(
                                lambda p: p[1] == model[assignment].as_long(),
                                participant_assignments,
                            ),
                        )
                    )
                )
            return final_assignments
        else:
            return []

"""
Arbitration between departments making competing resource demands
(e.g. CAIN wanting a GPU lane while PPVO also wants it for frame
prediction). Kept deliberately simple: priority wins, deterministic
tie-break, no starvation — a department that loses a round is bumped
ahead of the winner next time it contends.
"""


class BoardOfDirectors:
    def __init__(self):
        # Tracks how many consecutive rounds each department has lost,
        # so a persistently low-priority requester still eventually gets served.
        self._loss_streak = {}

    def resolve_conflict(self, dept_a, dept_b):
        """
        dept_a / dept_b: dicts like {"department": "CAIN", "priority": 2}
        (priority: 0=normal, 1=high, 2=critical, 3=emergency — see NerveBase.PRIORITY)

        Returns the winning dict. Higher priority wins; on a tie, whichever
        department has lost more consecutive rounds gets it (starvation guard).
        """
        name_a = dept_a.get("department", "A")
        name_b = dept_b.get("department", "B")
        prio_a = dept_a.get("priority", 0)
        prio_b = dept_b.get("priority", 0)

        if prio_a != prio_b:
            winner, loser = (dept_a, dept_b) if prio_a > prio_b else (dept_b, dept_a)
        else:
            streak_a = self._loss_streak.get(name_a, 0)
            streak_b = self._loss_streak.get(name_b, 0)
            winner, loser = (dept_a, dept_b) if streak_a >= streak_b else (dept_b, dept_a)

        winner_name = winner.get("department")
        loser_name = loser.get("department")
        self._loss_streak[winner_name] = 0
        self._loss_streak[loser_name] = self._loss_streak.get(loser_name, 0) + 1

        return winner

    def resolve_all(self, requests):
        """Resolve an arbitrary number of competing requests down to one winner."""
        if not requests:
            return None
        winner = requests[0]
        for challenger in requests[1:]:
            winner = self.resolve_conflict(winner, challenger)
        return winner


if __name__ == "__main__":
    board = BoardOfDirectors()
    a = {"department": "CAIN", "priority": 1}
    b = {"department": "PPVO", "priority": 1}
    print(board.resolve_conflict(a, b))  # tie -> starvation guard decides
    print(board.resolve_conflict(a, b))  # loser from last round now favored

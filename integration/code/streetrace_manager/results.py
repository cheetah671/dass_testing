"""Results module for StreetRace Manager."""


class ResultsModule:
    """Records outcomes, ranking points, and prize money."""

    POINTS_BY_POSITION = {0: 10, 1: 6, 2: 4}

    def __init__(self, race_module, inventory_module, reputation_module=None):
        self.races = race_module
        self.inventory = inventory_module
        self.reputation = reputation_module
        self.rankings = {}
        self._race_history = {}
        self._driver_stats = {}

    def record_race_result(self, race_id, final_order, prize_money=0, damaged_cars=None):
        """Record race results and apply cross-module updates."""
        race = self.races.get_race(race_id)
        if race is None:
            raise ValueError("Race not found.")
        if race.completed:
            raise ValueError("Race already completed.")
        if not final_order:
            raise ValueError("Result order cannot be empty.")
        if len(final_order) != len(race.participants):
            raise ValueError("Result order must include all race participants.")
        if len(set(final_order)) != len(final_order):
            raise ValueError("Result order cannot contain duplicate drivers.")

        for driver_name in final_order:
            if driver_name not in race.participants:
                raise ValueError("Result includes a driver not entered in race.")

        for index, driver_name in enumerate(final_order):
            points = self.POINTS_BY_POSITION.get(index, 1)
            self.rankings[driver_name] = self.rankings.get(driver_name, 0) + points
            stats = self._driver_stats.setdefault(
                driver_name,
                {"races": 0, "wins": 0, "podiums": 0, "points": 0},
            )
            stats["races"] += 1
            stats["points"] += points
            if index == 0:
                stats["wins"] += 1
            if index < 3:
                stats["podiums"] += 1
            if self.reputation is not None:
                self.reputation.add_reputation(driver_name, points)

        if prize_money > 0:
            self.inventory.add_cash(prize_money)

        for car_id in damaged_cars or []:
            self.inventory.mark_car_damaged(car_id)

        race.completed = True
        summary = {
            "race_id": race_id,
            "winner": final_order[0],
            "final_order": list(final_order),
            "prize_money": prize_money,
            "damaged_cars": list(damaged_cars or []),
        }
        self._race_history[race_id] = summary
        return summary

    def get_race_result(self, race_id):
        """Return stored race result summary after completion."""
        return self._race_history.get(race_id)

    def leaderboard(self, top_n=None):
        """Return rankings sorted by points descending."""
        ordered = sorted(self.rankings.items(), key=lambda item: item[1], reverse=True)
        if top_n is None:
            return ordered
        if top_n < 1:
            raise ValueError("top_n must be at least 1.")
        return ordered[:top_n]

    def get_driver_stats(self, driver_name):
        """Return cumulative racing stats for a driver."""
        return self._driver_stats.get(
            driver_name,
            {"races": 0, "wins": 0, "podiums": 0, "points": 0},
        )

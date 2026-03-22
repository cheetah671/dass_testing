"""Integration tests for StreetRace Manager module interactions."""

import pytest


def test_register_driver_then_enter_race_success(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.race.create_race("R-1", "Dock Sprint")

    race = app.race.enter_race("R-1", "Alex", "CAR-1")

    assert race.participants == ["Alex"]
    assert race.car_assignments["Alex"] == "CAR-1"


def test_assign_role_requires_registration(app):
    with pytest.raises(ValueError, match="registered"):
        app.crew.assign_role("Unregistered", "driver")


def test_enter_race_without_driver_role_fails(app):
    app.registration.register_member("Sam")
    app.crew.assign_role("Sam", "mechanic")
    app.race.create_race("R-2", "Tunnel Rush")

    with pytest.raises(ValueError, match="driver role"):
        app.race.enter_race("R-2", "Sam", "CAR-1")


def test_record_race_result_updates_rankings_cash_and_reputation(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.race.create_race("R-3", "Midnight Run")
    app.race.enter_race("R-3", "Alex", "CAR-1")

    before_cash = app.inventory.cash_balance
    summary = app.results.record_race_result("R-3", ["Alex"], prize_money=1200)

    assert summary["winner"] == "Alex"
    assert app.results.rankings["Alex"] == 10
    assert app.reputation.get_points("Alex") == 10
    assert app.inventory.cash_balance == before_cash + 1200


def test_record_result_with_car_damage_blocks_next_race_until_repaired(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Mia")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Mia", "mechanic")

    app.race.create_race("R-4", "Harbor Circuit")
    app.race.enter_race("R-4", "Alex", "CAR-1")
    app.results.record_race_result("R-4", ["Alex"], prize_money=500, damaged_cars=["CAR-1"])

    app.race.create_race("R-5", "Airport Dash")
    with pytest.raises(ValueError, match="Damaged cars"):
        app.race.enter_race("R-5", "Alex", "CAR-1")

    assert app.garage.repair_car("CAR-1") is True
    app.race.enter_race("R-5", "Alex", "CAR-1")


def test_mission_cannot_start_when_required_roles_unavailable(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.missions.create_mission("M-1", "delivery", ["driver", "strategist"])

    assert app.missions.start_mission("M-1") is False


def test_repair_mission_requires_mechanic_and_damaged_car(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.missions.create_mission("M-2", "repair_after_race", ["mechanic"])

    assert app.missions.start_mission("M-2") is False

    app.registration.register_member("Mia")
    app.crew.assign_role("Mia", "mechanic")
    app.inventory.mark_car_damaged("CAR-2", severity=20)

    assert app.missions.start_mission("M-2") is True


def test_complete_mission_updates_inventory_cash(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.missions.create_mission("M-3", "delivery", ["driver"])

    started = app.missions.start_mission("M-3")
    assert started is True

    before_cash = app.inventory.cash_balance
    mission = app.missions.complete_mission("M-3", reward_money=350)

    assert mission.completed is True
    assert app.inventory.cash_balance == before_cash + 350


def test_results_reject_unregistered_race_participant_in_outcome(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.race.create_race("R-6", "Bridge Heat")
    app.race.enter_race("R-6", "Alex", "CAR-1")

    with pytest.raises(ValueError, match="not entered"):
        app.results.record_race_result("R-6", ["Ghost"], prize_money=100)


def test_duplicate_registration_is_rejected(app):
    app.registration.register_member("Alex")
    with pytest.raises(ValueError, match="already registered"):
        app.registration.register_member("Alex")


def test_invalid_role_assignment_is_rejected_for_registered_member(app):
    app.registration.register_member("Lee")
    with pytest.raises(ValueError, match="Invalid role"):
        app.crew.assign_role("Lee", "hacker")


def test_set_skill_level_validation_and_persistence(app):
    with pytest.raises(ValueError, match="registered"):
        app.crew.set_skill_level("Ghost", "cornering", 8)

    app.registration.register_member("Jin")
    app.crew.assign_role("Jin", "driver")
    member = app.crew.set_skill_level("Jin", "cornering", 9)

    assert member.skills["cornering"] == 9

    with pytest.raises(ValueError, match="between 1 and 10"):
        app.crew.set_skill_level("Jin", "reaction", 11)


def test_duplicate_race_id_is_rejected(app):
    app.race.create_race("R-7", "Neon Loop")
    with pytest.raises(ValueError, match="already exists"):
        app.race.create_race("R-7", "Neon Loop 2")


def test_enter_race_fails_for_missing_race_or_damaged_car(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")

    with pytest.raises(ValueError, match="Race not found"):
        app.race.enter_race("R-X", "Alex", "CAR-1")

    app.race.create_race("R-8", "Night Grid")
    app.inventory.mark_car_damaged("CAR-1", severity=10)
    with pytest.raises(ValueError, match="Damaged cars"):
        app.race.enter_race("R-8", "Alex", "CAR-1")


def test_record_result_rejects_empty_and_completed_race(app):
    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.race.create_race("R-9", "Canal Rush")
    app.race.enter_race("R-9", "Alex", "CAR-1")

    with pytest.raises(ValueError, match="cannot be empty"):
        app.results.record_race_result("R-9", [], prize_money=50)

    app.results.record_race_result("R-9", ["Alex"], prize_money=50)
    with pytest.raises(ValueError, match="already completed"):
        app.results.record_race_result("R-9", ["Alex"], prize_money=50)


def test_results_not_found_and_zero_prize_keeps_cash(app):
    with pytest.raises(ValueError, match="Race not found"):
        app.results.record_race_result("R-404", ["Alex"], prize_money=100)

    app.registration.register_member("Alex")
    app.crew.assign_role("Alex", "driver")
    app.race.create_race("R-10", "Hill Climb")
    app.race.enter_race("R-10", "Alex", "CAR-1")

    before = app.inventory.cash_balance
    app.results.record_race_result("R-10", ["Alex"], prize_money=0)
    assert app.inventory.cash_balance == before


def test_mission_not_found_and_complete_before_start_errors(app):
    with pytest.raises(ValueError, match="Mission not found"):
        app.missions.can_start_mission("M-404")

    app.registration.register_member("Ria")
    app.crew.assign_role("Ria", "driver")
    app.missions.create_mission("M-4", "delivery", ["driver"])

    with pytest.raises(ValueError, match="started"):
        app.missions.complete_mission("M-4", reward_money=100)


def test_garage_repair_checks_mechanic_parts_tools_and_missing_car(app):
    app.inventory.mark_car_damaged("CAR-1", severity=30)

    # No mechanic yet
    assert app.garage.repair_car("CAR-1") is False

    app.registration.register_member("Mia")
    app.crew.assign_role("Mia", "mechanic")

    app.inventory.spare_parts = 0
    assert app.garage.repair_car("CAR-1") is False

    app.inventory.spare_parts = 2
    app.inventory.tools = 0
    assert app.garage.repair_car("CAR-1") is False

    with pytest.raises(ValueError, match="Car not found"):
        app.garage.repair_car("CAR-404")


def test_garage_repair_success_consumes_parts_and_clears_damage(app):
    app.registration.register_member("Mia")
    app.crew.assign_role("Mia", "mechanic")
    app.inventory.mark_car_damaged("CAR-2", severity=60)

    before_parts = app.inventory.spare_parts
    repaired = app.garage.repair_car("CAR-2", parts_required=1)

    assert repaired is True
    assert app.inventory.spare_parts == before_parts - 1
    assert app.inventory.get_car("CAR-2").damaged is False


def test_reputation_negative_points_rejected_and_leaderboard_sorted(app):
    with pytest.raises(ValueError, match="cannot be negative"):
        app.reputation.add_reputation("Alex", -1)

    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")

    app.race.create_race("R-11", "Freeway Blitz")
    app.race.enter_race("R-11", "Alex", "CAR-1")
    app.race.enter_race("R-11", "Kai", "CAR-2")
    app.results.record_race_result("R-11", ["Alex", "Kai"], prize_money=300)

    board = app.reputation.leaderboard()
    assert board[0][0] == "Alex"
    assert board[0][1] > board[1][1]


def test_registration_initial_role_flows_into_race_entry(app):
    app.registration.register_member("Neo", role="driver")
    app.race.create_race("R-12", "Canyon Run")

    race = app.race.enter_race("R-12", "Neo", "CAR-1")
    assert race.participants == ["Neo"]


def test_race_rejects_duplicate_driver_and_duplicate_car_in_same_race(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")
    app.race.create_race("R-13", "Metro Clash")

    app.race.enter_race("R-13", "Alex", "CAR-1")

    with pytest.raises(ValueError, match="already entered"):
        app.race.enter_race("R-13", "Alex", "CAR-2")

    with pytest.raises(ValueError, match="already assigned"):
        app.race.enter_race("R-13", "Kai", "CAR-1")


def test_completed_race_rejects_new_entries(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")
    app.race.create_race("R-14", "Ring Sprint")
    app.race.enter_race("R-14", "Alex", "CAR-1")
    app.results.record_race_result("R-14", ["Alex"], prize_money=100)

    with pytest.raises(ValueError, match="completed race"):
        app.race.enter_race("R-14", "Kai", "CAR-2")


def test_results_require_all_participants_to_appear_in_final_order(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")
    app.race.create_race("R-15", "Skyway Finals")
    app.race.enter_race("R-15", "Alex", "CAR-1")
    app.race.enter_race("R-15", "Kai", "CAR-2")

    with pytest.raises(ValueError, match="must include all race participants"):
        app.results.record_race_result("R-15", ["Alex"], prize_money=200)


def test_mission_cannot_be_completed_twice_or_restarted_for_extra_cash(app):
    app.registration.register_member("Ria")
    app.crew.assign_role("Ria", "driver")
    app.missions.create_mission("M-5", "delivery", ["driver"])

    assert app.missions.start_mission("M-5") is True
    before = app.inventory.cash_balance
    app.missions.complete_mission("M-5", reward_money=250)
    assert app.inventory.cash_balance == before + 250

    with pytest.raises(ValueError, match="already completed"):
        app.missions.complete_mission("M-5", reward_money=250)

    with pytest.raises(ValueError, match="already completed"):
        app.missions.start_mission("M-5")


def test_garage_inspect_and_list_damaged_cars(app):
    report = app.garage.inspect_car("CAR-1")
    assert report["recommendation"] == "race_ready"

    app.inventory.mark_car_damaged("CAR-2", severity=40)
    damaged = app.garage.list_damaged_cars()

    assert len(damaged) == 1
    assert damaged[0].car_id == "CAR-2"

    report = app.garage.inspect_car("CAR-2")
    assert report["damaged"] is True
    assert report["recommendation"] == "repair"


def test_garage_perform_maintenance_flow(app):
    app.registration.register_member("Mia")
    app.crew.assign_role("Mia", "mechanic")
    app.inventory.get_car("CAR-1").condition = 82

    assert app.garage.perform_maintenance("CAR-1") is True
    assert app.inventory.get_car("CAR-1").condition == 92

    # Cannot maintain damaged car.
    app.inventory.mark_car_damaged("CAR-1", severity=10)
    assert app.garage.perform_maintenance("CAR-1") is False


def test_garage_install_part_consumes_parts_and_validates(app):
    app.registration.register_member("Mia")
    app.crew.assign_role("Mia", "mechanic")
    app.inventory.get_car("CAR-2").condition = 70

    before_parts = app.inventory.spare_parts
    assert app.garage.install_part("CAR-2", parts_required=2) is True
    assert app.inventory.spare_parts == before_parts - 2
    assert app.inventory.get_car("CAR-2").condition == 100

    with pytest.raises(ValueError, match="parts_required"):
        app.garage.install_part("CAR-2", parts_required=0)


def test_results_store_race_history_and_fetch_summary(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")
    app.race.create_race("R-16", "Downtown Sprint")
    app.race.enter_race("R-16", "Alex", "CAR-1")
    app.race.enter_race("R-16", "Kai", "CAR-2")

    summary = app.results.record_race_result(
        "R-16", ["Kai", "Alex"], prize_money=450, damaged_cars=["CAR-2"]
    )
    fetched = app.results.get_race_result("R-16")

    assert fetched == summary
    assert fetched["winner"] == "Kai"
    assert fetched["final_order"] == ["Kai", "Alex"]
    assert fetched["damaged_cars"] == ["CAR-2"]


def test_results_leaderboard_supports_top_n(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.registration.register_member("Mia")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")
    app.crew.assign_role("Mia", "driver")
    app.inventory.add_car("CAR-3", "Evo")

    app.race.create_race("R-17", "Tunnel King")
    app.race.enter_race("R-17", "Alex", "CAR-1")
    app.race.enter_race("R-17", "Kai", "CAR-2")
    app.race.enter_race("R-17", "Mia", "CAR-3")

    app.results.record_race_result("R-17", ["Alex", "Kai", "Mia"], prize_money=100)

    top_two = app.results.leaderboard(top_n=2)
    assert len(top_two) == 2
    assert top_two[0][0] == "Alex"

    with pytest.raises(ValueError, match="top_n"):
        app.results.leaderboard(top_n=0)


def test_results_driver_stats_accumulate_across_races(app):
    app.registration.register_member("Alex")
    app.registration.register_member("Kai")
    app.crew.assign_role("Alex", "driver")
    app.crew.assign_role("Kai", "driver")

    app.race.create_race("R-18", "Harbor Heat")
    app.race.enter_race("R-18", "Alex", "CAR-1")
    app.race.enter_race("R-18", "Kai", "CAR-2")
    app.results.record_race_result("R-18", ["Alex", "Kai"], prize_money=120)

    app.race.create_race("R-19", "Hill Drift")
    app.race.enter_race("R-19", "Alex", "CAR-1")
    app.race.enter_race("R-19", "Kai", "CAR-2")
    app.results.record_race_result("R-19", ["Kai", "Alex"], prize_money=80)

    alex = app.results.get_driver_stats("Alex")
    kai = app.results.get_driver_stats("Kai")
    ghost = app.results.get_driver_stats("Ghost")

    assert alex["races"] == 2
    assert alex["wins"] == 1
    assert alex["podiums"] == 2
    assert alex["points"] == app.results.rankings["Alex"]

    assert kai["races"] == 2
    assert kai["wins"] == 1
    assert kai["podiums"] == 2
    assert kai["points"] == app.results.rankings["Kai"]

    assert ghost == {"races": 0, "wins": 0, "podiums": 0, "points": 0}

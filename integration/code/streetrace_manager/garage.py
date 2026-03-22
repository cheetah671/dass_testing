"""Extra module: garage maintenance and repair operations."""


class GarageModule:
    """Repairs damaged cars by checking mechanic and inventory resources."""

    def __init__(self, crew_module, inventory_module):
        self.crew = crew_module
        self.inventory = inventory_module

    def repair_car(self, car_id, parts_required=1):
        """Repair a damaged car if mechanic and parts are available."""
        car = self.inventory.get_car(car_id)
        if car is None:
            raise ValueError("Car not found.")
        if parts_required < 1:
            raise ValueError("parts_required must be at least 1.")
        if not car.damaged:
            return False
        if not self.crew.members_with_role("mechanic"):
            return False
        if self.inventory.spare_parts < parts_required:
            return False
        if self.inventory.tools <= 0:
            return False

        self.inventory.spare_parts -= parts_required
        car.damaged = False
        car.condition = min(100, car.condition + 40)
        return True

    def inspect_car(self, car_id):
        """Return a summary of a car's health and service recommendation."""
        car = self.inventory.get_car(car_id)
        if car is None:
            raise ValueError("Car not found.")

        if car.damaged:
            recommendation = "repair"
        elif car.condition < 60:
            recommendation = "install_part"
        elif car.condition < 85:
            recommendation = "maintenance"
        else:
            recommendation = "race_ready"

        return {
            "car_id": car.car_id,
            "model": car.model,
            "condition": car.condition,
            "damaged": car.damaged,
            "recommendation": recommendation,
        }

    def list_damaged_cars(self):
        """Return all currently damaged cars."""
        return [car for car in self.inventory.cars.values() if car.damaged]

    def perform_maintenance(self, car_id, tools_required=1):
        """Improve condition for non-damaged cars using available mechanics and tools."""
        car = self.inventory.get_car(car_id)
        if car is None:
            raise ValueError("Car not found.")
        if tools_required < 1:
            raise ValueError("tools_required must be at least 1.")
        if car.damaged:
            return False
        if not self.crew.members_with_role("mechanic"):
            return False
        if self.inventory.tools < tools_required:
            return False
        if car.condition >= 100:
            return False

        car.condition = min(100, car.condition + 10)
        return True

    def install_part(self, car_id, parts_required=1):
        """Install spare parts to improve condition of a non-damaged car."""
        car = self.inventory.get_car(car_id)
        if car is None:
            raise ValueError("Car not found.")
        if parts_required < 1:
            raise ValueError("parts_required must be at least 1.")
        if car.damaged:
            return False
        if not self.crew.members_with_role("mechanic"):
            return False
        if self.inventory.spare_parts < parts_required:
            return False
        if car.condition >= 100:
            return False

        self.inventory.spare_parts -= parts_required
        car.condition = min(100, car.condition + (15 * parts_required))
        return True

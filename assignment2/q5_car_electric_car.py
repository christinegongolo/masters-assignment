"""
Question 5 (20 marks)
Implement a Python class hierarchy with a base class Car (make, model,
year, and a method returning a formatted description), and a subclass
ElectricCar that:
  - Adds a battery_size attribute, set via the constructor.
  - Overrides the description method to include battery size.
  - Has a method returning a detailed battery description (size, charging
    time, range).
"""


class Car:
    """Base class representing a generic car."""

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def get_description(self):
        """Return a formatted description of the car."""
        return f"{self.year} {self.make} {self.model}"


class ElectricCar(Car):
    """A Car that also has a battery, with electric-specific details."""

    def __init__(self, make, model, year, battery_size,
                 charging_time_hours=None, range_km=None):
        # Reuse the base class constructor for the shared attributes
        super().__init__(make, model, year)
        self.battery_size = battery_size  # in kWh
        self.charging_time_hours = charging_time_hours
        self.range_km = range_km

    def get_description(self):
        """Override to include battery size alongside the base description."""
        base_description = super().get_description()
        return f"{base_description} with a {self.battery_size}kWh battery"

    def get_battery_description(self):
        """Return a detailed description of the battery."""
        details = f"Battery size: {self.battery_size}kWh"

        if self.charging_time_hours is not None:
            details += f", charging time: {self.charging_time_hours} hours"

        if self.range_km is not None:
            details += f", estimated range: {self.range_km}km"

        return details


if __name__ == "__main__":
    car = Car("Toyota", "Corolla", 2020)
    print(car.get_description())

    electric_car = ElectricCar(
        make="Tesla",
        model="Model 3",
        year=2024,
        battery_size=75,
        charging_time_hours=8,
        range_km=500,
    )
    print(electric_car.get_description())
    print(electric_car.get_battery_description())

import math
from Payload import cubesat
from environmetn import env
from flight_stages import td 
from report import Report


class ForcesCalculator:
    def __init__(self, air_density, gravity, payload_name, payload_mass, payload_area):
        # Define Environment quantities
        self.rho = air_density      # Air density (kg/m³)
        self.g = gravity            # Gravity (m/s²)
        # Define Payload quantities
        self.payload_name = payload_name
        self.payload_mass = payload_mass  # kg
        self.payload_area = payload_area  # m² (reference area)

    def drag_force(self, velocity, drag_coefficient):
        """
        Calculate drag force at a given velocity and drag coefficient.
        Formula:
            Fd = 0.5 * rho * v^2 * A * Cd
        where:
            Fd = Drag force (N)
            rho = Air density (kg/m³)
            v = Velocity (m/s)
            A = Reference area (m²)
            Cd = Drag coefficient (dimensionless)
        """
        return 0.5 * self.rho * velocity**2 * self.payload_area * drag_coefficient

    def opening_force(self, velocity, cl, l_over_d):
        """
        Calculate parachute opening force.
        Formula:
            F_open = 0.5 * Cl * rho * A * v^2 * (1 + L/D)
        where:
            F_open = Opening force (N)
            Cl = Lift coefficient (dimensionless)
            rho = Air density (kg/m³)
            A = Reference area (m²)
            v = Velocity (m/s)
            L/D = Lift-to-drag ratio (dimensionless)
        """
        return 0.5 * cl * self.rho * self.payload_area * velocity**2 * (1 + l_over_d)

    def snatch_force(self, delta_v, line_length, stiffness=1e5, n_lines=4):
        """
        Calculate snatch force using a simple Hookean spring model.
        Formula:
            F_snatch = n_lines * k * elongation
            elongation = delta_v / (2 * line_length)
        where:
            F_snatch = Snatch force (N)
            n_lines = Number of lines
            k = Spring constant (N/m)
            elongation = Estimated line elongation (m)
            delta_v = Change in velocity (m/s)
            line_length = Length of parachute lines (m)
        """
        elongation = delta_v / (2 * line_length)  # simplified elongation
        return n_lines * stiffness * elongation

# Example usage (you can later import the values from another file)
calc = ForcesCalculator(
    air_density=1.225,
    gravity=9.81,
    payload_name="Probe-1",
    payload_mass=50,
    payload_area=0.5
)

velocity = 80         # m/s
drag_coeff = 1.5      # typical for parachutes
cl = 1.75             # lift coefficient
l_over_d = 0.5        # lift-to-drag ratio

print("Forces for Payload:", calc.payload_name)
print("-" * 40)
print(f"Drag Force:     {calc.drag_force(velocity, drag_coeff):.2f} N")
print(f"Opening Force:  {calc.opening_force(velocity, cl, l_over_d):.2f} N")
print(f"Snatch Force:   {calc.snatch_force(delta_v=velocity, line_length=5):.2f} N")
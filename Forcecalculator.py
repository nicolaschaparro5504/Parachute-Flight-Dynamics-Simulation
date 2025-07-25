import math
from Payload import cubesat
from environment import env
from flight_stages import td
from parachute import p1
from parachute import Parachute

class ForcesCalculator:
    def __init__(self, environment, payload, parachute):
        self.parachute = parachute
        self.env = environment
        self.payload = payload

    def drag_force(self, velocity, drag_coefficient):
        rho = self.env.density
        A = self.parachute.surface_area
        return 0.5 * rho * velocity**2 * A * drag_coefficient

    def opening_force(self, velocity, cl, l_over_d):
        rho = self.env.density
        A = self.parachute.surface_area
        return 0.5 * cl * rho * A * velocity**2 * (1 + l_over_d)

    def snatch_force(self, delta_v, line_length, stiffness=1e5, n_lines=4):
        elongation = delta_v / (2 * line_length)
        return n_lines * stiffness * elongation
    
    def report(self):
        """
        Print a report of the forces acting on the payload.
        """
        print(f"\n--- Forces Report for {self.payload.name} ---")
        print(f"Environment Density: {self.env.density:.3f} kg/m³")
        print(f"Payload Mass: {self.payload.mass:.2f} kg")
        print(f"Frontal Area: {self.payload.frontal_area():.3f} m²")
        print(f"Drag Force at terminal velocity: {self.drag_force(td.terminal_velocity(), 1.5):.2f} N")
        print(f"Opening Force: {self.opening_force(td.terminal_velocity(), 1.75, 0.5):.2f} N")
        print(f"Snatch Force: {self.snatch_force(td.terminal_velocity(), 5.0):.2f} N")

# ----------------------------- Demo ----------------------------------

if __name__ == "__main__":
    calc = ForcesCalculator(env, cubesat, p1)

    velocity    = td.terminal_velocity()   
    cd          = 1.5
    cl          = 1.75
    l_over_d    = 0.5
    line_length = 5.0

    print(f"Forces for payload: {calc.payload.name}")
    print("-" * 42)
    print(f"Terminal velocity: {velocity:.2f} m/s")
    print(f"Drag force:        {calc.drag_force(velocity, cd):10.2f}  N")
    print(f"Opening force:     {calc.opening_force(velocity, cl, l_over_d):10.2f}  N")
    print(f"Snatch force:      {calc.snatch_force(delta_v=velocity, line_length=line_length):10.2f}  N")
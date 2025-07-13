import math
from Payload import cubesat
from environmetn import env
from flight_stages import td 
class ForcesCalculator:
    def __init__(self, environment, payload):
        self.env = environment
        self.payload = payload

    def drag_force(self, velocity, drag_coefficient):
        rho = self.env.density
        A = self.payload.frontal_area()
        return 0.5 * rho * velocity**2 * A * drag_coefficient

    def opening_force(self, velocity, cl, l_over_d):
        rho = self.env.density
        A = self.payload.frontal_area()
        return 0.5 * cl * rho * A * velocity**2 * (1 + l_over_d)

    def snatch_force(self, delta_v, line_length, stiffness=1e5, n_lines=4):
        elongation = delta_v / (2 * line_length)
        return n_lines * stiffness * elongation

# ----------------------------- Demo ----------------------------------

if __name__ == "__main__":
    calc = ForcesCalculator(env, cubesat)

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

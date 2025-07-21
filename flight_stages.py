import math
import numpy as np
import matplotlib.pyplot as plt
from parachute import Parachute
from Payload import Payload
from environment import Environment

# Initialize Payload, Parachute, and Environment objects
cubesat = Payload("CubeSat-Alpha", 12.0, "cuboid", 0.2, 0.2, 0.2)
p1 = Parachute(10, 1.5, mass=5, shape="reefed")
env = Environment(altitude=1000)


class FlightStages:
    def __init__(self, payload: Payload, parachute: Parachute, environment: Environment, 
                 t_max, t_deploy=2.0, horizontal_speed=None):
        """
        Initialize the flight simulation with payload, parachute, and environment objects
        """
        if environment.altitude <= 0:
            raise ValueError("Initial height must be greater than zero.")
        if t_max <= 0:
            raise ValueError("Maximum time must be greater than zero.")
        if parachute.inflation_time <= 0:
            raise ValueError("Inflation time must be greater than zero.")
        if t_deploy < 0:
            raise ValueError("Deployment time cannot be negative.")

        # Store inputs
        self.payload = payload
        self.parachute = parachute
        self.environment = environment

        self.z0 = environment.altitude
        self.t_max = t_max
        self.t_deploy = t_deploy
        self.t_inflation = parachute.inflation_time

        # Use horizontal speed from environment wind if not provided
        self.horizontal_speed = horizontal_speed if horizontal_speed is not None else environment.wind_horizontal

        self.g = environment.g
        self.rho = environment.compute_density()
        self.total_mass = payload.mass + parachute.mass

    def terminal_velocity(self):
        """
        Calculate the terminal velocity after parachute inflation, when the drag force equals the weight.
        Formula:
            Vt = sqrt( (2 * m * g) / (rho * Cd * A) )
        """
        return math.sqrt((2 * self.total_mass * self.g) /
                         (self.rho * self.parachute.drag_area)) # drag_area is Cd * A

    def generate_trajectory(self, dt=0.1):
        """
        Simulate the descent trajectory in three stages:
        1. Free fall before parachute deployment
        2. Inflation stage (constant deceleration)
        3. Terminal descent (constant velocity)
        Returns arrays for time, altitude, velocity, horizontal position, and acceleration.
        """
        v0 = -self.g * self.t_deploy  # velocity at the end of free fall
        terminal_velocity = self.terminal_velocity()
        a_infl = min((v0 + terminal_velocity) / self.t_inflation, 4 * self.g)

        t_values, z_values, v_values, x_values, a_values = [], [], [], [], []

        t = 0
        z = self.z0
        x = 0

        while z > 0 and t <= self.t_max:
            if t < self.t_deploy:
                z = self.z0 - 0.5 * self.g * t**2
                v = -self.g * t
                a = -self.g

            elif t < self.t_deploy + self.t_inflation:
                t_rel = t - self.t_deploy
                z0_infl = self.z0 - 0.5 * self.g * self.t_deploy**2
                v = v0 + a_infl * t_rel
                z = z0_infl + v0 * t_rel + 0.5 * a_infl * t_rel**2
                a = a_infl

            else:
                t_rel = t - (self.t_deploy + self.t_inflation)
                v = -terminal_velocity
                z0_term = self.z0 - 0.5 * self.g * self.t_deploy**2 + \
                          (v0 * self.t_inflation + 0.5 * a_infl * self.t_inflation**2)
                z = z0_term + v * t_rel
                a = 0

            x += self.horizontal_speed * dt

            t_values.append(t)
            z_values.append(max(z, 0))
            v_values.append(v)
            x_values.append(x)
            a_values.append(a)

            if z <= 0:
                break
            t += dt

        return np.array(t_values), np.array(z_values), np.array(v_values), np.array(x_values), np.array(a_values)

    def plot_trajectory(self):
        """
        Plot altitude vs time, showing deployment and inflation stages
        """
        t, z, _, x, _ = self.generate_trajectory()
        plt.figure(figsize=(8, 5))
        plt.plot(t, z, label="Altitude")
        plt.axvline(self.t_deploy, color='orange', linestyle='--', label="Deployment")
        plt.axvline(self.t_deploy + self.t_inflation, color='green', linestyle='--', label="End of Inflation")
        plt.xlabel("Time [s]")
        plt.ylabel("Altitude [m]")
        plt.title("Trajectory with Deployment and Inflation Stages")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        print(f"\nHorizontal displacement: {x[-1]:.2f} m")
    
    def plot_velocity(self):
        """
        Plot velocity vs time, showing deployment and inflation stages
        """
        t, _, v, _, _ = self.generate_trajectory()
        plt.figure(figsize=(8, 5))
        plt.plot(t, v, label="Velocity", color='red')
        plt.axvline(self.t_deploy, color='orange', linestyle='--', label="Deployment")
        plt.axvline(self.t_deploy + self.t_inflation, color='green', linestyle='--', label="End of Inflation")
        plt.xlabel("Time [s]")
        plt.ylabel("Velocity [m/s]")
        plt.title("Velocity with Deployment and Inflation Stages")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_acceleration(self):
        """
        Plot acceleration vs time, showing deployment and inflation stages
        """
        t, _, _, _, a = self.generate_trajectory()
        plt.figure(figsize=(8, 5))
        plt.plot(t, a, label="Acceleration", color='green')
        plt.axvline(self.t_deploy, color='orange', linestyle='--', label="Deployment")
        plt.axvline(self.t_deploy + self.t_inflation, color='blue', linestyle='--', label="End of Inflation")
        plt.xlabel("Time [s]")
        plt.ylabel("Acceleration [m/s²]")
        plt.title("Acceleration with Deployment and Inflation Stages")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def simulate(self):
        """
        Run the simulation and plot all trajectories
        """
        self.plot_trajectory()
        self.plot_velocity()
        self.plot_acceleration()

    def get_state_at_time(self, time_query, dt=0.1):
        """
        Print the state (altitude, velocity, acceleration, horizontal position) at a specific time.
        If the time is outside the simulation, show the last state.
        """
        t, z, v, x, a = self.generate_trajectory(dt=dt)

        if time_query > t[-1]:
            print(f"\n[WARNING] The time consulted ({time_query:.1f} s) exceeds the simulated interval (up to {t[-1]:.2f} s). Showing last state:\n")        
            idx = -1
        else:
            idx = np.abs(t - time_query).argmin()

        state = {
            "Time [s]": t[idx],
            "Altitude [m]": z[idx],
            "Vertical Speed [m/s]": v[idx],
            "Acceleration [m/s²]": a[idx],
            "Horizontal Position [m]": x[idx]
        }

        for k, val in state.items():
            print(f"{k:>25}: {val:.3f}")

td = FlightStages(
    payload=cubesat,
    parachute=p1,
    environment=env,
    t_max=60,
    t_deploy=2.0,
    horizontal_speed=1.0
)




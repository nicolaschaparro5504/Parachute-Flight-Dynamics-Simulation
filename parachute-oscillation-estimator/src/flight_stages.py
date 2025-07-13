class FlightStages:
    def __init__(self, mass, drag_coefficient, area, z0, t_max, t_deploy=2.0, t_inflation=2.0, horizontal_speed=0.0,
                 air_density=1.225, gravity=9.81):
        """
        Initialize the flight simulation parameters
        """
        # Input validation
        if mass <= 0:
            raise ValueError("Mass must be greater than zero.")
        if drag_coefficient <= 0 or area <= 0:
            raise ValueError("Drag coefficient and area must be greater than zero.")
        if z0 <= 0:
            raise ValueError("Initial height must be greater than zero.")
        if t_max <= 0:
            raise ValueError("Maximum time must be greater than zero.")
        if t_inflation <= 0:
            raise ValueError("Inflation time must be greater than zero.")
        if t_deploy < 0:
            raise ValueError("Deployment time cannot be negative.")
        
        # Store parameters
        self.mass = mass
        self.Cd = drag_coefficient
        self.A = area
        self.z0 = z0
        self.t_max = t_max
        self.t_deploy = t_deploy
        self.t_inflation = t_inflation
        self.horizontal_speed = horizontal_speed
        self.rho = air_density
        self.g = gravity

    def terminal_velocity(self):
        """
        Calculate the terminal velocity after parachute inflation, when the drag force equals the weight.
        The formula is derived from the balance of forces:
        Formula:
            Vt = sqrt( (2 * m * g) / (rho * Cd * A) )
        where:
            m = mass
            g = gravity
            rho = air density
            Cd = drag coefficient
            A = parachute area
        """
        return math.sqrt((2 * self.mass * self.g) / (self.rho * self.Cd * self.A))

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
        a_infl = (-terminal_velocity - v0) / self.t_inflation   # Constant deceleration during inflation stage

        t_values, z_values, v_values, x_values, a_values = [], [], [], [], []  # Initialize arrays

        # Initial conditions
        t = 0
        z = self.z0
        x = 0

        while z > 0 and t <= self.t_max:
            if t < self.t_deploy:
                """
                Stage 1: Free fall
                The object falls freely under the influence of gravity until the parachute is deployed.
                The equations of motion are:
                - Altitude: z = z0 - 0.5 * g * t^2
                - Velocity: v = -g * t
                - Acceleration: a = -g (constant)
                """
                z = self.z0 - 0.5 * self.g * t**2
                v = -self.g * t
                a = -self.g

            elif t < self.t_deploy + self.t_inflation:
                """
                Stage 2: Inflation (parachute opening)
                The parachute opens, causing a constant deceleration.
                The equations of motion are:
                - Altitude: z = z0_infl + v0 * t_rel + 0.5 * a_infl * t_rel^2
                - Velocity: v = v0 + a_infl * t_rel
                - Acceleration: a = a_infl (constant)
                where:
                - t_rel is the relative time since deployment
                - v0 is the initial velocity at deployment
                - z0_infl is the initial altitude at deployment
                """

                t_rel = t - self.t_deploy
                z0_infl = self.z0 - 0.5 * self.g * self.t_deploy**2

                
                v = v0 + a_infl * t_rel
                z = z0_infl + v0 * t_rel + 0.5 * a_infl * t_rel**2
                a = a_infl
            else:
                """
                Stage 3: Terminal descent
                After inflation, the parachute reaches terminal velocity.
                The equations of motion are:
                - Altitude: z = z0_term + v * t_rel
                - Velocity: v = -terminal_velocity (constant)
                - Acceleration: a = 0 (constant)
                where:
                - t_rel is the relative time since the end of inflation
                - z0_term is the altitude at the end of inflation
                """

                t_rel = t - (self.t_deploy + self.t_inflation)
                v = -terminal_velocity

                # Initial altitude at end of inflation
                z0_term = self.z0 - 0.5 * self.g * self.t_deploy**2 + \
                          (v0 * self.t_inflation + 0.5 * a_infl * self.t_inflation**2)
                
                z = z0_term + v * t_rel
                a = 0

            # Update horizontal position
            x += self.horizontal_speed * dt

            # Store values
            t_values.append(t)
            z_values.append(max(z, 0))  # Ensure altitude does not go below zero
            v_values.append(v)
            x_values.append(x)
            a_values.append(a)

            if z <= 0: # If the altitude reaches zero, stop the simulation
                break
            t += dt # Increment time

        # Convert lists to numpy arrays for easier handling
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

        if time_query > t[-1]: # If the queried time exceeds the simulation time, show the last state
            print(f"\n[WARNING] The time consulted ({time_query:.1f} s) exceeds the simulated interval (up to {t[-1]:.2f} s). Showing last state:\n")        
            idx = -1 # Last index
        else:
            idx = np.abs(t - time_query).argmin()  # Find the closest index to the queried time
            # argmin returns the index of the minimum value in the array, which is the closest time to the query

        state = {
            "Time [s]": t[idx],
            "Altitude [m]": z[idx],
            "Vertical Speed [m/s]": v[idx],
            "Acceleration [m/s²]": a[idx],
            "Horizontal Position [m]": x[idx]
        }

        for k, val in state.items():  # Format and print the state
            print(f"{k:>25}: {val:.3f}")  # k:>25 aligns the key to the right with a width of 25 characters

td = FlightStages(mass=80, drag_coefficient=1.5, area=0.5, z0=1000, t_max=60, horizontal_speed=1)
class OscillationEstimator:
    def __init__(self, flight_stage):
        self.flight_stage = flight_stage

    def calculate_angle_of_attack(self, velocity, vertical_speed):
        """
        Estimate the angle of attack based on the velocity and vertical speed.
        The angle of attack can be estimated using the formula:
            alpha = atan(vertical_speed / horizontal_speed)
        where:
            vertical_speed is the downward speed of the parachute,
            horizontal_speed is the horizontal speed of the parachute.
        """
        horizontal_speed = self.flight_stage.horizontal_speed
        if horizontal_speed == 0:
            return 90  # If horizontal speed is zero, angle of attack is 90 degrees
        return math.degrees(math.atan(vertical_speed / horizontal_speed))

    def estimate_oscillations(self, dt=0.1):
        """
        Estimate the changes in angle of attack during the descent.
        This method will simulate the descent and calculate the angle of attack at each time step.
        """
        t_values, z_values, v_values, x_values, a_values = self.flight_stage.generate_trajectory(dt)
        angles_of_attack = []

        for vertical_speed in v_values:
            angle = self.calculate_angle_of_attack(self.flight_stage.horizontal_speed, vertical_speed)
            angles_of_attack.append(angle)

        return t_values, angles_of_attack

    def plot_angle_of_attack(self):
        """
        Plot the angle of attack over time during the descent.
        """
        t, angles = self.estimate_oscillations()
        plt.figure(figsize=(8, 5))
        plt.plot(t, angles, label="Angle of Attack", color='purple')
        plt.xlabel("Time [s]")
        plt.ylabel("Angle of Attack [degrees]")
        plt.title("Angle of Attack During Parachute Descent")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
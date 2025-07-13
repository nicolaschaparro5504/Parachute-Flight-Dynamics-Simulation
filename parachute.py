import math
import matplotlib.pyplot as plt

class Parachute:
    def __init__(self, diameter, drag_coefficient, suspension_line_length = None, 
                 shape="hemispherical", inflation_time=None, opening_force_coefficient=None, mass=None):
        """
        Initializes a parachute object

        Args:
        - diameter (float): Diameter of the parachute (m)
        - drag_coefficient (float): Drag coefficient of the parachute (Cd)
        - suspension_line_length (float): Length of the suspension lines (m)
        - shape (str): Shape of the parachute ('flat', 'hemispherical',
            'conical', 'ribbon', 'reefed', 'guide_surface')
        - inflation_time (float): Inflation time in seconds
        - opening_force_coefficient (float): Opening force coefficient
        """
        self.diameter = diameter
        self.drag_coefficient = drag_coefficient
        self.mass = mass
        self.shape = shape.lower()  # Lowercase a text

        self.calculate_drag_area()  # Calculate the effective drag area based on the shape and diameter 

        # If the user does not provide a suspension line length,
        # estimate it based on the diameter and shape of the parachute    

        if suspension_line_length is None:
            self.suspension_line_length = self.estimate_suspension_line_length(self.diameter, self.shape)
        else:
            self.suspension_line_length = suspension_line_length

        # If opening_force_coefficient or inflation_time is not provided by the user,
        # estimate them based on the shape of the parachute

        if opening_force_coefficient is None or inflation_time is None:
            Cx, t_inf = self.estimate_opening_parameters(self.shape)
            self.opening_force_coefficient = Cx if opening_force_coefficient is None else opening_force_coefficient
            self.inflation_time = t_inf if inflation_time is None else inflation_time
        else:
            self.opening_force_coefficient = opening_force_coefficient
            self.inflation_time = inflation_time

    @staticmethod  
    # static method is used to define a method that does not depend on instance variables, 
    # because it only uses the shape parameter to estimate the opening parameters

    def estimate_opening_parameters(shape="hemispherical"):
        """
        Method to estimate the opening force coefficient and inflation time
        """
        # Coefficients and times based on the shape of the parachute
        shape_presets = {
            "flat": (1.8, 0.7),
            "hemispherical": (1.5, 1.0),
            "conical": (1.3, 1.2),
            "ribbon": (1.0, 1.8),
            "reefed": (0.6, 2.0),
            "guide_surface": (1.4, 1.0),
            "square": (1.2, 1.0)  # Assuming square parachute has similar properties to hemispherical
        }
        return shape_presets.get(shape.lower(), (1.5, 1.0))  # default values if shape not found
    
    @staticmethod
    def estimate_suspension_line_length(diameter, shape="hemispherical"):
        """
        Method to estimate the suspension line length based on the diameter and shape of the parachute
        """
        ratios = {
            "flat": 1.0,
            "hemispherical": 1.2,
            "conical": 1.3,
            "square": 1.1,
            "guide_surface": 1.3,
            "ribbon": 1.0,
            "reefed": 1.0
        }
        factor = ratios.get(shape.lower(), 1.2)  # The factor depends on the shape of the parachute
        return factor * diameter
    
    def print_area(self):
        print(f"Drag area for {self.shape} parachute is: {self.area:.4f} m²")

    def calculate_drag_area(self):
        """
        Method to calculate the effective drag area, depending on the shape of the parachute.
        """
        if self.shape == "square":
            surface_area = self.diameter ** 2  # Diameter is the side length for square parachutes
            self.area = self.drag_coefficient * surface_area
            
        else:
            surface_area = (math.pi / 4) * self.diameter ** 2  # Circular by default
            self.area = self.drag_coefficient * surface_area
            
    def get_inflated_drag_area(self, time):
        """
        Method to get the inflated drag area at a given time.    
        """
        if time >= self.inflation_time:
            area = self.area
        else:
            area = self.area * (time / self.inflation_time) ** 2
        return area

    def is_fully_inflated(self, time):
        """ 
        Method to check if the parachute is fully inflated at a given time 
        """
        return time >= self.inflation_time

    def plot_inflation_profile(self, t_max=None, steps=100):
        """
        Method to plot the inflation profile of the parachute over time
        If t_max is not provided, it defaults to 1.5 times the inflation time
        """
        if t_max is None:
            t_max = self.inflation_time * 1.5

        # times: list of time points at which the drag area will be evaluated and plotted
        times = [t_max * i / steps for i in range(steps + 1)] 
        areas = [self.get_inflated_drag_area(t) for t in times]

        plt.figure(figsize=(6, 4))
        plt.plot(times, areas, label="Inflated Drag Area", color='blue')
        plt.axvline(self.inflation_time, color='r', linestyle='--', label="Inflation Time")
        plt.xlabel("Time [s]")
        plt.ylabel("Effective Drag Area [m²]")
        plt.title(f"Inflation Profile of the Parachute ({self.shape})")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def parachute_data(self):
        print(
            f"Parachute data:\n"
            f"  Shape: {self.shape}\n"
            f"  Diameter: {self.diameter} m\n"
            f"  Suspension Line Length: {self.suspension_line_length} m\n"
            f"  Mass: {self.mass} kg\n"
            f"  Drag Coefficient (Cd): {self.drag_coefficient}\n"
            f"  Opening Force Coefficient (Cx): {self.opening_force_coefficient}\n"
            f"  Inflation Time: {self.inflation_time} s\n"
            f"  Area: {self.area:.3f} m²"
        )

p1 = Parachute(10, 1.5, shape="reefed")
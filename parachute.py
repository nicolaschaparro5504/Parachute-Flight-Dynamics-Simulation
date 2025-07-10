import math

class Parachute:
    def __init__(self, diameter, drag_coefficient, suspension_line_length = None, 
                 shape="hemispherical", inflation_time=None, opening_force_coefficient=None):
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
        self.shape = shape.lower()  # Lowercase a text
        self.current_time = 0

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

    def calculate_drag_area(self):
        """
        Method to calculate the effective drag area, depending on the shape of the parachute.
        """
        if self.shape == "square":
            surface_area = self.diameter ** 2  # Diameter is the side length for square parachutes
            print(f"Drag area for {self.shape} parachute is: {self.drag_coefficient * surface_area:.4f} m²")
        else:
            surface_area = (math.pi / 4) * self.diameter ** 2  # Circular by default
            print(f"Drag area for {self.shape} parachute is: {self.drag_coefficient * surface_area:.4f} m²")

    def parachute_data(self):
        return (f"Parachute(shape={self.shape}, d={self.diameter} m, Cd={self.drag_coefficient}, "
                f"Cx={self.opening_force_coefficient}, inflation_time={self.inflation_time}s, "
                f"area={self.area:.3f} m²)")

p1 = Parachute(10, 1.5, shape="square")
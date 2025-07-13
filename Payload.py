import math

class Payload:
    def __init__(self, name, mass, shape, width, height, depth=None):
        """
        Initialize a Payload object.

        Parameters:
        - name: str, name of the payload
        - mass: float, mass in kg
        - shape: str, 'cuboid', 'cylinder', or 'sphere'
        - width: float, width in meters (diameter for cylinder/sphere)
        - height: float, height in meters
        - depth: float, depth in meters (optional, only for cuboid)
        """
        self.name = name
        self.mass = mass
        self.shape = shape.lower()
        self.width = width
        self.height = height
        self.depth = depth if depth is not None else width  # For sphere/cylinder, depth is not needed

    def volume(self):
        """
        Calculate the volume of the payload based on its shape.

        Formulas:
        - Cuboid: V = width * height * depth
        - Cylinder: V = π * r^2 * height, where r = width / 2
        - Sphere: V = (4/3) * π * r^3, where r = width / 2
        """
        if self.shape == "cuboid":
            return self.width * self.height * self.depth
        elif self.shape == "cylinder":
            radius = self.width / 2
            return math.pi * radius**2 * self.height
        elif self.shape == "sphere":
            radius = self.width / 2
            return (4/3) * math.pi * radius**3
        else:
            raise ValueError("Unknown shape")

    def center_of_gravity(self):
        """
        Calculate the center of gravity coordinates (x, y, z) for the payload.

        For regular shapes, the center of gravity is at the geometric center:
        - Cuboid: (width/2, height/2, depth/2)
        - Cylinder: (width/2, height/2, width/2)
        - Sphere: (r, r, r)
        """
        if self.shape == "cuboid":
            return (self.width / 2, self.height / 2, self.depth / 2)
        elif self.shape == "cylinder":
            return (self.width / 2, self.height / 2, self.width / 2)
        elif self.shape == "sphere":
            r = self.width / 2
            return (r, r, r)
        else:
            raise ValueError("Unknown shape")
        
    def density(self):
        """
        Calculate the density of the payload.

        Formula:
        - Density = mass / volume
        """
        return self.mass / self.volume()

    def frontal_area(self):
        """
        Calculate the frontal (projected) area of the payload.

        Formulas:
        - Cuboid: A = width * height
        - Cylinder/Sphere: A = π * r^2, where r = width / 2
        """
        if self.shape == "cuboid":
            return self.width * self.height
        elif self.shape == "cylinder" or self.shape == "sphere":
            radius = self.width / 2
            return math.pi * radius**2
        else:
            raise ValueError("Unknown shape")

    def report(self):
        """
        Print a detailed report of the payload's main properties.
        """
        print(f"\n--- Payload Report: {self.name} ---")
        print(f"Mass: {self.mass} kg")
        print(f"Shape: {self.shape}")
        print(f"Volume: {self.volume():.3f} m³")
        print(f"Density: {self.density():.3f} kg/m³")
        cog = self.center_of_gravity()
        print(f"Center of Gravity (x, y, z): ({cog[0]:.3f}, {cog[1]:.3f}, {cog[2]:.3f})")
        print(f"Frontal Area: {self.frontal_area():.3f} m²")

# Example: Create a Payload object for a CubeSat and print its report
cubesat = Payload(
    name="CubeSat-Alpha",
    mass=12.0,              # Mass in kg
    shape="cuboid",
    width=0.2,              # Width in meters
    height=0.2,             # Height in meters
    depth=0.2               # Depth in meters
)

cubesat.report()
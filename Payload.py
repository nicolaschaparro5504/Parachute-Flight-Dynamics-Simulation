import math

class Payload:
    def __init__(self, name, mass, shape, width, height, depth=None):
        self.name = name
        self.mass = mass
        self.shape = shape.lower()
        self.width = width
        self.height = height
        self.depth = depth if depth is not None else width  # sphere may not need depth

    def volume(self):
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
        return self.mass / self.volume()

    def frontal_area(self):
        if self.shape == "cuboid":
            return self.width * self.height
        elif self.shape == "cylinder" or self.shape == "sphere":
            radius = self.width / 2
            return math.pi * radius**2
        else:
            raise ValueError("Unknown shape")

    def report(self):
        print(f"\n--- Payload Report: {self.name} ---")
        print(f"Mass: {self.mass} kg")
        print(f"Shape: {self.shape}")
        print(f"Dimensions (W x H x D): {self.width} x {self.height} x {self.depth} meters")
        print(f"Volume: {self.volume():.2f} m³")
        print(f"Density: {self.density():.2f} kg/m³")
        cog = self.center_of_gravity()
        print(f"Center of Gravity (x, y, z): ({cog[0]:.2f}, {cog[1]:.2f}, {cog[2]:.2f})")


# Create a Payload object for a CubeSat
cubesat = Payload(
    name="CubeSat-Alpha",
    mass=12.0,              # in kg
    shape="cuboid",
    width=0.2,              # meters
    height=0.2,
    depth=0.2
)

cubesat.report()

import math
import numpy as np
import matplotlib.pyplot as plt

class ParachuteFlightSimulation:
    def __init__(
        self,
        mass: float,
        drag_coefficient: float,
        area: float,
        initial_height: float,
        t_max: float,
        t_deploy: float = 2.0,
        t_inflation: float = 2.0,
        horizontal_speed: float = 0.0,
        air_density: float = 1.225,
        gravity: float = 9.81,
    ):
        # Validación de parámetros
        if mass <= 0:
            raise ValueError("La masa debe ser mayor que cero.")
        if drag_coefficient <= 0 or area <= 0:
            raise ValueError("El coeficiente de arrastre y el área deben ser mayores que cero.")
        if initial_height <= 0:
            raise ValueError("La altura inicial debe ser mayor que cero.")
        if t_max <= 0:
            raise ValueError("El tiempo máximo debe ser mayor que cero.")
        if t_inflation <= 0:
            raise ValueError("El tiempo de inflado debe ser mayor que cero.")
        if t_deploy < 0:
            raise ValueError("El tiempo de despliegue no puede ser negativo.")

        # Asignación de parámetros
        self.mass = mass
        self.Cd = drag_coefficient
        self.A = area
        self.z0 = initial_height
        self.t_max = t_max
        self.t_deploy = t_deploy
        self.t_inflation = t_inflation
        self.horizontal_speed = horizontal_speed
        self.rho = air_density
        self.g = gravity

    def terminal_velocity(self) -> float:
        """Calcula la velocidad terminal después del inflado del paracaídas."""
        return math.sqrt((2 * self.mass * self.g) / (self.rho * self.Cd * self.A))

    def generate_trajectory(self, dt: float = 0.1):
        """
        Simula la trayectoria de descenso en tres etapas:
        1. Caída libre antes del despliegue
        2. Inflado del paracaídas (deceleración constante)
        3. Descenso terminal (velocidad constante)
        Devuelve: arrays de tiempo, altura, velocidad, posición horizontal y aceleración.
        """
        v0 = -self.g * self.t_deploy  # velocidad al final de la caída libre
        vt = self.terminal_velocity()
        a_infl = (-vt - v0) / self.t_inflation  # Deceleración durante el inflado

        t_values, z_values, v_values, x_values, a_values = [], [], [], [], []

        t = 0
        z = self.z0
        x = 0

        while z > 0 and t <= self.t_max:
            if t < self.t_deploy:
                # Etapa 1: Caída libre
                z = self.z0 - 0.5 * self.g * t**2
                v = -self.g * t
                a = -self.g
            elif t < self.t_deploy + self.t_inflation:
                # Etapa 2: Inflado
                t_rel = t - self.t_deploy
                z0_infl = self.z0 - 0.5 * self.g * self.t_deploy**2
                v = v0 + a_infl * t_rel
                z = z0_infl + v0 * t_rel + 0.5 * a_infl * t_rel**2
                a = a_infl
            else:
                # Etapa 3: Descenso terminal
                t_rel = t - (self.t_deploy + self.t_inflation)
                v = -vt
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

        return (
            np.array(t_values),
            np.array(z_values),
            np.array(v_values),
            np.array(x_values),
            np.array(a_values),
        )

    def plot_trajectory(self):
        """Grafica la altura vs tiempo y muestra los eventos de despliegue e inflado."""
        t, z, _, x, _ = self.generate_trajectory()
        plt.figure(figsize=(8, 5))
        plt.plot(t, z, label="Altitud")
        plt.axvline(self.t_deploy, color='orange', linestyle='--', label="Despliegue")
        plt.axvline(self.t_deploy + self.t_inflation, color='green', linestyle='--', label="Fin de inflado")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Altitud [m]")
        plt.title("Trayectoria con etapas de despliegue e inflado")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        print(f"\nDesplazamiento horizontal: {x[-1]:.2f} m")

# Ejemplo de uso:
if __name__ == "__main__":
    sim = ParachuteFlightSimulation(
        mass=80,
        drag_coefficient=1.5,
        area=0.5,
        initial_height=1000,
        t_max=60,
        horizontal_speed=1
    )
    sim.plot_trajectory()
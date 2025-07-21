# Parachute-Flight-Dynamics-Simulation
This project focuses on the development of a tool to better understand the behavior of parachutes during the recovery phase of experimental rockets. It simulates key moments such as deployment and descent, helping to test and improve parachute designs before real launches.

# Modeling and Integration of Spacecraft Subsystems Using Object-Oriented Programming

## Overview

This project demonstrates the modeling and integration of key spacecraft subsystems using Python and object-oriented programming (OOP) principles. Each subsystem is encapsulated in its own class, allowing for modularity, reusability, and clear interfaces between components.

The main `Simulation.py` class coordinates the interaction between all subsystems, simulating realistic operations such as power management, altitude/orientation control, payload operation, anomaly detection, and flight stages.

---

## Subsystems

---

## Subsystems

### 1. `Environment`
- Models atmospheric conditions such as altitude, temperature, pressure, air density, and wind.
- Provides environmental data for flight and force calculations.
- Used to simulate realistic descent conditions for the parachute and payload.

### 2. `parachute`
- Represents the parachute's physical and aerodynamic properties (shape, diameter, drag coefficient, mass).
- Calculates drag area, inflation profile, and opening forces.
- Provides reporting and visualization of parachute behavior during descent.

### 3. `flight_stages`
- Manages the simulation of descent phases, including deployment, inflation, and steady descent.
- Calculates trajectory, velocity, and acceleration over time.
- Integrates payload, parachute, and environment for complete flight dynamics.

### 4. `Oscillations`
- Estimates and simulates oscillatory motion (angle of attack, swinging) of the parachute-payload system during descent.
- Uses physical parameters to model damping and frequency of oscillations.
- Provides visualization of oscillation profiles.

### 5. `Forcecalculator`
- Calculates forces acting on the payload and parachute, including drag, opening, and snatch forces.
- Uses payload and environment properties for accurate force estimation.
- Provides detailed force reports for analysis.

### 6. `Payload`
- Models the payload's geometry, mass, and physical properties.
- Calculates volume, density, center of gravity, and frontal area.
- Provides visualization of oscillation profiles.

---

## How to Run and Test

## Installation
Clone this repository and navigate into the project folder:
```bash
git clone https://github.com/nicolaschaparro5504/Parachute-Flight-Dynamics-Simulation.git


### 1. Define the Payload, Parachute, and Environment Objects
Create instances for the payload, parachute, and environment with your desired parameters:
```python
payload = Payload(name, mass, shape, width, height, depth)
parachute = Parachute(diameter, drag_coefficient, mass, shape=shape)
environment = Environment(altitude, wind_horizontal, wind_direction, wind_vertical)
```

### 2. Simulate Flight Stages
Initialize the flight simulation with the created objects:
```python
flight = FlightStages(payload=payload, parachute=parachute, environment=environment, t_max=60, t_deploy=2)
flight.simulate()  # Plots trajectory, velocity, and acceleration
```

### 3. Analyze Oscillations
Estimate and plot parachute oscillations during descent:
```python
oscillator = ParachuteOscillationEstimator(parachute, flight, damping_ratio=0.15, natural_freq=0.8, initial_angle=5.0)
oscillator.plot_oscillations()
```

### 4. Calculate Forces
Compute and report forces acting on the payload and parachute:
```python
forces = ForcesCalculator(environment, payload)
forces.report()
```

### 5. Generate Reports
Print detailed reports for each subsystem:
```python
payload.report()
parachute.report()
forces.report()
```

## File Structure
Simulation.py  
parachute.py  
Payload.py  
environmetn.py  
flight_stages.py  
Oscillations.py  
Forcecalculator.py  
report.py


## Requirements
Python 3.7+
No external dependencies required

## Key OOP Concepts Used
Encapsulation: Each subsystem is a class with its own state and methods.
Inheritance: All subsystems inherit from a common Subsystem base class.
Composition: The Spacecraft class composes all subsystems.
Polymorphism: Subsystems can override base methods as needed.

## Authors
*   Diego Francesco Alessandroni Lince
*   Jonh Jairo Urriago Suarez
*   Nicolas Chaparro Barrantes

## Notes
The code is modular and can be extended with more subsystems or features.
For real-world applications, consider adding error handling, logging, and more detailed simulation logic.

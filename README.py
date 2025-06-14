Web VPython 3.2

'''
RLC Circuit Simulation by Kellen Yu and Vincent Huang

Our project was to model and simulate an RLC circuit. 
We can adjust the components of the RLC circuit by changing the sliders for resistance in ohms, 
inductance in millihenries, capacitance in microfarads, and capacitor voltage in volts. 
When the simulation is running, we cannot adjust the components of the RLC circuit unless it is paused.

The changes will be reflected in the simulation through movement of the yellow balls representing the current and its direction, 
the color of the resistor band for resistance, the size of capacitor plates for capacitance, 
and the number of coils for the inductance, and the thickness of the green arrows for the initial capacitor voltage.

Furthermore, we can run the simulation by clicking the run button and pause the simulation by clicking the pause button.
We can also reset the simulation by clicking the reset button as well as change the speed of simulation by adjusting the time step.

As the simulation is running, we have also modeled the power dissipation in the resistor with the red arrows, 
the electric field magnitude and direction in the capacitor with the green arrows, and the magnetic field magnetic and direction with the blue arrow.

Another part of our project was finding the voltage drop across nodes.
We select node 1 and node 2 from the dropdown menu to select A, B, or C. 
By clicking the run button after the two nodes are selected, each of the graphs for the current and voltage over time will be displayed to show the changes.

Have fun :)

BTW the person on the sphere is Mr.Zhu
'''

spinning_sphere = sphere(
    pos=vector(0,0,0),
    radius=1,
    texture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYI1Se0t0fkmGpO-wCe7-GeDvzIaK84hYvJQ&s",
    shininess=0.8
)

distant_light(direction=vector(1,1,1), color=color.white)

# Oscillation parameters
amplitude = 1
frequency = 1
omega = 2 * pi * frequency

# Field wave parameters
num_rings = 12
ring_spacing = 1.0
arrow_density = 36  # angular divisions per ring
arrow_length = 0.4

field_arrows = []

for i in range(1, num_rings + 1):
    r = i * ring_spacing
    for j in range(arrow_density):
        theta = 2 * pi * j / arrow_density
        pos = vector(r * cos(theta), 0, r * sin(theta))
        arr = arrow(pos=pos, axis=vector(0,0,arrow_length), color=color.green, shaftwidth=0.05)
        field_arrows.append((arr, r, theta))  # Store ring radius and angle for animation

t = 0
dt = 0.01

while True:
    rate(100)
    # Bobbing motion (simple harmonic)
    y = amplitude * sin(omega * t)
    spinning_sphere.pos.y = y

    # Animate E-field as transverse oscillating arrows
    for arr, r, theta in field_arrows:
        phase = omega * (t - r / 10)  # Wave propagates outward, c ~ 10 units/s
        e_field = sin(phase)
        arr.axis = vector(0, e_field * arrow_length, 0)

    t += dt

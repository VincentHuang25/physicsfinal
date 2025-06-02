Web VPython 3.2

COPPER = vec(184/255, 115/255, 51/255)
ALUMINUM = vec(211/255, 211/255, 211/255)

u_0 = 4*pi*10e-7
e_0 = 8.85*10e-12
WIRE_RADIUS = 0.005

class Inductor:
    b_field_render_range = 1.0 #Multiple of coil radius
    b_field_density = 0.1
    thickness_factor = 0.05
    coil_down_factor = 0.1
    coil = None
    wire1 = None
    wire2 = None
    b_field = None
    
    def __init__(self, inductance=1.0, length=1.0, radius=1.0, pose=vec(0,0,0), orient=vec(0,0,1)):
        self.inductance = inductance
        self.length = length
        self.radius = radius
        self.pose = pose
        self.orient = hat(orient)
        self.render_coil()
        return
    
    def get_n_coils(self, inductance, length, radius):
        return round(sqrt((inductance*length)/(u_0*(radius**2)*pi))*self.coil_down_factor)
        
    def render_coil(self):
        #delete old coil
        if (self.coil != None):
            self.coil.visible = False
            
        if (self.wire1 != None):
            self.wire2.visible = False
            
        if (self.wire2 != None):
            self.wire2.visible = False
    
        self.coil = helix()
        self.coil.color = COPPER
        self.coil.pos = self.pose-0.5*self.orient*self.length*0.7
        self.coil.axis = self.orient
        self.coil.radius = self.radius
        self.coil.length = self.length*0.7
        self.coil.thickness = self.radius*self.thickness_factor
        self.coil.coils = self.get_n_coils(self.inductance, self.length, self.radius)
        
        self.wire1 = curve(
            pos=[
                self.pose-0.5*self.orient*self.length,
                self.pose-0.5*self.orient*self.length*0.7, 
                rotate(self.pose-0.5*self.orient*self.length*0.7+hat(self.coil.up)*self.coil.radius, angle=pi/2, axis=self.coil.axis)
                ]
            )
        self.wire1.radius = self.coil.thickness/2
        self.wire1.color = COPPER
        
        self.wire2 = curve(
            pos=[
                self.pose+0.5*self.orient*self.length,
                self.pose+0.5*self.orient*self.length*0.7, 
                rotate(self.pose+0.5*self.orient*self.length*0.7+hat(self.coil.up)*self.coil.radius, angle=pi/2, axis=self.coil.axis)
                ]
            )
        self.wire2.radius = self.coil.thickness/2
        self.wire2.color = COPPER
        
        return
    
    def render_b_field(self, current):
        #delete old b_fields
        if (self.b_field != None):
            self.b_field.visible = False
            
        self.b_field = arrow(
                pos=self.pose-0.5*self.orient*current*0.05, 
                axis=self.pose+self.orient*current*0.05,
                color = color.blue,
                round=True, 
                headwidth=log(1+abs(0.015*current)),
                shaftwidth=log(1+abs(0.005*current)),
                )
        
        return
    

class Capacitor:
    plate1 = None
    plate2 = None
    wire1 = None
    wire2 = None
    
    plate_area_factor = 1e-10
    plate_thickness = 0.01
    wire_thickness = 0.25
    wire_len = 0.25
    
    dist = 0.025
    
    e_fields = []
    e_field_density = 0.2
    e_field_scale = 1e-3
    
    def __init__(self, capacitance=1.0, radius=1.0, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.pose = pose
        self.radius = radius
        self.orient = hat(orient)
        self.capacitance = capacitance
        self.render_plates()
        return
    
    def render_plates(self):
        if (self.plate1 != None):
            self.plate1.visible = False
            
        if (self.plate2 != None):
            self.plate2.visible = False
            
        if (self.wire1 != None):
            self.wire1.visible = False
        
        if (self.wire2 != None):
            self.wire2.visible = False
        
        side_len = sqrt(self.capacitance*self.dist/e_0 * self.plate_area_factor)
        
        self.plate1 = box(
            pos=self.pose+0.5*self.orient*self.dist, 
            height=self.plate_thickness, length=side_len, width=side_len,
            up = self.orient,
            color = ALUMINUM
            )
            
        self.plate2 = box(
            pos=self.pose-0.5*self.orient*self.dist, 
            height=self.plate_thickness, length=side_len, width=side_len,
            up = -self.orient,
            color = ALUMINUM
            )
     
        self.wire1 = curve(
            pos=[
                self.pose+0.5*self.orient*(self.plate_thickness + self.dist),
                self.pose+0.5*self.orient*(self.plate_thickness + self.dist + self.wire_len)
                ],
            radius=self.radius,
            color=ALUMINUM
            )
            
        self.wire2 = curve(
            pos=[
                self.pose-0.5*self.orient*(self.plate_thickness + self.dist),
                self.pose-0.5*self.orient*(self.plate_thickness + self.dist + self.wire_len)
                ],
            radius=self.radius,
            color=ALUMINUM
            )
            
        return
    
    def render_e_fields(self, voltage):
        if len(self.e_fields) > 0:
            for e in self.e_fields:
                e.visible = False
            self.e_fields.clear()
        
        side_len = sqrt(self.capacitance*self.dist/e_0 * self.plate_area_factor)
        
        for x in range(-side_len, side_len, side_len*self.e_field_density):
            for y in range(-side_len, side_len, side_len*self.e_field_density):
                a = arrow(
                    pos=self.pose-0.5*(voltage/abs(voltage))*self.orient*self.dist,
                    axis=self.pose+0.5*(voltage/abs(voltage))*self.orient*self.dist,
                    color=color.green,
                    round=True,
                    shaftwidth=(voltage/self.dist)*self.e_field_scale*0.01,
                    headwidth=(voltage/self.dist)*self.e_field_scale*0.025,
                    )
                self.e_fields.append(a)

class Resistor:
    def __init__(self):
        return
    
class Wire:
    def __init__(self):
        return


def main():
    c = Capacitor(capacitance=10e-6, radius=WIRE_RADIUS)
    c.render_e_fields(5)  


#some variables
R = 100
L = 0.100
C = 0.000000100
t = 0
q = 0.5
i = 0.5
dt = 0.000001

def f1(q,i):
    return i
    
def f2(q,i):
    return -(R*i/L+q/L/C)

def iRK4(q,i,dt):
    k1 = dt*f1(q,i)
    l1 = dt*f2(q,i)
    k2 = dt*f1(q+k1/2,i+l1/2)
    l2 = dt*f2(q+k1/2,i+l1/2)
    k3 = dt*f1(q+k2/2,i+l2/2)
    l3 = dt*f2(q+k2/2,i+l2/2)
    k4 = dt*f1(q+k3,i+l3)
    l4 = dt*f2(q+k3,i+l3)
    k = (k1+2*k2+2*k3+k4)/6
    l = (l1+2*l2+2*l3+l4)/6
    q += k
    i += l
    return q,i
    
g1 = graph(title='Current vs Time', xtitle='Time (s)', ytitle='Current (i)', align='right')
gc1 = gcurve(color=color.red,graph=g1)

#Resistor
g2 = graph(title='Voltage vs Time for Resistor', xtitle='Time (s)', ytitle='Voltage (i)')
gc2 = gcurve(color=color.green,graph=g2)

#Inductor
g3 = graph(title='Voltage vs Time for Inductor', xtitle='Time (s)', ytitle='Voltage (i)')
gc3 = gcurve(color=color.blue,graph=g3)
i2=0

#Capacitor
g4 = graph(title='Voltage vs Time for Capacitor', xtitle='Time (s)', ytitle='Voltage (i)')
gc4 = gcurve(color=color.yellow,graph=g4)
i3=0

for j in range(10000):
    di2=i
    i3+=i
    q,i = iRK4(q,i,dt)
    gc1.plot(t,i)
    gc2.plot(t,i*R)
    gc3.plot(t,(i-i2)/dt)
    gc4.plot(t,i3)
    t += dt

if __name__ == "__main__":
    main()

wtext(text="Vary the Inductance: \n")
inductance_slider = slider( bind=inductance_set, min=0, max=50, step = 1, id = "inductance", value = 0)
wt=wtext(text='{:1.2f}'.format(inductance_slider.value))
scene.append_to_caption(' Henrys\n')
wtext(text='<br>')

wtext(text="Vary the Resistance: \n")
resistance_slider = slider( bind=resistance_set, min=0, max=50, step = 1, id = "resistance", value = 0)
wt=wtext(text='{:1.2f}'.format(resistance_slider.value))
scene.append_to_caption(' Ohms\n')
wtext(text='<br>')

wtext(text="Vary the Capacitance: \n")
capacitance_slider = slider( bind=capacitance_set, min=0, max=50, step = 1, id = "capacitance", value = 0)
wt=wtext(text='{:1.2f}'.format(capacitance_slider.value))
scene.append_to_caption(' Farads\n')
wtext(text='<br>')

wtext(text="Vary the Capacitor Voltage: \n")
capacitor_voltage_slider = slider( bind=capacitor_voltage_set, min=0, max=50, step = 1, id = "capacitor_voltage", value = 0)
wt=wtext(text='{:1.2f}'.format(capacitor_voltage_slider.value))
scene.append_to_caption(' Volts\n')
wtext(text='<br>')

wtext(text="Vary the Simulation Speed: \n", align="right")
simulation_speed_slider = slider( bind=simulation_speed_set, min=0, max=50, step = 1, id = "simulation_speed", value = 0)
wtext(text='<br>')

wtext(text="Vary the Time Step: \n")
timestep_resolution_slider = slider( bind=timestep_resolution_set, min=0, max=50, step = 1, id = "timestep_resolution", value = 0)
wtext(text='<br>')


def inductance_set(evt):
    console.log(evt)
    wt.text = '{:1.2f}'.format(inductance_slider.value)
    if evt.id is "inductance":
        self_inductance = evt.value

def resistance_set(evt):
    wt.text = '{:1.2f}'.format(resistance_slider.value)
    if evt.id is "resistance":
        self_resistance = evt.value

def capacitance_set(evt):
    wt.text = '{:1.2f}'.format(capacitance_slider.value)
    if evt.id is "capacitance":
        self_capacitance = evt.value

def capacitor_voltage_set(evt):
    wt.text = '{:1.2f}'.format(capacitor_voltage_slider.value)
    if evt.id is "capacitor_voltage":
        self_capacitor_voltage = evt.value

def simulation_speed_set(evt):
    wt.text = '{:1.2f}'.format(simulation_speed_slider.value)
    if evt.id is "simulation_speed":
        self_simulation_speed = evt.value

def timestep_resolution_set(evt):
    wt.text = '{:1.2f}'.format(timestep_resolution_slider.value)
    if evt.id is "timestep_resolution":
        self_timestep_resolution = evt.value
        
        
running = True
def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"
button(text="Pause", bind=Run)

button(bind=reset, text="Reset")
wtext(text='<br>')

def reset():
    pass

Web VPython 3.2

COPPER = vec(184/255, 115/255, 51/255)
ALUMINUM = vec(211/255, 211/255, 211/255)
RESISTOR = vec(255/255,249/255,230/255)

u_0 = 4*pi*10e-7
e_0 = 8.85*10e-12
WIRE_RADIUS = 0.02

from vpython import *

#class shit

class Inductor:
    b_field_scale = 5e2
    coil_down_factor = 2.5e-2
    
    def __init__(self, inductance=1.0, length=1.0, radius=1.0, wire_radius=0.01, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.inductance = inductance
        self.length = length
        self.radius = radius
        self.pose = pose
        self.orient = hat(orient)
        self.wire_radius = wire_radius
        self.coil = None
        self.wire1 = None
        self.wire2 = None
        self.b_field = None
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
        self.coil.thickness = self.wire_radius*2
        self.coil.coils = self.get_n_coils(self.inductance, self.length, self.radius)
        
        self.wire1 = curve(
            pos=[
                self.pose-0.5*self.orient*self.length,
                self.pose-0.5*self.orient*self.length*0.7, 
                self.pose-0.5*self.orient*self.length*0.7+hat(self.coil.up)*self.coil.radius
                ]
            )
        self.wire1.radius = self.coil.thickness/2
        self.wire1.color = COPPER
        self.wire1.rotate(axis=self.orient, angle=pi/2, origin=self.pose)
        
        self.wire2 = curve(
            pos=[
                self.pose+0.5*self.orient*self.length,
                self.pose+0.5*self.orient*self.length*0.7, 
                self.pose+0.5*self.orient*self.length*0.7+hat(self.coil.up)*self.coil.radius
                ]
            )
        self.wire2.radius = self.coil.thickness/2
        self.wire2.color = COPPER
        self.wire2.rotate(axis=self.orient, angle=pi/2, origin=self.pose)
        
        return
    
    def render_b_field(self, current):
        #delete old b_fields
        if (self.b_field != None):
            self.b_field.visible = False
        
        current *= self.b_field_scale
            
        self.b_field = arrow(
                pos=self.pose-self.orient*0.5*self.coil.length*current*0.05, 
                axis=self.orient*self.coil.length*current*0.05,
                color = color.blue,
                round=True, 
                headwidth=log(1+abs(0.015*current)),
                shaftwidth=log(1+abs(0.005*current)),
                )
        
        return
    
   

class Capacitor: 
    plate_area_factor = 1e-5
    plate_thickness = 0.025
    wire_thickness = 0.25
    
    dist = 0.25
    
    e_field_density = 0.25
    e_field_scale = 10
    
    def __init__(self, capacitance=1.0, length=1.0, radius=1.0, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.pose = pose
        self.radius = radius
        self.orient = hat(orient)
        self.length = length
        self.wire_len = length - (self.plate_thickness*2 + self.dist)/2
        self.capacitance = capacitance
        self.plate1 = None
        self.plate2 = None
        self.wire1 = None
        self.wire2 = None
        self.e_fields = []
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
        
        side_len = sqrt(self.capacitance*self.dist/e_0 * self.plate_area_factor)*1.1
        
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
            
        x_axis = norm(self.plate1.axis)
        y_axis = norm(cross(x_axis, self.plate1.up))
            
        for x in range(-side_len/2, side_len/2+side_len*self.e_field_density, side_len*self.e_field_density):
            for y in range(-side_len/2, side_len/2+side_len*self.e_field_density, side_len*self.e_field_density):
                a = arrow(
                    pos=self.pose-0.5*(voltage/abs(voltage))*self.orient*(self.dist-self.plate_thickness) + x_axis*x + y_axis*y,
                    axis=(voltage/abs(voltage))*self.orient*(self.dist-self.plate_thickness),
                    color=color.green,
                    round=True,
                    shaftwidth=(abs(voltage)/self.dist)*self.e_field_scale*0.001,
                    headwidth=(abs(voltage)/self.dist)*self.e_field_scale*0.003,
                    )
                self.e_fields.append(a)
                

class Resistor:
    band_spacing_factor = 0.125
    band_thickness_factor = 0.055
    
    power_vector_density = 0.25
    power_scale = 1e5
    

    arrow_despawn_radius = 2.0  # Distance from center to remove arrow
    
    arrow_length = 0.2
    arrow_scale = 0.025
    arrow_speed = 0.5

    def __init__(self, resistance=1.0, length=1.0, body_len=0.4, radius=0.125, wire_radius=0.01, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.resistance = int(resistance)
        self.length = length
        self.radius = radius
        self.wire_radius = wire_radius
        self.pose = pose
        self.orient = hat(orient)
        self.body_len = body_len
        self.body = None
        self.band1 = None
        self.band2 = None
        self.band3 = None
        self.band4 = None
        self.wire1 = None
        self.wire2 = None
        self._emission_timer = 0
        self.arrows = []
        self.render_resistor()
        return
    
    def render_resistor(self):
        if (self.body != None):
            self.body.visible = False
        if (self.band1 != None):
            self.band1.visible = False
        if (self.band2 != None):
            self.band2.visible = False
        if (self.band3 != None):
            self.band3.visible = False
        if (self.band4 != None):
            self.band4.visible = False
        if (self.wire1 != None):
            self.wire1.visible = False
        if (self.wire2 != None):
            self.wire2.visible = False
            
        bands = self.get_color_bands(self.resistance)
        
        self.body = cylinder(
            pos=self.pose-0.5*self.orient*(self.body_len), axis=self.orient,
            color=RESISTOR, radius=self.radius, 
            length=self.body_len
            )
            
        self.band1 = cylinder(
            pos=self.pose-0.5*self.orient*(self.body_len)+self.orient*self.band_spacing_factor*1*self.body_len,
            axis = self.orient,
            color = bands[0],
            radius = self.radius*1.01,
            length = self.body_len*self.band_thickness_factor
            )
        
        self.band2 = cylinder(
            pos=self.pose-0.5*self.orient*(self.body_len)+self.orient*self.band_spacing_factor*2*self.body_len,
            axis = self.orient,
            color = bands[1],
            radius = self.radius*1.01,
            length = self.body_len*self.band_thickness_factor
            )
        
        self.band3 = cylinder(
            pos=self.pose-0.5*self.orient*(self.body_len)+self.orient*self.band_spacing_factor*3*self.body_len,
            axis = self.orient,
            color = bands[2],
            radius = self.radius*1.01,
            length = self.body_len*self.band_thickness_factor
            )
        
        self.band4 = cylinder(
            pos=self.pose-0.5*self.orient*(self.body_len)+self.orient*self.band_spacing_factor*6*self.body_len,
            axis = self.orient,
            color = bands[3],
            radius = self.radius*1.01,
            length = self.body_len*self.band_thickness_factor
            )
        
        self.wire1 = curve(
            pos=[
                self.pose-0.5*self.orient*self.length,
                self.pose-0.5*self.orient*(self.body_len)
                ],
            radius=self.wire_radius,
            color=ALUMINUM
            )
        
        self.wire2 = curve(
            pos=[
                self.pose+0.5*self.orient*self.body_len,
                self.pose+0.5*self.orient*(self.length)
                ],
            radius=self.wire_radius,
            color=ALUMINUM
            )
        
        return
    
    def get_color_bands(self, resistance):
        e = 0
        while (resistance < 0) or (resistance >= 10):
            if (resistance < 0):
                resistance *= 10
                e -= 1
            else:
                resistance /=10
                e += 1
            
        #if (e == 1): e += 1
        b1 = self.value_to_color(int(resistance))
        b2 = self.value_to_color(int((resistance*10)%10))
        b3 = self.value_to_color(max(e-1, -2))
        b4 = self.value_to_color(-1)
        return [b1, b2, b3, b4]
        
    def value_to_color(self, value):
        if (value == 0):
            return color.black
        elif (value == 1):
            return vec(150/255, 75/255, 0/255)
        elif (value == 2):
            return color.red
        elif (value == 3):
            return color.orange
        elif (value == 4):
            return color.yellow
        elif (value == 5):
            return color.green
        elif (value == 6):
            return color.blue
        elif (value == 7):
            return color.purple
        elif (value == 8):
            return vec(0.75, 0.75, 0.75)
        elif (value == 9):
            return color.white
        elif (value == -1):
            return vec(255/255, 215/255, 0/255)
        elif (value == -2):
            return vec(0.5, 0.5, 0.5)
        return color.black

    def render_power(self, current, dt):
        power = (current ** 2) / self.resistance * self.power_scale
        emission_rate = self.power_vector_density * power

        self._emission_timer += dt
        new_arrows = int(self._emission_timer * emission_rate)
        self._emission_timer -= new_arrows / emission_rate if emission_rate else 0

        for _ in range(new_arrows):
            dir = self.random_unit_vector()
            start_pos = self.pose 
            arr = arrow(
                pos=start_pos,
                axis=dir * self.arrow_length,
                color=color.red,
                shaftwidth=self.arrow_scale,
                headwidth=self.arrow_scale * 2,
                emissive=True
            )
            arr.velocity = dir * self.arrow_speed
            arr.origin = vector(start_pos)
            self.arrows.append(arr)

        for arr in self.arrows[:]:
            arr.pos += arr.velocity * dt
            displacement = mag(arr.pos - arr.origin)
            fade = max(0, 1 - displacement / self.arrow_despawn_radius)

            arr.axis = norm(arr.velocity) * self.arrow_length * fade
            arr.color = vec(fade, 0, 0)
            arr.shininess = fade
            arr.opacity = fade

            if displacement > self.arrow_despawn_radius:
                arr.visible = False
                self.arrows.remove(arr)

    def random_unit_vector(self):
        theta = 2 * pi * random()
        phi = pi * random()
        return vec(
            sin(phi) * cos(theta),
            sin(phi) * sin(theta),
            cos(phi)
        )

    def random_point_on_surface(self):
        t = (random() - 0.5) * self.body_len
        a = 2 * pi * random()
        r = self.radius * 1.05
        up = self.get_perpendicular(self.orient)
        right = cross(self.orient, up)
        return self.pose + self.orient * t + up * r * cos(a) + right * r * sin(a)

    def get_perpendicular(self, v):
        if v.x != 0 or v.y != 0:
            return vec(-v.y, v.x, 0)
        else:
            return vec(0, -v.z, v.y)
        
        
class Wire:
    current_scale = 10
    charge_spacing = 0.1
    opacity = 0.5
    step_t = 0
    #charges = []
    slow_factor = 1
    
    def __init__(self, length=1.0, wire_radius=0.01, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.length = length
        self.wire_radius=wire_radius
        self.pose = pose
        self.orient=hat(orient)
        self.step_t = 0
        self.charges = []
        self.body = None
        self.end1 = None
        self.end2 = None
        self.render_wire()
        return
    
    def render_wire(self):
        if (self.body != None):
            self.body.visible = False
        if (self.end1 != None):
            self.end1.visible = False
        if (self.end2 != None):
            self.end2.visible = False
        
        self.body = cylinder(
            pos=self.pose-0.5*self.length*self.orient, axis = self.orient,
            length = self.length, radius = self.wire_radius,
            color = ALUMINUM, opacity=self.opacity
            )
        
        self.end1 = sphere(
            pos=self.pose-0.5*self.length*self.orient, 
            radius = self.wire_radius,
            color = ALUMINUM, opacity=self.opacity
            )
        
        self.end2 = sphere(
            pos=self.pose+0.5*self.length*self.orient, 
            radius = self.wire_radius,
            color = ALUMINUM, opacity=self.opacity
            )
            
    def render_current(self, current):
        if (len(self.charges) > 0):
            for c in self.charges:
                c.visible=False
            self.charges.clear()
            
        
        for i in range(-self.length/2, self.length/2 + self.charge_spacing, self.charge_spacing):
            chargepose = self.pose + i*self.orient + self.orient*self.step_t*self.charge_spacing/10
            if (dot(chargepose - (self.pose - 0.5*self.orient*self.length), self.orient) >= 0) and (dot(chargepose - (self.pose + 0.5*self.orient*self.length), -self.orient) >= 0):
                charge = sphere(
                    pos=chargepose,
                    radius = self.wire_radius*0.9,
                    color=color.yellow, emissive=True
                    )
                self.charges.append(charge)
        
        self.step_t += (current)*self.current_scale*self.slow_factor
        if (abs(self.step_t) >= 10):
            self.step_t = 0
            
        return
    
    

def iRK4(q,i,R,L,C,dt):
    def f1(q, i):
        return i
    def f2(q, i):
        return -(R*i/L+q/L/C)
        
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

    
def main():
    #Var
    R = 10
    L = 1
    C = 10e-6
    V = 10
    q = C*V
    i = 0
    dt = 0.00001
    t = 0
    simulation_speed = 1000
    time_step = 1
    
    running = False
    
    #Functions for input
    
    # Create sliders and buttons
    wtext(text="Resistance: \n")
    resistance_slider = slider( bind=handle_evt, min=1, max=1000, step = 1, id = "resistance")
    wt1=wtext(text='{:1.2f}'.format(resistance_slider.value))
    scene.append_to_caption(' ohms\n')
    wtext(text='<br>')
    
    wtext(text="Inductance: \n")
    inductance_slider = slider( bind=handle_evt, min=10, max=1000, step = 1, id = "inductance")
    wt2=wtext(text='{:1.2f}'.format(inductance_slider.value))
    scene.append_to_caption(' millihenrys\n')
    wtext(text='<br>')
    
    wtext(text="Capacitance: \n")
    capacitance_slider = slider( bind=handle_evt, min=10, max=1000, step = 1, id = "capacitance")
    wt3=wtext(text='{:1.2f}'.format(capacitance_slider.value))
    scene.append_to_caption(' microfarads\n')
    wtext(text='<br>')
    
    wtext(text="Vary the Capacitor Voltage: \n")
    capacitor_voltage_slider = slider( bind=handle_evt, min=1, max=50, step = 1, id = "capacitor_voltage")
    wt4=wtext(text='{:1.2f}'.format(capacitor_voltage_slider.value))
    scene.append_to_caption(' volts\n')
    wtext(text='<br>')
    
    wtext(text="Vary the Simulation Speed: \n")
    simulation_speed_slider = slider( bind=handle_evt, min=10, max=100, step = 1, id = "simulation_speed")
    wt5=wtext(text='{:1.2f}'.format(simulation_speed_slider.value))
    scene.append_to_caption(' \n')
    wtext(text='<br>')
    
    wtext(text="Vary the Time Step: \n")
    time_step_slider = slider( bind=handle_evt, min=1, max=100, step = 1, id = "time_step")
    wt6=wtext(text='{:1.2f}'.format(time_step_slider.value))
    scene.append_to_caption(' microseconds\n')
    wtext(text='<br>')
    
    run = button(text="Run", bind=run)
    wtext(text='<br>')
    wtext(text='<br>')
    
    button(bind=reset, text="Reset")
    
    #define classes for objects
    c_obj = Capacitor(capacitance=C, length=0.5, radius=WIRE_RADIUS, pose=vec(-2,0,0))
    l_obj = Inductor(inductance=L, length=1.0, radius=0.5, wire_radius = WIRE_RADIUS, pose=vec(2,0,0))
    r_obj = Resistor(resistance=R, length=1.0, body_len=0.5, radius=0.125, wire_radius=WIRE_RADIUS, pose=vec(0, 1, 0), orient=vec(1, 0, 0))
    wires = []
    wires.append(Wire(length=4.0, wire_radius=WIRE_RADIUS, pose=vec(0, -1, 0), orient=vec(1, 0, 0)))
    wires.append(Wire(length=1.5, wire_radius=WIRE_RADIUS, pose=vec(-1.25, 1, 0), orient=vec(-1, 0, 0)))
    wires.append(Wire(length=1.5, wire_radius=WIRE_RADIUS, pose=vec(1.25, 1, 0), orient=vec(-1, 0, 0)))
    wires.append(Wire(length=0.75, wire_radius=WIRE_RADIUS, pose=vec(-2, 0.375 + 0.25, 0), orient=vec(0, -1, 0)))
    wires.append(Wire(length=0.75, wire_radius=WIRE_RADIUS, pose=vec(-2, -(0.375 + 0.25), 0), orient=vec(0, -1, 0)))
    wires.append(Wire(length=0.5, wire_radius=WIRE_RADIUS, pose=vec(2, -0.75, 0), orient=vec(0, 1, 0)))
    wires.append(Wire(length=0.5, wire_radius=WIRE_RADIUS, pose=vec(2, 0.75, 0), orient=vec(0, 1, 0)))
    
    #init
    for w in wires:
        w.render_current(i)
    c_obj.render_e_fields(V)
    
    def handle_evt(evt):
        global R,L,C,q,V,simulation_speed,dt
        if evt.id is "resistance":
            wt1.text = '{:1.2f}'.format(resistance_slider.value)
            R = evt.value
            r_obj.resistance = int(evt.value)
            r_obj.render_resistor()
            return
        
        else if evt.id is "inductance":
            wt2.text = '{:1.2f}'.format(inductance_slider.value)
            L = evt.value*1e-3
            l_obj.inductance = evt.value*1e-3
            l_obj.render_coil()
            return
        
        else if evt.id is "capacitance":
            wt3.text = '{:1.2f}'.format(capacitance_slider.value)
            C = evt.value*1e-6
            c_obj.capacitance = evt.value * 1e-6
            c_obj.render_plates()
            c_obj.render_e_fields(-V)
            return
        
        else if evt.id is "capacitor_voltage":
            wt4.text = '{:1.2f}'.format(capacitor_voltage_slider.value)
            V = evt.value
            q = C*V
            c_obj.render_e_fields(-V)
            return
        
        else if evt.id is "simulation_speed":
            wt5.text = '{:1.2f}'.format(simulation_speed_slider.value)
            simulation_speed = evt.value * 100
            return
        
        else if evt.id is "time_step":
            wt6.text = '{:1.2f}'.format(time_step_slider.value)
            dt = evt.value * 1e-6
            return
        
        return
    
    def run(r):
        global running
        running = not running
        if running: r.text = "Pause"
        else: r.text = "Run"
        return
    
    def reset():
        global R,L,C,V,q,i,dt,t
        global gc1,gc2,gc3,gc4
        gc1.delete()
        gc2.delete()
        gc3.delete()
        gc4.delete()
        q = C*V
        i = 0
        t = 0
        l_obj.render_b_field(0)
        c_obj.render_e_fields(V)
        for w in wires:
            w.render_current(0)
        return
      
    g1 = graph(title='Current vs Time', xtitle='Time (s)', ytitle='Current (A)', width=400, height=300, align='left')
    gc1 = gcurve(color=color.red,graph=g1)
    
    g2 = graph(title='Voltage vs Time for Resistor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
    gc2 = gcurve(color=color.green,graph=g2)
    
    g3 = graph(title='Voltage vs Time for Inductor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
    gc3 = gcurve(color=color.blue,graph=g3)
    i2=0
    
    g4 = graph(title='Voltage vs Time for Capacitor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
    gc4 = gcurve(color=color.yellow,graph=g4)
    
    while True:
        rate(simulation_speed)
        if running:
            i2=i
            q,i = iRK4(q,i,R,L,C,dt)
            gc1.plot(t,i)
            gc2.plot(t,i*R)
            gc3.plot(t,(i-i2)/dt*L)
            gc4.plot(t,q/C)
            t += dt
            
            c_obj.render_e_fields(-i*R)
            l_obj.render_b_field(i)
            r_obj.render_power(i, 0.01)
            
            for w in wires:
                w.render_current(i)
            

if __name__ == "__main__":
    main()

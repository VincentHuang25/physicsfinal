Web VPython 3.2

COPPER = vec(184/255, 115/255, 51/255)
ALUMINUM = vec(211/255, 211/255, 211/255)

u_0 = 4*pi*10e-7
e_0 = 8.85*10e-12

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
                axis=self.pose + self.orient*current*0.05,
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
    
    dist = 0.1
    e_fields = []
    def __init__(self, capacitance=1.0, pose=vec(0,0,0), orient=vec(0,1,0)):
        self.pose = pose
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
            height=0.01, length=side_len, width=side_len,
            up = self.orient,
            color = ALUMINUM
            )
            
        self.plate2 = box(
            pos=self.pose-0.5*self.orient*self.dist, 
            height=0.01, length=side_len, width=side_len,
            up = -self.orient,
            color = ALUMINUM
            )
    
class Resistor:
    def __init__(self):
        return
    
class Wire:
    def __init__(self):
        return


def main():
    c = Capacitor(capactiance=10e-6)

if __name__ == "__main__":
    main()

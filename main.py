Web VPython 3.2

u_0 = 4*pi*10e-7

class Inductor:
    b_field_render_range = 1.0 #Multiple of coil radius
    b_field_density = 0.1
    thickness_factor = 0.025
    coil_down_factor = 0.1
    mesh = None
    b_fields = []
    
    def __init__(self, inductance=1.0, length=1.0, radius=1.0, pose=vec(0,0,0), orient=vec(0,0,1)):
        self.inductance = inductance
        self.length = length
        self.radius = radius
        self.pose = pose
        self.orient = orient
        self.render_coil()
        return
    
    def get_n_coils(self, inductance, length, radius):
        return round(sqrt((inductance*length)/(u_0*(radius**2)*pi))*self.coil_down_factor)
        
    def render_coil(self):
        #delete old coil
        if (self.mesh != None):
            self.mesh.visible = False
    
        self.mesh = helix()
        self.mesh.pos = self.pose-0.5*self.orient
        self.mesh.axis = self.pose+0.5*self.orient
        self.mesh.radius = self.radius
        self.mesh.length = self.length
        self.mesh.thickness = self.radius*self.thickness_factor
        self.mesh.coils = self.get_n_coils(self.inductance, self.length, self.radius)
        return
    
    def render_b_field(self, current):
        #delete old b_fields
        if (len(self.b_fields) != 0):
            for b in self.b_fields:
                b.visible = False
            b_fields.clear()
        
        
        
        
        return
    
    
    

class Capacitor:
    def __init__(self):
        return
    
class Resistor:
    def __init__(self):
        return
    
class Wire:
    def __init__(self):
        return


def main():
    e = Inductor(1, 2)
    GOON = 0.1
    pass

if __name__ == "__main__":
    main()

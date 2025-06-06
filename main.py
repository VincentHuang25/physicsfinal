Web VPython 3.2    

R = 10
L = 10
C = 10
V = 10
q = C*V
i = 0
dt = 0.000001
t = 0
simulation_speed = 1000
time_step = 1

wtext(text="Vary the Resistance: \n")
resistance_slider = slider( bind=resistance_set, min=10, max=500, step = 1, id = "resistance")
wt1=wtext(text='{:1.2f}'.format(resistance_slider.value))
scene.append_to_caption(' ohms\n')
wtext(text='<br>')

wtext(text="Vary the Inductance: \n")
inductance_slider = slider( bind=inductance_set, min=10, max=1000, step = 1, id = "inductance")
wt2=wtext(text='{:1.2f}'.format(inductance_slider.value))
scene.append_to_caption(' millihenrys\n')
wtext(text='<br>')

wtext(text="Vary the Capacitance: \n")
capacitance_slider = slider( bind=capacitance_set, min=10, max=1000, step = 1, id = "capacitance")
wt3=wtext(text='{:1.2f}'.format(capacitance_slider.value))
scene.append_to_caption(' nanofarads\n')
wtext(text='<br>')

wtext(text="Vary the Capacitor Voltage: \n")
capacitor_voltage_slider = slider( bind=capacitor_voltage_set, min=10, max=500, step = 1, id = "capacitor_voltage")
wt4=wtext(text='{:1.2f}'.format(capacitor_voltage_slider.value))
scene.append_to_caption(' volts\n')
wtext(text='<br>')

wtext(text="Vary the Simulation Speed: \n")
simulation_speed_slider = slider( bind=simulation_speed_set, min=10, max=100, step = 1, id = "simulation_speed")
wt5=wtext(text='{:1.2f}'.format(simulation_speed_slider.value))
scene.append_to_caption(' \n')
wtext(text='<br>')

wtext(text="Vary the Time Step: \n")
time_step_slider = slider( bind=time_step_set, min=1, max=100, step = 1, id = "time_step")
wt6=wtext(text='{:1.2f}'.format(time_step_slider.value))
scene.append_to_caption(' microseconds\n')
wtext(text='<br>')

def resistance_set(evt):
    global R
    wt1.text = '{:1.2f}'.format(resistance_slider.value)
    if evt.id is "resistance":
        R = evt.value

def inductance_set(evt):
    global L
    wt2.text = '{:1.2f}'.format(inductance_slider.value)
    if evt.id is "inductance":
        L = evt.value * 1e-3

def capacitance_set(evt):
    global C
    wt3.text = '{:1.2f}'.format(capacitance_slider.value)
    if evt.id is "capacitance":
        C = evt.value * 1e-9

def capacitor_voltage_set(evt):
    global V
    global C
    global q
    wt4.text = '{:1.2f}'.format(capacitor_voltage_slider.value)
    if evt.id is "capacitor_voltage":
        V = evt.value
        q = C*V

def simulation_speed_set(evt):
    global simulation_speed
    wt5.text = '{:1.2f}'.format(simulation_speed_slider.value)
    if evt.id is "simulation_speed":
        simulation_speed = evt.value * 100

def time_step_set(evt):
    global dt
    wt6.text = '{:1.2f}'.format(time_step_slider.value)
    if evt.id is "time_step":
        dt = evt.value * 1e-6
        
running = False

def Run(r):
    global reset
    reset = False
    global running
    running = not running
    if running: r.text = "Pause"
    else: r.text = "Run"

run = button(text="Run", bind=Run)

wtext(text='<br>')
wtext(text='<br>')

reset = False

def Reset():
    run.text = "Run"
    global running
    running = False

    global gc1,gc2,gc3,gc4,i2
    
    gc1.delete()
    gc2.delete()
    gc3.delete()
    gc4.delete()

    i2=0
    
    global R,L,C,V,q,i,dt,t
    q = C*V
    i = 0
    dt = 0.000001
    t = 0
    global reset
    reset = True
    return

button(bind=Reset, text="Reset")

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
    
g1 = graph(title='Current vs Time', xtitle='Time (s)', ytitle='Current (A)', width=400, height=300, align='left')
gc1 = gcurve(color=color.red,graph=g1)

g2 = graph(title='Voltage vs Time for Resistor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
gc2 = gcurve(color=color.green,graph=g2)

g3 = graph(title='Voltage vs Time for Inductor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
gc3 = gcurve(color=color.blue,graph=g3)
i2=0

g4 = graph(title='Voltage vs Time for Capacitor', xtitle='Time (s)', ytitle='Voltage (V)', width=400, height=300, align='left')
gc4 = gcurve(color=color.yellow,graph=g4)

while not reset:
    rate(simulation_speed)
    if running:
        i2=i
        q,i = iRK4(q,i,dt)
        gc1.plot(t,i)
        gc2.plot(t,i*R)
        gc3.plot(t,(i-i2)/dt*L)
        gc4.plot(t,q/C)
        t += dt

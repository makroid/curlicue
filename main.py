from gi.repository import Gtk

import matplotlib.pyplot as plt
import numpy as np
from scipy import weave
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


class CurlicueWindow(Gtk.Window):

    def __init__(self):
        """ perform all initialization """
        Gtk.Window.__init__(self, title="curlicue")
        self.set_size_request(300, 200)

        self.timeout_id = None
        self.iter_func  = "s *i*i"
        self.max_nsteps = 10000
        self.add_steps  = 50
        self.nsteps     = 2000
        self.s          =  (np.sqrt(5) + 1.0) / 2.0        
        self.stepsize   = 1
        
        self.bg_color   = '#003399'
        self.line_color = 'red'
        self.line_width = 2
        
        self.steps = np.arange(start=1, stop=self.max_nsteps)

        self.x = np.zeros(self.max_nsteps)
        self.y = np.zeros(self.max_nsteps)

        self.generate_plot_figure_canvas()
        self.generate_layout()

        self.update_plot(None)
        
    
    def generate_plot_figure_canvas(self):
        self.fig = plt.figure(figsize=(5,5), dpi=100)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])        
        
        self.fig.add_axes(self.ax)
        self.ax.plot(self.x, self.y, lw=self.line_width, color=self.line_color)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(600, 600)
        
        
    def generate_layout(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        
        self.entry = Gtk.Entry()
        self.entry.set_text(self.iter_func)
        self.entry.connect("activate", self.on_press_enter)
        
        hbox = Gtk.Box()
        hbox.pack_start(self.entry, True, True, 5)
        vbox.pack_start(hbox, False, True, 5)

        hbox = Gtk.Box()
        vbox.pack_start(hbox, True, True, 0)
        
        hbox.pack_start(self.canvas, True, True, 0)
        
        adjustment = Gtk.Adjustment(self.s, -10, 10, 0.05, 0.05, 0)
        adjustment.set_step_increment(0.05)

        self.scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.scale.set_digits(5)
        self.scale.connect("value-changed", self.update_plot)
        
        spinAdjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.spin_button = Gtk.SpinButton()
        self.spin_button.set_adjustment(spinAdjustment)
        self.spin_button.set_range(0, self.max_nsteps)
        self.spin_button.set_value(self.nsteps)
        self.spin_button.set_increments(self.add_steps, 100)
        self.spin_button.connect("value-changed", self.value_changed_nsteps)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)        
        hbox.pack_start(Gtk.Label("s:   "), False, True, 10)
        hbox.pack_start(self.scale, True, True, 10)
        vbox.pack_start(hbox, False, True, 10)
        
                
        bottom_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        bottom_hbox.pack_start(Gtk.Label("Iterations: "), False, True, 10)        
        bottom_hbox.pack_start(self.spin_button, False, True, 0)
        
        vbox.pack_start(bottom_hbox, False, True, 0)
        

    def update_plot(self, event):
        self.s = self.scale.get_value()
        print ("s=%.10f" % self.s)
        
        self.compile_exec( self.generate_func_c_code() )
        self.ax.cla()
        self.ax.set_axis_bgcolor(self.bg_color)
        self.ax.plot(self.x[:self.nsteps], self.y[:self.nsteps], lw=self.line_width, color=self.line_color)
        self.fig.canvas.draw_idle()
        
        
    def value_changed_nsteps(self, event):
        self.nsteps = self.spin_button.get_value()
        self.update_plot(None)
        
    
    def on_press_enter(self, event):
        self.iter_func = self.entry.get_text()
        self.update_plot(None)
        
            
    def compile_exec(self, func_c_code):
        x = self.x
        y = self.y
        s = self.s        
        stepsize = self.stepsize
        nsteps = self.nsteps
        weave.inline(func_c_code, ['x', 'y', 's', 'stepsize', 'nsteps'])
        
        
    def generate_func_c_code(self): 
        code = r'''
            float theta = 0.0;
            int i;            
            for (i=1; i<(int)nsteps; i++) {
                theta = 2.0 * M_PI * ( TOREPLACE ) ;
                X1(i) = X1(i-1) + stepsize * cos(theta);
                Y1(i) = Y1(i-1) + stepsize * sin(theta);
            }'''
        code = code.replace("TOREPLACE", self.iter_func)                
        return code
    
        
curlicue_window = CurlicueWindow()
curlicue_window.connect("delete-event", Gtk.main_quit)

curlicue_window.show_all()
Gtk.main()
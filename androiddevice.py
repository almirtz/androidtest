# -*- coding: utf-8 -*-
class Device:
    ostype = "ANDROID"
    
    def __init__(self):
        self.name = self.ostype
        self.screen = Screen(800, 480, 160)
 
    def dp_to_px(self,  dp):
        dp = int(dp)
        return int(dp * self.screen.density/160)
        
    def px_to_dp(self, px):
        px = int(px)
        return int(px*160/self.screen.density)
        
#------------------------------------------------------------------------------
class DeviceHTCM8(Device):
    
    def __init__(self):
        super().__init__()
        self.name = "HTC One M8"
        self.screen = Screen(0x640, 0xaf0, 240)

    def get_screen_matrix_size(self):
        return int(self.screen.xe), int(self.screen.ye)
    
    
#------------------------------------------------------------------------------
class Screen():
    
    def __init__(self, width, height, density_dpi):
        self.xs = 0
        self.ys = 0
        self.xe = width // density_dpi
        self.ye = height // density_dpi
        self.density = density_dpi
        
    

#------------------------------------------------------------------------------
#device=DeviceHTCM8()
#w,h = device.get_screen_matrix()
#print(w,h)        
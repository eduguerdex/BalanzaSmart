import screen_brightness_control as sbc 
  
print(sbc.get_brightness()) 
  
sbc.fade_brightness(0) 
print(sbc.get_brightness()) 
  
sbc.fade_brightness(75, start = 0) 
print(sbc.get_brightness()) 
  
sbc.fade_brightness(100, increment = 10) 
print(sbc.get_brightness())
from phue import Bridge

class hue:
    def __init__(self):
        self.bridge = Bridge('192.168.0.102')
        self.bridge.connect()
        self.lights = self.bridge.lights
        print(self.lights)

    def power_controll(self,bulb_num,power):
        try:
            if power == "on":
                self.lights[int(bulb_num)-1].on = True
            else:
                self.lights[int(bulb_num)-1].on = False
        except Exception as e:
            print("error a occur with ",e)
    def is_power_on(self):
        return (self.lights[0].on and self.lights[1].on and self.lights[2].on)

    def brightness_controll(self,bulb_num,brightness):
        try:
            self.lights[int(bulb_num)-1].brightness  = int(brightness)
        except Exception as e:
            print("error occur with ",e)

    def color_controll(self,bulb_num,colors_x,colors_y):
        try:
            self.lights[int(bulb_num)-1].xy = [float(colors_x),float(colors_y)]
        except Exception as e:
            print("error occur with ",e)

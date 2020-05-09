import logging
import random
import os
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi

class EXP(plugins.Plugin):
    __author__ = 'GaelicThunder'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Get exp every time a handshake get captured.'
    
    
    def __init__(self):
        self.percent=0
        self.bar=" "
        self.expgained=0
        self.exp=1
        self.lv=1
        self.cwd = os.getcwd()
        self.cwd = self.cwd+"/exp.txt"
        logging.info(self.cwd)
        if os.path.exists("exp.txt"):
            outfile= open(self.cwd, 'r+')
            self.exp = int(outfile.readline())
            self.lv = int(outfile.readline())
            outfile.close()
        else:
            outfile=open(self.cwd, 'w')
            print(self.exp,file=outfile)
            print(self.lv,file=outfile)
            outfile.close()
        self.expneeded=int((100*(self.lv*self.lv*self.lv))/5)

        
    def on_loaded(self):
        logging.info("Exp plugin loaded for %s" % self.options['device'])
        
        
    def on_ready(self, agent):
        if os.path.exists(self.options['device']):
            logging.info("enabling exp module for %s" % self.options['device'])
        
   
    def Save(self):
        outfile=open(self.cwd, 'w')
        print(self.exp,file=outfile)
        print(self.lv,file=outfile)
        outfile.close()
  
    
    def on_ui_setup(self, ui):
        ui.add_element('Lv', LabeledValue(color=BLACK, label='Lv', value=0, position=(ui.width() / 2 - 125, 95),
                                           label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('Exp', LabeledValue(color=BLACK, label='Exp', value=0, position=(ui.width() / 2 - 85, 95),
                                           label_font=fonts.Bold, text_font=fonts.Medium))
    def on_ui_update(self, ui):
        self.percent=int((self.exp/self.expneeded)*100)
        self.bar="╷          ╷"
        self.expneeded=int((100*(self.lv*self.lv*self.lv))/200)
        if self.percent<10:
            self.bar="╷          ╷"
        if self.percent>9 and self.percent<20:
            self.bar="╷▄         ╷"
        if self.percent>19 and self.percent<30:
            self.bar="╷▄▄        ╷"
        if self.percent>29 and self.percent<40:
            self.bar="╷▄▄▄       ╷"
        if self.percent>39 and self.percent<50:
            self.bar="╷▄▄▄▄      ╷"
        if self.percent>49 and self.percent<60:
            self.bar="╷▄▄▄▄▄     ╷"
        if self.percent>59 and self.percent<70:
            self.bar="╷▄▄▄▄▄▄    ╷"
        if self.percent>69 and self.percent<80:
            self.bar="╷▄▄▄▄▄▄▄   ╷"
        if self.percent>79 and self.percent<90:
            self.bar="╷▄▄▄▄▄▄▄▄  ╷"
        if self.percent>89 and self.percent<100:
            self.bar="╷▄▄▄▄▄▄▄▄▄▄╷"
        ui.set('Lv', "%d" % self.lv)
        ui.set('Exp', "%s" % self.bar)
        self.Save()
        
    def exp_check(self):
        logging.info("EXP CHECK")
        self.mainpoint=self.point+self.expgained
        if self.exp>=self.expneeded:
            self.lv=self.lv+1
            self.expneeded=int((100*(self.lv*self.lv*self.lv))/200)

        
    def on_association(self, agent, access_point):
        self.expgained=self.exp+(1*self.mod)
        self.exp=self.expgained
        self.exp_check()
        
    def on_deauthentication(self, agent, access_point, client_station):
        self.expgained=self.exp+(2*self.mod)
        self.exp=self.expgained
        self.exp_check()
        
    def on_handshake(self, agent, filename, access_point, client_station):
        self.expgained=self.exp+(3*self.mod)
        self.exp=self.expgained
        self.exp_check()
        
    def on_ai_best_reward(self, agent, reward):
        self.expgained=self.exp+(5*self.mod)
        self.exp=self.expgained
        self.exp_check()
        

        
        
        
        
        
        
        
        
        
     

import logging
import os
import random
import json

import pwnagotchi
import pwnagotchi.agent
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK


class EXP(plugins.Plugin):
    __author__ = 'GaelicThunder'
    __version__ = '1.0.3'
    __license__ = 'GPL3'
    __description__ = 'Get exp every time a handshake get captured.'

    MULTIPLIER_ASSOCIATION = 1
    MULTIPLIER_DEAUTH = 2
    MULTIPLIER_HANDSHAKE = 3
    MULTIPLIER_AI_BEST_REWARD = 5
    TAG = "[EXP Plugin]"

    #Attention number masking
    def LogInfo(self, text):
        logging.info(self.TAG + " " +text)
    
    #Attention number masking
    def LogDebug(self, text):
        logging.debug(self.TAG + " " +text)
    
    
    def __init__(self):
        self.percent=0
        self.bar=" "
        #never used
        #self.expgained=0
        self.calculateInitialXP = False
        self.exp=1
        self.lv=1
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.cwd = self.cwd+"/exp.txt"
        logging.info(self.cwd)

        #TODO: rework
        if os.path.exists(self.cwd):
            self.LogDebug("file exists")
            outfile= open(self.cwd, 'r+')
            self.exp = int(outfile.readline())
            self.lv = int(outfile.readline())
            outfile.close()
        else:
            self.LogDebug("file createt")
            outfile=open(self.cwd, 'w')
            print(self.exp,file=outfile)
            print(self.lv,file=outfile)
            outfile.close()
        
        if self.exp == 1:
            self.calculateInitialXP = True
            
        #This is a different value
        #self.expneeded=int((100*(self.lv**3))/5)
        self.expneeded = self.calcExpNeeded(self.lv)
        
    def on_loaded(self):
        #logging.info("Exp plugin loaded for %s" % self.options['device'])
        self.LogInfo("Plugin Loaded")
        
   
    def Save(self):
        self.LogDebug('Saving Exp')
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
        self.expneeded=self.calcExpNeeded(self.lv)
        self.percent=int((self.exp/self.expneeded)*100)
        self.bar="╷          ╷"     
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


    def calcExpNeeded(self, level):
        #if the pwnagotchi is lvl <1 it causes the keys to be deleted
        if level == 1:
            return 1
        return int((level**3)/2)
    


    def exp_check(self, agent):
        self.LogDebug("EXP CHECK")
        if self.exp>=self.expneeded:
            self.exp=1
            self.lv=self.lv+1
            self.expneeded=self.calcExpNeeded(self.lv)
            #TODO: do propery
            #get Excited ;-)
            agent.set_excited()

    def parseSessionStats(self):
        sum = 0
        dir = pwnagotchi.config['main']['plugins']['session-stats']['save_directory']
        #TODO: remove
        #dir="/var/tmp/test1"
        self.LogInfo("Session-Stats dir: " + dir)
        #TODO: Write Code here
        for filename in os.listdir(dir):
            self.LogInfo("Parsing " + filename + "...")
            if filename.endswith(".json") & filename.startswith("stats"):
                try:
                    sum += self.parseSessionStatsFile(os.path.join(dir,filename))
                except:
                    self.LogInfo("ERROR parsing File: "+ filename)
                
        return sum

    def parseSessionStatsFile(self, path):
        sum = 0
        deauths = 0
        handshakes = 0
        associations = 0
        with open(path) as json_file:
            data = json.load(json_file)
            for entry in data["data"]:
                deauths += data["data"][entry]["num_deauths"]
                handshakes += data["data"][entry]["num_handshakes"]
                associations += data["data"][entry]["num_associations"]
            

        sum += deauths * self.MULTIPLIER_DEAUTH
        sum += handshakes * self.MULTIPLIER_HANDSHAKE
        sum += associations * self.MULTIPLIER_ASSOCIATION

        return sum


    #if initial sum is 0, we try to parse it
    def calculateInitialSum(self, agent):
        sessionStatsActive = False
        sum = 0
        #check if session stats is loaded
        for plugin in pwnagotchi.plugins.loaded:
            if plugin == "session-stats":
                sessionStatsActive = True
                break
        
        if sessionStatsActive:
            try:
                self.LogInfo("parsing session-stats")
                sum = self.parseSessionStats()
            except:
                self.LogInfo("Error parsing session-stats")
            
            
        else:
            self.LogInfo("parsing last session")
            sum = self.lastSessionPoints(agent)

        self.LogInfo(str(sum) + " Points calculated")
        return sum


        
    #Get Last Sessions Points
    def lastSessionPoints(self, agent):
        summary = 0
        summary += agent.LastSession.handshakes * self.MULTIPLIER_HANDSHAKE
        summary += agent.LastSession.associated * self.MULTIPLIER_ASSOCIATION
        summary += agent.LastSession.deauthed * self.MULTIPLIER_DEAUTH
        return summary

    
    #Helper function to calculate multiple Levels from a sum of EXPs
    def calcLevelFromSum(self, sum, agent):
        sum1 = sum
        level = 1
        while sum1 > self.calcExpNeeded(level):
            sum1 -= self.calcExpNeeded(level)
            level += 1         
        self.lv = level
        self.exp = sum1
        self.expneeded = self.calcExpNeeded(level) - sum1
        if level > 1:
            #TODO: do propery
            #get Excited ;-)
            agent.set_excited()

    #Event Handling
    def on_association(self, agent, access_point):
        self.exp += self.MULTIPLIER_ASSOCIATION
        self.exp_check(agent)
        self.Save()
        
    def on_deauthentication(self, agent, access_point, client_station):
        self.exp += self.MULTIPLIER_DEAUTH
        self.exp_check(agent)
        self.Save()
        
    def on_handshake(self, agent, filename, access_point, client_station):
        self.exp += self.MULTIPLIER_HANDSHAKE
        self.exp_check(agent)
        self.Save()
        
    def on_ai_best_reward(self, agent, reward):
        self.exp += self.MULTIPLIER_AI_BEST_REWARD
        self.exp_check(agent)
        self.Save()

    def on_ready(self, agent):
        if self.calculateInitialXP:
            self.LogInfo("Initial point calculation")
            sum = self.calculateInitialSum(agent)
            self.calcLevelFromSum(sum, agent)
            self.Save()
                

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from win32api import GetSystemMetrics
from datetime import datetime, timedelta
import sys
import time

class StartUpWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    breakTimeValue = NumericProperty(10)
    pass

class SettingsWindow(Screen):
    pass

class BreakWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Window.borderless = True
        Window.clearcolor = (5/255, 45/255, 60/255, 1)    # app background color
        Window.size = (500, 400)                          # size of entire app window
        Window.top = (GetSystemMetrics(1)/2) - 225
        Window.left = (GetSystemMetrics(0)/2) - 250

        self.startTime = datetime.now()

        # default settings
        self.alarmActive = True
        self.quackActive = True
        self.checkBackTime = 15
        self.devModeMultiplier = 60

        # app quacks on launch
        self.playSound_quack()

        return Builder.load_file("../Kivy/my.kv")

    def updateTimeWorked(self, label):
        timeWorked = str(datetime.now() - self.startTime)
        hours = timeWorked[0:1]
        if timeWorked[2:3] == "0":
            minutes = timeWorked[3:4]
        else:
            minutes = timeWorked[2:4]

        if hours != "1" and minutes != "1":
            label.text = "Just Checking in!\nIt has been a while since your last break\n\n\nTotal Time Worked:\n" + hours + " hours and " + minutes + " minutes"
        elif hours != "1" and minutes == "1":
            label.text = "Just Checking in!\nIt has been a while since your last break\n\n\nTotal Time Worked:\n" + hours + " hours and " + minutes + " minute"
        elif hours == "1" and minutes != "1":
            label.text = "Just Checking in!\nIt has been a while since your last break\n\n\nTotal Time Worked:\n" + hours + " hour and " + minutes + " minutes"
        elif hours == "1" and minutes == "1":
            label.text = "Just Checking in!\nIt has been a while since your last break\n\n\nTotal Time Worked:\n" + hours + " hour and " + minutes + " minute"

    def alarm_switch(self, switchObject, switchValue, labelId):
        if(switchValue):
            labelId.text = "Alarm Enabled"
            self.alarmActive = True
        else:
            labelId.text = "Alarm Disabled"
            self.alarmActive = False

    def quack_switch(self, switchObject, switchValue, labelId):
        if(switchValue):
            labelId.text = "Quacks Enabled"
            self.quackActive = True
        else:
            labelId.text = "Quacks Disabled"
            self.quackActive = False

    def dev_switch(self, switchObject, switchValue, labelId):
        if (switchValue):
            labelId.text = "Developer Mode Enabled"
            self.devModeMultiplier = 1
        else:
            labelId.text = "Developer Mode Disabled"
            self.devModeMultiplier = 60

    def closeApp_pressed(self, id):
        id.source = "../Assets/close_pressed.png"

    def closeApp_released(self, id):
        id.source = "../Assets/close.png"
        quit()

    def options_pressed(self, id):
        id.source = "../Assets/gear_pressed.png"

    def options_released(self, id):
        id.source = "../Assets/gear.png"

    # alarm sound effect
    def playSound_alarm(self):
        if self.alarmActive:
            sound = SoundLoader.load("../Assets/alarmclock_sound.wav")
            if sound:
                sound.play()

    # quack sound effect
    def playSound_quack(self):
        if self.quackActive:
            sound = SoundLoader.load("../Assets/duckquack_sound.wav")
            if sound:
                sound.play()

    def initTimeLeftLabel(self, labelId):
        global timeLeftLabel
        timeLeftLabel = labelId

    # behavior for 'break' action
    def timedBreak(self, time):
        time = time * self.devModeMultiplier
        #Clock.schedule_once(self.breakOver, time) # time reduced to seconds for testing
        #self.root.BreakWindow.startCountdown(time)
        h = 0 #time // 60
        m = time // 60
        s = time % 60
        #print(h)
        #print(m)
        #print(s)
        self.delta = datetime.now() + timedelta(hours=h, minutes=m, seconds = s)
        self.function_interval = Clock.schedule_interval(self.updateCount, 1)

    def updateCount(self, *args):
        global timeLeftLabel
        timeLeft = str(self.delta - datetime.now())
        print(timeLeft[0:7])
        timeLeftLabel.text = "Break Time Remaining:\n" + timeLeft[0:7]
        if timeLeft[0:7] == "0:00:00":
            self.stopCount()
            self.breakOver()
        elif timeLeft[0:7] == "-1 day,":
            self.stopCount()
            self.breakOver()

    def stopCount(self, *args):
        self.function_interval.cancel()

    def dismissForBreak(self):
        App.get_running_app().root_window.minimize()

    def changeBackgroundColor(self, instance):
        if Window.clearcolor == (255 / 255, 255 / 255, 255 / 255, 1):
            Window.clearcolor = (255 / 255, 0 / 255, 0 / 255, 1)
        if Window.clearcolor == (255 / 255, 0 / 255, 0 / 255, 1):
            Window.clearcolor = (255 / 255, 255 / 255, 255 / 255, 1)

    # restoring app on break finish
    def breakOver(self):
        self.playSound_quack()
        self.playSound_alarm()
        App.get_running_app().root_window.restore()
        self.root.current = "startup"

    # ending break from 'end break now' button
    def forceBreakOver(self):
        self.stopCount()
        self.root.current = "startup"

    # 'dismiss' handling
    def checkBackLater(self):
        Clock.schedule_once(self.checkIn, self.checkBackTime * self.devModeMultiplier) # time set to 5 seconds for testing and demoing
        App.get_running_app().root_window.minimize()

    # 'check in' handling
    def checkIn(self, instance):
        self.playSound_quack()
        App.get_running_app().root_window.restore()

if __name__ == "__main__":
    MyApp().run()
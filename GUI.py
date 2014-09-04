#!/usr/bin/python

# slider.py
'''taken from http://wiki.wxpython.org/AnotherTutorial#wx.Slider
 and slightly modified
'''
import wx
from Dynamixel import dynamixel

ID = 1
SPEED_REG = 32
POS_REG = 30

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (300, 150))
        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.sld = wx.Slider(panel, -1, 512, 24, 1000, wx.DefaultPosition, (250, -1),
                              wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        btn1 = wx.Button(panel, 8, 'Move')
        btn2 = wx.Button(panel, 9, 'Close')

        wx.EVT_BUTTON(self, 8, self.OnAdjust)
        wx.EVT_BUTTON(self, 9, self.OnClose)
        vbox.Add(self.sld, 1, wx.ALIGN_CENTRE)
        hbox.Add(btn1, 1, wx.RIGHT, 10)
        hbox.Add(btn2, 1)
        vbox.Add(hbox, 0, wx.ALIGN_CENTRE | wx.ALL, 20)
        panel.SetSizer(vbox)

        #initialize dynamixels
        speed = 75
        self.ax12 = dynamixel()
        self.ax12.set_ax_reg(ID, SPEED_REG, ([(speed%256),(speed>>8)]))
        
        
    def OnAdjust(self, event):
        print "Moving"
        val = self.sld.GetValue()
        self.ax12.set_ax_reg(ID, POS_REG, ([(val%256),(val>>8)]))
        
    def OnClose(self, event):
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'slider.py')
        frame.Show(True)
        frame.Centre()
        return True

app = MyApp(0)
app.MainLoop()

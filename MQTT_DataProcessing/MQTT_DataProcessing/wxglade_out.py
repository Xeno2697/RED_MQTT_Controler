#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0pre on Sat Jul  9 06:45:18 2022
#
import time
from matplotlib.pyplot import show
import wx
import paho.mqtt.client as mqtt
from MQTTClient import MQTTClientClass
import json
# begin wxGlade: dependencies
import gettext

from DeviceInformation import DeviceInformation
# end wxGlade
# begin wxGlade: extracode
# end wxGlade

class RobotGraph(wx.Frame):
    def __init__(self, mqttc : MQTTClientClass,*args, **kwds):
        # begin wxGlade: RobotGraph.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((430, 732))
        self.SetTitle(_("frame"))

        self.panel_1 = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_1.SetBackgroundColour(wx.Colour(228, 255, 232))
        self.panel_1.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Robot Graph"))
        label_1.SetForegroundColour(wx.Colour(255, 0, 0))
        label_1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Select Robot ID : "))
        sizer_2.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.spin_ctrl_double_1 = wx.SpinCtrlDouble(self.panel_1, wx.ID_ANY, initial=0.0, min=0.0, max=1000000000.0)
        self.spin_ctrl_double_1.SetDigits(0)
        sizer_2.Add(self.spin_ctrl_double_1, 0, 0, 0)

        sizer_1.Add((400, 200), 1, wx.ALL | wx.EXPAND, 5)

        sizer_1.Add((400, 200), 1, wx.ALL | wx.EXPAND, 5)

        sizer_1.Add((400, 200), 1, wx.ALL | wx.EXPAND, 5)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

# end of class RobotGraph

class DeviceDataList(wx.Frame):
    def __init__(self,mqttc:MQTTClientClass,*args, **kwds):
        # begin wxGlade: DeviceDataList.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.MDIChildFrame.__init__(self, *args, **kwds)
        self.SetSize((495, 655))
        self.SetTitle(_("Device_List"))

        self.panel_1 = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_1.SetBackgroundColour(wx.Colour(255, 217, 251))
        self.panel_1.SetScrollRate(10, 10)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Device List"))
        label_1.SetForegroundColour(wx.Colour(255, 0, 0))
        label_1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        grid_sizer_1 = wx.GridSizer(2, 3, 0, 0)
        sizer_1.Add(grid_sizer_1, 0, 0, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Entire num : "))
        grid_sizer_1.Add(label_2, 0, 0, 0)

        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Connected num : "))
        grid_sizer_1.Add(label_3, 0, 0, 0)

        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Disconnected num : "))
        grid_sizer_1.Add(label_4, 0, 0, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, _("0"), style=wx.TE_READONLY)
        grid_sizer_1.Add(self.text_ctrl_1, 1, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_2 = wx.TextCtrl(self.panel_1, wx.ID_ANY, _("0"), style=wx.TE_READONLY)
        grid_sizer_1.Add(self.text_ctrl_2, 1, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_3 = wx.TextCtrl(self.panel_1, wx.ID_ANY, _("0"), style=wx.TE_READONLY)
        grid_sizer_1.Add(self.text_ctrl_3, 1, wx.EXPAND | wx.RIGHT, 5)

        self.list_ctrl_1 = wx.ListCtrl(self.panel_1, wx.ID_ANY, style=wx.BORDER_DEFAULT | wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.list_ctrl_1.AppendColumn(_("ID"), format=wx.LIST_FORMAT_LEFT, width=110)
        self.list_ctrl_1.AppendColumn(_("Connect"), format=wx.LIST_FORMAT_LEFT, width=61)
        self.list_ctrl_1.AppendColumn(_("Distance"), format=wx.LIST_FORMAT_LEFT, width=63)
        self.list_ctrl_1.AppendColumn(_("Azimuth"), format=wx.LIST_FORMAT_LEFT, width=72)
        sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        label_22 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Left"))
        sizer_2.Add(label_22, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.spin_ctrl_1 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        sizer_2.Add(self.spin_ctrl_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        label_23 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Right"))
        sizer_2.Add(label_23, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.spin_ctrl_2 = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "0", min=0, max=100)
        sizer_2.Add(self.spin_ctrl_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, _("Zero reset"))
        sizer_2.Add(self.button_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, _("Deselect"))
        sizer_2.Add(self.button_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.button_3 = wx.Button(self.panel_1, wx.ID_ANY, _("Send"))
        sizer_2.Add(self.button_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        grid_sizer_4 = wx.GridSizer(2, 4, 0, 0)
        sizer_1.Add(grid_sizer_4, 0, 0, 0)

        label_13 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Inner Rth : "))
        grid_sizer_4.Add(label_13, 0, 0, 0)

        label_14 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Mu : "))
        grid_sizer_4.Add(label_14, 0, 0, 0)

        label_15 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Sigma : "))
        grid_sizer_4.Add(label_15, 0, 0, 0)

        label_16 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Outer Rth : "))
        grid_sizer_4.Add(label_16, 0, 0, 0)

        self.text_ctrl_12 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_4.Add(self.text_ctrl_12, 1, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_13 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_4.Add(self.text_ctrl_13, 1, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_14 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_4.Add(self.text_ctrl_14, 1, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_15 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_4.Add(self.text_ctrl_15, 1, wx.EXPAND | wx.RIGHT, 5)

        grid_sizer_2 = wx.GridSizer(2, 2, 0, 0)
        sizer_1.Add(grid_sizer_2, 0, 0, 0)

        label_17 = wx.StaticText(self.panel_1, wx.ID_ANY, _("CeilingImage num : "))
        grid_sizer_2.Add(label_17, 0, 0, 0)

        label_18 = wx.StaticText(self.panel_1, wx.ID_ANY, _("FlootingImage num : "))
        grid_sizer_2.Add(label_18, 0, 0, 0)

        self.text_ctrl_16 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_16, 0, wx.RIGHT, 5)

        self.text_ctrl_17 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_2.Add(self.text_ctrl_17, 0, wx.RIGHT, 5)

        grid_sizer_3 = wx.GridSizer(2, 3, 0, 0)
        sizer_1.Add(grid_sizer_3, 0, 0, 0)

        label_19 = wx.StaticText(self.panel_1, wx.ID_ANY, _("FindCenter Rate : "))
        grid_sizer_3.Add(label_19, 0, 0, 0)

        label_20 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Accept Rate : "))
        grid_sizer_3.Add(label_20, 0, 0, 0)

        label_21 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Reject Rate : "))
        grid_sizer_3.Add(label_21, 0, 0, 0)

        self.text_ctrl_18 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_3.Add(self.text_ctrl_18, 0, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_19 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_3.Add(self.text_ctrl_19, 0, wx.EXPAND | wx.RIGHT, 5)

        self.text_ctrl_20 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        grid_sizer_3.Add(self.text_ctrl_20, 0, wx.EXPAND | wx.RIGHT, 5)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.button_1.Bind(wx.EVT_BUTTON, self.ZeroReset)
        self.button_2.Bind(wx.EVT_BUTTON, self.Deselect)
        self.button_3.Bind(wx.EVT_BUTTON, self.Send)
        # end wxGlade

    def ZeroReset(self, event):  # wxGlade: DeviceDataList.<event_handler>
        print("Event handler 'ZeroReset' not implemented!")
        event.Skip()

    def Deselect(self, event):  # wxGlade: DeviceDataList.<event_handler>
        print("Event handler 'Deselect' not implemented!")
        event.Skip()

    def Send(self, event):  # wxGlade: DeviceDataList.<event_handler>
        print("Event handler 'Send' not implemented!")
        event.Skip()

# end of class DeviceDataList

class RED_Algolism_Controler(wx.Frame):
    def __init__(self,parentApp, mqttc : MQTTClientClass,*args, **kwds): 
        
        # begin wxGlade: RED_Algolism_Controler.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle(_("RED_Algolism_Controler"))
        self.SetBackgroundColour(wx.Colour(255, 244, 244))
        
        self.mqttc = mqttc
        self.parentApp = parentApp
        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("RED_MQTT_Controler"))
        label_1.SetBackgroundColour(wx.Colour(255, 255, 255))
        label_1.SetForegroundColour(wx.Colour(255, 0, 0))
        label_1.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        label_1.SetFocus()
        sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1.SetMinSize((612, 561))
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)

        self.panel_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_2.SetBackgroundColour(wx.Colour(255, 244, 244))
        self.notebook_1.AddPage(self.panel_2, _("Title"))

        #??????????????????(ms)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh)
        self.timer.Start(100)

        sizer_19 = wx.BoxSizer(wx.VERTICAL)

        label_25 = wx.StaticText(self.panel_2, wx.ID_ANY, _("RED"), style=wx.ALIGN_CENTER_HORIZONTAL)
        label_25.SetForegroundColour(wx.Colour(255, 0, 0))
        label_25.SetFont(wx.Font(64, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_19.Add(label_25, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 90)

        self.Algorithm_Mode = wx.ScrolledWindow(self.notebook_1, wx.ID_ANY, style=wx.BORDER_THEME)
        self.Algorithm_Mode.SetScrollRate(10, 10)
        self.notebook_1.AddPage(self.Algorithm_Mode, _("Algorithm Mode"))

        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)

        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_21, 0, wx.ALL | wx.EXPAND, 1)

        label_26 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Server's IP adress : "))
        sizer_21.Add(label_26, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.Algorithm_Mode, wx.ID_ANY, _(self.mqttc.connectingIP), style=wx.TE_READONLY)
        sizer_21.Add(self.text_ctrl_1, 1, 0, 0)

        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_22, 0, wx.ALL | wx.EXPAND, 1)

        label_27 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Algolism Operate Robot : "))
        sizer_22.Add(label_27, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.combo_box_1 = wx.ComboBox(self.Algorithm_Mode, wx.ID_ANY, choices=[_("ALL")], style=wx.CB_DROPDOWN | wx.CB_SORT)
        self.combo_box_1.SetMinSize((70, 23))
        self.combo_box_1.SetSelection(0)
        sizer_22.Add(self.combo_box_1, 1, 0, 0)

        sizer_23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_23, 0, wx.ALL | wx.EXPAND, 1)

        label_28 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Algorithm : "))
        sizer_23.Add(label_28, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.AlgorithmBool = wx.ToggleButton(self.Algorithm_Mode, wx.ID_ANY, _("ON/OFF"))
        sizer_23.Add(self.AlgorithmBool, 0, 0, 0)

        sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_24, 0, wx.ALL | wx.EXPAND, 1)

        label_29 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Transit Time : "))
        sizer_24.Add(label_29, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.transittime = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=2.0, min=0.0, max=100.0)
        self.transittime.SetDigits(3)
        sizer_24.Add(self.transittime, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_30 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_24.Add(label_30, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_25, 0, wx.ALL | wx.EXPAND, 1)

        label_31 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Inner Rth : "))
        sizer_25.Add(label_31, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.innerrth = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=0.0, min=0.0, max=100.0)
        self.innerrth.SetDigits(3)
        sizer_25.Add(self.innerrth, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_32 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_25.Add(label_32, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_26 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_26, 0, wx.ALL | wx.EXPAND, 1)

        label_33 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Mu : "))
        sizer_26.Add(label_33, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.mu = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=1.0, min=0.0, max=100.0)
        self.mu.SetDigits(3)
        sizer_26.Add(self.mu, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

        label_34 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_26.Add(label_34, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_27 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_27, 0, wx.ALL | wx.EXPAND, 1)

        label_35 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Sigma : "))
        sizer_27.Add(label_35, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.sigma = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=1.0, min=0.0, max=100.0)
        self.sigma.SetDigits(3)
        sizer_27.Add(self.sigma, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_36 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_27.Add(label_36, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_28 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_28, 0, wx.ALL | wx.EXPAND, 1)

        label_37 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Outer Rth : "))
        sizer_28.Add(label_37, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.outerrth = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=3.0, min=0.0, max=100.0)
        self.outerrth.SetDigits(3)
        sizer_28.Add(self.outerrth, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_38 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_28.Add(label_38, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_29 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_29, 0, wx.ALL | wx.EXPAND, 1)

        label_39 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Height : "))
        sizer_29.Add(label_39, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.height = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=2.2, min=0.0, max=100.0)
        self.height.SetDigits(3)
        sizer_29.Add(self.height, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_40 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[m]"))
        sizer_29.Add(label_40, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_30 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_30, 0, wx.ALL | wx.EXPAND, 1)

        label_41 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Reject Mode : "))
        sizer_30.Add(label_41, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.reject = wx.Choice(self.Algorithm_Mode, wx.ID_ANY, choices=[_("A"), _("B"), _("C"), _("D")])
        self.reject.SetSelection(0)
        sizer_30.Add(self.reject, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_31 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_31, 0, wx.ALL | wx.EXPAND, 1)

        label_42 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Marker : "))
        sizer_31.Add(label_42, 2, wx.ALIGN_CENTER_VERTICAL, 0)

        label_43 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[A] : "))
        sizer_31.Add(label_43, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.markerhzA = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=5.0, min=0.0, max=100.0, style=wx.ALIGN_LEFT | wx.SP_ARROW_KEYS)
        self.markerhzA.SetDigits(1)
        sizer_31.Add(self.markerhzA, 1, wx.EXPAND, 0)

        label_281 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[Hz]"))
        sizer_31.Add(label_281, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_44 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[B] : "))
        sizer_31.Add(label_44, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)

        self.markerhzB = wx.SpinCtrlDouble(self.Algorithm_Mode, wx.ID_ANY, initial=0.0, min=0.0, max=100.0, style=wx.ALIGN_LEFT | wx.SP_ARROW_KEYS)
        self.markerhzB.SetDigits(1)
        sizer_31.Add(self.markerhzB, 1, wx.EXPAND, 0)

        label_280 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("[Hz]"))
        sizer_31.Add(label_280, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_32 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_32, 0, wx.ALL | wx.EXPAND, 1)

        label_283 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Height Collection : "))
        sizer_32.Add(label_283, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.heightcolectbool = wx.ToggleButton(self.Algorithm_Mode, wx.ID_ANY, _("ON/OFF"))
        sizer_32.Add(self.heightcolectbool, 0, 0, 0)

        sizer_33 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(sizer_33, 0, wx.ALL | wx.EXPAND, 1)

        label_284 = wx.StaticText(self.Algorithm_Mode, wx.ID_ANY, _("Shutter Speed : "))
        sizer_33.Add(label_284, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.shutterspeed = wx.Choice(self.Algorithm_Mode, wx.ID_ANY, choices=[_("100 (for Outdoor)"), _("1000"), _("10000 (for Indoor)")])
        self.shutterspeed.SetSelection(0)
        sizer_33.Add(self.shutterspeed, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.button_3 = wx.Button(self.Algorithm_Mode, wx.ID_ANY, _("\n Send parameters\n "))
        self.button_3.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_2.Add(self.button_3, 0, wx.ALL | wx.EXPAND, 5)

        self.panel_3 = wx.ScrolledWindow(self.notebook_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_3.SetScrollRate(10, 10)
        self.notebook_1.AddPage(self.panel_3, _("Radio Control Mode"))

        sizer_20 = wx.BoxSizer(wx.VERTICAL)

        sizer_34 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20.Add(sizer_34, 0, wx.ALL | wx.EXPAND, 1)

        label_45 = wx.StaticText(self.panel_3, wx.ID_ANY, _("Server's IP adress : "))
        sizer_34.Add(label_45, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.text_ctrl_2 = wx.TextCtrl(self.panel_3, wx.ID_ANY, _(self.mqttc.connectingIP), style=wx.TE_READONLY)
        self.text_ctrl_2.Enable(True)
        sizer_34.Add(self.text_ctrl_2, 1, 0, 0)

        sizer_35 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20.Add(sizer_35, 0, wx.ALL | wx.EXPAND, 1)

        label_46 = wx.StaticText(self.panel_3, wx.ID_ANY, _("Algolism Operate Robot : "))
        sizer_35.Add(label_46, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.combo_box_7 = wx.ComboBox(self.panel_3, wx.ID_ANY, choices=[_("ALL"), "", "", "", ""], style=wx.CB_DROPDOWN)
        self.combo_box_7.SetSelection(0)
        sizer_35.Add(self.combo_box_7, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        grid_sizer_1 = wx.GridSizer(3, 3, 0, 0)
        sizer_20.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 5)

        self.button_4 = wx.Button(self.panel_3, wx.ID_ANY, _(u"?????????"))
        grid_sizer_1.Add(self.button_4, 0, wx.EXPAND, 0)

        self.button_5 = wx.Button(self.panel_3, wx.ID_ANY, _(u"???\n??????"))
        self.button_5.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_5, 0, wx.EXPAND, 0)

        self.button_6 = wx.Button(self.panel_3, wx.ID_ANY, _(u"?????????"))
        grid_sizer_1.Add(self.button_6, 0, wx.EXPAND, 0)

        self.button_7 = wx.Button(self.panel_3, wx.ID_ANY, _(u"???\n?????????"))
        self.button_7.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_7, 0, wx.EXPAND, 0)

        self.button_8 = wx.Button(self.panel_3, wx.ID_ANY, _("STOP"))
        self.button_8.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_8, 0, wx.EXPAND, 0)

        self.button_9 = wx.Button(self.panel_3, wx.ID_ANY, _(u"???\n?????????"))
        self.button_9.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_9, 0, wx.EXPAND, 0)

        self.button_10 = wx.Button(self.panel_3, wx.ID_ANY, _(u"Shoot Floor\n???????\n?????????????????????"))
        self.button_10.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_10, 0, wx.EXPAND, 0)

        self.button_11 = wx.Button(self.panel_3, wx.ID_ANY, _(u"???\n??????"))
        self.button_11.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_11, 0, wx.EXPAND, 0)

        self.button_12 = wx.Button(self.panel_3, wx.ID_ANY, _(u"Shoot Ceiling\n???????\n?????????????????????"))
        self.button_12.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        grid_sizer_1.Add(self.button_12, 0, wx.EXPAND, 0)

        self.panel_1 = wx.ScrolledWindow(self.notebook_1, wx.ID_ANY, style=wx.BORDER_SIMPLE)
        self.panel_1.SetForegroundColour(wx.Colour(165, 42, 42))
        self.panel_1.SetScrollRate(10, 10)
        self.notebook_1.AddPage(self.panel_1, _("Manegement"))

        sizer_4 = wx.BoxSizer(wx.VERTICAL)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_6, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Swarm System Operation and Manegement"))
        label_2.SetForegroundColour(wx.Colour(255, 0, 0))
        label_2.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_6.Add(label_2, 0, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_5, 0, 0, 0)

        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Server's IP : "), style=wx.ALIGN_CENTER_HORIZONTAL)
        label_3.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_5.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_ctrl_3 = wx.TextCtrl(self.panel_1, wx.ID_ANY, _("192.168.2.123"), style=wx.TE_READONLY)
        self.text_ctrl_3.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_5.Add(self.text_ctrl_3, 1, wx.ALL | wx.EXPAND, 0)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, _("Send BlokerIP"))
        self.button_1.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_5.Add(self.button_1, 1, wx.ALL | wx.EXPAND, 0)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Camera View"))
        label_6.SetForegroundColour(wx.Colour(143, 0, 0))
        label_6.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_4.Add(label_6, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        bitmap_1 = wx.StaticBitmap(self.panel_1, wx.ID_ANY, wx.Bitmap("C:\\Users\\kaede\\Downloads\\noimage.png", wx.BITMAP_TYPE_ANY), style=wx.BORDER_SIMPLE | wx.FULL_REPAINT_ON_RESIZE)
        bitmap_1.SetMaxSize((1080, 720))
        sizer_4.Add(bitmap_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_7, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Robot ID : "))
        sizer_7.Add(label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.combo_box_2 = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_7.Add(self.combo_box_2, 0, 0, 0)

        sizer_7.Add((80, 2), 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, _("Camera : "))
        sizer_7.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.choice_1 = wx.Choice(self.panel_1, wx.ID_ANY, choices=[_("Flooting"), _("Ceiling")])
        self.choice_1.SetSelection(0)
        sizer_7.Add(self.choice_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_8, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_13 = wx.Button(self.panel_1, wx.ID_ANY, _("show device graph"))
        sizer_8.Add(self.button_13, 1, wx.EXPAND, 0)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, _("show device list"))
        sizer_8.Add(self.button_2, 1, wx.EXPAND, 0)

        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.button_14 = wx.Button(self.panel_1, wx.ID_ANY, _("Show local storage path"))
        self.button_14.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_9.Add(self.button_14, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.button_15 = wx.Button(self.panel_1, wx.ID_ANY, _("Save devicedata record"))
        self.button_15.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_9.Add(self.button_15, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(sizer_10, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.button_16 = wx.Button(self.panel_1, wx.ID_ANY, _("All Stop"))
        self.button_16.SetBackgroundColour(wx.Colour(255, 251, 164))
        sizer_10.Add(self.button_16, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.button_17 = wx.Button(self.panel_1, wx.ID_ANY, _("Start"))
        self.button_17.SetBackgroundColour(wx.Colour(137, 219, 219))
        sizer_10.Add(self.button_17, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.button_18 = wx.Button(self.panel_1, wx.ID_ANY, _("Restart"))
        self.button_18.SetBackgroundColour(wx.Colour(198, 242, 190))
        sizer_10.Add(self.button_18, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.button_19 = wx.Button(self.panel_1, wx.ID_ANY, _("Shutdown"))
        self.button_19.SetBackgroundColour(wx.Colour(246, 107, 107))
        sizer_10.Add(self.button_19, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.panel_1.SetSizer(sizer_4)

        self.panel_3.SetSizer(sizer_20)

        self.Algorithm_Mode.SetSizer(sizer_2)

        self.panel_2.SetSizer(sizer_19)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()

        self.button_3.Bind(wx.EVT_BUTTON, self.SendParameters)
        self.button_5.Bind(wx.EVT_BUTTON, self.RadiconForward)
        self.button_7.Bind(wx.EVT_BUTTON, self.RadiconLeft)
        self.button_8.Bind(wx.EVT_BUTTON, self.RadiconStop)
        self.button_9.Bind(wx.EVT_BUTTON, self.RadiconRight)
        self.button_10.Bind(wx.EVT_BUTTON, self.RadiconShootFlooting)
        self.button_11.Bind(wx.EVT_BUTTON, self.RadiconBack)
        self.button_12.Bind(wx.EVT_BUTTON, self.RadiconShootCeiling)
        self.button_1.Bind(wx.EVT_BUTTON, self.SendBlockerIP)
        self.button_13.Bind(wx.EVT_BUTTON, self.ShowDeviceGraph)
        self.button_2.Bind(wx.EVT_BUTTON, self.ShowDeviceList)
        self.button_14.Bind(wx.EVT_BUTTON, self.ShowLocalPath)
        self.button_15.Bind(wx.EVT_BUTTON, self.SaveDataRecord)
        self.button_16.Bind(wx.EVT_BUTTON, self.Navi_AllStop)
        self.button_17.Bind(wx.EVT_BUTTON, self.Navi_Start)
        self.button_18.Bind(wx.EVT_BUTTON, self.Navi_Restart)
        self.button_19.Bind(wx.EVT_BUTTON, self.Navi_Shutdown)

    def SendParameters(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        #data={'IsExploring':True, 'TransitTime':2.0, 'Mu':1.0, 'Sigma':1.0, 'Outer_Rth':3.0, 'Inner_Rth':0.0, 'Height':2.0, 'Height_Correction':True, 'Reject':'A', 'MarkerColor':'Green' #??????????, 'ShutterSpeed':100, 'LeftPWM':0.0,'RightPWM':0.0}
        id = self.combo_box_1.Value
        topic :str
        if id == "ALL":
            topic = "RED/Status"
        else:
            topic = "RED/"+str(id)+"/Param"
        data : dict = {}
        data["IsExploring"] = self.AlgorithmBool.Value
        data["TransitTime"] = self.transittime.Value
        data["Mu"] = self.mu.Value
        data["Sigma"] = self.sigma.Value
        data["Outer_Rth"] = self.outerrth.Value
        data["Inner_Rth"] = self.innerrth.Value
        data["Height"] = self.height.Value
        data["Height_Correction"] = self.heightcolectbool.Value
        data["Reject"] = self.reject.GetStringSelection()
        if not data["Reject"] in ("A","B","C","D"):
            print("Reject Value is ERROR!!")
            return
        data["ShutterSpeed"] = self.shutterspeed.GetSelection()
        if data["ShutterSpeed"] == 0:
            data["ShutterSpeed"] = 100
        elif data["ShutterSpeed"] == 1:
            data["ShutterSpeed"] = 1000
        elif data["ShutterSpeed"] == 2:
            data["ShutterSpeed"] = 10000
        else:
            print("Error! ShutterSpeed is wrong.")
        data["LeftPWM"] = 0.0
        data["RightPWM"] = 0.0
        if self.markerhzB.Value>0:
            if self.markerhzA.Value>0:
                data["MarkerColor"] = str(self.markerhzA.Value)+"_"+str(self.markerhzB.Value)
            else:
                data["MarkerColor"] = str(self.markerhzB.Value)
        else:
            data["MarkerColor"] = str(self.markerhzA.Value)
        
        massage = json.dumps(data)
        try:
            self.mqttc.publish(topic,massage)
            self.window = MyDialog("Sent parameters to RED.",None,  wx.ID_ANY, "")
        except:
            self.window = MyDialog("Error! Couldn't send...",None,  wx.ID_ANY, "")
        self.window.ShowModal()
        
        event.Skip()
    def refresh(self, event): # ???????????????????????????????????????????????????????????????????????????????????????
        showlist : list = self.combo_box_1.GetItems()
        showlist.remove("ALL")
        needrefresh = False
        i = DeviceInformation
        Dlist =self.mqttc._MQTTClientClass__DeviceInformationList
        for i in Dlist:
            id = i.ID
            if not id in showlist:
                self.combo_box_1.Append(id)
                showlist.remove(id)
        if needrefresh:
            self.combo_box_7.SetItems(self.combo_box_1.GetItems())
            self.Refresh()
            print("Device list refresh.")
    
    def RadiconForward(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconForward' not implemented!")
        event.Skip()
    def RadiconLeft(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconLeft' not implemented!")
        event.Skip()
    def RadiconStop(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconStop' not implemented!")
        event.Skip()
    def RadiconRight(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconRight' not implemented!")
        event.Skip()
    def RadiconShootFlooting(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconShootFlooting' not implemented!")
        event.Skip()
    def RadiconBack(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconBack' not implemented!")
        event.Skip()
    def RadiconShootCeiling(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'RadiconShootCeiling' not implemented!")
        event.Skip()
    
    def SendBlockerIP(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'SendBlockerIP' not implemented!")
        event.Skip()

    def ShowDeviceGraph(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        self.parentApp.Showdevicegraph()

    def ShowDeviceList(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        self.parentApp.Showdevicelist()

    def ShowLocalPath(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'ShowLocalPath' not implemented!")
        event.Skip()

    def SaveDataRecord(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'SaveDataRecord' not implemented!")
        event.Skip()

    def Navi_AllStop(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'Navi_AllStop' not implemented!")
        event.Skip()

    def Navi_Start(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'Navi_Start' not implemented!")
        event.Skip()

    def Navi_Restart(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'Navi_Restart' not implemented!")
        event.Skip()

    def Navi_Shutdown(self, event):  # wxGlade: RED_Algolism_Controler.<event_handler>
        print("Event handler 'Navi_Shutdown' not implemented!")
        event.Skip()

# end of class RED_Algolism_Controler

class MyDialog(wx.Dialog):
    def __init__(self, text :str , *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((165, 106))
        self.SetTitle(_("dialog"))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, text)
        sizer_1.Add(label_1, 0, wx.ALL, 10)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()

        self.button_OK.Bind(wx.EVT_BUTTON, self.CloseThis)
        # end wxGlade

    def CloseThis(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Destroy()
        event.Skip()

# end of class MyDialog

class MyDialog1(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog1.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(_("Shutdown"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("C:\\Windows\\System32\\SecurityAndMaintenance.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Are you sure you want to shut it down?"))
        sizer_1.Add(label_1, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 15)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self.button_CANCEL)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetAffirmativeId(self.button_OK.GetId())
        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()
 

class MyApp(wx.App):
    def __init__(self, redirect=False, mqttc = MQTTClientClass, filename=None, useBestVisual=False, clearSigInt=True):
        self.mqttc = mqttc
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
    
    def OnInit(self):
        self.RED_Algolism_Controler = RED_Algolism_Controler(self,self.mqttc, None, wx.ID_ANY, "")
        self.SetTopWindow(self.RED_Algolism_Controler)
        self.RED_Algolism_Controler.Show()
        return True
    
    def Showdevicelist(self):
        try:
            self.Devicelist.Close()
            self.Devicelist = DeviceDataList(self.mqttc, None, wx.ID_ANY, "")
        except:
            self.Devicelist = DeviceDataList(self.mqttc, None, wx.ID_ANY, "")
        self.Devicelist.Show()
    
    def Showdevicegraph(self):
        try:
            self.Devicegraph.Close()
            self.Devicegraph = RobotGraph(self.mqttc, None, wx.ID_ANY, "")
        except:
            self.Devicegraph = RobotGraph(self.mqttc, None, wx.ID_ANY, "")
        self.Devicegraph.Show()
    
    def MainLoop(self):
        time.sleep(0.03)
        return super().MainLoop()
    
# end of class MyApp

if __name__ == "__main__":
    gettext.install("RED_MQTT") # replace with the appropriate catalog name

    RED_MQTT = MyApp(0)
    RED_MQTT.MainLoop()

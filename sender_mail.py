#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# GUI generated by wxGlade 0.9.1
# Created By LuizFNunes

import wx
import configparser as cfp
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class mainFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_SIMPLE | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((350, 420))
		
		# Menu Bar
		self.frame_menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Settings\tCtrl+c", "")
		self.Bind(wx.EVT_MENU, self.openSettings, id=item.GetId())
		self.frame_menubar.Append(wxglade_tmp_menu, "&File")
		wxglade_tmp_menu = wx.Menu()
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "&About\tCtrl+a", "")
		self.Bind(wx.EVT_MENU, self.openAbout, id=item.GetId())
		item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Quit\tCtrl+q", "")
		self.Bind(wx.EVT_MENU, self.closeApp, id=item.GetId())
		self.frame_menubar.Append(wxglade_tmp_menu, "&Options")
		self.SetMenuBar(self.frame_menubar)
		# Menu Bar end
		self.mainPanel = wx.Panel(self, wx.ID_ANY)
		self.textFrom = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
		self.textTo = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
		self.textSubject = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "")
		self.textMessage = wx.TextCtrl(self.mainPanel, wx.ID_ANY, "", style=wx.TE_MULTILINE)
		self.buttonSendMail = wx.Button(self.mainPanel, wx.ID_ANY, "Send Email")
		self.buttonClear = wx.Button(self.mainPanel, wx.ID_ANY, "Clear All")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.sendMail, self.buttonSendMail)
		self.Bind(wx.EVT_BUTTON, self.clearAll, self.buttonClear)

		# Load Configuration
		self.__load_config()

	def __set_properties(self):
		self.SetTitle("Email App")
		self.SetBackgroundColour(wx.NullColour)
		self.textMessage.SetMinSize((324, 150))
		self.buttonSendMail.SetMinSize((96, 32))
		self.buttonClear.SetMinSize((96, 32))

	def __do_layout(self):
		contentSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
		subjectSizer = wx.BoxSizer(wx.HORIZONTAL)
		toSizer = wx.BoxSizer(wx.HORIZONTAL)
		fromSizer = wx.BoxSizer(wx.HORIZONTAL)
		labelFrom = wx.StaticText(self.mainPanel, wx.ID_ANY, "From ")
		labelFrom.SetMinSize((50, 16))
		fromSizer.Add(labelFrom, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		fromSizer.Add(self.textFrom, 1, wx.ALL, 4)
		mainSizer.Add(fromSizer, 0, wx.EXPAND, 0)
		labelTo = wx.StaticText(self.mainPanel, wx.ID_ANY, "To      ")
		labelTo.SetMinSize((50, 16))
		toSizer.Add(labelTo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		toSizer.Add(self.textTo, 1, wx.ALL, 4)
		mainSizer.Add(toSizer, 0, wx.EXPAND, 0)
		labelSubject = wx.StaticText(self.mainPanel, wx.ID_ANY, "Subject")
		labelSubject.SetMinSize((50, 16))
		subjectSizer.Add(labelSubject, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		subjectSizer.Add(self.textSubject, 1, wx.ALL, 4)
		mainSizer.Add(subjectSizer, 0, wx.EXPAND, 0)
		labelMessage = wx.StaticText(self.mainPanel, wx.ID_ANY, "Message")
		mainSizer.Add(labelMessage, 0, wx.ALL, 8)
		mainSizer.Add(self.textMessage, 0, wx.ALL | wx.EXPAND, 8)
		sizer_2.Add(self.buttonSendMail, 0, wx.ALL, 4)
		sizer_2.Add(self.buttonClear, 0, wx.ALL, 4)
		mainSizer.Add(sizer_2, 1, wx.EXPAND, 0)
		self.mainPanel.SetSizer(mainSizer)
		contentSizer.Add(self.mainPanel, 1, wx.ALL | wx.EXPAND, 4)
		self.SetSizer(contentSizer)
		self.Layout()
		self.Centre()
	
	def __load_config(self):
		self.config = configLoad()

	def openSettings(self, event): 
		settings = settingsDialog(None, wx.ID_ANY, "")
		settings.ShowModal()
		settings.Destroy()
		self.__load_config()

	def openAbout(self, event):
		about = aboutDialog(None, wx.ID_ANY, "")
		about.ShowModal()
		about.Destroy()

	def closeApp(self, event):
		self.Destroy()

	def sendMail(self, event): 
		fromVal = self.textFrom.GetValue()
		toVal = self.textTo.GetValue()
		subjectVal = self.textSubject.GetValue()
		messageVal = self.textMessage.GetValue()
		email = "Subject:{}\n\n{}".format(subjectVal,messageVal)
		host = self.config.getHost()
		port = self.config.getPort()
		user = self.config.getUser()
		password = self.config.getPassword()
		msg = MIMEMultipart()
		msg["From"] = fromVal
		msg["To"] = toVal
		msg.attach(MIMEText(email,'plain'))
		server = smtplib.SMTP(host=host,port=port)
		server.starttls()
		error = False
		try:
			server.login(user,password)
		except:
			error = True
			messageError = "Login Error!\nWrong username or password!"
			alert = messageDialog(messageError,None,wx.ID_ANY, "")
			alert.ShowModal()
			alert.Destroy()
		if not error:
			try:
				print("server.sendmail({},{},{})".format(fromVal,toVal,msg.as_string()))
				server.sendmail(fromVal,toVal,email)
				messageSuccess = "Email successfully sent!"
				alert = messageDialog(messageSuccess,None,wx.ID_ANY, "")
				alert.ShowModal()
				alert.Destroy()
			except:
				messageError = "Error!\nThe email can not be sent. Check your internet connection!"
				alert = messageDialog(messageError,None,wx.ID_ANY, "")
				alert.ShowModal()
				alert.Destroy()
		server.quit()
		event.Skip()

	def clearAll(self, event):
		self.textFrom.Clear()
		self.textTo.Clear()
		self.textSubject.Clear()
		self.textMessage.Clear()


class aboutDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((400, 320))
		self.textAbout = wx.TextCtrl(self, wx.ID_ANY, "Created by Luiz F Nunes\n\nLibraries:\n    Python 3\n    WxPython\n    SmtpLib\n\nContact:\n    http://github.com/luizfnunes", style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.buttonCloseAbout = wx.Button(self, wx.ID_CLOSE, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.closeAbout, self.buttonCloseAbout)

	def __set_properties(self):
		self.SetTitle("About")
		self.SetSize((400, 330))
		self.textAbout.SetMinSize((324, 124))

	def __do_layout(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		labelTitleAbout = wx.StaticText(self, wx.ID_ANY, "Email App")
		labelTitleAbout.SetFont(wx.Font(26, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		mainSizer.Add(labelTitleAbout, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		mainSizer.Add(self.textAbout, 0, wx.ALIGN_CENTER | wx.ALL , 10)
		mainSizer.Add(self.buttonCloseAbout, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(mainSizer)
		self.Layout()
		self.Centre()

	def closeAbout(self, event):
		print("Event handler 'closeAbout' not implemented!")
		event.Skip()

class settingsDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetSize((400, 220))
		self.textHost = wx.TextCtrl(self, wx.ID_ANY, "")
		self.textPort = wx.TextCtrl(self, wx.ID_ANY, "")
		self.textUser = wx.TextCtrl(self, wx.ID_ANY, "")
		self.textPassword = wx.TextCtrl(self, wx.ID_ANY, "")
		self.buttonSave = wx.Button(self, wx.ID_ANY, "Save")
		self.buttonCancel = wx.Button(self, wx.ID_ANY, "Cancel")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.saveSettings, self.buttonSave)
		self.Bind(wx.EVT_BUTTON, self.cancelSettings, self.buttonCancel)

		self.__load_config()
	
	def __load_config(self):
		self.config = configLoad()
		self.textHost.SetLabelText(self.config.getHost())
		self.textPort.SetLabelText(self.config.getPort())
		self.textUser.SetLabelText(self.config.getUser())
		self.textPassword.SetLabelText(self.config.getPassword())

	def __set_properties(self):
		self.SetTitle("Settings")
		self.SetSize((400, 220))

	def __do_layout(self):
		containerSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		buttonsSizer = wx.GridSizer(1, 2, 0, 0)
		passwordSizer = wx.BoxSizer(wx.HORIZONTAL)
		userSizer = wx.BoxSizer(wx.HORIZONTAL)
		portSizer = wx.BoxSizer(wx.HORIZONTAL)
		hostSizer = wx.BoxSizer(wx.HORIZONTAL)
		labelHost = wx.StaticText(self, wx.ID_ANY, "Host        ")
		hostSizer.Add(labelHost, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		hostSizer.Add(self.textHost, 1, wx.ALL, 4)
		mainSizer.Add(hostSizer, 0, wx.EXPAND, 0)
		labelPort = wx.StaticText(self, wx.ID_ANY, "Port         ")
		portSizer.Add(labelPort, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		portSizer.Add(self.textPort, 1, wx.ALL, 4)
		mainSizer.Add(portSizer, 0, wx.EXPAND, 0)
		labelUser = wx.StaticText(self, wx.ID_ANY, "User         ")
		userSizer.Add(labelUser, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		userSizer.Add(self.textUser, 1, wx.ALL, 4)
		mainSizer.Add(userSizer, 0, wx.EXPAND, 0)
		labelPassword = wx.StaticText(self, wx.ID_ANY, "Password")
		passwordSizer.Add(labelPassword, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
		passwordSizer.Add(self.textPassword, 1, wx.ALL, 4)
		mainSizer.Add(passwordSizer, 0, wx.EXPAND, 0)
		buttonsSizer.Add(self.buttonSave, 1, wx.ALIGN_CENTER | wx.ALL, 0)
		buttonsSizer.Add(self.buttonCancel, 1, wx.ALIGN_CENTER | wx.ALL, 0)
		mainSizer.Add(buttonsSizer, 1, wx.ALL | wx.EXPAND, 0)
		containerSizer.Add(mainSizer, 1, wx.ALL | wx.EXPAND, 0)
		self.SetSizer(containerSizer)
		self.Layout()
		self.Centre()

	def saveSettings(self, event): 
		host = self.textHost.GetValue()
		port = self.textPort.GetValue()
		user = self.textUser.GetValue()
		password = self.textPassword.GetValue()
		self.config = self.config.create_config(host,port,user,password)
		self.__load_config()
		message = "Settings has been saved!"
		dialog = messageDialog(message,None,wx.ID_ANY,"")
		dialog.ShowModal()
		dialog.Destroy()
		self.Destroy()

	def cancelSettings(self, event):
		self.Destroy()


class messageDialog(wx.Dialog):
	def __init__(self, message = None ,*args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.buttonClose = wx.Button(self, wx.ID_ANY, "OK")
		self.message = message
		self.__set_properties()
		self.__do_layout()
		self.__set_message()
		self.Bind(wx.EVT_BUTTON, self.closeAlert, self.buttonClose)

	def __set_properties(self):
		self.SetTitle("Alert")
		self.buttonClose.SetMinSize((96, 32))

	def __do_layout(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.labelAlert = wx.StaticText(self, wx.ID_ANY, "Configuration error!\nPlease adjust the settings in the File> Settings menu")
		mainSizer.Add(self.labelAlert, 2, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 10)
		mainSizer.Add(self.buttonClose, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.Layout()
		self.Centre()

	def __set_message(self):
		if self.message != None:
			self.labelAlert.SetLabel(self.message)

	def closeAlert(self, event):
		self.Destroy()

class configLoad():
	def __init__(self):
		self.config = cfp.ConfigParser()
		if not os.path.isfile('config.ini'):
			self.__create_default_config()
		else:
			self.__load_config()
	
	def __create_default_config(self):
		self.config["SMTP"] = {}
		self.config["SMTP"]["host"] = "smtp-mail.outlook.com"
		self.config["SMTP"]["port"]  = "587"
		self.config["SMTP"]["user"]  = "your@email"
		self.config["SMTP"]["password"]  = "Y0uRp4S5w0rD"
		with open("config.ini",'w') as configfile:
			self.config.write(configfile)
		return self.config

	def create_config(self,host,port,user,password):
		self.config["SMTP"]["host"] = host
		self.config["SMTP"]["port"]  = port
		self.config["SMTP"]["user"]  = user
		self.config["SMTP"]["password"]  = password
		with open("config.ini",'w') as configfile:
			self.config.write(configfile)
		return self.config
	
	def __load_config(self):
		self.config.read('config.ini')
		return self.config

	def getHost(self):
		return "{}".format(self.config["SMTP"]["host"])
	
	def getPort(self):
		return "{}".format(self.config["SMTP"]["port"])

	def getUser(self):
		return "{}".format(self.config["SMTP"]["user"])

	def getPassword(self):
		return "{}".format(self.config["SMTP"]["password"])

	def __str__(self):
		host = self.config['SMTP']["host"]
		port = self.config["SMTP"]["port"]
		user = self.config["SMTP"]["user"]
		password = self.config["SMTP"]["password"]
		return "Host: {}\nport: {}\nuser:{}\npassword:{}".format(host,port,user,password)

class emailApp(wx.App):
	def OnInit(self):
		self.frame = mainFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

if __name__ == "__main__":
	emailApp = emailApp(0)
	emailApp.MainLoop()

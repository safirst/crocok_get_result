# -*- coding: utf-8 -*-
#
#   =================================================================
#   crocok_get_result.py / Getting results from crocok testing system
#   v. 0.0.4
#   =================================================================

__author__ = "Anton Senkovskiy"
__copyright__ = "Copyright 2015, Anton Senkovskiy"
__version__ = "0.0.4"
__email__ = "asenkovskiy@croc.ru"
__status__ = "Production"

# importing wx files
import wx
# import ssh & sftp library
import paramiko
# import stuff for sleep timer
import time
# resource_path function
import res
# import the newly created GUI file
import gui
import json

SRV_URL = "exam.crocok.ru"
SRV_PORT = 22
SRV_KEY_PASS = "111111"
SRV_USER = "asenkovskiy"
SRV_SCRIPT = "/home/asenkovskiy/01_Тираж_2015/Results/get-exam-results.py"
SRV_OUT_PATH = "/home/asenkovskiy/ResOut/result_"
SRV_KEY_NAME = res.resource_path("key.pem")
VER_TXT = "ver. 0.0.4"
CONF_FILE = "./settings.cfg"

# set global vars
rep_name = ""
test_name = ""
num_attempts = 0

# inherit from the MainFrame created in wxFormBuilder and create CalcFrame
class MyFrame(gui.MainFrame):
    # constructor
    def __init__(self, parent):
        global test_name
        global rep_name
        global data
        global num_attempts

        # initialize parent class
        try:
            with open(CONF_FILE) as json_data_file:
                data = json.load(json_data_file)

            # initialize choiser with first name from config
            i = 0
            rep_name = data[i]["name"]
            test_name = data[i]["test_name"]
            num_attempts = data[i]["attempts"]

            for n in data:
                gui.test_choiserChoices.append(data[i]["name"])
                i += 1
            gui.MainFrame.__init__(self, parent)
            self.statusBar.SetStatusText(VER_TXT)

        except Exception:
            gui.MainFrame.__init__(self, parent)
            self.statusBar.SetStatusText("Нет конфига!")

    # wx calls this function with and 'event' object
    def getFunc(self, event):

        global test_name
        global rep_name
        global num_attempts

        try:
            # Connecting to SRV for making our files
            mkey = paramiko.RSAKey.from_private_key_file(SRV_KEY_NAME, SRV_KEY_PASS)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # print("Connecting...")
            self.statusBar.SetStatusText("Подключаюсь...")
            client.connect(hostname=SRV_URL, username=SRV_USER, pkey=mkey)
            # print("Connected.")
            self.statusBar.SetStatusText("Подключен.")

            # Running scripts to make result files
            command = SRV_SCRIPT + " " + test_name + " " + num_attempts + " > " + SRV_OUT_PATH + rep_name + ".csv"
            #print("Попытка: ", command)
            self.statusBar.SetStatusText("Ищу тесты...")
            # stdin, stdout, stderr = client.exec_command(command1)
            # waiting 6 seconds for script running
            client.exec_command(command)
            time.sleep(6)

            self.statusBar.SetStatusText("Нашел.")
            client.close()

            # Connecting to SRV for receiving files through SFTP
            client = paramiko.Transport((SRV_URL, SRV_PORT))
            client.connect(username=SRV_USER, pkey=mkey)
            sftp = paramiko.SFTPClient.from_transport(client)
            remotepath = SRV_OUT_PATH + rep_name + ".csv"

            localpath = "Результат_" + rep_name + ".csv"
            self.statusBar.SetStatusText("Качаю...")
            sftp.get(remotepath, localpath)
            time.sleep(3)
            sftp.close()
            client.close()
            self.statusBar.SetStatusText("Готово!")
        except Exception:
            # print("error")
            self.statusBar.SetStatusText("Ошибка!")

    # Get user repo choice from choiser
    def choiseFunc(self, event):
        global rep_name
        global test_name
        global data
        global num_attempts

        cur_name = []
        i = 0
        for n in data:
                cur_name.append(data[i]["name"])
                i += 1

        rep_name = self.test_choiser.GetStringSelection()
        cur_select = cur_name.index(rep_name)
        test_name = data[cur_select]["test_name"]
        num_attempts = data[cur_select]["attempts"]

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
app = wx.App(False)

# create an object of MainFrame
frame = MyFrame(None)
# show the frame
frame.Show(True)
# start the applications
app.MainLoop()

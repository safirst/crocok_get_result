# -*- coding: utf-8 -*-
#
#   =================================================================
#   crocok_get_result.py / Getting results from crocok testing system
#   v. 0.0.2b
#   =================================================================

__author__ = "Anton Senkovskiy"
__copyright__ = "Copyright 2015, Anton Senkovskiy"
__version__ = "0.0.3b"
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


SRV_URL = "exam.crocok.ru"
SRV_PORT = 22
SRV_KEY_PASS = "111111"
SRV_USER = "asenkovskiy"
SRV_SCRIPT = "/home/asenkovskiy/01_Тираж_2015/Results/get-tn-results.py"
SRV_OUT_PATH = "/home/asenkovskiy/result_"
SRV_KEY_NAME = res.resource_path("key.pem")

# set global vars to first choiser option
rep_name = "Логистика"
test_name = "Тестирование_Логистика"

# inherit from the MainFrame created in wxFormBuilder and create CalcFrame
class MyFrame(gui.MainFrame):
    # constructor
    def __init__(self, parent):
        # initialize parent class
        gui.MainFrame.__init__(self, parent)

    # wx calls this function with and 'event' object
    def getFunc(self, event):
        global test_name
        global rep_name
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
            command1 = SRV_SCRIPT + " " + test_name + " " + "> result_" + rep_name + ".csv"
            command2 = SRV_SCRIPT + " " + test_name + "2" + " " + "> result_" + rep_name + "2.csv"
            command3 = SRV_SCRIPT + " " + test_name + "3" + " " + "> result_" + rep_name + "3.csv"
            # print("Попытка1: ", command1)
            self.statusBar.SetStatusText("Ищу попытку 1...")
            # stdin, stdout, stderr = client.exec_command(command1)
            # waiting 6 seconds for script running
            client.exec_command(command1)
            time.sleep(6)
            self.statusBar.SetStatusText("Ищу попытку 2...")
            client.exec_command(command2)
            time.sleep(6)
            self.statusBar.SetStatusText("Ищу попытку 3...")
            client.exec_command(command3)
            time.sleep(6)
            self.statusBar.SetStatusText("Попытки найдены.")
            client.close()

            # Connecting to SRV for receiving files through SFTP
            client = paramiko.Transport((SRV_URL, SRV_PORT))
            client.connect(username=SRV_USER, pkey=mkey)
            sftp = paramiko.SFTPClient.from_transport(client)
            remotepath1 = SRV_OUT_PATH + rep_name + ".csv"
            remotepath2 = SRV_OUT_PATH + rep_name + "2.csv"
            remotepath3 = SRV_OUT_PATH + rep_name + "3.csv"
            localpath1 = "result_" + rep_name + "1.csv"
            localpath2 = "result_" + rep_name + "2.csv"
            localpath3 = "result_" + rep_name + "3.csv"
            self.statusBar.SetStatusText("Качаю попытку 1...")
            sftp.get(remotepath1, localpath1)
            time.sleep(2)
            self.statusBar.SetStatusText("Качаю попытку 2...")
            sftp.get(remotepath2, localpath2)
            time.sleep(2)
            self.statusBar.SetStatusText("Качаю попытку 3...")
            sftp.get(remotepath3, localpath3)
            time.sleep(2)
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

        rep_name = self.test_choiser.GetStringSelection()
        if rep_name == "Логистика":
            test_name = "Тестирование_Логистика"
        elif rep_name == "ТНТ":
            test_name = "Тестирование_ТНТ"
        elif rep_name == "Сибирь":
            test_name = "Тестирование_Сибирь"
        elif rep_name == "Гипротруба":
            test_name = "Тестирование_Гипротрубопровод"
        elif rep_name == "Западная сибирь":
            test_name = "Тестирование_Западная_сибирь"
        elif rep_name == "Дружба":
            test_name = "Тестирование_Дружба"
        elif rep_name == "Балтика":
            test_name = "Тестирование_Балтика"
        elif rep_name == "Надзор":
            test_name = "Тестирование_Надзор"
        elif rep_name == "Охрана":
            test_name = "Тестирование_Охрана"
        elif rep_name == "Приволга":
            test_name = "Тестирование_Приволга"
        elif rep_name == "Диаскан":
            test_name = "Тестирование_Диаскан"
        elif rep_name == "Козьмино":
            test_name = "Тестирование_Козьмино"
        elif rep_name == "Омега":
            test_name = "Тестирование_Омега"
        elif rep_name == "ТСД":
            test_name = "Тестирование_ТСД"
        elif rep_name == "Томский_завод":
            test_name = "Тестирование_Томский_завод"

# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
app = wx.App(False)

# create an object of CalcFrame
frame = MyFrame(None)
# show the frame
frame.Show(True)
# start the applications
app.MainLoop()

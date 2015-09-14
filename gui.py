# -*- coding: utf-8 -*- 

import wx
#import wx.xrc
import wx.xml
import res

CROC_IMG = res.resource_path(".\\croc.jpg")

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"КРОК-Экзамен", pos=wx.DefaultPosition,
                          size=wx.Size(205, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        #self.SetSizeHintsSz(wx.DefaultSize, wx.Size(205, 300))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(CROC_IMG, wx.BITMAP_TYPE_ANY),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_bitmap1, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"ТН-Тираж 2015", wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTRE)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))

        bSizer1.Add(self.m_staticText2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Результаты теста для:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        bSizer1.Add(self.m_staticText3, 0, wx.ALL | wx.EXPAND, 5)

        test_choiserChoices = [u"Логистика", u"ТНТ", u"Сибирь", u"Гипротруба", u"Западная сибирь", u"Дружба",
                               u"Балтика", u"Надзор", u"Охрана", u"Приволга", u"Диаскан", u"Козьмино", u"Омега", u"ТСД",
                               u"Томский_завод"]
        self.test_choiser = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, test_choiserChoices, 0)
        self.test_choiser.SetSelection(0)
        bSizer1.Add(self.test_choiser, 0, wx.ALL | wx.EXPAND, 5)

        self.get_button = wx.Button(self, wx.ID_ANY, u"Получить", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.get_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.statusBar = self.CreateStatusBar()


        self.Centre(wx.BOTH)

        # Connect Events
        self.test_choiser.Bind(wx.EVT_CHOICE, self.choiseFunc)
        self.get_button.Bind(wx.EVT_BUTTON, self.getFunc)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def choiseFunc(self, event):
        event.Skip()

    def getFunc(self, event):
        event.Skip()

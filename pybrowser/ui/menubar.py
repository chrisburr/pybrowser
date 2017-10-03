import wx


class FileMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        wx.Menu.__init__(self, *args, **kwargs)

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = self.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuExit = self.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def OnAbout(self, e):
        # A message dialog box with an OK button
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)


class MenuBar(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        wx.MenuBar.__init__(self, *args, **kwargs)

        self.file_menu = FileMenu()

        self.Append(self.file_menu, "&File")

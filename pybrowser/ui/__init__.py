import wx
import wxmplot

from .menubar import MenuBar
from .filesystem_tree import FileSystemTree
from .open_files_tree import OpenFilesTree


class TabPanel(wx.Panel):
    def __init__(self, parent, componet):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.component = componet(self)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.component, 1, wx.ALL | wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(vsizer)


class LeftNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

        # Create the first tab and add it to the notebook
        self.tree_tab = TabPanel(self, FileSystemTree)
        self.AddPage(self.tree_tab, "File system")

        # Create and add the second tab
        self.files_tab = TabPanel(self, OpenFilesTree)
        self.AddPage(self.files_tab, "Open files")

        # Create and add the third tab
        self.plot_config_tab = TabPanel(self, wx.TextCtrl)
        self.AddPage(self.plot_config_tab, "Plot settings")

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print(f'OnPageChanged,  old: {old} new: {new} sel: {sel}')
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print(f'OnPageChanging, old: {old} new: {new} sel: {sel}')
        event.Skip()


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.notebook = LeftNotebook(self)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(vsizer)


class RightPanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.plot = wxmplot.PlotPanel(self, dpi=100, size=(2400, 1600))
        self.plot.plot([0, 1, 2], [2, 3, 1])

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.plot, 1, wx.ALL | wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(vsizer)


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 700))

        splitter = wx.SplitterWindow(self)
        self.left_panel = LeftPanel(splitter)
        self.right_panel = RightPanel(splitter)

        # split the window
        splitter.SplitVertically(self.left_panel, self.right_panel)
        splitter.SetMinimumPaneSize(20)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Status Bar
        self.CreateStatusBar()

        # Menu Bar
        menubar = MenuBar()
        self.SetMenuBar(menubar)

        self.Show(True)


def run():
    app = wx.App(False)
    frame = MainWindow(None, "PyBrowser")
    frame.Center()
    app.MainLoop()

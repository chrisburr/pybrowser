import wx
import os
from pathlib import PurePosixPath

import pandas as pd

from .. import file_utils


class OpenFilesTree(wx.TreeCtrl):
    def __init__(self, *args, style=wx.TR_HAS_BUTTONS | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER, **kwargs):
        wx.TreeCtrl.__init__(self, *args, style=style, **kwargs)

        self._files = {}

        # Add an example file for now
        self.open_file('/Users/cburr/Physics/d2hll-analysis/output/classifier/2015/DpToKee_OS_data.hdf')

        # register the self.on_expand function to be called
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expand, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_double_click, self)

    def open_file(self, filename):
        self._files[filename] = pd.HDFStore(filename)
        self.build_tree(filename)

    def on_double_click(self, event):
        filename, path, branch, is_expanded = self.GetItemData(event.GetItem())
        if path and branch:
            # TODO: Pass around a top level object or something
            plot = self.GetParent().GetParent().GetParent().GetParent().GetParent().right_panel.plot
            df = self._files[filename][path]
            plot.clear()
            plot.axes.grid(True)
            plot.axes.hist(df[branch])
            plot.draw()
            plot.canvas.Refresh()
        else:
            print(self.GetItemData(event.GetItem()))

    def on_expand(self, event):
        '''on_expand is called when the user expands a node on the tree
        object. It checks whether the node has been previously expanded. If
        not, the extend_tree function is called to build out the node, which
        is then marked as expanded.'''

        # get the wxID of the entry to expand and check it's validity
        itemID = event.GetItem()
        if not itemID.IsOk():
            itemID = self.GetSelection()

        # only build that tree if not previously expanded
        filename, path, branch, is_expanded = self.GetItemData(itemID)
        if not is_expanded:
            # clean the subtree and rebuild it
            self.DeleteChildren(itemID)
            self.extend_tree(itemID)
            self.SetItemData(itemID, (filename, path, branch, True))

    def build_tree(self, rootdir):
        '''Add a new root element and then its children'''
        self.rootID = self.AddRoot(rootdir)
        self.SetItemData(self.rootID, (rootdir, None, None, True))
        self.extend_tree(self.rootID)
        self.Expand(self.rootID)

    def extend_tree(self, parentID):
        '''extend_tree is a semi-lazy directory tree builder. It takes
        the ID of a tree entry and fills in the tree with its child
        subdirectories and their children - updating 2 layers of the
        tree. This function is called by build_tree and on_expand methods'''

        # retrieve the associated absolute path of the parent
        filename, path, branch, is_expanded = self.GetItemData(parentID)

        if path is None:
            store = self._files[filename]

            for key in store:
                childID = self.AppendItem(parentID, key)
                self.SetItemData(childID, (filename, key, None, True))

                # Now the child entry will show up, but it current has no
                # known children of its own and will not have a '+' showing
                # that it can be expanded to step further down the tree.
                # Solution is to go ahead and register the child's children,
                # meaning the grandchildren of the original parent
                # TODO Can this be done without reading the full dataframe?
                item = store[key]
                if isinstance(item, pd.DataFrame):
                    for column in store.get(key).columns:
                        grandchildID = self.AppendItem(childID, column)
                        self.SetItemData(grandchildID, (filename, key, column, False))
                else:
                    print('TODO')
        elif branch is None:
            pass
        else:
            pass

import wx
import os

from .. import file_utils


class FileSystemTree(wx.TreeCtrl):
    def __init__(self, *args, style=wx.TR_HAS_BUTTONS | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER, **kwargs):
        wx.TreeCtrl.__init__(self, *args, style=style, **kwargs)

        # register the self.onExpand function to be called
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.onExpand, self)
        # initialize the tree
        self.buildTree('/')

    def onExpand(self, event):
        '''onExpand is called when the user expands a node on the tree
        object. It checks whether the node has been previously expanded. If
        not, the extendTree function is called to build out the node, which
        is then marked as expanded.'''

        # get the wxID of the entry to expand and check it's validity
        itemID = event.GetItem()
        if not itemID.IsOk():
            itemID = self.GetSelection()

        # only build that tree if not previously expanded
        old_pydata = self.GetItemData(itemID)
        if not old_pydata[1]:
            # clean the subtree and rebuild it
            self.DeleteChildren(itemID)
            self.extendTree(itemID)
            self.SetItemData(itemID, (old_pydata[0], True))

    def buildTree(self, rootdir):
        '''Add a new root element and then its children'''
        self.rootID = self.AddRoot(rootdir)
        self.SetItemData(self.rootID, (rootdir, 1))
        self.extendTree(self.rootID)
        self.Expand(self.rootID)

    def extendTree(self, parentID):
        '''extendTree is a semi-lazy directory tree builder. It takes
        the ID of a tree entry and fills in the tree with its child
        subdirectories and their children - updating 2 layers of the
        tree. This function is called by buildTree and onExpand methods'''

        # retrieve the associated absolute path of the parent
        parentDir = self.GetItemData(parentID)[0]

        subdirs = os.listdir(parentDir)
        subdirs.sort()
        for child in subdirs:
            child_path = os.path.join(parentDir, child)

            if file_utils.is_hidden(child_path):
                continue

            if os.path.isdir(child_path) and not os.path.islink(child):
                # add the child to the parent
                childID = self.AppendItem(parentID, child)
                # associate the full child path with its tree entry
                self.SetItemData(childID, (child_path, False))

                # Now the child entry will show up, but it current has no
                # known children of its own and will not have a '+' showing
                # that it can be expanded to step further down the tree.
                # Solution is to go ahead and register the child's children,
                # meaning the grandchildren of the original parent
                newParent = child
                newParentID = childID
                newParentPath = child_path

                try:
                    newsubdirs = os.listdir(newParentPath)
                except PermissionError:
                    print('TODO')
                except Exception:
                    print('TODO')
                else:
                    newsubdirs.sort()
                    for grandchild in newsubdirs:
                        grandchild_path = os.path.join(newParentPath, grandchild)
                        if os.path.isdir(grandchild_path) and not os.path.islink(grandchild_path):
                            grandchildID = self.AppendItem(newParentID, grandchild)
                            self.SetItemData(grandchildID, (grandchild_path, False))

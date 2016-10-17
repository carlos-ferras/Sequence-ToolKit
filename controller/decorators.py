from __future__ import unicode_literals


from PyQt5 import QtCore


def loadingCursor(empty=False):
    def decorator(fun):
        def inside(self, *arg):
            try:
                self.main_window.setCursor(QtCore.Qt.WaitCursor)
            except:
                try:
                    parent_windows = self.parent().parent().parent().parent()
                    parent_windows.setCursor(QtCore.Qt.WaitCursor)
                except:
                    pass
            if empty:
                out = fun(self)
            else:
                out = fun(self, *arg)
            try:
                self.main_window.setCursor(QtCore.Qt.ArrowCursor)
            except:
                try:
                    parent_windows = self.parent().parent().parent().parent()
                    parent_windows.setCursor(QtCore.Qt.ArrowCursor)
                except:
                    pass
            return out
        return inside
    return decorator

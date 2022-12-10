from PyQt5.QtWidgets import QErrorMessage


def error(err):
    error_dialog = QErrorMessage(err)
    error_dialog.show()

def strweight(s):
    for ch in s:
        if ch not in [' ', '\n']:
            return True
    return False
import win32gui
import win32process

def _EnumWindowsProc(hwnd, data):

    window_text, process_ids = data

    if win32gui.GetWindowText(hwnd) == window_text:

        process_ids.append(win32process.GetWindowThreadProcessId(hwnd)[1])

    return True

def get_window_process_ids(window_text):

    process_ids = []
    win32gui.EnumWindows(_EnumWindowsProc, (window_text, process_ids))

    return process_ids

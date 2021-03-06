from PIL import Image

import win32clipboard
from io import BytesIO
from time import sleep
import win32com.client
import keyboard
import pythoncom
import os
from shubi_files.core import path
import sys

server_uploads = path.get('server/uploads')

class ClipBoard:
    @classmethod
    def send_to_clipboard(cls, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    @classmethod
    def erase(cls, name):
        for _ in name + ' ':
            keyboard.send('backspace')

    @classmethod
    def paste(cls, file, tag):
        path = os.path.join(server_uploads, file)
        print(path)
        image = Image.open(path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        cls.send_to_clipboard(win32clipboard.CF_DIB, data)
        pythoncom.CoInitialize()
        # shell = win32com.client.Dispatch("WScript.Shell")
        # cls.erase(tag)
        # shell.SendKeys('^(v)')

# coding=utf-8
import sys
import traceback
import tkinter as tk
from tkinter import filedialog
from LogTools import LogTools
import multiprocessing
from threading import *
import threading


reload(sys)
sys.setdefaultencoding('utf-8')


class TkTools():


    def tk_openfile(self, result_queue=None, title='请选择一个文件', initialdir=r'D:\\', filetypes=[("python", ".py"), ('All Files', ' *')], defaultextension=".py", multiple=False):
        file_path = ""
        try:
            # lock = threading.RLock()
            # with lock:
            self.root = tk.Tk()
            self.root.attributes('-topmost', 'true')
            self.root.withdraw()
            file_path = filedialog.askopenfilename(parent=self.root, title=title, initialdir=initialdir, filetypes=filetypes, defaultextension=defaultextension, multiple=multiple)
        except Exception as e:
            print traceback.format_exc()
        if result_queue:
            result_queue.put(file_path)

    def openfile(self, title='请选择一个文件', initialdir=r'D:\\', filetypes=[("python", ".py"), ('All Files', ' *')], defaultextension=".py", multiple=False):
        """
        打开文件 使用线程打开tk
        :param title:
        :param initialdir:
        :param filetypes:
        :param defaultextension:
        :param multiple:
        :return:
        """
        file_path = ""
        # 创建RLock对象
        result_queue = multiprocessing.Queue()
        popup_thread = multiprocessing.Process(target=self.tk_openfile, args=(result_queue, title, initialdir, filetypes, defaultextension, multiple))
        popup_thread.start()
        # popup_thread.join()
        file_path = result_queue.get()

        return file_path
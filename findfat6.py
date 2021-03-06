#  coding:utf:8
#  file:findfat6.py
# 创建tkinter窗口和菜单
# 初步添加菜单功能，并添加菜单响应函数
# 增加ScanRubbish函数，并在MenuScanRubbish中多线程运行
# 添加扫描计算机所有的盘符，添加函数GetDrives()函数。
# 添加删除垃圾的函数DeleteRubbish()
# 添加扫描大文件函数ScanBigFile()
# 添加搜索文件函数SearchFile()


import os
import os.path
import threading
import tkinter
import tkinter.messagebox
import tkinter.simpledialog

#  定义垃圾文件的扩展名称，即文件类型

rubbishExt = ['.log', ]


# rubbishExt = ['.tmp', '.bak', '.old', '.wbk', '.xlk', '.mp', '.log', '.gid', '.chk', '.syd', '.$$$', '.@@@', '.~*']


class Windows:
    def __init__(self):

        # 定义路径

        self.drives = GetDrives()

        self.root = tkinter.Tk()
        # print('all drives:', self.drives)

        # 创建菜单

        menu = tkinter.Menu(self.root)

        # 创建“系统”子菜单

        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="关于...", command=self.MenuAbout)
        submenu.add_separator()
        submenu.add_command(label="退出", command=self.MenuExit)
        menu.add_cascade(label="系统", menu=submenu)

        #  创建“清理”子菜单

        submenu = tkinter.Menu(menu, tearoff=1)
        submenu.add_command(label="扫描垃圾文件", command=self.MenuScanRubbish)
        submenu.add_separator()
        submenu.add_command(label="删除垃圾文件", command=self.MenuDelRubbish)
        menu.add_cascade(label="清理", menu=submenu)

        # 创建“查找”子菜单

        submenu = tkinter.Menu(menu, tearoff=0)
        submenu.add_command(label="搜索大文件", command=self.MenuScanBigFile)
        submenu.add_separator()
        submenu.add_command(label="按名称搜索文件", command=self.MenuSearchFile)
        menu.add_cascade(label="搜索", menu=submenu)

        self.root.config(menu=menu)

        # 创建标签，用于显示状态信息

        self.progress = tkinter.Label(self.root, anchor=tkinter.W,
                                      text='状态', bitmap='hourglass', compound='left')
        self.progress.place(x=10, y=10, width=480, height=15)

        #  创建文本框，显示文件列表

        self.flist = tkinter.Text(self.root)
        self.flist.place(x=10, y=10, width=480, height=350)

        #  为文本添加垂直滚动条

        self.vscroll = tkinter.Scrollbar(self.flist)
        self.vscroll.pack(side='right', fill='y')
        self.flist['yscrollcommand'] = self.vscroll.set
        self.vscroll['command'] = self.flist.yview

    def Mainloop(self):
        self.root.title("Findfat-6")
        self.root.minsize(500, 400)
        self.root.maxsize(500, 400)
        self.root.mainloop()

    #  “关于”菜单

    def MenuAbout(self):
        tkinter.messagebox.showinfo("FindFat",
                                    "这是使用Python编写的Windows优化程序。\n")

    #  “退出”菜单

    def MenuExit(self):
        self.root.quit()

    #  “扫描垃圾文件”菜单

    def MenuScanRubbish(self):
        result = tkinter.messagebox.askquestion("FindFat", "扫描垃圾文件将需要较长时间，是否继续?")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("FindFat", "马上开始扫描垃圾文件")
        # self.ScanRubbish()
        self.drives = GetDrives()
        t = threading.Thread(target=self.ScanRubbish, args=(self.drives,))
        t.start()

    #  “删除垃圾文件”菜单

    def MenuDelRubbish(self):
        result = tkinter.messagebox.askquestion("FindFat", "删除垃圾文件将需要较长时间，是否继续？")
        if result == 'no':
            return
        tkinter.messagebox.showinfo("FindFat", "马上开始删除垃圾文件")
        self.drives = GetDrives()
        t = threading.Thread(target=self.DeleteRubbish, args=(self.drives,))
        t.start()

    #  “扫描大文件”菜单

    def MenuScanBigFile(self):
        s = tkinter.simpledialog.askinteger('Findfat', '请设置大文件的大小(M)')
        t = threading.Thread(target=self.ScanBigFile, args=(s,))
        t.start()

    #  “按名称搜索文件”菜单

    def MenuSearchFile(self):
        s = tkinter.simpledialog.askstring('FindFat', '请输入文件名部分或全部字符')
        t = threading.Thread(target=self.SearchFile, args=(s,))
        t.start()

    #################################################################
    #   编写ScanRubbish函数，在MenuScanRubbish中调用即可以使用
    #################################################################

    def ScanRubbish(self, scanpath):
        # print('all disk:',scanpath)
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root, dirs, files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit == '':  # 若无文件扩展名
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >= 0:  # 扩展名在垃圾文件里列表中
                                fname = os.path.join(os.path.abspath(root), fil)
                                filesize += os.path.getsize(fname)
                                if total % 20 == 0:
                                    self.flist.delete(0.0, tkinter.END)
                                self.flist.insert(tkinter.END, fname + '\n')
                                l = len(fname)
                                if l > 60:
                                    self.progress['text'] = fname[:30] + '...' + fname[1 - 30:1]
                                else:
                                    self.progress['text'] = fname
                                total += 1  # 计数
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass
        self.progress['text'] = "找到 %s 个垃圾文件，共占用 %.2f M 磁盘空间" % (total, filesize / 1024 / 1024)

    #  ##################删除垃圾文件############################################

    def DeleteRubbish(self, scanpath):
        global rubbishExt
        total = 0
        filesize = 0
        for drive in scanpath:
            for root, dirs, files in os.walk(drive):
                try:
                    for fil in files:
                        filesplit = os.path.splitext(fil)
                        if filesplit[1] == '':  # 若文件无扩展名
                            continue
                        try:
                            if rubbishExt.index(filesplit[1]) >= 0:  # 扩展名在垃圾文件扩展名中
                                fname = os.path.join(os.path.abspath(root), fil)
                                filesize += os.path.getsize(fname)
                                try:
                                    os.remove(fname)  # 删除文件
                                    l = len(fname)
                                    if l > 50:
                                        fname = fname[:25] + '...' + fname[1 - 25:1]
                                    if total % 15 == 0:
                                        self.flist.delete(0.0, tkinter.END)
                                    self.flist.insert(tkinter.END, 'Deleted' + fname + '\n')
                                    self.progress['text'] = fname
                                    total += 1
                                except:
                                    pass
                        except ValueError:
                            pass
                except Exception as e:
                    print(e)
                    pass

    #  #################搜索大文件###################################################

    def ScanBigFile(self, filesize):
        total = 0
        filesize = filesize * 1024 * 1024
        for drive in GetDrives():
            for root, dirs, files in os.walk(drive):
                for fil in files:
                    try:
                        fname = os.path.abspath(os.path.join(root, fil))
                        fsize = os.path.getsize(fname)
                        self.progress['text'] = fname  # 在标签的每一个地方遍历
                        if fsize >= filesize:
                            total += 1
                            self.flist.insert(tkinter.END, '%s,[%.2f M]\n' % (fname, fsize / 1024 / 1024))
                    except:
                        pass

    #  ###################按名称搜索文件##################################################

    def SearchFile(self, fname):
        total = 0
        fname = fname.upper()
        for drive in GetDrives():
            for root, dir, files in os.walk(drive):
                for fil in files:
                    try:
                        fn = os.path.abspath(os.path.join(root, fil))
                        l = len(fn)
                        if l > 50:
                            self.progress['text'] = fn[:25] + '...' + fn[1 - 25:1]
                        else:
                            self.progress['text'] = fn
                        if fil.upper().find(fname) >= 0:
                            total += 1
                            self.flist.insert(tkinter.END, fn + '\n')
                    except:
                        pass


##########################################################
# 取得当前计算机的盘符
##########################################################

def GetDrives():
    drives = []
    for i in range(65, 91):
        vol = chr(i) + ':/'
        if os.path.isdir(vol):
            drives.append(vol)
    return tuple(drives)


if __name__ == '__main__':
    window = Windows()
    window.Mainloop()

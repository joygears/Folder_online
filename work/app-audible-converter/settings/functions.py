# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: settings\functions.py
import os, sys, psutil, hashlib
from struct import unpack
from settings.settings import iswindows, isosx

def explorer_select_files(files):
    import webbrowser, subprocess
    if iswindows:
        from win32com.shell import shell, shellcon

    def win_select(files):
        if files:
            path = os.path.dirname(files[0])
            folder_pidl = shell.SHILCreateFromPath(path, 0)[0]
            desktop = shell.SHGetDesktopFolder()
            shell_folder = desktop.BindToObject(folder_pidl, None, shell.IID_IShellFolder)
            name_to_item_mapping = dict([(desktop.GetDisplayNameOf(item, shellcon.SHGDN_FORPARSING | shellcon.SHGDN_INFOLDER), item) for item in shell_folder])
            to_show = []
            for i in files:
                file = os.path.split(i)[1]
                if file in name_to_item_mapping:
                    to_show.append(name_to_item_mapping[file])

            shell.SHOpenFolderAndSelectItems(folder_pidl, to_show, 0)

    def osx_select(files):
        directory, _ = os.path.split(files[0])
        paths = [i[1:].replace('/', ':') for i in files]
        lines = []
        args = []
        for i, v in enumerate(paths):
            tmp = 'set txt' + str(i) + ' to alias ' + '"' + v + '"' + '\n'
            lines.append(tmp)
            args.append('txt' + str(i))

        lines.append('tell application "Finder" to reveal {' + ','.join(args) + '}')
        scriptpath = os.path.join(os.path.expanduser('~'), 'epubortmpscript')
        with open(scriptpath, 'w', encoding='utf8') as (fp):
            fp.writelines(lines)
        subprocess.call(['open', directory])
        subprocess.call(['osascript', scriptpath])
        os.remove(scriptpath)

    try:
        if iswindows:
            win_select(files)
        else:
            if isosx:
                osx_select(files)
    except Exception as e:
        print(e)


def restart():
    import sys
    python = sys.executable
    (os.execl)(python, python, *sys.argv)


def isexe(f):
    return os.path.isfile(f) and os.access(f, os.X_OK)


def getmac():
    import uuid
    return uuid.UUID(int=(uuid.getnode())).hex[-12:]


def limit_path(path):
    if len(path) > 240:
        return path[:240] + os.path.splitext(path)[1]
    else:
        return path


def os_sep(path):
    return path.replace('/', os.sep).replace('\\', os.sep)


def getExeDirectory():
    path = sys.path[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return path


def kill_conv():
    """
    当主程序关闭 杀死正在进行进行工作的exe进程
    :return:
    """
    try:
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if iswindows:
                if p.name() == 'win':
                    p.kill()
                else:
                    if p.name() == 'mac':
                        p.kill()

    except:
        pass


def mkdir(path):
    """数值递增的创建目录（如果目录已经存在）"""
    i = 1
    while True:
        if not os.path.exists(path):
            os.mkdir(path)
            return path
        tmpdirname = path + ' (%s)' % str(i)
        if not os.path.exists(tmpdirname):
            os.mkdir(tmpdirname)
            return tmpdirname
        i += 1


def choosename(filepath):
    """文件递增命名 不会覆盖同名文件"""
    i = 1
    while True:
        if not os.path.exists(filepath):
            return filepath
        tmppath = filepath[:-4] + ' (%s)' % str(i) + filepath[-4:]
        if not os.path.exists(tmppath):
            return tmppath
        i += 1


def getmd5(value):
    return hashlib.md5(value.encode('utf8')).hexdigest()


def get_cover_from_aa(aafile):
    """
    get cover from aa file
    :param aafile: aafile path
    :return: cover data
            1. have cover -- return cover data
            2. no cover -- return b''
    """
    magic_jfif = b'\xff\xd8\xff\xe0\x00\x10JFIF'
    magic_exif = b'\xff\xd8\xff\xe1\x00\x18Exif'
    cover_data = b''
    length = 4096
    try:
        with open(aafile, 'rb') as (f):
            for flag in [magic_exif, magic_jfif]:
                f.seek(0)
                if cover_data:
                    pass
                else:
                    pre = b''
                    for chunk in iter(lambda : f.read(length), b''):
                        if cover_data:
                            cover_data += chunk
                        else:
                            finded = (pre + chunk).find(flag)
                            if finded != -1:
                                cover_data = (pre + chunk)[finded:]
                            pre = chunk[-len(flag):]

    except Exception as e:
        print('Faild to get aa cover', e)

    return cover_data


def get_cover_from_aax(aaxfile):
    """
    get cover from aax file
    :param aaxfile: aaxfile path
    :return: cover data
            1. have cover -- return cover data
            2. no cover -- return b''
    """
    index = 0
    flag = b'covr'
    cover_data = b''
    length = 4096
    try:
        with open(aaxfile, 'rb') as (f):
            pre = b''
            for chunk in iter(lambda : f.read(length), b''):
                index += length
                finded = (pre + chunk).find(flag)
                if finded != -1:
                    index += finded - length - len(flag)
                    break
                pre = chunk[-len(flag):]

            if index:
                f.seek(index + len(flag))
                buf = unpack('>i', f.read(len(flag)))
                f.seek(12, 1)
                cover_size = buf[0] - 12
                cover_data = f.read(cover_size)
    except Exception as e:
        print('Faild to get aax cover', e)

    return cover_data


def os_name():
    import platform
    if iswindows:
        return 'Windows-' + platform.win32_ver()[0]
    else:
        if isosx:
            return 'macOS-' + platform.mac_ver()[0]
        return ''
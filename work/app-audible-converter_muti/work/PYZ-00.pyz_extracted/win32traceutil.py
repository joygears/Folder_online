# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: win32traceutil.py
import win32trace

def RunAsCollector():
    import sys
    try:
        import win32api
        win32api.SetConsoleTitle('Python Trace Collector')
    except:
        pass

    win32trace.InitRead()
    print('Collecting Python Trace Output...')
    try:
        while True:
            sys.stdout.write(win32trace.blockingread(500))

    except KeyboardInterrupt:
        print('Ctrl+C')


def SetupForPrint():
    win32trace.InitWrite()
    try:
        print('Redirecting output to win32trace remote collector')
    except:
        pass

    win32trace.setprint()


if __name__ == '__main__':
    RunAsCollector()
else:
    SetupForPrint()
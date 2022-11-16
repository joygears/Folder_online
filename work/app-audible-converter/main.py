# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: main.py


def main(product=None):
    try:
        from settings.settings import initProduct
        from module.logger import logger
        initProduct(product)
        from settings.settings import apps, sysLanguage, getMultiLang, iswindows, res
        from settings.functions import os_name
        logger.debug('Application start, ' + res.title + ', ' + os_name())
        if len(apps['app_language']) > 0:
            lang = apps['app_language'].replace('Epubor_', 'language_')
        else:
            apps['app_language'] = lang = sysLanguage()
        import os
        from settings.functions import os_sep, getExeDirectory
        from PyQt5.QtCore import QTranslator
        trans = QTranslator()
        trans.load(os_sep(os.path.join(getExeDirectory(), 'translator/' + lang)))
        from PyQt5.QtWidgets import QApplication
        if iswindows:
            from PyQt5.QtCore import Qt
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication([])
        app.installTranslator(trans)
        getMultiLang()
        from ui.dlgMain import dlgMain
        w = dlgMain()
        w.show()
        # res.regInfo.isRegister = True
        if res.regInfo.isRegister:
            w.btnReg.setVisible(False)
        else:
            from ui.dlgReg import DlgReg
            r = DlgReg(w)
            r.exec_()
        app.exec_()
    except Exception as e:
        import platform, traceback
        from settings import settings
        system_info = '%s_%s' % (platform.platform(), platform.machine())
        error_info = traceback.format_exc()
        response_info = '%s\n%s v%s\n%s' % (system_info, settings.res.__class__.__name__, settings.res.version, error_info)
        print(response_info)


if __name__ == '__main__':
    main()
/********************************************************************************
** Form generated from reading UI file 'sample_2_4.ui'
**
** Created by: Qt User Interface Compiler version 5.12.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SAMPLE_2_4_H
#define UI_SAMPLE_2_4_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_sample_2_4Class
{
public:
    QAction *actNew;
    QAction *actOpen;
    QAction *actExit;
    QAction *actCut;
    QAction *actCopy;
    QAction *actPaste;
    QAction *actItalic;
    QAction *actBold;
    QAction *actUnderline;
    QWidget *centralWidget;
    QWidget *widget;
    QTextEdit *textEdit;
    QPushButton *pushButton;
    QMenuBar *menuBar;
    QMenu *menu;
    QMenu *menu_2;
    QMenu *menu_3;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *sample_2_4Class)
    {
        if (sample_2_4Class->objectName().isEmpty())
            sample_2_4Class->setObjectName(QString::fromUtf8("sample_2_4Class"));
        sample_2_4Class->resize(1200, 800);
        actNew = new QAction(sample_2_4Class);
        actNew->setObjectName(QString::fromUtf8("actNew"));
        QIcon icon;
        icon.addFile(QString::fromUtf8(":/images/images/02.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actNew->setIcon(icon);
        actOpen = new QAction(sample_2_4Class);
        actOpen->setObjectName(QString::fromUtf8("actOpen"));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8(":/images/images/03.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actOpen->setIcon(icon1);
        actExit = new QAction(sample_2_4Class);
        actExit->setObjectName(QString::fromUtf8("actExit"));
        QIcon icon2;
        icon2.addFile(QString::fromUtf8(":/images/images/05.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actExit->setIcon(icon2);
        actCut = new QAction(sample_2_4Class);
        actCut->setObjectName(QString::fromUtf8("actCut"));
        QIcon icon3;
        icon3.addFile(QString::fromUtf8(":/images/images/06.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actCut->setIcon(icon3);
        actCopy = new QAction(sample_2_4Class);
        actCopy->setObjectName(QString::fromUtf8("actCopy"));
        QIcon icon4;
        icon4.addFile(QString::fromUtf8(":/images/images/11.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actCopy->setIcon(icon4);
        actPaste = new QAction(sample_2_4Class);
        actPaste->setObjectName(QString::fromUtf8("actPaste"));
        QIcon icon5;
        icon5.addFile(QString::fromUtf8(":/images/images/09.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actPaste->setIcon(icon5);
        actItalic = new QAction(sample_2_4Class);
        actItalic->setObjectName(QString::fromUtf8("actItalic"));
        actItalic->setCheckable(true);
        QIcon icon6;
        icon6.addFile(QString::fromUtf8(":/images/images/10.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actItalic->setIcon(icon6);
        actBold = new QAction(sample_2_4Class);
        actBold->setObjectName(QString::fromUtf8("actBold"));
        actBold->setCheckable(true);
        QIcon icon7;
        icon7.addFile(QString::fromUtf8(":/images/images/08.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actBold->setIcon(icon7);
        actUnderline = new QAction(sample_2_4Class);
        actUnderline->setObjectName(QString::fromUtf8("actUnderline"));
        actUnderline->setCheckable(true);
        QIcon icon8;
        icon8.addFile(QString::fromUtf8(":/images/images/12.ico"), QSize(), QIcon::Normal, QIcon::Off);
        actUnderline->setIcon(icon8);
        centralWidget = new QWidget(sample_2_4Class);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        widget = new QWidget(centralWidget);
        widget->setObjectName(QString::fromUtf8("widget"));
        widget->setGeometry(QRect(250, 40, 251, 361));
        textEdit = new QTextEdit(widget);
        textEdit->setObjectName(QString::fromUtf8("textEdit"));
        textEdit->setGeometry(QRect(-190, 0, 271, 121));
        pushButton = new QPushButton(widget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(0, 150, 75, 23));
        sample_2_4Class->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(sample_2_4Class);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1200, 23));
        menu = new QMenu(menuBar);
        menu->setObjectName(QString::fromUtf8("menu"));
        menu_2 = new QMenu(menuBar);
        menu_2->setObjectName(QString::fromUtf8("menu_2"));
        menu_3 = new QMenu(menuBar);
        menu_3->setObjectName(QString::fromUtf8("menu_3"));
        sample_2_4Class->setMenuBar(menuBar);
        mainToolBar = new QToolBar(sample_2_4Class);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        mainToolBar->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
        sample_2_4Class->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(sample_2_4Class);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        sample_2_4Class->setStatusBar(statusBar);

        menuBar->addAction(menu->menuAction());
        menuBar->addAction(menu_2->menuAction());
        menuBar->addAction(menu_3->menuAction());
        menu->addAction(actNew);
        menu->addAction(actOpen);
        menu->addAction(actExit);
        menu_2->addAction(actCut);
        menu_2->addAction(actCopy);
        menu_2->addAction(actPaste);
        menu_3->addAction(actItalic);
        menu_3->addAction(actBold);
        menu_3->addAction(actUnderline);
        mainToolBar->addAction(actNew);
        mainToolBar->addAction(actOpen);
        mainToolBar->addAction(actExit);
        mainToolBar->addAction(actCut);
        mainToolBar->addAction(actCopy);
        mainToolBar->addAction(actPaste);
        mainToolBar->addAction(actItalic);
        mainToolBar->addAction(actBold);
        mainToolBar->addAction(actUnderline);

        retranslateUi(sample_2_4Class);
        QObject::connect(actExit, SIGNAL(triggered()), sample_2_4Class, SLOT(close()));
        QObject::connect(actCut, SIGNAL(triggered()), textEdit, SLOT(cut()));
        QObject::connect(actCopy, SIGNAL(triggered()), textEdit, SLOT(copy()));
        QObject::connect(actPaste, SIGNAL(triggered()), textEdit, SLOT(paste()));

        QMetaObject::connectSlotsByName(sample_2_4Class);
    } // setupUi

    void retranslateUi(QMainWindow *sample_2_4Class)
    {
        sample_2_4Class->setWindowTitle(QApplication::translate("sample_2_4Class", "sample_2_4", nullptr));
        actNew->setText(QApplication::translate("sample_2_4Class", "\346\226\260\345\273\272", nullptr));
#ifndef QT_NO_TOOLTIP
        actNew->setToolTip(QApplication::translate("sample_2_4Class", "\346\226\260\345\273\272", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actNew->setShortcut(QApplication::translate("sample_2_4Class", "Ctrl+N", nullptr));
#endif // QT_NO_SHORTCUT
        actOpen->setText(QApplication::translate("sample_2_4Class", "\346\211\223\345\274\200", nullptr));
#ifndef QT_NO_TOOLTIP
        actOpen->setToolTip(QApplication::translate("sample_2_4Class", "\346\211\223\345\274\200\346\226\207\344\273\266", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actOpen->setShortcut(QApplication::translate("sample_2_4Class", "Ctrl+O", nullptr));
#endif // QT_NO_SHORTCUT
        actExit->setText(QApplication::translate("sample_2_4Class", "\351\200\200\345\207\272", nullptr));
#ifndef QT_NO_TOOLTIP
        actExit->setToolTip(QApplication::translate("sample_2_4Class", "\351\200\200\345\207\272\347\250\213\345\272\217", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actExit->setShortcut(QApplication::translate("sample_2_4Class", "Ctrl+E", nullptr));
#endif // QT_NO_SHORTCUT
        actCut->setText(QApplication::translate("sample_2_4Class", "\345\211\252\345\210\207", nullptr));
#ifndef QT_NO_TOOLTIP
        actCut->setToolTip(QApplication::translate("sample_2_4Class", "\345\211\252\345\210\207", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actCut->setShortcut(QApplication::translate("sample_2_4Class", "Ctrl+C", nullptr));
#endif // QT_NO_SHORTCUT
        actCopy->setText(QApplication::translate("sample_2_4Class", "\345\244\215\345\210\266", nullptr));
#ifndef QT_NO_TOOLTIP
        actCopy->setToolTip(QApplication::translate("sample_2_4Class", "\345\244\215\345\210\266", nullptr));
#endif // QT_NO_TOOLTIP
        actPaste->setText(QApplication::translate("sample_2_4Class", "\347\262\230\350\264\264", nullptr));
#ifndef QT_NO_TOOLTIP
        actPaste->setToolTip(QApplication::translate("sample_2_4Class", "\347\262\230\350\264\264", nullptr));
#endif // QT_NO_TOOLTIP
        actItalic->setText(QApplication::translate("sample_2_4Class", "\346\226\234\344\275\223", nullptr));
#ifndef QT_NO_TOOLTIP
        actItalic->setToolTip(QApplication::translate("sample_2_4Class", "\346\226\234\344\275\223", nullptr));
#endif // QT_NO_TOOLTIP
        actBold->setText(QApplication::translate("sample_2_4Class", "\347\262\227\344\275\223", nullptr));
#ifndef QT_NO_TOOLTIP
        actBold->setToolTip(QApplication::translate("sample_2_4Class", "\347\262\227\344\275\223", nullptr));
#endif // QT_NO_TOOLTIP
        actUnderline->setText(QApplication::translate("sample_2_4Class", "\344\270\213\345\210\222\347\272\277", nullptr));
#ifndef QT_NO_TOOLTIP
        actUnderline->setToolTip(QApplication::translate("sample_2_4Class", "\344\270\213\345\210\222\347\272\277", nullptr));
#endif // QT_NO_TOOLTIP
        pushButton->setText(QApplication::translate("sample_2_4Class", "PushButton", nullptr));
        menu->setTitle(QApplication::translate("sample_2_4Class", "\346\226\207\344\273\266", nullptr));
        menu_2->setTitle(QApplication::translate("sample_2_4Class", "\347\274\226\350\276\221", nullptr));
        menu_3->setTitle(QApplication::translate("sample_2_4Class", "\346\240\274\345\274\217", nullptr));
    } // retranslateUi

};

namespace Ui {
    class sample_2_4Class: public Ui_sample_2_4Class {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SAMPLE_2_4_H

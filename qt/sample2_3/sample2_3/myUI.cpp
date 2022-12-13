#include "myUI.h"
#include <QCoreApplication>

void myUI::setUI(QDialog* pMainWindow)
{
	if(pMainWindow->objectName().isEmpty())
		pMainWindow->setObjectName(QString::fromUtf8("mainWindow", -1));

	pVBoxLayout1 = new QVBoxLayout(pMainWindow);
	pVBoxLayout1->setSpacing(6);
	pVBoxLayout1->setContentsMargins(11, 11, 11, 11);
	pVBoxLayout1->setObjectName(QString::fromUtf8("verticalLayout"));

	groupFont = new QGroupBox(pMainWindow);
	groupFont->setObjectName(QString::fromUtf8("groupFont"));

	horizontalLayout = new QHBoxLayout(groupFont);
	horizontalLayout->setSpacing(6);
	horizontalLayout->setContentsMargins(11, 11, 11, 11);
	horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));

	checkBoxUnderline = new QCheckBox(groupFont);
	checkBoxUnderline->setObjectName(QString::fromUtf8("checkBoxUnderline"));
	horizontalLayout->addWidget(checkBoxUnderline,0,0);

	checkBoxItalic = new QCheckBox(groupFont);
	checkBoxItalic->setObjectName(QString::fromUtf8("checkBoxItalic"));
	horizontalLayout->addWidget(checkBoxItalic, 0, 0);

	checkBoxBold = new QCheckBox(groupFont);
	checkBoxBold->setObjectName(QString::fromUtf8("checkBoxBold"));
	horizontalLayout->addWidget(checkBoxBold, 0, 0);

	pVBoxLayout1->addWidget(groupFont);

	groupColor = new QGroupBox(pMainWindow);
	groupColor->setObjectName(QString::fromUtf8("groupColor"));

	horizontalLayout_2 = new QHBoxLayout(groupColor);
	horizontalLayout_2->setSpacing(6);
	horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout"));

	radioBtnBlue = new QRadioButton(groupColor);
	radioBtnBlue->setObjectName(QString::fromUtf8("radioBtnBlue"));
	horizontalLayout_2->addWidget(radioBtnBlue, 0, 0);

	radioBtnRed = new QRadioButton(groupColor);
	radioBtnRed->setObjectName(QString::fromUtf8("radioBtnRed"));
	horizontalLayout_2->addWidget(radioBtnRed, 0, 0);

	radioBtnBlack = new QRadioButton(groupColor);
	radioBtnBlack->setObjectName(QString::fromUtf8("radioBtnBlack"));
	horizontalLayout_2->addWidget(radioBtnBlack, 0, 0);

	pVBoxLayout1->addWidget(groupColor);

	textShower = new QPlainTextEdit(pMainWindow);
	textShower->setObjectName(QString::fromUtf8("textShower"));
	QFont  qfont;
	qfont.setPointSize(20);
	textShower->setFont(qfont);
	pVBoxLayout1->addWidget(textShower, 0, 0);

	aaa = new QHBoxLayout();
	aaa->setSpacing(6);
	aaa->setObjectName(QString::fromUtf8("aaa"));


	SpacerItem1 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	aaa->addItem(SpacerItem1);

	pushOK = new QPushButton(pMainWindow);
	pushOK->setObjectName(QString::fromUtf8("pushOK"));
	aaa->addWidget(pushOK);

	pushCencel = new QPushButton(pMainWindow);
	pushCencel->setObjectName(QString::fromUtf8("pushCencel"));
	aaa->addWidget(pushCencel);

	SpacerItem2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	aaa->addItem(SpacerItem2);

	pushExit = new QPushButton(pMainWindow);
	pushExit->setObjectName(QString::fromUtf8("pushExit"));
	aaa->addWidget(pushExit);

	SpacerItem3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	aaa->addItem(SpacerItem3);

	pVBoxLayout1->addLayout(aaa);
	reTranslateUI(pMainWindow);
	QObject::connect(pushExit, "2clicked()", pMainWindow, "1close()", Qt::ConnectionType::AutoConnection);
	QMetaObject::connectSlotsByName(pMainWindow);
}

void myUI::reTranslateUI(QDialog* pMainWindow)
{
	pMainWindow->setWindowTitle(QCoreApplication::translate("mainWindow", "sampl_2_2", 0, -1));
	
	groupFont->setTitle(QString(""));

	checkBoxUnderline->setText(QCoreApplication::translate("mainWindow", "Underline", 0, -1));
	checkBoxItalic->setText(QCoreApplication::translate("mainWindow", "Italic", 0, -1));
	checkBoxBold->setText(QCoreApplication::translate("mainWindow", "Bold", 0, -1));

	groupColor->setTitle(QString(""));

	radioBtnBlue->setText(QCoreApplication::translate("mainWindow", "blue", 0, -1));
	radioBtnRed->setText(QCoreApplication::translate("mainWindow", "red", 0, -1));
	radioBtnBlack->setText(QCoreApplication::translate("mainWindow", "black", 0, -1));


	textShower->setPlainText(QCoreApplication::translate("mainWindow", "this is a demo Text", 0, -1));
	
	pushOK->setText(QCoreApplication::translate("mainWindow", QString::fromLocal8Bit("确定").toUtf8(), 0, -1));
	pushCencel->setText(QCoreApplication::translate("mainWindow", QString::fromLocal8Bit("取消").toUtf8(), 0, -1));
	pushExit->setText(QCoreApplication::translate("mainWindow", QString::fromLocal8Bit("退出").toUtf8(), 0, -1));


}

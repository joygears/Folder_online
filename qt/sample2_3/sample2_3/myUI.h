#pragma once
#include <qdialog.h>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QCheckBox>
#include <QRadioButton>
#include <QPlainTextEdit>
#include <QPushButton>

class myUI
{
public:
	void setUI(QDialog* sample2_3Class);
	void reTranslateUI(QDialog* sample2_3Class);
private:
	QVBoxLayout *pVBoxLayout1;
	QGroupBox* groupFont;
	QHBoxLayout* horizontalLayout;
	QCheckBox* checkBoxUnderline;
	QCheckBox* checkBoxItalic;
	QCheckBox* checkBoxBold;
	QGroupBox* groupColor;
	QHBoxLayout* horizontalLayout_2;
	QRadioButton* radioBtnBlue;
	QRadioButton* radioBtnRed;
	QRadioButton* radioBtnBlack;
	QPlainTextEdit* textShower;
	QHBoxLayout* aaa;
	QSpacerItem* SpacerItem1;
	QSpacerItem* SpacerItem2;
	QSpacerItem* SpacerItem3;
	QPushButton* pushOK;
	QPushButton* pushCencel;
	QPushButton* pushExit;
};


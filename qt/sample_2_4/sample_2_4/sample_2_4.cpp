#include "sample_2_4.h"
#include <qdebug.h>
void sample_2_4::init()
{
    label = new QLabel;
    label->setText(QString::fromLocal8Bit("当前文件:"));
    label->setMinimumWidth(150);
    ui.statusBar->addWidget(label);

    this->processBar = new QProgressBar;
    processBar->setMinimum(5);
    processBar->setMaximum(50);
    processBar->setValue(ui.textEdit->font().pointSize());
    ui.statusBar->addWidget(processBar);

    spinFontSize = new QSpinBox;
    spinFontSize->setMinimum(5);
    spinFontSize->setMaximum(50);
    ui.mainToolBar->addWidget(new QLabel(QString::fromLocal8Bit("字体大小:")));
    ui.mainToolBar->addWidget(spinFontSize);

    fontComboBox =new  QFontComboBox;
    ui.mainToolBar->addWidget(new QLabel(QString::fromLocal8Bit("字体:")));
    ui.mainToolBar->addWidget(fontComboBox);
}

void sample_2_4::on_actItalic_triggered(bool checked)
{
    QTextCharFormat fmt;
    fmt.setFontItalic(checked);
    ui.textEdit->mergeCurrentCharFormat(fmt);
}

void sample_2_4::on_actUnderline_triggered(bool checked)
{
    QTextCharFormat fmt;
    fmt.setFontUnderline(checked);
    ui.textEdit->mergeCurrentCharFormat(fmt);
}

sample_2_4::sample_2_4(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);
    init();
    this->setCentralWidget(ui.textEdit);
}

void sample_2_4::on_actBold_triggered(bool checked) {

   /* QFont font  = ui.textEdit->font();
    font.setWeight(checked ? 75 : 55);
    ui.textEdit->setFont(font);*/
    QTextCharFormat fmt;
    fmt.setFontWeight(checked ? QFont::Bold : QFont::Normal);
    ui.textEdit->mergeCurrentCharFormat(fmt);
}

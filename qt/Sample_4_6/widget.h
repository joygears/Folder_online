#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
private slots:
    void on_btnInitList_clicked();
    void on_btnClearCombo_clicked();
    void on_btnMap_clicked();
    void on_checkEditable_stateChanged(int state);
private:
    Ui::Widget *ui;
};
#endif // WIDGET_H

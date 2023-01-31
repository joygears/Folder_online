#ifndef TASKTABLE_H
#define TASKTABLE_H

#include <QTableWidget>

class QTimer;
class QLabel;
class QMenu;
class QProgressBar;
class QToolButton;
class QPushButton;
class QStackedWidget;

class AbstractDownloadTask;
class ElidedTextLabel;
class TaskCellWidget;

class TaskTableWidget : public QTableWidget
{
    Q_OBJECT

public:
    explicit TaskTableWidget(QWidget *parent = nullptr);
    void save();
    void load();
    void addTasks(const QList<AbstractDownloadTask*>&, bool activate = true);



    void stopAll();
    void startAll();
    void removeAll();
   
private:
    QAction* startAllAct;
    QAction* stopAllAct;
    QAction* removeAllAct;
    bool dirty = false;
    QTimer* saveTasksTimer;
    void setDirty();

};
class TaskCellWidget : public QWidget
{
    Q_OBJECT
public:
    enum State { Stopped, Waiting, Downloading, Finished };
    State state = Stopped;
private:
    
    AbstractDownloadTask* task = nullptr;
public:
    TaskCellWidget(AbstractDownloadTask* task, QWidget* parent = nullptr);
    
    
    static int cellHeight();



private:
    QPushButton* iconButton;
    ElidedTextLabel* titleLabel;
    QLabel* qnDescLabel;
    QLabel* progressLabel;

    QProgressBar* progressBar;

    QLabel* downRateLabel;
    QLabel* timeLeftLabel;
    ElidedTextLabel* statusTextLabel;
    QWidget* downloadStatsWidget;
    QStackedWidget* statusStackedWidget;

    QPushButton* startStopButton;
    QPushButton* removeButton;

    QTimer* downRateTimer;
    QList<qint64> downRateWindow;


    void updateStartStopBtn();

};


#endif // TASKTABLE_H

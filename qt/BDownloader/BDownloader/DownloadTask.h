#ifndef DOWNLOADTASK_H
#define DOWNLOADTASK_H

#include <QObject>
#include <memory>
#include <QFile>
#include <QSaveFile>
//#include <utility>

class QNetworkReply;
class QFile;

using QnList = QList<int>;

struct QnInfo {
    QnList qnList;
    int currentQn;
};

class AbstractDownloadTask: public QObject
{
    Q_OBJECT

public:
   
    QString path;
    /**
     * @return a new AbstractDownloadTask object constructed from json. returns nullptr if invalid
     */
    static AbstractDownloadTask *fromJsonObj(const QJsonObject &json);
protected:
    AbstractDownloadTask(const QString& path) : path(path) {}
public :
    virtual QString getTitle() const;
};

class AbstractVideoDownloadTask : public AbstractDownloadTask
{
    Q_OBJECT

protected:
    int qn = 0; // quality (1080P, 720P, ...)
    qint64 downloadedBytesCnt = 0; // bytes downloaded, or total bytes if finished


    AbstractVideoDownloadTask(const QString& path, int qn)
        : AbstractDownloadTask(path), qn(qn) {}

};

class VideoDownloadTask : public AbstractVideoDownloadTask
{
    Q_OBJECT

        qint64 totalBytesCnt = 0;

protected:
    VideoDownloadTask(const QJsonObject& json);
    using AbstractVideoDownloadTask::AbstractVideoDownloadTask; // ctor
};

class PgcDownloadTask : public VideoDownloadTask
{
    Q_OBJECT

public:
    const qint64 ssId;
    const qint64 epId;
    PgcDownloadTask(qint64 ssId, qint64 epId, int qn, const QString& path)
        : VideoDownloadTask(path, qn), ssId(ssId), epId(epId) {}
    PgcDownloadTask(const QJsonObject& json);
};

class PugvDownloadTask : public VideoDownloadTask
{
    Q_OBJECT

public:
    const qint64 ssId;
    const qint64 epId;

    PugvDownloadTask(qint64 ssId, qint64 epId, int qn, const QString& path)
        : VideoDownloadTask(path, qn), ssId(ssId), epId(epId) {}

    PugvDownloadTask(const QJsonObject& json);

    
};

class UgcDownloadTask : public VideoDownloadTask
{
    Q_OBJECT

public:
    const qint64 aid;
    const qint64 cid;

    UgcDownloadTask(qint64 aid, qint64 cid, int qn, const QString& path)
        : VideoDownloadTask(path, qn), aid(aid), cid(cid) {}

    UgcDownloadTask(const QJsonObject& json);

};


class QSaveFile;
class ComicDownloadTask : public AbstractDownloadTask
{
    Q_OBJECT
private:
    int totalImgCnt = 0;
    int finishedImgCnt = 0;
    int curImgRecvBytesCnt = 0;
    int curImgTotalBytesCnt = 0;
    qint64 bytesCntTillLastImg = 0;



public:
    const qint64 comicId;
    const qint64 epId;
    ComicDownloadTask(qint64 comicId, qint64 epId, const QString& path)
        : AbstractDownloadTask(path), comicId(comicId), epId(epId) {}

    ComicDownloadTask(const QJsonObject& json);

    
};
#endif 
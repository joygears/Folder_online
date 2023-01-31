// Created by voidzero <vooidzero.github@qq.com>

#include "DownloadTask.h"
#include "Network.h"
#include "utils.h"
#include <QtNetwork>
#include "Extractor.h"






AbstractDownloadTask* AbstractDownloadTask::fromJsonObj(const QJsonObject& json)
{
    int type = json["type"].toInt(-1);
    switch (type) {
        case static_cast<int>(ContentType::PGC) :
            return new PgcDownloadTask(json);
            case static_cast<int>(ContentType::PUGV) :
                return new PugvDownloadTask(json);
                case static_cast<int>(ContentType::UGC) :
                    return new UgcDownloadTask(json);
                    case static_cast<int>(ContentType::Comic) :
                        return new ComicDownloadTask(json);
    }
    return nullptr;
}
QString AbstractDownloadTask::getTitle() const
{
    return QFileInfo(path).baseName();
}



VideoDownloadTask::VideoDownloadTask(const QJsonObject& json)
    : AbstractVideoDownloadTask(json["path"].toString(), json["qn"].toInt())
{
    downloadedBytesCnt = json["bytes"].toInt(0);
    totalBytesCnt = json["total"].toInt(0);
}

PgcDownloadTask::PgcDownloadTask(const QJsonObject& json)
    : VideoDownloadTask(json),
    ssId(json["ssid"].toInt()),
    epId(json["epid"].toInt())
{
}
PugvDownloadTask::PugvDownloadTask(const QJsonObject& json)
    : VideoDownloadTask(json),
    ssId(json["ssid"].toInt()),
    epId(json["epid"].toInt())
{
}

UgcDownloadTask::UgcDownloadTask(const QJsonObject& json)
    : VideoDownloadTask(json),
    aid(json["aid"].toInt()),
    cid(json["cid"].toInt())
{
}

ComicDownloadTask::ComicDownloadTask(const QJsonObject& json)
    : AbstractDownloadTask(json["path"].toString()),
    comicId(json["id"].toInt()),
    epId(json["epid"].toInt()),
    totalImgCnt(json["total"].toInt(0)),
    finishedImgCnt(json["imgs"].toInt(0)),
    bytesCntTillLastImg(json["bytes"].toInt(0))
{
}

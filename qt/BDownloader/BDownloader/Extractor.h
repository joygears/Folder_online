#ifndef EXTRACTOR_H
#define EXTRACTOR_H

#include <QObject>
#include <utility>

class QNetworkReply;

namespace ContentItemFlag
{
constexpr int NoFlags = 0;
constexpr int Disabled = 1;
constexpr int VipOnly = 2;
constexpr int PayOnly = 4;
constexpr int AllowWaitFree = 8; // manga

}

// UGC (User Generated Content): 普通视频
// PGC (Professional Generated Content): 剧集（番剧、电影、纪录片等）
// PUGV (Professional User Generated Video): 课程
enum class ContentType { UGC = 1, PGC, PUGV, Live, Comic };



#endif // EXTRACTOR_H

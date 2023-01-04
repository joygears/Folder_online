#include "config.h"
#include <QCoreApplication>
#include <QSettings>
#include <QDir>
#include <QStandardPaths>


QString createAppPath() {
	QDir dir(QStandardPaths::writableLocation(QStandardPaths::GenericDataLocation));
	dir.mkdir("iTubeGo");
	return dir.filePath("iTubeGo");
}
QString createLogPath() {

	QString appPath = createAppPath();
	appPath += "/Log";
	QDir dir;
	return dir.mkpath(appPath);
}


void preConfig() {
	QCoreApplication::setOrganizationName("iTubeGo");
	QCoreApplication::setOrganizationDomain("luckydogsoft.com");
	QCoreApplication::setApplicationName("iTubeGo");
	QSettings setting(0);
	if (setting.value("kDownload_MaxTask").isNull()) {
		setting.setValue("kDownload_MaxTask", QVariant(2));
	}
	setting.setValue("kDownload_MaxTask_Default", QVariant(2));
	if (setting.value("kConvert_MaxTask").isNull()) {
		setting.setValue("kConvert_MaxTask", QVariant(2));
	}
	setting.setValue("kConvert_MaxTask_Default", QVariant(2));

	if (setting.value("kDownload_MediaType").isNull()) {
		setting.setValue("kDownload_MediaType", QVariant("video"));
	}
	setting.setValue("kDownload_MediaType_Default", QVariant("video"));

	if (setting.value("kDownload_VideoQuality").isNull()) {
		setting.setValue("kDownload_VideoQuality", QVariant("1080P"));
	}
	setting.setValue("kDownload_VideoQuality_Default", QVariant("1080P"));

	if (setting.value("kDownload_AudioQuality").isNull()) {
		setting.setValue("kDownload_AudioQuality", QVariant("320Kb/s"));
	}
	setting.setValue("kDownload_AudioQuality_Default", QVariant("320Kb/s"));

	if (setting.value("kDownload_Subtitle").isNull()) {
		setting.setValue("kDownload_Subtitle", QVariant("English"));
	}
	setting.setValue("kDownload_Subtitle_Default", QVariant("English"));

	if (setting.value("kDownload_AutoDownSubtitle").isNull()) {
		setting.setValue("kDownload_AutoDownSubtitle", QVariant(1));
	}
	setting.setValue("kDownload_AutoDownSubtitle_Default", QVariant(1));

	if (setting.value("kDownload_ResumeOnStartup").isNull()) {
		setting.setValue("kDownload_ResumeOnStartup", QVariant(0));
	}
	setting.setValue("kDownload_ResumeOnStartup_Default", QVariant(0));

	if (setting.value("kDownload_ReadCookie").isNull()) {
		setting.setValue("kDownload_ReadCookie", QVariant(0));
	}
	setting.setValue("kDownload_ReadCookie_Default", QVariant(0));


	if (setting.value("kDownloadPlaylist_OrderNumber").isNull()) {
		setting.setValue("kDownloadPlaylist_OrderNumber", QVariant(1));
	}
	setting.setValue("kDownloadPlaylist_OrderNumber_Default", QVariant(1));


	if (setting.value("kPlaylist_MediaType").isNull()) {
		setting.setValue("kPlaylist_MediaType", QVariant("video"));
	}
	setting.setValue("kPlaylist_MediaType_Default", QVariant("video"));


	if (setting.value("kPlaylist_VideoQuality").isNull()) {
		setting.setValue("kPlaylist_VideoQuality", QVariant("1080P"));
	}
	setting.setValue("kPlaylist_VideoQuality_Default", QVariant("1080P"));

	if (setting.value("kPlaylist_AudioQuality").isNull()) {
		setting.setValue("kPlaylist_AudioQuality", QVariant("Best"));
	}
	setting.setValue("kPlaylist_AudioQuality_Default", QVariant("Best"));

	if (setting.value("kPlaylist_OrderMode").isNull()) {
		setting.setValue("kPlaylist_OrderMode", QVariant("Newest first"));
	}
	setting.setValue("kPlaylist_OrderMode_Default", QVariant("Newest first"));

	if (setting.value("kPlaylist_SkipDownloaded").isNull()) {
		setting.setValue("kPlaylist_SkipDownloaded", QVariant(0));
	}
	setting.setValue("kPlaylist_SkipDownloaded_Default", QVariant(0));

	QString kLocation_DownloadDir = QDir::cleanPath(QDir::homePath() + QDir::separator() + "Videos/iTubeGo/Download");

	if (setting.value("kLocation_DownloadDir").isNull()) {
		setting.setValue("kLocation_DownloadDir", QVariant(kLocation_DownloadDir));
	}
	setting.setValue("kLocation_DownloadDir_Default", QVariant(kLocation_DownloadDir));

	QString kLocation_ConvertDir = QDir::cleanPath(QDir::homePath() + QDir::separator() + "Videos/iTubeGo/Converted");

	if (setting.value("kLocation_ConvertDir").isNull()) {
		setting.setValue("kLocation_ConvertDir", QVariant(kLocation_ConvertDir));
	}
	setting.setValue("kLocation_ConvertDir_Default", QVariant(kLocation_ConvertDir));

	if (setting.value("kProxy_Setting_Enable").isNull()) {
		setting.setValue("kProxy_Setting_Enable", QVariant(0));
	}
	setting.setValue("kProxy_Setting_Enable_Default", QVariant(0));

	if (setting.value("kProxy_Setting_Authorization").isNull()) {
		setting.setValue("kProxy_Setting_Authorization", QVariant(0));
	}
	setting.setValue("kProxy_Setting_Authorization_Default", QVariant(0));

	if (setting.value("kSpeedLimitedManual").isNull()) {
		setting.setValue("kSpeedLimitedManual", QVariant("Unlimited"));
	}
	setting.setValue("kSpeedLimitedManual_Default", QVariant("Unlimited"));

	if (setting.value("kSpeedLimited").isNull()) {
		setting.setValue("kSpeedLimited", QVariant("512 KBps"));
	}
	setting.setValue("kSpeedLimited_Default", QVariant("512 KBps"));


	if (setting.value("kOneClickedDownloadMode").isNull()) {
		setting.setValue("kOneClickedDownloadMode", QVariant("MP4"));
	}
	setting.setValue("kOneClickedDownloadMode_Default", QVariant("MP4"));

	if (setting.value("kConvert_MediaType").isNull()) {
		setting.setValue("kConvert_MediaType", QVariant("Video"));
	}
	setting.setValue("kConvert_MediaType_Default", QVariant("Video"));

	if (setting.value("kConvert_VideoType").isNull()) {
		setting.setValue("kConvert_VideoType", QVariant("MP4"));
	}
	setting.setValue("kConvert_VideoType_Default", QVariant("MP4"));

	if (setting.value("kConvert_VideoResoulution").isNull()) {
		setting.setValue("kConvert_VideoResoulution", QVariant("Origin"));
	}
	setting.setValue("kConvert_VideoResoulution_Default", QVariant("Origin"));

	if (setting.value("kConvert_VideoIsMute").isNull()) {
		setting.setValue("kConvert_VideoIsMute", QVariant(0));
	}
	setting.setValue("kConvert_VideoIsMute_Default", QVariant(0));


	if (setting.value("kConvert_AudioType").isNull()) {
		setting.setValue("kConvert_AudioType", QVariant("MP3"));
	}
	setting.setValue("kConvert_AudioType_Default", QVariant("MP3"));

	if (setting.value("kConvert_AudioBitRate").isNull()) {
		setting.setValue("kConvert_AudioBitRate", QVariant("Origin"));
	}
	setting.setValue("kConvert_AudioBitRate_Default", QVariant("Origin"));




}
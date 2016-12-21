/******************************************************************************
*
*    Author: Mikhail Gusev, gusevmihs@gmail.com
*    Copyright (C) 2014-2016 NextGIS, info@nextgis.com
*
*    This file is part of the Qt Installer Framework modified for NextGIS
*    Installer project.
*
*    GNU Lesser General Public License Usage
*    This file may be used under the terms of the GNU Lesser
*    General Public License version 2.1 or version 3 as published by the Free
*    Software Foundation and appearing in the file LICENSE.LGPLv21 and
*    LICENSE.LGPLv3 included in the packaging of this file. Please review the
*    following information to ensure the GNU Lesser General Public License
*    requirements will be met: https://www.gnu.org/licenses/lgpl.html and
*    http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
*
*****************************************************************************/

#ifndef NG_ACCESS_H
#define NG_ACCESS_H

#include "simplecrypt.h"

#include <QString>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkReply>

#define NG_URL_FORGOT "https://my.nextgis.com/password/reset/"
#define NG_URL_REGISTER "https://my.nextgis.com/signup/"
//#define NG_URL_LOGIN "https://my.nextgis.com/login/"
#define NG_URL_LOGIN "https://my.nextgis.com/api/v1/simple_auth/"
#define NG_COOKIE_CSRF "ngid_csrftoken"
#define NG_SETTINGS_LOGIN "login"
#define NG_SETTINGS_PASSWORD "password"


class NgAccess: public QObject
{
    Q_OBJECT

    public:

     static QNetworkAccessManager manager;
     static bool authenticated;
     static QString _error;
     static QString _received;

    signals:

     void authFinished ();

    public:

     NgAccess ();
     ~NgAccess ();

     void startAuthetication (QString login, QString password);
     void readAuthData ();
     void writeAuthData ();
     QString getCurLogin () { return m_curLogin; }
     QString getCurPassword () { return m_curPassword; }

    private slots:

     void onReplyReadyRead ();
     void onReply2ReadyRead ();
     void onReplyFinished ();
     void onReply2Finished ();

    private:

     void _readReply (QNetworkReply *reply);

    private:

     SimpleCrypt crypto;
     QString m_curLogin;
     QString m_curPassword;

     QByteArray m_baReceived;
     QNetworkReply *m_netReply;
     QNetworkReply *m_netReply2;
};

#endif //NG_ACCESS_H





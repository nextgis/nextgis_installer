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

#include <iostream>

#include "ngaccess.h"

#include <QUrl>
#include <QNetworkCookie>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSettings>


// Global network manager for storing retrived from the server authentication
// cookies.
// Used as global variable all over the installer.
QNetworkAccessManager NgAccess::manager;

// Global variable to see if there was a successfull authentication e.g. in different
// installer GUI pages.
bool NgAccess::authenticated = false;

// Global error output for debugging.
QString NgAccess::_error;
QString NgAccess::_received;


NgAccess::NgAccess ():
    QObject()
{
    crypto.setKey(Q_UINT64_C(0x0c2ad4a4acb9f023)); // TEMP
}

NgAccess::~NgAccess ()
{
}


void NgAccess::readAuthData ()
{
    // TODO: maybe use QSettings::NativeFormat.
    QSettings settings(QSettings::IniFormat, QSettings::UserScope,
                       QString::fromUtf8("NextGIS"),
                       QString::fromUtf8("Common"));
    QString loginReaded = settings.value(QString::fromUtf8(NG_SETTINGS_LOGIN),
                                QString::fromUtf8("")).toString();
    QString passReaded = settings.value(QString::fromUtf8(NG_SETTINGS_PASSWORD),
                                QString::fromUtf8("")).toString();
    m_curLogin = crypto.decryptToString(loginReaded);
    m_curPassword = crypto.decryptToString(passReaded);
}

void NgAccess::writeAuthData ()
{
    // TODO: maybe use QSettings::NativeFormat.
    QString loginToSave = crypto.encryptToString(
                QString::fromUtf8(m_curLogin.toUtf8().data()));
    QString passToSave = crypto.encryptToString(
                QString::fromUtf8(m_curPassword.toUtf8().data()));
    QSettings settings(QSettings::IniFormat, QSettings::UserScope,
                       QString::fromUtf8("NextGIS"),
                       QString::fromUtf8("Common"));
    settings.setValue(QString::fromUtf8(NG_SETTINGS_LOGIN),loginToSave);
    settings.setValue(QString::fromUtf8(NG_SETTINGS_PASSWORD),passToSave);
}


void NgAccess::startAuthetication(QString login, QString password)
{
    std::cout << "[NGAuth] Sending request for cookies";

    _error = QString::fromUtf8("");
    _received = QString::fromUtf8("");

    m_curLogin = login;
    m_curPassword = password;

    m_baReceived.clear();
    QUrl url;
    url.setUrl(QString::fromUtf8(NG_URL_LOGIN));
    QNetworkRequest request(url);
    m_netReply = NgAccess::manager.get(request);
    QObject::connect(m_netReply, SIGNAL(finished()),
                     this, SLOT(onReplyFinished()));
    QObject::connect(m_netReply, SIGNAL(readyRead()),
                     this, SLOT(onReplyReadyRead()));
}


void NgAccess::onReplyReadyRead ()
{
    this->_readReply(m_netReply);
}

void NgAccess::onReply2ReadyRead ()
{
    this->_readReply(m_netReply2);
}


void NgAccess::onReplyFinished ()
{
    if (m_netReply->error() != QNetworkReply::NoError)
    {
        _error = QString::fromUtf8(m_netReply->errorString().toUtf8().data());
        _received = QString::fromUtf8(m_baReceived);

        m_netReply->deleteLater();
        NgAccess::authenticated = false;
        emit authFinished();
        return;
    }

    // Get cookie for csrftoken.
    QVariant va = m_netReply->header(QNetworkRequest::SetCookieHeader);
    QString strCsrf = QString::fromUtf8("");
    if (va.isValid())
    {
        QList<QNetworkCookie> cookies = va.value<QList<QNetworkCookie> >();
        foreach (QNetworkCookie cookie, cookies)
        {
            if (QString::fromUtf8(cookie.name())
                    == QString::fromUtf8(NG_COOKIE_CSRF))
            {
                strCsrf = QString::fromUtf8(cookie.value());
                break;
            }
        }
    }
    if (strCsrf == QString::fromUtf8(""))
    {
        _error = QString::fromUtf8(m_netReply->errorString().toUtf8().data());
        _received = QString::fromUtf8(m_baReceived);

        m_netReply->deleteLater();
        NgAccess::authenticated = false;
        emit authFinished();
        return;
    }

    std::cout << "[NGAuth] Sending auth request";

    // Make second (final) POST request if first GET one was successful.
    m_baReceived.clear();
    QUrl url;
    url.setUrl(QString::fromUtf8(NG_URL_LOGIN));
    QNetworkRequest request(url);
    QByteArray ba = QString::fromUtf8("username=").toUtf8()
            + QUrl::toPercentEncoding(m_curLogin) // to correctly replace e.g. '+' char
            + QString::fromUtf8("&password=").toUtf8()
            + QUrl::toPercentEncoding(m_curPassword)
            + QString::fromUtf8("&csrfmiddlewaretoken=").toUtf8()
            + strCsrf.toUtf8();
    request.setHeader(QNetworkRequest::ContentTypeHeader,
            QVariant(QString::fromUtf8("application/x-www-form-urlencoded")));
    request.setRawHeader(QString::fromUtf8("Referer").toUtf8(),
                         QString::fromUtf8(NG_URL_LOGIN).toUtf8());
    m_netReply2 = NgAccess::manager.post(request, ba);
    QObject::connect(m_netReply2, SIGNAL(finished()),
                     this, SLOT(onReply2Finished()));
    QObject::connect(m_netReply2, SIGNAL(readyRead()),
                     this, SLOT(onReply2ReadyRead()));

    m_netReply->deleteLater();
}


void NgAccess::onReply2Finished ()
{
    if (m_netReply2->error() != QNetworkReply::NoError)
    {
        _error = QString::fromUtf8(m_netReply2->errorString().toUtf8().data());
        _received = QString::fromUtf8(m_baReceived);

        m_netReply2->deleteLater();
        NgAccess::authenticated = false;
        emit authFinished();
        return;
    }

    // Parse reply for authentication errors.
    QJsonDocument jDoc = QJsonDocument::fromJson(m_baReceived);
    if (jDoc.isNull())
    {
        _error = QString::fromUtf8(m_netReply2->errorString().toUtf8().data());
        _received = QString::fromUtf8(m_baReceived);

        m_netReply2->deleteLater();
        NgAccess::authenticated = false;
        emit authFinished();
        return;
    }
    QJsonObject jObj = jDoc.object();
    QString strObj = jObj.value(QString::fromUtf8("status")).toString();
    if (strObj != QString::fromUtf8("success"))
    {
        _error = QString::fromUtf8(m_netReply2->errorString().toUtf8().data());
        _received = QString::fromUtf8(m_baReceived);

        m_netReply2->deleteLater();
        NgAccess::authenticated = false;
        emit authFinished();
        return;
    }

    std::cout << "[NGAuth] Authentication successful";

    m_netReply2->deleteLater();
    NgAccess::authenticated = true;
    emit authFinished();
}


void NgAccess::_readReply (QNetworkReply *reply)
{
    QByteArray ba;
    ba = reply->readAll();
    m_baReceived += ba;
}




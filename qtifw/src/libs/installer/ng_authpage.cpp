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

#include "ng_authpage.h"

#include <QVBoxLayout>
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>


using namespace QInstaller;


NextgisAuthPage::NextgisAuthPage (PackageManagerCore *core)
    : PackageManagerPage (core)
{
    m_isInstaller = core->isInstaller();

    //setPixmap(QWizard::WatermarkPixmap, QPixmap());
    setObjectName(QLatin1String("NextgisAuthPage"));
    setColoredTitle(tr("NextGIS authentication"));
    setColoredSubTitle(tr("Enter your NextGIS credentials"));

    m_labLogin = new QLabel(this);
    m_labLogin->setText(tr("Login or E-mail: "));

    m_labPassword = new QLabel(this);
    m_labPassword->setText(tr("Password: "));

    m_eLogin = new QLineEdit(this);

    m_ePassword = new QLineEdit(this);
    m_ePassword->setEchoMode(QLineEdit::Password);

    m_labInfo = new QLabel(this);
    m_labInfo->setText(tr(""));

    _test_textEdit = new QTextEdit(this);

    m_labForgot = new QLabel(this);
    m_labForgot->setText(QLatin1String("<a href=\"")
                         + QLatin1String(NG_URL_FORGOT)
                         + QLatin1String("\">")
                         + tr("Forgot password?")
                         + QLatin1String("</a>"));
    m_labForgot->setOpenExternalLinks(true);

    m_labGet = new QLabel(this);
    m_labGet->setText(QLatin1String("<a href=\"")
                      + QLatin1String(NG_URL_REGISTER)
                      + QLatin1String("\">")
                      + tr("Register now")
                      + QLatin1String("</a>"));
    m_labGet->setOpenExternalLinks(true);

    QFormLayout *lfAuth = new QFormLayout();
    lfAuth->addRow(m_labLogin, m_eLogin);
    lfAuth->addRow(m_labPassword, m_ePassword);

    QVBoxLayout *lvAll = new QVBoxLayout();
    lvAll->addLayout(lfAuth);
    lvAll->addWidget(m_labForgot);
    lvAll->addWidget(m_labGet);
    lvAll->addStretch();
    lvAll->addWidget(m_labInfo);
    lvAll->addWidget(_test_textEdit);

    QHBoxLayout *lhMain = new QHBoxLayout(this);
    lhMain->addStretch();
    lhMain->addLayout(lvAll);
    lhMain->addStretch();

    _test_textEdit->hide();

    m_ngAccessPtr = new NgAccess();

    // If this is not an installer:
    // Load last entered login and password.
    if (!m_isInstaller)
    {
        m_ngAccessPtr->readAuthData();
        m_eLogin->setText(m_ngAccessPtr->getCurLogin());
        m_ePassword->setText(m_ngAccessPtr->getCurPassword());
    }
}

NextgisAuthPage::~NextgisAuthPage ()
{
    delete m_ngAccessPtr;
}


bool NextgisAuthPage::validatePage ()
{
    m_labInfo->setText(tr("Connecting ..."));

    this->gui()->button(QWizard::NextButton)->setEnabled(false);

    // Wait for the end of the NextGIS authentication.
    QEventLoop eventLoop;
    connect(m_ngAccessPtr, SIGNAL(authFinished()), &eventLoop, SLOT(quit()));
    QString login = QString::fromUtf8(m_eLogin->text().toUtf8());
    QString password = QString::fromUtf8(m_ePassword->text().toUtf8());
    m_ngAccessPtr->startAuthetication(login, password);
    eventLoop.exec();

    this->gui()->button(QWizard::NextButton)->setEnabled(true);

    _test_textEdit->setText(NgAccess::_received);
    //m_labInfo->setText(NgAccess::_error);

    if (!NgAccess::authenticated)
    {
        if (NgAccess::_received == QString::fromUtf8("{\"status\": \"invalid login\"}"))
            m_labInfo->setText(tr("Invalid login or password"));
        else
            m_labInfo->setText(tr("Error connecting to server"));

        // If this is not an installer:
        // Always allow to switch to the next page so user could perform an
        // unistallation of the programs. The according update and add/remove
        // radio buttons will be disabled - see Introduction Page class for that.
        if (!m_isInstaller)
            return true;

        return false;
    }

    m_labInfo->setText(tr("Authorization successful."
                          "\nClick Next to continue installation"));
    m_ngAccessPtr->writeAuthData();
    return true;
}


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

#ifndef NG_AUTHPAGE_H
#define NG_AUTHPAGE_H

#include "packagemanagergui.h"
#include "ngaccess.h"

#include <QTextEdit>


namespace QInstaller
{

class INSTALLER_EXPORT NextgisAuthPage : public PackageManagerPage
{
    Q_OBJECT

    public:
     explicit NextgisAuthPage (PackageManagerCore *core);
     virtual ~NextgisAuthPage ();

//     bool isComplete () const;

     bool validatePage ();

//     void startInitialAuth ();

//    protected:
//     void leaving ();

    private slots:
//     void onAuthClicked ();
//     void onAuthFailed ();
//     void onAuthCompleted ();
//     void onAuthMaintainerFailed ();

    private:
     QLabel *m_labLogin;
     QLineEdit *m_eLogin;
     QLabel *m_labPassword;
     QLineEdit *m_ePassword;
//     QPushButton *m_bpAuth;
     QLabel *m_labInfo;
     QLabel *m_labForgot;
     QLabel *m_labGet;
     QTextEdit *_test_textEdit;

     NgAccess *m_ngAccessPtr;

//     bool m_isAuthorized;

     bool m_isInstaller;
};

}

#endif  // NG_AUTHPAGE_H

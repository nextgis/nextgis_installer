/******************************************************************************
*
*    Author: Mikhail Gusev, gusevmihs@gmail.com
*    Copyright (C) 2014-2017 NextGIS, info@nextgis.com
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
#include "ng_userpathwinenvironmentvariablesoperation.h"

#include <QSettings>

#ifdef Q_OS_WIN
# include <windows.h>
#endif

using namespace QInstaller;

#define NG_REGISTRY_USER_PATH "HKEY_CURRENT_USER\\Environment"


// Read old variable value from the Windows registry.
// Note: we do not need admin rights to do this because it's a user variable (not system).
// Returns "" if Path variable does not exist.
static QString readPath ()
{
    return QSettings(QLatin1String(NG_REGISTRY_USER_PATH),
                     QSettings::NativeFormat).value(QLatin1String("Path"),
                                                    QLatin1String("")).toString();
}

// Write back new variable value to the Windows registry.
// Note: we do not need admin rights to do this because it's a user variable (not system).
static void rewritePath (QString value)
{
    QSettings(QLatin1String(NG_REGISTRY_USER_PATH),
              QSettings::NativeFormat).setValue(QLatin1String("Path"), value);
}

// Note: This function is copied from EnvironmentVariableOperation.
#ifdef Q_OS_WIN
static void broadcastEnvironmentChange()
{
    // Use SendMessageTimeout to Broadcast a message to the whole system to update settings of all
    // running applications. This is needed to activate the changes done above without logout+login.
    DWORD_PTR aResult = 0;
    LRESULT sendresult = SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE,
        0, (LPARAM) L"Environment", SMTO_BLOCK | SMTO_ABORTIFHUNG, 5000, &aResult);
    if (sendresult == 0 || aResult != 0)
        qWarning("Failed to broadcast the WM_SETTINGCHANGE message.");
}
#endif


NgUserPathWinEnvironmentVariableOperation::NgUserPathWinEnvironmentVariableOperation (PackageManagerCore* core)
    : UpdateOperation(core)
{
    setName(QLatin1String("NgUserPathWinEnvironmentVariable"));
}


void NgUserPathWinEnvironmentVariableOperation::backup ()
{
}


bool NgUserPathWinEnvironmentVariableOperation::performOperation ()
{
    if (!checkArgumentCount(1))
        return false;

    const QStringList args = arguments();
    const QString value = args.at(0);

    QString curValue = readPath();
    if (curValue == QLatin1String(""))
        curValue = value;
    else
        curValue += QLatin1String(";") + value;
    rewritePath(curValue);

    broadcastEnvironmentChange(); // otherwise no changes in system right away

    return true;
}


bool NgUserPathWinEnvironmentVariableOperation::undoOperation ()
{
    if (!checkArgumentCount(1))
        return false;

    const QStringList args = arguments();
    const QString value = args.at(0);

    QString curValue = readPath();

    QStringList list = curValue.split(QLatin1String(";"));
    for (int i=list.size()-1; i>=0; i--) // search from the end because we had appended the variable
    {
        if (list[i] == value)
        {
            list.removeAt(i);
            break;
        }
    }

    if (list.size() == 0)
        curValue = QLatin1String("");
    else if (list.size() == 1)
        curValue = list[0];
    else
        curValue = list.join(QLatin1String(";"));

    // QUESTION: maybe delete the Path variable if it becomes void.

    rewritePath(curValue);

    return true;
}


bool NgUserPathWinEnvironmentVariableOperation::testOperation ()
{
    return true;
}

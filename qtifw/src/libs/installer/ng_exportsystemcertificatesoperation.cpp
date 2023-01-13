/******************************************************************************
*
*    Copyright (C) 2023 NextGIS, info@nextgis.com
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

#include "ng_exportsystemcertificatesoperation.h"

#include <QFile>
#include <QSslCertificate>
#include <QSslConfiguration>

using namespace QInstaller;

NgExportSystemCertificatesOperation::NgExportSystemCertificatesOperation (PackageManagerCore* core)
    : UpdateOperation(core)
{
    setName(QLatin1String("NgExportSystemCertificates"));
}


void NgExportSystemCertificatesOperation::backup ()
{
}

bool NgExportSystemCertificatesOperation::performOperation ()
{
    if (!checkArgumentCount(1))
    {
        return false;
    }

    const QStringList args = arguments();
    const QString &targetFilePath = args.at(0);

    QByteArray certificates;
    for (const QSslCertificate &certificate : QSslConfiguration::systemCaCertificates())
    {
        certificates += certificate.toPem();
    }

    QFile certFile(targetFilePath);
    if (certFile.open(QIODevice::WriteOnly | QIODevice::Truncate))
    {
        certFile.write(certificates);
        certFile.close();
    }
    else
    {
        setError(UserDefinedError);
        setErrorString(tr("Could not open file: %1").arg(targetFilePath));
        return false;
    }

    return true;
}

bool NgExportSystemCertificatesOperation::undoOperation ()
{
    return true;
}

bool NgExportSystemCertificatesOperation::testOperation ()
{
    return true;
}

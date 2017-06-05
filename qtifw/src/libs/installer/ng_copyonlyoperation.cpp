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

#include "ng_copyonlyoperation.h"

using namespace QInstaller;


NgCopyOnlyOperation::NgCopyOnlyOperation ()
{
    setName(QLatin1String("NgCopyOnly"));
}


void NgCopyOnlyOperation::backup ()
{
}


// This operation copies file in performOperation() and does not delete it in undoOperation().
bool NgCopyOnlyOperation::performOperation ()
{
    QStringList args = arguments();
    if (args.count() != 2)
    {
        setError(InvalidArguments);
        setErrorString(tr("[Ng] Invalid arguments: %1 argument(s) given, 2 expected.\n")
            .arg(arguments().count()));
        return false;
    }

    const QString srcPath = arguments().at(0);
    const QString tgtPath = arguments().at(1);

    QFile srcFile(srcPath);
    if (!srcFile.exists())
    {
        //setError(UserDefinedError);
        //setErrorString(tr("Could not copy a non-existent file: %1").arg(srcPath));
        //return false;

        // TODO: show warning if there was no file copied.
        // NOTE: for NextGIS software it is important not to throw error here in case of
        // .bash_profile file on Mac.
        return true;
    }

    // We must remove destination file first in order to copy the source file.
    // For the NextGIS software it is also important in cases when we install the software
    // second/third/etc time.
    QFile tgtFile(tgtPath);
    if (tgtFile.exists() && !tgtFile.remove())
    {
        setError(UserDefinedError);
        setErrorString(tr("Could not remove destination file %1: %2")
                       .arg(tgtPath, tgtFile.errorString()));
        return false;
    }

    bool ok = srcFile.copy(tgtPath);
    if (!ok)
    {
        setError(UserDefinedError);
        setErrorString(tr("Could not copy %1 to %2: %3")
                       .arg(srcPath, tgtPath, srcFile.errorString()));
        return false;
    }

    return true;
}


bool NgCopyOnlyOperation::undoOperation ()
{
    return true; // nothing to do here.
}


bool NgCopyOnlyOperation::testOperation ()
{
    return true;
}


KDUpdater::UpdateOperation *NgCopyOnlyOperation::clone () const
{
    return new NgCopyOnlyOperation();
}





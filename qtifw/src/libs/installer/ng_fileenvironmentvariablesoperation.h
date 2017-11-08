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

#ifndef NG_FILEENVIRONMENTVARIABLESOPERATION_H
#define NG_FILEENVIRONMENTVARIABLESOPERATION_H

#include "qinstallerglobal.h"

namespace QInstaller
{

class INSTALLER_EXPORT NgFileEnvironmentVariableOperation: public Operation
{
    Q_DECLARE_TR_FUNCTIONS(QInstaller::NgFileEnvironmentVariableOperation)
public:
     explicit NgFileEnvironmentVariableOperation(PackageManagerCore *core);

     void backup();
     bool performOperation();
     bool undoOperation();
     bool testOperation();
};

}

#endif // NG_FILEENVIRONMENTVARIABLESOPERATION_H




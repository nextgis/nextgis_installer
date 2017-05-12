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

#include <QTemporaryFile>
#include <QTextStream>
#include <QDir>

#include "ng_fileenvironmentvariablesoperation.h"

using namespace QInstaller;

#ifdef Q_OS_WIN
    #define NG_ENVVAR_DELIMITER ";"
#else
    #define NG_ENVVAR_DELIMITER ":"
#endif


NgFileEnvironmentVariableOperation::NgFileEnvironmentVariableOperation ()
{
    setName(QLatin1String("NgFileEnvironmentVariable"));
}


void NgFileEnvironmentVariableOperation::backup ()
{
}


// Add persistant environment variable to the system.
// WARNING. Do not use this operation to add more than one variable (via delimiter). Use several
// operations instead!
bool NgFileEnvironmentVariableOperation::performOperation ()
{
    QStringList args = arguments();
    if (args.count() != 3)
    {
        setError(InvalidArguments);
        setErrorString(tr("[Ng] Invalid arguments: %1 argument(s) given, 3 expected.\n")
            .arg(arguments().count()));
        return false;
    }

    const QString name = arguments().at(0);
    const QString value = arguments().at(1);
    const QString filePath = arguments().at(2);

    // Find/create the file with system variables.
    QFile file(filePath);
    if (!file.open(QIODevice::ReadWrite | QIODevice::Text))
    {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] File %1 not found or can not be opened.\n").arg(filePath));
        return false;
    }

    // Read/parse file.
    QStringList fileContents = this->readFile(&file);
    file.close(); // close in order to replace this file further

    // Find the given variable. Append the given value via delimeter if found. Otherwise create
    // a new line with variable and its value.
    QStringList values;
    int i = this->findVariable(fileContents, name, values);
    if (i == -1) // variable was not found
    {
        QString newVariableStr = QLatin1String("export ") + name + QLatin1String("=") + value;
        fileContents.append(newVariableStr);
    }
    else
    {
        QString newVariableStr = QString(QLatin1String(NG_ENVVAR_DELIMITER)) + value;
        fileContents[i] += newVariableStr;
        // NOTE: if this variable already has such value - we double it in order to correctly
        // remove the value in the undoOperation(). This behaviour can be important when user e.g.
        // for Mac already has a "some-path:$PATH" value in PATH variable and at the same time he
        // adds "another-path" + "$PATH" values.
    }

    // Write back modified file contents.
    if (!this->rewriteFile(filePath, fileContents))
    {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] Unable to rewrite the file %1 with modified contents.\n")
                       .arg(filePath));
        return false;
    }

    return true;
}


bool NgFileEnvironmentVariableOperation::undoOperation ()
{
    QStringList args = arguments();
    if (args.count() != 3)
        return false;

    const QString name = arguments().at(0);
    const QString value = arguments().at(1);
    const QString filePath = arguments().at(2);

    // Find the file with system variables.
    if (!QFile::exists(filePath))
        return true; // ok if there is no file but this is unusual
    QFile file(filePath);
    if (!file.open(QIODevice::ReadWrite | QIODevice::Text))
        return false;

    // Read/parse file.
    QStringList fileContents = this->readFile(&file);
    file.close(); // close in order to replace this file further

    // Find the given variable. If variable is found and it contains the given value - we delete
    // the value.
    QStringList values;
    int i = this->findVariable(fileContents, name, values);
    if (i != -1) // variable was found
    {
        int k;
        bool found = false;
        for (k = 0; k < values.size(); k++)
        {
            if (values[k] == value) // value of the variable was found
            {
                found = true;
                break;
            }
        }

        if (found)
        {
            // If variable becomes void after deletion of the value - we delete the whole variable.
            values.removeAt(k);
            if (values.size() == 0)
            {
                fileContents.removeAt(i);
            }
            else
            {
                QString newVariableStr = QLatin1String("export ") + name + QLatin1String("=")
                        + values.join(QLatin1String(NG_ENVVAR_DELIMITER));
                fileContents[i] = newVariableStr;
            }
        }
        else
        {
            return true;
        }
    }
    else
    {
        return true;
    }

    // Write back modified file contents.
    if (!this->rewriteFile(filePath, fileContents))
    {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] Unable to rewrite the file %1 with modified contents.\n")
                       .arg(filePath));
        return false;
    }

    return true;
}


bool NgFileEnvironmentVariableOperation::testOperation ()
{
    return true;
}


KDUpdater::UpdateOperation *NgFileEnvironmentVariableOperation::clone () const
{
    return new NgFileEnvironmentVariableOperation();
}


// Return all lines in a text file.
QStringList NgFileEnvironmentVariableOperation::readFile (QFile *file)
{
    QStringList fileContents;
    QTextStream in(file);
    while (true)
    {
        QString line = in.readLine();
        if (line.isNull())
            break;
        else
            fileContents.append(line);
    }
    return fileContents;
}


// Return a line number in a given list of system variables (with export commands) or -1 if
// variable is not found. The returned listValues is an array of values of the given variable.
int NgFileEnvironmentVariableOperation::findVariable (QStringList list, QString name,
                                                  QStringList &listValues)
{
    bool found = false;

    int i;
    for (i = 0; i < list.size(); i++)
    {
        QString str = list[i];
        if (!str.startsWith(QLatin1String("export "))) // will also ignore comments like "#export ..."
            continue;

        str.remove(0,7); // remove "export "
        QStringList strs = str.split(QLatin1String("=")); // 0 item will be the name of the variable
        if (strs[0] == name)
        {
            found = true;

            // Form the list of variable values for returning in parameter.
            strs.removeFirst();
            listValues = strs.join(QLatin1String("")).split(QLatin1String(NG_ENVVAR_DELIMITER));

            break;
        }
    }

    if (found)
        return i;

    return -1;
}


// Write to the temp file and than replace the target one.
bool NgFileEnvironmentVariableOperation::rewriteFile (QString targetFilePath, QStringList fileContents)
{
    QTemporaryFile tempFile(QDir::tempPath() + QLatin1String("/ng_envvarXXXXXX"));
    if (!tempFile.open())
        return false;

    QTextStream out(&tempFile);
    for (int i = 0; i < fileContents.size(); i++)
        out << fileContents[i] << QLatin1String("\n");

    // TODO: maybe implement some kind of a transaction here.
    if (!QFile::remove(targetFilePath) || !tempFile.copy(targetFilePath)) // copy with replacing
        return false;

    return true;
}





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

#include "ng_fileenvironmentvariablesoperation.h"

#include <QDir>
#include <QFile>
#include <QTemporaryFile>
#include <QTextStream>

using namespace QInstaller;

#ifdef Q_OS_WIN
    #define NG_ENVVAR_DELIMITER ";"
#else
    #define NG_ENVVAR_DELIMITER ":"
#endif

// Return all lines in a text file.
static QStringList readFile (QFile *file)
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
static int findExportVariable (const QStringList &list, const QString &name,
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

        if (strs.isEmpty())
            continue;
        if (strs[0] == name)
        {
            found = true;

            // Form the list of variable values for returning in parameter.
            strs.removeFirst();
            if (strs.isEmpty()) // so listValues will be empty
                break;
            listValues = strs.join(QLatin1String("")).split(QLatin1String(NG_ENVVAR_DELIMITER));
            break;
        }
    }

    if (found)
        return i;

    return -1;
}


// Return the new string with variable assignement.
static QString getNewAssignement (const QString &name, const QString &value)
{
    return name + QLatin1String("=\"") + value
            + QLatin1String(NG_ENVVAR_DELIMITER)
            + QLatin1String("${") + name + QLatin1String("}\"");
}


// Write to the temp file and than replace the target one.
static bool rewriteFile (const QString &targetFilePath, const QStringList &fileContents)
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


NgFileEnvironmentVariableOperation::NgFileEnvironmentVariableOperation (PackageManagerCore* core)
    : UpdateOperation(core)
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
    if (!checkArgumentCount(3,4)) {
        return false;
    }

    const QStringList args = arguments();
    const QString name = args.at(0);
    const QString value = args.at(1);
    const QString filePathListStr = args.at(2);
    const QStringList filePathList = filePathListStr.split(QLatin1String(";"));
    if(filePathList.isEmpty()) {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] Paths list is empty.\n"));
        return false;
    }

    const bool isSingle = args.count() > 3 ? args.at(3) == QLatin1String("single") : false;

    QStringList fileContents;
    QString filePath;
    // Check if file from list exists
    foreach(filePath, filePathList) {
        QFile file(filePath);
        if(file.exists()) {
            if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
                fileContents = readFile(&file);
                break;
            }
        }
    }

    // If file exists - add variable, else create first file from list
    if(fileContents.isEmpty()) {
        filePath = filePathList.first();
        QFile file(filePath);
        if (!file.open(QIODevice::ReadWrite | QIODevice::Text)) {
            setError(UserDefinedError);
            setErrorString(tr("[Ng] File %1 not found or can not be opened.\n").arg(filePath));
            return false;
        }
        fileContents = readFile(&file);
    }

    // Find the given variable. Append the given value via delimeter if found. Otherwise create
    // a new line with variable and its value.
    QStringList values;
    int i = findExportVariable(fileContents, name, values);
    if (-1 == i) { // variable was not found
        // Add new string with export assignement.
        QString newVariableStr = QLatin1String("export ") + name + QLatin1String("=") + value;
        fileContents.append(newVariableStr);
    }
    else {
        if(!isSingle) {
            // Case 1.
            // We must consider the case when we have e.g. "export PATH" without any "=". This
            // means that there is already some variable assignement above this string.
            // So we must add our own assignement right above the "export" string and also with
            // saving of an old value.
            if (values.isEmpty())  {
                QString assignementStr = getNewAssignement(name, value);
                fileContents.insert(i, assignementStr);
            }
            // Case 2.
            // Otherwise just append the variable.
            else {
                // NOTE: if this variable already has the same value - we double it in order to correctly
                // remove the value in the undoOperation(). This behaviour can be important when user e.g.
                // for Mac already has a "some-path:$PATH" value in PATH variable and at the same time he
                // adds "another-path" + "$PATH" values.
                QString newExportStr = QString(QLatin1String(NG_ENVVAR_DELIMITER)) + value;
                fileContents[i] += newExportStr;
            }
        }
    }

    // Write back modified file contents.
    if (!rewriteFile(filePath, fileContents)) {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] Unable to rewrite the file %1 with modified contents.\n")
                       .arg(filePath));
        return false;
    }

    return true;
}


bool NgFileEnvironmentVariableOperation::undoOperation ()
{
    if (!checkArgumentCount(3, 4)) {
        return false;
    }

    const QStringList args = arguments();
    const QString name = args.at(0);
    const QString value = args.at(1);
    const QString filePathListStr = args.at(2);
    const QStringList filePathList = filePathListStr.split(QLatin1String(";"));
    if(filePathList.isEmpty()) {
        setError(UserDefinedError);
        setErrorString(tr("[Ng] Paths list is empty.\n"));
        return false;
    }

    const bool isSingle = args.count() > 3 ? args.at(3) == QLatin1String("single") : false;

    // Find the file with system variables.
    QString filePath;
    bool isFound = false;
    // Check if file from list exists
    foreach(filePath, filePathList) {
        if (QFile::exists(filePath)) {
            isFound = true;
            break;
        }
    }

    if(!isFound) {
        return true; // ok if there is no file but this is unusual
    }

    QFile file(filePath);
    if (!file.open(QIODevice::ReadWrite | QIODevice::Text)) {
        return false;
    }

    // Read/parse file.
    QStringList fileContents = readFile(&file);
    file.close(); // close in order to replace this file further

    // Find the given variable. If variable is found and it contains the given value - we delete
    // the value.
    QStringList values;
    int i = findExportVariable(fileContents, name, values);
    if (-1 == i) { // variable was not found
        return true;
    }

    // Case 1: string with the void export (e.g. when we have "export PATH" without "=").
    // Delete the added string with an assignement which is placed above the "export" string.
    if (values.isEmpty()) {
        // Search for that string and remove it.
        // NOTE: currently we do not suppose that this string was changed by user.
        QString str = getNewAssignement(name, value);
        fileContents.removeAll(str);
    }

    // Case 2: string with export assignement. Look for the added value inside the "export"
    // string.
    else {
        int k;
        bool valueFound = false;

        for (k = 0; k < values.size(); k++) {
            if (values[k] == value) { // value of the variable was found
                valueFound = true;
                break;
            }
        }

        if (!valueFound) {
            return true;
        }

        // If a variable becomes void after deletion of the value - we delete the whole variable.
        values.removeAt(k);
        if (values.size() == 0) {
            fileContents.removeAt(i);
        }
        else {
            QString newVariableStr = QLatin1String("export ") + name + QLatin1String("=")
                    + values.join(QLatin1String(NG_ENVVAR_DELIMITER));
            fileContents[i] = newVariableStr;
        }
    }

    // Write back modified file contents.
    if (!rewriteFile(filePath, fileContents)) {
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

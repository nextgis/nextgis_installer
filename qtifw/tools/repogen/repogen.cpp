/**************************************************************************
**
** Copyright (C) 2021 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Installer Framework.
**
** $QT_BEGIN_LICENSE:GPL-EXCEPT$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 as published by the Free Software
** Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
**************************************************************************/

#include <repositorygen.h>
#include <errors.h>
#include <fileutils.h>
#include <init.h>
#include <updater.h>
#include <settings.h>
#include <utils.h>
#include <loggingutils.h>
#include <lib7z_facade.h>

#include <QDomDocument>
#include <QtCore/QDir>
#include <QtCore/QDirIterator>
#include <QtCore/QFileInfo>
#include <QTemporaryDir>

#include <iostream>

#define QUOTE_(x) #x
#define QUOTE(x) QUOTE_(x)

using namespace QInstaller;

static void printUsage()
{
    const QString appName = QFileInfo(QCoreApplication::applicationFilePath()).fileName();
    std::cout << "Usage: " << appName << " [options] repository-dir" << std::endl;
    std::cout << std::endl;
    std::cout << "Options:" << std::endl;

    QInstallerTools::printRepositoryGenOptions();

    std::cout << "  -r|--remove               Force removing target directory if existent." << std::endl;

    std::cout << "  --update                  Update a set of existing components (defined by " << std::endl;
    std::cout << "                            --include or --exclude) in the repository" << std::endl;

    std::cout << "  --update-new-components   Update a set of existing components (defined by " << std::endl;
    std::cout << "                            --include or --exclude) in the repository with all new components"
        << std::endl;

    std::cout << "  -v|--verbose              Verbose output" << std::endl;

    std::cout << "  --unite-metadata          Combine all metadata into one 7z. This speeds up metadata " << std::endl;
    std::cout << "                            download phase." << std::endl;

    std::cout << "  --component-metadata      Creates one metadata 7z per component. " << std::endl;

    std::cout << std::endl;
    std::cout << "Example:" << std::endl;
    std::cout << "  " << appName << " -p ../examples/packages repository/"
        << std::endl;
}

static int printErrorAndUsageAndExit(const QString &err)
{
    std::cerr << qPrintable(err) << std::endl << std::endl;
    printUsage();
    return 1;
}

int main(int argc, char** argv)
{
    QString tmpMetaDir;
    int exitCode = EXIT_FAILURE;
    try {
        QCoreApplication app(argc, argv);

        QInstaller::init();

        QStringList args = app.arguments().mid(1);

        QStringList filteredPackages;
        bool updateExistingRepository = false;
        QStringList packagesDirectories;
        QStringList repositoryDirectories;
        QInstallerTools::FilterType filterType = QInstallerTools::Exclude;
        bool remove = false;
        bool updateExistingRepositoryWithNewComponents = false;
        bool createUnifiedMetadata = true;
        bool createComponentMetadata = true;

        //TODO: use a for loop without removing values from args like it is in binarycreator.cpp
        //for (QStringList::const_iterator it = args.begin(); it != args.end(); ++it) {
        while (!args.isEmpty() && args.first().startsWith(QLatin1Char('-'))) {
            if (args.first() == QLatin1String("--verbose") || args.first() == QLatin1String("-v")) {
                args.removeFirst();
                LoggingHandler::instance().setVerbose(true);
            } else if (args.first() == QLatin1String("--exclude") || args.first() == QLatin1String("-e")) {
                args.removeFirst();
                if (!filteredPackages.isEmpty()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: --include and --exclude are mutually exclusive. Use either one or "
                        "the other."));
                }

                if (args.isEmpty() || args.first().startsWith(QLatin1Char('-'))) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Package to exclude missing"));
                }

                filteredPackages = args.first().split(QLatin1Char(','));
                args.removeFirst();
            } else if (args.first() == QLatin1String("--include") || args.first() == QLatin1String("-i")) {
                args.removeFirst();
                if (!filteredPackages.isEmpty()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: --include and --exclude are mutually exclusive. Use either one or "
                        "the other."));
                }

                if (args.isEmpty() || args.first().startsWith(QLatin1Char('-'))) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Package to include missing"));
                }

                filteredPackages = args.first().split(QLatin1Char(','));
                args.removeFirst();
                filterType = QInstallerTools::Include;
            } else if (args.first() == QLatin1String("--update")) {
                args.removeFirst();
                updateExistingRepository = true;
            } else if (args.first() == QLatin1String("--update-new-components")) {
                args.removeFirst();
                updateExistingRepositoryWithNewComponents = true;
                createUnifiedMetadata = false;
            } else if (args.first() == QLatin1String("-p") || args.first() == QLatin1String("--packages")) {
                args.removeFirst();
                if (args.isEmpty()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Packages parameter missing argument"));
                }
                const QDir dir(args.first());
                if (!dir.exists()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Package directory not found at the specified location"));
                }
                if (dir.entryList(QDir::Dirs | QDir::NoDotAndDotDot).isEmpty()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Package directory is empty"));
                }

                packagesDirectories.append(args.first());
                args.removeFirst();
            } else if (args.first() == QLatin1String("--repository")) {
                args.removeFirst();
                if (args.isEmpty()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Repository parameter missing argument"));
                }

                if (!QFileInfo(args.first()).exists()) {
                    return printErrorAndUsageAndExit(QCoreApplication::translate("QInstaller",
                        "Error: Only local filesystem repositories now supported"));
                }
                repositoryDirectories.append(args.first());
                args.removeFirst();
            } else if (args.first() == QLatin1String("--ignore-translations")
                || args.first() == QLatin1String("--ignore-invalid-packages")) {
                    args.removeFirst();
            } else if (args.first() == QLatin1String("-r") || args.first() == QLatin1String("--remove")) {
                remove = true;
                args.removeFirst();
            } else if (args.first() == QLatin1String("--unite-metadata")) {
                createComponentMetadata = false;
                args.removeFirst();
            } else if (args.first() == QLatin1String("--component-metadata")) {
                createUnifiedMetadata = false;
                args.removeFirst();
            }
            else {
                printUsage();
                return 1;
            }
        }

        if ((packagesDirectories.isEmpty() && repositoryDirectories.isEmpty()) || (args.count() != 1)) {
                printUsage();
                return 1;
        }

        const bool update = updateExistingRepository || updateExistingRepositoryWithNewComponents;
        if (remove && update) {
            throw QInstaller::Error(QCoreApplication::translate("QInstaller",
                "Argument -r|--remove and --update|--update-new-components are mutually exclusive!"));
        }

        const QString repositoryDir = QInstallerTools::makePathAbsolute(args.first());
        if (remove)
            QInstaller::removeDirectory(repositoryDir);

        if (updateExistingRepositoryWithNewComponents) {
            QStringList meta7z = QDir(repositoryDir).entryList(QStringList()
                << QLatin1String("*_meta.7z"), QDir::Files);
            if (!meta7z.isEmpty()) {
                throw QInstaller::Error(QCoreApplication::translate("QInstaller",
                    "Cannot update \"%1\" with --update-new-components. Use --update instead. "
                    "Currently it is not possible to update partial components inside one 7z.")
                    .arg(meta7z.join(QLatin1Char(','))));
            }
        }

        if (!update && QFile::exists(repositoryDir) && !QDir(repositoryDir).entryList(
            QDir::AllEntries | QDir::NoDotAndDotDot).isEmpty()) {

            throw QInstaller::Error(QCoreApplication::translate("QInstaller",
                "Repository target directory \"%1\" already exists.").arg(QDir::toNativeSeparators(repositoryDir)));
        }

        QInstallerTools::PackageInfoVector packages;

        QInstallerTools::PackageInfoVector precompressedPackages = QInstallerTools::createListOfRepositoryPackages(repositoryDirectories,
            &filteredPackages, filterType);
        packages.append(precompressedPackages);

        QInstallerTools::PackageInfoVector preparedPackages = QInstallerTools::createListOfPackages(packagesDirectories,
            &filteredPackages, filterType);
        packages.append(preparedPackages);

        if (updateExistingRepositoryWithNewComponents) {
             QInstallerTools::filterNewComponents(repositoryDir, packages);
             if (packages.isEmpty()) {
                 std::cout << QString::fromLatin1("Cannot find new components to update \"%1\".")
                     .arg(repositoryDir) << std::endl;
                 return EXIT_SUCCESS;
             }
        }

        QHash<QString, QString> pathToVersionMapping = QInstallerTools::buildPathToVersionMapping(packages);

        foreach (const QInstallerTools::PackageInfo &package, packages) {
            const QFileInfo fi(repositoryDir, package.name);
            if (fi.exists())
                removeDirectory(fi.absoluteFilePath());
        }

        QTemporaryDir tmp;
        tmp.setAutoRemove(false);
        tmpMetaDir = tmp.path();
        QStringList directories;
        directories.append(packagesDirectories);
        directories.append(repositoryDirectories);
        QStringList unite7zFiles;
        foreach (const QString &repositoryDirectory, repositoryDirectories) {
            QDirIterator it(repositoryDirectory, QStringList(QLatin1String("*_meta.7z"))
                            , QDir::Files | QDir::CaseSensitive);
            while (it.hasNext()) {
                it.next();
                unite7zFiles.append(it.fileInfo().absoluteFilePath());
            }
        }
        QInstallerTools::copyComponentData(directories, repositoryDir, &packages);
        QInstallerTools::copyMetaData(tmpMetaDir, repositoryDir, packages, QLatin1String("{AnyApplication}"),
            QLatin1String(QUOTE(IFW_REPOSITORY_FORMAT_VERSION)), unite7zFiles);

        QString existing7z = QInstallerTools::existingUniteMeta7z(repositoryDir);
        if (!existing7z.isEmpty())
            existing7z = repositoryDir + QDir::separator() + existing7z;
        QInstallerTools::compressMetaDirectories(tmpMetaDir, existing7z, pathToVersionMapping,
                                                 createComponentMetadata, createUnifiedMetadata);

        QDirIterator it(repositoryDir, QStringList(QLatin1String("Updates*.xml"))
                        << QLatin1String("*_meta.7z"), QDir::Files | QDir::CaseSensitive);
        while (it.hasNext()) {
            it.next();
            QFile::remove(it.fileInfo().absoluteFilePath());
        }
        QInstaller::moveDirectoryContents(tmpMetaDir, repositoryDir);
        exitCode = EXIT_SUCCESS;
    } catch (const Lib7z::SevenZipException &e) {
        std::cerr << "Caught 7zip exception: " << e.message() << std::endl;
    } catch (const QInstaller::Error &e) {
        std::cerr << "Caught exception: " << e.message() << std::endl;
    } catch (...) {
        std::cerr << "Unknown exception caught" << std::endl;
    }

    QInstaller::removeDirectory(tmpMetaDir, true);
    return exitCode;
}

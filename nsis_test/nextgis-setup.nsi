SetCompressor zlib

!include "LogicLib.nsh"
!include "Sections.nsh"
!include "MUI2.nsh"

!define VERSION "0.0.1"
!define SUBVERSION "Alpha"
!define PRODUCT "NextGIS programs"

; General configuration
Name "${PRODUCT}"
OutFile "nextgis-setup.exe"
InstallDir "$PROGRAMFILES\NextGIS-test"
RequestExecutionLevel highest ;Request application privileges for Windows Vista
SetDateSave on
SetDatablockOptimize on
CRCCheck on
XPStyle on
BrandingText "${PRODUCT}"
AutoCloseWindow false
ShowInstDetails show

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_HEADERIMAGE
!define MUI_COMPONENTSPAGE_SMALLDESC

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE $(myLicenseData)	
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH 
    
; Uninstall Pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES  

; Languages
!insertmacro MUI_LANGUAGE "Russian"
!insertmacro MUI_LANGUAGE "English"
	
; License data
LicenseLangString myLicenseData ${LANG_ENGLISH} "license.txt"
LicenseLangString myLicenseData ${LANG_RUSSIAN} "license.txt"

;Reserve Files
;These files should be inserted before other files in the data block
;Keep these lines before any File command
;Only for solid compression (by default, solid compression is enabled for BZIP2 and LZMA)
!insertmacro MUI_RESERVEFILE_LANGDLL

; Macro to download package 
!macro downloadPackage fileurl filename
    inetc::get "${fileurl}" "$INSTDIR\${filename}.zip" /end
    Pop $0
    ${If} $0 == "OK"
        nsisunz::Unzip "$INSTDIR\${filename}.zip" "$INSTDIR"
        Pop $1
        ${If} $1 == "success"
            CopyFiles /SILENT "$INSTDIR\${filename}\*.*" "$INSTDIR"
            RMDir /r "$INSTDIR\${filename}"
            Delete "${filename}.zip"
        ${Else}
            DetailPrint "Failed to unzip Formbuilder package! Error: $1"
        ${EndIf}
    ${Else}
        DetailPrint "Failed to download Formbuilder package! Error: $0"
    ${EndIf}  
!macroend
  
;Hidden section - common files.
Section "-common" SecCommon

    SetDetailsPrint textonly
    DetailPrint "Common files ..."
    SetDetailsPrint listonly 
    
    SetOutPath "$INSTDIR"
    WriteUninstaller "$INSTDIR\uninstall.exe"
    CreateDirectory "$SMPROGRAMS\NextGIS-test"
  
SectionEnd

;Package sections
SectionGroup /e "!$(str_Programs)" SecProgs

	Section "Formbuilder" SecFb 
		SetDetailsPrint textonly
		DetailPrint "Installing Formbuilder files ..."
		SetDetailsPrint listonly
        SetOutPath "$INSTDIR\bin"
		CreateShortCut "$SMPROGRAMS\NextGIS-test\Formbuilder.lnk" "$INSTDIR\bin\fb.exe"
        CreateShortCut "$DESKTOP\Formbuilder.lnk" "$INSTDIR\bin\fb.exe"
        SetOutPath "$INSTDIR"
		CreateShortCut "$SMPROGRAMS\NextGIS-test\Uninstall.lnk" "$INSTDIR\uninstall.exe"
		SetOutPath "$INSTDIR"
        !insertmacro downloadPackage "http://176.9.38.120/installer/formbuilder-install.zip" "formbuilder-install"

	SectionEnd
    
	Section "QGIS" SecQgis
		SetDetailsPrint textonly
		DetailPrint "Installing QGIS files ..."
		SetDetailsPrint listonly
		SetOutPath "$INSTDIR"
        !insertmacro downloadPackage "http://176.9.38.120/installer/qgis-install.zip" "qgis-install"

	SectionEnd	
    
SectionGroupEnd


;Descriptions
!include "LangFile.nsh"
LangString str_Programs ${LANG_ENGLISH} "Programs"
LangString str_Programs ${LANG_RUSSIAN} "Программы"
LangString str_DescriptionFb ${LANG_ENGLISH} "Forms creator for NextGIS Mobile"
LangString str_DescriptionFb ${LANG_RUSSIAN} "Построитель форм для NextGIS Mobile"
LangString str_DescriptionQgis ${LANG_ENGLISH} "Desktop GIS"
LangString str_DescriptionQgis ${LANG_RUSSIAN} "Настольная ГИС"
;Assign descriptions to sections
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
!insertmacro MUI_DESCRIPTION_TEXT ${SecFb} $(str_DescriptionFb)
!insertmacro MUI_DESCRIPTION_TEXT ${SecQgis} $(str_DescriptionQgis)
!insertmacro MUI_FUNCTION_DESCRIPTION_END


;Uninstaller Section
Section "Uninstall"

  SetDetailsPrint textonly
  DetailPrint "Uninstalling NextGIS programs ..."
  SetDetailsPrint listonly

  RMDir /r /REBOOTOK "$INSTDIR"
  
  RMDir /r "$SMPROGRAMS\NextGIS-test"
  Delete "$DESKTOP\Formbuilder.lnk"
  
SectionEnd

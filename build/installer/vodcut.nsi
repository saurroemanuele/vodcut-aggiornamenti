; NoonFrame - installer per Windows (NSIS)
; Installa nella cartella dell'utente (niente permessi da amministratore).
; Tutto e' dentro l'installer (Python, librerie, ffmpeg): non scarica niente e non usa PowerShell,
; cosi' gli antivirus non lo scambiano per un programma sospetto.

Unicode true
SetCompressor /SOLID lzma

!define APPNAME "NoonFrame"
; nome interno (cartella e registro): cosi' chi aveva VODcut si aggiorna sul posto
!define APPID "VODcut"
!define COMPANY "Emanuele Saurro"
!define VERSION "1.5.112"
!define UNINSTKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPID}"

Name "${APPNAME}"
OutFile "Noonframe-Setup.exe"
InstallDir "$LOCALAPPDATA\Programs\${APPID}"
InstallDirRegKey HKCU "Software\${APPID}" "InstallDir"
RequestExecutionLevel user
ShowInstDetails show
ShowUninstDetails show
BrandingText "${APPNAME} ${VERSION}"

VIProductVersion "${VERSION}.0"
VIAddVersionKey /LANG=1033 "ProductName" "${APPNAME}"
VIAddVersionKey /LANG=1033 "CompanyName" "${COMPANY}"
VIAddVersionKey /LANG=1033 "FileDescription" "Installazione di ${APPNAME}"
VIAddVersionKey /LANG=1033 "FileVersion" "${VERSION}"
VIAddVersionKey /LANG=1033 "ProductVersion" "${VERSION}"
VIAddVersionKey /LANG=1033 "LegalCopyright" "${COMPANY}"

!include "MUI2.nsh"
!include "LogicLib.nsh"

; ---------------- aspetto
!define MUI_ICON "vodcut.ico"
!define MUI_UNICON "vodcut.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "wizard.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "wizard.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "header.bmp"
!define MUI_ABORTWARNING
!define MUI_ABORTWARNING_TEXT "$(s_abort)"

; ---------------- pagine
!define MUI_WELCOMEPAGE_TITLE "$(s_wtitle)"
!define MUI_WELCOMEPAGE_TEXT "$(s_wtext)"
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE_TEXT_TOP "$(s_ltop)"
!define MUI_LICENSEPAGE_TEXT_BOTTOM "$(s_lbottom)"
!define MUI_LICENSEPAGE_BUTTON "$(s_lbutton)"
!insertmacro MUI_PAGE_LICENSE $(s_license)
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TITLE "$(s_ftitle)"
!define MUI_FINISHPAGE_TEXT "$(s_ftext)"
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "$(s_run)"
!define MUI_FINISHPAGE_RUN_FUNCTION RunApp
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; lingua: italiano se Windows e' in italiano, se no inglese
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "Italian"

LicenseLangString s_license ${LANG_ENGLISH} "license_en.txt"
LicenseLangString s_license ${LANG_ITALIAN} "licenza.txt"
LangString s_abort ${LANG_ENGLISH} "Do you really want to cancel the NoonFrame installation?"
LangString s_abort ${LANG_ITALIAN} "Vuoi davvero annullare l'installazione di NoonFrame?"
LangString s_wtitle ${LANG_ENGLISH} "Welcome to NoonFrame"
LangString s_wtitle ${LANG_ITALIAN} "Benvenuto in NoonFrame"
LangString s_wtext ${LANG_ENGLISH} "NoonFrame turns your streams into YouTube-ready videos: cuts, zooms, subtitles and export.$\r$\n$\r$\nEverything it needs is included: no internet connection required.$\r$\n$\r$\nClick Next to continue."
LangString s_wtext ${LANG_ITALIAN} "NoonFrame trasforma le tue live in video pronti per YouTube: tagli, zoom, sottotitoli ed export.$\r$\n$\r$\nDentro c'è già tutto quello che serve: non scarica niente da internet.$\r$\n$\r$\nClicca Avanti per continuare."
LangString s_ltop ${LANG_ENGLISH} "Please read the NoonFrame license agreement (scroll to read all of it)."
LangString s_ltop ${LANG_ITALIAN} "Leggi la licenza d'uso di NoonFrame (scorri per leggerla tutta)."
LangString s_lbottom ${LANG_ENGLISH} "If you accept the terms, click I Agree to continue. You must accept them to install NoonFrame."
LangString s_lbottom ${LANG_ITALIAN} "Se accetti le condizioni, clicca Accetto per continuare. Serve accettarle per installare NoonFrame."
LangString s_lbutton ${LANG_ENGLISH} "I &Agree"
LangString s_lbutton ${LANG_ITALIAN} "&Accetto"
LangString s_ftitle ${LANG_ENGLISH} "NoonFrame is ready"
LangString s_ftitle ${LANG_ITALIAN} "NoonFrame è pronto"
LangString s_ftext ${LANG_ENGLISH} "You'll find NoonFrame on the desktop and in the Start menu.$\r$\n$\r$\nThe first time you create subtitles, NoonFrame downloads the transcription model: it takes a few extra minutes."
LangString s_ftext ${LANG_ITALIAN} "Trovi NoonFrame sul desktop e nel menu Start.$\r$\n$\r$\nLa prima volta che crei i sottotitoli, NoonFrame scarica il modello di trascrizione: ci vuole qualche minuto in più."
LangString s_run ${LANG_ENGLISH} "Open NoonFrame"
LangString s_run ${LANG_ITALIAN} "Apri NoonFrame"
LangString s_python ${LANG_ENGLISH} "Downloading Python"
LangString s_python ${LANG_ITALIAN} "Scarico Python"
LangString s_pip ${LANG_ENGLISH} "Preparing the tools"
LangString s_pip ${LANG_ITALIAN} "Preparo gli strumenti"
LangString s_vc ${LANG_ENGLISH} "Checking Windows components"
LangString s_vc ${LANG_ITALIAN} "Controllo i componenti di Windows"
LangString s_libs ${LANG_ENGLISH} "Installing libraries (a few minutes)"
LangString s_libs ${LANG_ITALIAN} "Installo le librerie (qualche minuto)"
LangString s_win ${LANG_ENGLISH} "Preparing the app window"
LangString s_win ${LANG_ITALIAN} "Preparo la finestra dell'app"
LangString s_ff ${LANG_ENGLISH} "Downloading ffmpeg for videos (about 100 MB)"
LangString s_ff ${LANG_ITALIAN} "Scarico ffmpeg per i video (circa 100 MB)"
LangString s_gpu ${LANG_ENGLISH} "Checking the graphics card"
LangString s_gpu ${LANG_ITALIAN} "Controllo la scheda video"
LangString s_check ${LANG_ENGLISH} "Checking that everything is fine"
LangString s_check ${LANG_ITALIAN} "Controllo che sia tutto a posto"
LangString s_copy ${LANG_ENGLISH} "Copying NoonFrame"
LangString s_copy ${LANG_ITALIAN} "Copio NoonFrame"
LangString s_links ${LANG_ENGLISH} "Creating shortcuts"
LangString s_links ${LANG_ITALIAN} "Creo i collegamenti"
LangString s_done ${LANG_ENGLISH} "Done"
LangString s_done ${LANG_ITALIAN} "Fatto"
LangString s_fail ${LANG_ENGLISH} "Something went wrong (details in $INSTDIR\installazione.log)"
LangString s_fail ${LANG_ITALIAN} "Qualcosa non è andato (dettagli in $INSTDIR\installazione.log)"
LangString s_failbox ${LANG_ENGLISH} "The installation failed during:"
LangString s_failbox ${LANG_ITALIAN} "L'installazione non è riuscita durante:"
LangString s_failbox2 ${LANG_ENGLISH} "Check your internet connection and try again.$\r$\nDetails are in:"
LangString s_failbox2 ${LANG_ITALIAN} "Controlla la connessione a internet e riprova.$\r$\nI dettagli sono in:"
LangString s_open ${LANG_ENGLISH} "Open NoonFrame"
LangString s_open ${LANG_ITALIAN} "Apri NoonFrame"
LangString s_projtype ${LANG_ENGLISH} "NoonFrame project"
LangString s_projtype ${LANG_ITALIAN} "Progetto NoonFrame"
LangString s_accepted ${LANG_ENGLISH} "NoonFrame 1.0 license accepted during installation"
LangString s_accepted ${LANG_ITALIAN} "Licenza NoonFrame 1.0 accettata durante l'installazione"
LangString s_unkeep ${LANG_ENGLISH} "Do you also want to delete your projects and exported videos?$\r$\n($PROFILE\VODcut)$\r$\n$\r$\nIf you choose No, they stay on your PC."
LangString s_unkeep ${LANG_ITALIAN} "Vuoi eliminare anche i tuoi progetti e i video esportati?$\r$\n($PROFILE\VODcut)$\r$\n$\r$\nSe scegli No restano sul PC."
LangString s_lang ${LANG_ENGLISH} "en"
LangString s_lang ${LANG_ITALIAN} "it"

LangString s_running ${LANG_ENGLISH} "NoonFrame is open. Close it and click Retry."
LangString s_running ${LANG_ITALIAN} "NoonFrame è aperto. Chiudilo e clicca Riprova."
LangString s_py ${LANG_ENGLISH} "Copying Python and the libraries"
LangString s_py ${LANG_ITALIAN} "Copio Python e le librerie"
LangString s_ffc ${LANG_ENGLISH} "Copying ffmpeg"
LangString s_ffc ${LANG_ITALIAN} "Copio ffmpeg"

; NoonFrame aperto? (aggiornamento o disinstallazione): i suoi file non si possono sostituire
!macro WaitClosed UN
Function ${UN}WaitClosed
  retry:
  ${If} ${FileExists} "$INSTDIR\python\python312.dll"
    ClearErrors
    FileOpen $0 "$INSTDIR\python\python312.dll" a
    ${If} ${Errors}
      MessageBox MB_RETRYCANCEL|MB_ICONEXCLAMATION "$(s_running)" IDRETRY retry
      Abort
    ${EndIf}
    FileClose $0
  ${EndIf}
FunctionEnd
!macroend
!insertmacro WaitClosed ""
!insertmacro WaitClosed "un."

Function RunApp
  SetOutPath "$INSTDIR\app"
  Exec '"$INSTDIR\python\pythonw.exe" "$INSTDIR\app\server.py"'
FunctionEnd

Section "NoonFrame" SecMain
  SectionIn RO
  SetOutPath "$INSTDIR"
  Call WaitClosed
  ; aggiornamento: il codice, Python e ffmpeg si sostituiscono per intero (i progetti stanno altrove)
  RMDir /r "$INSTDIR\app"
  RMDir /r "$INSTDIR\python"
  RMDir /r "$INSTDIR\ffmpeg"
  Delete "$INSTDIR\setup.ps1"
  DetailPrint "$(s_copy)"
  SetOutPath "$INSTDIR\app"
  File /r "app\*.*"
  DetailPrint "$(s_py)"
  SetOutPath "$INSTDIR\python"
  File /r "..\offline\python\*.*"
  DetailPrint "$(s_ffc)"
  SetOutPath "$INSTDIR\ffmpeg"
  File /r "..\offline\ffmpeg\*.*"

  ; licenza accettata qui: l'app non la chiede di nuovo
  CreateDirectory "$PROFILE\VODcut"
  FileOpen $1 "$PROFILE\VODcut\licenza-accettata.txt" w
  FileWrite $1 "$(s_accepted)"
  FileClose $1

  ; collegamenti (desktop e menu Start)
  DetailPrint "$(s_links)"
  SetOutPath "$INSTDIR\app"
  Delete "$DESKTOP\VODcut.lnk"
  Delete "$SMPROGRAMS\VODcut.lnk"
  Delete "$DESKTOP\Nuvora.lnk"
  Delete "$SMPROGRAMS\Nuvora.lnk"
  Delete "$INSTDIR\Disinstalla VODcut.exe"
  CreateShortCut "$DESKTOP\NoonFrame.lnk" "$INSTDIR\python\pythonw.exe" '"$INSTDIR\app\server.py"' "$INSTDIR\app\vodcut.ico" 0 SW_SHOWNORMAL "" "$(s_open)"
  CreateShortCut "$SMPROGRAMS\NoonFrame.lnk" "$INSTDIR\python\pythonw.exe" '"$INSTDIR\app\server.py"' "$INSTDIR\app\vodcut.ico" 0 SW_SHOWNORMAL "" "$(s_open)"

  ; disinstallazione da Impostazioni > App
  WriteUninstaller "$INSTDIR\Disinstalla NoonFrame.exe"
  WriteRegStr HKCU "Software\${APPID}" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${UNINSTKEY}" "DisplayName" "${APPNAME}"
  WriteRegStr HKCU "${UNINSTKEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNINSTKEY}" "Publisher" "${COMPANY}"
  WriteRegStr HKCU "${UNINSTKEY}" "DisplayIcon" "$INSTDIR\app\vodcut.ico"
  WriteRegStr HKCU "${UNINSTKEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINSTKEY}" "UninstallString" '"$INSTDIR\Disinstalla NoonFrame.exe"'
  WriteRegDWORD HKCU "${UNINSTKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTKEY}" "NoRepair" 1
  WriteRegDWORD HKCU "${UNINSTKEY}" "EstimatedSize" 900000
  ; file .vodcut: doppio clic apre il progetto in NoonFrame
  WriteRegStr HKCU "Software\Classes\.vodcut" "" "VODcut.Progetto"
  WriteRegStr HKCU "Software\Classes\VODcut.Progetto" "" "$(s_projtype)"
  WriteRegStr HKCU "Software\Classes\VODcut.Progetto\DefaultIcon" "" "$INSTDIR\app\vodcut.ico"
  WriteRegStr HKCU "Software\Classes\VODcut.Progetto\shell\open\command" "" '"$INSTDIR\python\pythonw.exe" "$INSTDIR\app\server.py" "%1"'
  System::Call 'shell32::SHChangeNotify(i 0x08000000, i 0, p 0, p 0)'
  DetailPrint "$(s_done)"
SectionEnd

Section "Uninstall"
  Call un.WaitClosed
  Delete "$DESKTOP\NoonFrame.lnk"
  Delete "$SMPROGRAMS\NoonFrame.lnk"
  Delete "$DESKTOP\VODcut.lnk"
  Delete "$SMPROGRAMS\VODcut.lnk"
  Delete "$DESKTOP\Nuvora.lnk"
  Delete "$SMPROGRAMS\Nuvora.lnk"
  RMDir /r "$INSTDIR"
  ; aggiornamenti automatici scaricati (solo codice dell'app)
  RMDir /r "$LOCALAPPDATA\VODcut\aggiornamenti"
  RMDir "$LOCALAPPDATA\VODcut"
  DeleteRegKey HKCU "${UNINSTKEY}"
  DeleteRegKey HKCU "Software\${APPID}"
  DeleteRegKey HKCU "Software\Classes\.vodcut"
  DeleteRegKey HKCU "Software\Classes\VODcut.Progetto"
  MessageBox MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON2 "$(s_unkeep)" IDNO keep
    RMDir /r "$PROFILE\VODcut"
  keep:
SectionEnd

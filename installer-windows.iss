; Inno Setup Script for Jukebox Windows Installer
; Requires Inno Setup 6.0 or later: https://jrsoftware.org/isinfo.php

#define MyAppName "Jukebox Pi Money"
#define MyAppVersion "2.3.0"
#define MyAppPublisher "godfathercorleone994"
#define MyAppURL "https://github.com/godfathercorleone994-wq/Jukebox"
#define MyAppExeName "jukebox.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppId={{8F9A2B3C-4D5E-6F7A-8B9C-0D1E2F3A4B5C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\Jukebox
DisableProgramGroupPage=yes
LicenseFile=LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installers
OutputBaseFilename=jukebox-setup-windows-x64
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenuicon"; Description: "Criar atalho no Menu Iniciar"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "env.example"; DestDir: "{app}"; DestName: ".env.example"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICKSTART_EXECUTABLE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
var
  EnvConfigPage: TInputQueryWizardPage;
  
procedure InitializeWizard;
begin
  // Create custom page for environment configuration
  EnvConfigPage := CreateInputQueryPage(wpSelectDir,
    'Configuração Inicial', 
    'Configure as opções básicas do Jukebox',
    'Você pode mudar estas configurações depois editando o arquivo .env no diretório de instalação.');
  
  EnvConfigPage.Add('Chave Secreta (deixe vazio para gerar automaticamente):', False);
  EnvConfigPage.Add('Habilitar código de operador admin? (true/false):', False);
  EnvConfigPage.Add('Código de operador (deixe vazio se não habilitar):', True);
  
  EnvConfigPage.Values[0] := '';
  EnvConfigPage.Values[1] := 'false';
  EnvConfigPage.Values[2] := '';
end;

function GenerateRandomKey(): String;
var
  I: Integer;
  Chars: String;
begin
  Chars := 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  Result := '';
  for I := 1 to 32 do
    Result := Result + Chars[Random(Length(Chars)) + 1];
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvContent: TArrayOfString;
  SecretKey: String;
  AdminEnabled: String;
  AdminCode: String;
  EnvFile: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Generate .env file from user input
    EnvFile := ExpandConstant('{app}\.env');
    
    // Get values from custom page
    SecretKey := EnvConfigPage.Values[0];
    if SecretKey = '' then
      SecretKey := GenerateRandomKey();
    
    AdminEnabled := EnvConfigPage.Values[1];
    AdminCode := EnvConfigPage.Values[2];
    
    // Create .env content
    SetArrayLength(EnvContent, 20);
    EnvContent[0] := '# Configuração do Jukebox Pi Money';
    EnvContent[1] := '# Gerado automaticamente pelo instalador';
    EnvContent[2] := '';
    EnvContent[3] := '# Flask';
    EnvContent[4] := 'FLASK_ENV=production';
    EnvContent[5] := 'SECRET_KEY=' + SecretKey;
    EnvContent[6] := '';
    EnvContent[7] := '# Hardware (desabilitado por padrão no Windows)';
    EnvContent[8] := 'HARDWARE_ENABLED=false';
    EnvContent[9] := '';
    EnvContent[10] := '# YouTube Player (opcional)';
    EnvContent[11] := 'YOUTUBE_ENABLED=false';
    EnvContent[12] := '';
    EnvContent[13] := '# Preços';
    EnvContent[14] := 'PRICE_PER_SONG=5.00';
    EnvContent[15] := '';
    EnvContent[16] := '# Admin';
    EnvContent[17] := 'ADMIN_ENABLED=' + AdminEnabled;
    if AdminCode <> '' then
      EnvContent[18] := 'ADMIN_CODE=' + AdminCode
    else
      EnvContent[18] := '# ADMIN_CODE=seu_codigo_secreto';
    EnvContent[19] := 'ADMIN_CREDIT_AMOUNT=20.00';
    
    // Save .env file
    SaveStringsToFile(EnvFile, EnvContent, False);
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\data"
Type: files; Name: "{app}\.env"

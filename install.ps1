# Installs flutter-kickstart on Windows: the `fks` command (alias `flutter-kickstart`) plus
# the skills for every supported AI agent.
#
# One line, from anywhere (clones into %USERPROFILE%\.flutter-kickstart):
#   irm https://raw.githubusercontent.com/alamin-karno/flutter-kickstart/main/install.ps1 | iex
#
# From a checkout:
#   powershell -ExecutionPolicy Bypass -File install.ps1            # copy (default on Windows)
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall
param([switch]$Uninstall, [switch]$SkillsOnly)
$ErrorActionPreference = "Stop"
$Home_ = $env:USERPROFILE
$RepoUrl = if ($env:FLUTTER_KICKSTART_REPO) { $env:FLUTTER_KICKSTART_REPO } else { "https://github.com/alamin-karno/flutter-kickstart.git" }
$InstallDir = if ($env:FLUTTER_KICKSTART_HOME) { $env:FLUTTER_KICKSTART_HOME } else { "$Home_\.flutter-kickstart" }

# Piped through `irm | iex` (no script path) or run outside a checkout: fetch the repo, then run its installer.
$Self = $MyInvocation.MyCommand.Path
if (-not $Self -or -not (Test-Path (Join-Path (Split-Path -Parent $Self) "skills\flutter-kickstart"))) {
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required" }
  if (Test-Path "$InstallDir\.git") {
    Write-Host "Updating $InstallDir"
    git -C $InstallDir pull --ff-only --quiet
  } else {
    Write-Host "Cloning flutter-kickstart into $InstallDir"
    git clone --depth 1 --quiet $RepoUrl $InstallDir
  }
  & powershell -ExecutionPolicy Bypass -File "$InstallDir\install.ps1" @PSBoundParameters
  return
}

$Repo = Split-Path -Parent $Self
$AgentDirs = @(
  "$Home_\.claude\skills",
  "$Home_\.agents\skills",
  "$Home_\.codex\skills",
  "$Home_\.cursor\skills",
  "$Home_\.codeium\windsurf\skills",
  "$Home_\.gemini\config\skills",
  "$Home_\.gemini\antigravity\skills",
  "$Home_\.gemini\skills"
)
foreach ($skill in Get-ChildItem -Directory "$Repo\skills") {
  foreach ($dir in $AgentDirs) {
    $target = Join-Path $dir $skill.Name
    $marker = Join-Path $target ".installed-by-flutter-kickstart"
    if ($Uninstall) {
      if (Test-Path $marker) { Remove-Item -Recurse -Force $target; Write-Host "remove $target" }
      continue
    }
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    if ((Test-Path $target) -and -not (Test-Path $marker)) { Write-Host "skip   $target (not installed by this script)"; continue }
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $skill.FullName $target
    New-Item -ItemType File -Path $marker | Out-Null
    Write-Host "copy   $target"
  }
}

# `fks` (short) and `flutter-kickstart` (long) commands: .cmd shims in <repo>\bin, added to the user PATH.
$BinDir = Join-Path $Repo "bin"
$Shims = @("fks.cmd", "flutter-kickstart.cmd") | ForEach-Object { Join-Path $BinDir $_ }
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($Uninstall) {
  foreach ($Shim in $Shims) { if (Test-Path $Shim) { Remove-Item $Shim; Write-Host "remove $Shim" } }
  if ($UserPath -and $UserPath.Split(";") -contains $BinDir) {
    [Environment]::SetEnvironmentVariable("Path", (($UserPath.Split(";") | Where-Object { $_ -ne $BinDir }) -join ";"), "User")
  }
  return
}
if (-not $SkillsOnly) {
  foreach ($Shim in $Shims) { Set-Content -Path $Shim -Encoding ASCII -Value "@echo off`r`npython `"%~dp0flutter-kickstart`" %*" }
  if (-not ($UserPath -and $UserPath.Split(";") -contains $BinDir)) {
    [Environment]::SetEnvironmentVariable("Path", (@($UserPath, $BinDir) | Where-Object { $_ }) -join ";", "User")
    Write-Host "Added $BinDir to your user PATH (open a new terminal to use it)."
  }
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { Write-Host "warning: python not found; install Python 3.8+ before creating an app." }
if (-not (Get-Command flutter -ErrorAction SilentlyContinue)) { Write-Host "warning: flutter not found; install Flutter before creating an app." }

Write-Host ""
Write-Host "flutter-kickstart is installed. The command is ``fks`` (long name: flutter-kickstart)."
Write-Host ""
Write-Host "  fks create              answer a few questions, get a verified app"
Write-Host "  cd <app>; fks run       run it on the development flavor"
Write-Host ""
Write-Host "Or ask your AI agent (start a NEW session first): `"Create a new Flutter app called Acme Wallet for com.acme.`""

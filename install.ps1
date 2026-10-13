# Installs this plugin's skills globally for every supported AI agent (Windows).
#   powershell -ExecutionPolicy Bypass -File install.ps1            # copy (default on Windows)
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall
param([switch]$Uninstall)
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$Home_ = $env:USERPROFILE
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
if (-not $Uninstall) { Write-Host "Done. Start a NEW agent session so it picks up the skills. Re-run after git pull." }

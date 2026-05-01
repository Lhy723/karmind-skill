$ErrorActionPreference = "Stop"

$Repo = if ($env:KARMIND_REPO) { $env:KARMIND_REPO } else { "Lhy723/karmind-skill" }
$Ref = if ($env:KARMIND_REF) { $env:KARMIND_REF } else { "main" }
$Agent = if ($env:KARMIND_AGENT) { $env:KARMIND_AGENT } else { "" }
$ForceInstall = $env:KARMIND_FORCE -eq "1"
$SourceDir = if ($env:KARMIND_SOURCE_DIR) { $env:KARMIND_SOURCE_DIR } else { "" }
$RuntimeScripts = @(
  "ingest_cache.py",
  "init_wiki.py",
  "mirror_assets.py",
  "model_batch_ingest.py",
  "smoke_test.py",
  "wiki_doctor.py"
)

function Join-Parts {
  param([string]$Base, [string[]]$Parts)
  $Path = $Base
  foreach ($Part in $Parts) {
    $Path = Join-Path $Path $Part
  }
  return $Path
}

function Normalize-Agent {
  param([string]$Value)
  switch ($Value.ToLowerInvariant()) {
    "" { return "codex" }
    "1" { return "codex" }
    "codex" { return "codex" }
    "generic" { return "codex" }
    "agents" { return "codex" }
    "2" { return "opencode" }
    "opencode" { return "opencode" }
    "3" { return "trae" }
    "trae" { return "trae" }
    "4" { return "claude" }
    "claude" { return "claude" }
    "claude-code" { return "claude" }
    "5" { return "all" }
    "all" { return "all" }
    default { throw "unknown KARMIND_AGENT: $Value" }
  }
}

function Select-Agent {
  if ($Agent) {
    return Normalize-Agent $Agent
  }

  Write-Host "Install karmind-skill for:"
  Write-Host "  1) Codex / generic agents (.agents/skills)"
  Write-Host "  2) OpenCode (.opencode/skills)"
  Write-Host "  3) Trae (.trae/rules + .trae/skills)"
  Write-Host "  4) Claude Code manual fallback (.claude/skills)"
  Write-Host "  5) All project-level locations"
  $Choice = Read-Host "Choose [1]"
  if (-not $Choice) { $Choice = "1" }
  return Normalize-Agent $Choice
}

function Prepare-Source {
  if ($SourceDir) {
    if (-not (Test-Path (Join-Path $SourceDir "SKILL.md"))) {
      throw "KARMIND_SOURCE_DIR does not look like the repository root: $SourceDir"
    }
    return (Resolve-Path $SourceDir).Path
  }

  $Temp = Join-Path ([System.IO.Path]::GetTempPath()) ("karmind-skill-" + [System.Guid]::NewGuid().ToString("N"))
  New-Item -ItemType Directory -Force $Temp | Out-Null
  $Zip = Join-Path $Temp "source.zip"
  $Extract = Join-Path $Temp "source"
  Invoke-WebRequest -Uri "https://github.com/$Repo/archive/refs/heads/$Ref.zip" -OutFile $Zip
  Expand-Archive -Path $Zip -DestinationPath $Extract -Force
  $Root = Get-ChildItem -Path $Extract -Directory | Where-Object { $_.Name -like "karmind-skill-*" } | Select-Object -First 1
  if (-not $Root) {
    throw "failed to unpack karmind-skill"
  }
  return $Root.FullName
}

function Replace-Directory {
  param([string]$Path)
  if (Test-Path $Path) {
    if (-not $ForceInstall) {
      $Answer = Read-Host "$Path already exists. Replace it? [y/N]"
      if ($Answer -notin @("y", "Y", "yes", "YES")) {
        throw "aborted; set KARMIND_FORCE=1 to replace without prompting"
      }
    }
    Remove-Item -Recurse -Force $Path
  }
}

function Copy-RuntimeSkill {
  param([string]$Root, [string]$Destination, [bool]$IncludeAgents)
  Replace-Directory $Destination
  New-Item -ItemType Directory -Force (Join-Parts $Destination @("scripts")) | Out-Null
  Copy-Item (Join-Path $Root "SKILL.md") (Join-Path $Destination "SKILL.md")
  Copy-Item -Recurse (Join-Path $Root "references") (Join-Path $Destination "references")
  foreach ($Name in $RuntimeScripts) {
    Copy-Item (Join-Parts $Root @("scripts", $Name)) (Join-Parts $Destination @("scripts", $Name))
  }
  if ($IncludeAgents) {
    Copy-Item -Recurse (Join-Path $Root "agents") (Join-Path $Destination "agents")
  }
  Write-Host "installed skill: $Destination"
}

function Install-Codex {
  param([string]$Root)
  Copy-RuntimeSkill $Root ".agents\skills\karmind-skill" $true
}

function Install-OpenCode {
  param([string]$Root)
  Copy-RuntimeSkill $Root ".opencode\skills\karmind-skill" $false
}

function Install-Claude {
  param([string]$Root)
  Copy-RuntimeSkill $Root ".claude\skills\karmind-skill" $false
}

function Install-Trae {
  param([string]$Root)
  Copy-RuntimeSkill $Root ".trae\skills\karmind-skill" $false
  New-Item -ItemType Directory -Force ".trae\rules" | Out-Null
  Copy-Item (Join-Parts $Root @("adapters", "trae_project_rules.md")) ".trae\rules\project_rules.md"
  Write-Host "installed Trae project rules: .trae\rules\project_rules.md"
}

$SelectedAgent = Select-Agent
$RootDir = Prepare-Source

switch ($SelectedAgent) {
  "codex" { Install-Codex $RootDir }
  "opencode" { Install-OpenCode $RootDir }
  "trae" { Install-Trae $RootDir }
  "claude" { Install-Claude $RootDir }
  "all" {
    Install-Codex $RootDir
    Install-OpenCode $RootDir
    Install-Trae $RootDir
    Install-Claude $RootDir
  }
  default { throw "unknown agent: $SelectedAgent" }
}

Write-Host "done. Open your agent in this project and ask it to use karmind-skill."

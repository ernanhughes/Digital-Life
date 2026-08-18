# scripts/artifacts.ps1
# Generates one Writer artifact JSON + Markdown report per markdown chapter.
#
# The analysis copy masks TOML/YAML front matter with blank lines so:
# - metadata is not analyzed as prose
# - source line numbers still match the original chapter
#
# Input:
#   content/books/digital-life/*.md
#
# Output:
#   .writer/artifacts/[chapter-name].json
#   .writer/artifacts/[chapter-name].md

param(
    [string]$ChaptersDir = "content/books/digital-life",
    [string]$OutputDir = ".writer/artifacts",
    [string]$VenvDir = "C:/Projects/writer/venv",
    [string]$Profile = "technical",
    [switch]$ShowJsonResponse,
    [switch]$ShowMarkdownResponse
)

$ErrorActionPreference = "Stop"

# Keep Python / console output sane on Windows.
chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Get-MaskedMarkdownForAnalysis {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $text = Get-Content -Path $Path -Raw -Encoding UTF8
    $newline = if ($text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $lines = [regex]::Split($text, "\r?\n")

    if ($lines.Count -eq 0) {
        return [pscustomobject]@{
            OriginalText     = $text
            AnalysisText     = $text
            FrontMatterLines = 0
        }
    }

    # Hugo content here uses TOML (+++), but accept YAML (---) too.
    $firstLine = $lines[0].TrimStart([char]0xFEFF).Trim()
    if ($firstLine -ne "+++" -and $firstLine -ne "---") {
        return [pscustomobject]@{
            OriginalText     = $text
            AnalysisText     = $text
            FrontMatterLines = 0
        }
    }

    $closingIndex = -1
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].Trim() -eq $firstLine) {
            $closingIndex = $i
            break
        }
    }

    if ($closingIndex -lt 0) {
        throw "Unclosed markdown front matter in: $Path"
    }

    # Blank the metadata rather than removing it. This preserves every original
    # line number used by Writer evidence snippets and issue locations.
    for ($i = 0; $i -le $closingIndex; $i++) {
        $lines[$i] = ""
    }

    return [pscustomobject]@{
        OriginalText     = $text
        AnalysisText     = ($lines -join $newline)
        FrontMatterLines = ($closingIndex + 1)
    }
}

function Restore-SourcePathInText {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$AnalysisPath,
        [Parameter(Mandatory = $true)][string]$SourcePath
    )

    $result = $Text.Replace($AnalysisPath, $SourcePath)

    # JSON escapes Windows path separators, so restore that form too.
    $escapedAnalysisPath = $AnalysisPath.Replace("\", "\\")
    $escapedSourcePath = $SourcePath.Replace("\", "\\")
    $result = $result.Replace($escapedAnalysisPath, $escapedSourcePath)

    return $result
}

$ProjectRoot = Get-Location
$ChapterPath = Join-Path $ProjectRoot $ChaptersDir
$ReportPath = Join-Path $ProjectRoot $OutputDir
$WriterCommand = Join-Path $VenvDir "Scripts\writer.exe"
$AnalysisInputDir = Join-Path $ReportPath "_analysis-input"

if (-not (Test-Path $WriterCommand)) {
    throw "Writer command not found in venv: $WriterCommand"
}

if (-not (Test-Path $ChapterPath)) {
    throw "Chapters directory not found: $ChapterPath"
}

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null
New-Item -ItemType Directory -Force -Path $AnalysisInputDir | Out-Null

$chapterFiles = Get-ChildItem -Path $ChapterPath -Filter "*.md" -File |
    Where-Object { -not $_.Name.StartsWith("00") } |
    Sort-Object Name

if ($chapterFiles.Count -eq 0) {
    Write-Warning "No markdown chapter files found in: $ChapterPath"
    exit 0
}

Write-Host "Generating artifact reports..."
Write-Host "Chapters: $ChapterPath"
Write-Host "Reports:  $ReportPath"
Write-Host "Writer:   $WriterCommand"
Write-Host "Profile:  $Profile"
Write-Host "Front matter: excluded from analysis (line numbers preserved)"
Write-Host ""

foreach ($chapter in $chapterFiles) {
    $chapterName = [System.IO.Path]::GetFileNameWithoutExtension($chapter.Name)
    $jsonFile = Join-Path $ReportPath "$chapterName.json"
    $mdFile = Join-Path $ReportPath "$chapterName.md"
    $jsonErrFile = Join-Path $ReportPath "$chapterName.json.stderr.log"
    $mdErrFile = Join-Path $ReportPath "$chapterName.md.stderr.log"
    $analysisFile = Join-Path $AnalysisInputDir $chapter.Name

    $prepared = Get-MaskedMarkdownForAnalysis -Path $chapter.FullName
    $prepared.AnalysisText | Set-Content -Path $analysisFile -Encoding UTF8 -NoNewline

    Write-Host ""
    Write-Host "Scanning $($chapter.Name)"
    Write-Host "JSON: $jsonFile"
    Write-Host "MD:   $mdFile"
    if ($prepared.FrontMatterLines -gt 0) {
        Write-Host "Front matter masked: $($prepared.FrontMatterLines) lines"
    }

    # -------------------------
    # JSON report
    # -------------------------

    $jsonArgs = @(
        "artifact",
        "analyze",
        $analysisFile,
        "--profile",
        $Profile,
        "--json"
    )

    Write-Host "JSON call:"
    Write-Host "  $WriterCommand $($jsonArgs -join ' ')"

    $rawJsonOutput = & $WriterCommand @jsonArgs 2> $jsonErrFile
    $jsonExitCode = $LASTEXITCODE

    $rawText = ($rawJsonOutput -join "`n")

    # Extract JSON object from mixed stdout.
    $jsonStart = $rawText.IndexOf("{")
    $jsonEnd = $rawText.LastIndexOf("}")

    if ($jsonStart -ge 0 -and $jsonEnd -gt $jsonStart) {
        $cleanJson = $rawText.Substring($jsonStart, $jsonEnd - $jsonStart + 1)
        $cleanJson = Restore-SourcePathInText -Text $cleanJson -AnalysisPath $analysisFile -SourcePath $chapter.FullName

        # Validate JSON before writing.
        try {
            $null = $cleanJson | ConvertFrom-Json
            $cleanJson | Set-Content -Path $jsonFile -Encoding UTF8
            Write-Host "JSON saved: $jsonFile"
        }
        catch {
            Write-Warning "Could not parse JSON for $($chapter.Name). Writing raw output log instead."
            $rawText | Set-Content -Path "$jsonFile.raw.log" -Encoding UTF8
        }
    }
    else {
        Write-Warning "No JSON object found for $($chapter.Name). Writing raw output log instead."
        $rawText | Set-Content -Path "$jsonFile.raw.log" -Encoding UTF8
    }

    if ($ShowJsonResponse) {
        Write-Host "Raw JSON command response:"
        $rawJsonOutput | ForEach-Object { Write-Host "  $_" }
    }

    # -------------------------
    # Markdown report
    # -------------------------

    $mdArgs = @(
        "artifact",
        "report",
        $analysisFile,
        "--profile",
        $Profile,
        "--output",
        $mdFile
    )

    Write-Host "Markdown call:"
    Write-Host "  $WriterCommand $($mdArgs -join ' ')"

    $mdResponse = & $WriterCommand @mdArgs 2> $mdErrFile
    $mdExitCode = $LASTEXITCODE

    if (Test-Path $mdFile) {
        $mdText = Get-Content -Path $mdFile -Raw -Encoding UTF8
        $mdText = Restore-SourcePathInText -Text $mdText -AnalysisPath $analysisFile -SourcePath $chapter.FullName
        $mdText | Set-Content -Path $mdFile -Encoding UTF8
    }

    if ($ShowMarkdownResponse) {
        if ($mdResponse) {
            Write-Host "Markdown response:"
            $mdResponse | ForEach-Object { Write-Host "  $_" }
        } else {
            Write-Host "Markdown response: <empty>"
        }
    }

    if ((Test-Path $jsonErrFile) -and ((Get-Item $jsonErrFile).Length -eq 0)) {
        Remove-Item $jsonErrFile -Force
    }

    if ((Test-Path $mdErrFile) -and ((Get-Item $mdErrFile).Length -eq 0)) {
        Remove-Item $mdErrFile -Force
    }

    if ($jsonExitCode -gt 1) {
        Write-Warning "Artifact JSON analysis may have failed on $($chapter.Name). Exit code: $jsonExitCode"
        Write-Warning "See stderr log: $jsonErrFile"
    }

    if ($mdExitCode -gt 1) {
        Write-Warning "Artifact markdown report may have failed on $($chapter.Name). Exit code: $mdExitCode"
        Write-Warning "See stderr log: $mdErrFile"
    }
}

# Analysis copies are implementation detail only.
if (Test-Path $AnalysisInputDir) {
    Remove-Item -Path $AnalysisInputDir -Recurse -Force
}

Write-Host ""
Write-Host "Done. Reports written to: $ReportPath"

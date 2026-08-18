# scripts/artifacts.ps1
# Generates one Writer artifact JSON + Markdown report per markdown chapter.
#
# Input:
#   chapters/*.md
#
# Output:
#   .writer/artifacts/[chapter-name].json
#   .writer/artifacts/[chapter-name].md

param(
    [string]$ChaptersDir = "content/books/digital-life",
    [string]$OutputDir = ".writer/artifacts",
    [string]$VenvDir = "C:/Projects/writer/venv",
    [string]$Profile = "fiction",
    [switch]$ShowJsonResponse,
    [switch]$ShowMarkdownResponse
)

$ErrorActionPreference = "Stop"

# Keep Python / console output sane on Windows.
chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$ProjectRoot = Get-Location
$ChapterPath = Join-Path $ProjectRoot $ChaptersDir
$ReportPath = Join-Path $ProjectRoot $OutputDir
$WriterCommand = Join-Path $VenvDir "Scripts\writer.exe"

if (-not (Test-Path $WriterCommand)) {
    throw "Writer command not found in venv: $WriterCommand"
}

if (-not (Test-Path $ChapterPath)) {
    throw "Chapters directory not found: $ChapterPath"
}

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null

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
Write-Host ""

foreach ($chapter in $chapterFiles) {
    $chapterName = [System.IO.Path]::GetFileNameWithoutExtension($chapter.Name)
    $jsonFile = Join-Path $ReportPath "$chapterName.json"
    $mdFile = Join-Path $ReportPath "$chapterName.md"
    $jsonErrFile = Join-Path $ReportPath "$chapterName.json.stderr.log"
    $mdErrFile = Join-Path $ReportPath "$chapterName.md.stderr.log"

    Write-Host ""
    Write-Host "Scanning $($chapter.Name)"
    Write-Host "JSON: $jsonFile"
    Write-Host "MD:   $mdFile"

    # -------------------------
    # JSON report
    # -------------------------

    $jsonArgs = @(
        "artifact",
        "analyze",
        $chapter.FullName,
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
        $chapter.FullName,
        "--profile",
        $Profile,
        "--output",
        $mdFile
    )

    Write-Host "Markdown call:"
    Write-Host "  $WriterCommand $($mdArgs -join ' ')"

    $mdResponse = & $WriterCommand @mdArgs 2> $mdErrFile
    $mdExitCode = $LASTEXITCODE

    if ($ShowMarkdownResponse) {
        if ($mdResponse) {
            Write-Host "Markdown response:"
            $mdResponse | ForEach-Object { Write-Host "  $_" }
        } else {
            Write-Host "Markdown response: <empty>"
        }
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

Write-Host ""
Write-Host "Done. Reports written to: $ReportPath"
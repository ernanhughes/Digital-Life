# scripts/book-tics.ps1
#
# Generates one Writer book-tics Markdown report and one AI review prompt per
# markdown chapter.
#
# Front matter is masked before Writer analysis so TOML/YAML metadata is never
# treated as prose while original source line numbers remain stable.
#
# Requires the Writer artifact profile `technical_book` (see technical_book.yaml).

param(
    [string]$ChaptersDir = "content/books/digital-life",
    [string]$OutputDir = ".writer/book-tics",
    [string]$PromptDir = ".writer/book-tics-prompts",
    [string]$VenvDir = "C:\Projects\writer\venv",
    [string]$Profile = "technical_book",
    [switch]$ShowResponse,
    [switch]$FailFast
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
    $escapedAnalysisPath = $AnalysisPath.Replace("\", "\\")
    $escapedSourcePath = $SourcePath.Replace("\", "\\")
    $result = $result.Replace($escapedAnalysisPath, $escapedSourcePath)
    return $result
}

$ProjectRoot = Get-Location
$ChapterPath = Join-Path $ProjectRoot $ChaptersDir
$ReportPath = Join-Path $ProjectRoot $OutputDir
$PromptPath = Join-Path $ProjectRoot $PromptDir
$WriterCommand = Join-Path $VenvDir "Scripts\writer.exe"
$AnalysisInputDir = Join-Path $ReportPath "_analysis-input"

if (-not (Test-Path $WriterCommand)) {
    throw "Writer command not found in venv: $WriterCommand"
}

if (-not (Test-Path $ChapterPath)) {
    throw "Chapters directory not found: $ChapterPath"
}

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null
New-Item -ItemType Directory -Force -Path $PromptPath | Out-Null
New-Item -ItemType Directory -Force -Path $AnalysisInputDir | Out-Null

$chapterFiles = Get-ChildItem -Path $ChapterPath -Filter "*.md" -File |
    Where-Object { -not $_.Name.StartsWith("00") } |
    Sort-Object Name

if ($chapterFiles.Count -eq 0) {
    Write-Warning "No markdown chapter files found in: $ChapterPath"
    exit 0
}

Write-Host "Generating book-tics reports and prompt files..."
Write-Host "Chapters: $ChapterPath"
Write-Host "Reports:  $ReportPath"
Write-Host "Prompts:  $PromptPath"
Write-Host "Writer:   $WriterCommand"
Write-Host "Profile:  $Profile"
Write-Host "Front matter: excluded from analysis (line numbers preserved)"
Write-Host ""

$failed = @()

foreach ($chapter in $chapterFiles) {
    $chapterName = [System.IO.Path]::GetFileNameWithoutExtension($chapter.Name)

    $mdFile = Join-Path $ReportPath "$chapterName.md"
    $promptFile = Join-Path $PromptPath "$chapterName.prompt.md"
    $errFile = Join-Path $ReportPath "$chapterName.stderr.log"
    $rawLogFile = Join-Path $ReportPath "$chapterName.raw.log"
    $analysisFile = Join-Path $AnalysisInputDir $chapter.Name

    $prepared = Get-MaskedMarkdownForAnalysis -Path $chapter.FullName
    $prepared.AnalysisText | Set-Content -Path $analysisFile -Encoding UTF8 -NoNewline

    Write-Host ""
    Write-Host "Scanning $($chapter.Name)"
    Write-Host "Report: $mdFile"
    Write-Host "Prompt: $promptFile"
    if ($prepared.FrontMatterLines -gt 0) {
        Write-Host "Front matter masked: $($prepared.FrontMatterLines) lines"
    }

    $args = @(
        "artifact",
        "book-tics",
        $analysisFile,
        "--profile",
        $Profile,
        "-o",
        $mdFile
    )

    Write-Host "Book-tics call:"
    Write-Host "  $WriterCommand $($args -join ' ')"

    $response = & $WriterCommand @args 2> $errFile
    $exitCode = $LASTEXITCODE

    if ($ShowResponse) {
        if ($response) {
            Write-Host "Response:"
            $response | ForEach-Object { Write-Host "  $_" }
        } else {
            Write-Host "Response: <empty>"
        }
    }

    if ((Test-Path $errFile) -and ((Get-Item $errFile).Length -eq 0)) {
        Remove-Item $errFile -Force
    }

    if ($response) {
        $responseText = ($response -join "`n")
        $responseText = Restore-SourcePathInText -Text $responseText -AnalysisPath $analysisFile -SourcePath $chapter.FullName
        $responseText | Set-Content -Path $rawLogFile -Encoding UTF8
    } elseif (Test-Path $rawLogFile) {
        Remove-Item $rawLogFile -Force
    }

    if (-not (Test-Path $mdFile)) {
        Write-Warning "Book-tics report was not created for $($chapter.Name): $mdFile"
        $failed += $chapter.Name

        if ($FailFast) {
            throw "Book-tics failed before creating output for $($chapter.Name)"
        }

        continue
    }

    # Restore the real source path in the report after using the masked copy.
    $bookTicsReport = Get-Content -Path $mdFile -Raw -Encoding UTF8
    $bookTicsReport = Restore-SourcePathInText -Text $bookTicsReport -AnalysisPath $analysisFile -SourcePath $chapter.FullName
    $bookTicsReport | Set-Content -Path $mdFile -Encoding UTF8

    if ($exitCode -gt 1) {
        Write-Warning "Book-tics may have failed on $($chapter.Name). Exit code: $exitCode"
        Write-Warning "See stderr log: $errFile"
        $failed += $chapter.Name

        if ($FailFast) {
            throw "Book-tics failed on $($chapter.Name). Exit code: $exitCode"
        }
    }

    # -------------------------
    # Prompt file
    # -------------------------
    # The report is based on body text only. The prompt includes the original
    # chapter so front matter can be preserved exactly if a revised file is produced.

    $chapterText = $prepared.OriginalText

    $promptText = @"
# Review the Book Tics report against this Digital Life chapter

You are editing a chapter from *Digital Life From First Principles*, a hard-science / scientific-investigation book.

## Goal

Improve the reading experience without optimizing for detector scores.

Use the Book Tics Report as a heat map, not a checklist. A detected tic is evidence that a passage deserves inspection; it is not an instruction to rewrite it.

## Review method

1. Read the chapter as prose first.
2. Use the report to locate repeated or over-patterned passages.
3. Edit only where the repetition genuinely weakens rhythm, emphasis, clarity, or argument.
4. Protect deliberate scientific repetition, terminology, methodological contrast, and strong rhetorical lines.
5. Prefer deleting redundant repetition or redistributing paragraph rhythm over mechanically rephrasing every detected pattern.

## Editing rules

* Preserve scientific meaning, claim strength, experimental terminology, controls, measurements, and uncertainty.
* Preserve the chapter's argument, section structure, and authorial voice.
* Do not perform a broad rewrite.
* Do not try to remove every tic.
* Do not optimize for an artifact/tic score.
* Do not add dialogue, scene-setting, sensory detail, or fiction techniques merely to satisfy a detector.
* Front matter is metadata, not prose. Preserve the TOML/YAML front matter exactly and do not edit it in response to the report.
* Keep intentional short paragraphs and parallel constructions when they genuinely earn their emphasis.
* When several detections point to the same passage, treat that as one cadence problem and revise the passage once.
* Return the corrected chapter in full, with the original front matter preserved exactly.
* Do not include explanation before or after the corrected chapter.

## Chapter File

$($chapter.FullName)

---

# Book Tics Report

<BOOK_TICS_REPORT>
$bookTicsReport
</BOOK_TICS_REPORT>

---

# Chapter Text

<CHAPTER_TEXT>
$chapterText
</CHAPTER_TEXT>
"@

    $promptText | Set-Content -Path $promptFile -Encoding UTF8

    Write-Host "Book-tics saved: $mdFile"
    Write-Host "Prompt saved:    $promptFile"
}

if (Test-Path $AnalysisInputDir) {
    Remove-Item -Path $AnalysisInputDir -Recurse -Force
}

Write-Host ""
Write-Host "Done."
Write-Host "Book-tics reports written to: $ReportPath"
Write-Host "Prompt files written to:      $PromptPath"

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Warning "Some chapters had warnings/failures:"
    $failed | ForEach-Object { Write-Warning "  $_" }
    exit 1
}

exit 0

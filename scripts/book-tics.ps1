# scripts/book-tics.ps1

# Generates one Writer book-tics Markdown report and one AI prompt file per markdown chapter.

#

# Input:

# chapters/*.md

#

# Output:

# .writer/book-tics/[chapter-name].md

# .writer/book-tics-prompts/[chapter-name].prompt.md

# .writer/book-tics/[chapter-name].stderr.log if errors occur

param(
[string]$ChaptersDir = "chapters",
[string]$OutputDir = ".writer/book-tics",
[string]$PromptDir = ".writer/book-tics-prompts",
[string]$VenvDir = "C:\Projects\writer\venv",
[switch]$ShowResponse,
[switch]$FailFast
)

$ErrorActionPreference = "Stop"

# Keep Python / console output sane on Windows.

chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$ProjectRoot = Get-Location
$ChapterPath = Join-Path $ProjectRoot $ChaptersDir
$ReportPath = Join-Path $ProjectRoot $OutputDir
$PromptPath = Join-Path $ProjectRoot $PromptDir
$WriterCommand = Join-Path $VenvDir "Scripts\writer.exe"

if (-not (Test-Path $WriterCommand)) {
throw "Writer command not found in venv: $WriterCommand"
}

if (-not (Test-Path $ChapterPath)) {
throw "Chapters directory not found: $ChapterPath"
}

New-Item -ItemType Directory -Force -Path $ReportPath | Out-Null
New-Item -ItemType Directory -Force -Path $PromptPath | Out-Null

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
Write-Host ""

$failed = @()

foreach ($chapter in $chapterFiles) {
$chapterName = [System.IO.Path]::GetFileNameWithoutExtension($chapter.Name)


$mdFile = Join-Path $ReportPath "$chapterName.md"
$promptFile = Join-Path $PromptPath "$chapterName.prompt.md"
$errFile = Join-Path $ReportPath "$chapterName.stderr.log"
$rawLogFile = Join-Path $ReportPath "$chapterName.raw.log"

Write-Host ""
Write-Host "Scanning $($chapter.Name)"
Write-Host "Report: $mdFile"
Write-Host "Prompt: $promptFile"

$args = @(
    "artifact",
    "book-tics",
    $chapter.FullName,
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

$bookTicsReport = Get-Content -Path $mdFile -Raw -Encoding UTF8
$chapterText = Get-Content -Path $chapter.FullName -Raw -Encoding UTF8

$promptText = @"


# Please review these book tics and fix them in the associated chapter file

You are editing a single chapter from *Latent*.

## Task

Use the Book Tics Report below to surgically remove visible prose tics from the chapter.

Prioritize:

* overused prose frames such as "that was...", "not because...", "for a moment...", "it did not need to..."
* repeated gestures, repeated looking beats, and repeated dialogue responses
* exact duplicate or near-duplicate sentences
* process debris, TODO markers, accidental review residue, or manuscript artifacts
* local repetition that weakens prose or makes the author's hand visible

## Editing Rules

* Preserve the plot, continuity, character intention, chapter structure, and ending.
* Do not perform a broad rewrite.
* Do not remove intentional motifs unless they are clearly accidental or weakened by overuse.
* Keep the voice cold, precise, financial, procedural, literary, and ominous.
* Prefer surgical line edits over paragraph replacement.
* Maintain all important system logs, code blocks, chapter-specific terminology, and named entities.
* Return the corrected chapter in full.
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

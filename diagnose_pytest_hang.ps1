<#
===============================================================================
 MERCURY-AI V1 — PYTEST HANG / TIMEOUT FORENSIC DIAGNOSTIC
===============================================================================

 OBJETIVO
 --------
 Descobrir por que a execução ampla do pytest não conclui.

 ESTE SCRIPT:
   [OK] NÃO altera código de produção
   [OK] NÃO altera testes
   [OK] NÃO instala dependências
   [OK] NÃO mata processos arbitrariamente
   [OK] Cria logs e artefatos forenses
   [OK] Executa pytest com saída verbosa
   [OK] Detecta último teste iniciado/concluído
   [OK] Mede duração total
   [OK] Detecta timeout
   [OK] Extrai testes lentos
   [OK] Permite reproduzir o último teste isoladamente
   [OK] Gera relatório final

 USO:
   .\diagnose_pytest_hang.ps1

 OU:

   powershell -ExecutionPolicy Bypass -File `
       C:\Projetos\Mercury-AI\diagnose_pytest_hang.ps1

===============================================================================
#>

[CmdletBinding()]
param(
    [string]$ProjectRoot = "C:\Projetos\Mercury-AI",

    # Tempo máximo da execução completa.
    [int]$TimeoutSeconds = 1800,

    # Executa novamente o último teste detectado.
    [switch]$ReproduceLastTest,

    # Executa pytest somente em tests/
    [switch]$TestsOnly,

    # Mantém a saída do pytest visível em tempo real.
    [bool]$LiveOutput = $true
)

$ErrorActionPreference = "Stop"

# =============================================================================
# 1. VALIDAÇÃO INICIAL
# =============================================================================

function Write-Banner {
    param([string]$Text)

    Write-Host ""
    Write-Host ("=" * 79) -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host ("=" * 79) -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Text)
    Write-Host "[STEP] $Text" -ForegroundColor Yellow
}

function Write-Ok {
    param([string]$Text)
    Write-Host "[ OK ] $Text" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Text)
    Write-Host "[WARN] $Text" -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Text)
    Write-Host "[FAIL] $Text" -ForegroundColor Red
}

Write-Banner "MERCURY-AI V1 — PYTEST FORENSIC DIAGNOSTIC"

if (-not (Test-Path $ProjectRoot)) {
    throw "Projeto não encontrado: $ProjectRoot"
}

Set-Location $ProjectRoot

Write-Ok "Root encontrado: $ProjectRoot"

# =============================================================================
# 2. DIRETÓRIO DE ARTEFATOS
# =============================================================================

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

$ArtifactRoot = Join-Path $ProjectRoot "artifacts\pytest_forensics\$Timestamp"

New-Item `
    -ItemType Directory `
    -Path $ArtifactRoot `
    -Force | Out-Null

Write-Ok "Diretório de artefatos:"
Write-Host "      $ArtifactRoot"

$MainLog        = Join-Path $ArtifactRoot "pytest_output.log"
$MetadataLog    = Join-Path $ArtifactRoot "metadata.txt"
$ReportFile     = Join-Path $ArtifactRoot "FORENSIC_REPORT.txt"
$LastTestFile   = Join-Path $ArtifactRoot "last_test.txt"
$SlowTestsFile  = Join-Path $ArtifactRoot "slow_tests.txt"
$ProcessFile    = Join-Path $ArtifactRoot "process_snapshot.txt"
$ExitCodeFile   = Join-Path $ArtifactRoot "exit_code.txt"
$SummaryFile    = Join-Path $ArtifactRoot "summary.json"

# =============================================================================
# 3. METADATA DO AMBIENTE
# =============================================================================

Write-Step "Coletando metadata do ambiente..."

$metadata = @()

$metadata += "MERCURY-AI V1 — PYTEST FORENSIC DIAGNOSTIC"
$metadata += ""
$metadata += "TIMESTAMP: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$metadata += "ROOT: $ProjectRoot"
$metadata += "COMPUTER: $env:COMPUTERNAME"
$metadata += "USER: $env:USERNAME"
$metadata += ""

$metadata += "=== POWERSHELL ==="
$metadata += $PSVersionTable | Out-String

$metadata += "=== PYTHON ==="
try {
    $metadata += (& python --version 2>&1 | Out-String)
}
catch {
    $metadata += "python --version FAILED"
}

$metadata += "=== PYTEST ==="
try {
    $metadata += (& python -m pytest --version 2>&1 | Out-String)
}
catch {
    $metadata += "pytest --version FAILED"
}

$metadata += "=== GIT STATUS ==="
try {
    $metadata += (& git status --short 2>&1 | Out-String)
}
catch {
    $metadata += "git status unavailable"
}

$metadata | Set-Content `
    -Path $MetadataLog `
    -Encoding UTF8

Write-Ok "Metadata registrada."

# =============================================================================
# 4. SNAPSHOT DE PROCESSOS
# =============================================================================

function Save-ProcessSnapshot {
    param(
        [string]$Path
    )

    @(
        "PROCESS SNAPSHOT"
        "TIME: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        ""
        "=== PYTHON / PYTEST PROCESSES ==="
    ) | Set-Content $Path -Encoding UTF8

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.Name -match "python|pytest"
        } |
        Select-Object `
            ProcessId,
            ParentProcessId,
            Name,
            CommandLine |
        Format-List |
        Out-File `
            -FilePath $Path `
            -Append `
            -Encoding utf8

    Add-Content `
        -Path $Path `
        -Value "`n=== GENERAL PROCESS TOP 50 ==="

    Get-Process |
        Sort-Object CPU -Descending |
        Select-Object -First 50 `
            Id,
            ProcessName,
            CPU,
            WorkingSet64,
            StartTime |
        Format-Table -AutoSize |
        Out-File `
            -FilePath $Path `
            -Append `
            -Encoding utf8
}

Save-ProcessSnapshot -Path $ProcessFile

Write-Ok "Snapshot inicial de processos salvo."

# =============================================================================
# 5. CONSTRUÇÃO DO COMANDO PYTEST
# =============================================================================

Write-Step "Montando comando pytest..."

$PytestArgs = @(
    "-m"
    "pytest"
    "-vv"
    "-ra"
    "--durations=50"
)

if ($TestsOnly) {
    $PytestArgs += "tests"
}

Write-Host ""
Write-Host "COMMAND:" -ForegroundColor Cyan
Write-Host "python $($PytestArgs -join ' ')"
Write-Host ""

# =============================================================================
# 6. EXECUÇÃO CONTROLADA
# =============================================================================

Write-Step "Iniciando pytest..."

$StartTime = Get-Date

$script:LastInterestingLine = $null
$script:LastNodeId = $null
$script:TestCountSeen = 0

function Inspect-PytestLine {
    param(
        [string]$Line
    )

    if ([string]::IsNullOrWhiteSpace($Line)) {
        return
    }

    # Armazena linhas com aparência de nodeid de teste.
    #
    # Exemplos:
    # tests/test_x.py::test_y PASSED
    # tests/test_x.py::TestClass::test_y RUNNING

    if ($Line -match "([^\s]+::[^\s]+)") {
        $node = $Matches[1]

        $script:LastNodeId = $node
        $script:LastInterestingLine = $Line
        $script:TestCountSeen++
    }

    # Também captura collection / progress lines.
    if ($Line -match "PASSED|FAILED|ERROR|RUNNING|::") {
        $script:LastInterestingLine = $Line
    }
}

# -------------------------------------------------------------------------
# EXECUÇÃO COM REDIRECIONAMENTO PARA ARQUIVO + POLLING
#
# IMPORTANTE: NÃO usamos RedirectStandardOutput + ReadLine() porque o
# ReadLine() bloqueia indefinidamente quando o processo não produz saída,
# impedindo o check de timeout. Em vez disso, redirecionamos a saída para
# arquivos e fazemos polling do arquivo + do estado do processo.
# -------------------------------------------------------------------------

$StderrLog = Join-Path $ArtifactRoot "pytest_stderr.log"

$process = Start-Process `
    -FilePath "python" `
    -ArgumentList $PytestArgs `
    -WorkingDirectory $ProjectRoot `
    -RedirectStandardOutput $MainLog `
    -RedirectStandardError $StderrLog `
    -NoNewWindow `
    -PassThru

Write-Ok "pytest iniciado. PID=$($process.Id)"

$timeoutTriggered = $false
$lastLogSize = 0

while ($true) {

    $elapsed = ((Get-Date) - $StartTime).TotalSeconds

    # -------------------------------------------------------------------------
    # TIMEOUT
    # -------------------------------------------------------------------------

    if ($elapsed -ge $TimeoutSeconds -and -not $process.HasExited) {

        $timeoutTriggered = $true

        Write-Warn "TIMEOUT atingido: $TimeoutSeconds segundos"

        # 1) Encerra o processo travado PRIMEIRO (libera o lock do log).
        try {
            Stop-Process -Id $process.Id -Force -ErrorAction Stop
            Write-Warn "Processo pytest (PID $($process.Id)) encerrado por timeout."
        }
        catch {
            Write-Warn "Não foi possível encerrar o processo: $($_.Exception.Message)"
        }

        # 2) Anotações forenses em arquivo SEPARADO (o MainLog pode estar
        #    bloqueado pelo processo recém-encerrado).
        $ForensicFile = Join-Path $ArtifactRoot "forensic_timeout.txt"

        @(
            "[FORENSIC TIMEOUT] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            "[FORENSIC LAST NODEID] $script:LastNodeId"
            "[FORENSIC LAST LINE] $script:LastInterestingLine"
        ) | Set-Content -Path $ForensicFile -Encoding UTF8

        Save-ProcessSnapshot -Path (
            Join-Path $ArtifactRoot "process_snapshot_timeout.txt"
        )

        break
    }

    # -------------------------------------------------------------------------
    # POLLING DO LOG (novas linhas)
    # -------------------------------------------------------------------------

    if (Test-Path $MainLog) {

        $currentSize = (Get-Item $MainLog).Length

        if ($currentSize -gt $lastLogSize) {

            $newLines = Get-Content $MainLog -Tail 200

            foreach ($line in $newLines) {
                Inspect-PytestLine -Line $line
            }

            if ($LiveOutput) {
                Get-Content $MainLog -Tail 200 | ForEach-Object { Write-Host $_ }
            }

            $lastLogSize = $currentSize
        }
    }

    # -------------------------------------------------------------------------
    # STDERR (novas linhas)
    # -------------------------------------------------------------------------

    if (Test-Path $StderrLog) {

        $stderrContent = Get-Content $StderrLog -Raw -ErrorAction SilentlyContinue

        if (-not [string]::IsNullOrWhiteSpace($stderrContent)) {

            if ($LiveOutput) {
                Write-Host "[STDERR]" -ForegroundColor Red
                Write-Host $stderrContent -ForegroundColor Red
            }

            # Limpa o arquivo para não repetir.
            Set-Content -Path $StderrLog -Value "" -Encoding UTF8
        }
    }

    if ($process.HasExited) {
        break
    }

    Start-Sleep -Milliseconds 500
}

# =============================================================================
# 7. FINALIZAÇÃO
# =============================================================================

$EndTime = Get-Date

$Duration = ($EndTime - $StartTime).TotalSeconds

if (-not $timeoutTriggered) {

    # Aguarda processo terminar completamente.
    $process.WaitForExit()

    $ExitCode = $process.ExitCode
}
else {
    $ExitCode = $null
}

@"
PYTEST FORENSIC EXECUTION

START:
$StartTime

END:
$EndTime

DURATION_SECONDS:
$Duration

TIMEOUT:
$timeoutTriggered

EXIT_CODE:
$ExitCode

LAST_NODEID:
$script:LastNodeId

LAST_INTERESTING_LINE:
$script:LastInterestingLine
"@ | Set-Content `
        -Path $ExitCodeFile `
        -Encoding UTF8

if ($script:LastNodeId) {
    $script:LastNodeId |
        Set-Content `
            -Path $LastTestFile `
            -Encoding UTF8
}

Write-Host ""

if ($timeoutTriggered) {

    Write-Warn "Execução terminou como INCONCLUSIVA por timeout."

    Write-Host ""
    Write-Host "ÚLTIMO TESTE DETECTADO:" -ForegroundColor Yellow
    Write-Host "    $script:LastNodeId"

    Write-Host ""
    Write-Host "ÚLTIMA LINHA RELEVANTE:" -ForegroundColor Yellow
    Write-Host "    $script:LastInterestingLine"
}
else {

    if ($ExitCode -eq 0) {
        Write-Ok "pytest terminou com sucesso."
    }
    else {
        Write-Fail "pytest terminou com exit code $ExitCode"
    }
}

# =============================================================================
# 8. EXTRAÇÃO DOS TESTES LENTOS
# =============================================================================

Write-Step "Extraindo testes lentos..."

$slowSectionFound = $false
$slowLines = New-Object System.Collections.Generic.List[string]

if (Test-Path $MainLog) {

    $lines = Get-Content $MainLog

    foreach ($line in $lines) {

        if ($line -match "slowest durations") {
            $slowSectionFound = $true
        }

        if ($slowSectionFound) {

            $slowLines.Add($line)

            # Depois de um limite razoável, para.
            if ($slowLines.Count -gt 80) {
                break
            }
        }
    }
}

if ($slowLines.Count -gt 0) {

    $slowLines |
        Set-Content `
            -Path $SlowTestsFile `
            -Encoding UTF8

    Write-Ok "Seção de testes lentos encontrada."
}
else {

    @"
Nenhuma seção completa de --durations encontrada.

Possíveis motivos:

1. pytest foi interrompido antes de terminar.
2. ocorreu timeout.
3. a execução travou antes do resumo final.
4. pytest não alcançou a fase de reporting.
"@ | Set-Content `
        -Path $SlowTestsFile `
        -Encoding UTF8

    Write-Warn "Não foi possível obter a tabela completa de testes lentos."
}

# =============================================================================
# 9. REPRODUÇÃO DO ÚLTIMO TESTE
# =============================================================================

$ReproductionResult = "NOT REQUESTED"

if ($ReproduceLastTest) {

    Write-Banner "REPRODUÇÃO DO ÚLTIMO TESTE"

    if ([string]::IsNullOrWhiteSpace($script:LastNodeId)) {

        Write-Warn "Nenhum nodeid foi detectado. Reprodução ignorada."

        $ReproductionResult = "NO NODEID"
    }
    else {

        Write-Host ""
        Write-Host "Executando isoladamente:"
        Write-Host ""
        Write-Host "python -m pytest `"$script:LastNodeId`" -vv -s"
        Write-Host ""

        $ReproStart = Get-Date

        & python -m pytest `
            $script:LastNodeId `
            "-vv" `
            "-s" `
            "--durations=10"

        $ReproExitCode = $LASTEXITCODE

        $ReproDuration = ((Get-Date) - $ReproStart).TotalSeconds

        if ($ReproExitCode -eq 0) {

            $ReproductionResult =
                "PASS isolated in $ReproDuration seconds"

            Write-Ok "Último teste passou isoladamente."
        }
        else {

            $ReproductionResult =
                "FAIL exit=$ReproExitCode duration=$ReproDuration"

            Write-Fail "Último teste falhou isoladamente."
        }
    }
}

# =============================================================================
# 10. CLASSIFICAÇÃO FORENSE
# =============================================================================

$Classification = @()

if ($timeoutTriggered) {

    $Classification +=
        "SUITE_STATUS: INCONCLUSIVE_TIMEOUT"

    if ($script:LastNodeId) {

        $Classification +=
            "SUSPECTED_BOUNDARY_TEST: $script:LastNodeId"

        $Classification +=
            "IMPORTANT: o último teste exibido não é automaticamente o culpado."

        $Classification +=
            "O travamento pode ocorrer:"
        $Classification +=
            "- dentro do teste"
        $Classification +=
            "- durante teardown"
        $Classification +=
            "- em fixture posterior"
        $Classification +=
            "- em processo/thread filho"
        $Classification +=
            "- após o teste exibido"
    }
}
elseif ($ExitCode -eq 0) {

    $Classification +=
        "SUITE_STATUS: PASS"
}
else {

    $Classification +=
        "SUITE_STATUS: FAILED"

    $Classification +=
        "INSPECT pytest_output.log para failures."
}

if ($ReproduceLastTest -and
    $ReproductionResult -match "^PASS") {

    $Classification +=
        "ISOLATED_LAST_TEST: PASS"

    $Classification +=
        "POSSIBLE_INTERACTION_BUG: YES"

    $Classification +=
        "NEXT HYPOTHESIS: problema depende da ordem ou estado acumulado."
}

# =============================================================================
# 11. RELATÓRIO FINAL
# =============================================================================

$Verdict = "UNKNOWN"

if ($timeoutTriggered) {

    $Verdict = "INCONCLUSIVE — PYTEST TIMEOUT / HANG NOT YET LOCALIZED"
}
elseif ($ExitCode -eq 0) {

    $Verdict = "PASS — PYTEST EXECUTION COMPLETED"
}
else {

    $Verdict = "FAIL — PYTEST REPORTED FAILURES"
}

$report = @()

$report += "==============================================================================="
$report += "MERCURY-AI V1 — PYTEST FORENSIC DIAGNOSTIC REPORT"
$report += "==============================================================================="
$report += ""

$report += "TIMESTAMP"
$report += "---------"
$report += "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$report += ""

$report += "ROOT"
$report += "----"
$report += $ProjectRoot
$report += ""

$report += "EXECUTION"
$report += "---------"
$report += "START: $StartTime"
$report += "END: $EndTime"
$report += ("DURATION_SECONDS: {0:N2}" -f $Duration)
$report += "TIMEOUT_LIMIT: $TimeoutSeconds"
$report += "TIMEOUT_TRIGGERED: $timeoutTriggered"
$report += "EXIT_CODE: $ExitCode"
$report += ""

$report += "LAST OBSERVED TEST"
$report += "------------------"
$report += "$script:LastNodeId"
$report += ""

$report += "LAST INTERESTING OUTPUT"
$report += "-----------------------"
$report += "$script:LastInterestingLine"
$report += ""

$report += "REPRODUCTION"
$report += "------------"
$report += $ReproductionResult
$report += ""

$report += "FORENSIC CLASSIFICATION"
$report += "----------------------"
$report += $Classification
$report += ""

$report += "FINAL VERDICT"
$report += "-------------"
$report += $Verdict
$report += ""

$report += "ARTIFACTS"
$report += "---------"
$report += "MAIN LOG: $MainLog"
$report += "METADATA: $MetadataLog"
$report += "LAST TEST: $LastTestFile"
$report += "SLOW TESTS: $SlowTestsFile"
$report += "PROCESS SNAPSHOT: $ProcessFile"
$report += "EXECUTION INFO: $ExitCodeFile"
$report += ""

$report += "IMPORTANT INTERPRETATION"
$report += "------------------------"
$report += "PASS of focused resolver tests does not prove the entire pytest suite."
$report += "A timeout does not prove a functional failure."
$report += "The timeout boundary must be isolated before declaring the full suite closed."

$report |
    Set-Content `
        -Path $ReportFile `
        -Encoding UTF8

# =============================================================================
# 12. JSON SUMMARY
# =============================================================================

$summary = [PSCustomObject]@{
    timestamp             = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    root                  = $ProjectRoot
    duration_seconds      = [Math]::Round($Duration, 2)
    timeout_seconds       = $TimeoutSeconds
    timeout_triggered     = $timeoutTriggered
    exit_code             = $ExitCode
    last_nodeid           = $script:LastNodeId
    last_interesting_line = $script:LastInterestingLine
    reproduction          = $ReproductionResult
    verdict               = $Verdict
    artifacts             = @{
        main_log       = $MainLog
        metadata       = $MetadataLog
        report         = $ReportFile
        last_test      = $LastTestFile
        slow_tests     = $SlowTestsFile
        process        = $ProcessFile
    }
}

$summary |
    ConvertTo-Json -Depth 5 |
    Set-Content `
        -Path $SummaryFile `
        -Encoding UTF8

# =============================================================================
# 13. RESULTADO NO CONSOLE
# =============================================================================

Write-Banner "FORENSIC RESULT"

Write-Host ""
Write-Host "VERDICT:" -ForegroundColor Cyan
Write-Host "  $Verdict"

Write-Host ""
Write-Host "LAST NODEID:" -ForegroundColor Cyan
Write-Host "  $script:LastNodeId"

Write-Host ""
Write-Host "DURATION:" -ForegroundColor Cyan
Write-Host ("  {0:N2} seconds" -f $Duration)

Write-Host ""
Write-Host "ARTIFACT DIRECTORY:" -ForegroundColor Cyan
Write-Host "  $ArtifactRoot"

Write-Host ""
Write-Host "FINAL REPORT:" -ForegroundColor Cyan
Write-Host "  $ReportFile"

Write-Host ""

# =============================================================================
# EXIT CODE
# =============================================================================

if ($timeoutTriggered) {
    exit 124
}

if ($ExitCode -eq 0) {
    exit 0
}

exit $ExitCode
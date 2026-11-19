param([string]$PythonExe = "python")

$ErrorActionPreference = "Stop"
$auditScript = Join-Path $PSScriptRoot "audit_images.py"
& $PythonExe $auditScript
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

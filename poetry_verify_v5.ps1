param([string]$ProjectRoot = (Get-Location).Path)

$ErrorActionPreference = 'Stop'

Write-Host ''
Write-Host '== Poetry: prepare .venv ==' -ForegroundColor Cyan
$venv = Join-Path $ProjectRoot '.venv'
if (-not (Test-Path $venv)) { python -m venv $venv }
$act = Join-Path $venv 'Scripts\Activate.ps1'
if (-not (Test-Path $act)) { Write-Host 'FAIL - Activate.ps1 missing' -ForegroundColor Red; exit 1 }
. $act
python -V | Out-Host

Write-Host '== Poetry: install ==' -ForegroundColor Cyan
python -m pip install -U pip | Out-Host
python -m pip install poetry | Out-Host
$poetry = Join-Path $venv 'Scripts\poetry.exe'
if (-not (Test-Path $poetry)) { $poetry = 'poetry' }
& $poetry --version | Out-Host

Write-Host '== Poetry: use current venv ==' -ForegroundColor Cyan
& $poetry config virtualenvs.create false --local | Out-Host

Write-Host '== Poetry: check + lock ==' -ForegroundColor Cyan
$py = Join-Path $ProjectRoot 'pyproject.toml'
if (-not (Test-Path $py)) { Write-Host 'FAIL - pyproject.toml missing' -ForegroundColor Red; exit 1 }
& $poetry check | Out-Host
& $poetry lock | Out-Host
if (-not (Test-Path (Join-Path $ProjectRoot 'poetry.lock'))) { Write-Host 'FAIL - poetry.lock not generated' -ForegroundColor Red; exit 1 }
Write-Host 'OK   - poetry.lock created' -ForegroundColor Green

Write-Host '== Poetry: install deps ==' -ForegroundColor Cyan
& $poetry install | Out-Host

Write-Host '== Poetry: smoke test ==' -ForegroundColor Cyan
$smoke = Join-Path $ProjectRoot '._poetry_smoke.py'
Set-Content -Encoding UTF8 -Path $smoke -Value @(
'import django, rest_framework',
'print("django", django.get_version())',
'print("drf OK")'
)
& $poetry run python $smoke | Out-Host
Remove-Item $smoke -ErrorAction SilentlyContinue

Write-Host '== Poetry: django check/migrate/test ==' -ForegroundColor Cyan
& $poetry run python manage.py check | Out-Host
& $poetry run python manage.py migrate --noinput | Out-Host
& $poetry run python manage.py test portfolio -v 2
if ($LASTEXITCODE -ne 0) { Write-Host 'FAIL - tests failed via Poetry' -ForegroundColor Red; exit 1 }

Write-Host '== Poetry: E2E (optional) ==' -ForegroundColor Cyan
$e2e = Join-Path $ProjectRoot 'ebac_final_check.py'
if (Test-Path $e2e) {
  & $poetry run python $e2e
  if ($LASTEXITCODE -ne 0) { Write-Host 'FAIL - ebac_final_check failed via Poetry' -ForegroundColor Red; exit 1 }
} else {
  Write-Host 'ebac_final_check.py not found - skipping E2E' -ForegroundColor Yellow
}

Write-Host 'All good with Poetry.' -ForegroundColor Green
exit 0

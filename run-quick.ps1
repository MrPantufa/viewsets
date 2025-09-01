param([string]$Py = "python")
& $Py ".\ebac_final_check.py"
exit $LASTEXITCODE

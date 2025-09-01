# EBAC Fix Bundle

Este pacote contém:
- `ebac_final_check.py` — verificador completo (migrate, check, tests, endpoints e E2E).
- `run-quick.ps1` — wrapper simples para Windows PowerShell.
- `portfolio/models.py` e `portfolio/serializers.py` corrigidos (sem `...`).
- `portfolio/views` modularizado (por domínio).
- `pyproject.toml` para Poetry.

## Uso
1. Extraia os arquivos sobre o seu projeto (na raiz onde está `manage.py`).
2. Execute:
   ```powershell
   python ebac_final_check.py
   ```
3. Corrija qualquer item que o script reporte.

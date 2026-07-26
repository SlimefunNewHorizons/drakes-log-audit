# Drakes Log Audit

Auditoría reproducible para logs de Minecraft/Paper: descarga artefactos desde
Pterodactyl, agrupa errores y avisos, identifica TPS, crashes y mensajes de
jugadores que reportan bugs, lag o funciones que no operan.

Los logs, reportes y secretos están ignorados por Git.

## Uso

```powershell
python .\drakes_log_audit.py collect `
  --base-url https://panel.example.com `
  --server-id SERVER_ID `
  --key-file C:\ruta\.pterodactyl_key `
  --since 2026-07-22 `
  --output .\logs\2026-07-22

python .\drakes_log_audit.py analyze `
  --input .\logs\2026-07-22 `
  --report .\reports\audit-2026-07-22.md `
  --json .\reports\audit-2026-07-22.json
```

`collect` solo descarga `/logs` y `/crash-reports` modificados desde la fecha
indicada. `analyze` soporta `.log`, `.txt` y `.gz`.


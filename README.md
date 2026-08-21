<p align="center">
  <img src="https://raw.githubusercontent.com/DrakesCraft-Labs/drakes-log-audit/main/banner.svg" width="100%" alt="Drakes Log Audit animated banner" />
</p>

# Drakes Log Audit

> ### 🏰 ¡Únete a la Comunidad Oficial de DrakesCraft!
> 
> * 🎮 **IP del Servidor**: `play.drakescraft.cl` *(Java 1.21.11 & Bedrock)*
> * 💬 **Discord Oficial**: [discord.gg/drakescraft](https://discord.gg/rR7FbfCt9Y)
> * 🌐 **Web & Guía**: [web.drakescraft.cl](https://web.drakescraft.cl) — 🛒 **Tienda**: [web.drakescraft.cl/store](https://web.drakescraft.cl/store.html)
> 
> *¡Juega con este addon y más de 80 expansiones optimizadas en vivo en nuestra network de supervivencia técnica!*

---

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


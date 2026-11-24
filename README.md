<!-- credits:start -->
> **Credits & license.** Port and maintenance by [JackStar6677-1](https://github.com/JackStar6677-1) and [DrakesCraft Labs](https://github.com/SlimefunNewHorizons). Original authors: original work by [JackStar6677-1](https://github.com/JackStar6677-1). Upstream license: **GNU General Public License v3.0** (see [LICENSE](LICENSE)). Details: [docs/UPSTREAM_ATTRIBUTION.md](docs/UPSTREAM_ATTRIBUTION.md) · Policy: [Rights & Attribution](https://github.com/SlimefunNewHorizons/.github/blob/main/RIGHTS_AND_ATTRIBUTION.md). Independent community project, not affiliated with or endorsed by the original authors or the official Slimefun team.
>
> **Créditos y licencia.** Port y mantenimiento por [JackStar6677-1](https://github.com/JackStar6677-1) y [DrakesCraft Labs](https://github.com/SlimefunNewHorizons). Autores originales: obra original de [JackStar6677-1](https://github.com/JackStar6677-1). Licencia original: **GNU General Public License v3.0**. Detalle en [docs/UPSTREAM_ATTRIBUTION.md](docs/UPSTREAM_ATTRIBUTION.md).
<!-- credits:end -->

<p align="center">
  <img src="https://raw.githubusercontent.com/SlimefunNewHorizons/drakes-log-audit/main/banner.svg" width="100%" alt="Drakes Log Audit animated banner" />
</p>

# Drakes Log Audit

> ### 🏰 ¡Únete a la Comunidad Oficial de DrakesCraft!
> 
> * 🎮 **IP del Servidor**: `mc.drakescraft.cl` *(Java 1.21.11 & Bedrock)*
> * 💬 **Discord Oficial**: [discord.gg/drakescraft](https://discord.gg/rv3vtXZTk7)
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

---

## 📄 License & Upstream Attribution

This project is a sovereign fork maintained by [**JackStar6677-1**](https://github.com/JackStar6677-1) under [**DrakesCraft Labs**](https://github.com/SlimefunNewHorizons).

- **Original Project:** Created by the upstream authors and the open-source community.
- **DrakesCraft Optimizations:** Modernized for Paper/Purpur 1.21.11+, Java 21, high concurrency, asynchronous safety, and exploit/duplication prevention.
- **License:** Distributed under the original **GNU General Public License v3.0 (GPLv3)** (or original upstream license). See the [LICENSE](LICENSE) file for complete terms.

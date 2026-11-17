# 🛡️ Modo atacante · skill para Claude Code

**La misma IA que puede atacar tu proyecto también puede protegerlo.**

`modo-atacante` es una skill para [Claude Code](https://claude.com/claude-code) que revisa tu proyecto como lo haría un atacante. Te devuelve un informe con:

- 🔴 **Puntos débiles**: dónde está cada fallo (`archivo:línea`), cómo lo aprovecharía un atacante, su gravedad y cómo arreglarlo.
- 🟢 **Puntos fuertes**: lo que ya haces bien y conviene mantener.
- 🧭 **Plan de mejora**: qué arreglar hoy, esta semana y cuando puedas.

> Construida por **[@nicofernandez.ia](https://www.instagram.com/nicofernandez.ia/)** en Instagram. Si te sirve, pásate y cuéntame qué ha encontrado en tu proyecto.

## Qué revisa

| Área | Ejemplos |
|---|---|
| Claves y secretos | API keys en el código, `.env` subido, claves expuestas en el frontend |
| Inyecciones | SQL, comandos del sistema, XSS, rutas de archivo, SSRF |
| Accesos y permisos | Rutas sin login, ver datos de otro cambiando un ID, contraseñas sin hash |
| **IA y agentes** | Prompt injection, datos personales enviados al modelo, agentes con permisos peligrosos, endpoints de IA abiertos que gastan tus créditos |
| Webhooks y automatizaciones | Webhooks sin firma, procesos que se duplican, credenciales con demasiados permisos |
| Configuración | Modo debug, CORS abierto, cookies inseguras, puertos expuestos |
| Dependencias y datos | Versiones sin fijar, datos personales en logs o backups |

## Instalación

**Opción 1 · Copiar la carpeta (funciona siempre)**

```bash
git clone https://github.com/nicofernandezia/claude-cybersegurity.git
# Para todos tus proyectos:
cp -r claude-cybersegurity/skills/modo-atacante ~/.claude/skills/
# O solo para un proyecto:
cp -r claude-cybersegurity/skills/modo-atacante <tu-proyecto>/.claude/skills/
```

En Windows (PowerShell):

```powershell
Copy-Item -Recurse claude-cybersegurity\skills\modo-atacante "$env:USERPROFILE\.claude\skills\"
```

**Opción 2 · Como plugin**

Dentro de Claude Code:

```
/plugin marketplace add nicofernandezia/claude-cybersegurity
/plugin install modo-atacante@modo-atacante
```

Reinicia Claude Code después de instalarla.

## Uso

Abre Claude Code en la carpeta de tu proyecto y pide, por ejemplo:

- "Activa el modo atacante sobre mi proyecto"
- "Hackea mi proyecto y dime sus puntos débiles"
- "Haz una auditoría de seguridad antes de publicar"

O llámala directamente con `/modo-atacante`.

### Pruébala con el ejemplo

La carpeta [`ejemplo-vulnerable/`](ejemplo-vulnerable/) es una tienda pequeña con fallos puestos a propósito: inyección SQL, un agente de IA manipulable por WhatsApp, una clave en el código (inventada)… Abre Claude Code dentro de esa carpeta y activa el modo atacante para ver un informe completo.

## Límites (léelos)

- **Solo para tu propio código.** La skill analiza la carpeta en la que la abres y no ataca servidores, webs ni APIs, tampoco las tuyas en producción.
- **Solo lee.** No cambia tu código ni ejecuta nada sin pedirte permiso.
- **No sustituye a una auditoría profesional.** Encuentra muchos fallos habituales, pero si manejas datos sensibles o pagos, contrata además una revisión humana.
- **El informe contiene detalles de tus fallos.** No lo subas a un repositorio público (ya está en el `.gitignore`).

## Estructura

```
skills/modo-atacante/
  SKILL.md                     # instrucciones de la skill
  references/checklist.md      # lo que revisa, por categorías
  references/plantilla-informe.md
  scripts/buscar_secretos.py   # buscador de claves (solo lectura, las enmascara)
ejemplo-vulnerable/            # proyecto de prueba con fallos a propósito
```

## Licencia

MIT. Úsala, cámbiala y compártela.

---

Hecha por **[@nicofernandez.ia](https://www.instagram.com/nicofernandez.ia/)** · IA aplicada a negocios, sin humo.

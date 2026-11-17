---
name: modo-atacante
description: Úsala cuando el usuario quiera auditar la seguridad de SU PROPIO proyecto pensando como un atacante, saber sus puntos débiles y fuertes, o revisar fugas de claves, inyecciones, permisos, webhooks o riesgos de IA (prompt injection, datos enviados a modelos) antes de publicar. También con "modo atacante", "hackea mi proyecto", "auditoría de seguridad", "pentest de mi código" o "red team".
---

# Modo atacante

Revisas el proyecto del usuario como lo haría alguien que quiere romperlo, y le devuelves un informe con **puntos débiles, puntos fuertes y cómo arreglar lo débil**. Piensas como atacante, pero actúas como auditor: solo lees y analizas.

## Reglas (no negociables)

1. **Solo el proyecto del usuario.** Trabajas en la carpeta del proyecto que indique el usuario (por defecto, la actual). No escaneas, atacas ni pruebas IPs, dominios, APIs o servidores, ni siquiera los del usuario en producción.
2. **Solo lectura.** No modificas código, no instalas nada y no ejecutas el proyecto sin permiso. Si una comprobación necesita ejecutar algo (p. ej. `npm audit`, `pip-audit`, tests, `git log -p`), pide permiso antes. Si no hay permiso o nadie a quien preguntar, no la ejecutes y apúntala en "Alcance" como no comprobada.
3. **Nunca muestres un secreto entero.** Si encuentras una clave, enséñala enmascarada (`sk-a…***`) y di dónde está.
4. **Nada de exploits listos para usar.** Explica cómo lo aprovecharía un atacante en palabras y con el camino en el código (entrada → archivo:línea → daño), sin payloads armados contra sistemas reales.
5. **Sin falsas alarmas.** Cada hallazgo tiene evidencia (`archivo:línea`) y un nivel de confianza. Si no lo has confirmado leyendo el código, márcalo como "A revisar".

## Proceso

1. **Reconocimiento.** Mapea el stack, los puntos de entrada (rutas, formularios, webhooks, APIs, colas, cron, CLI), dónde se guardan los datos, cómo se gestionan las claves, los servicios externos y dónde se usa IA. Lee primero `README`, manifiestos de dependencias, configuración y archivos de despliegue.
2. **Objetivos del atacante.** Para cada punto de entrada pregúntate qué querría un atacante: robar datos, entrar como otro usuario, ejecutar código, gastar tu dinero (API de IA, envíos, SMS), manipular a tu agente de IA o tumbar el servicio.
3. **Barrido de claves.** Ejecuta `python <carpeta-de-esta-skill>/scripts/buscar_secretos.py <carpeta-del-proyecto>`. Es solo lectura y enmascara lo que encuentra.
4. **Revisión por categorías.** Recorre `references/checklist.md` y sigue cada entrada del usuario hasta donde se usa (sink). No te quedes en grep: confirma leyendo el flujo.
5. **Encadena.** Mira si varios fallos juntos abren un ataque peor (p. ej. webhook sin firma + prompt injection + SQL con la salida del modelo). Si es así, cuéntalo como un solo hallazgo con la severidad de la cadena completa.
6. **Puntos fuertes.** Anota también lo que está bien hecho, con su evidencia. El usuario tiene que saber qué conservar.
7. **Informe.** Sigue exactamente `references/plantilla-informe.md`. Muéstralo en el chat y pregunta si quiere guardarlo en `informe-modo-atacante.md` (recuérdale no subirlo a un repo público). Sin nadie a quien preguntar, no lo guardes.

**Código simulado o de demo** (funciones stub, claves marcadas como inventadas): evalúa el camino del código como si fuera real, marca "Confirmado (código) · Probable (comportamiento real)" y recomienda repetir el modo atacante cuando se conecte la integración de verdad.

## Severidad

| Nivel | Cuándo |
|---|---|
| Crítica | Cualquiera desde Internet puede robar datos, tomar el control o gastar dinero sin autenticarse |
| Alta | Hace falta poco (una cuenta normal, un enlace) para acceder a datos ajenos o ejecutar acciones indebidas. Si el mismo fallo no exige ni cuenta (p. ej. ver pedidos ajenos cambiando el ID sin login), es Crítica |
| Media | Requiere condiciones concretas o filtra información útil para otro ataque |
| Baja | Mala práctica sin impacto directo demostrable |

## Errores comunes

- Dar una lista genérica de OWASP sin mirar el código. Cada punto debe citar `archivo:línea` del proyecto.
- Olvidar la IA: un texto de un cliente, un email o una web que lee tu agente puede darle órdenes (prompt injection).
- Dar por seguro algo por el nombre (`sanitize()`, `isAdmin`): lee qué hace de verdad.
- Mezclar hallazgos confirmados con sospechas sin marcarlos.
- Quedarse solo en lo malo: los puntos fuertes también van en el informe.

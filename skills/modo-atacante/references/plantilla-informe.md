# Plantilla del informe

El informe tiene estas partes, en este orden. Escribe en el idioma del usuario, con frases cortas y sin jerga innecesaria.

```markdown
# Informe modo atacante · <nombre del proyecto>

**Veredicto:** <una frase: cómo de expuesto está y qué arreglar primero>
**Alcance:** <carpetas revisadas> · <qué no se ha podido comprobar y por qué>

## Resumen
| Severidad | Hallazgos |
|---|---|
| Crítica | n |
| Alta | n |
| Media | n |
| Baja | n |

## Puntos débiles
### 1. <Título corto> · <Crítica/Alta/Media/Baja> · <Confirmado/Probable/A revisar>
- **Dónde:** `archivo:línea` (o `archivo:inicio-fin`; si es una cadena, cada paso con su ubicación)
- **Cómo lo usaría un atacante:** <entrada → camino en el código → daño, en 2-3 frases>
- **Impacto:** <qué pierde el usuario o sus clientes>
- **Cómo arreglarlo:** <cambio concreto; fragmento de código corregido si es corto>

(ordenados de más a menos grave)

## Puntos fuertes
- <buena práctica> — `archivo:línea`

## Plan de mejora
1. **Hoy:** <críticas y altas>
2. **Esta semana:** <medias>
3. **Cuando puedas:** <bajas y endurecimiento>

## Cómo seguir
<1-3 recomendaciones: tests de seguridad, auditor de dependencias, revisión antes de cada despliegue…>
```

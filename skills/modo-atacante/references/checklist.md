# Checklist del atacante

Para cada punto, busca la evidencia en el código. Si no aplica al proyecto, sáltalo sin mencionarlo.

## 1. Claves y secretos
- Claves, tokens o contraseñas escritas en el código, en el frontend o en el historial de git (`git log -p` solo si el usuario lo permite).
- `.env` subido al repo o ausente del `.gitignore`.
- Claves de servidor expuestas al navegador (variables `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` con secretos).
- Secretos que se imprimen en logs o se devuelven en respuestas de error.

## 2. Entradas sin validar (inyecciones)
- SQL/NoSQL montado concatenando texto del usuario.
- Comandos del sistema (`exec`, `subprocess`, `os.system`, `child_process`) con datos externos.
- HTML con datos del usuario sin escapar (XSS): `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `|safe`.
- Rutas de archivo construidas con datos del usuario (path traversal) y subidas de archivos sin límite de tipo o tamaño.
- Deserialización insegura (`pickle`, `eval`, `yaml.load` sin `SafeLoader`).
- Peticiones a URLs que decide el usuario (SSRF).

## 3. Autenticación y permisos
- Rutas o endpoints sin comprobación de sesión.
- Acceso a recursos por ID sin comprobar que son del usuario (IDOR): `/pedido/123` → `/pedido/124`.
- Roles comprobados solo en el frontend.
- Contraseñas sin hash fuerte (bcrypt/argon2), tokens sin caducidad, JWT sin verificar firma o con `alg: none`.
- Sin límite de intentos en login, recuperación de contraseña o códigos.

## 4. IA y agentes
- **Prompt injection**: textos externos (emails, webs, PDFs, mensajes de WhatsApp, reseñas) que entran en el prompt sin separar de las instrucciones.
- El agente tiene herramientas peligrosas (borrar, pagar, enviar emails, ejecutar código) sin confirmación humana.
- Datos personales o confidenciales enviados al modelo sin necesidad (nombres, DNI, historiales, contratos).
- La respuesta del modelo se ejecuta o se inserta tal cual (SQL, HTML, comandos, JSON sin validar). Trátala como entrada de un desconocido: si un mensaje puede convencer al modelo de devolver `"1 OR 1=1"` en un campo que acaba en un `UPDATE`, es una inyección SQL de segundo orden.
- El agente actúa sobre recursos sin comprobar que son de quien escribe (cancelar el pedido de otro cliente).
- Endpoint de IA abierto sin autenticación ni límite: cualquiera puede gastar tus créditos.
- System prompt con secretos o reglas de negocio que no deberían filtrarse.

## 5. Webhooks y automatizaciones (n8n, Make, Zapier, crons)
- Webhooks sin firma, token o comprobación de origen.
- Procesos que se repiten si el webhook llega dos veces (sin idempotencia).
- Credenciales con más permisos de los necesarios.
- Errores que se tragan en silencio y dejan datos a medias.

## 6. Configuración y despliegue
- `DEBUG=True` o trazas de error visibles en producción.
- CORS abierto (`*`) con credenciales; cookies sin `HttpOnly`/`Secure`/`SameSite`.
- Faltan cabeceras de seguridad (CSP, HSTS) en apps web.
- Puertos, paneles de administración o bases de datos expuestos en `docker-compose`/config.
- Contenedores corriendo como root, imágenes sin versión fija.

## 7. Dependencias
- Versiones sin fijar o muy antiguas en `package.json`, `requirements.txt`, etc.
- Paquetes abandonados o con nombres sospechosos (typosquatting).
- Si el usuario lo permite: `npm audit`, `pip-audit` u otro auditor del ecosistema.

## 8. Datos y privacidad
- Datos personales guardados sin necesidad o sin cifrar.
- Backups o exportaciones dentro del repo.
- Logs con emails, teléfonos o tokens.

"""Busca claves y secretos escritos en el código. Solo lee archivos; nunca muestra un secreto completo.

Uso:  python buscar_secretos.py [CARPETA]   (por defecto, la carpeta actual)
Sale con código 1 si encuentra algo, 0 si no.
"""
import re
import sys
from pathlib import Path

IGNORAR_DIRS = {".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist", "build", ".next",
                ".nuxt", "vendor", "target", ".cache", "coverage"}
MAX_BYTES = 1_000_000

PATRONES = [
    ("Clave de Anthropic", r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    ("Clave de OpenAI", r"sk-(?!ant-)(?:proj-)?[A-Za-z0-9_\-]{20,}"),
    ("Clave de AWS", r"AKIA[0-9A-Z]{16}"),
    ("Token de GitHub", r"gh[pousr]_[A-Za-z0-9]{36,}"),
    ("Token de Slack", r"xox[abposr]-[A-Za-z0-9\-]{10,}"),
    ("Clave de Stripe", r"(?:sk|rk)_live_[A-Za-z0-9]{20,}"),
    ("Clave de Google", r"AIza[0-9A-Za-z_\-]{35}"),
    ("Clave privada", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ("JWT", r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    ("URL con contraseña", r"[a-z][a-z0-9+.\-]*://[^\s:/@]+:[^\s:/@]{4,}@[^\s/]+"),
    ("Contraseña o token asignado", r"(?i)\b(?:password|passwd|pwd|secret|token|api[_-]?key|apikey|contrase(?:ñ|n)a)\b\s*[:=]\s*[\"'][^\"'\s]{6,}[\"']"),
]
PATRONES = [(n, re.compile(p)) for n, p in PATRONES]
FALSOS = re.compile(r"(?i)(example|ejemplo|placeholder|fake|dummy|demo|inventad|your[_-]|tu[_-]|xxxx|changeme|<[^>]+>|\$\{|process\.env|os\.environ|getenv)")


def enmascara(s: str) -> str:
    s = s.strip()
    return s[:4] + "…***" if len(s) > 8 else "***"


def es_texto(p: Path) -> bool:
    try:
        with p.open("rb") as f:
            return b"\0" not in f.read(2048)
    except OSError:
        return False


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    hallazgos = []
    for p in raiz.rglob("*"):
        if any(part in IGNORAR_DIRS for part in p.relative_to(raiz).parts[:-1]) or not p.is_file():
            continue
        if p.stat().st_size > MAX_BYTES or not es_texto(p):
            continue
        rel = p.relative_to(raiz).as_posix()
        if p.name == ".env" or p.name.startswith(".env.") and not p.name.endswith((".example", ".sample")):
            hallazgos.append((rel, 0, "Archivo .env dentro del proyecto", "revisa que esté en .gitignore", "media"))
        for n, linea in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for nombre, rx in PATRONES:
                for m in rx.finditer(linea):
                    dudoso = bool(FALSOS.search(linea))
                    hallazgos.append((rel, n, nombre, enmascara(m.group(0)), "baja (parece de ejemplo)" if dudoso else "alta"))

    gi = raiz / ".gitignore"
    reglas = {l.strip() for l in gi.read_text(encoding="utf-8", errors="ignore").splitlines()} if gi.exists() else set()
    if not reglas & {".env", ".env*", "*.env", ".env.*", "/.env"}:
        hallazgos.append((".gitignore", 0, ".env no está ignorado", "añade .env a .gitignore", "media"))

    if not (raiz / ".git").exists():
        print("Aviso: la carpeta no es un repositorio git; no se ha podido revisar el historial.\n")
    if not hallazgos:
        print("Sin secretos aparentes. (Esto no garantiza que no haya: revisa también el historial de git.)")
        return 0
    print(f"{len(hallazgos)} posible(s) secreto(s):\n")
    for rel, n, nombre, valor, conf in hallazgos:
        print(f"- {rel}{':' + str(n) if n else ''} · {nombre} · {valor} · confianza {conf}")
    print("\nSi una clave real ha estado en el repo, cámbiala (rótala) aunque la borres: sigue en el historial.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

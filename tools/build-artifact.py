#!/usr/bin/env python3
"""Crea una versione a file singolo di Luludex da pubblicare come Artifact su claude.ai.

Uso: python3 tools/build-artifact.py [percorso-output]
Toglie lo scheletro HTML (lo aggiunge la piattaforma), manifest, icone, librerie Firebase
e service worker, e forza la modalità locale (nessun database).
"""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else root / 'dist' / 'luludex-artifact.html')
s = (root / 'index.html').read_text()
drop = [r'<!doctype html>\n', r'<html lang="it">\n', r'<head>\n', r'<meta charset="utf-8">\n',
        r'<meta name="viewport"[^\n]*\n', r'<link rel="(manifest|icon|apple-touch-icon)"[^\n]*\n',
        r'<meta name="(apple-mobile-web-app[^"]*|mobile-web-app-capable)"[^\n]*\n',
        r'</body>\n', r'</html>\n?',
        r'<script src="vendor/[^"]+"></script>\n',
        r"if \('serviceWorker' in navigator[^\n]*\n"]
for pat in [r'</head>\n', r'<body[^>]*>\n']:  # opzionali
    s = re.sub(pat, '', s)
for pat in drop:
    s, n = re.subn(pat, '', s)
    assert n, pat
s = s.replace('<script src="config.js"></script>', '<script>window.LULUDEX_FIREBASE = null; // artifact: solo modalità locale</script>')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(s)
print(out, len(s))

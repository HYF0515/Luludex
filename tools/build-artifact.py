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
        r'<meta name="viewport"[^\n]*\n', r'<link rel="(manifest|icon|apple-touch-icon)"[^\n]*\n', r'(<link rel="apple-touch-startup-image"[^\n]*\n)+',
        r'<meta name="(apple-mobile-web-app[^"]*|mobile-web-app-capable)"[^\n]*\n',
        r'</body>\n', r'</html>\n?',
        r'<script src="vendor/[^"]+"></script>\n',
        ]
for pat in [r'</head>\n', r'<body[^>]*>\n']:  # opzionali
    s = re.sub(pat, '', s)
for pat in drop:
    s, n = re.subn(pat, '', s)
    assert n, pat
# l'icona della schermata d'avvio va inclusa nel file (nell'Artifact non ci sono altri file)
import base64
icon = base64.b64encode((root / 'icons' / 'icon-192.png').read_bytes()).decode()
assert re.search(r'src="icons/icon-\d+\.png"', s)
s = re.sub(r'src="icons/icon-\d+\.png"', 'src="data:image/png;base64,' + icon + '"', s)
# niente service worker dentro l'Artifact
assert "if ('serviceWorker' in navigator && location.protocol === 'https:') {" in s
s = s.replace("if ('serviceWorker' in navigator && location.protocol === 'https:') {", "if (false) { // service worker disattivato nell'Artifact")
s = s.replace('<script src="config.js"></script>', '<script>window.LULUDEX_FIREBASE = null; // artifact: solo modalità locale</script>')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(s)
print(out, len(s))

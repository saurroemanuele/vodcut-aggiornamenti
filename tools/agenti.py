#!/usr/bin/env python3
"""NoonFrame · pagina "Agenti AI": come collegare Claude, ChatGPT, Codex o Cursor a NoonFrame (server MCP).

Scrive docs/agenti.html (italiano) e docs/en/agents.html (inglese) dallo stesso modello.
Uso: python3 tools/agenti.py
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"
MCP_URL = "https://jhoidpugjjvvkjccyrxg.supabase.co/functions/v1/mcp"

T = {
    "it": {
        "file": "agenti.html", "other": "en/agents.html", "otherLang": "English", "root": "",
        "title": "NoonFrame · Collega il tuo agente AI",
        "desc": "Collega Claude, ChatGPT, Codex o Cursor a NoonFrame: il tuo agente AI trova i momenti migliori delle tue live e crea clip verticali con sottotitoli.",
        "h1": "Collega il tuo agente AI a NoonFrame.",
        "sub": "Chiedi a Claude o al tuo agente di trasformare le tue live e i tuoi video in clip verticali, mentre fai altro.",
        "copy": "Copia", "copied": "Copiato",
        "stepsH": "Due passi",
        "s1h": "Aggiungi NoonFrame",
        "s1": [
            ("Claude (sito e app)", "Apri <b>Personalizza › Connettori</b>, tocca <b>Aggiungi connettore personalizzato</b>, incolla l'indirizzo e tocca <b>Aggiungi</b>. Poi tocca <b>Collega</b> accanto a NoonFrame."),
            ("Claude Code", "<code>claude mcp add --transport http noonframe " + MCP_URL + "</code> e poi <code>/mcp</code> per accedere."),
            ("Codex", "<code>codex mcp add noonframe --url " + MCP_URL + "</code> e poi <code>codex mcp login noonframe</code>."),
            ("ChatGPT, Cursor e gli altri", "Aggiungi un server MCP remoto con questo indirizzo."),
        ],
        "s2h": "Accedi e tocca Collega",
        "s2": "Si apre una pagina NoonFrame. Accedi con lo stesso account Google dell'app e tocca <b>Collega</b>. Il tuo agente è pronto.",
        "askH": "Cosa puoi chiedere",
        "ask": [
            "Fammi le clip della live di ieri, twitch.tv/videos/…",
            "Quanti crediti mi restano?",
            "Nella clip 2 metti i sottotitoli al centro e togli il titolo.",
            "Rifai le clip di questo video, solo i momenti più divertenti.",
        ],
        "canH": "Può", "cantH": "Non può",
        "can": [
            "Vedere il tuo piano e i crediti",
            "Leggere un link di Twitch, Kick o YouTube e dirti quanto costa",
            "Creare le clip, seguirle e mostrarti titoli e video",
            "Modificare una clip: impaginazione, titolo, sottotitoli, inizio e fine",
        ],
        "cant": [
            "Vedere i file del tuo computer",
            "Comprare o cambiare il tuo abbonamento",
            "Cambiare il tuo account o vedere quello di altri",
        ],
        "youH": "Decidi tu",
        "you": [
            "L'agente ti dice sempre quanto costa un video prima di crearne le clip.",
            "Le clip costano gli stessi crediti delle clip dal web.",
            "Scolleghi un agente quando vuoi da <a href=\"collega.html\">noonframe.com/collega.html</a>.",
        ],
        "faqH": "Domande",
        "faq": [
            ("Serve un abbonamento?", "Sì. Gli agenti AI sono per gli abbonati Starter, Pro e Ultimate. <a href=\"clip.html?compra=plan-starter\">Scegli un piano</a>."),
            ("Funziona anche dal telefono?", "Sì. Collegalo una volta dal sito di Claude e lo usi anche dall'app di Claude sul telefono."),
            ("Dice che serve l'autenticazione?", "Ricollega NoonFrame dal tuo agente (in Claude Code con <code>/mcp</code>) e accedi di nuovo."),
            ("Le clip dell'app sul computer?", "Per ora l'agente usa le clip dal web. L'app NoonFrame sul computer resta gratis e funziona come sempre."),
        ],
        "foot": [("privacy.html", "Privacy"), ("termini.html", "Termini d'uso"), ("index.html", "Home")],
    },
    "en": {
        "file": "en/agents.html", "other": "agenti.html", "otherLang": "Italiano", "root": "../",
        "title": "NoonFrame · Connect your AI agent",
        "desc": "Connect Claude, ChatGPT, Codex or Cursor to NoonFrame: your AI agent finds the best moments of your streams and makes vertical clips with subtitles.",
        "h1": "Connect your AI agent to NoonFrame.",
        "sub": "Ask Claude or your agent to turn your streams and videos into vertical clips while you do something else.",
        "copy": "Copy", "copied": "Copied",
        "stepsH": "Two steps",
        "s1h": "Add NoonFrame",
        "s1": [
            ("Claude (web and app)", "Open <b>Customize › Connectors</b>, tap <b>Add custom connector</b>, paste the address and tap <b>Add</b>. Then tap <b>Connect</b> next to NoonFrame."),
            ("Claude Code", "<code>claude mcp add --transport http noonframe " + MCP_URL + "</code> then <code>/mcp</code> to sign in."),
            ("Codex", "<code>codex mcp add noonframe --url " + MCP_URL + "</code> then <code>codex mcp login noonframe</code>."),
            ("ChatGPT, Cursor and others", "Add a remote MCP server with this address."),
        ],
        "s2h": "Sign in and tap Connect",
        "s2": "A NoonFrame page opens. Sign in with the same Google account you use in the app and tap <b>Connect</b>. Your agent is ready.",
        "askH": "What you can ask",
        "ask": [
            "Make clips from yesterday's stream, twitch.tv/videos/…",
            "How many credits do I have left?",
            "In clip 2 put the subtitles in the middle and remove the title.",
            "Redo the clips of this video, only the funniest moments.",
        ],
        "canH": "It can", "cantH": "It can't",
        "can": [
            "See your plan and credits",
            "Read a Twitch, Kick or YouTube link and tell you the cost",
            "Make the clips, follow them and show you titles and videos",
            "Edit a clip: layout, title, subtitles, start and end",
        ],
        "cant": [
            "See the files on your computer",
            "Buy anything or change your plan",
            "Change your account or see anyone else's",
        ],
        "youH": "You decide",
        "you": [
            "Your agent always tells you what a video costs before making clips.",
            "Clips cost the same credits as web clips.",
            "Disconnect an agent anytime from <a href=\"../collega.html?lang=en\">noonframe.com/collega.html</a>.",
        ],
        "faqH": "Questions",
        "faq": [
            ("Do I need a subscription?", "Yes. AI agents are for Starter, Pro and Ultimate subscribers. <a href=\"clip.html?compra=plan-starter\">Pick a plan</a>."),
            ("Does it work on my phone?", "Yes. Connect it once on the Claude website and use it from the Claude app on your phone too."),
            ("It says authentication is needed?", "Reconnect NoonFrame from your agent (in Claude Code with <code>/mcp</code>) and sign in again."),
            ("What about clips in the desktop app?", "For now your agent uses web clips. The NoonFrame desktop app stays free and works as always."),
        ],
        "foot": [("privacy.html", "Privacy"), ("terms.html", "Terms"), ("index.html", "Home")],
    },
}

CSS = """
@font-face { font-family: "Inter"; font-style: normal; font-display: swap; font-weight: 100 900; src: url({root}fonts/inter-latin-wght-normal.woff2) format("woff2"); }
:root { --ink:#050A1C; --card:#0A1430; --blue:#1E6BFF; --blue-hi:#4C8DFF; --fg:#F2F6FF; --fg2:#A6B4D4; --fg3:#6F7FA6; --line:rgba(160,190,255,.16); --ok:#22C55E; --err:#F87171; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--ink); color: var(--fg); font: 16px/1.6 "Inter", -apple-system, "Segoe UI", system-ui, sans-serif;
  background-image: radial-gradient(70% 38% at 50% -6%, rgba(30,107,255,.32), transparent 70%); background-repeat: no-repeat; }
.wrap { width: min(760px, 100%); margin: 0 auto; padding: 0 16px; }
header .wrap { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.brand { display: flex; align-items: center; gap: 10px; color: var(--fg); text-decoration: none; font-weight: 650; }
.brand img { width: 30px; height: 30px; }
.lang { color: var(--fg2); text-decoration: none; font-size: 14px; }
.hero { padding: 48px 0 24px; }
h1 { margin: 0 0 12px; font-size: clamp(30px, 6vw, 44px); line-height: 1.1; letter-spacing: -.03em; }
.sub { margin: 0 0 24px; color: var(--fg2); font-size: 18px; max-width: 34em; }
.url { display: flex; align-items: center; gap: 8px; padding: 8px 8px 8px 14px; border-radius: 14px; background: var(--card); box-shadow: inset 0 0 0 1px var(--line); }
.url code { flex: 1; min-width: 0; overflow-x: auto; white-space: nowrap; font: 500 14px/1.4 ui-monospace, "SF Mono", Consolas, monospace; color: var(--fg); scrollbar-width: none; }
.url code::-webkit-scrollbar { display: none; }
button { flex: none; height: 38px; padding: 0 14px; border: 0; border-radius: 10px; background: var(--blue); color: #fff; font: 600 14.5px/1 inherit; font-family: inherit; cursor: pointer; }
button:hover { background: var(--blue-hi); }
button:focus-visible, a:focus-visible { outline: 2px solid var(--blue-hi); outline-offset: 3px; }
section { padding: 28px 0; }
h2 { margin: 0 0 16px; font-size: 22px; letter-spacing: -.02em; }
.steps { display: grid; gap: 14px; }
.step { padding: 20px; border-radius: 18px; background: var(--card); box-shadow: inset 0 0 0 1px var(--line); }
.step h3 { margin: 0 0 12px; font-size: 17px; display: flex; gap: 10px; align-items: center; }
.step h3 i { font-style: normal; display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: rgba(30,107,255,.18); color: var(--blue-hi); font-size: 14px; }
.how { display: grid; gap: 12px; }
.how div { color: var(--fg2); font-size: 15px; }
.how b, .step p b { color: var(--fg); font-weight: 600; }
.how strong { display: block; color: var(--fg); font-size: 14px; font-weight: 600; }
.step p { margin: 0; color: var(--fg2); font-size: 15px; }
code { font: 500 13px/1.5 ui-monospace, "SF Mono", Consolas, monospace; color: var(--fg); background: rgba(160,190,255,.08); padding: 1px 5px; border-radius: 6px; overflow-wrap: anywhere; }
.asks { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }
.asks li { padding: 12px 14px; border-radius: 14px 14px 14px 4px; background: rgba(30,107,255,.14); color: var(--fg); font-size: 15px; width: fit-content; max-width: 100%; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 600px) { .cols { grid-template-columns: 1fr; } }
.list { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; font-size: 15px; }
.list li { display: flex; gap: 10px; align-items: flex-start; }
.list li::before { content: ""; flex: none; width: 18px; height: 18px; margin-top: 3px; border-radius: 50%; background: rgba(34,197,94,.16) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5 9.4l2.6 2.5L13 6.4' fill='none' stroke='%2322C55E' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/18px no-repeat; }
.list.no li { color: var(--fg2); }
.list.no li::before { background: rgba(248,113,113,.14) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M6 6l6 6M12 6l-6 6' fill='none' stroke='%23F87171' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E") center/18px no-repeat; }
.you { margin: 0; padding-left: 18px; color: var(--fg2); display: grid; gap: 6px; }
details { border-top: 1px solid var(--line); padding: 14px 0; }
details:last-child { border-bottom: 1px solid var(--line); }
summary { cursor: pointer; font-weight: 600; list-style: none; display: flex; justify-content: space-between; gap: 12px; }
summary::-webkit-details-marker { display: none; }
summary::after { content: "+"; color: var(--fg3); font-weight: 400; }
details[open] summary::after { content: "–"; }
details p { margin: 8px 0 0; color: var(--fg2); }
a { color: var(--blue-hi); }
footer { padding: 32px 0 48px; color: var(--fg3); font-size: 14px; }
footer .wrap { display: flex; flex-wrap: wrap; gap: 18px; }
footer a { color: var(--fg3); text-decoration: none; }
footer a:hover { color: var(--fg2); }
"""


def page(lg: str) -> str:
    t = T[lg]
    r = t["root"]
    e = html.escape
    li = lambda items: "".join(f"<li>{e(x)}</li>" for x in items)
    how = "".join(f"<div><strong>{e(a)}</strong>{b}</div>" for a, b in t["s1"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in t["faq"])
    foot = "".join(f'<a href="{href}">{e(name)}</a>' for href, name in t["foot"])
    canon = "https://noonframe.com/" + t["file"]
    alt_it = "https://noonframe.com/agenti.html"
    alt_en = "https://noonframe.com/en/agents.html"
    return f"""<!doctype html>
<html lang="{lg}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="it" href="{alt_it}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{canon}">
<link rel="icon" href="{r}favicon.png">
<style>{CSS.replace("{root}", r)}</style>
<script src="{r}agenti.js" defer></script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="{r}index.html"><img src="{r}logo.png" alt=""><span>NoonFrame</span></a><a class="lang" href="{r}{t["other"]}" hreflang="{"en" if lg == "it" else "it"}">{e(t["otherLang"])}</a></div></header>
<main class="wrap">
  <div class="hero">
    <h1>{e(t["h1"])}</h1>
    <p class="sub">{e(t["sub"])}</p>
    <div class="url"><code id="mcp">{MCP_URL}</code><button type="button" id="cp" data-ok="{e(t["copied"])}">{e(t["copy"])}</button></div>
  </div>
  <section>
    <h2>{e(t["stepsH"])}</h2>
    <div class="steps">
      <div class="step"><h3><i>1</i>{e(t["s1h"])}</h3><div class="how">{how}</div></div>
      <div class="step"><h3><i>2</i>{e(t["s2h"])}</h3><p>{t["s2"]}</p></div>
    </div>
  </section>
  <section>
    <h2>{e(t["askH"])}</h2>
    <ul class="asks">{li(t["ask"])}</ul>
  </section>
  <section class="cols">
    <div><h2>{e(t["canH"])}</h2><ul class="list">{li(t["can"])}</ul></div>
    <div><h2>{e(t["cantH"])}</h2><ul class="list no">{li(t["cant"])}</ul></div>
  </section>
  <section>
    <h2>{e(t["youH"])}</h2>
    <ul class="you">{"".join(f"<li>{x}</li>" for x in t["you"])}</ul>
  </section>
  <section>
    <h2>{e(t["faqH"])}</h2>
    {faq}
  </section>
</main>
<footer><div class="wrap"><span>© 2026 NoonFrame</span>{foot}</div></footer>
</body>
</html>
"""


def main():
    for lg in ("it", "en"):
        out = ROOT / T[lg]["file"]
        out.write_text(page(lg), encoding="utf-8", newline="\n")
        print("scritta", out.relative_to(ROOT.parent))


if __name__ == "__main__":
    main()

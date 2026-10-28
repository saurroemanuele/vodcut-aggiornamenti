"""NoonFrame - landing v2 (dal mockup "Landing v2"), italiano e inglese.

uso: python3 tools/landing2.py            -> docs/anteprima/v2/index.html e docs/anteprima/v2/en/index.html (non indicizzate)
     python3 tools/landing2.py --live     -> docs/index.html e docs/en/index.html (solo con l'ok di Emanuele)

Il modello e' tools/landing2.src.html (il mockup, con i suoi segnaposto). Questo script lo trasforma in una pagina
statica: niente librerie, niente immagini di altri creator (al loro posto grafiche fatte in CSS), link veri
(clip online, download, email del link per il PC).
"""
import html as H
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "landing2.src.html")
LIVE = "--live" in sys.argv
DL = "https://github.com/saurroemanuele/vodcut-aggiornamenti/releases/latest/download/"
FN = "https://jhoidpugjjvvkjccyrxg.supabase.co/functions/v1/"
BADGES = "/badges/"

# testi del mockup -> inglese (frase intera, come compare nella pagina)
EN = {
    "Come funziona": "How it works", "Domande": "FAQ", "Accedi": "Log in", "Scarica gratis": "Download free",
    "Dalla live alle clip, mentre fai altro.": "From stream to clips, while you do something else.",
    "Incolla il link di una live. NoonFrame trova i momenti migliori e li prepara in verticale, pronti per i social.":
        "Paste a stream link. NoonFrame finds the best moments and turns them into vertical clips, ready for social.",
    "Incolla il link di una live": "Paste a stream link", "Crea le clip": "Create clips",
    "Hai un computer? ": "Got a computer? ", "Ricevi l'app gratis ›": "Get the app free ›",
    "La tua email": "Your email", "Invia link": "Send link", "Link inviato": "Link sent", "Cambia": "Change",
    "L'app è per Windows e Mac: ti mandiamo il link via email.": "The app is for Windows and Mac: we'll email you the link.",
    "Vista": "View", "mar 27 ott 21:14": "Tue Oct 27 9:14 PM", "twitch.tv · Live 22 ottobre": "twitch.tv · Stream Oct 22",
    "Trovati 5 momenti": "5 moments found", "Apri le clip": "Open clips",
    "Incolla un link: le clip arrivano da sole": "Paste a link: the clips show up on their own",
    "Prende le live da qui, prepara le clip per lì": "Takes streams from here, makes clips for there",
    "Quattro passaggi. Tre li fa NoonFrame.": "Four steps. NoonFrame does three.",
    "01 · Tu": "01 · You", "04 · Tu": "04 · You", "Incolla il link": "Paste the link",
    "Una live di Twitch, YouTube o Kick, oppure un video dal computer. Non devi scaricare niente a mano.":
        "A Twitch, YouTube or Kick stream, or a video from your computer. No manual downloads.",
    "Clip veloci": "Quick clips", "Da una live o da un video lungo alle clip verticali": "From a stream or a long video to vertical clips",
    "Live 22 ottobre · Fortnite": "Stream Oct 22 · Fortnite", "Pronta": "Ready",
    "Live 22 ottobre · Elden Ring": "Stream Oct 22 · Elden Ring", "5 momenti trovati": "5 moments found",
    "Trova i momenti migliori": "Finds the best moments",
    "Guarda tutta la live al posto tuo e ti propone i passaggi da clip, già tagliati. Tre ore diventano cinque minuti da scegliere.":
        "It watches the whole stream for you and suggests the clip-worthy parts, already cut. Three hours become five minutes to choose from.",
    "Prepara le clip in verticale": "Makes vertical clips",
    "Formato 9:16, sottotitoli, zoom sui momenti forti e via pause ed errori. Se vuoi cambiare qualcosa, apri l'editor.":
        "9:16 format, captions, zooms on the big moments, pauses and mistakes gone. Want to change something? Open the editor.",
    "martedì 27 ottobre": "Tuesday, October 27",
    "Scegli e scarica": "Pick and download",
    "Tieni le clip che ti piacciono e scaricale, pronte per TikTok, Shorts e Reels.":
        "Keep the clips you like and download them, ready for TikTok, Shorts and Reels.",
    "La tua ultima live è già piena di clip.": "Your last stream is already full of clips.",
    "Scaricala e incolla il primo link.": "Download it and paste your first link.",
    "Privacy": "Privacy", "Termini": "Terms", "Contatti": "Contact",
}
TX = {  # testi messi da questo script
    "it": {"navPhone": "Ricevi il link", "win": "Scarica per Windows", "mac": "Scarica per Mac", "scan": "Analisi", "done": "Fatto",
           "sentTo": "a {} · aprilo dal computer", "bad": "Controlla l'email", "fail": "Non riesco a mandarla ora, riprova tra poco",
           "rate": "Troppe richieste: riprova tra qualche minuto", "linkLabel": "Link della live", "emailLabel": "La tua email",
           "title": "NoonFrame · Dalla live alle clip, mentre fai altro",
           "desc": "Incolla il link di una live: NoonFrame trova i momenti migliori e li prepara in verticale, pronti per i social. Gratis per Windows e Mac.",
           "copy": "Copia", "copied": "Copiato", "url": "https://noonframe.com/", "locale": "it_IT", "ogAlt": "NoonFrame, dalla live alle clip",
           "clip": "/clip.html", "privacy": "/privacy.html", "terms": "/termini.html", "lang": "it", "other": "English", "otherHref": "en/"},
    "en": {"navPhone": "Get the link", "win": "Download for Windows", "mac": "Download for Mac", "scan": "Analyzing", "done": "Done",
           "sentTo": "to {} · open it on your computer", "bad": "Check your email", "fail": "Can't send it right now, try again shortly",
           "rate": "Too many requests: try again in a few minutes", "linkLabel": "Stream link", "emailLabel": "Your email",
           "title": "NoonFrame · From stream to clips, while you do something else",
           "desc": "Paste a stream link: NoonFrame finds the best moments and turns them into vertical clips, ready for social. Free for Windows and Mac.",
           "copy": "Copy", "copied": "Copied", "url": "https://noonframe.com/en/", "locale": "en_US", "ogAlt": "NoonFrame, from stream to clips",
           "clip": "/en/clip.html", "privacy": "/en/privacy.html", "terms": "/en/terms.html", "lang": "en", "other": "Italiano", "otherHref": "../"},
}
# la pubblicazione sui social non c'e' ancora: la landing non la promette (Emanuele, 28 ott 2026)
# sul web le clip si pagano (almeno la ricarica XS), nell'app sono gratis
MAC_CMD = "xattr -cr /Applications/NoonFrame.app && open /Applications/NoonFrame.app"
FAQ = {   # (domanda, risposta) oppure (domanda, risposta, True) = risposta con il comando per il Mac da copiare
    "it": [("È gratis?", "L'app per computer sì. Le clip dal web si sbloccano da 2,99 €, e con un piano hai più crediti per l'AI."),
           ("Da quali piattaforme prende le live?", "Twitch, YouTube e Kick. Puoi anche caricare un video che hai già sul computer."),
           ("Su che computer funziona?", "Su Windows e su Mac."),
           ("Come apro l'app la prima volta?", "Windows: se compare un avviso, premi Ulteriori informazioni e poi Esegui comunque. "
            "Mac: trascina NoonFrame in Applicazioni e, solo la prima volta, incolla nel Terminale", True)],
    "en": [("Is it free?", "The desktop app is. Web clips unlock from €2.99, and a plan gives you more AI credits."),
           ("Which platforms does it take streams from?", "Twitch, YouTube and Kick. You can also upload a video you already have on your computer."),
           ("Which computers does it run on?", "Windows and Mac."),
           ("How do I open the app the first time?", "Windows: if a warning shows up, click More info and then Run anyway. "
            "Mac: drag NoonFrame to Applications and, the first time only, paste this in Terminal", True)],
}
FAQ_B = {"it": ["Windows:", "Ulteriori informazioni", "Esegui comunque", "Mac:"], "en": ["Windows:", "More info", "Run anyway", "Mac:"]}
# miniature: sfumature al posto degli screenshot di altri creator
TH = ["linear-gradient(160deg,#6CB2FF,#1F3FA8 70%)", "linear-gradient(160deg,#C7A2FF,#5B2BB5 70%)", "linear-gradient(160deg,#5BEAAE,#0E6E5A 70%)"]
CLIPS = {"it": ["Il facepalm in diretta", "Non si ferma fino alla fine", "\"Ragazzi…\""],
         "en": ["The live facepalm", "Doesn't stop till the end", "\"Guys…\""]}
# notifiche sul telefono del passo 4: clip pronte e scaricate (niente post pubblicati o programmati)
POSTS = {"it": [("NoonFrame", "ora", "Clip scaricata: \"Ascolta questa assurdità\""),
                ("NoonFrame", "2 min fa", "Clip scaricata: \"Non si ferma fino alla fine\""),
                ("NoonFrame", "5 min fa", "5 clip pronte dalla tua live")],
         "en": [("NoonFrame", "now", "Clip downloaded: \"Listen to this madness\""),
                ("NoonFrame", "2 min ago", "Clip downloaded: \"Doesn't stop till the end\""),
                ("NoonFrame", "5 min ago", "5 clips ready from your stream")]}
CAPTION = {"it": "Ascolta questa assurdità", "en": "Listen to this madness"}

# grafiche al posto delle immagini del mockup (niente foto di altri)
STREAM_ART = ('<div aria-hidden="true" style="position:absolute;inset:0;background:radial-gradient(60% 70% at 30% 60%,rgba(255,140,90,.55),rgba(255,140,90,0) 70%),'
              'radial-gradient(50% 60% at 75% 35%,rgba(110,160,255,.6),rgba(110,160,255,0) 70%),linear-gradient(160deg,#1B2340,#2B1B4A 55%,#0F1424)"></div>'
              '<div aria-hidden="true" style="position:absolute;right:3%;bottom:6%;width:22%;aspect-ratio:4/3;border-radius:8px;background:linear-gradient(160deg,#3A4A6E,#1A2238);border:2px solid rgba(255,255,255,.25)"></div>')
TIMELINE_ART = ('<div aria-hidden="true" style="position:absolute;inset:0;display:flex;flex-direction:column;gap:6%;padding:5% 4%;background:#11151C">'
                '<div style="display:flex;gap:2%;height:14%"><i style="flex:5;border-radius:4px;background:#3D86FF"></i><i style="flex:2;border-radius:4px;background:#3D86FF;opacity:.6"></i></div>'
                '<div style="display:flex;gap:2%;height:14%"><i style="flex:2;border-radius:4px;background:#A57BFF"></i><i style="flex:3;border-radius:4px;background:#A57BFF;opacity:.7"></i><i style="flex:2"></i></div>'
                '<div style="display:flex;gap:1%;height:22%"><i style="flex:3;border-radius:4px;background:linear-gradient(90deg,#2B3A5E,#41557F)"></i><i style="flex:2;border-radius:4px;background:linear-gradient(90deg,#3A2B5E,#5A417F)"></i><i style="flex:4;border-radius:4px;background:linear-gradient(90deg,#2B5E55,#417F72)"></i></div>'
                '<div style="height:18%;border-radius:4px;background:repeating-linear-gradient(90deg,rgba(108,178,255,.55) 0 2px,transparent 2px 5px)"></div></div>')


def clip_art(lang):
    return ('<div aria-hidden="true" style="position:absolute;inset:0;background:radial-gradient(70% 45% at 50% 30%,rgba(255,170,120,.55),rgba(255,170,120,0) 70%),'
            'radial-gradient(70% 45% at 50% 78%,rgba(110,160,255,.55),rgba(110,160,255,0) 70%),linear-gradient(180deg,#26324F,#151B2B 50%,#2A1F45)"></div>'
            '<div style="position:absolute;left:50%;top:49%;transform:translate(-50%,-50%);padding:5px 8px;border-radius:6px;background:#fff;color:#0C1222;'
            f'font:800 12px/1.15 Manrope,sans-serif;text-align:center;width:max-content;max-width:80%">{H.escape(CAPTION[lang])}</div>')


def sc_for(m, name, items):
    """<sc-for list="{{ name }}" as="x">...</sc-for> -> ripetuto per ogni elemento (dict)"""
    pat = re.compile(r'<sc-for list="\{\{ ' + name + r' \}\}" as="(\w+)"[^>]*>(.*?)</sc-for>', re.S)

    def rep(mo):
        var, body = mo.group(1), mo.group(2)
        return "".join(re.sub(r"\{\{ " + var + r"\.(\w+) \}\}", lambda x: str(it[x.group(1)]), body) for it in items)
    return pat.sub(rep, m)


def build(lang):
    s = open(SRC, encoding="utf-8").read()
    css = s[s.find("<style>") + 7:s.find("</style>")]
    a = s.find('<sc-if value="{{ notPhone }}"')
    a = s.find(">", a) + 1
    m = s[a:s.rfind("</sc-if>", 0, s.find("</x-dc>"))]
    T = TX[lang]
    esc = H.escape

    # immagini del mockup (screenshot di altri creator) -> grafiche
    m = re.sub(r'<image-slot id="lp-hero-stream"[^>]*></image-slot>', STREAM_ART, m)
    m = re.sub(r'<image-slot id="lp-step3-timeline"[^>]*></image-slot>', TIMELINE_ART, m)
    m = re.sub(r'<image-slot id="lp-step3-clip"[^>]*></image-slot>', clip_art(lang), m)
    m = m.replace("#1D222C url(uploads/pasted-1793074135691-0.png) 50% 38%/110% auto no-repeat",
                  "radial-gradient(60% 70% at 30% 60%,rgba(255,140,90,.5),rgba(255,140,90,0) 70%),linear-gradient(160deg,#1B2A4A,#3B1F5C)")
    m = re.sub(r"#[0-9A-Fa-f]{6} url\(\{\{ (\w+)\.img \}\}\)[^;\"]*", r"{{ \1.img }}", m)
    assert "uploads/" not in m, "immagine di un altro creator rimasta"

    # niente pubblicazione sui social: si scelgono e si scaricano le clip
    for a_, b_ in ((">Prende le live da qui, pubblica le clip lì<", ">Prende le live da qui, prepara le clip per lì<"),
                   (">Scegli e pubblica<", ">Scegli e scarica<"),
                   (">Tieni le clip che ti piacciono e mandale su TikTok, Shorts e Reels, ognuna con lo stile del suo account. Niente esce senza la tua conferma.<",
                    ">Tieni le clip che ti piacciono e scaricale, pronte per TikTok, Shorts e Reels.<")):
        assert m.count(a_) == 1, a_
        m = m.replace(a_, b_)

    # liste
    names = CLIPS[lang]
    m = sc_for(m, "heroClips", [{"title": esc(names[i]), "meta": "9:16 · " + d, "img": TH[i]} for i, d in enumerate(["0:28", "0:41", "0:19"])])
    plats = [("Twitch", "#9146FF", "twitch-on"), ("YouTube", "#FF0033", "youtube-on"), ("Kick", "#1E9E3A", "kick-on"),
             ("TikTok", "#111318", "tiktok-free"), ("Instagram", "#D62976", "instagram-on"), ("X", "#111318", "x-on")]
    m = sc_for(m, "platforms", [{"name": n, "color": c, "icon": BADGES + i + ".png"} for n, c, i in plats])
    m = sc_for(m, "moments", [{"left": l, "w": w} for l, w in [(6, 2), (22, 3), (34, 1.6), (66, 2.4), (81, 2)]])
    m = sc_for(m, "momentList", [{"t": t, "title": esc(names[i]), "d": d, "img": TH[i]} for i, (t, d) in enumerate([("12:47", "0:28"), ("1:04:10", "0:41"), ("2:31:05", "0:19")])])
    m = sc_for(m, "posts", [{"account": esc(a), "when": esc(w), "note": esc(n), "color": "#FFFFFF", "icon": "/logo.png"} for a, w, n in POSTS[lang]])

    def faq_html(f):
        a, cmd = esc(f[1]), ""
        if len(f) > 2:   # primo avvio: parole chiave in grassetto, Mac a capo, comando da copiare
            for w in FAQ_B[lang]:
                a = a.replace(esc(w), "<b>" + esc(w) + "</b>", 1)
            a = a.replace(". <b>Mac:</b>", ".<br><b>Mac:</b>")
            cmd = f'<div class="cmd"><code>{esc(MAC_CMD)}</code><button type="button" class="js-copy">{esc(T["copy"])}</button></div>'
        return f'<details class="faq"><summary>{esc(f[0])}</summary><p>{a}</p>{cmd}</details>'
    m = re.sub(r'<sc-for list="\{\{ faqs \}\}".*?</sc-for>', "".join(faq_html(f) for f in FAQ[lang]), m, flags=re.S)

    # pezzi che cambiano col telefono o con lo stato: classi e variabili CSS al posto della logica del mockup
    m = m.replace("{{ hdrTop }}px", "12px")
    m = m.replace('data-theme="{{ theme }}"', 'id="lp" data-theme="light"').replace('data-wp="{{ wp }}"', 'id="wp" data-wp="alba"')
    m = m.replace("width:{{ scanPct }}%", "width:18%").replace('<div style="height:100%;width:18%', '<div id="scanbar" style="height:100%;width:18%')
    m = m.replace("{{ scanLabel }}", f'<span id="scanlbl">{T["scan"]} 18%</span>')
    m = m.replace('onClick="{{ navGo }}" href="#scarica"', 'id="navcta" href="#scarica"')
    m = m.replace("{{ navCta }}", f'<span data-only="desk">{esc(EN["Scarica gratis"] if lang == "en" else "Scarica gratis")}</span><span data-only="phone">{esc(T["navPhone"])}</span>')
    m = re.sub(r'<a href="#"([^>]*)>((?:(?!</a>).)*?)\{\{ ctaPrimary \}\}', lambda x: f'<a href="{DL}Noonframe-Setup.exe" class="js-dl"{x.group(1)}>{x.group(2)}<span class="js-os">{esc(T["win"])}</span>', m, flags=re.S)
    m = m.replace('<form onSubmit="{{ goClip }}"', '<form id="clipform"')
    m = m.replace('<input value="{{ link }}" onInput="{{ onLink }}"', f'<input id="clipurl" name="link" type="text" inputmode="url" autocomplete="off" aria-label="{esc(T["linkLabel"])}"')
    m = m.replace('<form onSubmit="{{ lSend }}"', '<form class="js-send" novalidate')
    m = m.replace('<input type="email" value="{{ lEmail }}" onInput="{{ lOnEmail }}"', f'<input type="email" class="js-email" autocomplete="email" aria-label="{esc(T["emailLabel"])}"')
    m = m.replace('<button onClick="{{ lReset }}"', '<button type="button" class="js-reset"').replace('<button onClick="{{ lOpenIt }}"', '<button type="button" class="js-open"')
    m = m.replace("{{ lSentTo }}", '<span class="js-sentto"></span>')
    for v in ["navLinks", "navLogin", "mFrameAR", "mDesk", "mPill", "mStreamL", "mStreamT", "mStreamW", "mPanelR", "mPanelT", "mPanelW"]:
        m = m.replace("{{ " + v + " }}", "var(--" + v + ")")
    m = re.sub(r'<sc-if value="\{\{ (\w+) \}\}"[^>]*>', r'<div class="dc" data-if="\1">', m).replace("</sc-if>", "</div>")
    m = re.sub(r'\sstyle-hover="[^"]*"', "", m)
    # link veri
    m = m.replace('src="web/logo.png"', 'src="/logo.png"')
    m = m.replace('<a href="#" style="display:var(--navLogin)', f'<a href="{T["clip"]}" style="display:var(--navLogin)')
    foot = {"Privacy": T["privacy"], "Termini": T["terms"], "Contatti": "mailto:business@noonframe.com"}
    for k, href in foot.items():
        m = m.replace(f'<a href="#" style="color:var(--t3)">{k}</a>', f'<a href="{href}" style="color:var(--t3)">{k}</a>')
    other = "en" if lang == "it" else "it"
    m = m.replace('<span>© 2026</span>', f'<span>© 2026 NoonFrame</span><a href="{T["otherHref"]}" hreflang="{other}" data-lang="{other}" style="color:var(--t3)">{T["other"]}</a>')
    # le ancore della landing di prima: l'email con il link per il PC rimanda a #domande, i dati strutturati a #download
    for a_, b_ in (('id="faq"', 'id="domande"'), ('href="#faq"', 'href="#domande"'), ('<div id="scarica" ', '<div id="download" '), ('href="#scarica"', 'href="#download"')):
        assert m.count(a_) == 1, a_
        m = m.replace(a_, b_)
    left = re.findall(r"\{\{[^}]*\}\}|<sc-|<image-slot|href=\"#\" ", m)
    assert not left, left

    if lang == "en":   # testi: solo nodi di testo e attributi interi, mai pezzi di parole
        for it_, en in sorted(EN.items(), key=lambda x: -len(x[0])):
            for a_, b_ in ((">" + esc(it_, False) + "<", ">" + esc(en, False) + "<"), (">" + it_ + "<", ">" + en + "<"),
                           ('placeholder="' + it_ + '"', 'placeholder="' + en + '"')):
                m = m.replace(a_, b_)
        m = m.replace(">Incolla il link di una live<", ">" + EN["Incolla il link di una live"] + "<")

    page_css = css + """
@font-face{font-family:Manrope;font-style:normal;font-weight:200 800;font-display:swap;src:url(/fonts/manrope.ttf) format("truetype")}
:root{--navLinks:flex;--navLogin:block;--mFrameAR:16/10;--mDesk:inline;--mPill:flex;--mStreamL:6%;--mStreamT:13%;--mStreamW:56%;--mPanelR:5%;--mPanelT:10%;--mPanelW:31%}
html,body{background:#F7F8FB}html.dark,html.dark body{background:#07090E}
.dc{display:contents}[data-if=narrowL],[data-if=lIsOpen],[data-if=lSent],[data-only=phone]{display:none}
.l-open [data-if=lClosed],.l-sent [data-if=lNotSent]{display:none}.l-open [data-if=lIsOpen],.l-sent [data-if=lSent]{display:contents}
@media (max-width:639px){:root{--navLinks:none;--navLogin:none;--mFrameAR:3/5;--mDesk:none;--mPill:none;--mStreamL:5%;--mStreamT:9%;--mStreamW:90%;--mPanelR:8%;--mPanelT:34%;--mPanelW:84%}
[data-if=narrowL]{display:contents}[data-if=notNarrowL],[data-only=desk]{display:none}[data-only=phone]{display:inline}}
.faq{border-bottom:1px solid var(--line)}.faq summary{list-style:none;display:flex;align-items:center;gap:16px;padding:20px 0;color:var(--ink);font:600 15px Manrope,sans-serif;cursor:pointer}
.faq summary::-webkit-details-marker{display:none}.faq summary::after{content:"+";margin-left:auto;font-size:18px;font-weight:400;color:var(--t3)}.faq[open] summary::after{content:"–"}
.faq p{margin:0 0 20px;max-width:560px;font-size:14px;line-height:1.65;color:var(--t2)}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:2px solid var(--ac);outline-offset:3px;border-radius:999px}
.js-msg{font-size:12.5px;color:#E5484D}
.faq p b{color:var(--ink);font-weight:600}
.cmd{display:flex;align-items:center;gap:8px;margin:-8px 0 20px;padding:6px 6px 6px 12px;border-radius:12px;border:1px solid var(--line);background:rgba(127,140,170,.08)}
.cmd code{flex:1;min-width:0;overflow-x:auto;white-space:nowrap;font:500 12.5px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--ink)}
.cmd button{flex:none;padding:7px 12px;border:0;border-radius:999px;background:var(--ac);color:#fff;font:700 12px Manrope,sans-serif;cursor:pointer}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""
    js = """
(function(){
var T=%(T)s, FN=%(FN)s, DL=%(DL)s, LIVE=%(LIVE)s, GOING=false;
// la pagina non si apre dentro altri siti (niente click rubati)
if(window.top!==window.self){document.documentElement.style.display='none';try{window.top.location=location.href}catch(e){}return}
// lingua: quella scelta l'ultima volta, se no quella del browser (come la landing di prima)
document.querySelectorAll('[data-lang]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('nuvora.lang',a.getAttribute('data-lang'))}catch(e){}})});
if(LIVE){var saved=null;try{saved=localStorage.getItem('nuvora.lang')}catch(e){}
 var want=saved||((navigator.language||'it').toLowerCase().indexOf('it')===0?'it':'en');
 if(want!==T.lang){var la=document.querySelector('[data-lang="'+want+'"]');if(la){GOING=true;location.replace(la.href)}}}
// visite anonime per il pannello: niente cookie, niente dati personali, l'IP non si salva. Chi chiede di non essere tracciato non viene contato
var QS=new URLSearchParams(location.search);
function hit(k,d){if(!LIVE||GOING||location.hostname!=='noonframe.com'||navigator.globalPrivacyControl||navigator.doNotTrack==='1')return;
 try{var b=JSON.stringify({k:k,d:d||'',p:location.pathname,l:T.lang,r:document.referrer,us:QS.get('utm_source')||QS.get('ref'),um:QS.get('utm_medium'),uc:QS.get('utm_campaign'),w:innerWidth});
 if(!(navigator.sendBeacon&&navigator.sendBeacon(FN+'site-hit',b)))fetch(FN+'site-hit',{method:'POST',body:b,keepalive:true,mode:'no-cors'})}catch(e){}}
hit('view');
var root=document.documentElement, lp=document.getElementById('lp'), wp=document.getElementById('wp');
function theme(){var t;try{t=localStorage.getItem('nf-theme')}catch(e){}if(t!=='dark'&&t!=='light')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
 lp.setAttribute('data-theme',t);wp.setAttribute('data-wp',t==='dark'?'notte':'alba');root.classList.toggle('dark',t==='dark')}
theme();addEventListener('nf-theme',theme);addEventListener('storage',theme);
var mac=/Mac/i.test(navigator.platform||navigator.userAgent);
document.querySelectorAll('.js-dl').forEach(function(a){a.href=DL+(mac?'NoonFrame-Mac.zip':'Noonframe-Setup.exe');a.querySelector('.js-os').textContent=mac?T.mac:T.win;
 a.addEventListener('click',function(){hit('dl',mac?'mac':'win')})});
document.querySelectorAll('.js-copy').forEach(function(b){b.addEventListener('click',function(){var c=b.previousElementSibling.textContent;
 function done(){b.textContent=T.copied;setTimeout(function(){b.textContent=T.copy},1600)}
 function sel(){var r=document.createRange();r.selectNodeContents(b.previousElementSibling);var s=getSelection();s.removeAllRanges();s.addRange(r)}
 try{navigator.clipboard.writeText(c).then(done,sel)}catch(e){sel()}})});
var bar=document.getElementById('scanbar'),lbl=document.getElementById('scanlbl'),p=18;
if(!matchMedia('(prefers-reduced-motion: reduce)').matches)setInterval(function(){p=p>=100?18:Math.min(100,p+6);bar.style.width=p+'%%';lbl.textContent=p>=100?T.done:T.scan+' '+p+'%%'},500);
else{bar.style.width='100%%';lbl.textContent=T.done}
document.getElementById('clipform').addEventListener('submit',function(e){e.preventDefault();var v=document.getElementById('clipurl').value.trim();
 hit('dl','web');location.href=T.clip+(v?'?link='+encodeURIComponent(v):'')});
function openMail(){lp.classList.add('l-open');var el=document.getElementById('scarica-m');if(!el)return;
 scrollTo({top:el.getBoundingClientRect().top+scrollY-140,behavior:'smooth'});setTimeout(function(){var i=el.querySelector('.js-email');if(i)i.focus({preventScroll:true})},500)}
document.getElementById('navcta').addEventListener('click',function(e){if(innerWidth<640){e.preventDefault();openMail()}});
document.querySelectorAll('.js-open').forEach(function(b){b.addEventListener('click',openMail)});
document.querySelectorAll('.js-reset').forEach(function(b){b.addEventListener('click',function(){lp.classList.remove('l-sent')})});
document.querySelectorAll('.js-send').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();
 var inp=f.querySelector('.js-email'),btn=f.querySelector('button'),v=inp.value.trim(),msg=f.parentNode.querySelector('.js-msg');
 if(!msg){msg=document.createElement('div');msg.className='js-msg';msg.setAttribute('role','alert');f.after(msg)}msg.textContent='';
 if(!/^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$/i.test(v)){msg.textContent=T.bad;inp.focus();return}
 btn.disabled=true;var src=new URLSearchParams(location.search).get('utm_source')||(document.referrer?new URL(document.referrer).hostname:'diretto');
 fetch(FN+'download-link',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:v,lang:T.lang,marketing:false,source:src,website:''})})
 .then(function(r){return r.json().catch(function(){return{}}).then(function(j){if(r.status===429)throw new Error(T.rate);if(!r.ok)throw new Error(j.error==='email'?T.bad:T.fail)})})
 .then(function(){document.querySelectorAll('.js-sentto').forEach(function(s){s.textContent=T.sentTo.replace('{}',v)});lp.classList.add('l-sent');hit('mail')})
 .catch(function(err){msg.textContent=err.message||T.fail}).then(function(){btn.disabled=false})})});
})();
""" % {"T": json.dumps({k: T[k] for k in ["win", "mac", "scan", "done", "sentTo", "bad", "fail", "rate", "clip", "lang", "copy", "copied"]}, ensure_ascii=False),
       "FN": '"' + FN + '"', "DL": '"' + DL + '"', "LIVE": "true" if LIVE else "false"}

    robots = "" if LIVE else '<meta name="robots" content="noindex,nofollow">\n'
    # come la landing di prima: verifica di Google, canonical e lingue, anteprima sui social, dati strutturati
    og = "https://noonframe.com/shots/og.png"
    ld = [{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "NoonFrame", "operatingSystem": "Windows 10, Windows 11, macOS 13+",
           "applicationCategory": "MultimediaApplication", "applicationSubCategory": "Video editor", "description": T["desc"], "url": T["url"], "image": og,
           "inLanguage": ["it", "en"], "downloadUrl": T["url"] + "#download", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
           "publisher": {"@type": "Organization", "name": "NoonFrame", "url": "https://noonframe.com/"}},
          {"@context": "https://schema.org", "@type": "Organization", "name": "NoonFrame", "url": "https://noonframe.com/", "logo": "https://noonframe.com/logo.png",
           "email": "business@noonframe.com", "sameAs": ["https://discord.gg/5cQvNEBfee"]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": f[0], "acceptedAnswer": {"@type": "Answer", "text": f[1] + (" " + MAC_CMD if len(f) > 2 else "")}} for f in FAQ[lang]]}]
    ld_html = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>\n" for x in ld)
    head = f"""<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="google-site-verification" content="ARsuTk6v1O_ER9c3LhR758GaG5tOuTTTrLrspeQR910">
<link rel="canonical" href="{T["url"]}">
<link rel="alternate" hreflang="it" href="https://noonframe.com/">
<link rel="alternate" hreflang="en" href="https://noonframe.com/en/">
<link rel="alternate" hreflang="x-default" href="https://noonframe.com/en/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="NoonFrame">
<meta property="og:title" content="{esc(T["title"])}">
<meta property="og:description" content="{esc(T["desc"])}">
<meta property="og:url" content="{T["url"]}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(T["ogAlt"])}">
<meta property="og:locale" content="{T["locale"]}">
<meta property="og:locale:alternate" content="{"en_US" if lang == "it" else "it_IT"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(T["title"])}">
<meta name="twitter:description" content="{esc(T["desc"])}">
<meta name="twitter:image" content="{og}">
<link rel="apple-touch-icon" href="/logo.png">
<meta name="theme-color" content="#F7F8FB" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#07090E" media="(prefers-color-scheme: dark)">
{ld_html}"""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src https://jhoidpugjjvvkjccyrxg.supabase.co; object-src 'none'; base-uri 'self'; form-action 'none'">
{robots}<title>{esc(T["title"])}</title>
<meta name="description" content="{esc(T["desc"])}">
<link rel="icon" href="/favicon.png">
{head}<style>{page_css}</style>
</head>
<body>
{m}
<script>{js}</script>
</body>
</html>
"""


if __name__ == "__main__":
    base = DOCS if LIVE else os.path.join(DOCS, "anteprima", "v2")
    os.makedirs(os.path.join(base, "en"), exist_ok=True)
    for lang, out in (("it", os.path.join(base, "index.html")), ("en", os.path.join(base, "en", "index.html"))):
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(lang))
        print("scritto", os.path.relpath(out, ROOT))

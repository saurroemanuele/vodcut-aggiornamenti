"""Genera la pagina delle clip dal web: docs/clip.html (italiano) e docs/en/clip.html (inglese).
python3 tools/clip_page.py"""
import base64
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

T = {
    "it": {
        "lang": "it", "title": "Clip AI dalla tua live, anche dal telefono | NoonFrame",
        "desc": "Incolla il link della live di Twitch, Kick o YouTube: l'AI trova i momenti migliori e ti dà clip verticali pronte per TikTok, Reels e Shorts.",
        "home": "./", "other": "en/clip.html", "otherLabel": "EN", "privacy": "privacy.html", "terms": "termini.html", "dl": "./#download",
        "h1": "Clip virali dai tuoi video.<br>Anche dal telefono.",
        "sub": "Incolla il link di un video YouTube o di una live: l'AI trova i momenti migliori e li monta in verticale con i sottotitoli, pronti per TikTok, Reels e Shorts.",
        "ph": "Link del video o della live (YouTube, Twitch, Kick)", "go": "Trova le clip",
        "note": "120 crediti gratis per iniziare · accesso con Google",
        "kickB": "Nuovo", "kick": "Dalla live alle clip in pochi minuti, senza installare niente",
        "how1": "Incolla il link", "how1d": "Un video YouTube o il VOD di una live, anche di ore.",
        "how2": "L'AI sceglie", "how2d": "I momenti più forti, con un punteggio per piattaforma.",
        "how3": "Scarica e pubblica", "how3d": "Clip verticali con sottotitoli, in pochi minuti.",
    },
    "en": {
        "lang": "en", "title": "AI clips from your stream, even from your phone | NoonFrame",
        "desc": "Paste your Twitch, Kick or YouTube stream link: AI finds the best moments and gives you vertical clips ready for TikTok, Reels and Shorts.",
        "home": "./", "other": "../clip.html", "otherLabel": "IT", "privacy": "privacy.html", "terms": "terms.html", "dl": "./#download",
        "h1": "Viral clips from your videos.<br>Even from your phone.",
        "sub": "Paste a YouTube video or stream link: AI finds the best moments and edits them vertically with captions, ready for TikTok, Reels and Shorts.",
        "ph": "Video or stream link (YouTube, Twitch, Kick)", "go": "Find clips",
        "note": "120 free credits to start · sign in with Google",
        "kickB": "New", "kick": "From stream to clips in minutes, nothing to install",
        "how1": "Paste the link", "how1d": "A YouTube video or a stream VOD, even hours long.",
        "how2": "AI picks", "how2d": "The strongest moments, scored for each platform.",
        "how3": "Download and post", "how3d": "Vertical clips with captions, in minutes.",
    },
}

# testi usati dal codice della pagina
JS = {
    "it": {
        "login": "Accedi con Google", "logout": "Esci", "credits": "crediti", "badLink": "Questo link non va bene: usa un video di YouTube, twitch.tv/videos/… o kick.com/canale/videos/….", "checking": "Leggo il video…", "estT": "Userà {c} crediti", "estHave": "Ne hai {b}", "estGo": "Crea le clip", "estChange": "Cambia link", "estShort": "Non hai abbastanza crediti per questo video.", "hours": "h",
        "loginFirst": "Accedi con Google per continuare: la tua live parte subito dopo.",
        "inApp": "Google non permette l'accesso dentro l'app che stai usando. Tocca ⋯ in alto e scegli \"Apri nel browser\" (Safari o Chrome). Il link è già copiato: puoi anche incollarlo nel browser.",
        "stages": {"queued": "In coda", "start": "Preparo il lavoro", "download": "Scarico il video", "prepare": "Analizzo il video", "clips": "Trascrivo e scelgo i momenti", "render": "Monto le clip", "upload": "Quasi pronto", "done": "Pronte"},
        "steps": ["Scarico", "Trascrivo", "Scelgo i momenti", "Monto le clip"],
        "working": "Sto lavorando sul tuo video", "leave": "Puoi chiudere la pagina: ti mandiamo un'email quando le clip sono pronte.",
        "cancel": "Annulla", "cancelled": "Annullato: i crediti ti sono stati restituiti.", "ready": "clip pronte", "readyOne": "clip pronta",
        "from": "Dalla live", "download": "Scarica", "best": "Ottima per", "why": "Perché funziona", "score": "punteggio",
        "again": "Fai le clip di un'altra live", "failed": "Non è andata", "retry": "Riprova",
        "history": "Le tue live", "open": "Apri", "statusDone": "Pronte", "statusRun": "In corso", "statusFail": "Non riuscita", "statusCancel": "Annullata",
        "editT": "Vuoi ritoccarle e spendere meno?", "editD": "Con NoonFrame sul computer cambi sottotitoli, tagli, zoom e grafica di ogni clip. E le clip costano molto meno: trascrizione e montaggio li fa gratis il tuo PC.",
        "editDesk": "Scarica NoonFrame", "editMob": "Mandami il link per il PC", "editSent": "Fatto: ti abbiamo mandato il link via email, aprilo dal computer.",
        "noCredits": "Hai finito i crediti: ricarica per continuare.",
        "pf": {"title": "Il tuo profilo", "since": "Su NoonFrame da {d}", "credits": "Crediti", "clips": "Clip create", "hours": "Video trasformato", "plan": "Piano", "free": "Gratis", "renews": "Si rinnova il {d}", "ends": "Attivo fino al {d}", "monthly": "{n} crediti al mese", "topup": "Ricarica crediti", "manage": "Gestisci abbonamento", "upgrade": "Scegli un piano", "reports": "Le tue segnalazioni", "noReports": "Non hai ancora mandato segnalazioni o idee.", "newFb": "Manda un feedback", "reply": "Risposta del team", "app": "Scarica l'app per computer", "appD": "Editor completo, grafica e clip direttamente sul tuo computer", "discord": "Entra nella community su Discord", "discordD": "Aiuto, consigli e anteprime delle novità", "logout": "Esci", "close": "Chiudi", "load": "Carico il profilo…", "st": {"nuova": "Ricevuta", "approvata": "Presa in carico", "in_lavorazione": "In lavorazione", "in_beta": "In prova", "fatta": "Risolta", "chiusa": "Chiusa", "rifiutata": "Chiusa"}, "kinds": {"bug": "Problema", "idea": "Idea"}, "inVer": "nella versione {v}"},
        "fb": {"btn": "Feedback", "title": "Aiutaci a migliorare NoonFrame", "lead": "Lo leggiamo tutti, davvero. Ti rispondiamo qui, nel tuo profilo, e per email.", "kinds": {"bug": ["Qualcosa non va", "Un errore, una clip sbagliata, un pulsante che non risponde"], "idea": ["Idea o modifica", "Una funzione che vorresti, qualcosa da cambiare o migliorare"]}, "ph": {"bug": "Cosa è successo? Cosa stavi facendo e cosa ti aspettavi?", "idea": "Cosa vorresti? Più dettagli ci dai, prima lo costruiamo"}, "shot": "Aggiungi uno screenshot", "shotOk": "Screenshot allegato", "shotRm": "Togli", "job": "Allega il lavoro che hai aperto", "send": "Manda", "sending": "Invio…", "ok": "Ricevuto, grazie!", "okD": "Trovi la tua segnalazione nel profilo: lì vedi a che punto è e le nostre risposte.", "see": "Vedi nel profilo", "again": "Mandane un'altra", "short": "Scrivi qualche parola in più.", "login": "Accedi con Google per mandarci un feedback: così possiamo risponderti."},
        "buy": {"btn": "Ricarica", "t": "Crediti NoonFrame", "lead": "Un credito = un minuto di video trasformato in clip. Scegli come averli.", "have": "Hai {b}", "packs": "Ricarica", "manage": "Gestisci abbonamento", "planNow": "Piano {p}", "mine": "Il tuo piano", "change": "Passa a questo", "changed": "Piano cambiato: la differenza la calcola Stripe, i crediti arrivano in pochi secondi.", "hasSub": "Hai già un abbonamento: per cambiarlo o disdirlo apri la sua pagina.", "billedYear": "{p} all'anno, pagati una volta", "perMoN": "{n} crediti al mese", "once": "Pagamento singolo", "never": "I crediti non scadono", "best": "Conviene di più", "packsD": "Paghi una volta, i crediti non scadono.", "plans": "Abbonamento", "plansD": "Crediti nuovi ogni mese, disdici quando vuoi.", "month": "Mensile", "year": "Annuale", "save": "risparmi {p}%", "perMonth": "/mese", "perYear": "/anno", "credits": "crediti", "perMo": "crediti al mese", "go": "Compra", "sub": "Abbonati", "wait": "Apro il pagamento…", "ok": "Pagamento riuscito: i crediti arrivano in pochi secondi.", "ko": "Pagamento annullato: non ti è stato addebitato nulla.", "secure": "Pagamento sicuro con Stripe · carta, Apple Pay, Google Pay · codici sconto nella pagina di pagamento", "close": "Chiudi", "load": "Carico i prezzi…", "loadErr": "Prezzi non disponibili: riprova tra poco.", "minutes": "≈ {h} di video in clip", "popular": "Il più scelto"},
        "costNote": "Incolla il link: poi scegli sottotitoli e titolo. Costo: 1 credito per ogni minuto di video, hai {b} crediti.",
        "expire": "Le clip restano disponibili per 7 giorni.", "net": "Connessione assente: riprovo…", "err": "Qualcosa non ha funzionato: riprova tra poco.",
        "ed": {"btn": "Modifica", "t": "Modifica la clip", "lay": "Impaginazione", "lays": {"auto": ["Automatica", "Come l'ha scelta l'AI"], "split": ["Webcam + gioco", "Webcam sopra, gioco sotto"], "full": ["Tutto schermo", "Persona o gioco a tutto schermo"], "fit": ["Intero", "Sfondo sfocato sopra e sotto"]},
               "title": "Titolo d'apertura", "noTitle": "Senza titolo", "subs": "Sottotitoli", "noSubs": "Nessuno", "keep": "Come ora", "trim": "Inizio e fine", "start": "Inizio", "end": "Fine",
               "earlier": "prima", "later": "dopo", "len": "Durata: {d}", "free": "Modifiche gratis rimaste per questa clip: {n}", "paid": "Questa modifica costa {c} crediti",
               "save": "Rifai la clip", "cancel": "Annulla", "working": "Rifaccio la clip", "done": "Clip aggiornata", "same": "Non hai cambiato niente", "until": "Puoi modificare le clip fino al {d}"},
        "setT": "Come le vuoi", "stepsT": ["Video", "Stile", "Clip"], "back": "Cambia video", "autoNote": "L'impaginazione la sceglie l'AI clip per clip: webcam sopra e gioco sotto quando giochi, persona a tutto schermo quando parli.", "kindT": "Che video è?", "kindAuto": "Automatico", "kindAutoPod": "Sembra un podcast", "kindAutoGame": "Sembra gaming", "kindAutoNo": "Lo capisce l'AI",
        "kinds": {"podcast": ["Podcast · intervista", "Persona a tutto schermo"], "gaming": ["Gaming con webcam", "Webcam sopra, gioco sotto"], "fit": ["Video intero", "Sfondo sfocato sopra e sotto"]},
        "subsT": "Sottotitoli", "subStyles": {"classico": "Classico", "verde": "Verde", "riquadro": "Riquadro", "pulito": "Pulito", "impatto": "Impatto"},
        "posT": "Posizione", "pos": {"auto": "Automatica", "centro": "Al centro", "basso": "In basso"},
        "wordsT": "Parole per volta", "words": {"parola": "Una", "poche": "Poche", "frase": "Frase"},
        "hookT": "Titolo d'apertura", "hookOn": "Scritta grande nei primi secondi", "hookStyles": {"classico": "Classico", "verde": "Verde", "box": "Riquadro", "neon": "Neon", "pulito": "Pulito", "impatto": "Impatto"},
        "promptT": "Cosa cercare", "promptPh": "Facoltativo. Es. momenti divertenti, opinioni forti, consigli pratici", "subSample": "CHE DOVREBBE", "hookSample": "NON CI CREDO",
        "min": "min", "credUsed": "{n} crediti usati", "expired": "Le clip di questa live sono scadute (restano 7 giorni). Rifalle quando vuoi.",
    },
    "en": {
        "login": "Sign in with Google", "logout": "Sign out", "credits": "credits", "badLink": "This link won't work: use a YouTube video, twitch.tv/videos/… or kick.com/channel/videos/….", "checking": "Reading the video…", "estT": "Will use {c} credits", "estHave": "You have {b}", "estGo": "Create clips", "estChange": "Change link", "estShort": "You don't have enough credits for this video.", "hours": "h",
        "loginFirst": "Sign in with Google to continue: your stream starts right after.",
        "inApp": "Google doesn't allow sign-in inside the app you're using. Tap ⋯ at the top and choose \"Open in browser\" (Safari or Chrome). The link is already copied: you can also paste it in your browser.",
        "stages": {"queued": "Queued", "start": "Getting ready", "download": "Downloading the video", "prepare": "Analyzing the video", "clips": "Transcribing and picking moments", "render": "Editing the clips", "upload": "Almost done", "done": "Ready"},
        "steps": ["Download", "Transcribe", "Pick moments", "Edit clips"],
        "working": "Working on your video", "leave": "You can close this page: we'll email you when your clips are ready.",
        "cancel": "Cancel", "cancelled": "Cancelled: your credits have been refunded.", "ready": "clips ready", "readyOne": "clip ready",
        "from": "From", "download": "Download", "best": "Great for", "why": "Why it works", "score": "score",
        "again": "Clip another stream", "failed": "That didn't work", "retry": "Try again",
        "history": "Your streams", "open": "Open", "statusDone": "Ready", "statusRun": "In progress", "statusFail": "Failed", "statusCancel": "Cancelled",
        "editT": "Want to tweak them and spend less?", "editD": "With NoonFrame on your computer you can change captions, cuts, zooms and graphics of every clip. And clips cost much less: your PC does transcription and editing for free.",
        "editDesk": "Download NoonFrame", "editMob": "Email me the PC link", "editSent": "Done: we emailed you the link, open it on your computer.",
        "noCredits": "You're out of credits: top up to continue.",
        "pf": {"title": "Your profile", "since": "On NoonFrame since {d}", "credits": "Credits", "clips": "Clips made", "hours": "Video turned into clips", "plan": "Plan", "free": "Free", "renews": "Renews on {d}", "ends": "Active until {d}", "monthly": "{n} credits a month", "topup": "Top up credits", "manage": "Manage subscription", "upgrade": "Choose a plan", "reports": "Your feedback", "noReports": "You haven't sent any reports or ideas yet.", "newFb": "Send feedback", "reply": "Reply from the team", "app": "Get the desktop app", "appD": "Full editor, design and clips right on your computer", "discord": "Join the Discord community", "discordD": "Help, tips and early looks at new features", "logout": "Sign out", "close": "Close", "load": "Loading your profile…", "st": {"nuova": "Received", "approvata": "Accepted", "in_lavorazione": "In progress", "in_beta": "In testing", "fatta": "Fixed", "chiusa": "Closed", "rifiutata": "Closed"}, "kinds": {"bug": "Problem", "idea": "Idea"}, "inVer": "in version {v}"},
        "fb": {"btn": "Feedback", "title": "Help us make NoonFrame better", "lead": "We read every message. We'll reply here, in your profile, and by email.", "kinds": {"bug": ["Something's wrong", "An error, a wrong clip, a button that doesn't respond"], "idea": ["Idea or change", "A feature you'd like, something to change or improve"]}, "ph": {"bug": "What happened? What were you doing and what did you expect?", "idea": "What would you like? The more detail, the sooner we build it"}, "shot": "Add a screenshot", "shotOk": "Screenshot attached", "shotRm": "Remove", "job": "Attach the job you have open", "send": "Send", "sending": "Sending…", "ok": "Got it, thanks!", "okD": "You'll find it in your profile, with its status and our replies.", "see": "See in profile", "again": "Send another", "short": "Write a few more words.", "login": "Sign in with Google to send feedback, so we can reply to you."},
        "buy": {"btn": "Top up", "t": "NoonFrame credits", "lead": "One credit = one minute of video turned into clips. Choose how to get them.", "have": "You have {b}", "packs": "Top-up", "manage": "Manage subscription", "planNow": "{p} plan", "mine": "Your plan", "change": "Switch to this", "changed": "Plan changed: Stripe works out the difference, credits arrive in a few seconds.", "hasSub": "You already have a subscription: open its page to change or cancel it.", "billedYear": "{p} a year, billed once", "perMoN": "{n} credits a month", "once": "One-time payment", "never": "Credits never expire", "best": "Best value", "packsD": "Pay once, credits never expire.", "plans": "Subscription", "plansD": "Fresh credits every month, cancel anytime.", "month": "Monthly", "year": "Yearly", "save": "save {p}%", "perMonth": "/mo", "perYear": "/yr", "credits": "credits", "perMo": "credits per month", "go": "Buy", "sub": "Subscribe", "wait": "Opening checkout…", "ok": "Payment complete: your credits arrive in a few seconds.", "ko": "Payment cancelled: you haven't been charged.", "secure": "Secure payment with Stripe · card, Apple Pay, Google Pay · discount codes on the payment page", "close": "Close", "load": "Loading prices…", "loadErr": "Prices unavailable: try again shortly.", "minutes": "≈ {h} of video into clips", "popular": "Most popular"},
        "costNote": "Paste the link, then pick captions and title. Cost: 1 credit per minute of video, you have {b} credits.",
        "expire": "Clips stay available for 7 days.", "net": "No connection: retrying…", "err": "Something went wrong: try again shortly.",
        "ed": {"btn": "Edit", "t": "Edit clip", "lay": "Layout", "lays": {"auto": ["Automatic", "As the AI picked it"], "split": ["Webcam + game", "Webcam on top, game below"], "full": ["Full screen", "Person or game full screen"], "fit": ["Whole video", "Blurred background above and below"]},
               "title": "Opening title", "noTitle": "No title", "subs": "Captions", "noSubs": "None", "keep": "As now", "trim": "Start and end", "start": "Start", "end": "End",
               "earlier": "earlier", "later": "later", "len": "Length: {d}", "free": "Free edits left for this clip: {n}", "paid": "This edit costs {c} credits",
               "save": "Remake clip", "cancel": "Cancel", "working": "Remaking the clip", "done": "Clip updated", "same": "You didn't change anything", "until": "You can edit clips until {d}"},
        "setT": "How you want them", "stepsT": ["Video", "Style", "Clips"], "back": "Change video", "autoNote": "The AI picks the layout clip by clip: webcam on top and game below when you play, person full screen when you talk.", "kindT": "What kind of video?", "kindAuto": "Automatic", "kindAutoPod": "Looks like a podcast", "kindAutoGame": "Looks like gaming", "kindAutoNo": "The AI decides",
        "kinds": {"podcast": ["Podcast · interview", "Person full screen"], "gaming": ["Gaming with webcam", "Webcam on top, game below"], "fit": ["Whole video", "Blurred background above and below"]},
        "subsT": "Captions", "subStyles": {"classico": "Classic", "verde": "Green", "riquadro": "Box", "pulito": "Clean", "impatto": "Impact"},
        "posT": "Position", "pos": {"auto": "Automatic", "centro": "Middle", "basso": "Bottom"},
        "wordsT": "Words at a time", "words": {"parola": "One", "poche": "A few", "frase": "Sentence"},
        "hookT": "Opening title", "hookOn": "Big text in the first seconds", "hookStyles": {"classico": "Classic", "verde": "Green", "box": "Box", "neon": "Neon", "pulito": "Clean", "impatto": "Impact"},
        "promptT": "What to look for", "promptPh": "Optional. E.g. funny moments, strong opinions, practical tips", "subSample": "WHAT SHOULD", "hookSample": "I CAN'T BELIEVE IT",
        "min": "min", "credUsed": "{n} credits used", "expired": "The clips from this stream have expired (they stay for 7 days). You can make them again anytime.",
    },
}

PAGE = r"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://jhoidpugjjvvkjccyrxg.supabase.co https://lh3.googleusercontent.com https://*.ytimg.com https://static-cdn.jtvnw.net https://images.kick.com; media-src https://jhoidpugjjvvkjccyrxg.supabase.co; font-src 'self'; connect-src https://jhoidpugjjvvkjccyrxg.supabase.co; object-src 'none'; base-uri 'self'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://noonframe.com/{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://noonframe.com/shots/og.png">
<meta name="theme-color" content="#050A1C">
<link rel="icon" href="{root}favicon.png">
<style>
@font-face { font-family: "Inter"; font-style: normal; font-display: swap; font-weight: 100 900; src: url({root}fonts/inter-latin-wght-normal.woff2) format("woff2"); }
:root { --ink-0:#050A1C; --ink-1:#0A1430; --ink-2:#0F1C40; --blue:#1E6BFF; --blue-hi:#4C8DFF; --sky:#8CC2FF; --fg:#F2F6FF; --fg-2:#A6B4D4; --fg-3:#6C7DA6;
  --line:rgba(160,190,255,.10); --line-2:rgba(160,190,255,.18); --score:#22C55E; --hook:#FFD60A; --err:#F87171;
  --body:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; min-height: 100vh; background: var(--ink-0); color: var(--fg); font: 16px/1.55 var(--body); -webkit-font-smoothing: antialiased; overflow-x: hidden; }
body::before { content: ""; position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(60% 50% at 50% -6%, rgba(30,107,255,.42), transparent 70%), radial-gradient(40% 35% at 85% 20%, rgba(76,141,255,.10), transparent 70%), radial-gradient(45% 40% at 10% 85%, rgba(76,141,255,.07), transparent 70%); }
a { color: inherit; }
:focus-visible { outline: 2px solid var(--blue-hi); outline-offset: 3px; border-radius: 6px; }
.wrap { width: min(1080px, 100% - 32px); margin-inline: auto; }
main.wrap { width: min(980px, 100% - 32px); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; height: 48px; padding: 0 20px; border-radius: 13px; font: 600 15.5px/1 var(--body);
  text-decoration: none; border: 0; cursor: pointer; transition: background .2s, transform .15s, opacity .2s; white-space: nowrap; color: var(--fg); }
.btn:active { transform: translateY(1px); }
.btn:disabled { opacity: .55; cursor: default; }
.btn svg { width: 18px; height: 18px; flex: none; }
.btn-primary { background: var(--blue); color: #fff; box-shadow: inset 0 1px 0 rgba(255,255,255,.22), 0 10px 30px -12px rgba(30,107,255,.95); }
.btn-primary:hover:not(:disabled) { background: var(--blue-hi); }
.btn-ghost { background: rgba(255,255,255,.06); box-shadow: inset 0 0 0 1px var(--line-2); }
.btn-ghost:hover { background: rgba(255,255,255,.1); }
.btn-sm { height: 36px; padding: 0 13px; border-radius: 10px; font-size: 14px; }
.btn-white { background: #fff; color: #0A1638; }
.link { background: none; border: 0; padding: 0; color: var(--fg-2); font: inherit; font-size: 14px; text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }

header { position: sticky; top: 0; z-index: 10; background: rgba(5,10,28,.72); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid var(--line); }
header .wrap { display: flex; align-items: center; gap: 12px; height: 60px; }
.brand { display: inline-flex; align-items: center; gap: 9px; font-weight: 650; font-size: 16px; letter-spacing: -.02em; text-decoration: none; }
.brand img { width: 26px; height: 26px; }
.grow { flex: 1; }
.langs { display: inline-flex; gap: 2px; padding: 3px; border-radius: 9px; background: rgba(255,255,255,.05); font-size: 12px; font-weight: 600; }
.lang { padding: 4px 8px; border-radius: 7px; color: var(--fg-3); text-decoration: none; }
.lang.on { background: rgba(255,255,255,.1); color: var(--fg); }
.lang:not(.on):hover { color: var(--fg); }
.who { display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; color: var(--fg-2); }
.cred { display: inline-flex; align-items: center; gap: 6px; height: 30px; padding: 0 11px; border-radius: 999px; background: rgba(255,255,255,.06); box-shadow: inset 0 0 0 1px var(--line-2);
  font-weight: 600; color: var(--fg); font-variant-numeric: tabular-nums; font-size: 13.5px; }
.cred i { width: 8px; height: 8px; border-radius: 50%; background: var(--hook); box-shadow: 0 0 10px rgba(255,214,10,.7); }
.avatar { width: 30px; height: 30px; border-radius: 50%; object-fit: cover; background: var(--ink-2); }

.hero { padding: 54px 0 10px; text-align: center; }
h1 { margin: 0 auto; max-width: 15ch; font-size: clamp(36px, 7.2vw, 64px); line-height: 1.02; font-weight: 650; letter-spacing: -.05em; text-wrap: balance;
  background: linear-gradient(180deg, #fff 35%, #A9C2F5); -webkit-background-clip: text; background-clip: text; color: transparent; padding-bottom: .05em; }
.sub { max-width: 560px; margin: 18px auto 0; font-size: clamp(16px, 2vw, 18.5px); color: var(--fg-2); text-wrap: pretty; }

.ask { max-width: 620px; margin: 30px auto 0; padding: 8px; border-radius: 20px; background: rgba(10,20,48,.75); box-shadow: inset 0 0 0 1px var(--line-2), 0 30px 80px -40px rgba(30,107,255,.8);
  display: flex; gap: 8px; }
.ask input { flex: 1; min-width: 0; height: 52px; padding: 0 16px; border: 0; border-radius: 14px; background: rgba(255,255,255,.05); color: var(--fg); font: 16px var(--body); }
.ask input::placeholder { color: var(--fg-3); }
.ask input:focus { outline: none; box-shadow: inset 0 0 0 2px var(--blue-hi); }
.ask .btn { height: 52px; border-radius: 14px; }
.hint { margin: 12px auto 0; font-size: 13.5px; color: var(--fg-3); min-height: 1.4em; }
.hint.err { color: var(--err); }
.plats { display: flex; justify-content: center; gap: 18px; margin-top: 18px; color: var(--fg-3); font-size: 13px; }
.plats span { display: inline-flex; align-items: center; gap: 6px; }
.plats svg { width: 16px; height: 16px; }

.how { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 46px 0 0; }
.how div { padding: 18px; border-radius: 16px; background: rgba(255,255,255,.03); box-shadow: inset 0 0 0 1px var(--line); }
.how b { display: block; font-size: 15.5px; letter-spacing: -.01em; }
.how b em { font-style: normal; color: var(--sky); margin-right: 6px; font-variant-numeric: tabular-nums; }
.how p { margin: 4px 0 0; font-size: 14px; color: var(--fg-2); }
.kick { display: inline-flex; align-items: center; gap: 10px; margin: 0 0 22px; padding: 4px 14px 4px 4px; border-radius: 999px; background: rgba(255,255,255,.05); box-shadow: inset 0 0 0 1px var(--line-2); font-size: 13px; color: var(--fg-2); max-width: 100%; }
.kick b { padding: 3px 9px; border-radius: 999px; background: var(--blue); color: #fff; font-size: 12px; font-weight: 600; flex: none; }
.kick span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.reels { display: flex; justify-content: center; align-items: center; gap: 2%; margin: 44px auto 0; max-width: 820px; perspective: 1200px; }
.reels figure { position: relative; margin: 0; width: 17%; flex: none; transition: transform .4s cubic-bezier(.2,.8,.2,1); }
.reels img { display: block; width: 100%; height: auto; aspect-ratio: 9 / 16; border-radius: 14px; box-shadow: 0 0 0 1px rgba(160,190,255,.18), 0 30px 60px -24px rgba(0,0,0,.9); background: var(--ink-2); }
.reels figure:nth-child(1) { transform: translateY(6%) rotate(-5deg); } .reels figure:nth-child(5) { transform: translateY(6%) rotate(5deg); }
.reels figure:nth-child(2) { transform: translateY(-2%) rotate(-2deg); } .reels figure:nth-child(4) { transform: translateY(-2%) rotate(2deg); }
.reels figure.mid { width: 20%; transform: translateY(-8%); z-index: 1; }
.reels figure.mid img { box-shadow: 0 0 0 1px rgba(140,194,255,.45), 0 40px 80px -24px rgba(30,107,255,.75); }
.reels figure span { position: absolute; top: 8px; left: 8px; padding: 3px 7px; border-radius: 8px; background: rgba(5,10,28,.78); color: var(--score); font: 700 12px/1 var(--body); font-variant-numeric: tabular-nums; backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); box-shadow: inset 0 0 0 1px rgba(34,197,94,.35); }
@media (hover: hover) { .reels:hover figure.mid { transform: translateY(-11%) scale(1.03); } }
.how div { text-align: left; display: grid; grid-template-columns: auto 1fr; column-gap: 12px; align-items: start; }
.how div i { grid-row: span 2; width: 38px; height: 38px; border-radius: 11px; display: grid; place-items: center; background: rgba(30,107,255,.14); color: var(--sky); box-shadow: inset 0 0 0 1px rgba(76,141,255,.25); }
.how div i svg { width: 19px; height: 19px; }
.hero.step2 > .kick, .hero.step2 > .reels { display: none; }
@media (max-width: 640px) { .reels { gap: 3%; margin-top: 34px; } .reels figure { width: 28%; } .reels figure.mid { width: 33%; } .reels figure:nth-child(1), .reels figure:nth-child(5) { display: none; } .kick { font-size: 12px; } }
@media (max-width: 480px) { header:has(#who:not(.hide)) .brand .bt, header:has(#who:not(.hide)) .langs { display: none; } }
@media (max-width: 420px) { .brand .bt { display: none; } .fbk { width: 46px; height: 46px; padding: 0; justify-content: center; } .fbk span { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); } }
@media (prefers-reduced-motion: reduce) { .reels figure { transition: none; } }

.est { max-width: 620px; margin: 16px auto 0; padding: 12px; border-radius: 18px; background: rgba(10,20,48,.8); box-shadow: inset 0 0 0 1px var(--line-2); display: grid; grid-template-columns: 132px 1fr; gap: 14px; text-align: left; align-items: center; }
.est img, .est .ph { width: 132px; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 11px; background: var(--ink-2); }
.est h3 { margin: 0; font-size: 15.5px; line-height: 1.3; letter-spacing: -.01em; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.est .meta { margin: 3px 0 0; font-size: 13px; color: var(--fg-3); }
.est .cost { margin: 8px 0 0; font-size: 14px; color: var(--fg-2); }
.est .cost b { color: var(--hook); font-variant-numeric: tabular-nums; }
.est .acts { grid-column: 1 / -1; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.est .acts .btn { flex: 1; min-width: 180px; }
.hero.step2 > h1, .hero.step2 > .sub, .hero.step2 > .ask, .hero.step2 > .plats, .hero.step2 > .how, .hero.step2 > .hint { display: none; }
.hero.step2 .est { margin-top: 6px; }
.stp { grid-column: 1 / -1; display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--fg-3); }
.stp ol { display: flex; gap: 6px; list-style: none; margin: 0; padding: 0; flex: 1; }
.stp li { display: flex; align-items: center; gap: 6px; }
.stp li + li::before { content: ""; width: 18px; height: 1px; background: var(--line-2); margin-right: 2px; }
.stp li i { font-style: normal; width: 20px; height: 20px; border-radius: 50%; display: grid; place-items: center; font-size: 11.5px; font-weight: 700; background: rgba(255,255,255,.06); color: var(--fg-3); }
.stp li.ok i { background: var(--score); color: #04130A; }
.stp li.on { color: var(--fg); font-weight: 600; }
.stp li.on i { background: var(--blue); color: #fff; }
.note { margin: 0; font-size: 12.5px; color: var(--fg-3); line-height: 1.45; }
.set { grid-column: 1 / -1; border-top: 1px solid var(--line); padding-top: 14px; display: grid; gap: 16px; }
.set h4 { margin: 0 0 8px; font-size: 13px; font-weight: 600; color: var(--fg-2); }
.kinds { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.kind { appearance: none; border: 0; cursor: pointer; text-align: left; padding: 10px; border-radius: 13px; background: rgba(255,255,255,.03); box-shadow: inset 0 0 0 1px var(--line-2); color: var(--fg); font: inherit; display: grid; gap: 8px; align-content: start; }
.kind[aria-checked="true"] { background: rgba(30,107,255,.14); box-shadow: inset 0 0 0 2px var(--blue-hi); }
.kind b { font-size: 13px; line-height: 1.25; font-weight: 600; }
.kind small { font-size: 11.5px; line-height: 1.3; color: var(--fg-3); }
.ph9 { position: relative; width: 30px; height: 52px; border-radius: 6px; background: #13224A; box-shadow: inset 0 0 0 1.5px rgba(160,190,255,.35); overflow: hidden; }
.ph9 i, .ph9 u { position: absolute; display: block; }
.ph9.podcast i { left: 50%; top: 13px; width: 11px; height: 11px; margin-left: -5.5px; border-radius: 50%; background: var(--sky); }
.ph9.podcast u { left: 50%; bottom: -6px; width: 24px; height: 22px; margin-left: -12px; border-radius: 12px 12px 0 0; background: var(--sky); }
.ph9.gaming i { left: 0; right: 0; top: 0; height: 40%; background: rgba(140,194,255,.55); }
.ph9.gaming u { left: 0; right: 0; bottom: 0; height: 60%; background: repeating-linear-gradient(135deg, #2A4C9A 0 5px, #1E3A7A 5px 10px); }
.ph9.fit i { left: 0; right: 0; top: 0; bottom: 0; background: rgba(140,194,255,.18); filter: blur(1px); }
.ph9.fit u { left: 0; right: 0; top: 50%; height: 14px; margin-top: -7px; background: var(--sky); }
.ph9.auto { display: grid; place-items: center; color: var(--hook); }
.ph9.auto svg { width: 16px; height: 16px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { appearance: none; border: 0; cursor: pointer; padding: 8px 11px; border-radius: 11px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); color: var(--fg); font: inherit; display: grid; gap: 4px; justify-items: center; min-width: 88px; }
.chip[aria-checked="true"] { box-shadow: inset 0 0 0 2px var(--blue-hi); background: rgba(30,107,255,.14); }
.chip small { font-size: 11.5px; color: var(--fg-3); }
.chip { overflow: hidden; }
.smp { font-weight: 900; font-size: 13px; letter-spacing: .01em; color: #fff; text-shadow: 0 0 2px #000, 0 1px 2px #000; white-space: nowrap; }
.smp em { font-style: normal; }
.smp.box { background: rgba(0,0,0,.7); padding: 1px 5px; border-radius: 4px; text-shadow: none; }
.smp.hbox { background: #fff; color: #111; padding: 1px 6px; border-radius: 6px; text-shadow: none; }
.smp.low { text-transform: none; font-weight: 800; }
.segs { display: flex; flex-wrap: wrap; gap: 14px 22px; }
.seg { display: inline-flex; padding: 3px; border-radius: 11px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); gap: 2px; }
.seg button { appearance: none; border: 0; cursor: pointer; padding: 7px 12px; border-radius: 8px; background: none; color: var(--fg-2); font: inherit; font-size: 13.5px; }
.seg button[aria-pressed="true"] { background: var(--blue); color: #fff; }
.tog { display: flex; align-items: center; gap: 10px; font-size: 14px; color: var(--fg-2); cursor: pointer; margin-bottom: 10px; }
.tog input { width: 18px; height: 18px; accent-color: var(--blue); }
.hooks.off { opacity: .4; pointer-events: none; }
.set input.q { width: 100%; height: 44px; border-radius: 12px; border: 0; padding: 0 13px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); color: var(--fg); font: inherit; font-size: 14.5px; }
.set input.q::placeholder { color: var(--fg-3); }
.set :focus-visible { outline: 2px solid var(--sky); outline-offset: 2px; }
.est .warn { grid-column: 1 / -1; margin: 0; font-size: 14px; color: var(--err); }
.panel { margin: 30px auto 0; max-width: 620px; padding: 24px; border-radius: 22px; background: rgba(10,20,48,.8); box-shadow: inset 0 0 0 1px var(--line-2); }
.panel h2 { margin: 0; font-size: 21px; letter-spacing: -.02em; line-height: 1.25; }
.panel .src { margin: 6px 0 0; font-size: 13.5px; color: var(--fg-3); word-break: break-all; }
.bar { position: relative; height: 8px; margin: 20px 0 10px; border-radius: 99px; background: rgba(255,255,255,.07); overflow: hidden; }
.bar i { position: absolute; inset: 0 auto 0 0; border-radius: inherit; background: linear-gradient(90deg, var(--blue), var(--sky)); transition: width .8s cubic-bezier(.2,.7,.2,1); }
.bar i::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,.35), transparent); animation: shine 1.6s infinite; }
@keyframes shine { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
.stage { display: flex; justify-content: space-between; font-size: 14px; color: var(--fg-2); font-variant-numeric: tabular-nums; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 18px; }
.steps span { font-size: 12px; color: var(--fg-3); padding-top: 8px; border-top: 2px solid rgba(255,255,255,.08); }
.steps span.on { color: var(--fg); border-color: var(--blue-hi); }
.steps span.ok { color: var(--fg-2); border-color: var(--score); }
.leave { margin: 18px 0 0; font-size: 14px; color: var(--fg-2); }
.panel .row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; align-items: center; }
.msg-err { color: var(--err); font-size: 15px; margin: 10px 0 0; }

.done-h { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin: 36px 0 14px; flex-wrap: wrap; }
.done-h h2 { margin: 0; font-size: clamp(24px, 4vw, 32px); letter-spacing: -.035em; line-height: 1.1; }
.done-h h2 span { color: var(--score); font-variant-numeric: tabular-nums; }
.done-h p { margin: 6px 0 0; font-size: 14px; color: var(--fg-3); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.clip { display: flex; flex-direction: column; border-radius: 18px; overflow: hidden; background: rgba(10,20,48,.85); box-shadow: inset 0 0 0 1px var(--line-2); }
.vid { position: relative; aspect-ratio: 9 / 16; background: #000; }
.vid video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; background: #000; }
/* a schermo intero la clip resta verticale (barre nere ai lati), mai tagliata per riempire lo schermo */
.vid video:fullscreen { object-fit: contain !important; width: 100%; height: 100%; }
.vid video:-webkit-full-screen { object-fit: contain !important; width: 100%; height: 100%; }
.play { position: absolute; inset: 0; z-index: 1; display: grid; place-items: center; border: 0; padding: 0; background: linear-gradient(180deg, transparent 55%, rgba(5,10,28,.55)); cursor: pointer; }
.play span { width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.92); box-shadow: 0 10px 30px rgba(0,0,0,.45); transition: transform .15s; }
.play:hover span { transform: scale(1.06); }
.play svg { width: 22px; height: 22px; margin-left: 3px; fill: #0A1638; }
.badge { position: absolute; top: 10px; left: 10px; z-index: 2; display: inline-flex; align-items: baseline; gap: 4px; padding: 5px 9px; border-radius: 10px;
  background: rgba(5,10,28,.78); backdrop-filter: blur(8px); font-weight: 700; font-size: 17px; color: var(--score); font-variant-numeric: tabular-nums; pointer-events: none; }
.badge small { font-size: 11px; font-weight: 600; color: var(--fg-2); }
.clip .body { padding: 14px 14px 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.clip h3 { margin: 0; font-size: 15.5px; line-height: 1.3; letter-spacing: -.01em; }
.pf { display: inline-flex; align-self: flex-start; align-items: center; gap: 6px; font-size: 12.5px; color: var(--fg-2); padding: 4px 9px; border-radius: 999px; background: rgba(255,255,255,.06); }
.pf b { color: var(--fg); }
.clip details { font-size: 13.5px; color: var(--fg-2); }
.clip summary { cursor: pointer; color: var(--fg-3); font-size: 13px; }
.clip details p { margin: 6px 0 0; }
.clip .btn { margin-top: auto; height: 42px; font-size: 14.5px; }

.cacts { display: flex; gap: 8px; margin-top: auto; }
.cacts .btn-primary { flex: 1; }
.cacts .btn-ed { flex: none; height: 42px; padding: 0 12px; border-radius: 12px; font-size: 14px; }
.vbusy { position: absolute; inset: 0; z-index: 3; display: grid; place-content: center; justify-items: center; gap: 10px; padding: 14px; text-align: center; background: rgba(5,10,28,.82); backdrop-filter: blur(4px); font-size: 13.5px; color: var(--fg-2); }
.vbusy b { color: var(--fg); font-size: 14.5px; }
.spin { width: 28px; height: 28px; border-radius: 50%; border: 3px solid rgba(255,255,255,.12); border-top-color: var(--sky); animation: rot .9s linear infinite; }
@keyframes rot { to { transform: rotate(360deg); } }
.cerr { margin: 0; font-size: 13px; color: var(--err); }
.edlg { position: fixed; inset: 0; z-index: 50; display: grid; place-items: center; padding: 16px; background: rgba(2,6,18,.72); backdrop-filter: blur(6px); }
.edlg .ebox { width: min(620px, 100%); max-height: calc(100dvh - 32px); overflow: auto; border-radius: 22px; background: #0A1430; box-shadow: inset 0 0 0 1px var(--line-2), 0 40px 80px -30px #000; padding: 20px; display: grid; gap: 16px; }
.edlg h2 { margin: 0; font-size: 19px; letter-spacing: -.02em; }
.edlg h4 { margin: 0 0 8px; font-size: 13px; font-weight: 600; color: var(--fg-2); }
.edlg .kinds { grid-template-columns: repeat(4, 1fr); }
.edlg input.q { width: 100%; height: 44px; border-radius: 12px; border: 0; padding: 0 13px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); color: var(--fg); font: inherit; font-size: 15px; }
.edlg input.q:disabled { opacity: .4; }
.trims { display: flex; flex-wrap: wrap; gap: 12px 22px; align-items: center; }
.trim { display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--fg-2); }
.trim b { min-width: 74px; text-align: center; color: var(--fg); font-variant-numeric: tabular-nums; }
.trim button { appearance: none; border: 0; cursor: pointer; width: 38px; height: 34px; border-radius: 10px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); color: var(--fg); font: inherit; font-size: 13px; }
.edlg .foot { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; position: sticky; bottom: -20px; margin: 0 -20px -20px; padding: 14px 20px 20px; background: #0A1430; border-top: 1px solid var(--line); }
.edlg .foot small { flex: 1 1 100%; font-size: 13px; color: var(--fg-3); }
.edlg .foot .btn-primary { flex: 1; }
.edlg .foot .btn { height: 46px; }
.edlg :focus-visible { outline: 2px solid var(--sky); outline-offset: 2px; }
.topup { height: 32px; padding: 0 12px; font-size: 13.5px; }
.avbtn { position: relative; width: 34px; height: 34px; padding: 0; border: 0; border-radius: 50%; background: linear-gradient(140deg, #4C8DFF, #1E6BFF); color: #fff; cursor: pointer; display: grid; place-items: center; flex: none; box-shadow: 0 0 0 2px rgba(255,255,255,.08); transition: box-shadow .15s; }
.avbtn:hover { box-shadow: 0 0 0 2px rgba(140,194,255,.55); }
.avbtn .avatar { position: absolute; inset: 0; width: 100%; height: 100%; }
.avi { font: 700 14px/1 var(--body); }
/* feedback: sempre a portata di pollice */
.fbk { position: fixed; right: 18px; bottom: calc(18px + env(safe-area-inset-bottom)); z-index: 30; display: inline-flex; align-items: center; gap: 8px; height: 44px; padding: 0 16px 0 13px; border: 0; border-radius: 999px;
  background: rgba(15,28,64,.92); color: var(--fg); font: 600 14px/1 var(--body); cursor: pointer; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  box-shadow: inset 0 0 0 1px var(--line-2), 0 14px 34px -12px rgba(0,0,0,.8); transition: transform .15s, background .15s; }
.fbk:hover { background: rgba(30,107,255,.95); transform: translateY(-1px); }
.fbk svg { width: 18px; height: 18px; }
.edlg .bx { position: absolute; top: 14px; right: 14px; width: 34px; height: 34px; border-radius: 50%; border: 0; background: rgba(255,255,255,.06); color: var(--fg-2); display: grid; place-items: center; cursor: pointer; z-index: 2; }
.edlg .bx:hover { background: rgba(255,255,255,.12); color: var(--fg); }
.edlg .bx svg { width: 15px; height: 15px; }
/* profilo */
.pdlg .ebox, .fdlg .ebox { width: min(560px, 100%); padding: 0; gap: 0; position: relative; }
.phead { display: flex; gap: 16px; align-items: center; padding: 26px 24px 20px; background: radial-gradient(90% 140% at 0% 0%, rgba(30,107,255,.28), transparent 60%); border-bottom: 1px solid var(--line); }
.pav { position: relative; width: 64px; height: 64px; border-radius: 50%; flex: none; display: grid; place-items: center; overflow: hidden; background: linear-gradient(140deg, #4C8DFF, #1E6BFF); box-shadow: 0 0 0 3px rgba(255,255,255,.08); }
.pav img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.pav b { font-size: 26px; }
.pwho { min-width: 0; padding-right: 30px; }
.pwho h2 { margin: 0; font-size: 21px; letter-spacing: -.02em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pwho p { margin: 2px 0 0; color: var(--fg-2); font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pwho .psince { color: var(--fg-3); font-size: 12.5px; }
.pbody { padding: 18px 24px 22px; display: grid; gap: 16px; }
.pstats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.pstats div { display: grid; gap: 2px; padding: 12px; border-radius: 14px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line); }
.pstats b { font-size: 22px; letter-spacing: -.03em; font-variant-numeric: tabular-nums; }
.pstats span { font-size: 12px; color: var(--fg-3); }
.pplan { display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap; padding: 14px 16px; border-radius: 16px; background: linear-gradient(120deg, rgba(30,107,255,.16), rgba(30,107,255,.03)); box-shadow: inset 0 0 0 1px rgba(76,141,255,.3); }
.pplan > div:first-child { display: grid; gap: 1px; }
.pplan .muted { font-size: 12px; color: var(--fg-3); }
.pplan b { font-size: 17px; }
.pplan small { font-size: 12.5px; color: var(--fg-2); }
.pplan-a { display: flex; gap: 8px; flex-wrap: wrap; }
.prep-h { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; margin-bottom: 8px; }
.prep h3 { margin: 0; font-size: 15px; }
.prep ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; max-height: 300px; overflow: auto; }
.prep li { padding: 12px 14px; border-radius: 14px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line); }
.prep li p { margin: 6px 0 0; font-size: 14px; color: var(--fg-2); white-space: pre-wrap; overflow-wrap: anywhere; }
.prep-t { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; font-size: 12px; }
.prep-t time { margin-left: auto; color: var(--fg-3); }
.rk { padding: 2px 8px; border-radius: 99px; font-weight: 650; background: rgba(255,255,255,.08); color: var(--fg-2); }
.rk.bug { background: rgba(248,113,113,.14); color: #FCA5A5; } .rk.idea { background: rgba(140,194,255,.14); color: var(--sky); }
.rst { padding: 2px 8px; border-radius: 99px; background: rgba(255,214,10,.12); color: var(--hook); font-weight: 600; }
.rst.fatta { background: rgba(34,197,94,.14); color: #5BE0A7; } .rst.chiusa, .rst.rifiutata { background: rgba(255,255,255,.07); color: var(--fg-3); }
.prep-r { margin-top: 10px; padding: 10px 12px; border-radius: 12px; background: rgba(30,107,255,.12); border-left: 3px solid var(--blue-hi); }
.prep-r b { font-size: 12px; color: var(--sky); }
.prep-r p { margin: 4px 0 0 !important; color: var(--fg) !important; }
.pempty { margin: 0; font-size: 14px; color: var(--fg-3); }
.plinks { display: grid; gap: 8px; }
.plinks a { display: grid; gap: 2px; padding: 12px 14px; border-radius: 14px; text-decoration: none; background: rgba(255,255,255,.04); box-shadow: inset 0 0 0 1px var(--line); transition: background .15s; }
.plinks a:hover { background: rgba(255,255,255,.08); }
.plinks b { font-size: 14.5px; } .plinks span { font-size: 12.5px; color: var(--fg-3); }
.plogout { justify-self: start; color: var(--fg-3); }
/* feedback */
.fhead { padding: 26px 24px 16px; background: radial-gradient(90% 140% at 0% 0%, rgba(30,107,255,.24), transparent 60%); border-bottom: 1px solid var(--line); }
.fhead h2 { margin: 0; padding-right: 36px; font-size: 21px; letter-spacing: -.02em; }
.fhead p { margin: 6px 0 0; color: var(--fg-2); font-size: 14px; }
.fbody { padding: 18px 24px 22px; display: grid; gap: 12px; }
.fkinds { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.fkind { display: grid; gap: 3px; text-align: left; padding: 12px 14px; border: 0; border-radius: 14px; background: #0B1638; color: var(--fg); font: inherit; cursor: pointer; box-shadow: inset 0 0 0 1px var(--line-2); }
.fkind b { font-size: 14.5px; } .fkind span { font-size: 12.5px; color: var(--fg-3); line-height: 1.4; }
.fkind[aria-checked="true"] { box-shadow: inset 0 0 0 2px var(--blue-hi); background: rgba(30,107,255,.12); }
.fkind.bug[aria-checked="true"] { box-shadow: inset 0 0 0 2px #F87171; background: rgba(248,113,113,.10); }
.fbody textarea { width: 100%; min-height: 130px; resize: vertical; border: 0; border-radius: 14px; padding: 12px 14px; background: #0B1638; color: var(--fg); font: 15px/1.5 var(--body); box-shadow: inset 0 0 0 1px var(--line-2); }
.fbody textarea:focus { outline: none; box-shadow: inset 0 0 0 2px var(--blue-hi); }
.fextra { display: flex; gap: 10px 16px; flex-wrap: wrap; align-items: center; font-size: 13.5px; color: var(--fg-2); }
.fshot { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; color: var(--sky); }
.fshot img { width: 34px; height: 34px; object-fit: cover; border-radius: 8px; }
.fjob { margin: 0; }
.fmsg { margin: 0; min-height: 0; font-size: 13.5px; } .fmsg.err { color: var(--err); }
.fact { display: flex; gap: 8px; flex-wrap: wrap; }
.fact .btn-primary { flex: 1; }
.fok { display: grid; justify-items: center; text-align: center; gap: 8px; padding: 10px 0 4px; }
.fok-i { width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; background: rgba(34,197,94,.16); color: #5BE0A7; }
.fok-i svg { width: 28px; height: 28px; }
.fok h3 { margin: 4px 0 0; font-size: 20px; } .fok p { margin: 0; color: var(--fg-2); font-size: 14px; max-width: 40ch; }
.fok .fact { width: 100%; margin-top: 8px; }
@media (max-width: 640px) { .fbk { right: 12px; bottom: calc(12px + env(safe-area-inset-bottom)); height: 42px; padding: 0 14px 0 12px; } .fkinds { grid-template-columns: 1fr; } .pstats b { font-size: 19px; } .phead { padding: 22px 18px 16px; } .pbody, .fbody { padding: 16px 18px 18px; } .fhead { padding: 22px 18px 14px; } }
@media (prefers-reduced-motion: reduce) { .fbk { transition: none; } }
.bdlg .ebox { width: min(760px, 100%); padding: 0; gap: 0; position: relative; }
.bx { position: absolute; top: 14px; right: 14px; width: 34px; height: 34px; border-radius: 50%; border: 0; background: rgba(255,255,255,.06); color: var(--fg-2); display: grid; place-items: center; cursor: pointer; z-index: 2; }
.bx:hover { background: rgba(255,255,255,.12); color: var(--fg); }
.bx svg { width: 15px; height: 15px; }
.bhero { padding: 26px 24px 18px; display: grid; gap: 6px; background: radial-gradient(80% 120% at 0% 0%, rgba(30,107,255,.22), transparent 60%); border-bottom: 1px solid var(--line); }
.bhero h2 { margin: 0; font-size: 22px; letter-spacing: -.02em; }
.bhero p { margin: 0; color: var(--fg-2); font-size: 14px; }
.bbal { display: inline-flex; align-items: center; gap: 8px; margin-top: 6px; width: max-content; padding: 6px 12px 6px 8px; border-radius: 99px; background: rgba(255,255,255,.06); font-size: 13.5px; color: var(--fg-2); }
.bbal b { color: var(--fg); font-variant-numeric: tabular-nums; }
.bbal i { width: 18px; height: 18px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #FFE680, #F5B300 70%); box-shadow: 0 0 10px rgba(255,214,10,.35); }
.bbal .pl { padding-left: 8px; margin-left: 2px; border-left: 1px solid var(--line-2); }
.bbody { padding: 18px 24px 22px; display: grid; gap: 16px; }
.btabs { display: grid; grid-template-columns: 1fr 1fr; padding: 4px; gap: 4px; border-radius: 13px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line); }
.btabs button { height: 40px; border: 0; border-radius: 10px; background: none; color: var(--fg-2); font: 600 14.5px/1 var(--body); cursor: pointer; }
.btabs button[aria-selected="true"] { background: rgba(255,255,255,.09); color: var(--fg); box-shadow: 0 1px 2px rgba(0,0,0,.35); }
.bper { display: flex; justify-content: center; }
.bper .seg em { font-style: normal; font-size: 11.5px; font-weight: 700; color: #052A1C; background: var(--score); border-radius: 99px; padding: 1px 7px; margin-left: 6px; }
.bitems { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
.bitem { position: relative; display: flex; flex-direction: column; gap: 6px; padding: 18px 16px 16px; border-radius: 18px; background: #0B1638; box-shadow: inset 0 0 0 1px var(--line-2); }
.bitem.pop { background: linear-gradient(180deg, rgba(30,107,255,.16), rgba(30,107,255,.03) 55%), #0B1638; box-shadow: inset 0 0 0 1.5px var(--blue-hi), 0 20px 40px -24px rgba(30,107,255,.8); }
.bitem.hl { box-shadow: inset 0 0 0 2px var(--sky); }
.bitem .nm { font-weight: 650; font-size: 15px; display: flex; align-items: center; gap: 8px; }
.bitem .pr { font-size: 30px; font-weight: 750; letter-spacing: -.035em; line-height: 1.1; font-variant-numeric: tabular-nums; }
.bitem .pr small { font-size: 13.5px; font-weight: 500; letter-spacing: 0; color: var(--fg-3); margin-left: 3px; }
.bitem .bsub { margin-top: -2px; font-size: 12.5px; color: var(--fg-3); min-height: 17px; }
.bitem .cr { display: flex; align-items: center; gap: 7px; margin-top: 6px; font-size: 14px; font-weight: 600; color: var(--fg); }
.bitem .cr i { width: 14px; height: 14px; border-radius: 50%; flex: none; background: radial-gradient(circle at 35% 30%, #FFE680, #F5B300 70%); }
.bitem ul { list-style: none; margin: 4px 0 0; padding: 0; display: grid; gap: 5px; color: var(--fg-2); font-size: 13px; }
.bitem li { display: flex; gap: 7px; align-items: flex-start; }
.bitem li::before { content: ""; flex: none; width: 13px; height: 13px; margin-top: 2px; background: var(--score); -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12.5l4.5 4.5L19 7'/%3E%3C/svg%3E") center / contain no-repeat; mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 12.5l4.5 4.5L19 7'/%3E%3C/svg%3E") center / contain no-repeat; }
.bitem .btn { margin-top: auto; width: 100%; height: 44px; font-size: 15px; }
.bitem .gap { flex: 1; min-height: 12px; }
.bitem .tag { position: absolute; top: -10px; left: 16px; background: var(--blue); color: #fff; font-size: 11.5px; font-weight: 650; padding: 3px 9px; border-radius: 99px; }
.bitem .mine { font-size: 11px; font-weight: 650; padding: 2px 8px; border-radius: 99px; background: rgba(34,197,94,.16); color: #5BE0A7; }
.bmsg { margin: 0; padding: 11px 14px; border-radius: 12px; background: rgba(255,214,10,.08); color: var(--hook); font-size: 14px; display: flex; gap: 10px; align-items: center; justify-content: space-between; flex-wrap: wrap; }
.bmsg.err { background: rgba(248,113,113,.1); color: var(--err); }
.bfoot { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: space-between; padding: 14px 24px 18px; border-top: 1px solid var(--line); color: var(--fg-3); font-size: 12.5px; }
.bfoot span { display: inline-flex; gap: 8px; align-items: center; }
.bfoot svg { width: 14px; height: 14px; flex: none; }
.bsecure { margin: 0; color: var(--fg-3); font-size: 12.5px; }
@media (max-width: 640px) { .bitem { padding: 16px 14px 14px; } .bitem ul { display: none; } .bitems { gap: 14px; } .bhero { padding: 22px 18px 16px; } .bbody { padding: 16px 18px 18px; } .bfoot { padding: 12px 18px 16px; } .bitem .pr { font-size: 27px; } }
.edit { margin: 28px 0 0; padding: 24px; border-radius: 22px; display: grid; grid-template-columns: 1fr auto; gap: 18px; align-items: center;
  background: linear-gradient(135deg, #1E6BFF, #3B4FD8); box-shadow: 0 30px 70px -35px rgba(30,107,255,.9); }
.edit h3 { margin: 0; font-size: 21px; letter-spacing: -.02em; }
.edit p { margin: 6px 0 0; font-size: 15px; color: rgba(255,255,255,.85); max-width: 52ch; }
.edit .ok { grid-column: 1 / -1; margin: 0; font-size: 14px; color: #fff; }

.hist { margin: 44px 0 0; }
.hist h2 { font-size: 15px; color: var(--fg-3); font-weight: 600; margin: 0 0 10px; }
.hist ul { list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--line); }
.hist li { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--line); font-size: 14.5px; }
.hist li .t { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hist li .s { font-size: 12.5px; color: var(--fg-3); }
.hist li .s.done { color: var(--score); }
.hist li .s.failed { color: var(--err); }

footer { margin: 70px 0 0; padding: 26px 0 40px; border-top: 1px solid var(--line); font-size: 13px; color: var(--fg-3); }
footer .wrap { display: flex; gap: 16px; flex-wrap: wrap; }
footer a { color: var(--fg-3); }
.hide { display: none !important; }

@media (max-width: 640px) {
  .hero { padding-top: 34px; }
  .ask { flex-direction: column; padding: 8px; }
  .ask .btn { width: 100%; }
  .ask input { flex: none; }
  .est { grid-template-columns: 104px 1fr; gap: 12px; }
  .est img, .est .ph { width: 104px; }
  .kinds { grid-template-columns: repeat(2, 1fr); }
  .chip { min-width: 0; flex: 1 1 40%; padding: 8px 6px; }
  .smp { font-size: 12px; }
  .how { grid-template-columns: 1fr; gap: 8px; margin-top: 34px; }
  .grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .clip .body { padding: 11px 11px 13px; }
  .clip h3 { font-size: 14px; }
  .clip details { display: none; }
  .edit { grid-template-columns: 1fr; padding: 20px; }
  .edlg { padding: 0; place-items: end stretch; }
  .edlg .ebox { border-radius: 22px 22px 0 0; max-height: 92dvh; }
  .edlg .kinds { grid-template-columns: repeat(2, 1fr); }
  .cacts { flex-direction: column; }
  .cacts .btn-primary { flex: none; }
  .cacts .btn-ed { width: 100%; }
  .edit .btn { width: 100%; }
  .who .mail { display: none; }
  .panel { padding: 20px; }
}
@media (prefers-reduced-motion: reduce) { .bar i, .bar i::after { transition: none; animation: none; } }
</style>
</head>
<body>
<header><div class="wrap">
  <a class="brand" href="{home}"><img src="{root}logo.png" alt="" width="26" height="26"><span class="bt">NoonFrame</span></a>
  <span class="grow"></span>
  <span class="who hide" id="who"><span class="cred" title=""><i></i><span id="bal">0</span></span><button class="btn btn-primary btn-sm topup" id="topup" type="button"></button><button class="avbtn" id="me" type="button" aria-haspopup="dialog"><img class="avatar hide" id="av" alt=""><span class="avi" id="avi" aria-hidden="true"></span></button></span>
  <button class="btn btn-ghost btn-sm hide" id="in" type="button"></button>
  <span class="langs">{langsHtml}</span>
</div></header>

<main class="wrap">
  <section class="hero" id="hero">
    <p class="kick"><b>{kickB}</b><span>{kick}</span></p>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <form class="ask" id="ask" novalidate>
      <input id="url" type="url" inputmode="url" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="{ph}" aria-label="{ph}">
      <button class="btn btn-primary" id="go" type="submit"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></svg><span>{go}</span></button>
    </form>
    <div class="est hide" id="est" aria-live="polite"></div>
    <p class="hint" id="hint" role="status">{note}</p>
    <div class="plats" aria-hidden="true">
      <span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 2 2.5 6v14h5v3h3l3-3h4L22 15.5V2H4zm16 12.5-3 3h-5l-3 3v-3H5V4h15v10.5zM16 7h2v6h-2V7zm-5 0h2v6h-2V7z"/></svg>Twitch</span>
      <span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 3h6v4h2V5h2V3h8v6h-2v2h-2v2h2v2h2v6h-8v-2h-2v-2H9v4H3V3z"/></svg>Kick</span>
      <span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.8 3-5.8 3z"/></svg>YouTube</span>
    </div>
    <div class="reels" aria-hidden="true">
      <figure><img src="{root}shots/reel1.webp" alt="" width="360" height="640" loading="lazy"><span>84</span></figure>
      <figure><img src="{root}shots/reel3.webp" alt="" width="360" height="640" loading="lazy"><span>91</span></figure>
      <figure class="mid"><img src="{root}shots/reel0.webp" alt="" width="360" height="640"><span>97</span></figure>
      <figure><img src="{root}shots/reel5.webp" alt="" width="360" height="640" loading="lazy"><span>89</span></figure>
      <figure><img src="{root}shots/reel7.webp" alt="" width="360" height="640" loading="lazy"><span>82</span></figure>
    </div>
    <div class="how">
      <div><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg></i><b><em>1</em>{how1}</b><p>{how1d}</p></div>
      <div><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/></svg></i><b><em>2</em>{how2}</b><p>{how2d}</p></div>
      <div><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg></i><b><em>3</em>{how3}</b><p>{how3d}</p></div>
    </div>
  </section>

  <section id="run" class="panel hide" aria-live="polite"></section>
  <section id="done" class="hide"></section>
  <section id="hist" class="hist hide"></section>
</main>

<button class="fbk" id="fbk" type="button" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.8 7L4 20l1.1-4.6A8 8 0 1 1 21 12z"/><path d="M9 11h6M9 14h4"/></svg><span id="fbkl"></span></button>
<footer><div class="wrap"><span>© NoonFrame</span><a href="{privacy}">Privacy</a><a href="{terms}">{termsLabel}</a><a href="{home}">noonframe.com</a></div></footer>

<script>
// la pagina non si apre dentro altri siti (niente click rubati sul tasto che usa i crediti)
if (window.top !== window.self) { document.documentElement.style.display = 'none'; try { window.top.location = window.location.href; } catch (e) {} }
const L = {js};
const SB = 'https://jhoidpugjjvvkjccyrxg.supabase.co';
const KEY = 'sb_publishable_vam6nGEE5qCrRCXknhoWqQ_GvrpnvzR';
const FN = SB + '/functions/v1/webclip';
const DLFN = SB + '/functions/v1/download-link';
const LINKS = [/^https:\/\/(www\.|m\.)?twitch\.tv\/videos\/\d{5,14}(\?\S*)?$/, /^https:\/\/(www\.)?kick\.com\/[A-Za-z0-9_\-]{2,30}\/videos\/[0-9a-fA-F\-]{8,40}(\?\S*)?$/,
  /^https:\/\/(www\.|m\.)?youtube\.com\/(watch\?v=|live\/)[\w\-]{11}([&?]\S*)?$/, /^https:\/\/youtu\.be\/[\w\-]{11}(\?\S*)?$/];
const mobile = /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || '');
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const store = { get(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } },
  set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
const once = { get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v); } catch (e) {} } };

// ---- accesso con Google (lo stesso account dell'app)
let S = store.get('nf.sess');
function fromHash() {
  if (!location.hash || location.hash.length < 10) return;
  const p = new URLSearchParams(location.hash.slice(1));
  let asked = 0, back = '';
  try { asked = Number(localStorage.getItem('nf.login') || 0); back = localStorage.getItem('nf.back') || ''; localStorage.removeItem('nf.login'); localStorage.removeItem('nf.back'); } catch (e) {}
  // accetta un accesso solo se l'ha chiesto questa scheda da poco (un link preparato da altri non ti fa entrare nel suo account)
  if (p.get('access_token') && asked && Date.now() - asked < 15 * 60000) {
    S = { at: p.get('access_token'), rt: p.get('refresh_token'), exp: Date.now() / 1000 + Number(p.get('expires_in') || 3600) };
    store.set('nf.sess', S);
  }
  if (p.get('error_description')) setHint(p.get('error_description'), true);
  // si torna sempre sull'indirizzo ufficiale della pagina: qui si rimettono i parametri che c'erano (es. ?job=)
  history.replaceState(null, '', location.pathname + (location.search || (/^\?[\w=&%.-]{0,200}$/.test(back) ? back : '')));
}
async function token() {
  if (!S) return null;
  if (S.exp - 90 > Date.now() / 1000) return S.at;
  try {
    const r = await fetch(SB + '/auth/v1/token?grant_type=refresh_token', { method: 'POST', headers: { apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh_token: S.rt }) });
    if (!r.ok) throw new Error('refresh');
    const j = await r.json();
    S = { at: j.access_token, rt: j.refresh_token, exp: Date.now() / 1000 + Number(j.expires_in || 3600) };
    store.set('nf.sess', S);
    return S.at;
  } catch (e) { S = null; store.set('nf.sess', null); return null; }
}
const HOME = 'https://noonframe.com/{canon}';     // l'indirizzo esatto autorizzato per il ritorno da Google (noonframe.com/clip senza .html non lo e')
const IN_APP = /Instagram|FBAN|FBAV|FB_IAB|TikTok|musical_ly|Bytedance|Snapchat|LinkedInApp|\bLine\//i.test(navigator.userAgent || '');
function login() {
  if (IN_APP) {
    // dentro Instagram, TikTok & co. Google blocca l'accesso: si apre la pagina nel browser vero
    const here = HOME + location.search;
    if (/Android/i.test(navigator.userAgent || '')) { location.href = 'intent://' + here.replace(/^https:\/\//, '') + '#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=' + encodeURIComponent(here) + ';end'; }
    try { navigator.clipboard.writeText(here).catch(() => {}); } catch (e) {}
    setHint(L.inApp, true);
    return;
  }
  try { localStorage.setItem('nf.login', String(Date.now())); localStorage.setItem('nf.back', location.search || ''); } catch (e) {}
  location.href = SB + '/auth/v1/authorize?provider=google&redirect_to=' + encodeURIComponent(HOME);
}
function logout() { S = null; store.set('nf.sess', null); location.href = location.pathname; }
function me() {
  try { const p = JSON.parse(atob(S.at.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))); const um = p.user_metadata || {}; return { email: p.email || '', pic: um.avatar_url || um.picture || '', name: um.full_name || um.name || '' }; } catch (e) { return { email: '', pic: '', name: '' }; }
}

async function call(op, body) {
  const t = await token();
  if (!t) { showSignedOut(); throw new Error('auth'); }
  let r;
  try { r = await fetch(FN, { method: 'POST', headers: { Authorization: 'Bearer ' + t, apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(Object.assign({ op }, body || {})) }); }
  catch (e) { const x = new Error(L.net); x.net = true; throw x; }
  const j = await r.json().catch(() => ({}));
  if (r.status === 401) { S = null; store.set('nf.sess', null); showSignedOut(); throw new Error('auth'); }
  if (!r.ok) { const x = new Error(j.error || L.err); x.code = j.code; throw x; }
  return j;
}

// ---- interfaccia
function setHint(t, err) { const h = $('hint'); h.textContent = t; h.classList.toggle('err', !!err); }
function showSignedOut() { $('who').classList.add('hide'); $('in').classList.remove('hide'); }
function showSignedIn(bal) {
  $('in').classList.add('hide'); $('who').classList.remove('hide');
  const m = me(); $('bal').textContent = bal == null ? '…' : bal; $('bal').parentNode.title = L.credits;
  $('avi').textContent = ((m.name || m.email || '?').trim()[0] || '?').toUpperCase();
  if (m.pic) { $('av').onload = () => { $('av').classList.remove('hide'); $('avi').classList.add('hide'); }; $('av').onerror = () => { $('av').classList.add('hide'); $('avi').classList.remove('hide'); }; $('av').src = m.pic; $('av').alt = ''; }
}
$('in').textContent = L.login;
$('in').onclick = login;
$('me').setAttribute('aria-label', L.pf.title); $('me').onclick = () => openProfile();
$('fbkl').textContent = L.fb.btn; $('fbk').onclick = () => openFeedback();
$('topup').textContent = L.buy.btn; $('topup').onclick = () => openBuy(null);
$('bal').parentNode.style.cursor = 'pointer'; $('bal').parentNode.onclick = () => openBuy(null);

let current = null, timer = null, perHour = 30;
const stageIdx = { queued: 0, start: 0, download: 0, prepare: 1, clips: 2, render: 3, upload: 3, done: 4 };

function renderRun(j) {
  const el = $('run');
  el.classList.remove('hide');
  $('done').classList.add('hide');
  if (j.status === 'failed' || j.status === 'cancelled') {
    el.innerHTML = '<h2>' + esc(j.status === 'cancelled' ? L.cancel : L.failed) + '</h2><p class="src">' + esc(j.title || j.url) + '</p>'
      + '<p class="msg-err">' + esc(j.status === 'cancelled' ? L.cancelled : j.error || L.err) + '</p>'
      + '<div class="row"><button class="btn btn-primary" id="retry" type="button">' + esc(L.retry) + '</button></div>';
    $('retry').onclick = () => { $('url').value = j.url; showAsk(); $('url').focus(); };
    return;
  }
  const p = Math.round((j.progress || 0) * 100), si = stageIdx[j.stage] ?? 0;
  el.innerHTML = '<h2>' + esc(L.working) + '</h2><p class="src">' + esc(j.title || j.url) + '</p>'
    + '<div class="bar"><i style="width:' + Math.max(3, p) + '%"></i></div>'
    + '<div class="stage"><span>' + esc(L.stages[j.stage] || j.message || L.stages.queued) + '</span><span>' + p + '%</span></div>'
    + '<div class="steps">' + L.steps.map((s, i) => '<span class="' + (i < si ? 'ok' : i === si ? 'on' : '') + '">' + esc(s) + '</span>').join('') + '</div>'
    + '<p class="leave">' + esc(L.leave) + '</p>'
    + '<div class="row"><button class="link" id="cancel" type="button">' + esc(L.cancel) + '</button>'
    + (j.credits ? '<span class="src" style="margin:0">' + esc(L.credUsed.replace('{n}', j.credits)) + '</span>' : '') + '</div>';
  $('cancel').onclick = async () => { try { await call('cancel', { job: j.id }); poll(j.id, true); } catch (e) {} };
}

function bestPf(pf) {
  if (!pf) return null;
  const names = { tiktok: 'TikTok', reels: 'Reels', shorts: 'Shorts' };
  let k = null; for (const x of Object.keys(names)) if (pf[x] != null && (k == null || pf[x] > pf[k])) k = x;
  return k ? names[k] : null;
}
function fileName(c, j) { return ('noonframe-clip-' + String(c.n).padStart(2, '0')) + '.mp4'; }

const EDIT_FROM = Date.parse('2026-10-09T18:10:00Z');   // i lavori fatti prima non hanno la copia sul server per le modifiche
const canEdit = (j) => !!(j.editUntil && new Date(j.editUntil).getTime() > Date.now() && Date.parse(j.created_at || 0) > EDIT_FROM);
function renderDone(j) {
  const busy = (c) => !!(j.editing && j.editing.n === c.n);
  $('run').classList.add('hide');
  const el = $('done');
  el.classList.remove('hide');
  const n = j.clips.length;
  el.innerHTML = '<div class="done-h"><div><h2><span>' + n + '</span> ' + esc(n === 1 ? L.readyOne : L.ready) + '</h2>'
    + '<p>' + esc((j.title ? L.from + ' ' + j.title + ' · ' : '') + L.expire) + '</p></div>'
    + '<button class="btn btn-ghost btn-sm" id="again" type="button">' + esc(L.again) + '</button></div>'
    + '<div class="grid">' + j.clips.map((c) => {
      const pf = bestPf(c.pf);
      const dl = c.video ? c.video + (c.video.includes('?') ? '&' : '?') + 'download=' + encodeURIComponent(fileName(c, j)) : '';
      return '<article class="clip"><div class="vid">' + (c.score != null ? '<span class="badge">' + Math.round(c.score) + '<small>/100</small></span>' : '')
        + '<video playsinline preload="none"' + (c.poster ? ' poster="' + esc(c.poster) + '"' : '') + ' src="' + esc(c.video || '') + '"></video><button class="play" type="button" aria-label="Play"><span><svg viewBox="0 0 24 24"><path d="M7 4.5v15l13-7.5z"/></svg></span></button>'
        + (busy(c) ? '<div class="vbusy" role="status"><span class="spin"></span><b>' + esc(L.ed.working) + '</b><span>' + esc(j.editing.message || '') + ' · ' + Math.round((j.editing.progress || 0) * 100) + '%</span></div>' : '') + '</div>'
        + '<div class="body"><h3>' + esc(c.name || ('Clip ' + c.n)) + '</h3>'
        + (pf ? '<span class="pf">' + esc(L.best) + ' <b>' + pf + '</b></span>' : '')
        + (c.why ? '<details><summary>' + esc(L.why) + '</summary><p>' + esc(c.why) + '</p></details>' : '')
        + (j.editErr && j.editErr.n === c.n ? '<p class="cerr">' + esc(j.editErr.error) + '</p>' : '')
        + '<div class="cacts">'
        + (dl && !busy(c) ? '<a class="btn btn-primary" href="' + esc(dl) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>' + esc(L.download) + '</a>' : '')
        + (canEdit(j) ? '<button class="btn btn-ghost btn-ed" type="button" data-ed="' + c.n + '"' + (j.editing ? ' disabled' : '') + '>' + esc(L.ed.btn) + '</button>' : '')
        + '</div></div></article>';
    }).join('') + '</div>'
    + '<aside class="edit"><div><h3>' + esc(L.editT) + '</h3><p>' + esc(L.editD) + '</p></div>'
    + (mobile ? '<button class="btn btn-white" id="sendpc" type="button">' + esc(L.editMob) + '</button>' : '<a class="btn btn-white" href="{dl}">' + esc(L.editDesk) + '</a>')
    + '<p class="ok hide" id="sentok">' + esc(L.editSent) + '</p></aside>';
  $('again').onclick = () => { history.replaceState(null, '', location.pathname); showAsk(); $('url').value = ''; $('url').focus(); };
  el.querySelectorAll('[data-ed]').forEach((b) => b.addEventListener('click', () => openEdit(j, j.clips.find((c) => c.n === Number(b.dataset.ed)))));
  // una clip alla volta: quando ne parte una, le altre si fermano
  el.querySelectorAll('video').forEach((v) => v.addEventListener('play', () => el.querySelectorAll('video').forEach((o) => { if (o !== v) o.pause(); })));
  el.querySelectorAll('.play').forEach((b) => b.addEventListener('click', () => { const v = b.previousElementSibling; v.controls = true; b.remove(); v.play().catch(() => {}); }));
  const sp = $('sendpc');
  if (sp) sp.onclick = async () => {
    sp.disabled = true;
    try {
      const r = await fetch(DLFN, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: me().email, lang: LANG, marketing: false, source: 'clip-web', website: '' }) });
      if (!r.ok) throw new Error();
      $('sentok').classList.remove('hide'); sp.classList.add('hide');
    } catch (e) { sp.disabled = false; }
  };
}

function showAsk() { $('hero').classList.remove('hide', 'step2'); $('est').classList.add('hide'); $('run').classList.add('hide'); $('done').classList.add('hide'); setHint(costNote()); }
let bal = null;
function costNote() { return S ? L.costNote.replace('{n}', perHour).replace('{b}', bal == null ? '…' : bal) : '{note}'; }

async function poll(id, now) {
  clearTimeout(timer);
  try {
    const r = await call('status', { job: id });
    bal = r.balance; showSignedIn(bal);
    current = r.job;
    if (current.status === 'done' && current.expired) { showAsk(); $('url').value = current.url; setHint(L.expired); loadHist(); return; }
    if (current.status === 'done') {
      $('hero').classList.add('hide');
      const was = editingN; editingN = current.editing ? current.editing.n : null;
      if (!(document.querySelector('.edlg'))) renderDone(current);
      if (current.editing) { timer = setTimeout(() => poll(id), 4000); return; }
      if (was != null && !current.editErr) toast(L.ed.done);
      loadHist(); return;
    }
    $('hero').classList.add('hide');
    renderRun(current);
    if (current.status === 'queued' || current.status === 'running') timer = setTimeout(() => poll(id), 4000);
    else loadHist();
  } catch (e) {
    if (e.message === 'auth') return;
    if (e.net) timer = setTimeout(() => poll(id), 6000);
    else { showAsk(); setHint(e.message, true); }
  }
}

let editingN = null;
function toast(t) { const d = document.createElement('div'); d.className = 'hint'; d.setAttribute('role', 'status'); d.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:60;background:#13224A;color:#F2F6FF;padding:10px 16px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.4)'; d.textContent = t; document.body.append(d); setTimeout(() => d.remove(), 2600); }
// ---- ricariche e abbonamenti (pagamento su Stripe; i crediti arrivano solo dal webhook firmato)
const PAYFN = SB + '/functions/v1/pay';
const LANG = document.documentElement.lang === 'en' ? 'en' : 'it';
let CAT = null;
async function payCall(body) {
  const t = await token();
  if (!t) { login(); throw new Error('auth'); }
  let r;
  try { r = await fetch(PAYFN, { method: 'POST', headers: { Authorization: 'Bearer ' + t, apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); }
  catch (e) { throw new Error(L.net); }
  const j = await r.json().catch(() => ({}));
  if (r.status === 401) { S = null; store.set('nf.sess', null); showSignedOut(); login(); throw new Error('auth'); }
  if (!r.ok) { const x = new Error((j.error && j.error.message) || L.err); x.code = j.code || (j.error && j.error.code); throw x; }
  return j;
}
async function catalog() {
  if (CAT) return CAT;
  const r = await fetch(PAYFN, { method: 'POST', headers: { apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ op: 'catalog' }) });
  if (!r.ok) throw new Error(L.buy.loadErr);
  CAT = await r.json();
  return CAT;
}
const eur = (v) => new Intl.NumberFormat(LANG === 'en' ? 'en-IE' : 'it-IT', { style: 'currency', currency: 'EUR' }).format(Number(v || 0));
// ---- funzioni del database con l'accesso dell'utente (profilo, feedback)
async function rpc(fn, body) {
  const t = await token();
  if (!t) { showSignedOut(); throw new Error('auth'); }
  let r;
  try { r = await fetch(SB + '/rest/v1/rpc/' + fn, { method: 'POST', headers: { Authorization: 'Bearer ' + t, apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) }); }
  catch (e) { throw new Error(L.net); }
  const j = await r.json().catch(() => ({}));
  if (r.status === 401) { S = null; store.set('nf.sess', null); showSignedOut(); throw new Error('auth'); }
  if (!r.ok) throw new Error((j && j.message && !/^auth$/.test(j.message) ? j.message : L.err));
  return j;
}
const DISCORD = 'https://discord.gg/5cQvNEBfee';
const fmtDay = (iso) => { try { return new Date(iso).toLocaleDateString(LANG === 'en' ? 'en-GB' : 'it-IT', { day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return ''; } };
function dialog(cls, label, html) {
  const dlg = document.createElement('div');
  dlg.className = 'edlg ' + cls;
  dlg.innerHTML = '<div class="ebox" role="dialog" aria-modal="true" aria-label="' + esc(label) + '"><button class="bx" type="button" data-close aria-label="' + esc(L.pf.close) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' + html + '</div>';
  document.body.append(dlg);
  const prev = document.activeElement;
  const close = () => { dlg.remove(); document.removeEventListener('keydown', onKey); try { prev && prev.focus(); } catch (e) {} };
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  dlg.addEventListener('click', (e) => { if (e.target === dlg || e.target.closest('[data-close]')) close(); });
  setTimeout(() => { const f = dlg.querySelector('[data-focus]') || dlg.querySelector('.bx'); try { f.focus(); } catch (e) {} }, 30);
  return { dlg, close };
}
function openProfile() {
  if (!S) { login(); return; }
  if (document.querySelector('.pdlg')) return;
  const P = L.pf, m = me();
  const { dlg, close } = dialog('pdlg', P.title, '<div class="phead"><span class="pav">' + (m.pic ? '<img src="' + esc(m.pic) + '" alt="" referrerpolicy="no-referrer">' : '') + '<b>' + esc(((m.name || m.email || '?').trim()[0] || '?').toUpperCase()) + '</b></span>'
    + '<div class="pwho"><h2>' + esc(m.name || m.email.split('@')[0]) + '</h2><p>' + esc(m.email) + '</p><p class="psince" id="psince"></p></div></div><div class="pbody" id="pbody"><p class="bsecure">' + esc(P.load) + '</p></div>');
  const img = dlg.querySelector('.pav img'); if (img) { img.onload = () => dlg.querySelector('.pav b').classList.add('hide'); img.onerror = () => img.remove(); }
  const body = dlg.querySelector('#pbody');
  rpc('web_profile').then((d) => {
    const w = d.wallet || { balance: bal || 0, plan: 'free' }, sub = d.sub, c = d.clips || {};
    if (d.since) dlg.querySelector('#psince').textContent = P.since.replace('{d}', fmtDay(d.since));
    bal = w.balance; showSignedIn(bal);
    const hrs = (c.minutes || 0) >= 60 ? (Math.round((c.minutes || 0) / 6) / 10).toString().replace('.', LANG === 'en' ? '.' : ',') + ' h' : (c.minutes || 0) + ' min';
    const paid = w.plan && w.plan !== 'free';
    const planLine = sub ? (sub.ends ? P.ends.replace('{d}', fmtDay(sub.ends)) : sub.renews ? P.renews.replace('{d}', fmtDay(sub.renews)) : '') : '';
    const st = (r) => '<span class="rst ' + esc(r.status) + '">' + esc(P.st[r.status] || r.status) + (r.status === 'fatta' && r.version && r.version !== 'web' ? ' · ' + esc(P.inVer.replace('{v}', r.version)) : '') + '</span>';
    body.innerHTML = '<div class="pstats"><div><b>' + Number(w.balance || 0).toLocaleString(LANG === 'en' ? 'en' : 'it') + '</b><span>' + esc(P.credits) + '</span></div><div><b>' + (c.clips || 0) + '</b><span>' + esc(P.clips) + '</span></div><div><b>' + esc(hrs) + '</b><span>' + esc(P.hours) + '</span></div></div>'
      + '<div class="pplan"><div><span class="muted">' + esc(P.plan) + '</span><b>' + esc(paid ? (d.planName || w.plan) : P.free) + '</b>' + (planLine ? '<small>' + esc(planLine) + '</small>' : '') + '</div>'
      + '<div class="pplan-a"><button class="btn btn-primary btn-sm" type="button" id="ptop">' + esc(paid ? P.topup : P.upgrade) + '</button>' + (sub ? '<button class="btn btn-ghost btn-sm" type="button" id="pman">' + esc(P.manage) + '</button>' : '') + '</div></div>'
      + '<section class="prep"><div class="prep-h"><h3>' + esc(P.reports) + '</h3><button class="link" type="button" id="pfb">' + esc(P.newFb) + '</button></div>'
      + ((d.reports || []).length ? '<ul>' + d.reports.map((r) => '<li><div class="prep-t"><span class="rk ' + esc(r.kind) + '">' + esc(P.kinds[r.kind] || r.kind) + '</span>' + st(r) + '<time>' + esc(fmtDay(r.at)) + '</time></div><p>' + esc(r.text) + '</p>'
          + (r.replies || []).map((x) => '<div class="prep-r"><b>' + esc(P.reply) + '</b><p>' + esc(x.body) + '</p></div>').join('') + '</li>').join('') + '</ul>'
        : '<p class="muted pempty">' + esc(P.noReports) + '</p>') + '</section>'
      + '<nav class="plinks"><a href="' + DISCORD + '" target="_blank" rel="noopener noreferrer"><b>' + esc(P.discord) + '</b><span>' + esc(P.discordD) + '</span></a>'
      + (mobile ? '' : '<a href="{dl}"><b>' + esc(P.app) + '</b><span>' + esc(P.appD) + '</span></a>') + '</nav>'
      + '<button class="link plogout" type="button" id="pout">' + esc(P.logout) + '</button>';
    body.querySelector('#ptop').onclick = () => { close(); openBuy(paid ? { kind: 'pack', id: '' } : null); };
    const pm = body.querySelector('#pman'); if (pm) pm.onclick = async () => { pm.disabled = true; try { const r = await payCall({ op: 'portal' }); if (r.url && /^https:\/\/(billing\.stripe\.com|[a-z0-9-]+\.lemonsqueezy\.com)\//.test(r.url)) { location.href = r.url; return; } } catch (e) { if (e.message !== 'auth') toast(e.message); } pm.disabled = false; };
    body.querySelector('#pfb').onclick = () => { close(); openFeedback(); };
    body.querySelector('#pout').onclick = logout;
  }).catch((e) => { if (e.message === 'auth') { close(); return; } body.innerHTML = '<p class="bmsg err">' + esc(e.message) + '</p><button class="link plogout" type="button" id="pout">' + esc(P.logout) + '</button>'; body.querySelector('#pout').onclick = logout; });
}
// immagine allegata: ridotta nel browser (lato lungo 1600 px, JPEG) prima di mandarla
function shrinkImage(file) {
  return new Promise((res, rej) => {
    if (!/^image\/(png|jpeg|webp|gif)$/.test(file.type) || file.size > 25e6) { rej(new Error('img')); return; }
    const fr = new FileReader();
    fr.onerror = () => rej(new Error('img'));
    fr.onload = () => { const im = new Image();
      im.onload = () => { const k = Math.min(1, 1600 / Math.max(im.width, im.height)); const c = document.createElement('canvas'); c.width = Math.round(im.width * k); c.height = Math.round(im.height * k);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); res(c.toDataURL('image/jpeg', 0.82)); };
      im.onerror = () => rej(new Error('img')); im.src = fr.result; };
    fr.readAsDataURL(file);
  });
}
function openFeedback(kind) {
  if (!S) { setHint(L.fb.login); try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) {} setTimeout(login, 900); return; }
  if (document.querySelector('.fdlg')) return;
  const F = L.fb;
  let k = kind === 'bug' ? 'bug' : 'idea', shot = null;
  const job = new URLSearchParams(location.search).get('job');
  const { dlg, close } = dialog('fdlg', F.title, '<div class="fhead"><h2>' + esc(F.title) + '</h2><p>' + esc(F.lead) + '</p></div><div class="fbody" id="fbody"></div>');
  const body = dlg.querySelector('#fbody');
  const form = () => {
    body.innerHTML = '<div class="fkinds" role="radiogroup">' + Object.entries(F.kinds).map(([id, [t, d]]) => '<button type="button" role="radio" class="fkind ' + id + '" data-k="' + id + '" aria-checked="' + (k === id) + '"><b>' + esc(t) + '</b><span>' + esc(d) + '</span></button>').join('') + '</div>'
      + '<textarea id="ftext" maxlength="4000" rows="5" data-focus placeholder="' + esc(F.ph[k]) + '" aria-label="' + esc(F.title) + '"></textarea>'
      + '<div class="fextra"><label class="fshot"><input type="file" accept="image/png,image/jpeg,image/webp" id="ffile" hidden><span id="fshotl">' + esc(F.shot) + '</span></label>'
      + (job && /^[0-9a-f-]{36}$/i.test(job) ? '<label class="tog fjob"><input type="checkbox" id="fjob" checked> ' + esc(F.job) + '</label>' : '') + '</div>'
      + '<p class="fmsg" id="fmsg" role="status"></p><div class="fact"><button class="btn btn-primary" type="button" id="fsend">' + esc(F.send) + '</button></div>';
    const ta = body.querySelector('#ftext');
    try { const draft = once.get('nf.fbdraft'); if (draft) ta.value = draft; } catch (e) {}
    ta.addEventListener('input', () => once.set('nf.fbdraft', ta.value));
    body.querySelectorAll('[data-k]').forEach((b) => b.onclick = () => { k = b.dataset.k; body.querySelectorAll('[data-k]').forEach((x) => x.setAttribute('aria-checked', String(x === b))); ta.placeholder = F.ph[k]; ta.focus(); });
    const fl = body.querySelector('#ffile'), lbl = body.querySelector('#fshotl');
    const paintShot = () => { lbl.innerHTML = shot ? '<img src="' + shot + '" alt=""> ' + esc(F.shotOk) + ' · <u>' + esc(F.shotRm) + '</u>' : esc(F.shot); };
    fl.onchange = async () => { const f = fl.files && fl.files[0]; fl.value = ''; if (!f) return; try { shot = await shrinkImage(f); } catch (e) { shot = null; } paintShot(); };
    lbl.parentNode.addEventListener('click', (e) => { if (shot && e.target.tagName === 'U') { e.preventDefault(); shot = null; paintShot(); } });
    paintShot();
    const send = body.querySelector('#fsend'), msg = body.querySelector('#fmsg');
    send.onclick = async () => {
      const tx = ta.value.trim();
      if (tx.length < 3) { msg.textContent = F.short; msg.className = 'fmsg err'; ta.focus(); return; }
      send.disabled = true; send.textContent = F.sending; msg.textContent = ''; msg.className = 'fmsg';
      const jb = body.querySelector('#fjob');
      try {
        await rpc('web_feedback', { p: { kind: k, text: tx, image: shot, job: jb && jb.checked ? job : null, screen: job ? 'clip-web-job' : 'clip-web', ua: navigator.userAgent, lang: LANG, w: innerWidth, h: innerHeight,
          os: (/(Android|iPhone|iPad|Windows|Mac OS X|Linux)/.exec(navigator.userAgent) || ['web'])[0] } });
        once.set('nf.fbdraft', null);
        body.innerHTML = '<div class="fok"><span class="fok-i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg></span><h3>' + esc(F.ok) + '</h3><p>' + esc(F.okD) + '</p>'
          + '<div class="fact"><button class="btn btn-primary" type="button" id="fsee">' + esc(F.see) + '</button><button class="btn btn-ghost" type="button" id="fagain">' + esc(F.again) + '</button></div></div>';
        body.querySelector('#fsee').onclick = () => { close(); openProfile(); };
        body.querySelector('#fagain').onclick = () => { shot = null; form(); };
      } catch (e) {
        if (e.message === 'auth') { close(); return; }
        msg.textContent = e.message; msg.className = 'fmsg err'; send.disabled = false; send.textContent = F.send;
      }
    };
  };
  form();
}

function openBuy(want) {
  if (!S) { login(); return; }
  if (document.querySelector('.bdlg')) return;
  const B = L.buy;
  let tab = want && want.kind === 'pack' ? 'packs' : 'plans', period = want && want.period === 'year' ? 'year' : 'month', sub = null, note = null;
  const dlg = document.createElement('div');
  dlg.className = 'edlg bdlg';
  dlg.innerHTML = '<div class="ebox" role="dialog" aria-modal="true" aria-labelledby="bttl">'
    + '<button class="bx" type="button" id="bclose" aria-label="' + esc(B.close) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>'
    + '<div class="bhero"><h2 id="bttl">' + esc(B.t) + '</h2><p>' + esc(B.lead) + '</p><span class="bbal" id="bbal"><i></i><span>' + esc(B.have.replace('{b}', '')) + '</span><b>' + (bal == null ? '…' : bal) + '</b></span></div>'
    + '<div class="bbody" id="bbody"><p class="bsecure">' + esc(B.load) + '</p></div>'
    + '<div class="bfoot"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>' + esc(B.secure) + '</span><span id="bmanage"></span></div></div>';
  document.body.append(dlg);
  const prevFocus = document.activeElement;
  const close = () => { dlg.remove(); document.removeEventListener('keydown', onKey); try { prevFocus && prevFocus.focus(); } catch (e) {} };
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });
  dlg.querySelector('#bclose').onclick = close;
  const body = dlg.querySelector('#bbody');
  const hours = (cr) => { const m = Math.round(cr / Math.max(1, perHour) * 60); return m >= 60 ? (Math.round(m / 6) / 10).toString().replace('.', LANG === 'en' ? '.' : ',') + ' h' : m + ' min'; };
  const coinI = '<i></i>';
  const portal = async (btn) => {
    if (btn) btn.disabled = true;
    try { const r = await payCall({ op: 'portal' }); if (r.url && /^https:\/\/(billing\.stripe\.com|[a-z0-9-]+\.lemonsqueezy\.com)\//.test(r.url)) { location.href = r.url; return; } }
    catch (e) { if (e.message !== 'auth') { note = { t: e.message, err: true }; paint(); } }
    if (btn) btn.disabled = false;
  };
  const paintManage = () => {
    const m = dlg.querySelector('#bmanage');
    m.innerHTML = sub ? '<button class="link" type="button" id="bportal">' + esc(B.manage) + '</button>' : '';
    if (sub) m.querySelector('#bportal').onclick = (e) => portal(e.currentTarget);
    const pl = dlg.querySelector('#bbal');
    if (sub && CAT) { const p = CAT.plans.find((x) => x.id === sub.plan); if (p && !pl.querySelector('.pl')) pl.insertAdjacentHTML('beforeend', '<span class="pl">' + esc(B.planNow.replace('{p}', p.name)) + '</span>'); }
  };
  const paint = () => {
    const c = CAT || { plans: [], packs: [] };
    const tg = (x) => (LANG === 'en' ? x.tagline_en : x.tagline) || '';
    const perks = (x) => (LANG === 'en' ? x.perks_en : x.perks) || [];
    const save = Math.max(0, ...c.plans.filter((p) => p.price_year_eur).map((p) => Math.round((1 - p.price_year_eur / (p.price_eur * 12)) * 100)));
    const popId = c.plans.length >= 3 ? c.plans[Math.floor(c.plans.length / 2)].id : (c.plans[0] || {}).id;
    let html = (note ? '<div class="bmsg' + (note.err ? ' err' : '') + '" role="status"><span>' + esc(note.t) + '</span>' + (note.portal ? '<button class="btn btn-ghost btn-sm" type="button" data-portal>' + esc(B.manage) + '</button>' : '') + '</div>' : '')
      + '<div class="btabs" role="tablist"><button type="button" role="tab" data-tab="plans" aria-selected="' + (tab === 'plans') + '">' + esc(B.plans) + '</button><button type="button" role="tab" data-tab="packs" aria-selected="' + (tab === 'packs') + '">' + esc(B.packs) + '</button></div>';
    if (tab === 'plans') {
      html += '<div class="bper"><div class="seg" role="group"><button type="button" data-per="month" aria-pressed="' + (period === 'month') + '">' + esc(B.month) + '</button><button type="button" data-per="year" aria-pressed="' + (period === 'year') + '">' + esc(B.year) + (save ? '<em>−' + save + '%</em>' : '') + '</button></div></div>'
        + '<div class="bitems">' + c.plans.map((x) => {
          const yr = period === 'year' && x.price_year_eur, mine = sub && sub.plan === x.id && (sub.period || 'month') === period, pop = x.id === popId;
          return '<div class="bitem' + (pop ? ' pop' : '') + (want && want.kind === 'plan' && want.id === x.id ? ' hl' : '') + '">' + (pop ? '<span class="tag">' + esc(B.popular) + '</span>' : '')
            + '<span class="nm">' + esc(x.name) + (mine ? '<span class="mine">' + esc(B.mine) + '</span>' : '') + '</span>'
            + '<span class="pr">' + esc(eur(yr ? Math.round(x.price_year_eur / 12 * 100) / 100 : x.price_eur)) + '<small>' + esc(B.perMonth) + '</small></span>'
            + '<span class="bsub">' + esc(yr ? B.billedYear.replace('{p}', eur(x.price_year_eur)) : tg(x)) + '</span>'
            + '<span class="cr">' + coinI + esc(B.perMoN.replace('{n}', x.monthly.toLocaleString(LANG === 'en' ? 'en' : 'it'))) + '</span>'
            + '<ul><li>' + esc(B.minutes.replace('{h}', hours(x.monthly))) + '</li>' + perks(x).map((k) => '<li>' + esc(k) + '</li>').join('') + '</ul><span class="gap"></span>'
            + (mine ? '<button class="btn btn-ghost" type="button" disabled>' + esc(B.mine) + '</button>'
              : '<button class="btn ' + (pop ? 'btn-primary' : 'btn-ghost') + '" type="button" data-buy="plan" data-id="' + esc(x.id) + '">' + esc(sub ? B.change : B.sub) + '</button>') + '</div>';
        }).join('') + '</div>';
    } else {
      html += '<div class="bitems">' + c.packs.map((x, i) => {
        const pop = i === c.packs.length - 1 && c.packs.length > 1;
        return '<div class="bitem' + (pop ? ' pop' : '') + (want && want.kind === 'pack' && want.id === x.id ? ' hl' : '') + '">' + (pop ? '<span class="tag">' + esc(B.best) + '</span>' : '')
          + '<span class="nm">' + esc(x.name) + '</span><span class="pr">' + esc(eur(x.price_eur)) + '</span><span class="bsub">' + esc(B.once) + '</span>'
          + '<span class="cr">' + coinI + esc(x.credits.toLocaleString(LANG === 'en' ? 'en' : 'it') + ' ' + B.credits) + '</span>'
          + '<ul><li>' + esc(B.minutes.replace('{h}', hours(x.credits))) + '</li><li>' + esc(B.never) + '</li></ul><span class="gap"></span>'
          + '<button class="btn ' + (pop ? 'btn-primary' : 'btn-ghost') + '" type="button" data-buy="pack" data-id="' + esc(x.id) + '">' + esc(B.go) + ' · ' + esc(eur(x.price_eur)) + '</button></div>';
      }).join('') + '</div>';
    }
    body.innerHTML = html;
    body.querySelectorAll('[data-tab]').forEach((b) => b.onclick = () => { tab = b.dataset.tab; note = null; paint(); });
    body.querySelectorAll('[data-per]').forEach((b) => b.onclick = () => { period = b.dataset.per; paint(); });
    const pb = body.querySelector('[data-portal]'); if (pb) pb.onclick = () => portal(pb);
    body.querySelectorAll('[data-buy]').forEach((b) => b.onclick = async () => {
      body.querySelectorAll('[data-buy]').forEach((x) => { x.disabled = true; });
      const lab = b.textContent; b.textContent = B.wait;
      try {
        const r = await payCall({ op: 'buy', item: { kind: b.dataset.buy, id: b.dataset.id, period }, lang: LANG, back: 'clip' });
        if (r.url && /^https:\/\/(checkout\.stripe\.com|[a-z0-9-]+\.lemonsqueezy\.com)\//.test(r.url)) { location.href = r.url; return; }
        if (r.changed) { note = { t: B.changed }; setTimeout(loadHist, 3000); paint(); return; }
      } catch (e) {
        if (e.message === 'auth') return;
        // ha gia' un abbonamento fatto altrove: si gestisce dalla pagina dell'abbonamento, che qui c'e'
        note = e.code === 'other_provider' || e.code === 'has_plan' || e.code === 'same_plan' ? { t: e.code === 'same_plan' ? e.message : B.hasSub, portal: true } : { t: e.message, err: e.code !== 'sales_soon' };
        paint(); return;
      }
      b.textContent = lab; body.querySelectorAll('[data-buy]').forEach((x) => { x.disabled = false; });
    });
    if (!dlg.contains(document.activeElement) || document.activeElement === document.body) { const f = body.querySelector('.hl [data-buy]') || body.querySelector('.pop [data-buy]'); if (f) try { f.focus({ preventScroll: true }); } catch (e) {} }
  };
  Promise.all([catalog(), payCall({ op: 'status' }).catch(() => ({}))]).then(([, st]) => { sub = (st && st.sub) || null; paint(); paintManage(); })
    .catch((e) => { body.innerHTML = '<p class="bmsg err">' + esc(e.message || B.loadErr) + '</p>'; });
}
function wantFrom(q) {
  // ?compra=pack-s | plan-pro | plan-pro-year (dalla pagina dei prezzi del sito)
  const m = /^(pack|plan)-([a-z0-9_]{1,30})(?:-(month|year))?$/.exec(q || '');
  return m ? { kind: m[1], id: m[2], period: m[3] || 'month' } : null;
}

function openEdit(j, c) {
  if (!c || j.editing) return;
  const st = { layout: c.layout || 'auto', hook: c.hook || '', hookOff: !c.hook, subs: null, da: 0, db: 0 };
  const startLay = st.layout, startHook = st.hook, startOff = st.hookOff;
  const fmt = (v) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v) + ' s';
  const durOf = () => Math.max(0, Math.round((c.dur || 0) - st.da + st.db));
  const dlg = document.createElement('div');
  dlg.className = 'edlg';
  dlg.innerHTML = '<div class="ebox" role="dialog" aria-modal="true" aria-label="' + esc(L.ed.t) + '">'
    + '<h2>' + esc(L.ed.t) + ' · ' + esc(c.name || ('Clip ' + c.n)) + '</h2>'
    + '<div><h4>' + esc(L.ed.lay) + '</h4><div class="kinds" role="radiogroup">' + Object.entries(L.ed.lays).map(([k, v]) => '<button type="button" class="kind" role="radio" data-lay="' + k + '" aria-checked="' + (st.layout === k) + '"><span class="ph9 ' + ({ auto: 'auto', split: 'gaming', full: 'podcast', fit: 'fit' }[k]) + '">'
      + (k === 'auto' ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.2 6.3L20.5 10l-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-1.7z"/></svg>' : '<i></i><u></u>') + '</span><b>' + esc(v[0]) + '</b><small>' + esc(v[1]) + '</small></button>').join('') + '</div></div>'
    + '<div><h4>' + esc(L.ed.title) + '</h4><input class="q" id="edhook" maxlength="80" value="' + esc(st.hook) + '"' + (st.hookOff ? ' disabled' : '') + '><label class="tog" style="margin:10px 0 0"><input type="checkbox" id="edhookoff"' + (st.hookOff ? ' checked' : '') + '> ' + esc(L.ed.noTitle) + '</label></div>'
    + '<div><h4>' + esc(L.ed.subs) + '</h4><div class="chips" role="radiogroup"><button type="button" class="chip" role="radio" data-es="keep" aria-checked="true"><span class="smp">' + esc(L.ed.keep) + '</span><small>&nbsp;</small></button>'
      + Object.entries(L.subStyles).map(([k, l]) => '<button type="button" class="chip" role="radio" data-es="' + k + '" aria-checked="false">' + sample(L.subSample, SUB_LOOK[k]) + '<small>' + esc(l) + '</small></button>').join('')
      + '<button type="button" class="chip" role="radio" data-es="off" aria-checked="false"><span class="smp low">—</span><small>' + esc(L.ed.noSubs) + '</small></button></div>'
      + '<div class="segs" style="margin-top:12px" id="edpos" hidden><div><h4>' + esc(L.posT) + '</h4><div class="seg" role="group">' + Object.entries(L.pos).map(([k, l]) => '<button type="button" data-ep="' + k + '" aria-pressed="' + (k === 'auto') + '">' + esc(l) + '</button>').join('') + '</div></div></div></div>'
    + '<div><h4>' + esc(L.ed.trim) + '</h4><div class="trims">'
      + '<span class="trim">' + esc(L.ed.start) + ' <button type="button" data-t="da" data-d="-5" aria-label="' + esc(L.ed.start + ' 5 s ' + L.ed.earlier) + '">−5</button><b id="tda">' + fmt(0) + '</b><button type="button" data-t="da" data-d="5" aria-label="' + esc(L.ed.start + ' 5 s ' + L.ed.later) + '">+5</button></span>'
      + '<span class="trim">' + esc(L.ed.end) + ' <button type="button" data-t="db" data-d="-5" aria-label="' + esc(L.ed.end + ' 5 s ' + L.ed.earlier) + '">−5</button><b id="tdb">' + fmt(0) + '</b><button type="button" data-t="db" data-d="5" aria-label="' + esc(L.ed.end + ' 5 s ' + L.ed.later) + '">+5</button></span>'
      + '<small class="trim" id="tlen">' + esc(L.ed.len.replace('{d}', durOf() + ' s')) + '</small></div></div>'
    + '<div class="foot"><small>' + esc(c.editsLeft > 0 ? L.ed.free.replace('{n}', c.editsLeft) : L.ed.paid.replace('{c}', j.editCost || 3)) + '</small>'
      + '<button class="btn btn-ghost" type="button" id="edno">' + esc(L.ed.cancel) + '</button><button class="btn btn-primary" type="button" id="edgo">' + esc(L.ed.save) + '</button></div>'
    + '</div>';
  document.body.append(dlg);
  const box = dlg.querySelector('.ebox');
  const close = () => { dlg.remove(); document.removeEventListener('keydown', onKey); };
  const onKey = (ev) => { if (ev.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  dlg.addEventListener('click', (ev) => { if (ev.target === dlg) close(); });
  box.addEventListener('click', (ev) => {
    const t = ev.target.closest('button'); if (!t) return;
    if (t.dataset.lay) { st.layout = t.dataset.lay; box.querySelectorAll('[data-lay]').forEach((x) => x.setAttribute('aria-checked', String(x === t))); }
    else if (t.dataset.es) {
      box.querySelectorAll('[data-es]').forEach((x) => x.setAttribute('aria-checked', String(x === t)));
      st.subs = t.dataset.es === 'keep' ? null : t.dataset.es === 'off' ? { on: false } : { style: t.dataset.es, pos: (st.subs && st.subs.pos) || 'auto', words: 'poche' };
      box.querySelector('#edpos').hidden = !(st.subs && st.subs.style);
    } else if (t.dataset.ep) { if (st.subs && st.subs.style) st.subs.pos = t.dataset.ep; box.querySelectorAll('[data-ep]').forEach((x) => x.setAttribute('aria-pressed', String(x === t))); }
    else if (t.dataset.t) {
      const k = t.dataset.t, v = st[k] + Number(t.dataset.d);
      if (Math.abs(v) > 30) return;
      const old = st[k]; st[k] = v;
      if (durOf() < 5 || durOf() > 180) { st[k] = old; return; }
      box.querySelector('#t' + k).textContent = fmt(st[k]);
      box.querySelector('#tlen').textContent = L.ed.len.replace('{d}', durOf() + ' s');
    }
  });
  const hk = box.querySelector('#edhook'), off = box.querySelector('#edhookoff');
  hk.addEventListener('input', () => { st.hook = hk.value; });
  off.addEventListener('change', () => { st.hookOff = off.checked; hk.disabled = off.checked; if (!off.checked) hk.focus(); });
  box.querySelector('#edno').onclick = close;
  const go = box.querySelector('#edgo');
  go.onclick = async () => {
    const ch = {};
    if (st.layout !== startLay) ch.layout = st.layout;
    const hookNow = st.hookOff ? '' : st.hook.trim();
    if (st.hookOff !== startOff || (!st.hookOff && hookNow !== startHook.trim())) ch.hook = hookNow;
    if (st.subs) ch.subs = st.subs;
    if (st.da) ch.da = st.da;
    if (st.db) ch.db = st.db;
    if (!Object.keys(ch).length) { toast(L.ed.same); return; }
    go.disabled = true;
    try {
      const r = await call('edit', { job: j.id, n: c.n, changes: ch });
      close();
      current = r.job; bal = r.balance; showSignedIn(bal); editingN = c.n;
      renderDone(current);
      clearTimeout(timer); timer = setTimeout(() => poll(j.id), 3000);
    } catch (e) { go.disabled = false; if (e.message !== 'auth') toast(e.message); }
  };
  (box.querySelector('[data-lay][aria-checked="true"]') || go).focus();
}

async function loadHist() {
  try {
    const r = await call('status', {});
    bal = r.balance; perHour = r.perHour || perHour; showSignedIn(bal);
    const list = (r.jobs || []).filter((j) => !current || j.id !== current.id);
    const el = $('hist');
    if (!list.length) { el.classList.add('hide'); return r; }
    const st = { done: L.statusDone, running: L.statusRun, queued: L.statusRun, failed: L.statusFail, cancelled: L.statusCancel };
    el.innerHTML = '<h2>' + esc(L.history) + '</h2><ul>' + list.map((j) => '<li><span class="t">' + esc(j.title || j.url) + '</span><span class="s ' + esc(j.status) + '">'
      + esc(st[j.status] || j.status) + (j.status === 'done' ? ' · ' + j.clips.length : '') + '</span>'
      + (j.status === 'done' || j.status === 'running' || j.status === 'queued' ? '<a class="btn btn-ghost btn-sm" href="?job=' + esc(j.id) + '">' + esc(L.open) + '</a>' : '') + '</li>').join('') + '</ul>';
    el.classList.remove('hide');
    return r;
  } catch (e) { return null; }
}

function fmtDur(sec) {
  const m = Math.round(sec / 60), h = Math.floor(m / 60);
  return h ? h + ' ' + L.hours + ' ' + String(m % 60).padStart(2, '0') + ' ' + L.min : m + ' ' + L.min;
}
let estFor = null;
// impostazioni come nel tool (ricordate su questo dispositivo)
const DEF_OPTS = { mode: 'auto', subs: { style: 'classico', pos: 'auto', words: 'poche' }, hook: { on: true, style: 'classico' }, prompt: '' };
let OPTS = (() => { const o = store.get('nf.opts') || {}; return { ...DEF_OPTS, ...o, mode: 'auto', subs: { ...DEF_OPTS.subs, ...(o.subs || {}) }, hook: { ...DEF_OPTS.hook, ...(o.hook || {}) }, prompt: '' }; })();
const saveOpts = () => store.set('nf.opts', { mode: OPTS.mode, subs: OPTS.subs, hook: OPTS.hook });
const SUB_LOOK = { classico: ['', '#FFD60A'], verde: ['', '#3DDC84'], riquadro: ['box', '#FFD60A'], pulito: ['low', '#FFFFFF'], impatto: ['', '#FF5A1F'] };
const HOOK_LOOK = { classico: ['', '#FFD60A'], verde: ['', '#3DDC84'], box: ['hbox', '#FF3B30'], neon: ['', '#FF4FD8'], pulito: ['low', '#3DDC84'], impatto: ['', '#FF5A1F'] };
function sample(txt, look) {
  if (look[0] === 'low') txt = txt.charAt(0) + txt.slice(1).toLowerCase();
  const w = txt.split(' '), last = w.pop();
  return '<span class="smp ' + look[0] + '">' + esc(w.join(' ')) + ' <em style="color:' + look[1] + '">' + esc(last) + '</em></span>';
}
function settingsHtml(kind) {
  const auto = kind === 'podcast' ? L.kindAutoPod : kind === 'gaming' ? L.kindAutoGame : L.kindAutoNo;
  const kindBtn = (k, name, sub) => '<button type="button" class="kind" role="radio" data-k="' + k + '" aria-checked="' + (OPTS.mode === k) + '"><span class="ph9 ' + k + '">'
    + (k === 'auto' ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.2 6.3L20.5 10l-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-1.7z"/></svg>' : '<i></i><u></u>') + '</span><b>' + esc(name) + '</b><small>' + esc(sub) + '</small></button>';
  const seg = (key, opts) => '<div class="seg" role="group">' + Object.entries(opts).map(([k, l]) => '<button type="button" data-seg="' + key + '" data-v="' + k + '" aria-pressed="' + (OPTS.subs[key] === k) + '">' + esc(l) + '</button>').join('') + '</div>';
  return '<div class="set" id="set">'
    + '<div><h4>' + esc(L.subsT) + '</h4><div class="chips" role="radiogroup" aria-label="' + esc(L.subsT) + '">'
    + Object.entries(L.subStyles).map(([k, l]) => '<button type="button" class="chip" role="radio" data-sub="' + k + '" aria-checked="' + (OPTS.subs.style === k) + '">' + sample(L.subSample, SUB_LOOK[k]) + '<small>' + esc(l) + '</small></button>').join('')
    + '</div><div class="segs" style="margin-top:12px"><div><h4>' + esc(L.posT) + '</h4>' + seg('pos', L.pos) + '</div><div><h4>' + esc(L.wordsT) + '</h4>' + seg('words', L.words) + '</div></div></div>'
    + '<div><h4>' + esc(L.hookT) + '</h4><label class="tog"><input type="checkbox" id="hookon"' + (OPTS.hook.on ? ' checked' : '') + '> ' + esc(L.hookOn) + '</label>'
    + '<div class="chips hooks' + (OPTS.hook.on ? '' : ' off') + '" role="radiogroup" aria-label="' + esc(L.hookT) + '">'
    + Object.entries(L.hookStyles).map(([k, l]) => '<button type="button" class="chip" role="radio" data-hook="' + k + '" aria-checked="' + (OPTS.hook.style === k) + '">' + sample(L.hookSample, HOOK_LOOK[k]) + '<small>' + esc(l) + '</small></button>').join('')
    + '</div></div>'
    + '<div><h4>' + esc(L.promptT) + '</h4><input class="q" id="optq" maxlength="200" placeholder="' + esc(L.promptPh) + '" value="' + esc(OPTS.prompt) + '"></div>'
    + '<p class="note">' + esc(L.autoNote) + '</p>'
    + '</div>';
}
function bindSettings(box) {
  const set = box.querySelector('#set'); if (!set) return;
  set.addEventListener('click', (ev) => {
    const t = ev.target.closest('button'); if (!t) return;
    if (t.dataset.k) { OPTS.mode = t.dataset.k; set.querySelectorAll('.kind').forEach((x) => x.setAttribute('aria-checked', String(x === t))); }
    else if (t.dataset.sub) { OPTS.subs.style = t.dataset.sub; set.querySelectorAll('[data-sub]').forEach((x) => x.setAttribute('aria-checked', String(x === t))); }
    else if (t.dataset.hook) { OPTS.hook.style = t.dataset.hook; set.querySelectorAll('[data-hook]').forEach((x) => x.setAttribute('aria-checked', String(x === t))); }
    else if (t.dataset.seg) { OPTS.subs[t.dataset.seg] = t.dataset.v; set.querySelectorAll('[data-seg="' + t.dataset.seg + '"]').forEach((x) => x.setAttribute('aria-pressed', String(x === t))); }
    else return;
    saveOpts();
  });
  const on = set.querySelector('#hookon');
  on.addEventListener('change', () => { OPTS.hook.on = on.checked; set.querySelector('.hooks').classList.toggle('off', !on.checked); saveOpts(); });
  const q = set.querySelector('#optq');
  q.addEventListener('input', () => { OPTS.prompt = q.value.slice(0, 200); });
}
async function startJob(url) {
  const b = $('estgo'); if (b) b.disabled = true;
  try {
    const r = await call('start', { url, lang: '', opts: OPTS });
    history.replaceState(null, '', '?job=' + r.job.id);
    perHour = r.perHour || perHour;
    $('est').classList.add('hide');
    poll(r.job.id);
  } catch (e) {
    if (e.message !== 'auth') setHint(e.code === 'credits' ? L.noCredits : e.message, true);
    if (e.code === 'credits') openBuy(null);
    if (b) b.disabled = false;
  }
}
async function estimate(url) {
  const box = $('est'), b = $('go');
  box.classList.add('hide'); setHint(L.checking); b.disabled = true; estFor = url;
  try {
    const r = await call('estimate', { url });
    if (estFor !== url) return;
    bal = r.balance; showSignedIn(bal);
    const stp = '<div class="stp"><ol>' + L.stepsT.map((t, i) => '<li class="' + (i === 0 ? 'ok' : i === 1 ? 'on' : '') + '"><i>' + (i === 0 ? '✓' : i + 1) + '</i>' + esc(t) + '</li>').join('') + '</ol></div>';
    box.innerHTML = stp + (r.thumbnail ? '<img src="' + esc(r.thumbnail) + '" alt="" referrerpolicy="no-referrer">' : '<span class="ph"></span>')
      + '<div><h3>' + esc(r.title || url) + '</h3><p class="meta">' + esc([r.channel, fmtDur(r.duration)].filter(Boolean).join(' · ')) + '</p>'
      + '<p class="cost"><b>' + esc(L.estT.replace('{c}', r.cost)) + '</b> · ' + esc(L.estHave.replace('{b}', r.balance)) + '</p></div>'
      + (r.enough ? settingsHtml(r.kind) : '')
      + (r.enough ? '<div class="acts"><button class="btn btn-primary" id="estgo" type="button">' + esc(L.estGo) + ' · ' + r.cost + '</button><button class="link" id="estno" type="button">' + esc(L.estChange) + '</button></div>'
        : '<p class="warn">' + esc(L.estShort) + '</p><div class="acts"><button class="btn btn-primary" id="estbuy" type="button">' + esc(L.buy.btn) + '</button><button class="link" id="estno" type="button">' + esc(L.estChange) + '</button></div>');
    box.classList.remove('hide'); setHint('');
    if (r.enough) { $('hero').classList.add('step2'); try { window.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) {} }
    bindSettings(box);
    if ($('estgo')) $('estgo').onclick = () => startJob(url);
    if ($('estbuy')) $('estbuy').onclick = () => openBuy(null);
    $('estno').onclick = () => { box.classList.add('hide'); $('hero').classList.remove('step2'); estFor = null; setHint(costNote()); $('url').select(); };
  } catch (e) {
    if (e.message !== 'auth') setHint(e.message, true);
  } finally { b.disabled = false; }
}

$('ask').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const url = $('url').value.trim();
  if (!LINKS.some((rx) => rx.test(url))) { setHint(L.badLink, true); $('url').focus(); return; }
  if (!S) { once.set('nf.pending', url); setHint(L.loginFirst); setTimeout(login, 600); return; }
  estimate(url);
});
// incollando un link valido la stima parte da sola
$('url').addEventListener('input', () => {
  const url = $('url').value.trim();
  $('est').classList.add('hide');
  if (S && url !== estFor && LINKS.some((rx) => rx.test(url))) estimate(url);
});

(async function boot() {
  fromHash();
  const job = new URLSearchParams(location.search).get('job');
  const qs = new URLSearchParams(location.search), paid = qs.get('pagamento'), want = wantFrom(qs.get('compra'));
  // senza accesso: si entra con Google e si torna qui con lo stesso ?compra= (lo ricorda login())
  if (!S) { showSignedOut(); if (job) setHint(L.loginFirst); if (want) { setHint(L.loginFirst); setTimeout(login, 700); } return; }
  if (paid || want) { qs.delete('pagamento'); qs.delete('compra'); history.replaceState(null, '', location.pathname + (qs.toString() ? '?' + qs : '')); }
  showSignedIn(null);
  if (paid === 'ok') { toast(L.buy.ok); [4000, 10000, 25000].forEach((t) => setTimeout(loadHist, t)); }
  if (paid === 'annullato') toast(L.buy.ko);
  if (want) setTimeout(() => openBuy(want), 300);
  const pending = once.get('nf.pending');
  if (pending) { once.set('nf.pending', null); $('url').value = pending; }
  if (job && /^[0-9a-f-]{36}$/i.test(job)) { poll(job); return; }
  await loadHist();
  setHint(costNote());
  if (pending) $('ask').requestSubmit();
})();
</script>
</body>
</html>
"""


def build():
    for lg, t in T.items():
        root = "" if lg == "it" else "../"
        html = PAGE
        html = html.replace("{js}", json.dumps(JS[lg], ensure_ascii=False))
        vals = dict(t, root=root, canon=("clip.html" if lg == "it" else "en/clip.html"), otherLang=("en" if lg == "it" else "it"),
                    termsLabel=("Termini" if lg == "it" else "Terms"),
                    langsHtml=('<a class="lang on" aria-current="true">IT</a><a class="lang" href="en/clip.html" lang="en">EN</a>' if lg == "it" else '<a class="lang" href="../clip.html" lang="it">IT</a><a class="lang on" aria-current="true">EN</a>'))
        for k, v in vals.items():
            html = html.replace("{" + k + "}", v)
        # CSP: solo lo script di questa pagina puo' girare (impronta sha256), niente script inseriti da fuori
        a = html.index("<script>") + len("<script>")
        b = html.index("</script>", a)
        digest = base64.b64encode(hashlib.sha256(html[a:b].encode("utf-8")).digest()).decode()
        assert html.count("<script") == 1
        assert "script-src 'self' 'unsafe-inline'" in html
        html = html.replace("script-src 'self' 'unsafe-inline'", "script-src 'sha256-" + digest + "'")
        out = os.path.join(ROOT, "docs", "clip.html" if lg == "it" else "en/clip.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("scritto", out)


if __name__ == "__main__":
    build()

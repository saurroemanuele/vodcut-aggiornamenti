"""NoonFrame - genera la landing (italiano e inglese) da un solo modello.

uso: python3 tools/landing.py            -> docs/index.html e docs/en/index.html
     python3 tools/landing.py --preview  -> docs/anteprima/index.html e docs/anteprima/en.html (non indicizzate)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# ------------------------------------------------------------------ testi: chiave -> (italiano, inglese)
S = {
    "lang": ("it", "en"),
    "title": ("NoonFrame · Lo studio per creator: clip AI, editor e grafica, gratis",
              "NoonFrame · The creator studio: AI clips, editor and design, free"),
    "desc": ("NoonFrame è lo studio gratuito per creator su Windows e Mac: l'AI trova i momenti virali delle tue live e li monta in clip verticali, editor video completo, grafica come Photoshop e video AI dalla A alla Z.",
             "NoonFrame is the free creator studio for Windows and Mac: AI finds the viral moments in your streams and edits them into vertical clips, a full video editor, Photoshop-style design and AI videos from A to Z."),
    "nav_clips": ("Clip AI", "AI clips"), "nav_editor": ("Editor", "Editor"), "nav_ai": ("Video AI", "AI video"),
    "nav_design": ("Grafica", "Design"), "nav_comm": ("Community", "Community"), "nav_faq": ("Domande", "FAQ"),
    "cta_nav": ("Scarica gratis", "Download free"),
    "hero_kicker": ("Gratis per Windows e Mac", "Free for Windows and Mac"),
    "hero_h1a": ("Dalla live", "From stream"), "hero_h1b": ("alle clip virali.", "to viral clips."),
    "hero_sub": ("NoonFrame è lo studio per creator che lavora al posto tuo: l'AI ascolta la live, trova i momenti che possono esplodere e li monta in clip verticali pronte da pubblicare. Poi editor, grafica e video AI. Tutto in un'app.",
                 "NoonFrame is the creator studio that does the work for you: AI listens to your stream, finds the moments that can blow up and edits them into vertical clips ready to post. Plus editor, design and AI video. All in one app."),
    "dl_main": ("Scarica NoonFrame", "Download NoonFrame"), "dl_all": ("Tutti i download", "All downloads"),
    "dl_phone": ("Mandami il link per il PC", "Send me the link for my computer"),
    "hero_note": ("Windows 10 e 11 · macOS 13 o successivo · Accesso con Google", "Windows 10 and 11 · macOS 13 or later · Sign in with Google"),
    "pipe_live": ("La tua live", "Your stream"), "pipe_scan": ("L'AI ascolta e guarda", "AI listens and watches"),
    "pipe_out": ("Clip pronte", "Ready clips"), "viral": ("viralità", "virality"),
    "sub1": ("e <span>adesso</span> cosa", "what <span>now</span>"), "sub2": ("l'ho <span>preso</span>", "I <span>got</span> it"),
    "sub3": ("no <span>raga</span> no", "no <span>way</span> guys"), "sub4": ("guardate <span>la chat</span>", "look at <span>chat</span>"),
    "pr_ai_big": ("A consumo", "Pay as you go"),
    "hook1": ("NON CI CREDO", "NO WAY"), "hook2": ("ULTIMO SECONDO", "LAST SECOND"), "hook3": ("È LUI?!", "IS THAT HIM?!"), "hook4": ("CHAT IMPAZZITA", "CHAT WENT WILD"),
    # sostituisce
    "rep_k": ("Un'app al posto di quattro abbonamenti", "One app instead of four subscriptions"),
    "rep_h": ("Smetti di pagare quattro tool.", "Stop paying for four tools."),
    "rep_p": ("Quello che di solito paghi ogni mese in app diverse, qui è nello stesso posto. Gli strumenti sono gratis e girano sul tuo computer.",
              "What you usually pay for every month across different apps lives in one place here. The tools are free and run on your computer."),
    "rep1a": ("Tool per clip AI", "AI clipping tool"), "rep1b": ("Clip virali con punteggio", "Viral clips with a score"),
    "rep2a": ("Editor video in abbonamento", "Subscription video editor"), "rep2b": ("Editor con timeline e montaggio automatico", "Timeline editor and auto-editing"),
    "rep3a": ("Programma di grafica a pagamento", "Paid design software"), "rep3b": ("Grafica a livelli, apre e salva PSD", "Layered design, opens and saves PSD"),
    "rep4a": ("Tool per sottotitoli e sfondi", "Subtitle and background tools"), "rep4b": ("Sottotitoli e rimozione sfondo", "Subtitles and background removal"),
    "incl": ("Incluso", "Included"),
    # clip
    "clip_k": ("Clip AI", "AI clips"),
    "clip_h": ("Ogni live diventa dieci contenuti.", "Every stream becomes ten pieces of content."),
    "clip_p": ("L'AI legge parole, urla, risate e reazioni, sceglie i momenti che funzionano da soli e li monta in verticale: webcam sopra, gioco sotto, sottotitoli grandi, zoom quando parli e un titolo che aggancia nei primi due secondi.",
               "AI reads words, screams, laughs and reactions, picks the moments that work on their own and edits them vertically: webcam on top, gameplay below, big subtitles, zooms when you talk and a hook that grabs attention in the first two seconds."),
    "cf1h": ("Punteggio di viralità", "Virality score"), "cf1p": ("Da 0 a 100 per ogni clip, con il motivo. Pubblichi prima le migliori.", "From 0 to 100 for every clip, with the reason. Post the best first."),
    "cf2h": ("Dove funziona meglio", "Where it works best"), "cf2p": ("TikTok, Reels o Shorts: per ogni clip l'AI ti dice dove ha più possibilità.", "TikTok, Reels or Shorts: for every clip the AI tells you where it has the best chance."),
    "cf3h": ("Clip a mano, quando vuoi", "Manual clips, whenever you want"), "cf3p": ("Prendi qualsiasi momento della live, o allunga una clip per dare il contesto.", "Grab any moment of the stream, or lengthen a clip to add context."),
    "cf4h": ("Sottotitoli che si leggono", "Subtitles people read"), "cf4p": ("Parola per parola, evidenziata, nel tuo stile. In sei lingue.", "Word by word, highlighted, in your style. In six languages."),
    "best_on": ("Meglio su", "Best on"),
    # editor
    "ed_k": ("Editor video", "Video editor"),
    "ed_h": ("Il montaggio noioso lo fa lui.", "The boring editing is done for you."),
    "ed_p": ("Dalla live di tre ore al video per YouTube: via pause e silenzi, zoom su di te quando parli, sottotitoli e titoli animati. Poi rifinisci tutto in una timeline vera, come in un editor professionale.",
             "From a three-hour stream to a YouTube video: pauses and silences gone, zooms on you when you talk, subtitles and animated titles. Then polish it all in a real timeline, like a pro editor."),
    "ed_live": ("La tua live", "Your stream"), "ed_done": ("Il video montato", "The edited video"),
    "ed_t1": ("Pause tagliate", "Pauses cut"), "ed_t2": ("Zoom su di te", "Zoom on you"), "ed_t3": ("Sottotitoli", "Subtitles"), "ed_t4": ("Titoli animati", "Animated titles"),
    "ed_note": ("Durate di esempio.", "Example durations."),
    # video AI
    "ai_k": ("Video AI dalla A alla Z", "AI video from A to Z"),
    "ai_h": ("Un'idea entra. Un video esce.", "An idea goes in. A video comes out."),
    "ai_p": ("Per vendere un prodotto digitale, raccontare una storia o lanciare una pagina faceless: NoonFrame scrive lo script, prepara schermate e immagini, crea la voce e monta il video. Tu scegli e approvi.",
             "To sell a digital product, tell a story or launch a faceless page: NoonFrame writes the script, prepares screens and images, creates the voice and edits the video. You choose and approve."),
    "ai1": ("Script", "Script"), "ai1p": ("Hook, struttura e testo, nel tono che vuoi.", "Hook, structure and copy, in the tone you want."),
    "ai2": ("Schermate e immagini", "Screens and images"), "ai2p": ("Generate con l'AI, nel tuo stile.", "Generated with AI, in your style."),
    "ai3": ("Voce", "Voice"), "ai3p": ("Voci naturali, anche in altre lingue.", "Natural voices, in other languages too."),
    "ai4": ("Video montato", "Edited video"), "ai4p": ("Movimento, testi e musica, pronto da esportare.", "Motion, text and music, ready to export."),
    # grafica
    "gr_k": ("Grafica", "Design"),
    "gr_h": ("Miniature come in Photoshop.", "Thumbnails like in Photoshop."),
    "gr_p": ("Livelli, maschere, selezioni e AI nello stesso posto dei tuoi video. Apri i PSD, rimuovi gli sfondi, esporti per ogni social.",
             "Layers, masks, selections and AI in the same place as your videos. Open PSDs, remove backgrounds, export for every platform."),
    "gr1": ("Livelli ed effetti", "Layers and effects"), "gr2": ("Rimuovi lo sfondo con l'AI", "AI background removal"), "gr3": ("Riempimento generativo", "Generative fill"),
    "gr4": ("Apre e salva PSD", "Opens and saves PSD"), "gr5": ("Tutte le misure dei social", "Every social format"), "gr6": ("Brand kit per ogni cliente", "Brand kit per client"),
    "gr_l": ("Livelli", "Layers"), "gr_l1": ("Io, senza sfondo", "Me, no background"), "gr_l2": ("Sfondo", "Background"), "gr_l3": ("Curve", "Curves"),
    "thumb1": ("ULTIMA", "FINAL"), "thumb2": ("PARTITA?!", "MATCH?!"),
    # community
    "cm_k": ("Costruito con chi lo usa", "Built with the people who use it"),
    "cm_h": ("Lo cambi tu. Ogni giorno.", "You shape it. Every day."),
    "cm_p": ("Scrivi un'idea o un problema dall'app: la community decide le priorità, noi la costruiamo e l'aggiornamento arriva da solo. Anche più volte al giorno.",
             "Send an idea or a problem from the app: the community sets the priorities, we build it and the update arrives on its own. Sometimes several times a day."),
    "cm1": ("Chiedi dall'app", "Ask from the app"), "cm2": ("La costruiamo", "We build it"), "cm3": ("Arriva da sola", "It arrives on its own"),
    "upd_t": ("Ultimi aggiornamenti", "Latest updates"),
    "discord": ("Entra nel Discord", "Join the Discord"),
    # prezzi
    "pr_k": ("Prezzo", "Pricing"),
    "pr_h": ("Gli strumenti sono gratis. L'AI la paghi solo se la usi.", "The tools are free. You only pay for AI if you use it."),
    "pr_free": ("Gratis, per sempre", "Free, forever"),
    "pr_free_p": ("Editor, grafica, sottotitoli, rimozione sfondo, esportazione senza filigrana. Gira sul tuo computer.", "Editor, design, subtitles, background removal, export with no watermark. Runs on your computer."),
    "pr_ai": ("Crediti AI", "AI credits"),
    "pr_ai_p": ("Per clip AI, immagini e video AI usi i crediti: ne ricevi alcuni in regalo appena entri. Oppure collega le tue chiavi AI e paghi direttamente il servizio.",
                "AI clips, images and AI video use credits: you get some free when you sign up. Or connect your own AI keys and pay the provider directly."),
    "pr_soon": ("Abbonamenti con più crediti in arrivo, con un'offerta di lancio per chi c'è dall'inizio.", "Plans with more credits are coming, with a launch offer for early users."),
    # download
    "dl_h": ("Scarica NoonFrame.", "Download NoonFrame."),
    "dl_free": ("È gratis.", "It's free."), "dl_free_p": ("Niente abbonamento. Niente filigrana. Solo un account gratuito.", "No subscription. No watermark. Just a free account."),
    "ph_t": ("Sei sul telefono? NoonFrame si usa sul computer: ti mandiamo il link via email, così lo apri da lì.", "On your phone? NoonFrame runs on computers: we'll email you the link so you can open it there."),
    "ph_email": ("La tua email", "Your email"), "ph_send": ("Mandami il link", "Send me the link"),
    "ph_mk": ("Voglio ricevere anche le novità di NoonFrame (al massimo una email al mese).", "I'd also like NoonFrame news (at most one email a month)."),
    "ph_priv": ("Usiamo la tua email per mandarti il link e, solo se spunti la casella, per le novità. Dettagli nella", "We use your email to send you the link and, only if you tick the box, for news. Details in the"),
    "privacy_w": ("privacy", "privacy policy"),
    "win_s": ("Windows 10 e 11, 64 bit · 155 MB", "Windows 10 and 11, 64-bit · 155 MB"),
    "mac_s": ("macOS 13 o successivo, Apple Silicon e Intel · 358 MB", "macOS 13 or later, Apple Silicon and Intel · 358 MB"),
    "dl_btn": ("Scarica", "Download"),
    "first_h": ("Primo avvio", "First launch"),
    "first1": ("<b>Windows:</b> apri Noonframe-Setup.exe. Se Windows avvisa, premi <b>Ulteriori informazioni</b> e poi <b>Esegui comunque</b>.",
               "<b>Windows:</b> open Noonframe-Setup.exe. If Windows warns you, click <b>More info</b> and then <b>Run anyway</b>."),
    "first2": ("<b>Mac:</b> trascina NoonFrame in Applicazioni.", "<b>Mac:</b> drag NoonFrame to Applications."),
    "first3": ("<b>Mac, solo la prima volta:</b> incolla nel Terminale", "<b>Mac, first time only:</b> paste in Terminal"),
    "copy": ("Copia", "Copy"),
    # domande
    "faq_h": ("Domande", "Questions"),
    "q1": ("NoonFrame è davvero gratis?", "Is NoonFrame really free?"),
    "a1": ("Sì. Editor video, grafica e tutte le funzioni che girano sul tuo computer sono gratis, senza abbonamento e senza filigrana. Serve solo un account gratuito: entri con Google in un clic.",
           "Yes. The video editor, design and every feature that runs on your computer are free, with no subscription and no watermark. You just need a free account: sign in with Google in one click."),
    "q2": ("Come funzionano le clip AI?", "How do AI clips work?"),
    "a2": ("Apri una live (o un video lungo), premi Trova le clip: l'AI legge la trascrizione e il volume, sceglie i momenti migliori e li monta in verticale con punteggio, titolo e piattaforma consigliata. Usa i crediti AI, oppure le tue chiavi.",
           "Open a stream (or any long video) and press Find clips: AI reads the transcript and the audio, picks the best moments and edits them vertically with a score, a title and a suggested platform. It uses AI credits, or your own keys."),
    "q3": ("I miei video vengono caricati online?", "Are my videos uploaded online?"),
    "a3": ("No. I video restano sul tuo computer. Per le funzioni AI inviamo solo quello che serve, per esempio il testo della trascrizione.",
           "No. Your videos stay on your computer. For AI features we only send what's needed, such as the transcript text."),
    "q4": ("Perché serve un account?", "Why do I need an account?"),
    "a4": ("Per mandarti gli aggiornamenti, ascoltare le tue richieste, gestire i crediti e tenere NoonFrame al sicuro dagli abusi. Vediamo quali strumenti usi, mai i tuoi video.",
           "To send you updates, hear your requests, manage credits and keep NoonFrame safe from abuse. We see which tools you use, never your videos."),
    "q5": ("Posso aprire i file di Photoshop?", "Can I open Photoshop files?"),
    "a5": ("Sì: apri i PSD con i livelli e li salvi di nuovo in PSD. Esporti anche in PNG, JPG, WebP, PDF (anche CMYK per la stampa), SVG, GIF e MP4.",
           "Yes: open PSDs with their layers and save them back as PSD. You can also export PNG, JPG, WebP, PDF (CMYK for print too), SVG, GIF and MP4."),
    "q6": ("Serve un computer potente?", "Do I need a powerful computer?"),
    "a6": ("No. Con una scheda NVIDIA sottotitoli ed esportazioni sono più veloci.", "No. With an NVIDIA card, subtitles and exports are faster."),
    "q7": ("Funziona anche senza live?", "Does it work without streams?"),
    "a7": ("Sì: qualsiasi video, in 16:9, 9:16, 1:1 o 4:5. E nella Grafica crei miniature, post e grafiche da zero.", "Yes: any video, in 16:9, 9:16, 1:1 or 4:5. And in Design you create thumbnails, posts and graphics from scratch."),
    "q8": ("In che lingue?", "Which languages?"),
    "a8": ("L'app è in italiano e inglese. Sottotitoli e clip in italiano, inglese, spagnolo, francese, tedesco e portoghese.",
           "The app is in Italian and English. Subtitles and clips in Italian, English, Spanish, French, German and Portuguese."),
    "foot": ("© 2026 NoonFrame · Ogni frame nella sua luce migliore.", "© 2026 NoonFrame · Every frame in its best light."),
    "terms": ("Termini d'uso", "Terms of use"), "terms_href": ("termini.html", "terms.html"),
    "sections": ("Sezioni", "Sections"), "langs_l": ("Lingua", "Language"),
    # script
    "js": ("""{
  lang: 'it', dlMac: 'Scarica per Mac', dlWin: 'Scarica per Windows', otherWin: 'Hai Windows?', otherMac: 'Hai un Mac?',
  noteMac: 'macOS 13 o successivo · 358 MB · Accesso con Google', noteWin: 'Windows 10 e 11 · 155 MB · Accesso con Google',
  mobile: 'NoonFrame funziona su computer Windows e Mac: ti mandiamo il link via email.',
  sending: 'Invio…', sent: 'Fatto! Controlla la posta (anche lo spam) e apri l\\'email dal computer.', queued: 'Ricevuto! Ti mandiamo il link a breve: aprilo dal computer.',
  badEmail: 'Controlla l\\'email: sembra scritta male.', rate: 'Troppe richieste: riprova tra un po\\'.', fail: 'Non è partita. Riprova tra poco.',
  months: ['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic'], count: ' aggiornamenti dal lancio',
  types: { feat: 'Novità', impr: 'Miglioramenti', fix: 'Correzioni' }, copied: 'Copiato', pressCopy: 'Premi Ctrl+C', copy: 'Copia',
}""", """{
  lang: 'en', dlMac: 'Download for Mac', dlWin: 'Download for Windows', otherWin: 'On Windows?', otherMac: 'On a Mac?',
  noteMac: 'macOS 13 or later · 358 MB · Sign in with Google', noteWin: 'Windows 10 and 11 · 155 MB · Sign in with Google',
  mobile: 'NoonFrame runs on Windows and Mac computers: we\\'ll email you the link.',
  sending: 'Sending…', sent: 'Done! Check your inbox (and spam) and open the email on your computer.', queued: 'Got it! We\\'ll send you the link shortly: open it on your computer.',
  badEmail: 'Check your email: it looks mistyped.', rate: 'Too many requests: try again later.', fail: 'It didn\\'t go through. Try again shortly.',
  months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], count: ' updates since launch',
  types: { feat: 'New', impr: 'Improvements', fix: 'Fixes' }, copied: 'Copied', pressCopy: 'Press Ctrl+C', copy: 'Copy',
}"""),
}

# ------------------------------------------------------------------ testi della versione 2 (stile software, meno testo)
S.update({
    "title": ("NoonFrame · Lo studio AI per creator", "NoonFrame · The AI studio for creators"),
    "pill_new": ("Novità", "New"), "pill_t": ("Clip AI con la piattaforma migliore per ogni clip", "AI clips with the best platform for each clip"),
    "h1a": ("Lo studio AI", "The AI studio"), "h1b": ("per creator.", "for creators."),
    "sub2": ("Clip virali dalle tue live, editor video, grafica e video AI. In un'app gratuita per Windows e Mac.",
             "Viral clips from your streams, video editor, design and AI video. In one free app for Windows and Mac."),
    "st1": ("per gli strumenti", "for the tools"), "st2": ("piattaforme valutate per ogni clip", "platforms scored for every clip"),
    "st3": ("lingue per sottotitoli e clip", "languages for subtitles and clips"), "st4": ("aggiornamenti dal lancio", "updates since launch"),
    "bn_h": ("Tutto quello che serve a un creator.", "Everything a creator needs."),
    "bn_p": ("Un'app sola al posto di quattro abbonamenti.", "One app instead of four subscriptions."),
    "b1h": ("Clip AI", "AI clips"), "b1p": ("L'AI trova i momenti virali della live e li monta in verticale, con punteggio e piattaforma migliore.",
                                         "AI finds the viral moments in your stream and edits them vertically, with a score and the best platform."),
    "b2h": ("Punteggio di viralità", "Virality score"), "b2p": ("Pubblichi prima le clip che hanno più possibilità.", "Post the clips with the best chance first."),
    "b3h": ("Allunga o accorcia", "Lengthen or shorten"), "b3p": ("Prendi il contesto prima o il finale dopo, direttamente dalla live.", "Grab context before or the ending after, straight from the stream."),
    "b4h": ("Grafica come Photoshop", "Photoshop-style design"), "b4p": ("Miniature con livelli, rimozione sfondo con l'AI, PSD.", "Thumbnails with layers, AI background removal, PSD."),
    "b5h": ("Sottotitoli che si leggono", "Subtitles people read"), "b5p": ("Parola per parola, nel tuo stile, in sei lingue.", "Word by word, in your style, in six languages."),
    "b6h": ("Video AI dalla A alla Z", "AI video from A to Z"), "b6p": ("Script, immagini, voce e montaggio per vendere un prodotto digitale o lanciare una pagina faceless.",
                                                                       "Script, images, voice and editing to sell a digital product or launch a faceless page."),
    "ai_s1": ("Script", "Script"), "ai_s2": ("Immagini", "Images"), "ai_s3": ("Voce", "Voice"), "ai_s4": ("Video", "Video"),
    "ext_was": ("clip dell'AI", "AI clip"), "ext_add": ("+ 18 s di contesto", "+ 18 s of context"),
    "ed2_k": ("Editor", "Editor"), "ed2_h": ("Dalla live al video. Da solo.", "From stream to video. On its own."),
    "ed2_p": ("Pause tagliate, zoom su di te, sottotitoli e titoli animati in automatico. Poi rifinisci in una timeline vera.",
              "Pauses cut, zooms on you, subtitles and animated titles, automatically. Then polish it in a real timeline."),
    "ed2_1": ("Montaggio automatico delle live", "Automatic stream editing"), "ed2_2": ("Timeline con tracce, testi ed effetti", "Timeline with tracks, text and effects"),
    "ed2_3": ("Esporti per YouTube, TikTok, Reels e Shorts", "Export for YouTube, TikTok, Reels and Shorts"),
    "cm2_h": ("Migliora ogni giorno, con chi lo usa.", "Better every day, with the people who use it."),
    "cm2_p": ("Chiedi una funzione dall'app: la community decide, noi la costruiamo, l'aggiornamento arriva da solo.",
              "Request a feature from the app: the community decides, we build it, the update arrives on its own."),
    "pr2_h": ("Gratis. L'AI solo se la usi.", "Free. AI only if you use it."),
    "faq2_h": ("Domande", "FAQ"),
    "shot_alt1": ("La galleria delle clip AI di NoonFrame con punteggio e piattaforma", "NoonFrame's AI clip gallery with score and platform"),
    "shot_alt2": ("Dettaglio di una clip: dove funziona meglio", "Clip detail: where it works best"),
    "shot_alt3": ("L'editor di NoonFrame con anteprima e timeline", "NoonFrame's editor with preview and timeline"),
    "shot_alt4": ("La grafica di NoonFrame con una miniatura", "NoonFrame design with a thumbnail"),
})

# ------------------------------------------------------------------ testi della versione 3 (capitoli, niente box)
S.update({
    "c1_h": ("Dalla live alle clip, in pochi minuti.", "From stream to clips, in minutes."),
    "c1_p": ("L'AI ascolta parole, urla e reazioni, sceglie i momenti che funzionano da soli e li monta in verticale, pronti da pubblicare.",
             "AI listens to words, screams and reactions, picks the moments that work on their own and edits them vertically, ready to post."),
    "f1t": ("Punteggio di viralità", "Virality score"), "f1p": ("Da 0 a 100 per ogni clip, con il motivo.", "From 0 to 100 for every clip, with the reason."),
    "f2t": ("Dove funziona meglio", "Where it works best"), "f2p": ("TikTok, Reels o Shorts: l'AI te lo dice per ogni clip.", "TikTok, Reels or Shorts: the AI tells you for every clip."),
    "f3t": ("Allunga o accorcia", "Lengthen or shorten"), "f3p": ("Il contesto che serve, preso direttamente dalla live.", "The context you need, taken straight from the stream."),
    "f4t": ("Sottotitoli che si leggono", "Subtitles people read"), "f4p": ("Parola per parola, nel tuo stile, in sei lingue.", "Word by word, in your style, in six languages."),
    "g_list": ("Livelli e maschere · Rimozione sfondo con l'AI · Riempimento generativo · Apre e salva PSD", "Layers and masks · AI background removal · Generative fill · Opens and saves PSD"),
})

S.update({
    "reel_h": ("Da una sola live, clip così.", "From one stream, clips like these."),
    "reel_p": ("Ognuna con punteggio di viralità e piattaforma consigliata.", "Each with a virality score and a suggested platform."),
    "end_p": ("Gratis per Windows e Mac. Entri con Google e parti.", "Free for Windows and Mac. Sign in with Google and go."),
})

# ------------------------------------------------------------------ SEO
# landing v4 (una pagina scura, cinque parti)
S.update({
    "nav_what": ("Cosa fa", "What it does"),
    "t_h": ("Tutto quello che ti serve. In un'app.", "Everything you need. In one app."),
    "t_p": ("Dalla live alla clip pubblicata, senza saltare tra quattro programmi diversi.", "From stream to published clip, without jumping between four different apps."),
    "pr_free_n": ("Gratis", "Free"),
    "pr_free_c": ("Per sempre", "Forever"),
    "dl_free_p2": ("Gratis, senza filigrana. Entri con Google e parti.", "Free, no watermark. Sign in with Google and go."),
    "dl_win_b": ("Scarica per Windows", "Download for Windows"),
    "dl_mac_b": ("Scarica per Mac", "Download for Mac"),
})

# piani (stessi prezzi di credits_plans / credits_packs su Supabase: se cambiano li', cambiarli anche qui)
S.update({
    "pr_soon": ("I piani si attivano dall'app a breve, con un'offerta di lancio per chi c'è dall'inizio.", "Plans will be available in the app soon, with a launch offer for early users."),
    "pl_mo": ("/mese", "/month"),
    "pl1_p": ("11,99 €", "€11.99"), "pl1_c": ("1.000 crediti al mese", "1,000 credits a month"), "pl1_t": ("Per iniziare con l'AI.", "To get started with AI."),
    "pl1_y": ("Oppure 119,90 € all'anno: 2 mesi gratis.", "Or €119.90 a year: 2 months free."),
    "pl2_p": ("29,99 €", "€29.99"), "pl2_c": ("2.800 crediti al mese", "2,800 credits a month"), "pl2_t": ("Per chi pubblica ogni giorno. Fino a 12 generazioni insieme.", "For daily creators. Up to 12 generations at once."),
    "pl2_y": ("Oppure 299,90 € all'anno: 2 mesi gratis.", "Or €299.90 a year: 2 months free."),
    "pl3_p": ("69,99 €", "€69.99"), "pl3_c": ("6.500 crediti al mese", "6,500 credits a month"), "pl3_t": ("Tutti i modelli video premium. Fino a 30 generazioni insieme.", "All premium video models. Up to 30 generations at once."),
    "pl3_y": ("Oppure 699,90 € all'anno: 2 mesi gratis.", "Or €699.90 a year: 2 months free."),
    "pl_top_k": ("Ricariche una tantum:", "One-time top-ups:"),
    "pl_top": ("500 crediti a 5,99 €, 1.500 crediti a 14,99 €. Non scadono.", "500 credits for €5.99, 1,500 credits for €14.99. They don't expire."),
    "pl_note": ("Prezzi in euro, IVA inclusa. L'abbonamento si rinnova da solo e lo disdici quando vuoi, dall'app.",
                "Prices in euros, VAT included. Your plan renews automatically and you can cancel anytime from the app."),
    "pl_terms": ("Pagamenti, disdetta e rimborsi", "Payments, cancellation and refunds"),
})

S.update({
    "title": ("Clip AI gratis dalle tue live per TikTok e Shorts | NoonFrame",
              "Free AI clips from your streams for TikTok & Shorts | NoonFrame"),
    "desc": ("Trasforma le live di Twitch, Kick e YouTube in clip virali con l'AI: punteggio, sottotitoli e zoom automatici. Editor e grafica inclusi. Gratis per PC e Mac.",
             "Turn Twitch, Kick and YouTube streams into viral clips with AI: virality score, auto subtitles and zooms. Editor and design included. Free for PC and Mac."),
    "sub2": ("Clip virali dalle tue live di Twitch, Kick e YouTube, editor video, grafica e video AI. In un'app gratuita per Windows e Mac.",
             "Viral clips from your Twitch, Kick and YouTube streams, video editor, design and AI video. In one free app for Windows and Mac."),
    "og_locale": ("it_IT", "en_US"), "og_alt": ("en_US", "it_IT"),
    "canon": ("https://noonframe.com/", "https://noonframe.com/en/"),
    "og_img_alt": ("NoonFrame, lo studio AI per creator", "NoonFrame, the AI studio for creators"),
})

DISCORD = "https://discord.gg/5cQvNEBfee"

TPL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "landing.tpl.html"), encoding="utf-8").read()


def build(lang, prefix, other_href, self_is_it, out, preview, legal):
    i = 0 if lang == "it" else 1
    html = TPL
    for k, v in S.items():
        html = html.replace("{{" + k + "}}", v[i])
    html = (html.replace("{{P}}", prefix).replace("{{OTHER}}", other_href).replace("{{DISCORD}}", DISCORD).replace("{{LEGAL}}", legal)
            .replace("{{ROBOTS}}", '<meta name="robots" content="noindex">' if preview else "")
            .replace("{{REDIRECT}}", "false" if preview else "true"))
    import json as _json
    ld = [
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "NoonFrame",
         "operatingSystem": "Windows 10, Windows 11, macOS 13+", "applicationCategory": "MultimediaApplication",
         "applicationSubCategory": "Video editor",
         "description": S["desc"][i], "url": S["canon"][i], "image": "https://noonframe.com/shots/og.png",
         "inLanguage": ["it", "en"], "downloadUrl": S["canon"][i] + "#download",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
         "publisher": {"@type": "Organization", "name": "NoonFrame", "url": "https://noonframe.com/", "logo": "https://noonframe.com/logo.png"}},
        {"@context": "https://schema.org", "@type": "Organization", "name": "NoonFrame", "url": "https://noonframe.com/",
         "logo": "https://noonframe.com/logo.png", "email": "business@noonframe.com", "sameAs": [DISCORD]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": S[q][i], "acceptedAnswer": {"@type": "Answer", "text": S[a][i]}}
            for q, a in (("q1", "a1"), ("q2", "a2"), ("q3", "a3"), ("q4", "a4"), ("q6", "a6"))]},
    ]
    html = html.replace("{{JSONLD}}", "".join('<script type="application/ld+json">' + _json.dumps(x, ensure_ascii=False).replace("</", "<\\/") + "</script>\n" for x in ld))
    if self_is_it:
        langs = ('<span class="lang on" aria-current="true" lang="it">IT</span>'
                 f'<a class="lang" href="{other_href}" data-lang="en" lang="en">EN</a>')
    else:
        langs = (f'<a class="lang" href="{other_href}" data-lang="it" lang="it">IT</a>'
                 '<span class="lang on" aria-current="true" lang="en">EN</span>')
    html = html.replace("{{LANGS}}", langs)
    assert "{{" not in html, html[html.index("{{"):html.index("{{") + 40]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("scritto", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    if "--preview" in sys.argv:
        d = os.path.join(DOCS, "anteprima")
        build("it", "../", "en.html", True, os.path.join(d, "index.html"), True, "../")
        build("en", "../", "index.html", False, os.path.join(d, "en.html"), True, "../en/")
    else:
        build("it", "", "en/index.html", True, os.path.join(DOCS, "index.html"), False, "")
        build("en", "../", "../index.html", False, os.path.join(DOCS, "en", "index.html"), False, "")

// NoonFrame · pagina "Collega": qui arriva chi aggiunge NoonFrame a un agente AI (Claude, ChatGPT, Codex, Cursor…).
// Supabase Auth (server OAuth 2.1) apre questa pagina con ?authorization_id=…: accesso con Google, controllo
// dell'abbonamento (solo Starter, Pro, Ultimate), poi "Collega" o "Annulla". Senza authorization_id la pagina
// mostra gli agenti gia' collegati, con "Scollega".
(function () {
  'use strict';
  // niente riquadri di altri siti sopra il pulsante "Collega"
  if (window.top !== window.self) { try { window.top.location = window.location.href; } catch (e) {} return; }
  document.documentElement.classList.remove('nf-hide');

  var SB = 'https://jhoidpugjjvvkjccyrxg.supabase.co';
  var KEY = 'sb_publishable_vam6nGEE5qCrRCXknhoWqQ_GvrpnvzR';
  var MCP = SB + '/functions/v1/mcp';
  var HOME = 'https://noonframe.com/collega.html';   // l'indirizzo esatto autorizzato per il ritorno da Google
  var qs = new URLSearchParams(location.search);
  var EN = qs.get('lang') ? qs.get('lang') === 'en' : !/^it\b/i.test(navigator.language || 'it');
  document.documentElement.lang = EN ? 'en' : 'it';

  var T = EN ? {
    title: 'NoonFrame · Connect your AI agent', wait: 'One moment…',
    signH: 'Connect your AI agent to NoonFrame', signP: 'Sign in with the same Google account you use in the app.', signBtn: 'Sign in with Google',
    inApp: 'Open this page in your browser (Safari or Chrome) to sign in with Google.',
    askH: '{app} wants to connect to your NoonFrame', back: 'After connecting you go back to {host}.',
    can: 'It can', cant: 'It can’t',
    canL: ['See your plan and credits', 'Make clips from your video links, always telling you the cost first', 'See and change your web clips'],
    cantL: ['See the files on your computer', 'Buy anything or change your plan', 'Change your account'],
    go: 'Connect', no: 'Cancel', fine: 'You can disconnect it anytime from this page.', out: 'Sign out', retry: 'Try again',
    payH: 'AI agents are for subscribers', payP: 'With Starter your agent makes clips from your videos, follows them and edits them for you.',
    payOffer: 'Try Starter for {p} the first month', payPlan: 'Subscribe to Starter · {p}/month', payThen: 'Then {p}/month. Cancel anytime.',
    recheck: 'I subscribed, check again', notYet: 'No active plan yet. If you just paid, wait a few seconds and try again.',
    doneH: 'Connected', doneP: 'Taking you back to {app}…', deniedH: 'Not connected', deniedP: 'Taking you back to {app}…',
    badH: 'This link has expired', badP: 'Start connecting again from your AI agent. The link only lasts a few minutes.',
    mineH: 'Connected AI agents', mineP: 'Agents that can use your NoonFrame. Disconnect the ones you don’t use.', mineNone: 'No agent connected.',
    since: 'connected on {d}', off: 'Disconnect', offOk: 'Disconnected.', how: 'How to connect an agent',
    mineSign: 'Sign in to see the agents connected to your NoonFrame.',
    oops: 'Something didn’t work. Try again in a moment.',
  } : {
    title: 'NoonFrame · Collega il tuo agente AI', wait: 'Un attimo…',
    signH: 'Collega il tuo agente AI a NoonFrame', signP: 'Accedi con lo stesso account Google che usi nell’app.', signBtn: 'Accedi con Google',
    inApp: 'Apri questa pagina nel browser (Safari o Chrome) per accedere con Google.',
    askH: '{app} vuole collegarsi al tuo NoonFrame', back: 'Dopo il collegamento torni su {host}.',
    can: 'Potrà', cant: 'Non potrà',
    canL: ['Vedere il tuo piano e i crediti', 'Creare clip dai link dei tuoi video, dicendoti sempre prima quanto costano', 'Vedere e modificare le tue clip dal web'],
    cantL: ['Vedere i file del tuo computer', 'Comprare o cambiare il tuo abbonamento', 'Cambiare il tuo account'],
    go: 'Collega', no: 'Annulla', fine: 'Puoi scollegarlo quando vuoi da questa pagina.', out: 'Esci', retry: 'Riprova',
    payH: 'Gli agenti AI sono per gli abbonati', payP: 'Con Starter il tuo agente crea le clip dai tuoi video, le segue e le modifica per te.',
    payOffer: 'Prova Starter a {p} il primo mese', payPlan: 'Abbonati a Starter · {p} al mese', payThen: 'Poi {p} al mese. Disdici quando vuoi.',
    recheck: 'Mi sono abbonato, ricontrolla', notYet: 'Non vedo ancora un piano attivo. Se hai appena pagato, aspetta qualche secondo e riprova.',
    doneH: 'Collegato', doneP: 'Ti riporto su {app}…', deniedH: 'Non collegato', deniedP: 'Ti riporto su {app}…',
    badH: 'Questo link è scaduto', badP: 'Ricomincia il collegamento dal tuo agente AI. Il link vale solo pochi minuti.',
    mineH: 'Agenti AI collegati', mineP: 'Gli agenti che possono usare il tuo NoonFrame. Scollega quelli che non usi.', mineNone: 'Nessun agente collegato.',
    since: 'collegato il {d}', off: 'Scollega', offOk: 'Scollegato.', how: 'Come collegare un agente',
    mineSign: 'Accedi per vedere gli agenti collegati al tuo NoonFrame.',
    oops: 'Qualcosa non ha funzionato. Riprova tra poco.',
  };
  document.title = T.title;
  var GUIDE = EN ? 'en/agents.html' : 'agenti.html';

  var card = document.getElementById('card');
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var fill = function (s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k] == null ? '' : o[k]; }); };
  var eur = function (n) { n = Number(n); return EN ? '€' + n.toFixed(2) : n.toFixed(2).replace('.', ',') + ' €'; };
  var TOP = '<div class="top"><img src="logo.png" alt=""><span>NoonFrame</span></div>';
  function show(html) { card.innerHTML = TOP + html; }
  function waiting() { show('<h1><span class="dot"></span>' + esc(T.wait) + '</h1>'); }

  // ---- sessione: la stessa della pagina clip (nf.sess), cosi' chi ha gia' fatto l'accesso non lo rifa'
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } },
    set: function (k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  var S = store.get('nf.sess');
  (function fromHash() {
    if (!location.hash || location.hash.length < 10) return;
    var p = new URLSearchParams(location.hash.slice(1)), asked = 0, back = '';
    try { asked = Number(localStorage.getItem('nf.login') || 0); back = localStorage.getItem('nf.back') || ''; localStorage.removeItem('nf.login'); localStorage.removeItem('nf.back'); } catch (e) {}
    // accetta un accesso solo se l'ha chiesto questa scheda da poco (un link preparato da altri non ti fa entrare nel suo account)
    if (p.get('access_token') && asked && Date.now() - asked < 15 * 60000) {
      S = { at: p.get('access_token'), rt: p.get('refresh_token'), exp: Date.now() / 1000 + Number(p.get('expires_in') || 3600) };
      store.set('nf.sess', S);
    }
    var keep = location.search || (/^\?[\w=&%.-]{0,300}$/.test(back) ? back : '');
    history.replaceState(null, '', location.pathname + keep);
    qs = new URLSearchParams(keep);
  })();
  function token() {
    if (!S) return Promise.resolve(null);
    if (S.exp - 90 > Date.now() / 1000) return Promise.resolve(S.at);
    return fetch(SB + '/auth/v1/token?grant_type=refresh_token', { method: 'POST', headers: { apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh_token: S.rt }) })
      .then(function (r) { if (!r.ok) throw new Error('refresh'); return r.json(); })
      .then(function (j) { S = { at: j.access_token, rt: j.refresh_token, exp: Date.now() / 1000 + Number(j.expires_in || 3600) }; store.set('nf.sess', S); return S.at; })
      .catch(function () { S = null; store.set('nf.sess', null); return null; });
  }
  function me() {
    try { var p = JSON.parse(atob(S.at.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))); return p.email || ''; } catch (e) { return ''; }
  }
  var IN_APP = /Instagram|FBAN|FBAV|FB_IAB|TikTok|musical_ly|Bytedance|Snapchat|LinkedInApp|\bLine\//i.test(navigator.userAgent || '');
  function login() {
    try { localStorage.setItem('nf.login', String(Date.now())); localStorage.setItem('nf.back', location.search || ''); } catch (e) {}
    location.href = SB + '/auth/v1/authorize?provider=google&redirect_to=' + encodeURIComponent(HOME);
  }
  function logout() { S = null; store.set('nf.sess', null); start(); }

  // ---- chiamate con l'accesso dell'utente
  function api(method, path, body) {
    return token().then(function (at) {
      if (!at) { var e = new Error('auth'); e.auth = true; throw e; }
      return fetch(SB + path, { method: method, headers: { apikey: KEY, Authorization: 'Bearer ' + at, 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
    }).then(function (r) {
      if (r.status === 401) { S = null; store.set('nf.sess', null); var e = new Error('auth'); e.auth = true; throw e; }
      if (r.status === 204) return {};
      return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { var e = new Error(j.msg || j.message || j.error_description || 'http'); e.status = r.status; throw e; } return j; });
    });
  }
  // piano e proposta di Starter: li decide la funzione mcp, la stessa che usano gli agenti
  function account() {
    return token().then(function (at) {
      return fetch(MCP, { method: 'POST', headers: { Authorization: 'Bearer ' + at, 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'get_account', arguments: {} } }) });
    }).then(function (r) { return r.json(); }).then(function (j) {
      var c = j && j.result;
      if (!c || c.isError) throw new Error('account');
      return JSON.parse(c.content[0].text);
    });
  }
  // il ritorno all'agente: solo indirizzi veri, mai javascript: o data:
  function goBack(url) {
    if (typeof url !== 'string' || !/^[a-z][a-z0-9+.-]*:/i.test(url) || /^(javascript|data|vbscript|file):/i.test(url)) { bad(); return; }
    setTimeout(function () { location.href = url; }, 600);
  }
  function hostOf(u) { try { var x = new URL(u); return x.protocol === 'https:' || x.protocol === 'http:' ? x.hostname : x.protocol.replace(':', ''); } catch (e) { return ''; } }

  // ---- schermate
  function signIn(h, p) {
    show('<h1>' + esc(h) + '</h1><p>' + esc(p) + '</p><div class="btns"><button type="button" id="in">' + esc(T.signBtn) + '</button></div>'
      + (IN_APP ? '<p class="fine err">' + esc(T.inApp) + '</p>' : '') + '<p class="fine"><a href="' + GUIDE + '">' + esc(T.how) + '</a></p>');
    document.getElementById('in').onclick = login;
  }
  function bad() { show('<h1>' + esc(T.badH) + '</h1><p>' + esc(T.badP) + '</p><p class="fine"><a href="' + GUIDE + '">' + esc(T.how) + '</a></p>'); }
  function oops(e) {
    if (e && e.auth) { start(); return; }
    show('<p class="err">' + esc(T.oops) + '</p><div class="btns"><button type="button" class="sec" id="re">' + esc(T.retry) + '</button></div>');
    document.getElementById('re').onclick = start;
  }
  function whoRow() { return '<div class="who"><b>' + esc(me()) + '</b><button type="button" class="sec small" id="out">' + esc(T.out) + '</button></div>'; }
  function bindOut() { var o = document.getElementById('out'); if (o) o.onclick = logout; }

  function paywall(acc, id, d) {
    var offer = Number(acc.upgradePrice) < Number(acc.upgradeFull);
    show('<h1>' + esc(T.payH) + '</h1><p>' + esc(T.payP) + '</p>' + whoRow()
      + '<div class="btns"><a class="btn" id="buy" target="_blank" rel="noopener" href="' + esc(acc.upgradeLink) + '">'
      + esc(fill(offer ? T.payOffer : T.payPlan, { p: eur(acc.upgradePrice) })) + '</a>'
      + '<button type="button" class="sec" id="re">' + esc(T.recheck) + '</button></div>'
      + (offer ? '<p class="fine">' + esc(fill(T.payThen, { p: eur(acc.upgradeFull) })) + '</p>' : '') + '<p class="fine err" id="msg" role="status"></p>');
    bindOut();
    document.getElementById('re').onclick = function () {
      var b = this; b.disabled = true;
      account().then(function (a) {
        if (a.subscribed) { consent(id, d); return; }
        b.disabled = false; document.getElementById('msg').textContent = T.notYet;
      }).catch(oops);
    };
  }
  function consent(id, d) {
    var app = (d.client && d.client.name) || (EN ? 'An AI agent' : 'Un agente AI'), host = hostOf(d.redirect_uri);
    show('<h1>' + esc(fill(T.askH, { app: app })) + '</h1>' + whoRow()
      + '<div class="lbl">' + esc(T.can) + '</div><ul class="list">' + T.canL.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'
      + '<div class="lbl">' + esc(T.cant) + '</div><ul class="list no">' + T.cantL.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'
      + '<div class="btns"><button type="button" id="go">' + esc(T.go) + '</button><button type="button" class="sec" id="no">' + esc(T.no) + '</button></div>'
      + '<p class="fine">' + (host ? esc(fill(T.back, { host: host })) + ' ' : '') + esc(T.fine) + '</p>');
    bindOut();
    var decide = function (action) {
      document.getElementById('go').disabled = true; document.getElementById('no').disabled = true;
      api('POST', '/auth/v1/oauth/authorizations/' + encodeURIComponent(id) + '/consent', { action: action }).then(function (r) {
        show('<h1>' + esc(action === 'approve' ? T.doneH : T.deniedH) + '</h1><p>' + esc(fill(action === 'approve' ? T.doneP : T.deniedP, { app: app })) + '</p>');
        goBack(r.redirect_url);
      }).catch(function (e) { if (e.auth) start(); else bad(); });
    };
    document.getElementById('go').onclick = function () { decide('approve'); };
    document.getElementById('no').onclick = function () { decide('deny'); };
  }

  // senza richiesta di un agente: gli agenti gia' collegati
  function mine() {
    if (!S) { signIn(T.mineH, T.mineSign); return; }
    waiting();
    api('GET', '/auth/v1/user/oauth/grants').then(function (list) {
      list = Array.isArray(list) ? list : [];
      show('<h1>' + esc(T.mineH) + '</h1><p>' + esc(T.mineP) + '</p>' + whoRow()
        + (list.length ? list.map(function (g, i) {
          var d = g.granted_at ? new Date(g.granted_at).toLocaleDateString(EN ? 'en-GB' : 'it-IT', { day: 'numeric', month: 'long', year: 'numeric' }) : '';
          return '<div class="agent"><div><b>' + esc((g.client && g.client.name) || '—') + '</b>' + (d ? '<small>' + esc(fill(T.since, { d: d })) + '</small>' : '') + '</div>'
            + '<button type="button" class="sec small" data-i="' + i + '">' + esc(T.off) + '</button></div>';
        }).join('') : '<p class="fine">' + esc(T.mineNone) + '</p>')
        + '<p class="fine"><a href="' + GUIDE + '">' + esc(T.how) + '</a></p>');
      bindOut();
      card.querySelectorAll('button[data-i]').forEach(function (b) {
        b.onclick = function () {
          var g = list[Number(b.dataset.i)]; b.disabled = true;
          api('DELETE', '/auth/v1/user/oauth/grants?client_id=' + encodeURIComponent(g.client.id)).then(function () {
            b.outerHTML = '<span class="fine ok">' + esc(T.offOk) + '</span>';
          }).catch(function (e) { if (e.auth) start(); else { b.disabled = false; } });
        };
      });
    }).catch(oops);
  }

  function start() {
    var id = qs.get('authorization_id');
    if (!id) { mine(); return; }
    if (!/^[\w.-]{8,200}$/.test(id)) { bad(); return; }
    if (!S) { signIn(T.signH, T.signP); return; }
    waiting();
    api('GET', '/auth/v1/oauth/authorizations/' + encodeURIComponent(id)).then(function (d) {
      // gia' approvato in passato: si torna subito all'agente
      if (d && d.redirect_url && !d.authorization_id) { show('<h1>' + esc(T.doneH) + '</h1>'); goBack(d.redirect_url); return; }
      if (!d || !d.authorization_id) { bad(); return; }
      return account().then(function (acc) { if (acc.subscribed) consent(id, d); else paywall(acc, id, d); });
    }).catch(function (e) { if (e.auth) start(); else if (e.status && e.status < 500) bad(); else oops(e); });
  }
  start();
})();

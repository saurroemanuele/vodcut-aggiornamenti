(function () {
  var SB = 'https://jhoidpugjjvvkjccyrxg.supabase.co';
  var KEY = 'sb_publishable_vam6nGEE5qCrRCXknhoWqQ_GvrpnvzR';
  var en = !/^it/i.test(navigator.language || '');
  var NAMES = { tiktok: 'TikTok', instagram: 'Instagram', youtube: 'YouTube' };
  var T = en ? {
    ok: 'Account connected', okm: function (n, u) { return 'Your ' + n + ' account' + (u ? ' (' + u + ')' : '') + ' is connected to NoonFrame. You can close this page and go back to the app.'; },
    no: 'Connection cancelled', nom: 'You did not grant access. Nothing was connected; you can try again from NoonFrame.',
    er: 'Something went wrong', erm: 'We could not connect the account. Go back to NoonFrame and try again.'
  } : {
    ok: 'Account collegato', okm: function (n, u) { return 'Il tuo account ' + n + (u ? ' (' + u + ')' : '') + ' è collegato a NoonFrame. Puoi chiudere questa pagina e tornare all’app.'; },
    no: 'Collegamento annullato', nom: 'Non hai concesso l’accesso. Non è stato collegato niente: puoi riprovare da NoonFrame.',
    er: 'Qualcosa non ha funzionato', erm: 'Non siamo riusciti a collegare l’account. Torna su NoonFrame e riprova.'
  };
  if (en) document.documentElement.lang = 'en';
  function show(kind, title, msg) {
    document.getElementById('card').className = 'card ' + kind;
    document.getElementById('t').innerHTML = '<span class="dot"></span> ';
    document.getElementById('t').appendChild(document.createTextNode(title));
    document.getElementById('m').textContent = msg;
  }
  var q = new URLSearchParams(location.search);
  var code = q.get('code'), state = q.get('state');
  history.replaceState(null, '', location.pathname);
  if (q.get('error') || q.get('error_code') || !code) {
    var denied = /denied|cancel|access_denied/i.test((q.get('error') || '') + (q.get('error_reason') || '') + (q.get('error_description') || ''));
    return denied || !code ? show('err', T.no, T.nom) : show('err', T.er, T.erm);
  }
  fetch(SB + '/functions/v1/social', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', apikey: KEY, Authorization: 'Bearer ' + KEY },
    body: JSON.stringify({ op: 'callback', code: code, state: state, scopes: q.get('scopes') || q.get('scope') || '' })
  }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
    .then(function (x) {
      if (!x.ok || !x.j || !x.j.ok) throw new Error((x.j && x.j.error) || 'fail');
      show('ok', T.ok, T.okm(NAMES[x.j.provider] || x.j.provider, x.j.username || ''));
      if (x.j.back) setTimeout(function () { location.href = x.j.back; }, 1500);
    })
    .catch(function () { show('err', T.er, T.erm); });
})();

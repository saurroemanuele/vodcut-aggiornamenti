// NoonFrame · pagina "Agenti AI": il pulsante che copia l'indirizzo del server MCP
(function () {
  var b = document.getElementById('cp'), c = document.getElementById('mcp');
  if (!b || !c) return;
  var label = b.textContent;
  b.onclick = function () {
    var done = function () { b.textContent = b.dataset.ok; setTimeout(function () { b.textContent = label; }, 1800); };
    try {
      navigator.clipboard.writeText(c.textContent.trim()).then(done, function () { pick(); });
    } catch (e) { pick(); }
  };
  // senza appunti (browser vecchi): si seleziona il testo, cosi' basta copiarlo a mano
  function pick() { var r = document.createRange(); r.selectNodeContents(c); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
})();

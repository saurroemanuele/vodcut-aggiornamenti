// NoonFrame · pagamento sicuro. Il modulo della carta e' Stripe (Elements con Checkout Sessions): i dati della carta
// vanno direttamente a Stripe, mai a NoonFrame. I crediti li aggiunge solo il server, quando Stripe conferma il pagamento.
// Si apre nel foglio di pagamento dell'app (embed=1, solo carta), in una finestra a parte per PayPal (method=paypal)
// o da sola. I dati arrivano dopo il # (non vanno a nessun server): cs, pk, lang, theme, kind, name, det, price, period,
// email, po (indirizzo dell'app che apre il foglio), test, mock (prove senza Stripe, con le carte di prova).
(function () {
  'use strict';
  var T = {
    it: { payment: 'Pagamento', total_today: 'Totale oggi', have_code: 'Hai un codice sconto?', code_ph: 'Codice sconto', apply: 'Applica', code_bad: 'Questo codice non esiste o è scaduto',
      by_stripe: 'Pagamento gestito da Stripe', no_card_data: 'I dati della carta non passano dai server di NoonFrame.', or_card: 'oppure paga con la carta',
      terms: 'Accetto i Termini di vendita. Chiedo di avere subito i crediti e so che, una volta usati, perdo il diritto di recesso di 14 giorni.', terms_link: 'Termini di vendita',
      pay_x: 'Paga {p}', renews_auto: 'Si rinnova da solo · disdici quando vuoi', one_time: 'Pagamento una tantum', sub_monthly: 'Abbonamento mensile', sub_yearly: 'Abbonamento annuale', topup: 'Ricarica',
      renews: 'Poi {p} ogni mese dal {date}. Disdici quando vuoi da Account: resta attivo fino a fine periodo.', renews_y: 'Poi {p} ogni anno dal {date}. Disdici quando vuoi da Account: resta attivo fino a fine periodo.',
      vat_incl: 'Prezzi IVA inclusa', vat_of: 'di cui IVA {r}%', discount: 'Codice {code}', processing: 'Pagamento in corso…', to_paypal: 'Ti porto su PayPal…', adding: 'Sto aggiungendo i crediti…', dont_close: 'Non chiudere NoonFrame',
      bank_title: 'Conferma il pagamento', bank_sub: 'Verifica della tua banca · 3D Secure', bank_text: 'Ti abbiamo mandato una notifica nell\'app della banca. Approva il pagamento di {p} a NoonFrame.', other_method: 'Annulla e scegli un altro metodo',
      welcome: 'Benvenuto in {plan}!', welcome_text: 'L\'abbonamento è attivo. L\'assistente AI e le Clip veloci senza logo sono già sbloccati.', added: 'Crediti aggiunti', added_text: 'Puoi usarli subito per l\'AI e le Clip veloci. Non scadono.',
      got: '+{g} crediti · ora ne hai {n}', back_edit: 'Torna a montare',
      paypal_wait: 'Completa il pagamento nella finestra di PayPal', paypal_wait_t: 'Appena PayPal conferma, i crediti arrivano da soli.',
      err_declined: 'La carta è stata rifiutata', err_declined_t: 'La banca non ha autorizzato il pagamento. Prova un\'altra carta o un altro metodo: non ti abbiamo addebitato niente.',
      err_funds: 'Fondi insufficienti', err_funds_t: 'Sulla carta non c\'è abbastanza credito. Prova un\'altra carta o un altro metodo.',
      err_3ds_no: 'La banca ha rifiutato il pagamento', err_3ds_no_t: 'Non ti abbiamo addebitato niente. Prova un altro metodo o contatta la banca.',
      err_3ds_time: 'La banca non ha confermato in tempo', err_3ds_time_t: 'Il pagamento è stato annullato e non ti è stato addebitato niente. Riprova o usa un altro metodo.',
      err_check: 'Controlla i dati della carta', err_check_t: 'Numero, scadenza e codice di sicurezza devono essere completi.', err_terms: 'Accetta i Termini di vendita', err_terms_t: 'Spunta la casella qui sopra prima di pagare.',
      err_load: 'Il pagamento non si è aperto', err_load_t: 'Chiudi e riprova tra un attimo: non ti abbiamo addebitato niente.', err_expired: 'Il pagamento è scaduto', err_expired_t: 'Chiudi e riprova: non ti abbiamo addebitato niente.',
      copy_details: 'Copia i dettagli per il supporto', copied: 'Copiato', test: 'Prova', card_number: 'Numero della carta', expiry: 'Scadenza', cvc: 'Codice di sicurezza', name_on_card: 'Nome sulla carta', zip: 'CAP',
      test_cards: 'Carte di prova: 4242 va a buon fine, 3184 chiede la banca, 0002 rifiutata, 9995 fondi insufficienti. Codice NOON20.' },
    en: { payment: 'Payment', total_today: 'Total today', have_code: 'Have a discount code?', code_ph: 'Discount code', apply: 'Apply', code_bad: 'This code doesn\'t exist or has expired',
      by_stripe: 'Payment handled by Stripe', no_card_data: 'Card details never touch NoonFrame\'s servers.', or_card: 'or pay by card',
      terms: 'I accept the Terms of sale. I want the credits right away and understand that once used I lose the 14-day right of withdrawal.', terms_link: 'Terms of sale',
      pay_x: 'Pay {p}', renews_auto: 'Renews automatically · cancel anytime', one_time: 'One-time payment', sub_monthly: 'Monthly subscription', sub_yearly: 'Yearly subscription', topup: 'Top-up',
      renews: 'Then {p} every month from {date}. Cancel anytime in Account: it stays active until the end of the period.', renews_y: 'Then {p} every year from {date}. Cancel anytime in Account: it stays active until the end of the period.',
      vat_incl: 'Prices include VAT', vat_of: 'incl. {r}% VAT', discount: 'Code {code}', processing: 'Processing payment…', to_paypal: 'Taking you to PayPal…', adding: 'Adding your credits…', dont_close: 'Don\'t close NoonFrame',
      bank_title: 'Confirm the payment', bank_sub: 'Your bank\'s check · 3D Secure', bank_text: 'We sent a notification to your bank app. Approve the {p} payment to NoonFrame.', other_method: 'Cancel and choose another method',
      welcome: 'Welcome to {plan}!', welcome_text: 'Your subscription is active. The AI assistant and logo-free Quick clips are unlocked.', added: 'Credits added', added_text: 'Use them right away for AI and Quick clips. They never expire.',
      got: '+{g} credits · you now have {n}', back_edit: 'Back to editing',
      paypal_wait: 'Finish paying in the PayPal window', paypal_wait_t: 'As soon as PayPal confirms, your credits arrive on their own.',
      err_declined: 'Your card was declined', err_declined_t: 'Your bank didn\'t authorise the payment. Try another card or method: you haven\'t been charged.',
      err_funds: 'Insufficient funds', err_funds_t: 'There isn\'t enough credit on the card. Try another card or method.',
      err_3ds_no: 'Your bank rejected the payment', err_3ds_no_t: 'You haven\'t been charged. Try another method or contact your bank.',
      err_3ds_time: 'Your bank didn\'t confirm in time', err_3ds_time_t: 'The payment was cancelled and you haven\'t been charged. Try again or use another method.',
      err_check: 'Check your card details', err_check_t: 'Number, expiry and security code must be complete.', err_terms: 'Accept the Terms of sale', err_terms_t: 'Tick the box above before paying.',
      err_load: 'The payment didn\'t open', err_load_t: 'Close and try again in a moment: you haven\'t been charged.', err_expired: 'The payment has expired', err_expired_t: 'Close and try again: you haven\'t been charged.',
      copy_details: 'Copy details for support', copied: 'Copied', test: 'Test', card_number: 'Card number', expiry: 'Expiry', cvc: 'Security code', name_on_card: 'Name on card', zip: 'Postal code',
      test_cards: 'Test cards: 4242 succeeds, 3184 asks your bank, 0002 declined, 9995 insufficient funds. Code NOON20.' },
    fr: { payment: 'Paiement', total_today: 'Total aujourd\'hui', have_code: 'Tu as un code promo ?', code_ph: 'Code promo', apply: 'Appliquer', code_bad: 'Ce code n\'existe pas ou a expiré',
      by_stripe: 'Paiement géré par Stripe', no_card_data: 'Les données de carte ne passent pas par les serveurs de NoonFrame.', or_card: 'ou paie par carte',
      terms: 'J\'accepte les Conditions de vente. Je demande les crédits tout de suite et je sais qu\'une fois utilisés, je perds le droit de rétractation de 14 jours.', terms_link: 'Conditions de vente',
      pay_x: 'Payer {p}', renews_auto: 'Renouvellement automatique · résilie quand tu veux', one_time: 'Paiement unique', sub_monthly: 'Abonnement mensuel', sub_yearly: 'Abonnement annuel', topup: 'Recharge',
      renews: 'Puis {p} chaque mois à partir du {date}. Résilie quand tu veux dans Compte : il reste actif jusqu\'à la fin de la période.', renews_y: 'Puis {p} chaque année à partir du {date}. Résilie quand tu veux dans Compte : il reste actif jusqu\'à la fin de la période.',
      vat_incl: 'Prix TTC', vat_of: 'dont TVA {r} %', discount: 'Code {code}', processing: 'Paiement en cours…', to_paypal: 'Je t\'emmène sur PayPal…', adding: 'J\'ajoute tes crédits…', dont_close: 'Ne ferme pas NoonFrame',
      bank_title: 'Confirme le paiement', bank_sub: 'Vérification de ta banque · 3D Secure', bank_text: 'Nous avons envoyé une notification dans l\'app de ta banque. Approuve le paiement de {p} à NoonFrame.', other_method: 'Annuler et choisir un autre moyen',
      welcome: 'Bienvenue dans {plan} !', welcome_text: 'L\'abonnement est actif. L\'assistant IA et les Clips rapides sans logo sont débloqués.', added: 'Crédits ajoutés', added_text: 'Utilise-les tout de suite pour l\'IA et les Clips rapides. Ils n\'expirent pas.',
      got: '+{g} crédits · tu en as maintenant {n}', back_edit: 'Retour au montage',
      paypal_wait: 'Termine le paiement dans la fenêtre PayPal', paypal_wait_t: 'Dès que PayPal confirme, les crédits arrivent tout seuls.',
      err_declined: 'Ta carte a été refusée', err_declined_t: 'Ta banque n\'a pas autorisé le paiement. Essaie une autre carte ou un autre moyen : rien n\'a été débité.',
      err_funds: 'Fonds insuffisants', err_funds_t: 'Le solde de la carte est insuffisant. Essaie une autre carte ou un autre moyen.',
      err_3ds_no: 'Ta banque a refusé le paiement', err_3ds_no_t: 'Rien n\'a été débité. Essaie un autre moyen ou contacte ta banque.',
      err_3ds_time: 'Ta banque n\'a pas confirmé à temps', err_3ds_time_t: 'Le paiement a été annulé et rien n\'a été débité. Réessaie ou utilise un autre moyen.',
      err_check: 'Vérifie les données de la carte', err_check_t: 'Numéro, date d\'expiration et code de sécurité doivent être complets.', err_terms: 'Accepte les Conditions de vente', err_terms_t: 'Coche la case ci-dessus avant de payer.',
      err_load: 'Le paiement ne s\'est pas ouvert', err_load_t: 'Ferme et réessaie dans un instant : rien n\'a été débité.', err_expired: 'Le paiement a expiré', err_expired_t: 'Ferme et réessaie : rien n\'a été débité.',
      copy_details: 'Copier les détails pour le support', copied: 'Copié', test: 'Test', card_number: 'Numéro de carte', expiry: 'Expiration', cvc: 'Code de sécurité', name_on_card: 'Nom sur la carte', zip: 'Code postal',
      test_cards: 'Cartes de test : 4242 réussit, 3184 demande la banque, 0002 refusée, 9995 fonds insuffisants. Code NOON20.' },
    de: { payment: 'Zahlung', total_today: 'Heute fällig', have_code: 'Hast du einen Rabattcode?', code_ph: 'Rabattcode', apply: 'Anwenden', code_bad: 'Dieser Code existiert nicht oder ist abgelaufen',
      by_stripe: 'Zahlung über Stripe', no_card_data: 'Kartendaten laufen nie über die Server von NoonFrame.', or_card: 'oder mit Karte zahlen',
      terms: 'Ich akzeptiere die Verkaufsbedingungen. Ich möchte die Credits sofort und weiß, dass ich nach der Nutzung mein 14-tägiges Widerrufsrecht verliere.', terms_link: 'Verkaufsbedingungen',
      pay_x: '{p} bezahlen', renews_auto: 'Verlängert sich automatisch · jederzeit kündbar', one_time: 'Einmalzahlung', sub_monthly: 'Monatsabo', sub_yearly: 'Jahresabo', topup: 'Aufladung',
      renews: 'Danach {p} monatlich ab {date}. Jederzeit unter Konto kündbar: bleibt bis zum Ende des Zeitraums aktiv.', renews_y: 'Danach {p} jährlich ab {date}. Jederzeit unter Konto kündbar: bleibt bis zum Ende des Zeitraums aktiv.',
      vat_incl: 'Preise inkl. MwSt.', vat_of: 'inkl. {r} % MwSt.', discount: 'Code {code}', processing: 'Zahlung läuft…', to_paypal: 'Weiter zu PayPal…', adding: 'Credits werden hinzugefügt…', dont_close: 'NoonFrame nicht schließen',
      bank_title: 'Zahlung bestätigen', bank_sub: 'Prüfung deiner Bank · 3D Secure', bank_text: 'Wir haben eine Mitteilung an deine Banking-App geschickt. Bestätige die Zahlung von {p} an NoonFrame.', other_method: 'Abbrechen und andere Methode wählen',
      welcome: 'Willkommen bei {plan}!', welcome_text: 'Dein Abo ist aktiv. KI-Assistent und Schnelle Clips ohne Logo sind freigeschaltet.', added: 'Credits hinzugefügt', added_text: 'Sofort nutzbar für KI und Schnelle Clips. Sie verfallen nicht.',
      got: '+{g} Credits · du hast jetzt {n}', back_edit: 'Zurück zum Schneiden',
      paypal_wait: 'Schließ die Zahlung im PayPal-Fenster ab', paypal_wait_t: 'Sobald PayPal bestätigt, kommen die Credits von selbst.',
      err_declined: 'Deine Karte wurde abgelehnt', err_declined_t: 'Deine Bank hat die Zahlung nicht freigegeben. Versuch eine andere Karte oder Methode: Dir wurde nichts berechnet.',
      err_funds: 'Unzureichende Deckung', err_funds_t: 'Auf der Karte ist nicht genug Guthaben. Versuch eine andere Karte oder Methode.',
      err_3ds_no: 'Deine Bank hat die Zahlung abgelehnt', err_3ds_no_t: 'Dir wurde nichts berechnet. Versuch eine andere Methode oder kontaktiere deine Bank.',
      err_3ds_time: 'Deine Bank hat nicht rechtzeitig bestätigt', err_3ds_time_t: 'Die Zahlung wurde abgebrochen, dir wurde nichts berechnet. Versuch es erneut oder nutze eine andere Methode.',
      err_check: 'Prüf deine Kartendaten', err_check_t: 'Nummer, Ablaufdatum und Prüfnummer müssen vollständig sein.', err_terms: 'Akzeptiere die Verkaufsbedingungen', err_terms_t: 'Hak das Kästchen oben an, bevor du zahlst.',
      err_load: 'Die Zahlung hat sich nicht geöffnet', err_load_t: 'Schließ und versuch es gleich noch einmal: Dir wurde nichts berechnet.', err_expired: 'Die Zahlung ist abgelaufen', err_expired_t: 'Schließ und versuch es erneut: Dir wurde nichts berechnet.',
      copy_details: 'Details für den Support kopieren', copied: 'Kopiert', test: 'Test', card_number: 'Kartennummer', expiry: 'Ablaufdatum', cvc: 'Prüfnummer', name_on_card: 'Name auf der Karte', zip: 'PLZ',
      test_cards: 'Testkarten: 4242 klappt, 3184 fragt die Bank, 0002 abgelehnt, 9995 keine Deckung. Code NOON20.' },
    pt: { payment: 'Pagamento', total_today: 'Total hoje', have_code: 'Tem um código de desconto?', code_ph: 'Código de desconto', apply: 'Aplicar', code_bad: 'Este código não existe ou expirou',
      by_stripe: 'Pagamento processado pela Stripe', no_card_data: 'Os dados do cartão não passam pelos servidores da NoonFrame.', or_card: 'ou pague com cartão',
      terms: 'Aceito os Termos de venda. Peço os créditos agora e sei que, depois de usados, perco o direito de arrependimento de 14 dias.', terms_link: 'Termos de venda',
      pay_x: 'Pagar {p}', renews_auto: 'Renova automaticamente · cancele quando quiser', one_time: 'Pagamento único', sub_monthly: 'Assinatura mensal', sub_yearly: 'Assinatura anual', topup: 'Recarga',
      renews: 'Depois {p} por mês a partir de {date}. Cancele quando quiser em Conta: fica ativa até o fim do período.', renews_y: 'Depois {p} por ano a partir de {date}. Cancele quando quiser em Conta: fica ativa até o fim do período.',
      vat_incl: 'Preços com impostos incluídos', vat_of: 'inclui {r}% de impostos', discount: 'Código {code}', processing: 'Processando o pagamento…', to_paypal: 'Levando você para o PayPal…', adding: 'Adicionando os créditos…', dont_close: 'Não feche o NoonFrame',
      bank_title: 'Confirme o pagamento', bank_sub: 'Verificação do seu banco · 3D Secure', bank_text: 'Enviamos uma notificação para o app do seu banco. Aprove o pagamento de {p} para a NoonFrame.', other_method: 'Cancelar e escolher outro método',
      welcome: 'Boas-vindas ao {plan}!', welcome_text: 'A assinatura está ativa. O assistente de IA e os Clips rápidos sem logo já estão liberados.', added: 'Créditos adicionados', added_text: 'Você já pode usá-los na IA e nos Clips rápidos. Eles não expiram.',
      got: '+{g} créditos · agora você tem {n}', back_edit: 'Voltar a editar',
      paypal_wait: 'Conclua o pagamento na janela do PayPal', paypal_wait_t: 'Assim que o PayPal confirmar, os créditos chegam sozinhos.',
      err_declined: 'O cartão foi recusado', err_declined_t: 'O banco não autorizou o pagamento. Tente outro cartão ou método: nada foi cobrado.',
      err_funds: 'Saldo insuficiente', err_funds_t: 'O cartão não tem saldo suficiente. Tente outro cartão ou método.',
      err_3ds_no: 'O banco recusou o pagamento', err_3ds_no_t: 'Nada foi cobrado. Tente outro método ou fale com o seu banco.',
      err_3ds_time: 'O banco não confirmou a tempo', err_3ds_time_t: 'O pagamento foi cancelado e nada foi cobrado. Tente de novo ou use outro método.',
      err_check: 'Confira os dados do cartão', err_check_t: 'Número, validade e código de segurança precisam estar completos.', err_terms: 'Aceite os Termos de venda', err_terms_t: 'Marque a caixa acima antes de pagar.',
      err_load: 'O pagamento não abriu', err_load_t: 'Feche e tente de novo daqui a pouco: nada foi cobrado.', err_expired: 'O pagamento expirou', err_expired_t: 'Feche e tente de novo: nada foi cobrado.',
      copy_details: 'Copiar os detalhes para o suporte', copied: 'Copiado', test: 'Teste', card_number: 'Número do cartão', expiry: 'Validade', cvc: 'Código de segurança', name_on_card: 'Nome no cartão', zip: 'CEP',
      test_cards: 'Cartões de teste: 4242 aprovado, 3184 pede o banco, 0002 recusado, 9995 saldo insuficiente. Código NOON20.' },
    es: { payment: 'Pago', total_today: 'Total hoy', have_code: '¿Tienes un código de descuento?', code_ph: 'Código de descuento', apply: 'Aplicar', code_bad: 'Este código no existe o ha caducado',
      by_stripe: 'Pago gestionado por Stripe', no_card_data: 'Los datos de la tarjeta no pasan por los servidores de NoonFrame.', or_card: 'o paga con tarjeta',
      terms: 'Acepto los Términos de venta. Pido los créditos ya y sé que, una vez usados, pierdo el derecho de desistimiento de 14 días.', terms_link: 'Términos de venta',
      pay_x: 'Pagar {p}', renews_auto: 'Se renueva solo · cancela cuando quieras', one_time: 'Pago único', sub_monthly: 'Suscripción mensual', sub_yearly: 'Suscripción anual', topup: 'Recarga',
      renews: 'Después {p} cada mes desde el {date}. Cancela cuando quieras en Cuenta: sigue activo hasta el final del periodo.', renews_y: 'Después {p} cada año desde el {date}. Cancela cuando quieras en Cuenta: sigue activo hasta el final del periodo.',
      vat_incl: 'Precios con IVA incluido', vat_of: 'IVA {r} % incluido', discount: 'Código {code}', processing: 'Procesando el pago…', to_paypal: 'Te llevo a PayPal…', adding: 'Añadiendo los créditos…', dont_close: 'No cierres NoonFrame',
      bank_title: 'Confirma el pago', bank_sub: 'Verificación de tu banco · 3D Secure', bank_text: 'Te hemos enviado una notificación a la app del banco. Aprueba el pago de {p} a NoonFrame.', other_method: 'Cancelar y elegir otro método',
      welcome: '¡Bienvenido a {plan}!', welcome_text: 'La suscripción está activa. El asistente de IA y los Clips rápidos sin logo ya están desbloqueados.', added: 'Créditos añadidos', added_text: 'Puedes usarlos ya para la IA y los Clips rápidos. No caducan.',
      got: '+{g} créditos · ahora tienes {n}', back_edit: 'Volver a editar',
      paypal_wait: 'Termina el pago en la ventana de PayPal', paypal_wait_t: 'En cuanto PayPal confirme, los créditos llegan solos.',
      err_declined: 'Tu tarjeta ha sido rechazada', err_declined_t: 'Tu banco no ha autorizado el pago. Prueba otra tarjeta u otro método: no te hemos cobrado nada.',
      err_funds: 'Fondos insuficientes', err_funds_t: 'La tarjeta no tiene saldo suficiente. Prueba otra tarjeta u otro método.',
      err_3ds_no: 'Tu banco ha rechazado el pago', err_3ds_no_t: 'No te hemos cobrado nada. Prueba otro método o contacta con tu banco.',
      err_3ds_time: 'Tu banco no ha confirmado a tiempo', err_3ds_time_t: 'El pago se ha cancelado y no te hemos cobrado nada. Vuelve a intentarlo o usa otro método.',
      err_check: 'Revisa los datos de la tarjeta', err_check_t: 'Número, caducidad y código de seguridad deben estar completos.', err_terms: 'Acepta los Términos de venta', err_terms_t: 'Marca la casilla de arriba antes de pagar.',
      err_load: 'El pago no se ha abierto', err_load_t: 'Cierra y vuelve a intentarlo en un momento: no te hemos cobrado nada.', err_expired: 'El pago ha caducado', err_expired_t: 'Cierra y vuelve a intentarlo: no te hemos cobrado nada.',
      copy_details: 'Copiar los detalles para soporte', copied: 'Copiado', test: 'Prueba', card_number: 'Número de tarjeta', expiry: 'Caducidad', cvc: 'Código de seguridad', name_on_card: 'Nombre en la tarjeta', zip: 'Código postal',
      test_cards: 'Tarjetas de prueba: 4242 funciona, 3184 pide el banco, 0002 rechazada, 9995 fondos insuficientes. Código NOON20.' },
  };
  var TERMS_URL = { it: 'termini.html', en: 'en/terms.html' };

  // ---------------------------------------------------------------- parametri (dopo il #; dopo il ritorno da PayPal: ?esito=ok)
  var P = {};
  (location.hash || '').slice(1).split('&').forEach(function (kv) {
    var i = kv.indexOf('=');
    if (i > 0) { try { P[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1)); } catch (e) { /* parametro rotto: si ignora */ } }
  });
  var Q = new URLSearchParams(location.search);
  var back = Q.get('esito') === 'ok';
  if (back) { try { var keep = JSON.parse(sessionStorage.getItem('nf-pay') || '{}'); Object.keys(keep).forEach(function (k) { if (!(k in P)) P[k] = keep[k]; }); } catch (e) { /* */ } }
  var LANG = T[P.lang] ? P.lang : ((navigator.language || 'it').slice(0, 2) in T ? (navigator.language || 'it').slice(0, 2) : 'it');
  var L = T[LANG];
  var t = function (k, v) { var s = L[k] || T.it[k] || k; if (v) Object.keys(v).forEach(function (x) { s = s.split('{' + x + '}').join(v[x]); }); return s; };
  var LOCALE = { it: 'it-IT', en: 'en-GB', fr: 'fr-FR', de: 'de-DE', pt: 'pt-BR', es: 'es-ES' }[LANG];
  var embed = P.embed === '1' && /^http:\/\/(127\.0\.0\.1|localhost):\d{2,5}$/.test(P.po || '');
  var paypalWin = P.method === 'paypal';
  var mock = P.mock === '1';
  var isPlan = P.kind === 'plan' || P.kind === 'plan_offer';
  var yearly = P.period === 'year';
  document.documentElement.lang = LANG;
  document.documentElement.dataset.theme = P.theme === 'light' ? 'light' : 'dark';
  if (!embed) document.body.classList.add('top');

  var $ = function (id) { return document.getElementById(id); };
  var el = function (tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; };
  // verso l'app che ha aperto il foglio (solo lei, e solo dall'indirizzo locale dell'app)
  var tell = function (ev, data) {
    if (!embed) return;
    var m = { nf: 'pay', ev: ev };
    if (data) Object.keys(data).forEach(function (k) { m[k] = data[k]; });
    try { parent.postMessage(m, P.po); } catch (e) { /* */ }
  };

  // ---------------------------------------------------------------- testi della pagina
  document.querySelectorAll('[data-t]').forEach(function (e) { e.textContent = t(e.dataset.t); });
  document.querySelectorAll('[data-tp]').forEach(function (e) { e.placeholder = t(e.dataset.tp); });
  $('x').setAttribute('aria-label', LANG === 'it' ? 'Chiudi' : 'Close');
  (function terms() {
    var s = t('terms'), link = t('terms_link'), i = s.indexOf(link), box = $('termst');
    var a = el('a', null, link);
    a.href = 'https://noonframe.com/' + (TERMS_URL[LANG] || TERMS_URL.en);
    a.target = '_blank'; a.rel = 'noopener';
    if (i < 0) { box.textContent = s + ' '; box.appendChild(a); return; }
    box.appendChild(document.createTextNode(s.slice(0, i))); box.appendChild(a); box.appendChild(document.createTextNode(s.slice(i + link.length)));
  })();

  // ---------------------------------------------------------------- riepilogo (prima dai dati dell'app, poi da Stripe)
  $('kind').textContent = isPlan ? t(yearly ? 'sub_yearly' : 'sub_monthly') : t('topup');
  $('name').textContent = P.name || 'NoonFrame';
  $('det').textContent = P.det || '';
  $('test').hidden = !(P.test === '1' || mock);
  $('payn').textContent = isPlan ? t('renews_auto') : t('one_time');
  var nextDate = function () { var d = new Date(); if (yearly) d.setFullYear(d.getFullYear() + 1); else d.setMonth(d.getMonth() + 1); return d.toLocaleDateString(LOCALE, { day: 'numeric', month: 'long' }); };
  function summary(s) {
    // s: { item, items:[{name, amount}], discount:[{label, amount}], tax:[{label}], total, next }
    var rows = $('rows');
    rows.textContent = '';
    (s.items || []).forEach(function (it) { var r = el('div', 'pg-row'); r.appendChild(el('span', null, it.name)); r.appendChild(el('b', null, it.amount)); rows.appendChild(r); });
    (s.discount || []).forEach(function (d) { var r = el('div', 'pg-row ok'); r.appendChild(el('span', null, d.label)); r.appendChild(el('b', null, '−' + d.amount)); rows.appendChild(r); });
    (s.tax && s.tax.length ? s.tax : [{ label: t('vat_incl') }]).forEach(function (x) { var r = el('div', 'pg-row'); r.appendChild(el('span', null, x.label)); if (x.amount) r.appendChild(el('b', null, x.amount)); rows.appendChild(r); });
    $('total').textContent = s.total || '';
    $('payt').textContent = t('pay_x', { p: s.total || '' });
    var rn = $('renew');
    rn.hidden = !isPlan;
    if (isPlan) rn.textContent = t(yearly ? 'renews_y' : 'renews', { p: s.next || s.total || '', date: nextDate() });
  }
  summary({ items: [{ name: P.name || '', amount: P.price || '' }], total: P.price || '' });

  // ---------------------------------------------------------------- stati: in corso, banca, fatto, errore
  var busy = false;
  function setBusy(on) { busy = on; $('x').disabled = on; $('pay').disabled = on; tell('busy', { on: on }); }
  var state = $('state');
  function showState(nodes) { state.textContent = ''; nodes.forEach(function (n) { if (n) state.appendChild(n); }); state.hidden = false; }
  function hideState() { state.hidden = true; state.textContent = ''; }
  function spinning(title, sub) { showState([el('div', 'pg-spin'), el('p', 'big', title), sub ? el('p', 'muted', sub) : null]); }
  var errInfo = '';
  function fail(key, info) {
    hideState(); setBusy(false);
    $('errt').textContent = t('err_' + key); $('errx').textContent = t('err_' + key + '_t');
    errInfo = info || ''; $('copy').hidden = !errInfo; $('copy').textContent = t('copy_details');
    $('err').hidden = false;
    $('err').scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }
  function clearErr() { $('err').hidden = true; }
  $('copy').addEventListener('click', function () {
    var b = $('copy');
    (navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(errInfo) : Promise.reject()).then(function () { b.textContent = t('copied'); }, function () { b.textContent = errInfo; });
  });
  var gotLine = null;
  function done() {
    setBusy(false);
    var c = el('div', 'pg-check');
    c.innerHTML = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
    gotLine = el('p', 'big', t('adding'));
    var btn = el('button', 'btn', t('back_edit'));
    btn.addEventListener('click', function () { if (embed) tell('close'); else try { window.close(); } catch (e) { /* */ } });
    showState([c, el('h3', null, isPlan ? t('welcome', { plan: P.plan || P.name || 'NoonFrame' }) : t('added')), el('p', null, isPlan ? t('welcome_text') : t('added_text')), gotLine,
      embed || !back ? btn : null]);
    tell('done', { kind: P.kind || '' });
    try { sessionStorage.removeItem('nf-pay'); } catch (e) { /* */ }
  }
  // l'app dice quanti crediti sono arrivati (dal server, dopo la conferma di Stripe)
  window.addEventListener('message', function (e) {
    if (!embed || e.origin !== P.po || !e.data || e.data.nf !== 'pay') return;
    if (e.data.ev === 'paid' && !gotLine) done();   // pagato nella finestra di PayPal
    if (e.data.ev === 'credited' && !gotLine) done();
    if (e.data.ev === 'credited' && gotLine) {
      var fmt = function (n) { return Number(n || 0).toLocaleString(LOCALE); };
      gotLine.textContent = e.data.got > 0 ? t('got', { g: fmt(e.data.got), n: fmt(e.data.balance) }) : '';
    }
  });
  $('x').addEventListener('click', function () { if (busy) return; if (embed) tell('close'); else try { window.close(); } catch (e) { /* */ } });

  // ---------------------------------------------------------------- codice sconto
  $('codeq').addEventListener('click', function () { $('code').hidden = false; $('codeq').hidden = true; $('codein').focus(); });
  var applyCode = null;   // (codice) => Promise<boolean>
  $('codego').addEventListener('click', function () {
    var v = $('codein').value.trim();
    if (!v || !applyCode) return;
    $('codego').disabled = true; $('codeerr').hidden = true;
    applyCode(v).then(function (ok) { $('codego').disabled = false; $('codeerr').hidden = ok; if (ok) $('codein').value = ''; });
  });
  $('codein').addEventListener('keydown', function (e) { if (e.key === 'Enter') $('codego').click(); });

  // ---------------------------------------------------------------- PayPal: nel foglio dell'app si apre la sua finestra
  if (embed && !paypalWin) {
    $('paypal').hidden = false;
    $('paypal').addEventListener('click', function () {
      clearErr();
      if (!$('terms').checked) return fail('terms');
      tell('paypal');
      var cancel = el('button', 'linkish', t('other_method'));
      cancel.addEventListener('click', function () { hideState(); tell('paypal_cancel'); });
      showState([el('div', 'pg-spin'), el('p', 'big', t('paypal_wait')), el('p', 'muted', t('paypal_wait_t')), cancel]);
    });
  }
  $('or').hidden = $('paypal').hidden;   // "oppure paga con la carta" solo se sopra c'e' un altro modo di pagare

  // ritorno da PayPal (o da un'altra pagina della banca): il pagamento e' fatto, i crediti arrivano dal server
  if (back) { done(); return; }
  if (!P.cs && !mock) { fail('load'); $('pay').disabled = true; return; }

  // ---------------------------------------------------------------- prove senza Stripe (mock=1): le carte di prova del mockup
  if (mock && paypalWin) { spinning(t('to_paypal'), t('dont_close')); return setTimeout(done, 1800); }   // prova: PayPal finto
  if (mock) return mockPay();

  // ---------------------------------------------------------------- Stripe
  var s = document.createElement('script');
  s.src = 'https://js.stripe.com/endive/stripe.js';
  s.onload = function () { start().catch(function (e) { fail('load', String(e && e.message || e)); }); };
  s.onerror = function () { fail('load', 'stripe.js'); };
  document.head.appendChild(s);

  function appearance() {
    var cs = getComputedStyle(document.documentElement), v = function (n) { return cs.getPropertyValue(n).trim(); };
    var light = document.documentElement.dataset.theme === 'light';
    return {
      theme: light ? 'stripe' : 'night',
      variables: { colorPrimary: v('--ac'), colorBackground: light ? '#FFFFFF' : '#17191F', colorText: v('--tx'), colorDanger: v('--err'), fontFamily: 'Manrope, system-ui, sans-serif', borderRadius: '11px', spacingUnit: '4px' },
      rules: { '.Input': { border: '1.5px solid ' + v('--gline'), padding: '12px' }, '.Label': { fontSize: '12px', fontWeight: '600', color: v('--t2') } },
    };
  }
  async function start() {
    /* global Stripe */
    var stripe = Stripe(P.pk, { locale: LOCALE });
    var fontUrl = new URL('fonts/manrope.ttf', location.href).href;
    var checkout = stripe.initCheckoutElementsSdk({ clientSecret: P.cs, elementsOptions: { appearance: appearance(), fonts: [{ family: 'Manrope', src: 'url(' + fontUrl + ')', weight: '200 800' }] } });
    var lr = await checkout.loadActions();
    if (lr.type !== 'success') return fail('load', (lr.error && lr.error.message) || 'loadActions');
    var actions = lr.actions;
    var paint = function (ss) {
      if (!ss) return;
      if (ss.status && ss.status.type === 'expired') return fail('expired');
      if (ss.status && ss.status.type === 'complete') return done();
      var items = (ss.lineItems || []).map(function (li) { return { name: li.name, amount: (li.subtotal || li.total || {}).amount }; });
      var disc = (ss.discountAmounts || []).map(function (d) { return { label: d.promotionCode ? t('discount', { code: d.promotionCode }) : d.displayName, amount: d.amount }; });
      var tax = (ss.taxAmounts || []).filter(function (x) { return x.inclusive; }).map(function (x) { return { label: x.percentage ? t('vat_of', { r: x.percentage }) : x.displayName, amount: x.amount }; });
      var next = ss.recurring && ss.recurring.dueNext && ss.recurring.dueNext.total ? ss.recurring.dueNext.total.amount : '';
      summary({ items: items, discount: disc, tax: tax, total: ss.total && ss.total.total ? ss.total.total.amount : P.price, next: next });
    };
    paint(actions.getSession());
    checkout.on('change', paint);
    applyCode = function (code) { return actions.applyPromotionCode(code).then(function (r) { return !(r && r.type === 'error'); }, function () { return false; }); };
    var pe = checkout.createPaymentElement({ layout: 'tabs' });
    pe.mount('#pe');
    pe.on('ready', function () { $('pay').disabled = false; tell('ready'); });
    var pay = async function () {
      clearErr();
      if (!paypalWin && !$('terms').checked) return fail('terms');
      var ss = actions.getSession();
      if (!paypalWin && ss && ss.canConfirm === false) return fail('check');
      setBusy(true);
      spinning(paypalWin ? t('to_paypal') : t('processing'), t('dont_close'));
      // PayPal (finestra a parte) va sulla sua pagina; la carta resta qui (3D Secure compreso, lo mostra Stripe)
      if (paypalWin) { try { sessionStorage.setItem('nf-pay', JSON.stringify({ lang: P.lang, theme: P.theme, kind: P.kind, name: P.name, plan: P.plan, period: P.period, email: P.email })); } catch (e) { /* */ } }
      var r = await actions.confirm(paypalWin ? {} : { redirect: 'if_required' });
      if (r && r.type === 'error') {
        var e = r.error || {}, code = String(e.code || ''), dc = String(e.declineCode || e.decline_code || '');
        var key = dc === 'insufficient_funds' ? 'funds' : /authentication/.test(code + ' ' + dc) ? '3ds_no' : /incomplete|invalid|incorrect|validation/.test(code) && !/declin/.test(code) ? 'check' : 'declined';
        return fail(key, [code, dc, ss && ss.id].filter(Boolean).join(' · '));
      }
      done();
    };
    $('pay').addEventListener('click', function () { if (!busy) pay().catch(function (e) { fail('declined', String(e && e.message || e)); }); });
    // finestra di PayPal: i Termini li hai gia' accettati nel foglio, si va subito su PayPal
    if (paypalWin) pe.on('ready', function () { pay().catch(function (e) { fail('declined', String(e && e.message || e)); }); });
  }

  // ---------------------------------------------------------------- modalita' prova senza Stripe
  function mockPay() {
    var box = $('mockpe'), price = Number(String(P.price || '0').replace(/[^\d,.-]/g, '').replace(',', '.')) || 9.99, off = 0;
    var money = function (n) { return n.toLocaleString(LOCALE, { style: 'currency', currency: 'EUR' }); };
    var paint = function () {
      var tot = Math.round(price * (1 - off) * 100) / 100;
      summary({ items: [{ name: P.name || '', amount: money(price) }], discount: off ? [{ label: t('discount', { code: 'NOON20' }), amount: money(price - tot) }] : [], total: money(tot) });
    };
    $('pe').hidden = true; box.hidden = false;
    var field = function (key, ph, wide, id) {
      var l = el('label', wide ? 'w' : null, t(key)), i = el('input');
      i.placeholder = ph; i.id = id; i.inputMode = 'numeric'; l.appendChild(i); box.appendChild(l); return i;
    };
    var num = field('card_number', '1234 1234 1234 1234', true, 'mnum');
    field('expiry', { en: 'MM / YY', de: 'MM / JJ' }[LANG] || 'MM / AA', false, 'mexp'); field('cvc', 'CVC', false, 'mcvc');
    box.appendChild(el('p', 'hint', t('test_cards')));
    applyCode = function (code) { return new Promise(function (res) { setTimeout(function () { var ok = code.toUpperCase() === 'NOON20'; if (ok) { off = 0.2; paint(); } res(ok); }, 400); }); };
    paint();
    $('pay').disabled = false;
    tell('ready');
    $('pay').addEventListener('click', function () {
      if (busy) return;
      clearErr();
      if (!$('terms').checked) return fail('terms');
      var n = num.value.replace(/\D/g, '');
      if (n.length < 15 || !/^\d{2}\s*\/\s*\d{2}$/.test($('mexp').value.trim()) || $('mcvc').value.trim().length < 3) return fail('check');
      setBusy(true);
      spinning(t('processing'), t('dont_close'));
      var end = n.slice(-4);
      setTimeout(function () {
        if (end === '0002') return fail('declined', 'card_declined · generic_decline · mock');
        if (end === '9995') return fail('funds', 'card_declined · insufficient_funds · mock');
        if (end === '3184') {
          var bank = el('div', 'pg-bank');
          bank.appendChild(el('p', 'big', t('bank_title'))); bank.appendChild(el('p', 'muted', t('bank_sub'))); bank.appendChild(el('p', null, t('bank_text', { p: $('total').textContent })));
          showState([bank]);
          return setTimeout(done, 2200);
        }
        done();
      }, 900);
    });
  }
})();

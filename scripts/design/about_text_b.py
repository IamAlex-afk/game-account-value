# "About" page — ar, vi, hi, fr, de, it (adapted from about_text_a.py 'en')
from about_text_a import M, GH, BOT
TEXT = {
'ar': {'about': {
 'title': 'عن GameAccountValue',
 'desc': 'ماذا يقدّم GameAccountValue، ومن أين تأتي نطاقات الأسعار، وكيف يُموَّل المشروع، وما الذي لا يفعله أبدًا.',
 'h1': 'عن GameAccountValue',
 'lead': 'حاسبة مجانية على هذا الموقع وبوت تقييم بالذكاء الاصطناعي في تيليجرام، مبنيّان على بيانات سوق مؤرَّخة ويمكن التحقق منها.',
 'sec': [
  ('ماذا تقدّم الخدمة', '<ul><li><strong>على هذا الموقع:</strong> حاسبة مجانية لكل لعبة من الألعاب التسع تعطيك نطاقًا تقريبيًا داخل متصفحك — دون إرسال أي شيء.</li><li><strong>في البوت:</strong> تقدير مجاني واحد يوميًا من لقطة شاشة واحدة.</li><li><strong>الفحص الكامل المدفوع</strong> (2–3 لقطات، والدفع بنجوم تيليجرام): نطاق سعري مع مستوى الثقة والسيولة، وبطاقة PDF مرقّمة قابلة للاقتناء مع تحقق عبر رمز QR، وفيديو قصير.</li></ul>'),
  ('من أين تأتي الأرقام', '<p>تُبنى نطاقات الأسعار من إعلانات حيّة في الأسواق تُراجَع يدويًا، ويظهر تاريخ المراجعة في كل صفحة. وهي <strong>أسعار يطلبها البائعون، وليست مبيعات مؤكَّدة</strong>، لذا فكل نتيجة نطاقٌ وليست عرض سعر. ولا يُذكر عنصر بوصفه عاملًا في القيمة إلا إذا ظهر في إعلانين مستقلين أو أكثر من بين الأعلى سعرًا. القواعد كاملة في <a href="./methodology.html">صفحة المنهجية</a>.</p>'),
  ('ما لا نفعله أبدًا', '<ul><li>طلب أسماء الدخول أو كلمات المرور للألعاب.</li><li>حفظ لقطات شاشتك.</li><li>عرض إعلانات أو أدوات تتبّع أو ملفات كوكيز على هذا الموقع.</li><li>جمع البيانات من الأسواق آليًا — فالإعلانات يراجعها إنسان.</li></ul>'),
  ('كيف يُموَّل المشروع', '<p>فقط من الفحوص المدفوعة في البوت، التي تُدفع بنجوم تيليجرام. واليوم لا يوجد أي موقع في التصنيفات أو التقديرات على هذا الموقع مدفوع الثمن؛ وإذا ظهر رابط مموَّل يومًا ما، فسيُوسَم بوضوح بأنه مموَّل.</p>'),
  ('وجدت خطأ؟', f'<p>الأسعار تتغيّر والترجمات قد تخطئ. إذا رأيت رقمًا خاطئًا أو معلومة قديمة أو ترجمة ركيكة، فاكتب إلى {BOT} — ستُصحَّح الصفحة ويُحدَّث تاريخها.</p>'),
  ('التواصل', f'<p>تيليجرام: {BOT} · الشيفرة وملف المؤلف: {GH}. راجع أيضًا <a href="./privacy.html">سياسة الخصوصية</a> و<a href="./terms.html">شروط الخدمة</a>.</p>'),
 ]}},
'vi': {'about': {
 'title': 'Giới thiệu GameAccountValue',
 'desc': 'GameAccountValue làm gì, các khoảng giá lấy từ đâu, dự án sống bằng gì và những điều dự án không bao giờ làm.',
 'h1': 'Giới thiệu GameAccountValue',
 'lead': 'Máy tính định giá miễn phí trên trang này và bot thẩm định bằng AI trên Telegram, dựa trên dữ liệu thị trường có ghi ngày và kiểm chứng được.',
 'sec': [
  ('Dịch vụ làm gì', '<ul><li><strong>Trên trang này:</strong> máy tính miễn phí cho từng game trong 9 game cho bạn khoảng giá ước lượng ngay trong trình duyệt — không gửi gì đi cả.</li><li><strong>Trong bot:</strong> mỗi ngày một lần ước tính miễn phí từ một ảnh chụp màn hình.</li><li><strong>Kiểm định đầy đủ trả phí</strong> (2–3 ảnh, trả bằng Telegram Stars): khoảng giá kèm mức độ tin cậy và thanh khoản, thẻ sưu tầm PDF có đánh số và mã QR xác minh, cùng một video ngắn.</li></ul>'),
  ('Các con số lấy từ đâu', '<p>Khoảng giá được xây dựng từ các tin đăng đang hoạt động trên chợ giao dịch, được kiểm tra thủ công và ghi ngày trên từng trang. Đó là <strong>giá người bán đưa ra, không phải giao dịch đã xác nhận</strong>, nên mọi kết quả đều là một khoảng chứ không phải báo giá. Một vật phẩm chỉ được gọi là yếu tố tạo giá trị nếu nó xuất hiện trong từ hai tin đăng giá cao độc lập trở lên. Toàn bộ quy tắc có ở <a href="./methodology.html">trang phương pháp</a>.</p>'),
  ('Những điều chúng tôi không bao giờ làm', '<ul><li>Hỏi tên đăng nhập hoặc mật khẩu game.</li><li>Lưu ảnh chụp màn hình của bạn.</li><li>Đặt quảng cáo, công cụ theo dõi hay cookie trên trang này.</li><li>Tự động thu thập dữ liệu từ các chợ giao dịch — tin đăng do con người kiểm tra.</li></ul>'),
  ('Dự án sống bằng gì', '<p>Chỉ bằng các bản kiểm định trả phí trong bot, thanh toán bằng Telegram Stars. Hiện không có vị trí nào trong bảng xếp hạng hay ước tính trên trang này là trả tiền; nếu sau này có liên kết được tài trợ, nó sẽ được ghi rõ là tài trợ.</p>'),
  ('Bạn thấy lỗi?', f'<p>Giá cả thay đổi và bản dịch có thể sai sót. Nếu bạn thấy con số sai, thông tin lỗi thời hay câu dịch vụng về, hãy nhắn cho {BOT} — trang sẽ được sửa và cập nhật ngày.</p>'),
  ('Liên hệ', f'<p>Telegram: {BOT} · Mã nguồn và hồ sơ tác giả: {GH}. Xem thêm <a href="./privacy.html">chính sách bảo mật</a> và <a href="./terms.html">điều khoản dịch vụ</a>.</p>'),
 ]}},
'hi': {'about': {
 'title': 'GameAccountValue के बारे में',
 'desc': 'GameAccountValue क्या करता है, कीमतों की रेंज कहाँ से आती है, प्रोजेक्ट का ख़र्च कैसे चलता है और यह क्या कभी नहीं करता।',
 'h1': 'GameAccountValue के बारे में',
 'lead': 'इस साइट पर मुफ़्त कैलकुलेटर और Telegram में AI मूल्यांकन बॉट, जो तारीख़ वाले और जाँचे जा सकने वाले बाज़ार डेटा पर आधारित हैं।',
 'sec': [
  ('सेवा क्या करती है', '<ul><li><strong>इस साइट पर:</strong> 9 गेम में से हर एक के लिए मुफ़्त कैलकुलेटर आपके ब्राउज़र में ही अनुमानित रेंज देता है — कुछ भी कहीं नहीं भेजा जाता।</li><li><strong>बॉट में:</strong> एक स्क्रीनशॉट से रोज़ एक मुफ़्त अनुमान।</li><li><strong>पेड पूरा ऑडिट</strong> (2–3 स्क्रीनशॉट, Telegram Stars में भुगतान): भरोसे के स्तर और लिक्विडिटी के साथ कीमत की रेंज, QR सत्यापन वाला नंबर वाला PDF कलेक्टर कार्ड और एक छोटा वीडियो।</li></ul>'),
  ('आँकड़े कहाँ से आते हैं', '<p>कीमत की रेंज मार्केटप्लेस की लाइव लिस्टिंग से बनती है, जिन्हें हाथ से जाँचा जाता है और हर पेज पर जाँच की तारीख़ लिखी होती है। ये <strong>विक्रेताओं की माँगी गई कीमतें हैं, पक्की बिक्री नहीं</strong>, इसलिए हर परिणाम एक रेंज है, कोई तय कीमत नहीं। किसी आइटम को तभी कीमत बढ़ाने वाला बताया जाता है जब वह सबसे महँगी दो या ज़्यादा स्वतंत्र लिस्टिंग में दिखे। सारे नियम <a href="./methodology.html">मेथडोलॉजी पेज</a> पर हैं।</p>'),
  ('हम क्या कभी नहीं करते', '<ul><li>गेम लॉगिन या पासवर्ड माँगना।</li><li>आपके स्क्रीनशॉट सेव करना।</li><li>इस साइट पर विज्ञापन, ट्रैकर या कुकी लगाना।</li><li>मार्केटप्लेस से अपने आप डेटा निकालना — लिस्टिंग इंसान जाँचता है।</li></ul>'),
  ('प्रोजेक्ट का ख़र्च कैसे चलता है', '<p>सिर्फ़ बॉट के पेड ऑडिट से, जिनका भुगतान Telegram Stars में होता है। आज इस साइट की किसी रैंकिंग या अनुमान में कोई जगह पैसे देकर नहीं मिली है; अगर कभी कोई स्पॉन्सर्ड लिंक आया, तो उस पर साफ़ तौर पर स्पॉन्सर्ड लिखा होगा।</p>'),
  ('कोई ग़लती दिखी?', f'<p>कीमतें बदलती हैं और अनुवाद में चूक हो सकती है। अगर आपको कोई ग़लत आँकड़ा, पुरानी जानकारी या अटपटा अनुवाद दिखे, तो {BOT} पर लिखें — पेज ठीक किया जाएगा और उसकी तारीख़ अपडेट होगी।</p>'),
  ('संपर्क', f'<p>Telegram: {BOT} · कोड और लेखक प्रोफ़ाइल: {GH}. <a href="./privacy.html">प्राइवेसी पॉलिसी</a> और <a href="./terms.html">सेवा शर्तें</a> भी देखें।</p>'),
 ]}},
'fr': {'about': {
 'title': 'À propos de GameAccountValue',
 'desc': 'Ce que fait GameAccountValue, d’où viennent ses fourchettes de prix, comment le projet est financé et ce qu’il ne fait jamais.',
 'h1': 'À propos de GameAccountValue',
 'lead': 'Un calculateur gratuit sur ce site et un bot d’estimation par IA sur Telegram, fondés sur des données de marché datées et vérifiables.',
 'sec': [
  ('Ce que fait le service', '<ul><li><strong>Sur ce site :</strong> un calculateur gratuit pour chacun des 9 jeux donne une fourchette approximative directement dans votre navigateur — rien n’est envoyé.</li><li><strong>Dans le bot :</strong> une estimation gratuite par jour à partir d’une seule capture.</li><li><strong>Audit complet payant</strong> (2–3 captures, payé en Telegram Stars) : fourchette de prix avec niveau de confiance et liquidité, carte à collectionner numérotée en PDF avec vérification par QR, et une courte vidéo.</li></ul>'),
  ('D’où viennent les chiffres', '<p>Les fourchettes de prix reposent sur des annonces actives de places de marché, vérifiées à la main et datées sur chaque page. Ce sont des <strong>prix demandés, pas des ventes confirmées</strong> : chaque résultat est donc une fourchette, pas un devis. Un objet n’est cité comme facteur de valeur que s’il apparaît dans au moins deux annonces indépendantes parmi les plus chères. Toutes les règles figurent sur la <a href="./methodology.html">page méthodologie</a>.</p>'),
  ('Ce que nous ne faisons jamais', '<ul><li>Demander des identifiants ou mots de passe de jeux.</li><li>Conserver vos captures d’écran.</li><li>Mettre des publicités, des traceurs ou des cookies sur ce site.</li><li>Collecter automatiquement les données des places de marché — les annonces sont vérifiées par une personne.</li></ul>'),
  ('Comment le projet est financé', '<p>Uniquement par les audits payants du bot, réglés en Telegram Stars. Aujourd’hui, aucune place dans un classement ou une estimation de ce site n’est payée ; si un lien sponsorisé apparaît un jour, il sera clairement signalé comme tel.</p>'),
  ('Vous avez repéré une erreur ?', f'<p>Les prix bougent et les traductions peuvent déraper. Si vous voyez un chiffre faux, une information périmée ou une traduction maladroite, écrivez à {BOT} : la page sera corrigée et sa date mise à jour.</p>'),
  ('Contact', f'<p>Telegram : {BOT} · Code et profil de l’auteur : {GH}. Voir aussi la <a href="./privacy.html">politique de confidentialité</a> et les <a href="./terms.html">conditions d’utilisation</a>.</p>'),
 ]}},
'de': {'about': {
 'title': 'Über GameAccountValue',
 'desc': 'Was GameAccountValue macht, woher die Preisspannen kommen, wie sich das Projekt finanziert und was es nie tut.',
 'h1': 'Über GameAccountValue',
 'lead': 'Ein kostenloser Rechner auf dieser Website und ein KI-Bewertungsbot in Telegram, gestützt auf datierte, überprüfbare Marktdaten.',
 'sec': [
  ('Was der Dienst macht', '<ul><li><strong>Auf dieser Website:</strong> Ein kostenloser Rechner für jedes der 9 Spiele liefert direkt im Browser eine grobe Spanne – es wird nichts gesendet.</li><li><strong>Im Bot:</strong> eine kostenlose Schätzung pro Tag anhand eines einzigen Screenshots.</li><li><strong>Bezahlte Komplettprüfung</strong> (2–3 Screenshots, Zahlung in Telegram Stars): Preisspanne mit Sicherheit und Liquidität, eine nummerierte PDF-Sammelkarte mit QR-Prüfung und ein kurzes Video.</li></ul>'),
  ('Woher die Zahlen kommen', '<p>Die Preisspannen beruhen auf aktiven Marktplatz-Angeboten, die von Hand geprüft und auf jeder Seite mit Datum versehen werden. Es sind <strong>Angebotspreise, keine bestätigten Verkäufe</strong> – deshalb ist jedes Ergebnis eine Spanne und kein Angebot. Ein Gegenstand wird nur dann als Werttreiber genannt, wenn er in mindestens zwei unabhängigen Top-Preis-Angeboten vorkommt. Alle Regeln stehen auf der <a href="./methodology.html">Methodik-Seite</a>.</p>'),
  ('Was wir nie tun', '<ul><li>Nach Spiel-Logins oder Passwörtern fragen.</li><li>Deine Screenshots speichern.</li><li>Werbung, Tracker oder Cookies auf dieser Website einsetzen.</li><li>Marktplätze automatisch auslesen – Angebote prüft ein Mensch.</li></ul>'),
  ('Wie sich das Projekt finanziert', '<p>Ausschließlich über bezahlte Prüfungen im Bot, bezahlt in Telegram Stars. Derzeit ist kein Platz in Rankings oder Schätzungen auf dieser Website bezahlt; sollte je ein gesponserter Link erscheinen, wird er klar als gesponsert gekennzeichnet.</p>'),
  ('Einen Fehler gefunden?', f'<p>Preise ändern sich, und Übersetzungen können danebenliegen. Wenn du eine falsche Zahl, eine veraltete Angabe oder eine holprige Übersetzung siehst, schreib an {BOT} – die Seite wird korrigiert und ihr Datum aktualisiert.</p>'),
  ('Kontakt', f'<p>Telegram: {BOT} · Code und Autorenprofil: {GH}. Siehe auch die <a href="./privacy.html">Datenschutzerklärung</a> und die <a href="./terms.html">Nutzungsbedingungen</a>.</p>'),
 ]}},
'it': {'about': {
 'title': 'Chi siamo: GameAccountValue',
 'desc': 'Cosa fa GameAccountValue, da dove vengono le sue fasce di prezzo, come si finanzia il progetto e cosa non fa mai.',
 'h1': 'Chi siamo',
 'lead': 'Un calcolatore gratuito su questo sito e un bot di stima con IA su Telegram, basati su dati di mercato datati e verificabili.',
 'sec': [
  ('Cosa fa il servizio', '<ul><li><strong>Su questo sito:</strong> un calcolatore gratuito per ciascuno dei 9 giochi ti dà una fascia indicativa direttamente nel browser, senza inviare nulla.</li><li><strong>Nel bot:</strong> una stima gratuita al giorno con un solo screenshot.</li><li><strong>Report completo a pagamento</strong> (2–3 screenshot, pagamento in Telegram Stars): fascia di prezzo con livello di affidabilità e liquidità, carta da collezione numerata in PDF con verifica tramite QR e un breve video.</li></ul>'),
  ('Da dove vengono i numeri', '<p>Le fasce di prezzo si basano su annunci attivi dei marketplace, controllati a mano e datati su ogni pagina. Sono <strong>prezzi richiesti, non vendite confermate</strong>: ogni risultato è quindi una fascia, non un preventivo. Un oggetto viene indicato come fattore di valore solo se compare in almeno due annunci indipendenti tra i più cari. Tutte le regole sono nella <a href="./methodology.html">pagina sulla metodologia</a>.</p>'),
  ('Cosa non facciamo mai', '<ul><li>Chiedere login o password dei giochi.</li><li>Conservare i tuoi screenshot.</li><li>Usare pubblicità, tracker o cookie su questo sito.</li><li>Raccogliere dati dai marketplace in modo automatico: gli annunci li controlla una persona.</li></ul>'),
  ('Come si finanzia il progetto', '<p>Solo con i report a pagamento del bot, pagati in Telegram Stars. Oggi nessuna posizione in classifiche o stime di questo sito è a pagamento; se un giorno comparirà un link sponsorizzato, sarà chiaramente indicato come tale.</p>'),
  ('Hai trovato un errore?', f'<p>I prezzi cambiano e le traduzioni possono sbagliare. Se vedi un numero errato, un’informazione superata o una traduzione goffa, scrivi a {BOT}: la pagina verrà corretta e la sua data aggiornata.</p>'),
  ('Contatti', f'<p>Telegram: {BOT} · Codice e profilo dell’autore: {GH}. Vedi anche l’<a href="./privacy.html">informativa sulla privacy</a> e i <a href="./terms.html">termini di servizio</a>.</p>'),
 ]}},
}

# "About" page — ja, ko, zh, th, pl, tl (adapted from about_text_a.py 'en')
from about_text_a import M, GH, BOT
TEXT = {
'ja': {'about': {
 'title': 'GameAccountValue について',
 'desc': 'GameAccountValue のサービス内容、価格帯の根拠、運営資金、そして決してしないこと。',
 'h1': 'GameAccountValue について',
 'lead': 'このサイトの無料計算ツールと Telegram の AI 査定ボットは、日付入りで検証できる市場データに基づいています。',
 'sec': [
  ('サービス内容', '<ul><li><strong>このサイト：</strong>9つのゲームそれぞれに無料の計算ツールがあり、ブラウザ内でおおよその価格帯がわかります。データはどこにも送信されません。</li><li><strong>ボット：</strong>スクリーンショット1枚で、1日1回の無料査定。</li><li><strong>有料の詳細査定</strong>（スクリーンショット2〜3枚、Telegram Stars で支払い）：信頼度と流動性つきの価格帯、QR で照合できる番号入り PDF コレクションカード、短い動画。</li></ul>'),
  ('数字の根拠', '<p>価格帯は、マーケットプレイスに出ている現行の出品を手作業で確認して作っており、確認日は各ページに記載しています。これは<strong>売り手の希望価格であり、成立した取引価格ではありません</strong>。そのため結果は常に幅のある価格帯で、見積もりではありません。高額出品のうち独立した2件以上に登場したアイテムだけを、価値を左右する要素として挙げています。ルールの詳細は<a href="./methodology.html">調査方法のページ</a>をご覧ください。</p><p>調査・翻訳・コードには AI ツールを使っていますが、何を皆さんに届けるかは、このページに書いたルールで決めています。</p>'),
  ('私たちが決してしないこと', '<ul><li>ゲームのログイン情報やパスワードを尋ねること。</li><li>スクリーンショットの保存。</li><li>このサイトでの広告・トラッカー・Cookie の使用。</li><li>マーケットプレイスからの自動収集——出品は人が確認しています。</li></ul>'),
  ('運営資金', '<p>ボットの有料査定（Telegram Stars での支払い）だけで運営しています。現在、このサイトのランキングや査定で、お金を受け取って掲載している枠は一つもありません。将来スポンサーリンクを置く場合は、スポンサーであることを明示します。</p>'),
  ('誤りを見つけたら', f'<p>価格は変わりますし、翻訳に不備があることもあります。間違った数字、古い情報、不自然な翻訳を見つけたら、{BOT} までお知らせください。ページを修正し、確認日を更新します。</p>'),
  ('お問い合わせ', f'<p>Telegram：{BOT} · コードと作者のプロフィール：{GH}。<a href="./privacy.html">プライバシーポリシー</a>と<a href="./terms.html">利用規約</a>もあわせてご覧ください。</p>'),
 ]}},
'ko': {'about': {
 'title': 'GameAccountValue 소개',
 'desc': 'GameAccountValue가 하는 일, 가격 범위의 근거, 운영 자금, 그리고 절대 하지 않는 일.',
 'h1': 'GameAccountValue 소개',
 'lead': '이 사이트의 무료 계산기와 텔레그램 AI 감정 봇은 날짜가 표시된, 확인 가능한 시장 데이터를 바탕으로 합니다.',
 'sec': [
  ('서비스 내용', '<ul><li><strong>이 사이트:</strong> 9개 게임마다 무료 계산기가 있어 브라우저 안에서 대략적인 가격 범위를 알려 줍니다. 아무것도 전송되지 않습니다.</li><li><strong>봇:</strong> 스크린샷 한 장으로 하루 한 번 무료 감정.</li><li><strong>유료 전체 감정</strong>(스크린샷 2–3장, 텔레그램 스타 결제): 신뢰도와 유동성이 표시된 가격 범위, QR로 검증되는 번호 매긴 PDF 컬렉션 카드, 짧은 영상.</li></ul>'),
  ('숫자의 출처', '<p>가격 범위는 마켓플레이스에 올라와 있는 실제 매물을 사람이 직접 확인해 만들며, 확인 날짜는 모든 페이지에 적혀 있습니다. 이는 <strong>판매자의 호가이지 확정된 거래가가 아니므로</strong>, 결과는 항상 견적이 아닌 범위로 제시됩니다. 최고가 매물 중 독립된 두 건 이상에 등장한 아이템만 가치를 좌우하는 요소로 소개합니다. 모든 규칙은 <a href="./methodology.html">조사 방법 페이지</a>에 있습니다.</p><p>조사·번역·코드 작업에는 AI 도구가 도움을 주지만, 여러분에게 무엇이 전달될지는 이 페이지의 규칙이 결정합니다.</p>'),
  ('절대 하지 않는 일', '<ul><li>게임 로그인 정보나 비밀번호 요청.</li><li>스크린샷 저장.</li><li>이 사이트에 광고·추적기·쿠키 사용.</li><li>마켓플레이스 자동 수집 — 매물은 사람이 확인합니다.</li></ul>'),
  ('운영 자금', '<p>봇의 유료 감정(텔레그램 스타 결제)으로만 운영합니다. 현재 이 사이트의 순위나 감정에서 돈을 받고 넣은 자리는 하나도 없으며, 앞으로 스폰서 링크가 생긴다면 스폰서임을 분명히 표시하겠습니다.</p>'),
  ('오류를 발견했나요?', f'<p>가격은 바뀌고 번역에는 실수가 있을 수 있습니다. 틀린 숫자, 오래된 정보, 어색한 번역을 발견하면 {BOT}으로 알려 주세요. 페이지를 고치고 확인 날짜를 갱신합니다.</p>'),
  ('문의', f'<p>텔레그램: {BOT} · 코드와 제작자 프로필: {GH}. <a href="./privacy.html">개인정보처리방침</a>과 <a href="./terms.html">이용약관</a>도 참고하세요.</p>'),
 ]}},
'zh': {'about': {
 'title': '关于 GameAccountValue',
 'desc': 'GameAccountValue 做什么、价格区间从何而来、项目靠什么维持，以及它绝不会做的事。',
 'h1': '关于 GameAccountValue',
 'lead': '本站的免费计算器和 Telegram 上的 AI 估值机器人，均基于标注日期、可核查的市场数据。',
 'sec': [
  ('服务内容', '<ul><li><strong>本站：</strong>9 款游戏各有一个免费计算器，直接在浏览器中给出大致价格区间——不会发送任何数据。</li><li><strong>机器人：</strong>每天可用一张截图免费估算一次。</li><li><strong>付费完整评估</strong>（2–3 张截图，用 Telegram Stars 支付）：附带可信度和流动性的价格区间、可通过二维码验证的编号 PDF 收藏卡牌，以及一段短视频。</li></ul>'),
  ('数字从何而来', '<p>价格区间依据各交易平台上的在售挂单整理而成，均为人工核查，每个页面都标注了核查日期。这些是<strong>卖家的要价，而非已确认的成交价</strong>，因此结果始终是一个区间，而不是报价。只有在两条及以上相互独立的高价挂单中都出现的物品，才会被列为影响价值的因素。完整规则见<a href="./methodology.html">方法说明页</a>。</p><p>AI 工具协助调研、翻译和编写代码；而最终呈现给你的内容，由本页列出的规则决定。</p>'),
  ('我们绝不会做的事', '<ul><li>索要游戏账号或密码。</li><li>保存你的截图。</li><li>在本站投放广告、追踪器或 Cookie。</li><li>自动抓取交易平台数据——挂单由人工核查。</li></ul>'),
  ('项目靠什么维持', '<p>仅靠机器人中的付费评估，使用 Telegram Stars 支付。目前本站的任何排名或估值中都没有付费位置；如果将来出现赞助链接，会明确标注为赞助。</p>'),
  ('发现错误？', f'<p>价格会变，翻译也可能出错。如果你发现数字有误、信息过时或翻译生硬，请联系 {BOT}——我们会修正页面并更新核查日期。</p>'),
  ('联系方式', f'<p>Telegram：{BOT} · 代码与作者主页：{GH}。另请参阅<a href="./privacy.html">隐私政策</a>和<a href="./terms.html">服务条款</a>。</p>'),
 ]}},
'th': {'about': {
 'title': 'เกี่ยวกับ GameAccountValue',
 'desc': 'GameAccountValue ทำอะไร ช่วงราคามาจากไหน โครงการอยู่ได้ด้วยอะไร และสิ่งที่ไม่เคยทำ',
 'h1': 'เกี่ยวกับ GameAccountValue',
 'lead': 'เครื่องคำนวณฟรีบนเว็บไซต์นี้และบอทประเมินราคาด้วย AI บน Telegram ที่อิงข้อมูลตลาดซึ่งระบุวันที่และตรวจสอบได้',
 'sec': [
  ('บริการทำอะไร', '<ul><li><strong>บนเว็บไซต์นี้:</strong> เครื่องคำนวณฟรีสำหรับแต่ละเกมจาก 9 เกม ให้ช่วงราคาคร่าว ๆ ในเบราว์เซอร์ของคุณ โดยไม่ส่งข้อมูลไปไหน</li><li><strong>ในบอท:</strong> ประเมินฟรีวันละครั้งจากภาพหน้าจอภาพเดียว</li><li><strong>การตรวจสอบเต็มรูปแบบแบบชำระเงิน</strong> (ภาพหน้าจอ 2–3 ภาพ ชำระด้วย Telegram Stars): ช่วงราคาพร้อมระดับความมั่นใจและสภาพคล่อง การ์ดสะสม PDF แบบมีหมายเลขพร้อมการยืนยันด้วย QR และวิดีโอสั้น</li></ul>'),
  ('ตัวเลขมาจากไหน', '<p>ช่วงราคาสร้างจากประกาศขายที่ยังเปิดอยู่บนตลาดซื้อขาย ซึ่งตรวจสอบด้วยมือ และระบุวันที่ตรวจไว้ทุกหน้า ตัวเลขเหล่านี้คือ<strong>ราคาที่ผู้ขายตั้ง ไม่ใช่ราคาที่ขายได้จริง</strong> ผลลัพธ์จึงเป็นช่วงราคาเสมอ ไม่ใช่ใบเสนอราคา ไอเทมจะถูกระบุว่าเป็นปัจจัยด้านมูลค่าก็ต่อเมื่อปรากฏในประกาศราคาสูงสุดที่เป็นอิสระต่อกันตั้งแต่สองรายการขึ้นไป กฎทั้งหมดอยู่ใน<a href="./methodology.html">หน้าระเบียบวิธี</a></p><p>เครื่องมือ AI ช่วยด้านการค้นคว้า การแปล และการเขียนโค้ด ส่วนสิ่งที่ส่งถึงคุณนั้นตัดสินด้วยกฎในหน้านี้</p>'),
  ('สิ่งที่เราไม่เคยทำ', '<ul><li>ขอข้อมูลล็อกอินหรือรหัสผ่านเกม</li><li>เก็บภาพหน้าจอของคุณ</li><li>ใช้โฆษณา ตัวติดตาม หรือคุกกี้บนเว็บไซต์นี้</li><li>ดึงข้อมูลจากตลาดซื้อขายโดยอัตโนมัติ — ประกาศขายตรวจสอบโดยคน</li></ul>'),
  ('โครงการอยู่ได้ด้วยอะไร', '<p>จากการตรวจสอบแบบชำระเงินในบอทเท่านั้น ซึ่งชำระด้วย Telegram Stars ปัจจุบันไม่มีตำแหน่งใดในอันดับหรือการประเมินบนเว็บไซต์นี้ที่มีการจ่ายเงิน หากวันหนึ่งมีลิงก์สปอนเซอร์ จะระบุชัดเจนว่าเป็นสปอนเซอร์</p>'),
  ('พบข้อผิดพลาด?', f'<p>ราคาเปลี่ยนแปลงได้และคำแปลอาจผิดพลาด หากคุณเห็นตัวเลขผิด ข้อมูลล้าสมัย หรือคำแปลที่ไม่เป็นธรรมชาติ แจ้งมาที่ {BOT} เราจะแก้ไขหน้าและอัปเดตวันที่</p>'),
  ('ติดต่อ', f'<p>Telegram: {BOT} · โค้ดและโปรไฟล์ผู้สร้าง: {GH} ดูเพิ่มเติมที่<a href="./privacy.html">นโยบายความเป็นส่วนตัว</a>และ<a href="./terms.html">ข้อกำหนดการให้บริการ</a></p>'),
 ]}},
'pl': {'about': {
 'title': 'O GameAccountValue',
 'desc': 'Co robi GameAccountValue, skąd biorą się przedziały cen, z czego utrzymuje się projekt i czego nigdy nie robi.',
 'h1': 'O GameAccountValue',
 'lead': 'Darmowy kalkulator na tej stronie i bot wyceniający z AI na Telegramie, oparte na datowanych, sprawdzalnych danych rynkowych.',
 'sec': [
  ('Co robi usługa', '<ul><li><strong>Na tej stronie:</strong> darmowy kalkulator dla każdej z 9 gier podaje przybliżony przedział w przeglądarce — nic nie jest nigdzie wysyłane.</li><li><strong>W bocie:</strong> jedna darmowa wycena dziennie na podstawie jednego zrzutu ekranu.</li><li><strong>Płatny pełny audyt</strong> (2–3 zrzuty, płatność w Telegram Stars): przedział ceny z poziomem pewności i płynnością, numerowana karta kolekcjonerska PDF z weryfikacją QR i krótki film.</li></ul>'),
  ('Skąd biorą się liczby', '<p>Przedziały cen powstają na podstawie aktywnych ogłoszeń na marketplace’ach, sprawdzanych ręcznie i datowanych na każdej stronie. To <strong>ceny wystawione przez sprzedających, a nie potwierdzone transakcje</strong>, dlatego każdy wynik jest przedziałem, a nie ofertą. Przedmiot wskazujemy jako czynnik wartości tylko wtedy, gdy pojawia się w co najmniej dwóch niezależnych najdroższych ogłoszeniach. Wszystkie zasady są na <a href="./methodology.html">stronie metodologii</a>.</p><p>Narzędzia AI pomagają w researchu, tłumaczeniach i kodzie; o tym, co do Ciebie trafia, decydują zasady opisane na tej stronie.</p>'),
  ('Czego nigdy nie robimy', '<ul><li>Nie prosimy o loginy ani hasła do gier.</li><li>Nie przechowujemy Twoich zrzutów ekranu.</li><li>Nie używamy na tej stronie reklam, trackerów ani plików cookie.</li><li>Nie pobieramy danych z marketplace’ów automatycznie — ogłoszenia sprawdza człowiek.</li></ul>'),
  ('Z czego utrzymuje się projekt', '<p>Wyłącznie z płatnych audytów w bocie, opłacanych w Telegram Stars. Obecnie żadne miejsce w rankingach ani wycenach na tej stronie nie jest płatne; jeśli kiedyś pojawi się link sponsorowany, zostanie wyraźnie oznaczony jako sponsorowany.</p>'),
  ('Widzisz błąd?', f'<p>Ceny się zmieniają, a tłumaczenia mogą zawieść. Jeśli widzisz błędną liczbę, nieaktualny fakt albo niezgrabne tłumaczenie, napisz do {BOT} — strona zostanie poprawiona, a jej data zaktualizowana.</p>'),
  ('Kontakt', f'<p>Telegram: {BOT} · Kod i profil autora: {GH}. Zobacz też <a href="./privacy.html">politykę prywatności</a> i <a href="./terms.html">regulamin</a>.</p>'),
 ]}},
'tl': {'about': {
 'title': 'Tungkol sa GameAccountValue',
 'desc': 'Ano ang ginagawa ng GameAccountValue, saan galing ang mga price range, paano pinopondohan ang proyekto at ano ang hindi nito kailanman ginagawa.',
 'h1': 'Tungkol sa GameAccountValue',
 'lead': 'Libreng calculator sa site na ito at AI appraisal bot sa Telegram, batay sa market data na may petsa at puwedeng suriin.',
 'sec': [
  ('Ano ang ginagawa ng serbisyo', '<ul><li><strong>Sa site na ito:</strong> may libreng calculator para sa bawat isa sa 9 na laro na nagbibigay ng tinatayang range mismo sa iyong browser — walang ipinapadala kahit saan.</li><li><strong>Sa bot:</strong> isang libreng estimate kada araw mula sa isang screenshot.</li><li><strong>Bayad na full audit</strong> (2–3 screenshot, bayad sa Telegram Stars): price range na may confidence at liquidity, may numerong PDF collector card na may QR verification, at maikling video.</li></ul>'),
  ('Saan galing ang mga numero', '<p>Binubuo ang mga price range mula sa mga aktibong listing sa marketplace na mano-manong sinusuri, at may petsa ng pagsusuri sa bawat page. Ang mga ito ay <strong>hinihinging presyo ng nagbebenta, hindi kumpirmadong bentahan</strong>, kaya range ang bawat resulta at hindi quote. Tinatawag lang na value driver ang isang item kung lumalabas ito sa dalawa o higit pang independiyenteng pinakamahal na listing. Nasa <a href="./methodology.html">page ng metodolohiya</a> ang lahat ng panuntunan.</p><p>Tumutulong ang mga AI tool sa pananaliksik, pagsasalin at code; ang mga panuntunan sa page na ito ang nagpapasya kung ano ang aabot sa iyo.</p>'),
  ('Ang hindi namin kailanman ginagawa', '<ul><li>Humingi ng login o password ng laro.</li><li>Itago ang iyong mga screenshot.</li><li>Maglagay ng ads, tracker o cookie sa site na ito.</li><li>Awtomatikong kumuha ng data sa mga marketplace — tao ang sumusuri ng mga listing.</li></ul>'),
  ('Paano pinopondohan ang proyekto', '<p>Sa bayad na audit lang sa bot, na binabayaran sa Telegram Stars. Sa ngayon, walang posisyon sa anumang ranking o estimate sa site na ito ang binayaran; kung may lalabas na sponsored link balang araw, malinaw itong mamarkahang sponsored.</p>'),
  ('May nakitang mali?', f'<p>Gumagalaw ang presyo at puwedeng magkamali ang salin. Kung may makita kang maling numero, lumang impormasyon o pangit na salin, sumulat sa {BOT} — itatama ang page at ia-update ang petsa nito.</p>'),
  ('Makipag-ugnayan', f'<p>Telegram: {BOT} · Code at profile ng may-akda: {GH}. Tingnan din ang <a href="./privacy.html">Patakaran sa Privacy</a> at ang <a href="./terms.html">Mga Tuntunin ng Serbisyo</a>.</p>'),
 ]}},
}

(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var LANG = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
  if (["en", "ru", "id", "pt", "es", "fr", "ar", "de", "tr", "vi", "hi", "it", "ja", "ko", "zh", "pl", "th"].indexOf(LANG) === -1) LANG = "en";

  function lerp(t, a, b) { return a + (b - a) * t; }

  function norm(v, min, max) {
    if (max === min) return 0;
    var t = (v - min) / (max - min);
    return t < 0 ? 0 : t > 1 ? 1 : t;
  }

  // brackets: array of [low, high] anchor points spaced evenly across the 0..1 score.
  // These anchor values are copied verbatim from each page's own published price table —
  // the slider only interpolates between real, already-cited numbers, it never invents new ones.
  function interpBrackets(score, brackets) {
    var n = brackets.length;
    var scaled = score * (n - 1);
    var i = Math.min(Math.floor(scaled), n - 2);
    var t = scaled - i;
    var lo = lerp(t, brackets[i][0], brackets[i + 1][0]);
    var hi = lerp(t, brackets[i][1], brackets[i + 1][1]);
    return [lo, hi];
  }

  function formatMoney(n) {
    if (n < 10) return "$" + n.toFixed(2).replace(/\.00$/, "");
    if (n < 1000) return "$" + Math.round(n);
    var rounded = n < 10000 ? Math.round(n / 10) * 10 : Math.round(n / 100) * 100;
    return "$" + rounded.toLocaleString("en-US");
  }

  // --- i18n --------------------------------------------------------------
  // Only UI text is localized here. All scoring/pricing math below is
  // language-independent and identical across en/ru/id/pt.
  var STR = {
    en: {
      sliders: {
        "brawl-stars": { trophies: "Trophies (cups)", maxed: "Power Level 11 brawlers" },
        "clash-of-clans": { th: "Town Hall level" },
        "clash-royale": { kt: "King Tower level", maxed: "Max-level cards" },
        "free-fire": { rank: "Rank", bundles: "Rare bundles/pets" },
        "genshin-impact": { fivestars: "5★ characters", c6: "Characters with C6" },
        "mobile-legends": { skins: "Total skins", rank: "Rank" },
        "fortnite": { skins: "Total skins", ogItems: "Rare OG items" },
        "minecraft": { type: "Account type" },
        "roblox": { age: "Account age", robux: "Robux balance", limiteds: "Common Limited items (not named rares)" }
      },
      select: { "clash-of-clans": { label: "Upgrade type", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "year" : "years"); },
      minecraftTypes: ["Regular account", "MVP+/Hypixel, rare cape", "Minecon cape holder", "2-char name (alphanumeric)"],
      checkboxHeading: "Named rare items (optional):",
      confidence: { low: "Low", medium: "Medium", high: "High" },
      confidencePrefix: "Confidence: ",
      copiedFallback: "Copied!",
      gamepad: { up: "Previous field", down: "Next field", left: "Decrease", right: "Increase", a: "Reset all fields", b: "Share result", resetCaption: "RESET", shareCaption: "SHARE" }
    },
    ru: {
      sliders: {
        "brawl-stars": { trophies: "Трофеи (кубки)", maxed: "Бойцы Power Level 11" },
        "clash-of-clans": { th: "Уровень Ратуши (Town Hall)" },
        "clash-royale": { kt: "Уровень King Tower", maxed: "Карт максимального уровня" },
        "free-fire": { rank: "Ранг", bundles: "Редких бандлов/питомцев" },
        "genshin-impact": { fivestars: "5★ персонажей", c6: "Персонажей с C6" },
        "mobile-legends": { skins: "Всего скинов", rank: "Ранг" },
        "fortnite": { skins: "Всего скинов", ogItems: "Редких OG-предметов" },
        "minecraft": { type: "Тип аккаунта" },
        "roblox": { age: "Возраст аккаунта", robux: "Баланс Robux", limiteds: "Обычных Limited-предметов (не именных редких)" }
      },
      select: { "clash-of-clans": { label: "Тип прокачки", options: [["full", "Full Max"], ["standard", "Стандартный"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "год" : (v >= 2 && v <= 4 ? "года" : "лет")); },
      minecraftTypes: ["Обычный аккаунт", "MVP+/Hypixel, редкий скин плаща", "Держатель плаща Minecon", "2-симв. ник (алфавитно-цифровой)"],
      checkboxHeading: "Именные редкие предметы (опционально):",
      confidence: { low: "Низкая", medium: "Средняя", high: "Высокая" },
      confidencePrefix: "Уверенность: ",
      copiedFallback: "Скопировано!",
      gamepad: { up: "Предыдущее поле", down: "Следующее поле", left: "Уменьшить", right: "Увеличить", a: "Сбросить всё", b: "Поделиться результатом", resetCaption: "СБРОС", shareCaption: "ПОДЕЛИТЬСЯ" }
    },
    id: {
      sliders: {
        "brawl-stars": { trophies: "Trofi (cup)", maxed: "Brawler Power Level 11" },
        "clash-of-clans": { th: "Level Town Hall" },
        "clash-royale": { kt: "Level King Tower", maxed: "Kartu level maksimum" },
        "free-fire": { rank: "Rank", bundles: "Bundle/pet langka" },
        "genshin-impact": { fivestars: "Karakter 5★", c6: "Karakter dengan C6" },
        "mobile-legends": { skins: "Total skin", rank: "Rank" },
        "fortnite": { skins: "Total skin", ogItems: "Item OG langka" },
        "minecraft": { type: "Jenis akun" },
        "roblox": { age: "Usia akun", robux: "Saldo Robux", limiteds: "Item Limited biasa (bukan yang langka bernama)" }
      },
      select: { "clash-of-clans": { label: "Jenis upgrade", options: [["full", "Full Max"], ["standard", "Standar"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " tahun"; },
      minecraftTypes: ["Akun biasa", "MVP+/Hypixel, cape langka", "Pemilik cape Minecon", "Nama 2 karakter (alfanumerik)"],
      checkboxHeading: "Item langka bernama (opsional):",
      confidence: { low: "Rendah", medium: "Sedang", high: "Tinggi" },
      confidencePrefix: "Keyakinan: ",
      copiedFallback: "Disalin!",
      gamepad: { up: "Kolom sebelumnya", down: "Kolom berikutnya", left: "Kurangi", right: "Tambah", a: "Reset semua", b: "Bagikan hasil", resetCaption: "RESET", shareCaption: "BAGIKAN" }
    },
    pt: {
      sliders: {
        "brawl-stars": { trophies: "Troféus (copas)", maxed: "Brawlers Power Level 11" },
        "clash-of-clans": { th: "Nível do Town Hall" },
        "clash-royale": { kt: "Nível da King Tower", maxed: "Cartas no nível máximo" },
        "free-fire": { rank: "Rank", bundles: "Bundles/pets raros" },
        "genshin-impact": { fivestars: "Personagens 5★", c6: "Personagens com C6" },
        "mobile-legends": { skins: "Total de skins", rank: "Rank" },
        "fortnite": { skins: "Total de skins", ogItems: "Itens OG raros" },
        "minecraft": { type: "Tipo de conta" },
        "roblox": { age: "Idade da conta", robux: "Saldo de Robux", limiteds: "Itens Limited comuns (não os raros nomeados)" }
      },
      select: { "clash-of-clans": { label: "Tipo de evolução", options: [["full", "Full Max"], ["standard", "Padrão"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "ano" : "anos"); },
      minecraftTypes: ["Conta comum", "MVP+/Hypixel, cape raro", "Dono de cape Minecon", "Nick de 2 caracteres (alfanumérico)"],
      checkboxHeading: "Itens raros nomeados (opcional):",
      confidence: { low: "Baixa", medium: "Média", high: "Alta" },
      confidencePrefix: "Confiança: ",
      copiedFallback: "Copiado!",
      gamepad: { up: "Campo anterior", down: "Próximo campo", left: "Diminuir", right: "Aumentar", a: "Reiniciar tudo", b: "Compartilhar resultado", resetCaption: "REINICIAR", shareCaption: "COMPARTILHAR" }
    },
    es: {
      sliders: {
        "brawl-stars": { trophies: "Trofeos (copas)", maxed: "Brawlers Power Level 11" },
        "clash-of-clans": { th: "Nivel del Ayuntamiento (Town Hall)" },
        "clash-royale": { kt: "Nivel de la King Tower", maxed: "Cartas al nivel máximo" },
        "free-fire": { rank: "Rango", bundles: "Bundles/mascotas raras" },
        "genshin-impact": { fivestars: "Personajes 5★", c6: "Personajes con C6" },
        "mobile-legends": { skins: "Total de skins", rank: "Rango" },
        "fortnite": { skins: "Total de skins", ogItems: "Objetos OG raros" },
        "minecraft": { type: "Tipo de cuenta" },
        "roblox": { age: "Antigüedad de la cuenta", robux: "Saldo de Robux", limiteds: "Objetos Limited comunes (no los raros con nombre)" }
      },
      select: { "clash-of-clans": { label: "Tipo de mejora", options: [["full", "Full Max"], ["standard", "Estándar"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "año" : "años"); },
      minecraftTypes: ["Cuenta normal", "MVP+/Hypixel, capa rara", "Poseedor de la capa Minecon", "Nick de 2 caracteres (alfanumérico)"],
      checkboxHeading: "Objetos raros con nombre (opcional):",
      confidence: { low: "Baja", medium: "Media", high: "Alta" },
      confidencePrefix: "Confianza: ",
      copiedFallback: "¡Copiado!",
      gamepad: { up: "Campo anterior", down: "Campo siguiente", left: "Disminuir", right: "Aumentar", a: "Reiniciar todo", b: "Compartir resultado", resetCaption: "REINICIAR", shareCaption: "COMPARTIR" }
    },
    fr: {
      sliders: {
        "brawl-stars": { trophies: "Trophées (coupes)", maxed: "Brawlers Power Level 11" },
        "clash-of-clans": { th: "Niveau de l'Hôtel de Ville" },
        "clash-royale": { kt: "Niveau de la King Tower", maxed: "Cartes au niveau maximum" },
        "free-fire": { rank: "Rang", bundles: "Bundles/familiers rares" },
        "genshin-impact": { fivestars: "Personnages 5★", c6: "Personnages en C6" },
        "mobile-legends": { skins: "Total de skins", rank: "Rang" },
        "fortnite": { skins: "Total de skins", ogItems: "Objets OG rares" },
        "minecraft": { type: "Type de compte" },
        "roblox": { age: "Ancienneté du compte", robux: "Solde de Robux", limiteds: "Objets Limited courants (pas les rares nommés)" }
      },
      select: { "clash-of-clans": { label: "Type de progression", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "an" : "ans"); },
      minecraftTypes: ["Compte standard", "MVP+/Hypixel, cape rare", "Détenteur de la cape Minecon", "Pseudo à 2 caractères (alphanumérique)"],
      checkboxHeading: "Objets rares nommés (facultatif) :",
      confidence: { low: "Faible", medium: "Moyenne", high: "Élevée" },
      confidencePrefix: "Confiance : ",
      copiedFallback: "Copié !",
      gamepad: { up: "Champ précédent", down: "Champ suivant", left: "Diminuer", right: "Augmenter", a: "Tout réinitialiser", b: "Partager le résultat", resetCaption: "RESET", shareCaption: "PARTAGER" }
    },
    ar: {
      sliders: {
        "brawl-stars": { trophies: "الكؤوس", maxed: "مقاتلون بمستوى قوة 11" },
        "clash-of-clans": { th: "مستوى مركز المدينة" },
        "clash-royale": { kt: "مستوى برج الملك", maxed: "بطاقات بأقصى مستوى" },
        "free-fire": { rank: "الرتبة", bundles: "حزم/رفقاء نادرة" },
        "genshin-impact": { fivestars: "شخصيات 5 نجوم", c6: "شخصيات بمستوى C6" },
        "mobile-legends": { skins: "إجمالي الأزياء", rank: "الرتبة" },
        "fortnite": { skins: "إجمالي الأزياء", ogItems: "عناصر OG نادرة" },
        "minecraft": { type: "نوع الحساب" },
        "roblox": { age: "عمر الحساب", robux: "رصيد Robux", limiteds: "عناصر Limited عادية (ليست النادرة المسماة)" }
      },
      select: { "clash-of-clans": { label: "نوع الترقية", options: [["full", "Full Max"], ["standard", "قياسي"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "سنة" : "سنوات"); },
      minecraftTypes: ["حساب عادي", "MVP+/Hypixel، عباءة نادرة", "حامل عباءة Minecon", "اسم من حرفين (أرقام وحروف)"],
      checkboxHeading: "عناصر نادرة مسماة (اختياري):",
      confidence: { low: "منخفضة", medium: "متوسطة", high: "عالية" },
      confidencePrefix: "مستوى الثقة: ",
      copiedFallback: "تم النسخ!",
      gamepad: { up: "الحقل السابق", down: "الحقل التالي", left: "إنقاص", right: "زيادة", a: "إعادة تعيين الكل", b: "مشاركة النتيجة", resetCaption: "إعادة", shareCaption: "مشاركة" }
    },
    de: {
      sliders: {
        "brawl-stars": { trophies: "Trophäen (Pokale)", maxed: "Brawler mit Power Level 11" },
        "clash-of-clans": { th: "Rathaus-Level (Town Hall)" },
        "clash-royale": { kt: "King-Tower-Level", maxed: "Karten auf Höchststufe" },
        "free-fire": { rank: "Rang", bundles: "Seltene Bundles/Begleiter" },
        "genshin-impact": { fivestars: "5★-Charaktere", c6: "Charaktere mit C6" },
        "mobile-legends": { skins: "Skins insgesamt", rank: "Rang" },
        "fortnite": { skins: "Skins insgesamt", ogItems: "Seltene OG-Items" },
        "minecraft": { type: "Kontotyp" },
        "roblox": { age: "Kontoalter", robux: "Robux-Guthaben", limiteds: "Gewöhnliche Limited-Items (nicht die namhaften seltenen)" }
      },
      select: { "clash-of-clans": { label: "Ausbaustatus", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "Jahr" : "Jahre"); },
      minecraftTypes: ["Normaler Account", "MVP+/Hypixel, seltener Cape", "Minecon-Cape-Besitzer", "2-Zeichen-Name (alphanumerisch)"],
      checkboxHeading: "Namhafte seltene Items (optional):",
      confidence: { low: "Niedrig", medium: "Mittel", high: "Hoch" },
      confidencePrefix: "Sicherheit: ",
      copiedFallback: "Kopiert!",
      gamepad: { up: "Vorheriges Feld", down: "Nächstes Feld", left: "Verringern", right: "Erhöhen", a: "Alles zurücksetzen", b: "Ergebnis teilen", resetCaption: "RESET", shareCaption: "TEILEN" }
    },
    tr: {
      sliders: {
        "brawl-stars": { trophies: "Kupa", maxed: "Power Level 11 karakterler" },
        "clash-of-clans": { th: "Köy Merkezi (Town Hall) seviyesi" },
        "clash-royale": { kt: "Kral Kulesi seviyesi", maxed: "Maksimum seviye kartlar" },
        "free-fire": { rank: "Rütbe", bundles: "Nadir bundle/evcil hayvanlar" },
        "genshin-impact": { fivestars: "5★ karakter", c6: "C6 karakterler" },
        "mobile-legends": { skins: "Toplam skin", rank: "Rütbe" },
        "fortnite": { skins: "Toplam skin", ogItems: "Nadir OG eşyalar" },
        "minecraft": { type: "Hesap türü" },
        "roblox": { age: "Hesap yaşı", robux: "Robux bakiyesi", limiteds: "Sıradan Limited eşyalar (isimli nadirler değil)" }
      },
      select: { "clash-of-clans": { label: "Yükseltme türü", options: [["full", "Full Max"], ["standard", "Standart"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " yıl"; },
      minecraftTypes: ["Normal hesap", "MVP+/Hypixel, nadir pelerin", "Minecon pelerini sahibi", "2 karakterli isim (alfanümerik)"],
      checkboxHeading: "İsimli nadir eşyalar (opsiyonel):",
      confidence: { low: "Düşük", medium: "Orta", high: "Yüksek" },
      confidencePrefix: "Güven: ",
      copiedFallback: "Kopyalandı!",
      gamepad: { up: "Önceki alan", down: "Sonraki alan", left: "Azalt", right: "Artır", a: "Tümünü sıfırla", b: "Sonucu paylaş", resetCaption: "SIFIRLA", shareCaption: "PAYLAŞ" }
    },
    vi: {
      sliders: {
        "brawl-stars": { trophies: "Cúp", maxed: "Tướng Power Level 11" },
        "clash-of-clans": { th: "Cấp Trụ sở chính (Town Hall)" },
        "clash-royale": { kt: "Cấp King Tower", maxed: "Thẻ cấp tối đa" },
        "free-fire": { rank: "Rank", bundles: "Bundle/thú cưng hiếm" },
        "genshin-impact": { fivestars: "Nhân vật 5★", c6: "Nhân vật C6" },
        "mobile-legends": { skins: "Tổng số skin", rank: "Rank" },
        "fortnite": { skins: "Tổng số skin", ogItems: "Vật phẩm OG hiếm" },
        "minecraft": { type: "Loại acc" },
        "roblox": { age: "Tuổi acc", robux: "Số dư Robux", limiteds: "Vật phẩm Limited thường (không phải hàng hiếm có tên)" }
      },
      select: { "clash-of-clans": { label: "Loại nâng cấp", options: [["full", "Full Max"], ["standard", "Tiêu chuẩn"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " năm"; },
      minecraftTypes: ["Acc thường", "MVP+/Hypixel, cape hiếm", "Sở hữu cape Minecon", "Tên 2 ký tự (chữ+số)"],
      checkboxHeading: "Vật phẩm hiếm có tên (tùy chọn):",
      confidence: { low: "Thấp", medium: "Trung bình", high: "Cao" },
      confidencePrefix: "Độ tin cậy: ",
      copiedFallback: "Đã sao chép!",
      gamepad: { up: "Trường trước", down: "Trường tiếp theo", left: "Giảm", right: "Tăng", a: "Đặt lại tất cả", b: "Chia sẻ kết quả", resetCaption: "RESET", shareCaption: "CHIA SẺ" }
    },
    hi: {
      sliders: {
        "brawl-stars": { trophies: "ट्रॉफ़ी", maxed: "Power Level 11 ब्रॉलर" },
        "clash-of-clans": { th: "Town Hall लेवल" },
        "clash-royale": { kt: "King Tower लेवल", maxed: "मैक्स-लेवल कार्ड्स" },
        "free-fire": { rank: "रैंक", bundles: "रेयर बंडल/पेट्स" },
        "genshin-impact": { fivestars: "5★ करैक्टर", c6: "C6 वाले करैक्टर" },
        "mobile-legends": { skins: "कुल स्किन्स", rank: "रैंक" },
        "fortnite": { skins: "कुल स्किन्स", ogItems: "रेयर OG आइटम्स" },
        "minecraft": { type: "अकाउंट टाइप" },
        "roblox": { age: "अकाउंट की उम्र", robux: "Robux बैलेंस", limiteds: "आम Limited आइटम्स (नामी रेयर नहीं)" }
      },
      select: { "clash-of-clans": { label: "अपग्रेड टाइप", options: [["full", "Full Max"], ["standard", "स्टैंडर्ड"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " साल"; },
      minecraftTypes: ["रेगुलर अकाउंट", "MVP+/Hypixel, रेयर केप", "Minecon केप होल्डर", "2-कैरेक्टर नाम (अल्फ़ान्यूमेरिक)"],
      checkboxHeading: "नामी रेयर आइटम्स (ऑप्शनल):",
      confidence: { low: "कम", medium: "मीडियम", high: "हाई" },
      confidencePrefix: "कॉन्फिडेंस: ",
      copiedFallback: "कॉपी हो गया!",
      gamepad: { up: "पिछला फ़ील्ड", down: "अगला फ़ील्ड", left: "घटाएं", right: "बढ़ाएं", a: "सब रीसेट करें", b: "रिज़ल्ट शेयर करें", resetCaption: "रीसेट", shareCaption: "शेयर" }
    },
    it: {
      sliders: {
        "brawl-stars": { trophies: "Trofei (coppe)", maxed: "Brawler Power Level 11" },
        "clash-of-clans": { th: "Livello Municipio (Town Hall)" },
        "clash-royale": { kt: "Livello King Tower", maxed: "Carte al livello massimo" },
        "free-fire": { rank: "Rango", bundles: "Bundle/pet rari" },
        "genshin-impact": { fivestars: "Personaggi 5★", c6: "Personaggi con C6" },
        "mobile-legends": { skins: "Skin totali", rank: "Rango" },
        "fortnite": { skins: "Skin totali", ogItems: "Oggetti OG rari" },
        "minecraft": { type: "Tipo di account" },
        "roblox": { age: "Anzianità dell'account", robux: "Saldo Robux", limiteds: "Oggetti Limited comuni (non i rari con nome)" }
      },
      select: { "clash-of-clans": { label: "Tipo di potenziamento", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "anno" : "anni"); },
      minecraftTypes: ["Account normale", "MVP+/Hypixel, cape raro", "Possessore cape Minecon", "Nome 2 caratteri (alfanumerico)"],
      checkboxHeading: "Oggetti rari con nome (opzionale):",
      confidence: { low: "Bassa", medium: "Media", high: "Alta" },
      confidencePrefix: "Affidabilità: ",
      copiedFallback: "Copiato!",
      gamepad: { up: "Campo precedente", down: "Campo successivo", left: "Diminuisci", right: "Aumenta", a: "Reimposta tutto", b: "Condividi risultato", resetCaption: "RESET", shareCaption: "CONDIVIDI" }
    },
    ja: {
      sliders: {
        "brawl-stars": { trophies: "トロフィー", maxed: "Power Level 11のブロウラー" },
        "clash-of-clans": { th: "タウンホールレベル" },
        "clash-royale": { kt: "キングタワーレベル", maxed: "最大レベルのカード" },
        "free-fire": { rank: "ランク", bundles: "レアなバンドル/ペット" },
        "genshin-impact": { fivestars: "★5キャラクター", c6: "凸6(C6)キャラクター" },
        "mobile-legends": { skins: "スキン総数", rank: "ランク" },
        "fortnite": { skins: "スキン総数", ogItems: "レアなOGアイテム" },
        "minecraft": { type: "アカウントタイプ" },
        "roblox": { age: "アカウントの年数", robux: "Robux残高", limiteds: "一般的なLimitedアイテム(名前付きレアではない)" }
      },
      select: { "clash-of-clans": { label: "アップグレードタイプ", options: [["full", "フルマックス"], ["standard", "標準"], ["rushed", "ラッシュ"]] } },
      ageUnit: function (v) { return v + "年"; },
      minecraftTypes: ["通常アカウント", "MVP+/Hypixel、レアなケープ", "Mineconケープ所持者", "2文字の名前(英数字)"],
      checkboxHeading: "名前付きレアアイテム(任意):",
      confidence: { low: "低い", medium: "中程度", high: "高い" },
      confidencePrefix: "信頼度: ",
      copiedFallback: "コピーしました!",
      gamepad: { up: "前のフィールド", down: "次のフィールド", left: "減らす", right: "増やす", a: "すべてリセット", b: "結果をシェア", resetCaption: "リセット", shareCaption: "シェア" }
    },
    ko: {
      sliders: {
        "brawl-stars": { trophies: "트로피", maxed: "Power Level 11 브롤러" },
        "clash-of-clans": { th: "Town Hall 레벨" },
        "clash-royale": { kt: "King Tower 레벨", maxed: "최대 레벨 카드" },
        "free-fire": { rank: "랭크", bundles: "희귀 번들/펫" },
        "genshin-impact": { fivestars: "5성 캐릭터", c6: "C6 캐릭터" },
        "mobile-legends": { skins: "전체 스킨 수", rank: "랭크" },
        "fortnite": { skins: "전체 스킨 수", ogItems: "희귀 OG 아이템" },
        "minecraft": { type: "계정 유형" },
        "roblox": { age: "계정 연식", robux: "Robux 잔액", limiteds: "일반 Limited 아이템(네임드 희귀 아님)" }
      },
      select: { "clash-of-clans": { label: "업그레이드 유형", options: [["full", "Full Max"], ["standard", "표준"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + "년"; },
      minecraftTypes: ["일반 계정", "MVP+/Hypixel, 희귀 케이프", "Minecon 케이프 보유자", "2글자 이름(영숫자)"],
      checkboxHeading: "네임드 희귀 아이템(선택):",
      confidence: { low: "낮음", medium: "보통", high: "높음" },
      confidencePrefix: "신뢰도: ",
      copiedFallback: "복사됨!",
      gamepad: { up: "이전 필드", down: "다음 필드", left: "감소", right: "증가", a: "전체 초기화", b: "결과 공유", resetCaption: "초기화", shareCaption: "공유" }
    },
    zh: {
      sliders: {
        "brawl-stars": { trophies: "奖杯", maxed: "Power Level 11 角色" },
        "clash-of-clans": { th: "大本营等级" },
        "clash-royale": { kt: "国王塔等级", maxed: "满级卡牌" },
        "free-fire": { rank: "段位", bundles: "稀有套装/宠物" },
        "genshin-impact": { fivestars: "5星角色", c6: "满命(C6)角色" },
        "mobile-legends": { skins: "皮肤总数", rank: "段位" },
        "fortnite": { skins: "皮肤总数", ogItems: "稀有OG道具" },
        "minecraft": { type: "账号类型" },
        "roblox": { age: "账号年龄", robux: "Robux余额", limiteds: "普通Limited道具(非知名稀有款)" }
      },
      select: { "clash-of-clans": { label: "升级类型", options: [["full", "满级"], ["standard", "标准"], ["rushed", "抢建(Rushed)"]] } },
      ageUnit: function (v) { return v + "年"; },
      minecraftTypes: ["普通账号", "MVP+/Hypixel，稀有披风", "Minecon披风持有者", "2字符ID(字母数字)"],
      checkboxHeading: "知名稀有道具(可选)：",
      confidence: { low: "低", medium: "中", high: "高" },
      confidencePrefix: "可信度：",
      copiedFallback: "已复制！",
      gamepad: { up: "上一项", down: "下一项", left: "减少", right: "增加", a: "全部重置", b: "分享结果", resetCaption: "重置", shareCaption: "分享" }
    },
    pl: {
      sliders: {
        "brawl-stars": { trophies: "Puchary", maxed: "Brawlerzy Power Level 11" },
        "clash-of-clans": { th: "Poziom Ratusza (Town Hall)" },
        "clash-royale": { kt: "Poziom King Tower", maxed: "Karty na max. poziomie" },
        "free-fire": { rank: "Ranga", bundles: "Rzadkie bundle/zwierzaki" },
        "genshin-impact": { fivestars: "Postacie 5★", c6: "Postacie z C6" },
        "mobile-legends": { skins: "Łączna liczba skórek", rank: "Ranga" },
        "fortnite": { skins: "Łączna liczba skórek", ogItems: "Rzadkie przedmioty OG" },
        "minecraft": { type: "Typ konta" },
        "roblox": { age: "Wiek konta", robux: "Saldo Robux", limiteds: "Zwykłe przedmioty Limited (nie rzadkie z nazwą)" }
      },
      select: { "clash-of-clans": { label: "Typ rozbudowy", options: [["full", "Full Max"], ["standard", "Standard"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " " + (v === 1 ? "rok" : (v >= 2 && v <= 4 ? "lata" : "lat")); },
      minecraftTypes: ["Zwykłe konto", "MVP+/Hypixel, rzadki płaszcz", "Posiadacz płaszcza Minecon", "2-znakowa nazwa (alfanumeryczna)"],
      checkboxHeading: "Rzadkie przedmioty z nazwą (opcjonalnie):",
      confidence: { low: "Niska", medium: "Średnia", high: "Wysoka" },
      confidencePrefix: "Pewność: ",
      copiedFallback: "Skopiowano!",
      gamepad: { up: "Poprzednie pole", down: "Następne pole", left: "Zmniejsz", right: "Zwiększ", a: "Resetuj wszystko", b: "Udostępnij wynik", resetCaption: "RESET", shareCaption: "UDOSTĘPNIJ" }
    },
    th: {
      sliders: {
        "brawl-stars": { trophies: "ถ้วยรางวัล", maxed: "ตัวละคร Power Level 11" },
        "clash-of-clans": { th: "เลเวล Town Hall" },
        "clash-royale": { kt: "เลเวล King Tower", maxed: "การ์ดเลเวลสูงสุด" },
        "free-fire": { rank: "แรงค์", bundles: "บันเดิล/สัตว์เลี้ยงหายาก" },
        "genshin-impact": { fivestars: "ตัวละคร 5★", c6: "ตัวละคร C6" },
        "mobile-legends": { skins: "สกินทั้งหมด", rank: "แรงค์" },
        "fortnite": { skins: "สกินทั้งหมด", ogItems: "ไอเทม OG หายาก" },
        "minecraft": { type: "ประเภทบัญชี" },
        "roblox": { age: "อายุบัญชี", robux: "ยอดคงเหลือ Robux", limiteds: "ไอเทม Limited ทั่วไป (ไม่ใช่ของหายากที่มีชื่อ)" }
      },
      select: { "clash-of-clans": { label: "ประเภทการอัปเกรด", options: [["full", "Full Max"], ["standard", "มาตรฐาน"], ["rushed", "Rushed"]] } },
      ageUnit: function (v) { return v + " ปี"; },
      minecraftTypes: ["บัญชีทั่วไป", "MVP+/Hypixel, เคปหายาก", "เจ้าของเคป Minecon", "ชื่อ 2 ตัวอักษร (ตัวอักษร+ตัวเลข)"],
      checkboxHeading: "ไอเทมหายากที่มีชื่อ (ไม่บังคับ):",
      confidence: { low: "ต่ำ", medium: "ปานกลาง", high: "สูง" },
      confidencePrefix: "ความมั่นใจ: ",
      copiedFallback: "คัดลอกแล้ว!",
      gamepad: { up: "ฟิลด์ก่อนหน้า", down: "ฟิลด์ถัดไป", left: "ลด", right: "เพิ่ม", a: "รีเซ็ตทั้งหมด", b: "แชร์ผลลัพธ์", resetCaption: "รีเซ็ต", shareCaption: "แชร์" }
    }
  };
  var T = STR[LANG];

  // Roblox named-item price adds (checked 2026-09-26, see roblox.html).
  // Headless: Eldorado.gg "Headless accounts" category (337 listings) —
  // middle half of the displayed listings asked $400-700, most of them
  // Headless + Korblox, so Headless alone = that range minus Korblox's.
  // Korblox (17,000 R$) and Violet Valkyrie (50,000 R$): official Robux
  // price x the $0.0065-0.0075/Robux Eldorado.gg resale asking price —
  // no large Korblox-only or Valkyrie-only listing sample exists to cite.
  // Cross-check: Headless+Korblox+Valkyrie = $725-1,075 vs $750-1,500 listed.
  var ROBLOX_RARE_ITEMS = [
    { key: "korblox", name: "Korblox Deathspeaker", lo: 110, hi: 130 },
    { key: "headless", name: "Headless Horseman", lo: 290, hi: 570 },
    { key: "violet", name: "Violet Valkyrie", lo: 325, hi: 375 }
  ];

  // Robux balance: Roblox's official DevEx cash-out rate ($0.0038/R$) as
  // the floor, the cheapest Eldorado.gg Robux resale ask ($0.0065/R$) as
  // the ceiling (checked 2026-09-26).
  var ROBUX_USD = [0.0038, 0.0065];

  // Fortnite named-skin ranges: middle half of Eldorado.gg's displayed
  // listings for each skin's category, 2026-09-26 (24 listings each for
  // Black Knight / IKONIK / Travis Scott). The four "OG 2017" entries are
  // the original-owner styles only — Renegade Raider and Aerial Assault
  // Trooper were re-sold in the Item Shop from 19 Dec 2024 (fortnite.com),
  // and re-release copies list at ordinary-skin prices ($12-99). OG ranges
  // come from the smaller set of OG-labelled listings (4-10 per skin).
  // Several checked skins add up; the result never drops below the
  // slider estimate. Cross-check: Black Knight + IKONIK = $405-670 vs
  // $550/$699 listed; OG Renegade + Black Knight = $1,170-2,320 vs $1,599.
  var FORTNITE_RARE_ITEMS = [
    { key: "blackknight", name: "Black Knight", lo: 170, hi: 320 },
    { key: "ikonik", name: "IKONIK", lo: 235, hi: 350 },
    { key: "travis", name: "Travis Scott", lo: 180, hi: 390 },
    { key: "renegade", name: "Renegade Raider — OG 2017", lo: 1000, hi: 2000, og: true },
    { key: "aerial", name: "Aerial Assault Trooper — OG 2017", lo: 1100, hi: 1700, og: true },
    { key: "skull", name: "Skull Trooper — OG purple 2017", lo: 800, hi: 1700, og: true },
    { key: "ghoul", name: "Ghoul Trooper — OG pink 2017", lo: 1150, hi: 2500, og: true }
  ];

  function sumChecked(items, v) {
    var lo = 0, hi = 0, og = false, any = false;
    items.forEach(function (item) {
      if (v[item.key]) { lo += item.lo; hi += item.hi; any = true; if (item.og) og = true; }
    });
    return { lo: lo, hi: hi, any: any, og: og };
  }

  // Rank ladders are the games' own official English rank names — kept
  // identical across languages on purpose, the same way "Town Hall" or
  // "C6" isn't translated either.
  var FREE_FIRE_RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Heroic", "Grandmaster"];
  var ML_RANKS = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythical Glory"];

  // Tier vocabulary matches the bot's PDF certificate (core/valuation.py:
  // STARTER/CASUAL/PRO/COLLECTOR — kept in English in every language, same
  // as the bot does), so the site and the bot speak the same language. The
  // boundaries themselves are this widget's own score quartiles, not a
  // byte-for-byte copy of the bot's per-game conditions — those depend on
  // named items (specific skins, badges) this slider-only widget
  // deliberately doesn't collect. Two games (Clash of Clans by TH, Genshin
  // by C6 count) happen to line up with the bot's real thresholds because
  // their score IS that same slider; the rest are an honest approximation,
  // not a claimed 1:1 match.
  function tierFromScore(score) {
    if (score >= 0.75) return { label: "COLLECTOR", cls: "tier-collector" };
    if (score >= 0.5) return { label: "PRO", cls: "tier-pro" };
    if (score >= 0.25) return { label: "CASUAL", cls: "tier-casual" };
    return { label: "STARTER", cls: "tier-starter" };
  }

  function confidenceLabel(ratio) {
    if (ratio >= 0.8) return T.confidence.high;
    if (ratio >= 0.4) return T.confidence.medium;
    return T.confidence.low;
  }

  // --- per-game config -----------------------------------------------
  // Every bracket/table value is taken directly from that game's own
  // "Real Market Prices" table on the same page.
  var GAMES = {
    "brawl-stars": {
      name: "Brawl Stars",
      sliders: [
        { key: "trophies", min: 5000, max: 45000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US"); } },
        { key: "maxed", min: 0, max: 85, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) { return 0.5 * norm(v.trophies, 5000, 45000) + 0.5 * norm(v.maxed, 0, 85); },
      compute: function (v, score) { return interpBrackets(score, [[3, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "clash-of-clans": {
      name: "Clash of Clans",
      sliders: [
        { key: "th", min: 13, max: 18, step: 1, fmt: function (v) { return "TH" + v; } }
      ],
      choices: [{ key: "type", label: T.select["clash-of-clans"].label, options: T.select["clash-of-clans"].options }],
      score: function (v) { return norm(v.th, 13, 18); },
      compute: function (v) {
        var table = {
          18: { full: [100, 260], standard: [45, 120], rushed: [20, 35] },
          17: { full: [55, 185], standard: [30, 50], rushed: [30, 55] },
          16: { full: [40, 100], standard: [20, 35], rushed: [15, 25] },
          15: { full: [30, 65], standard: [15, 25], rushed: [15, 20] },
          14: { full: [25, 50], standard: [15, 25], rushed: [10, 20] },
          13: { full: [15, 40], standard: [10, 15], rushed: [8, 12] }
        };
        return table[v.th][v.type];
      }
    },
    "clash-royale": {
      name: "Clash Royale",
      sliders: [
        { key: "kt", min: 9, max: 15, step: 1, fmt: function (v) { return "KT" + v; } },
        { key: "maxed", min: 0, max: 40, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) { return 0.5 * norm(v.kt, 9, 15) + 0.5 * norm(v.maxed, 0, 40); },
      compute: function (v, score) { return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 600]]); }
    },
    "free-fire": {
      name: "Free Fire",
      sliders: [
        { key: "bundles", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      choices: [{ key: "rank", label: T.sliders["free-fire"].rank, options: FREE_FIRE_RANKS.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return 0.5 * norm(v.rank, 1, 7) + 0.5 * norm(v.bundles, 0, 10); },
      compute: function (v, score) { return interpBrackets(score, [[0.73, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "genshin-impact": {
      name: "Genshin Impact",
      sliders: [
        { key: "fivestars", min: 0, max: 20, step: 1, fmt: function (v) { return v; } },
        { key: "c6", min: 0, max: 20, step: 1, fmt: function (v) { return v; } }
      ],
      score: function (v) {
        if (v.fivestars < 3) return 0;
        return 0.5 * norm(v.fivestars, 3, 20) + 0.5 * norm(v.c6, 0, 20);
      },
      compute: function (v, score) {
        if (v.fivestars < 3) return [5, 60];
        return interpBrackets(score, [[30, 200], [300, 1000], [1000, 4200], [8400, 8995]]);
      }
    },
    "mobile-legends": {
      name: "Mobile Legends",
      sliders: [
        { key: "skins", min: 0, max: 400, step: 10, fmt: function (v) { return v; } }
      ],
      choices: [{ key: "rank", label: T.sliders["mobile-legends"].rank, options: ML_RANKS.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return 0.5 * norm(v.skins, 0, 400) + 0.5 * norm(v.rank, 1, 7); },
      compute: function (v, score) { return interpBrackets(score, [[0.5, 15], [15, 50], [50, 150], [150, 300]]); }
    },
    "fortnite": {
      name: "Fortnite",
      sliders: [
        { key: "skins", min: 0, max: 250, step: 5, fmt: function (v) { return v; } },
        { key: "ogItems", min: 0, max: 5, step: 1, fmt: function (v) { return v; } }
      ],
      checkboxes: FORTNITE_RARE_ITEMS,
      score: function (v) {
        var s = 0.5 * norm(v.skins, 0, 250) + 0.5 * norm(v.ogItems, 0, 5);
        var items = sumChecked(FORTNITE_RARE_ITEMS, v);
        return items.og ? Math.max(s, 0.75) : items.any ? Math.max(s, 0.5) : s;
      },
      compute: function (v, score) {
        var base = interpBrackets(0.5 * norm(v.skins, 0, 250) + 0.5 * norm(v.ogItems, 0, 5), [[10.9, 15], [15, 50], [50, 150], [150, 1100]]);
        var items = sumChecked(FORTNITE_RARE_ITEMS, v);
        return [Math.max(base[0], items.lo), Math.max(base[1], items.hi)];
      }
    },
    "minecraft": {
      name: "Minecraft",
      choices: [{ key: "type", label: T.sliders["minecraft"].type, options: T.minecraftTypes.map(function (name, i) { return [String(i + 1), name]; }) }],
      score: function (v) { return norm(v.type, 1, 4); },
      compute: function (v) {
        var table = { 1: [0.5, 25], 2: [25, 632], 3: [2000, 5000], 4: [25000, 50000] };
        return table[v.type];
      }
    },
    "roblox": {
      name: "Roblox",
      sliders: [
        { key: "age", min: 0, max: 15, step: 1, fmt: function (v) { return T.ageUnit(v); } },
        { key: "robux", min: 0, max: 50000, step: 1000, fmt: function (v) { return v.toLocaleString("en-US") + " R$"; } },
        { key: "limiteds", min: 0, max: 10, step: 1, fmt: function (v) { return v; } }
      ],
      checkboxes: ROBLOX_RARE_ITEMS,
      score: function (v) {
        var s = (norm(v.age, 0, 15) + norm(v.robux, 0, 50000) + norm(v.limiteds, 0, 10)) / 3;
        if (v.headless || v.violet) return Math.max(s, 0.75);
        return v.korblox ? Math.max(s, 0.5) : s;
      },
      compute: function (v) {
        // Account itself (age + common limiteds) on the page's $0.50-60
        // marketplace range; Robux balance and named items priced separately.
        var base = interpBrackets((norm(v.age, 0, 15) + norm(v.limiteds, 0, 10)) / 2, [[0.5, 5], [5, 25], [25, 60]]);
        var items = sumChecked(ROBLOX_RARE_ITEMS, v);
        return [base[0] + v.robux * ROBUX_USD[0] + items.lo, base[1] + v.robux * ROBUX_USD[1] + items.hi];
      }
    }
  };

  var GAME_ORDER = ["roblox", "brawl-stars", "clash-of-clans", "clash-royale", "free-fire",
    "genshin-impact", "mobile-legends", "fortnite", "minecraft"];

  var rafIds = new WeakMap();

  function animateNumber(el, fromVal, toVal) {
    if (prefersReducedMotion || fromVal === toVal) { el.textContent = formatMoney(toVal); return; }
    var pending = rafIds.get(el);
    if (pending) cancelAnimationFrame(pending);
    var start = null;
    var duration = 220;
    function tick(now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / duration, 1);
      el.textContent = formatMoney(fromVal + (toVal - fromVal) * p);
      if (p < 1) {
        rafIds.set(el, requestAnimationFrame(tick));
      } else {
        rafIds.delete(el);
      }
    }
    rafIds.set(el, requestAnimationFrame(tick));
  }

  function ensureResultShell(root) {
    var resultBox = root.querySelector(".vc-result");
    var valueEl = resultBox.querySelector(".vc-result-value");
    valueEl.setAttribute("aria-live", "polite");
    if (!valueEl.querySelector(".vc-lo")) {
      valueEl.innerHTML = '<span class="vc-lo">—</span> – <span class="vc-hi">—</span>';
    }
    if (!resultBox.querySelector(".vc-scale")) {
      var scale = document.createElement("div");
      scale.className = "vc-scale";
      scale.setAttribute("aria-hidden", "true");
      scale.innerHTML = '<div class="vc-scale-fill"></div>';
      valueEl.insertAdjacentElement("afterend", scale);
      var meta = document.createElement("div");
      meta.className = "vc-meta";
      meta.innerHTML = '<span class="vc-tier"></span><span class="vc-confidence"></span>';
      scale.insertAdjacentElement("afterend", meta);
    }
    return {
      lo: valueEl.querySelector(".vc-lo"),
      hi: valueEl.querySelector(".vc-hi"),
      scaleFill: resultBox.querySelector(".vc-scale-fill"),
      tier: resultBox.querySelector(".vc-tier"),
      confidence: resultBox.querySelector(".vc-confidence")
    };
  }

  function mount(root, gameId) {
    var cfg = GAMES[gameId];
    if (!cfg) return;
    root.setAttribute("data-game", gameId);
    root.setAttribute("data-title", cfg.name);

    var slidersWrap = root.querySelector(".vc-sliders");
    slidersWrap.innerHTML = "";
    var els = ensureResultShell(root);
    var resultNote = root.querySelector(".vc-result-note");

    var state = {};
    var totalInputs = (cfg.sliders || []).length + (cfg.choices ? cfg.choices.length : 0) + (cfg.checkboxes ? cfg.checkboxes.length : 0);
    var touched = new Set();
    var prevLo = null, prevHi = null;
    var controls = []; // gamepad D-pad navigation targets, built in the same order fields are rendered

    function recompute() {
      var score = cfg.score(state);
      var range = cfg.compute(state, score);
      var lo = range[0], hi = range[1];
      animateNumber(els.lo, prevLo === null ? lo : prevLo, lo);
      animateNumber(els.hi, prevHi === null ? hi : prevHi, hi);
      prevLo = lo; prevHi = hi;

      els.scaleFill.style.width = Math.round(score * 100) + "%";
      var tier = tierFromScore(score);
      els.tier.textContent = tier.label;
      els.tier.className = "vc-tier " + tier.cls;
      els.confidence.textContent = T.confidencePrefix + confidenceLabel(totalInputs ? touched.size / totalInputs : 1);
    }

    (cfg.sliders || []).forEach(function (s) {
      var label = T.sliders[gameId][s.key];
      var field = document.createElement("div");
      field.className = "vc-field";
      var labelId = root.id + "-" + s.key + "-label";
      field.innerHTML =
        '<label for="' + root.id + "-" + s.key + '" id="' + labelId + '">' +
        label + ': <strong class="vc-field-val"></strong></label>' +
        '<input type="range" id="' + root.id + "-" + s.key + '" min="' + s.min +
        '" max="' + s.max + '" step="' + s.step + '" value="' + s.min +
        '" aria-labelledby="' + labelId + '">';
      slidersWrap.appendChild(field);

      var input = field.querySelector("input");
      var valEl = field.querySelector(".vc-field-val");
      state[s.key] = s.min;
      valEl.textContent = s.fmt(s.min);
      input.addEventListener("input", function () {
        touched.add(s.key);
        var v = Number(input.value);
        state[s.key] = v;
        valEl.textContent = s.fmt(v);
        recompute();
      });
      controls.push({ type: "range", field: field, el: input, step: s.step, min: s.min, max: s.max });
    });

    (cfg.choices || []).forEach(function (choice) {
      var field = document.createElement("div");
      field.className = "vc-field";
      var groupName = root.id + "-" + choice.key;
      var html = '<span class="vc-choice-heading">' + choice.label + '</span><div class="vc-choice-tiles" role="radiogroup" aria-label="' + choice.label + '">';
      choice.options.forEach(function (opt, i) {
        var optId = groupName + "-" + i;
        html += '<input type="radio" name="' + groupName + '" id="' + optId + '" value="' + opt[0] + '"' + (i === 0 ? " checked" : "") + '>' +
          '<label for="' + optId + '" class="vc-choice-tile">' + opt[1] + "</label>";
      });
      html += "</div>";
      field.innerHTML = html;
      slidersWrap.appendChild(field);
      state[choice.key] = choice.options[0][0];
      var radios = Array.prototype.slice.call(field.querySelectorAll('input[type="radio"]'));
      radios.forEach(function (radio) {
        radio.addEventListener("change", function () {
          touched.add(choice.key);
          state[choice.key] = radio.value;
          recompute();
        });
      });
      controls.push({ type: "radio", field: field, radios: radios });
    });

    if (cfg.checkboxes && cfg.checkboxes.length) {
      var cbField = document.createElement("div");
      cbField.className = "vc-field vc-checkbox-group";
      var cbHtml = '<span class="vc-checkbox-heading">' + T.checkboxHeading + '</span>';
      cfg.checkboxes.forEach(function (item, i) {
        var cbId = root.id + "-cb-" + item.key;
        cbHtml += '<label class="vc-checkbox" for="' + cbId + '">' +
          '<input type="checkbox" id="' + cbId + '">' +
          '<span>' + item.name + ' (+' + formatMoney(item.lo) + '–' + formatMoney(item.hi) + ')</span>' +
          '</label>';
      });
      cbField.innerHTML = cbHtml;
      slidersWrap.appendChild(cbField);
      cfg.checkboxes.forEach(function (item) {
        var cbId = root.id + "-cb-" + item.key;
        var input = cbField.querySelector("#" + cbId);
        var cbLabel = input.closest(".vc-checkbox");
        state[item.key] = false;
        input.addEventListener("change", function () {
          touched.add(item.key);
          state[item.key] = input.checked;
          recompute();
        });
        controls.push({ type: "checkbox", field: cbLabel, el: input });
      });
    }

    // Gamepad D-pad: a decorative remote-control layer over the real
    // inputs above. It only ever calls .value=/.checked= then dispatches
    // the same input/change events the inputs already listen for, so the
    // scoring/pricing logic never has a second code path to go out of sync.
    if (controls.length && T.gamepad) {
      var gp = document.createElement("div");
      gp.className = "vc-gamepad";
      gp.innerHTML =
        '<div class="vc-dpad" role="group" aria-label="' + T.gamepad.up + ' / ' + T.gamepad.down + ' / ' + T.gamepad.left + ' / ' + T.gamepad.right + '">' +
        '<button type="button" class="vc-dpad-btn vc-dpad-up" aria-label="' + T.gamepad.up + '">▲</button>' +
        '<button type="button" class="vc-dpad-btn vc-dpad-left" aria-label="' + T.gamepad.left + '">◀</button>' +
        '<span class="vc-dpad-center" aria-hidden="true"></span>' +
        '<button type="button" class="vc-dpad-btn vc-dpad-right" aria-label="' + T.gamepad.right + '">▶</button>' +
        '<button type="button" class="vc-dpad-btn vc-dpad-down" aria-label="' + T.gamepad.down + '">▼</button>' +
        '</div>' +
        '<div class="vc-abtns">' +
        '<div class="vc-btn-wrap"><button type="button" class="vc-btn-round vc-btn-b" aria-label="' + T.gamepad.b + '">B</button><span class="vc-btn-label">' + T.gamepad.shareCaption + '</span></div>' +
        '<div class="vc-btn-wrap"><button type="button" class="vc-btn-round vc-btn-a" aria-label="' + T.gamepad.a + '">A</button><span class="vc-btn-label">' + T.gamepad.resetCaption + '</span></div>' +
        '</div>';
      slidersWrap.insertBefore(gp, slidersWrap.firstChild);

      var activeIndex = 0;
      function setActive(i) {
        var n = controls.length;
        activeIndex = ((i % n) + n) % n;
        controls.forEach(function (c) { c.field.classList.remove("vc-field-active"); });
        var target = controls[activeIndex];
        target.field.classList.add("vc-field-active");
        // Deferred to the next frame so the browser applies the class change
        // through its normal layout pass instead of us forcing a synchronous
        // recalc by reading scroll position in the same tick (Lighthouse
        // "forced reflow" — same visual result, just not forced early).
        requestAnimationFrame(function () {
          target.field.scrollIntoView({ block: "nearest", behavior: prefersReducedMotion ? "auto" : "smooth" });
        });
      }
      function fire(el, type) { el.dispatchEvent(new Event(type, { bubbles: true })); }
      function nudge(dir) {
        var c = controls[activeIndex];
        if (c.type === "range") {
          var step = c.step * dir;
          var v = Math.min(c.max, Math.max(c.min, Number(c.el.value) + step));
          c.el.value = v;
          fire(c.el, "input");
        } else if (c.type === "radio") {
          var idx = c.radios.findIndex(function (r) { return r.checked; });
          var next = ((idx + dir) % c.radios.length + c.radios.length) % c.radios.length;
          c.radios[next].checked = true;
          fire(c.radios[next], "change");
        } else if (c.type === "checkbox") {
          c.el.checked = !c.el.checked;
          fire(c.el, "change");
        }
      }
      gp.querySelector(".vc-dpad-up").addEventListener("click", function () { setActive(activeIndex - 1); });
      gp.querySelector(".vc-dpad-down").addEventListener("click", function () { setActive(activeIndex + 1); });
      gp.querySelector(".vc-dpad-left").addEventListener("click", function () { nudge(-1); });
      gp.querySelector(".vc-dpad-right").addEventListener("click", function () { nudge(1); });
      gp.querySelector(".vc-btn-a").addEventListener("click", function () {
        // Reset every field to its default (works on every game, unlike a
        // checkbox toggle which is a no-op on the games with none).
        controls.forEach(function (c) {
          if (c.type === "range") { c.el.value = c.min; fire(c.el, "input"); }
          else if (c.type === "radio") { c.radios[0].checked = true; fire(c.radios[0], "change"); }
          else if (c.type === "checkbox") { if (c.el.checked) { c.el.checked = false; fire(c.el, "change"); } }
        });
        touched.clear();
        recompute();
        setActive(0);
      });
      gp.querySelector(".vc-btn-b").addEventListener("click", function () {
        var shareBtnNow = root.querySelector(".vc-share-btn");
        if (shareBtnNow) shareBtnNow.click();
      });
      setActive(0);
    }

    recompute();

    var shareBtn = root.querySelector(".vc-share-btn");
    if (shareBtn && !shareBtn.dataset.bound) {
      shareBtn.dataset.bound = "1";
      shareBtn.addEventListener("click", function () {
        var text = els.lo.textContent + " – " + els.hi.textContent;
        var title = root.getAttribute("data-title") || "GameAccountValue";
        var shareText = title + ": " + text + " — https://t.me/GameAccountValue_Bot";
        if (navigator.share) {
          navigator.share({ text: shareText }).catch(function () {});
        } else if (navigator.clipboard) {
          navigator.clipboard.writeText(shareText).then(function () {
            var original = shareBtn.textContent;
            shareBtn.textContent = resultNote.getAttribute("data-copied") || T.copiedFallback;
            setTimeout(function () { shareBtn.textContent = original; }, 1800);
          }).catch(function () {});
        }
      });
    }
  }

  function initSwitcher(root) {
    var switcher = root.querySelector(".vc-switcher");
    if (!switcher) return;
    switcher.innerHTML = "";
    GAME_ORDER.forEach(function (id) {
      var opt = document.createElement("option");
      opt.value = id;
      opt.textContent = GAMES[id].name;
      switcher.appendChild(opt);
    });
    switcher.value = GAME_ORDER[0];
    mount(root, GAME_ORDER[0]);
    switcher.addEventListener("change", function () {
      mount(root, switcher.value);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".value-calc[data-switcher]").forEach(initSwitcher);
    document.querySelectorAll(".value-calc[data-game]:not([data-switcher])").forEach(function (root) {
      mount(root, root.getAttribute("data-game"));
    });
  });

  window.GAVCalc = { GAMES: GAMES, GAME_ORDER: GAME_ORDER, mount: mount };
})();

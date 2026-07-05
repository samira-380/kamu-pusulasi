// Bu dosya H1 (tracer-bullet) için sabit mock verilerdir.
// Şema Ü1'in orkestratör JSON sözleşmesiyle birebir uyumlu olacak şekilde tasarlandı.
// H2'de bu dosyanın yerini gerçek API çağrıları alacak (bkz. README).

export const belgeSenaryolari = [
  {
    id: "dilekce-normal",
    baslik: "Dilekçe — standart akış",
    aciklama: "Guardrail'i sorunsuz geçen, yönlendirmesi net bir örnek.",
    doc_id: "a1f9-normal",
    trace: [
      { step: "ajan_a_algila", label: "Ajan-a · Algı", status: "ok", confidence: 0.94, detail: "Tür: dilekçe · 5 alan çıkarıldı" },
      { step: "ajan_b_mevzuat", label: "Ajan-b · Mevzuat-RAG", status: "ok", confidence: 0.88, detail: "2 madde atıflı bulundu" },
      { step: "ajan_c_taslak", label: "Ajan-c · Taslak-NLG", status: "ok", confidence: 0.91, detail: "Bilgilendirme taslağı üretildi" },
      { step: "ajan_d_yonlendir", label: "Ajan-d · Yönlendirme", status: "ok", confidence: 0.83, detail: "Birim önerisi hazır" },
      { step: "guardrail", label: "Guardrail", status: "ok", detail: "Atıf var, güven eşik üstü — geçti" },
    ],
    state: {
      evrak_turu: "Dilekçe",
      zorunlu_alanlar: {
        konu: "Su faturasına itiraz",
        tarih: "02.07.2026",
        gonderen: "M. Kaya",
        kurum: "İlçe Belediyesi",
      },
      eksik_alanlar: [],
    },
    ozet: "Vatandaş, Haziran ayı su faturasındaki tutara itiraz ediyor ve sayaç tekrar okuması talep ediyor.",
    mevzuat: [
      { madde: "Su ve Kanalizasyon Hizmetleri Yönetmeliği m.14", versiyon: "Commons v2026.3", ozet: "İtiraz halinde sayaç yeniden okuma prosedürünü tanımlar." },
      { madde: "5393 sayılı Belediye Kanunu m.15/f", versiyon: "Commons v2026.1", ozet: "Belediyenin tarife ve itiraz süreçlerindeki yetkisini belirler." },
    ],
    guardrail: { durum: "gecti", mesaj: null },
    taslak: {
      tur: "Bilgilendirme yazısı",
      icerik: "Sayın M. Kaya,\n\n02.07.2026 tarihli dilekçeniz incelenmiştir. Su ve Kanalizasyon Hizmetleri Yönetmeliği m.14 uyarınca sayacınızın yeniden okunması için ekipler 5 iş günü içinde adresinize yönlendirilecektir.\n\nBilgilerinize sunulur.",
      guven: 0.91,
    },
    yonlendirme: {
      birim: "Su ve Kanalizasyon İşleri Müdürlüğü",
      gerekce: "Konu doğrudan sayaç okuma ve tarife itirazı kapsamında; ilgili yönetmelik bu birimi yetkili kılıyor.",
      guven: 0.83,
      alternatifler: [],
    },
  },
  {
    id: "tebligat-blok",
    baslik: "Tebligat — guardrail BLOK",
    aciklama: "Atıfsız bağlayıcı ifade nedeniyle çıktının bloklandığı örnek.",
    doc_id: "b2e7-blok",
    trace: [
      { step: "ajan_a_algila", label: "Ajan-a · Algı", status: "ok", confidence: 0.89, detail: "Tür: tebligat · 4 alan çıkarıldı" },
      { step: "ajan_b_mevzuat", label: "Ajan-b · Mevzuat-RAG", status: "ok", confidence: 0.52, detail: "Zayıf eşleşme, tek aday madde" },
      { step: "ajan_c_taslak", label: "Ajan-c · Taslak-NLG", status: "checkpoint", confidence: 0.45, detail: "Bağlayıcı ifade madde no'suz üretildi" },
      { step: "guardrail", label: "Guardrail", status: "blocked", detail: "Atıfsız bağlayıcı cümle — çıktı geçmedi" },
    ],
    state: {
      evrak_turu: "Tebligat",
      zorunlu_alanlar: {
        konu: "İmar para cezası tebligatı",
        tarih: "28.06.2026",
        gonderen: "A. Yıldırım",
        kurum: "İl Özel İdaresi",
      },
      eksik_alanlar: ["ceza_tutari"],
    },
    ozet: "Ruhsatsız yapı nedeniyle düzenlenen para cezası tebligatına itiraz; ceza tutarı belgede eksik.",
    mevzuat: [
      { madde: "3194 sayılı İmar Kanunu m.32 (düşük güven)", versiyon: "Commons v2026.1", ozet: "Aday madde bulundu ancak madde numarası teyit edilemedi." },
    ],
    guardrail: {
      durum: "bloklandi",
      mesaj: "Taslakta bağlayıcı bir hüküm (\"ceza kesinleşmiştir\") madde no + Commons versiyon-ID olmadan üretildi. Kural: atıfsız bağlayıcı ifade asla memura sunulmaz. Bu evrak insan incelemesine düşer.",
    },
    taslak: null,
    yonlendirme: {
      birim: "İmar ve Şehircilik Müdürlüğü",
      gerekce: "Guardrail bloğu nedeniyle otomatik gerekçe üretilmedi — insan kararına bırakıldı.",
      guven: 0.0,
      alternatifler: ["Hukuk İşleri Müdürlüğü"],
      insan_karari: true,
    },
  },
  {
    id: "basvuru-cekin",
    baslik: "Başvuru — düşük güven, çekindi",
    aciklama: "Guardrail'in bloklamadığı ama düşük güvende insan kararına bıraktığı örnek.",
    doc_id: "c3a1-cekin",
    trace: [
      { step: "ajan_a_algila", label: "Ajan-a · Algı", status: "ok", confidence: 0.77, detail: "Tür: başvuru · 3 alan çıkarıldı" },
      { step: "ajan_b_mevzuat", label: "Ajan-b · Mevzuat-RAG", status: "ok", confidence: 0.81, detail: "1 madde atıflı bulundu" },
      { step: "ajan_c_taslak", label: "Ajan-c · Taslak-NLG", status: "ok", confidence: 0.79, detail: "Eksik-bilgi talebi taslağı üretildi" },
      { step: "ajan_d_yonlendir", label: "Ajan-d · Yönlendirme", status: "checkpoint", confidence: 0.58, detail: "Güven eşik altı" },
      { step: "guardrail", label: "Guardrail", status: "checkpoint", detail: "Düşük güven — insan kararına bırakıldı" },
    ],
    state: {
      evrak_turu: "Başvuru",
      zorunlu_alanlar: {
        konu: "Engelli park kartı başvurusu",
        tarih: "01.07.2026",
        gonderen: "S. Demir",
        kurum: "belirtilmemiş",
      },
      eksik_alanlar: ["kurum"],
    },
    ozet: "Vatandaş engelli park kartı için başvuruyor; başvuruda hangi kuruma hitaben yazıldığı belirtilmemiş.",
    mevzuat: [
      { madde: "2918 sayılı Karayolları Trafik Kanunu Ek m.1", versiyon: "Commons v2026.2", ozet: "Engelli park kartı başvuru ve yetki sürecini tanımlar." },
    ],
    guardrail: {
      durum: "cekindi",
      mesaj: "Yönlendirme güveni eşik altı (0.58 < 0.75). İki birim de olası olduğundan sistem otomatik seçim yapmıyor; memur kararı gerekiyor.",
    },
    taslak: {
      tur: "Eksik bilgi talebi",
      icerik: "Sayın S. Demir,\n\n01.07.2026 tarihli başvurunuzda hangi kuruma hitaben başvurduğunuz belirtilmemiştir. Başvurunuzun değerlendirilebilmesi için ilgili kurum bilgisini 10 iş günü içinde tarafımıza iletmenizi rica ederiz.",
      guven: 0.79,
    },
    yonlendirme: {
      birim: null,
      gerekce: "Alan eksikliği nedeniyle iki birim arasında ayrım yapılamadı.",
      guven: 0.58,
      alternatifler: ["Ulaşım Hizmetleri Müdürlüğü", "Sosyal Hizmetler Müdürlüğü"],
      insan_karari: true,
    },
  },
];

# Kamu Pusulası — web arayüzü (Ü4)

Bu klasör, Kamu Pusulası projesinin memur-yüzlü web arayüzünün **H1 (tracer-bullet)** iskeletidir.
Gerçek model/servis yok — her şey `src/mockData.js` içindeki sabit, sözleşmeye uygun JSON ile çalışır.

## Çalıştırma

```bash
npm install
npm run dev
```

`npm run build` ile üretim derlemesi alınır, `dist/` klasörü GitHub Pages / Vercel / Netlify gibi
statik bir sunucuya doğrudan verilebilir.

## Akış

1. **Evrak** — 3 mock senaryodan biri seçilir (normal akış, guardrail bloğu, düşük güven çekinmesi).
2. **Analiz** — Ajan-a/Ajan-b çıktısı: sınıflandırma, zorunlu alanlar (eksikse işaretli), özet, atıflı mevzuat.
3. **Onay** — Ajan-c/Ajan-d çıktısı: taslak (filigranlı), güven skoru, yönlendirme gerekçesi;
   memur onaylar / düzenler / reddeder. Sağdaki **ajan izi** paneli her adımı canlı gösterir.

## Sözleşme (JSON contract)

`src/mockData.js` içindeki her belge nesnesi, Ü1'in orkestratör sözleşmesiyle birebir hizalı:

```
doc_id, trace[], state{evrak_turu, zorunlu_alanlar, eksik_alanlar},
guardrail{durum, mesaj}, taslak{tur, icerik, guven}, yonlendirme{birim, gerekce, guven, alternatifler}
```

`trace[].status` üç değer alır: `ok`, `checkpoint` (düşük güven, çekindi), `blocked` (guardrail bloğu).
Arayüz bu üç durumu farklı renk/rozet ile gösterir — jüriye "ajan olduğu iddia değil kanıt" ilkesini
görsel olarak taşımak için tasarlandı.

## H2'de değişecekler (gerçek entegrasyon)

- `mockData.js` yerine gerçek API çağrıları gelecek (`fetch('/api/analiz', ...)` gibi) — Ü1'in
  orkestratör endpoint'ine bağlanılacak, JSON şekli aynı kalacak.
- `UploadScreen` gerçek dosya yükleme (PDF/görsel) alacak, Ü2/Ü3'ün OCR + model servislerine gidecek.
- `ApprovalPanel`'daki onay/red aksiyonları gerçek bir "onay kaydı" endpoint'ine yazacak.
- Eval harness (Ü4) ve tarafsızlık raporu bu arayüzün dışında, ayrı bir script/rapor olarak kalacak.

## Tasarım notları

- Renk/tipografi: resmi kurum hissi veren sıcak kağıt zemin + lacivert + Source Serif 4 başlıklar,
  IBM Plex Sans gövde, IBM Plex Mono ajan izi/etiketler için.
- "Ajan izi" paneli kasıtlı olarak bir "mühür defteri" metaforuyla tasarlandı (yeşil/turuncu/kırmızı
  mühürler) — kamu evrak temasıyla doğrudan örtüşsün diye.

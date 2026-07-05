# KAMU PUSULASI

**Gelen evrakı okuyup sınıflandıran + mevzuatı atıflı öneren + özetleyen (G1),
sonra resmî taslak yazıp doğru birime yönlendiren (G2); ama hiçbir çıktıyı
otomatik göndermeyip her taslağı memur onayına sunan açık kaynak bir ajan.**

## Nedir?

KAMU PUSULASI, bir kamu kurumuna gelen resmî evrakı (dilekçe, üst yazı,
tebligat, başvuru; çoğu taranmış/PDF/metin) alıp memurun işini hızlandıran
çok-ajanlı bir yapay zekâ sistemidir.

- **Görev 1 (Anlama):** Evrakı okur, türünü sınıflandırır, önemli bilgiyi
  çıkarır, eksik bilgiyi tespit eder, ilgili mevzuatı atıflı önerir, kısa
  özet çıkarır.
- **Görev 2 (Taslaklama):** Resmî üslupta üst yazı / cevap yazısı /
  bilgilendirme taslaklar, doğru birime gerekçe + güven skoruyla yönlendirir,
  gerekirse eksik bilgi talebi hazırlar.

> ⚠️ Sistem hiçbir çıktıyı otomatik göndermez. Üretilen her taslak
> `TASLAK - memur onayı gerekir` filigranıyla işaretlenir ve nihai onay
> her zaman insana (memura) bırakılır.

## Mimari (özet)

Dört ajan, ortak bir "belge zarfı" (state) üzerinden JSON sözleşmeleriyle
birbirine bağlanır:

```
oku_siniflandir → mevzuat_eslestir → taslakla → yonlendir
```

Orkestrasyon döngüsü: **hedef → plan → ajan-çağrı → durum**

Ayrıntılı mimari dokümantasyonu için bkz. [`docs/mimari.md`](docs/mimari.md)
(Sprint 4'te tamamlanacak).

## Klasör yapısı

```
kamu-pusulasi/
├── orchestrator/       # döngü, state şeması, guardrail, JSON sözleşmeleri
│   └── contracts/      # ajanlar arası JSON şemaları
├── agents/             # 4 ajan (şimdilik mock)
├── examples/           # örnek evrak/test verisi
├── tests/              # uçtan uca testler
└── docs/               # mimari dokümantasyonu
```

## Durum

Bu proje aktif geliştirme aşamasındadır (Sprint 1: mock uçtan uca iskelet).

## Guardrail ilkeleri

- Atıfsız (madde no + kaynak-ID'siz) bağlayıcı ifadeler bloklanır.
- Düşük güven skorunda sistem çekimser davranır ("insan kararına bırakıldı").
- Hiçbir çıktı otomatik gönderilmez; her taslak memur onayına sunulur.

## Lisans

Apache License 2.0 — bkz. [LICENSE](LICENSE)

## Etkinlik

🏷️ `BilisimVadisi2026`

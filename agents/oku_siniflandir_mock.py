"""
Ajan 1: oku_siniflandir (MOCK)
==============================
Gercek surumde: OCR/metin cikarma + tur siniflandirma + alan cikarma
(NER benzeri) yapacak. Su an sabit ama semaya uygun bir cikti donduren
bir mock.

Girdi: state["girdi"]["ham_metin"]
Cikti: orchestrator/contracts/oku_siniflandir.schema.json ile uyumlu dict
"""

from __future__ import annotations
from typing import Any


def calistir(state: dict[str, Any]) -> dict[str, Any]:
    ham_metin = state["girdi"]["ham_metin"]

    # --- MOCK MANTIK ---
    # Gercek ajan burada OCR/LLM ile metni analiz edecek.
    # Simdilik anahtar kelimeye gore kaba bir "sahte siniflandirma" yapiyoruz,
    # boylece farkli ornek evraklarla test edilebilir.
    if "dilekce" in ham_metin.lower() or "arz ederim" in ham_metin.lower():
        tur = "dilekce"
    elif "üst yazı" in ham_metin.lower() or "ust yazi" in ham_metin.lower():
        tur = "ust_yazi"
    elif "tebliğ" in ham_metin.lower() or "teblig" in ham_metin.lower():
        tur = "tebligat"
    else:
        tur = "basvuru"

    eksik_alanlar = []
    if "T.C. Kimlik" not in ham_metin and "TC Kimlik" not in ham_metin:
        eksik_alanlar.append("tc_kimlik_no")
    if "İmza" not in ham_metin and "imza" not in ham_metin.lower():
        eksik_alanlar.append("imza")

    return {
        "siniflandirma": {
            "tur": tur,
            "guven": 0.82,
        },
        "cikarilan_alanlar": {
            "gonderen": "Ahmet Yılmaz",       # mock sabit deger
            "tarih": "2026-07-01",             # mock sabit deger
            "konu": "Su faturasına itiraz",    # mock sabit deger
            "eksik_alanlar": eksik_alanlar,
        },
        "ozet": (
            "Vatandaş, Temmuz ayı su faturasındaki yüksek tutara itiraz "
            "ederek sayaç kontrolü talep etmektedir."
        ),
    }

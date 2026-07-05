"""
Ajan 3: taslakla (MOCK)
=======================
Gercek surumde: resmi uslupta LLM ile taslak metin uretecek.

Girdi: state["siniflandirma"], state["cikarilan_alanlar"],
       state["mevzuat_onerileri"], state["cikarilan_alanlar"]["eksik_alanlar"]
Cikti: orchestrator/contracts/taslakla.schema.json ile uyumlu dict

KURAL: "filigran" alani HER ZAMAN sabit deger olmak zorunda.
Bu deger runtime'da (loop.py) da ayrica dogrulanir/zorlanir; sadece
ajanin "iyi niyetine" birakilmaz.
"""

from __future__ import annotations
from typing import Any

FILIGRAN = "TASLAK - memur onayi gerekir"


def calistir(state: dict[str, Any]) -> dict[str, Any]:
    eksik_alanlar = state.get("cikarilan_alanlar", {}).get("eksik_alanlar", [])

    if eksik_alanlar:
        # Eksik zorunlu alan varsa, cevap taslagi yerine "eksik bilgi talebi" uretilir.
        alan_listesi = ", ".join(eksik_alanlar)
        metin = (
            f"Sayın {state['cikarilan_alanlar'].get('gonderen', 'İlgili')},\n\n"
            f"{state['cikarilan_alanlar'].get('tarih', '')} tarihli başvurunuz "
            f"incelenmiş olup, değerlendirme yapılabilmesi için aşağıdaki "
            f"bilgi/belgelerin tarafımıza iletilmesi gerekmektedir:\n"
            f"- {alan_listesi}\n\n"
            f"Bilgilerinize sunulur."
        )
        tip = "eksik_bilgi_talebi"
    else:
        konu = state["cikarilan_alanlar"].get("konu", "")
        mevzuat = state.get("mevzuat_onerileri", [])
        atif = (
            f"{mevzuat[0]['kanun']} {mevzuat[0]['madde']}"
            if mevzuat else "ilgili mevzuat"
        )
        metin = (
            f"Sayın {state['cikarilan_alanlar'].get('gonderen', 'İlgili')},\n\n"
            f"\"{konu}\" konulu başvurunuz incelenmiştir. {atif} kapsamında "
            f"gerekli değerlendirme yapılmak üzere ilgili birime "
            f"yönlendirilmiştir. Sonuç tarafınıza ayrıca bildirilecektir.\n\n"
            f"Bilgilerinize sunulur."
        )
        tip = "cevap"

    return {
        "taslak": {
            "tip": tip,
            "metin": metin,
            "filigran": FILIGRAN,
        }
    }

"""
Ajan 4: yonlendir (MOCK)
========================
Gercek surumde: kurum ic-organizasyon semasina gore, evrak konusuna
en uygun birimi guven skoruyla onerecek.

Girdi: state["siniflandirma"]["tur"], state["cikarilan_alanlar"]["konu"]
Cikti: orchestrator/contracts/yonlendir.schema.json ile uyumlu dict
"""

from __future__ import annotations
from typing import Any


def calistir(state: dict[str, Any]) -> dict[str, Any]:
    konu = state.get("cikarilan_alanlar", {}).get("konu", "") or ""

    # --- MOCK MANTIK ---
    if "fatura" in konu.lower() or "su" in konu.lower():
        birim = "Su ve Kanalizasyon İşleri Müdürlüğü"
        gerekce = (
            "Başvuru konusu su faturasına itiraz olduğundan, sayaç/tahakkuk "
            "kontrolü yapma yetkisi bu birime aittir."
        )
        guven = 0.79
    else:
        birim = "Yazı İşleri Müdürlüğü"
        gerekce = (
            "Başvuru genel evrak niteliğinde olup, ilk değerlendirme ve "
            "ilgili birime dağıtım bu müdürlük tarafından yapılmaktadır."
        )
        guven = 0.5

    return {
        "yonlendirme": {
            "birim": birim,
            "gerekce": gerekce,
            "guven": guven,
        }
    }

"""
Ajan 2: mevzuat_eslestir (MOCK)
===============================
Gercek surumde: RAG ile mevzuat veritabanindan atifli oneri getirecek
(Ü3'un yerel LLM baseline'i buraya baglanacak).

Girdi: state["siniflandirma"]["tur"], state["cikarilan_alanlar"]["konu"]
Cikti: orchestrator/contracts/mevzuat_eslestir.schema.json ile uyumlu dict

NOT (guardrail sozlesmesi): "kaynak_id" alani ASLA bos birakilmamali.
Bos/eksik kaynak_id, orkestrasyon seviyesinde atifsiz-baglayici ifade
olarak isaretlenip Sprint 3'te BLOK'lanacak.
"""

from __future__ import annotations
from typing import Any


def calistir(state: dict[str, Any]) -> dict[str, Any]:
    konu = state.get("cikarilan_alanlar", {}).get("konu", "") or ""

    # --- MOCK MANTIK ---
    # Gercek ajan burada RAG ile mevzuat veritabanini arayacak.
    if "fatura" in konu.lower() or "su" in konu.lower():
        onerileri = [
            {
                "kanun": "5393 Sayılı Belediye Kanunu",
                "madde": "Madde 15",
                "kaynak_id": "mevzuat-db://5393/md15/v2024",
                "guven": 0.74,
            },
            {
                "kanun": "Tüketicinin Korunması Hakkında Kanun",
                "madde": "Madde 68",
                "kaynak_id": "mevzuat-db://6502/md68/v2023",
                "guven": 0.61,
            },
        ]
    else:
        onerileri = [
            {
                "kanun": "3071 Sayılı Dilekçe Hakkının Kullanılmasına Dair Kanun",
                "madde": "Madde 4",
                "kaynak_id": "mevzuat-db://3071/md4/v2022",
                "guven": 0.55,
            }
        ]

    return {"mevzuat_onerileri": onerileri}

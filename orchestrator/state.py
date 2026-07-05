"""
State / Bellek Semasi
======================
Sisteme giren her evrak icin, pipeline boyunca zenginlesen tek bir
"belge zarfi" (state) nesnesi olusturulur. 4 ajan da bu ortak nesne
uzerinden okur/yazar. Boylece ajanlar birbirinden bagimsiz gelistirilebilir;
tek sabit nokta bu semadir (sozlesme).

Mock ajanlar da, gercek modeller de, ayni state semasina uymak zorundadir.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import uuid


def init_state(girdi: dict[str, Any]) -> dict[str, Any]:
    """
    Yeni bir evrak sisteme girdiginde bos ama semaya uygun bir state
    nesnesi olusturur.

    girdi: {
        "kaynak_tipi": "pdf" | "taranmis" | "metin",
        "ham_metin": str,
        "dosya_url": str | None
    }
    """
    return {
        "belge_id": str(uuid.uuid4()),
        "girdi": {
            "kaynak_tipi": girdi.get("kaynak_tipi", "metin"),
            "ham_metin": girdi.get("ham_metin", ""),
            "dosya_url": girdi.get("dosya_url"),
        },
        "siniflandirma": {
            "tur": None,          # dilekce | ust_yazi | tebligat | basvuru
            "guven": 0.0,
        },
        "cikarilan_alanlar": {
            "gonderen": None,
            "tarih": None,
            "konu": None,
            "eksik_alanlar": [],
        },
        "mevzuat_onerileri": [],
        "ozet": None,
        "taslak": {
            "tip": None,           # ust_yazi | cevap | bilgilendirme | eksik_bilgi_talebi
            "metin": None,
            "filigran": "TASLAK - memur onayi gerekir",
        },
        "yonlendirme": {
            "birim": None,
            "gerekce": None,
            "guven": 0.0,
        },
        "guardrail": {
            "blok": False,
            "sebep": None,
            "cekingen_mi": False,
        },
        "log": [],
    }


def log_adim(state: dict[str, Any], ajan: str, not_: str = "") -> None:
    """Her ajan cagrisindan sonra state'e iz birakir (yerinde/in-place)."""
    state["log"].append({
        "adim": len(state["log"]) + 1,
        "ajan": ajan,
        "zaman": datetime.now(timezone.utc).isoformat(),
        "not": not_,
    })


def merge_into_state(state: dict[str, Any], ajan_adi: str, sonuc: dict[str, Any]) -> dict[str, Any]:
    """
    Bir ajanin ciktisini (sonuc) state'in ilgili bolumune yerlestirir.
    Her ajan sadece kendi sorumlu oldugu anahtar(lar)i gunceller;
    digerlerine dokunmaz.
    """
    hedef_anahtar = {
        "oku_siniflandir": ["siniflandirma", "cikarilan_alanlar", "ozet"],
        "mevzuat_eslestir": ["mevzuat_onerileri"],
        "taslakla": ["taslak"],
        "yonlendir": ["yonlendirme"],
    }.get(ajan_adi, [])

    for anahtar in hedef_anahtar:
        if anahtar in sonuc:
            state[anahtar] = sonuc[anahtar]

    # guardrail bilgisi herhangi bir ajandan gelebilir (opsiyonel)
    if "guardrail" in sonuc:
        state["guardrail"].update(sonuc["guardrail"])

    log_adim(state, ajan_adi)
    return state

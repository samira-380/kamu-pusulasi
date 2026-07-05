"""
Orkestrasyon Dongusu: hedef -> plan -> ajan-cagri -> durum
===========================================================
Bu modul, 4 ajani sirayla (ve ileride kosullu olarak) cagirip,
ortak state nesnesini adim adim zenginlestiren ana dongudur.

Akis (Sprint 1 - sabit sira, kosulsuz):
    oku_siniflandir -> mevzuat_eslestir -> taslakla -> yonlendir

Sprint 2'de eklenecek: eksik zorunlu alan varsa plan'da dallanma.
Sprint 3'te eklenecek: guardrail.blok=True ise dongu erken durur.
"""

from __future__ import annotations
from typing import Any, Callable
import importlib
import json
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

from orchestrator.state import init_state, merge_into_state

CONTRACTS_DIR = Path(__file__).parent / "contracts"

# --- PLAN: hedef + hangi ajan + sozlesme dosyasi ---
# Sprint 1: sabit dogrusal plan. Sprint 2'de bu yapi kosullu hale gelecek
# (orn. "eksik_alanlar doluysa taslakla yerine eksik_bilgi_talebi_uret").
PLAN: list[dict[str, str]] = [
    {
        "hedef": "Evrağı oku, türünü sınıflandır, alanları çıkar, özetle",
        "agent_modul": "agents.oku_siniflandir_mock",
        "agent_adi": "oku_siniflandir",
        "sozlesme": "oku_siniflandir.schema.json",
    },
    {
        "hedef": "İlgili mevzuatı atıflı şekilde öner",
        "agent_modul": "agents.mevzuat_eslestir_mock",
        "agent_adi": "mevzuat_eslestir",
        "sozlesme": "mevzuat_eslestir.schema.json",
    },
    {
        "hedef": "Resmi taslak (cevap / eksik bilgi talebi) hazırla",
        "agent_modul": "agents.taslakla_mock",
        "agent_adi": "taslakla",
        "sozlesme": "taslakla.schema.json",
    },
    {
        "hedef": "Doğru birime gerekçeli ve güven skorlu yönlendirme yap",
        "agent_modul": "agents.yonlendir_mock",
        "agent_adi": "yonlendir",
        "sozlesme": "yonlendir.schema.json",
    },
]


def _sozlesme_yukle(dosya_adi: str) -> dict[str, Any]:
    with open(CONTRACTS_DIR / dosya_adi, encoding="utf-8") as f:
        return json.load(f)


def _sozlesmeyi_dogrula(ajan_adi: str, cikti: dict[str, Any], schema: dict[str, Any]) -> None:
    """Ajan ciktisi sozlesmeye (JSON Schema) uymuyorsa aciktan patlar.
    Sessizce gecmek, ileride gercek modele geciste sessiz veri bozulmasina
    yol acar - bu yuzden burada kasitli olarak katiyiz."""
    if jsonschema is None:
        return  # kutuphane yoksa dogrulama atlanir (bkz. README kurulum notu)
    jsonschema.validate(instance=cikti, schema=schema)


def _agent_cagir(agent_modul: str) -> Callable[[dict[str, Any]], dict[str, Any]]:
    modul = importlib.import_module(agent_modul)
    return modul.calistir


def process_document(girdi: dict[str, Any], plan: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """
    Tek bir evrağı, plan'daki ajanlardan sırayla geçirip nihai state'i döner.

    girdi: {"kaynak_tipi": ..., "ham_metin": ..., "dosya_url": ...}
    """
    state = init_state(girdi)
    plan = plan if plan is not None else PLAN

    for adim in plan:
        # --- ajan-cagri ---
        calistir = _agent_cagir(adim["agent_modul"])
        sonuc = calistir(state)

        # --- sozlesme dogrulama ---
        schema = _sozlesme_yukle(adim["sozlesme"])
        _sozlesmeyi_dogrula(adim["agent_adi"], sonuc, schema)

        # --- durum guncelle ---
        state = merge_into_state(state, adim["agent_adi"], sonuc)

        # Sprint 3'te: if state["guardrail"]["blok"]: break

    return state


if __name__ == "__main__":
    # Hizli manuel deneme (asil test tests/test_e2e_mock.py icinde)
    ornek_girdi = {
        "kaynak_tipi": "metin",
        "ham_metin": (
            "DİLEKÇE\n\nSayın Belediye Başkanlığı,\n\n"
            "Temmuz ayı su faturamın önceki aylara göre anormal derecede "
            "yüksek geldiğini fark ettim. Sayacımın kontrol edilmesini "
            "ve gerekli düzeltmenin yapılmasını arz ederim.\n\n"
            "Ahmet Yılmaz"
        ),
        "dosya_url": None,
    }
    sonuc_state = process_document(ornek_girdi)
    print(json.dumps(sonuc_state, ensure_ascii=False, indent=2))

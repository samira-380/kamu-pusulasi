"""
Uctan Uca Mock Test
====================
Amac: Tek bir evrak turunde (dilekce), 4 mock ajanin sirayla calisip
JSON'un pipeline boyunca dogru sekilde aktigini dogrulamak.

Calistirma:
    python -m tests.test_e2e_mock
veya (pytest kuruluysa):
    pytest tests/test_e2e_mock.py -v
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

# Proje kok dizinini import path'ine ekle (agents/orchestrator paket olarak gorulsun)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from orchestrator.loop import process_document

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def _girdi_yukle(dosya_adi: str) -> dict:
    with open(EXAMPLES_DIR / dosya_adi, encoding="utf-8") as f:
        return json.load(f)


def test_eksik_alanli_dilekce_akisi():
    """Eksik zorunlu alan (TC kimlik/imza) olan dilekce -> eksik_bilgi_talebi taslagi uretmeli."""
    girdi = _girdi_yukle("ornek_dilekce.json")
    state = process_document(girdi)

    assert state["siniflandirma"]["tur"] == "dilekce"
    assert state["siniflandirma"]["guven"] > 0
    assert len(state["cikarilan_alanlar"]["eksik_alanlar"]) > 0
    assert state["ozet"]

    assert len(state["mevzuat_onerileri"]) > 0
    for oneri in state["mevzuat_onerileri"]:
        assert oneri["kaynak_id"], "guardrail sozlesmesi: kaynak_id bos olamaz"

    assert state["taslak"]["tip"] == "eksik_bilgi_talebi"
    assert state["taslak"]["filigran"] == "TASLAK - memur onayi gerekir"

    assert state["yonlendirme"]["birim"]
    assert state["yonlendirme"]["guven"] > 0

    assert len(state["log"]) == 4  # 4 ajan sirayla calisti
    print("[OK] eksik alanli dilekce akisi -> eksik_bilgi_talebi uretildi")


def test_tam_dilekce_akisi():
    """Zorunlu alanlari tam olan dilekce -> normal cevap taslagi uretmeli."""
    girdi = _girdi_yukle("ornek_dilekce_tam.json")
    state = process_document(girdi)

    assert state["siniflandirma"]["tur"] == "dilekce"
    assert state["cikarilan_alanlar"]["eksik_alanlar"] == []
    assert state["taslak"]["tip"] == "cevap"
    assert state["taslak"]["filigran"] == "TASLAK - memur onayi gerekir"
    assert state["yonlendirme"]["birim"] == "Su ve Kanalizasyon İşleri Müdürlüğü"
    print("[OK] tam dilekce akisi -> cevap taslagi uretildi")


def _tumunu_calistir():
    test_eksik_alanli_dilekce_akisi()
    test_tam_dilekce_akisi()
    print("\nTUM TESTLER GECTI - JSON pipeline boyunca dogru akiyor.")


if __name__ == "__main__":
    _tumunu_calistir()

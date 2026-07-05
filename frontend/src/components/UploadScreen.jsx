import { belgeSenaryolari } from "../mockData.js";

export default function UploadScreen({ onSelect }) {
  return (
    <div>
      <h2 className="section-title">Evrak seç</h2>
      <p className="section-sub">
        H1 aşamasında gerçek yükleme yok — sözleşmeye uygun 3 mock senaryo üzerinden
        akışı gösteriyoruz. H2'de burası gerçek OCR/algı servisine (Ü2/Ü3) bağlanacak.
      </p>
      <div className="doc-picker">
        {belgeSenaryolari.map((b) => (
          <button key={b.id} className="doc-card" onClick={() => onSelect(b)}>
            <div className="doc-title">{b.baslik}</div>
            <div className="doc-desc">{b.aciklama}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

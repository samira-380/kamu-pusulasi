export default function ResultView({ belge, onDevam }) {
  const { state, ozet, mevzuat } = belge;
  const alanlar = Object.entries(state.zorunlu_alanlar);

  return (
    <div>
      <h2 className="section-title">{state.evrak_turu} — analiz sonucu</h2>
      <p className="section-sub">Ajan-a ve Ajan-b'nin çıktısı. Hiçbir şey henüz kaydedilmedi.</p>

      <div className="field-grid">
        {alanlar.map(([key, val]) => {
          const eksik = state.eksik_alanlar.includes(key) || val === "belirtilmemiş";
          return (
            <div key={key} className={`field ${eksik ? "missing" : ""}`}>
              <div className="field-label">{key.replace("_", " ")}</div>
              <div className="field-value">{eksik ? "eksik — memur tamamlamalı" : val}</div>
            </div>
          );
        })}
      </div>

      <h2 className="section-title" style={{ fontSize: 15, marginBottom: 10 }}>
        Kısa özet
      </h2>
      <div className="summary-box">{ozet}</div>

      <h2 className="section-title" style={{ fontSize: 15, marginBottom: 10 }}>
        İlgili mevzuat (atıflı)
      </h2>
      <ul className="citation-list">
        {mevzuat.map((m, i) => (
          <li key={i}>
            <div className="citation-ref">{m.madde} · {m.versiyon}</div>
            {m.ozet}
          </li>
        ))}
      </ul>

      <button className="btn" onClick={onDevam}>
        Taslak ve yönlendirmeye geç →
      </button>
    </div>
  );
}

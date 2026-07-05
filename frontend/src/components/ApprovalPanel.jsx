import { useState } from "react";

function guvenSinifi(g) {
  if (g >= 0.75) return "high";
  if (g >= 0.5) return "mid";
  return "low";
}

export default function ApprovalPanel({ belge, onReset }) {
  const { guardrail, taslak, yonlendirme } = belge;
  const [draftText, setDraftText] = useState(taslak?.icerik ?? "");
  const [secilenBirim, setSecilenBirim] = useState(yonlendirme.birim);
  const [karar, setKarar] = useState(null); // 'onaylandi' | 'reddedildi' | null

  const bloklandi = guardrail.durum === "bloklandi";

  return (
    <div>
      <h2 className="section-title">Memur onayı</h2>
      <p className="section-sub">
        Hiçbir çıktı otomatik gönderilmez veya dosyalanmaz. Son karar her zaman sizindir.
      </p>

      {guardrail.durum !== "gecti" && (
        <div className={`guardrail-banner ${bloklandi ? "blocked" : "checkpoint"}`}>
          <strong>{bloklandi ? "Guardrail bloğu:" : "Guardrail çekindi:"}</strong>
          <span>{guardrail.mesaj}</span>
        </div>
      )}

      {taslak && (
        <div className="draft-frame">
          <div className="watermark">TASLAK · ONAY GEREKİR</div>
          <div className="field-label" style={{ marginBottom: 8 }}>
            {taslak.tur}
          </div>
          <textarea
            value={draftText}
            onChange={(e) => setDraftText(e.target.value)}
            disabled={karar === "onaylandi"}
          />
        </div>
      )}

      {taslak && (
        <div className="confidence-row">
          <span>Taslak güveni</span>
          <div className="confidence-bar">
            <div
              className={`confidence-fill ${guvenSinifi(taslak.guven)}`}
              style={{ width: `${taslak.guven * 100}%` }}
            />
          </div>
          <span>{Math.round(taslak.guven * 100)}%</span>
        </div>
      )}

      <div className="routing-box">
        <div className="field-label" style={{ marginBottom: 6 }}>Yönlendirme önerisi</div>
        {secilenBirim ? (
          <div className="unit-name">{secilenBirim}</div>
        ) : (
          <div className="unit-name" style={{ color: "var(--amber)" }}>
            Sistem birim seçmedi — aşağıdan siz seçin
          </div>
        )}
        <div className="reason-box" style={{ marginTop: 10, marginBottom: 0 }}>
          {yonlendirme.gerekce}
        </div>
        {yonlendirme.alternatifler.length > 0 && (
          <div className="routing-alt">
            {secilenBirim ? "Alternatif birimler: " : "Seçenekler: "}
            {yonlendirme.alternatifler.map((alt) => (
              <button
                key={alt}
                onClick={() => setSecilenBirim(alt)}
                style={{
                  marginRight: 8,
                  marginTop: 6,
                  font: "inherit",
                  fontFamily: "var(--font-mono)",
                  fontSize: 11.5,
                  background: "var(--paper)",
                  border: "1px solid var(--line-strong)",
                  borderRadius: 4,
                  padding: "3px 8px",
                  cursor: "pointer",
                }}
              >
                {alt}
              </button>
            ))}
          </div>
        )}
      </div>

      {karar === null && !bloklandi && (
        <div className="action-row">
          <button className="btn" onClick={() => setKarar("onaylandi")} disabled={!secilenBirim}>
            Onayla ve gönder
          </button>
          <button className="btn secondary" onClick={onReset}>
            Düzenlemeye devam et
          </button>
          <button className="btn danger" onClick={() => setKarar("reddedildi")}>
            Reddet
          </button>
        </div>
      )}

      {karar === null && bloklandi && (
        <div className="action-row">
          <button className="btn" onClick={onReset}>
            İnsan incelemesine gönder
          </button>
        </div>
      )}

      {karar === "onaylandi" && (
        <div className="guardrail-banner" style={{ background: "var(--green-soft)", color: "#1e5b28" }}>
          Onaylandı ({secilenBirim}). Not: bu bir mock akıştır, gerçek gönderim H2'de bağlanacak.
        </div>
      )}
      {karar === "reddedildi" && (
        <div className="guardrail-banner" style={{ background: "var(--red-soft)", color: "#7a2114" }}>
          Reddedildi — evrak tekrar incelemeye düştü.
        </div>
      )}

      {karar !== null && (
        <button className="btn secondary" style={{ marginTop: 16 }} onClick={onReset}>
          Başka bir evrak seç
        </button>
      )}
    </div>
  );
}

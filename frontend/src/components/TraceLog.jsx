export default function TraceLog({ trace, visibleCount }) {
  return (
    <div className="trace-pane">
      <h2>Ajan izi</h2>
      <p className="trace-caption">
        Orkestratörün her adımı burada canlı görünür — iddia değil, kanıt.
      </p>
      {trace.slice(0, visibleCount).map((t, i) => (
        <div key={i} className={`trace-entry ${t.status}`}>
          <div className="dot" />
          <div className="step-name">{t.label}</div>
          {t.detail && <div className="step-meta">{t.detail}</div>}
          {typeof t.confidence === "number" && (
            <div className="step-meta">güven: {t.confidence.toFixed(2)}</div>
          )}
          <span className="badge">
            {t.status === "ok" ? "tamam" : t.status === "checkpoint" ? "çekindi" : "bloklandı"}
          </span>
        </div>
      ))}
    </div>
  );
}

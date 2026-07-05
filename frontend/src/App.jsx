import { useEffect, useRef, useState } from "react";
import UploadScreen from "./components/UploadScreen.jsx";
import ResultView from "./components/ResultView.jsx";
import ApprovalPanel from "./components/ApprovalPanel.jsx";
import TraceLog from "./components/TraceLog.jsx";

const ADIMLAR = [
  { key: "upload", label: "Evrak" },
  { key: "sonuc", label: "Analiz" },
  { key: "onay", label: "Onay" },
];

export default function App() {
  const [adim, setAdim] = useState("upload");
  const [belge, setBelge] = useState(null);
  const [visibleTrace, setVisibleTrace] = useState(0);
  const timerRef = useRef(null);

  const secimYap = (secilenBelge) => {
    setBelge(secilenBelge);
    setAdim("sonuc");
    setVisibleTrace(0);
  };

  useEffect(() => {
    if (!belge) return;
    setVisibleTrace(0);
    let i = 0;
    timerRef.current = setInterval(() => {
      i += 1;
      setVisibleTrace(i);
      if (i >= belge.trace.length) clearInterval(timerRef.current);
    }, 500);
    return () => clearInterval(timerRef.current);
  }, [belge]);

  const sifirla = () => {
    setBelge(null);
    setAdim("upload");
  };

  const adimDurumu = (key) => {
    const idx = ADIMLAR.findIndex((a) => a.key === key);
    const current = ADIMLAR.findIndex((a) => a.key === adim);
    if (idx < current) return "done";
    if (idx === current) return "active";
    return "";
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="seal">KP</div>
        <div>
          <h1>Kamu Pusulası</h1>
          <div className="subtitle">Çok-ajanlı evrak &amp; yazışma destek sistemi — H1 mock arayüz iskeleti</div>
        </div>
      </header>

      <div className="stepper">
        {ADIMLAR.map((a, i) => (
          <div key={a.key} className={`step-pill ${adimDurumu(a.key)}`}>
            <span className="num">{i + 1}</span>
            {a.label}
          </div>
        ))}
      </div>

      <div className="main-layout">
        <div className="content-pane">
          {adim === "upload" && <UploadScreen onSelect={secimYap} />}
          {adim === "sonuc" && belge && (
            <ResultView belge={belge} onDevam={() => setAdim("onay")} />
          )}
          {adim === "onay" && belge && (
            <ApprovalPanel belge={belge} onReset={sifirla} />
          )}
        </div>

        {belge && (
          <TraceLog trace={belge.trace} visibleCount={visibleTrace} />
        )}
      </div>
    </div>
  );
}

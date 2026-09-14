"""Alertas de scan — som ao concluir + progresso real (APRESENTACAO, sem inteligencia).

Contrato S33-E.6 (mesmo padrao de scan_presentation/m5_widgets):
- NUNCA recalcula ranking/score/decisao, NUNCA chama scanner/engines.
- Consome apenas o view-model de present_scan() (dict) — verbatim.
- Som 100% front-end (Web Audio API, sem arquivo externo, sem rede).
  Funciona em outra aba: o browser toca o beep quando o rerun entrega o
  novo scan_id (autoplay permitido apos 1 clique do usuario na pagina).
- Progresso usa APENAS completed/total reais do ScanReport (nunca timer falso).

Uso em 01_Scanner.py / dashboard.py / operation_center.py:
    from app.dashboard.scan_alerts import render_scan_progress, render_scan_done_sound
    render_scan_progress(view)          # barra + contadores + por-ativo
    render_scan_done_sound(view)        # som 1x por scan_id + toast visual
"""
from __future__ import annotations

from typing import Any, Mapping

try:
    import streamlit as st
    import streamlit.components.v1 as components
except ImportError:  # pragma: no cover
    st = None
    components = None


def _progress_frac(view: Mapping[str, Any]) -> float:
    try:
        total = int(view.get("total") or 0)
        done = int(view.get("completed") or 0)
    except (TypeError, ValueError):
        return 0.0
    if total <= 0:
        return 0.0
    return max(0.0, min(1.0, done / total))


def render_scan_progress(view: Mapping[str, Any]) -> None:
    """Barra de andamento REAL (completed/total) + contadores + tabela por ativo."""
    if st is None:
        return
    total = view.get("total", 0) or 0
    done = view.get("completed", 0) or 0
    frac = _progress_frac(view)
    status = view.get("status", "?")
    scan_id = view.get("scan_id", "?")

    st.subheader("📡 Andamento do scaneamento")
    # Barra grande e legivel a distancia (outra tela).
    st.progress(frac, text=f"Escanenando Mercury AI — {done}/{total} ({frac * 100:.0f}%) — {status}")
    c = view.get("counters", {}) or {}
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Processados", f"{done}/{total}")
    m2.metric("Ranqueados", c.get("ranked", 0))
    m3.metric("Data-quality skip", c.get("skipped_dq", 0))
    m4.metric("Erros", c.get("error", 0))
    m5.metric("Timeouts", c.get("timeout_rows", 0))
    st.caption(f"scan_id={scan_id} | duracao={view.get('duration_s')}s | workers={view.get('workers')}")
    # Detalhe por ativo: o que ja terminou e o que falta (derivado de per_asset).
    per = view.get("per_asset", []) or []
    if per and done < total:
        faltam = total - done
        st.caption(f"⏳ Faltam ~{faltam} ativo(s). Ultimos concluidos:")
        try:
            import pandas as pd

            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "symbol": r.get("symbol"),
                            "outcome": r.get("outcome"),
                            "decision": r.get("decision"),
                            "score": r.get("score"),
                        }
                        for r in per[-10:]
                    ]
                ),
                use_container_width=True,
                height=320,
            )
        except Exception:
            st.write([f"{r.get('symbol')}:{r.get('outcome')}" for r in per[-10:]])


_BEEP_JS = """
<script>
(function() {
  const kind = "%KIND%";
  try {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    const ctx = new Ctx();
    if (ctx.state === "suspended") { ctx.resume(); }
    const now = ctx.currentTime;
    // COMPLETE: arpejo 880->1174->1568 (3x 180ms). PARTIAL: 2 beeps. ERROR/TIMEOUT: buzz grave.
    const seq = kind === "COMPLETE" ? [[880,0],[1174,0.2],[1568,0.4]]
              : kind === "PARTIAL" ? [[880,0],[880,0.25]]
              : [[196,0],[196,0.3],[147,0.6]];
    seq.forEach(([freq, dt]) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = kind === "ERROR" || kind === "TIMEOUT" ? "sawtooth" : "sine";
      o.frequency.value = freq;
      g.gain.setValueAtTime(0.0001, now + dt);
      g.gain.exponentialRampToValueAtTime(0.5, now + dt + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, now + dt + 0.18);
      o.connect(g).connect(ctx.destination);
      o.start(now + dt);
      o.stop(now + dt + 0.2);
    });
  } catch (e) { console.warn("scan-sound bloqueado:", e); }
})();
</script>
"""


def render_scan_done_sound(view: Mapping[str, Any], enable_toggle: bool = True) -> None:
    """Toca 1 beep ao concluir o ciclo (1x por scan_id) + toast visual grande.

    - Toggle "🔔 Som ao concluir" (default ON) no sidebar ou inline.
    - Guarda o ultimo scan_id em st.session_state: so toca quando chega um
      ciclo NOVO com status final (COMPLETE/PARTIAL/TIMEOUT/ERROR).
    - Alem do som: st.toast + st.success/warning/error gigante (visivel longe)
      + st.balloons() quando COMPLETE com Top-3 (opcional, sem recarregar).
    """
    if st is None or components is None:
        return
    status = str(view.get("status", "")).upper()
    scan_id = str(view.get("scan_id", ""))
    if status not in ("COMPLETE", "PARTIAL", "TIMEOUT", "ERROR"):
        return  # ciclo ainda rodando: sem som

    sound_on = True
    if enable_toggle:
        sound_on = st.sidebar.checkbox("🔔 Som ao concluir o scan", value=True)

    last_key = "_mercury_last_sounded_scan"
    already = st.session_state.get(last_key)
    is_new = already != scan_id
    if is_new:
        st.session_state[last_key] = scan_id

    # Banner gigante sempre (visivel de longe / outra tela).
    top3n = len(view.get("top3") or [])
    if status == "COMPLETE":
        st.success(f"✅ SCAN CONCLUÍDO — {view.get('progress_text')} | Top-3: {top3n} sinal(is)")
    elif status == "PARTIAL":
        st.warning(f"⚠️ SCAN PARCIAL — {view.get('progress_text')} | Top-3: {top3n}")
    elif status == "TIMEOUT":
        st.error(f"⏱ SCAN TIMEOUT — {view.get('progress_text')} (parciais preservados)")
    else:
        st.error(f"❌ SCAN ERROR — {view.get('error')}")

    if not sound_on or not is_new:
        return
    # Som via Web Audio (sem mp3 externo). Altura do components p/ executar o <script>.
    html = _BEEP_JS.replace("%KIND%", status)
    components.html(html, height=0)
    try:
        if status == "COMPLETE":
            st.toast(f"✅ Scan {scan_id[:8]} concluído — {view.get('progress_text')}", icon="🔔")
            if top3n:
                st.balloons()
        elif status == "PARTIAL":
            st.toast(f"⚠️ Scan parcial — {view.get('progress_text')}", icon="🔔")
        else:
            st.toast(f"❌ Scan {status} — ver detalhe", icon="🔔")
    except Exception:
        pass

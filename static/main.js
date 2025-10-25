
// =====================
//  POP overs + MathJax
// =====================
document.addEventListener("DOMContentLoaded", () => {
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  [...popoverTriggerList].forEach(el => {
    new bootstrap.Popover(el, {
      container: 'body',
      sanitize: false,
      html: true,
      trigger: el.getAttribute('data-bs-trigger') || 'hover focus',
      placement: el.getAttribute('data-bs-placement') || 'top'
    });
    el.addEventListener('shown.bs.popover', () => {
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    });
  });
});

// =====================
//  Torricelli mini lab
// =====================
function computeV(g, h) {
  if (g < 0 || h < 0) return null;
  return Math.sqrt(2 * g * h);
}

document.addEventListener("DOMContentLoaded", () => {
  const gInput = document.getElementById("gInput");
  const hRange = document.getElementById("hRange");
  const hInput = document.getElementById("hInput");
  const btnLive = document.getElementById("btnLive");
  const out = document.getElementById("resultado");

  if (gInput && hRange && hInput && out) {
    hRange.addEventListener("input", () => (hInput.value = hRange.value));
    hInput.addEventListener("input", () => (hRange.value = hInput.value));

    const render = (v) => {
      if (v === null || isNaN(v)) {
        out.innerHTML = `<p class="text-danger">Valores inválidos.</p>`;
        return;
      }
      out.innerHTML = `
        <p class="mb-1">Resultado (en vivo):</p>
        <p class="fs-5">\\( v = \\sqrt{2\\, g\\, h} = ${v.toFixed(4)}\\,\\text{m/s} \\)</p>
      `;
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    };

    btnLive?.addEventListener("click", () => {
      const g = parseFloat(gInput.value);
      const h = parseFloat(hInput.value);
      render(computeV(g, h));
    });
  }
});

// ===================================
//  Vaciado: gráficos + diagrama SVG
// ===================================
(function(){
  const $ = (id) => document.getElementById(id);

  function paramsFromInputs(){
    const A  = parseFloat($('AInput')?.value);
    const a  = parseFloat($('aInput')?.value);
    const g  = parseFloat($('gInput')?.value);
    const h0 = parseFloat($('h0Input')?.value);
    return {A, a, g, h0};
  }
  function computeT(A,a,g,h0){
    if(!(A>0 && a>0 && g>=0 && h0>=0)) return null;
    const k = (a/A) * Math.sqrt(2*g);
    return (2*Math.sqrt(h0))/k;
  }
  function h_of_t(t, A,a,g,h0){
    const term = Math.sqrt(h0) - (a/(2*A))*Math.sqrt(2*g)*t;
    return Math.max(0, term*term);
  }

  // -------- Chart.js: curva + sombra + marcador --------
  let chart = null;
  const CURVE = { T: null, labels: [], data: [] };
  const DS_CURVE  = 0;
  const DS_SHADE  = 1;
  const DS_MARKER = 2;

  // “plantillas” de datasets
  function makeShadeDataset(){
    return {
      label: 'Área hasta t',
      data: [],
      fill: 'origin',
      backgroundColor: 'rgba(30,144,255,0.20)',
      borderWidth: 0,
      pointRadius: 0,
      tension: 0.15
    };
  }
  function makeMarkerDataset(){
    return {
      label: 't actual',
      data: [],
      showLine: false,
      borderColor: 'rgba(0,0,0,0)',
      pointRadius: 5,
      pointHoverRadius: 6
    };
  }

  function ensureShadeAndMarkerDatasets(c){
    // Si tu chart “viejo” sólo tenía 1 dataset, añadimos los que faltan
    const ds = c.data.datasets;
    if (ds.length < 2) ds[1] = makeShadeDataset();
    if (ds.length < 3) ds[2] = makeMarkerDataset();
  }

  function getOrCreateChart(){
    const canvas = $('chartH');
    if (!canvas) return null;

    const existing = Chart.getChart(canvas);
    if (existing) {
      chart = existing;
      ensureShadeAndMarkerDatasets(chart);
      return chart;
    }

    chart = new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          { label: 'h(t) [m]', data: [], tension: 0.15 },
          makeShadeDataset(),
          makeMarkerDataset()
        ]
      },
      options: {
        responsive: true,
        animation: false,
        scales: {
          x: { title: { display: true, text: 't [s]' } },
          y: { title: { display: true, text: 'h [m]' }, beginAtZero: true }
        },
        plugins: { legend: { display: true } }
      }
    });
    return chart;
  }

  function plotFromInputs(){
    const resDiv = $('resultadoT');
    const {A,a,g,h0} = paramsFromInputs();
    const T = computeT(A,a,g,h0);

    if (!chart) getOrCreateChart();
    if (!chart) return;
    ensureShadeAndMarkerDatasets(chart); // <- por si vino de una versión con 1 dataset

    if (T == null || !isFinite(T)) {
      if (resDiv) resDiv.innerHTML = '<p class="text-danger">Parámetros inválidos.</p>';
      chart.data.labels = [];
      chart.data.datasets[DS_CURVE].data  = [];
      chart.data.datasets[DS_SHADE].data  = [];
      chart.data.datasets[DS_MARKER].data = [];
      chart.update();
      return;
    }

    if (resDiv) {
      resDiv.innerHTML =
        `<p class="mb-1">Tiempo total de vaciado (en vivo):</p>
         <p class="fs-5">\\( T = ${T.toFixed(4)}\\,\\text{s} \\)</p>`;
      if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();
    }

    const N = 60;
    const labels = [];
    const data = [];
    for (let i=0;i<=N;i++){
      const t = T * i / N;
      labels.push(t.toFixed(2));
      data.push(h_of_t(t, A,a,g,h0));
    }

    chart.data.labels = labels;
    chart.data.datasets[DS_CURVE].data = data;

    CURVE.T = T; CURVE.labels = labels; CURVE.data = data;

    const tSlider = $('tRange');
    if (tSlider) {
      tSlider.max = T.toFixed(6);
      if (parseFloat(tSlider.value) > T) tSlider.value = T;
    }

    updateShadingFromSlider();
    chart.update('none');
  }

  function updateShadingFromSlider() {
    const tSlider = $('tRange');
    if (!tSlider || CURVE.T == null) return;
    const t = Math.min(parseFloat(tSlider.value) || 0, CURVE.T);
    updateShadingAtTime(t);
  }

  function updateShadingAtTime(t) {
    if (CURVE.T == null || !isFinite(CURVE.T) || !chart) return;
    ensureShadeAndMarkerDatasets(chart); // <- asegura índices 1 y 2
    const N = CURVE.labels.length - 1;
    const idx = Math.max(0, Math.min(N, Math.round((t / CURVE.T) * N)));

    chart.data.datasets[DS_SHADE].data  = CURVE.data.map((v, i) => (i <= idx ? v : null));
    chart.data.datasets[DS_MARKER].data = CURVE.data.map((v, i) => (i === idx ? v : null));

    chart.update('none');
  }

  // -------- Diagrama SVG (tanque) --------
  const TANK_BOT_Y = 300;
  const INNER_HEIGHT_PX = 220;
  const RX = 80, RY = 24;

  function drawWater(h, h0){
    const waterRect = $('waterRect');
    const waterTop  = $('waterTop');
    if (!waterRect || !waterTop) return;

    const hRel = (h0>0) ? Math.min(Math.max(h/h0, 0), 1) : 0;
    const yTop = TANK_BOT_Y - hRel*INNER_HEIGHT_PX;

    const bodyHeight = Math.max(0, (TANK_BOT_Y - yTop));
    waterRect.setAttribute('y', yTop);
    waterRect.setAttribute('height', bodyHeight);

    waterTop.setAttribute('cy', yTop);
    waterTop.setAttribute('rx', RX);
    waterTop.setAttribute('ry', RY);

    const hUp   = $('hArrowUp');
    const hDown = $('hArrowDown');
    const hLbl  = $('hLabel');
    if (hUp && hDown && hLbl){
      hUp.setAttribute('x1', 260); hUp.setAttribute('x2', 260);
      hDown.setAttribute('x1', 260); hDown.setAttribute('x2', 260);
      hUp.setAttribute('y1', TANK_BOT_Y);
      hUp.setAttribute('y2', yTop+4);
      hDown.setAttribute('y1', yTop+4);
      hDown.setAttribute('y2', TANK_BOT_Y);
      hLbl.setAttribute('x', 266);
      hLbl.setAttribute('y', (yTop + TANK_BOT_Y)/2 - 6);
    }
  }

  function setLabels(A,a){
    const Atext = $('Atext'), atext = $('atext'), Rtext = $('Rtext'), rtext = $('rtext');
    const R = (A>0) ? Math.sqrt(A/Math.PI) : NaN;
    const r = (a>0) ? Math.sqrt(a/Math.PI) : NaN;

    if (Atext) Atext.textContent = `A = πR² = ${isFinite(A)?A.toFixed(4):'—'} m²`;
    if (atext) atext.textContent = `a = πr² = ${isFinite(a)?a.toFixed(6):'—'} m²`;
    if (Rtext) Rtext.textContent = `R = ${isFinite(R)?R.toFixed(4):'—'} m`;
    if (rtext) rtext.textContent = `r = ${isFinite(r)?r.toFixed(4):'—'} m`;
  }

  function updateDiagram(){
    const {A,a,g,h0} = paramsFromInputs();
    const tSlider = $('tRange');
    const tDisp   = $('tVal');
    const hDisp   = $('hVal');

    const T = computeT(A,a,g,h0);
    if (!isFinite(T) || T<=0) {
      if (tSlider) { tSlider.max = 1; tSlider.value = 0; }
      if (tDisp) tDisp.textContent = '0.00';
      if (hDisp) hDisp.textContent = '—';
      drawWater(h0, h0);
      setLabels(A,a);
      return;
    }

    if (tSlider) tSlider.max = T.toFixed(6);
    const t = Math.min(parseFloat(tSlider?.value)||0, T);
    if (tSlider) tSlider.value = t;

    const h = h_of_t(t, A,a,g,h0);
    if (tDisp) tDisp.textContent = t.toFixed(2);
    if (hDisp) hDisp.textContent = h.toFixed(4);

    drawWater(h, h0);
    setLabels(A,a);
  }

  // -------- Eventos --------
  document.getElementById('btnPlot')?.addEventListener('click', () => {
    plotFromInputs();
    updateDiagram();
  });

  ['AInput','aInput','gInput','h0Input'].forEach(id=>{
    const el = $(id);
    if (el) el.addEventListener('input', () => {
      plotFromInputs();
      updateDiagram();
    });
  });

  $('tRange')?.addEventListener('input', () => {
    updateShadingFromSlider();
    updateDiagram();
  });

  // -------- Inicialización al cargar --------
  window.addEventListener('load', () => {
    getOrCreateChart();          // crea o reutiliza
    updateDiagram();             // diagrama
    plotFromInputs();            // curva + sombra
  });

})();


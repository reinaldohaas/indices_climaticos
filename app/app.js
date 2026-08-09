/**
 * Explorador Interativo de Índices Climáticos
 * Front-end Logic, Plotly Rendering, Moving Average Smoothing, Correlation & Lag Analysis
 */

// Global State
let rawData = {};
let metadata = [];
let selectedIndices = ['oni', 'sam', 'psa1'];
let startYear = 1950;
let endYear = 2026;
let smoothingWindow = 1;
let normalizeZScore = true;
let dualYAxis = false;

// Distinct Vibrant Colors Palette for Plotly Traces
const TRACE_COLORS = [
  '#00f2fe', '#4facfe', '#8b5cf6', '#10b981', '#f59e0b',
  '#f43f5e', '#ec4899', '#a855f7', '#3b82f6', '#06b6d4',
  '#84cc16', '#eab308', '#f97316', '#ef4444'
];

// Presets Definition
const PRESETS = {
  enso_sam: ['oni', 'sam', 'psa1'],
  atlantic_dipole: ['sad', 'sasdi', 'sacz'],
  pacific_modes: ['pdo', 'pmm', 'oni'],
  monsoon_sacz: ['sami', 'sacz', 'mjo_omi'],
  solar_climate: ['ssn', 'ao', 'nao']
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  await loadDataAndMetadata();
  initUIControls();
  updateDashboard();
});

// Load JSON datasets with robust path resolution
async function loadDataAndMetadata() {
  try {
    const isAppSubdir = window.location.pathname.includes('/app/');
    const dataPath = isAppSubdir ? 'data.json' : 'app/data.json';
    const metaPath = isAppSubdir ? 'metadata.json' : 'app/metadata.json';

    const [dataResp, metaResp] = await Promise.all([
      fetch(dataPath),
      fetch(metaPath)
    ]);

    if (!dataResp.ok || !metaResp.ok) {
      throw new Error(`HTTP Error ${dataResp.status} / ${metaResp.status}`);
    }

    rawData = await dataResp.json();
    metadata = await metaResp.json();
    
    // Update badge
    document.getElementById('total-indices-badge').innerHTML = 
      `<i class="fa-solid fa-database"></i> ${Object.keys(rawData).length} Índices`;
      
    populateIndexCheckboxes();
    populateSelectDropdowns();
    renderCatalogTable();
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('timeseries-plotly-chart').innerHTML = 
      `<div class="info-callout" style="border-color:#f43f5e; color:#f43f5e;">
        <i class="fa-solid fa-triangle-exclamation"></i> 
        Erro ao carregar dados (${err.message}). Certifique-se de acessar via <a href="app/index.html" style="color:#00f2fe;">app/index.html</a>.
       </div>`;
  }
}

// Populate Index Checkboxes in Sidebar
function populateIndexCheckboxes(filteredList = null) {
  const container = document.getElementById('indices-checkbox-list');
  if (!container) return;
  container.innerHTML = '';

  const listToRender = filteredList || Object.keys(rawData);

  listToRender.sort().forEach(idxKey => {
    const metaItem = metadata.find(m => m.index === idxKey) || {};
    const label = metaItem.description || idxKey.toUpperCase();
    const category = metaItem.category || 'Outros';
    const isChecked = selectedIndices.includes(idxKey);

    const item = document.createElement('div');
    item.className = `checkbox-item ${isChecked ? 'selected' : ''}`;
    item.onclick = (e) => {
      if (e.target.tagName !== 'INPUT') {
        const chk = item.querySelector('input');
        chk.checked = !chk.checked;
        toggleIndexSelection(idxKey, chk.checked);
      }
    };

    item.innerHTML = `
      <input type="checkbox" id="chk-${idxKey}" ${isChecked ? 'checked' : ''} onchange="toggleIndexSelection('${idxKey}', this.checked)">
      <span class="checkbox-label-text" title="${label}">${idxKey.toUpperCase()} - ${label}</span>
      <span class="badge-tag">${category.split(' ')[0]}</span>
    `;

    container.appendChild(item);
  });
}

function toggleIndexSelection(idxKey, isChecked) {
  if (isChecked && !selectedIndices.includes(idxKey)) {
    selectedIndices.push(idxKey);
  } else if (!isChecked && selectedIndices.includes(idxKey)) {
    selectedIndices = selectedIndices.filter(k => k !== idxKey);
  }
  populateIndexCheckboxes();
  populateSelectDropdowns();
  updateDashboard();
}

function clearSelectedIndices() {
  selectedIndices = [];
  populateIndexCheckboxes();
  populateSelectDropdowns();
  updateDashboard();
}

// Populate Select Dropdowns for Lag and Scatter plots
function populateSelectDropdowns() {
  const selects = ['lag-index-a', 'lag-index-b', 'scatter-index-x', 'scatter-index-y'];
  
  selects.forEach(selId => {
    const elem = document.getElementById(selId);
    if (!elem) return;
    const currentVal = elem.value;
    elem.innerHTML = '';

    const list = selectedIndices.length >= 2 ? selectedIndices : Object.keys(rawData);
    list.forEach(k => {
      const opt = document.createElement('option');
      opt.value = k;
      opt.textContent = k.toUpperCase();
      elem.appendChild(opt);
    });

    if (currentVal && list.includes(currentVal)) {
      elem.value = currentVal;
    } else if (list.length >= 2) {
      if (selId.endsWith('b') || selId.endsWith('y')) {
        elem.value = list[1];
      } else {
        elem.value = list[0];
      }
    }
  });
}

// Filter Categories
function filterCategory(catName) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  if (event && event.target) {
    event.target.classList.add('active');
  }

  if (catName === 'all') {
    populateIndexCheckboxes();
    return;
  }

  const matchingKeys = metadata
    .filter(m => m.category && m.category.toLowerCase().includes(catName.toLowerCase()))
    .map(m => m.index);

  populateIndexCheckboxes(matchingKeys);
}

// Filter Search Box
function filterIndexList() {
  const query = document.getElementById('index-search-input').value.toLowerCase();
  const matchingKeys = Object.keys(rawData).filter(k => {
    const metaItem = metadata.find(m => m.index === k) || {};
    return k.toLowerCase().includes(query) || (metaItem.description && metaItem.description.toLowerCase().includes(query));
  });
  populateIndexCheckboxes(matchingKeys);
}

// Controls Listeners
function initUIControls() {
  const sInput = document.getElementById('start-year-input');
  const eInput = document.getElementById('end-year-input');
  if (sInput) sInput.value = startYear;
  if (eInput) eInput.value = endYear;
}

function setQuickDateRange(start, end) {
  startYear = start;
  endYear = end;
  document.getElementById('start-year-input').value = start;
  document.getElementById('end-year-input').value = end;
  updateDashboard();
}

function onSmoothingChange(val) {
  smoothingWindow = parseInt(val);
  const badge = document.getElementById('smoothing-val-badge');
  if (badge) badge.textContent = smoothingWindow === 1 ? '1 mês (Bruto)' : `${smoothingWindow} meses`;
  updateDashboard();
}

function setSmoothing(win) {
  const slider = document.getElementById('smoothing-window-slider');
  if (slider) slider.value = win;
  onSmoothingChange(win);
}

function applyPreset(presetKey) {
  if (PRESETS[presetKey]) {
    selectedIndices = [...PRESETS[presetKey]];
    populateIndexCheckboxes();
    populateSelectDropdowns();
    updateDashboard();
  }
}

// Master Dashboard Update Routine
function updateDashboard() {
  const sInput = document.getElementById('start-year-input');
  const eInput = document.getElementById('end-year-input');
  const zToggle = document.getElementById('normalize-zscore-toggle');
  const dToggle = document.getElementById('dual-yaxis-toggle');

  if (sInput) startYear = parseInt(sInput.value) || 1749;
  if (eInput) endYear = parseInt(eInput.value) || 2026;
  if (zToggle) normalizeZScore = zToggle.checked;
  if (dToggle) dualYAxis = dToggle.checked;

  renderTimeSeriesChart();
  renderCorrelationMatrix();
  renderLagChart();
  renderScatterChart();
}

// Math Helpers: Moving Average & Z-Score
function calculateMovingAverage(values, windowSize) {
  if (windowSize <= 1) return values;
  const result = [];
  for (let i = 0; i < values.length; i++) {
    let sum = 0;
    let count = 0;
    for (let j = Math.max(0, i - windowSize + 1); j <= i; j++) {
      if (values[j] !== null && !isNaN(values[j])) {
        sum += values[j];
        count++;
      }
    }
    result.push(count > 0 ? sum / count : null);
  }
  return result;
}

function calculateZScore(values) {
  const validVals = values.filter(v => v !== null && !isNaN(v));
  if (validVals.length === 0) return values;

  const mean = validVals.reduce((a, b) => a + b, 0) / validVals.length;
  const variance = validVals.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / validVals.length;
  const std = Math.sqrt(variance) || 1;

  return values.map(v => (v !== null && !isNaN(v)) ? (v - mean) / std : null);
}

// Render Plotly Time Series Chart
function renderTimeSeriesChart() {
  const container = document.getElementById('timeseries-plotly-chart');
  if (!container) return;

  if (selectedIndices.length === 0) {
    Plotly.purge(container);
    container.innerHTML = '<div class="info-callout"><i class="fa-solid fa-circle-exclamation"></i> Nenhum índice selecionado. Escolha pelo menos um índice no painel lateral.</div>';
    return;
  }

  const traces = [];

  selectedIndices.forEach((idxKey, colorIdx) => {
    const series = rawData[idxKey];
    if (!series) return;

    const filteredDates = [];
    const filteredVals = [];

    for (let i = 0; i < series.dates.length; i++) {
      const yr = series.years[i];
      if (yr >= startYear && yr <= endYear) {
        filteredDates.push(series.dates[i]);
        filteredVals.push(series.values[i]);
      }
    }

    let processedVals = calculateMovingAverage(filteredVals, smoothingWindow);
    if (normalizeZScore) {
      processedVals = calculateZScore(processedVals);
    }

    const metaItem = metadata.find(m => m.index === idxKey) || {};
    const label = `${idxKey.toUpperCase()} - ${metaItem.description || ''}`;

    const trace = {
      x: filteredDates,
      y: processedVals,
      mode: 'lines',
      name: label,
      line: {
        color: TRACE_COLORS[colorIdx % TRACE_COLORS.length],
        width: 2.2
      },
      hoverinfo: 'x+y+name'
    };

    if (dualYAxis && selectedIndices.length === 2 && colorIdx === 1) {
      trace.yaxis = 'y2';
    }

    traces.push(trace);
  });

  const layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#9ca3af', family: 'Inter, sans-serif' },
    margin: { l: 50, r: dualYAxis ? 50 : 20, t: 30, b: 50 },
    xaxis: {
      gridcolor: '#1f293d',
      zerolinecolor: '#374151',
      rangeslider: { visible: true, thickness: 0.08, bgcolor: '#090d16' }
    },
    yaxis: {
      title: normalizeZScore ? 'Desvio Padronizado (Z-Score)' : 'Valor Absoluto',
      gridcolor: '#1f293d',
      zerolinecolor: '#374151'
    },
    legend: {
      orientation: 'h',
      y: 1.15,
      x: 0,
      font: { color: '#f3f4f6', size: 12 }
    }
  };

  if (dualYAxis && selectedIndices.length === 2) {
    layout.yaxis2 = {
      title: `${selectedIndices[1].toUpperCase()} (Eixo Secundário)`,
      overlaying: 'y',
      side: 'right',
      gridcolor: '#1f293d',
      zerolinecolor: '#374151'
    };
  }

  Plotly.react(container, traces, layout, { responsive: true, displayModeBar: true });
}

// Render Correlation Matrix Heatmap
function renderCorrelationMatrix() {
  const container = document.getElementById('correlation-matrix-chart');
  if (!container) return;

  if (selectedIndices.length < 2) {
    Plotly.purge(container);
    container.innerHTML = '<div class="info-callout"><i class="fa-solid fa-circle-info"></i> Selecione pelo menos 2 índices para calcular a matriz de correlação.</div>';
    return;
  }

  const matrix = [];
  const labels = selectedIndices.map(k => k.toUpperCase());

  selectedIndices.forEach((keyA) => {
    const row = [];
    selectedIndices.forEach((keyB) => {
      const r = calculatePairwiseCorrelation(keyA, keyB);
      row.push(r !== null ? parseFloat(r.toFixed(3)) : 0);
    });
    matrix.push(row);
  });

  const trace = {
    z: matrix,
    x: labels,
    y: labels,
    type: 'heatmap',
    colorscale: [
      [0, '#3b82f6'],
      [0.5, '#111827'],
      [1, '#ef4444']
    ],
    zmin: -1,
    zmax: 1,
    colorbar: { title: 'Correlação (r)', tickcolor: '#9ca3af' }
  };

  const layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#9ca3af', family: 'Inter, sans-serif' },
    margin: { l: 80, r: 20, t: 20, b: 80 }
  };

  Plotly.react(container, [trace], layout, { responsive: true });
}

// Pairwise Pearson Correlation
function calculatePairwiseCorrelation(keyA, keyB, lag = 0) {
  const sA = rawData[keyA];
  const sB = rawData[keyB];
  if (!sA || !sB) return null;

  const dictB = {};
  for (let i = 0; i < sB.dates.length; i++) {
    dictB[sB.dates[i]] = sB.values[i];
  }

  const valA = [];
  const valB = [];

  for (let i = 0; i < sA.dates.length; i++) {
    const yr = sA.years[i];
    if (yr >= startYear && yr <= endYear) {
      const d = sA.dates[i];
      const vA = sA.values[i];
      const vB = dictB[d];

      if (vA !== null && vB !== null && !isNaN(vA) && !isNaN(vB)) {
        valA.push(vA);
        valB.push(vB);
      }
    }
  }

  if (valA.length < 12) return null;

  let x = valA;
  let y = valB;

  if (lag > 0) {
    x = valA.slice(0, valA.length - lag);
    y = valB.slice(lag);
  } else if (lag < 0) {
    const absLag = Math.abs(lag);
    x = valA.slice(absLag);
    y = valB.slice(0, valB.length - absLag);
  }

  const meanX = x.reduce((a, b) => a + b, 0) / x.length;
  const meanY = y.reduce((a, b) => a + b, 0) / y.length;

  let num = 0;
  let denX = 0;
  let denY = 0;

  for (let i = 0; i < x.length; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    num += dx * dy;
    denX += dx * dx;
    denY += dy * dy;
  }

  const den = Math.sqrt(denX * denY);
  return den === 0 ? 0 : num / den;
}

// Render Lagged Cross-Correlation Chart (-24 to +24 months)
function renderLagChart() {
  const container = document.getElementById('lag-plotly-chart');
  const selA = document.getElementById('lag-index-a');
  const selB = document.getElementById('lag-index-b');

  if (!container || !selA || !selB) return;

  const keyA = selA.value;
  const keyB = selB.value;

  if (!keyA || !keyB || !rawData[keyA] || !rawData[keyB]) {
    Plotly.purge(container);
    return;
  }

  const lags = [];
  const corrs = [];

  for (let l = -24; l <= 24; l++) {
    lags.push(l);
    const r = calculatePairwiseCorrelation(keyA, keyB, l);
    corrs.push(r !== null ? parseFloat(r.toFixed(3)) : 0);
  }

  const maxCorrIdx = corrs.indexOf(Math.max(...corrs));
  const peakLag = lags[maxCorrIdx];
  const peakVal = corrs[maxCorrIdx];

  const infoBox = document.getElementById('lag-info-box');
  if (infoBox) {
    infoBox.innerHTML = `
      <i class="fa-solid fa-bullseye"></i> 
      <strong>Pico de Correlação:</strong> Correlação máxima de <strong>r = ${peakVal}</strong> ocorre na defasagem de <strong>${peakLag} meses</strong> 
      (${keyA.toUpperCase()} antecede ${keyB.toUpperCase()} em ${peakLag} meses).
    `;
  }

  const trace = {
    x: lags,
    y: corrs,
    type: 'bar',
    marker: {
      color: corrs.map((v, i) => i === maxCorrIdx ? '#00f2fe' : '#3b82f6')
    }
  };

  const layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#9ca3af', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 20, t: 20, b: 50 },
    xaxis: { title: `Defasagem em Meses (${keyA.toUpperCase()} vs ${keyB.toUpperCase()})`, gridcolor: '#1f293d' },
    yaxis: { title: 'Coeficiente de Correlação (r)', gridcolor: '#1f293d', range: [-1, 1] }
  };

  Plotly.react(container, [trace], layout, { responsive: true });
}

// Render Scatter Plot & Regression
function renderScatterChart() {
  const container = document.getElementById('scatter-plotly-chart');
  const selX = document.getElementById('scatter-index-x');
  const selY = document.getElementById('scatter-index-y');

  if (!container || !selX || !selY) return;

  const keyX = selX.value;
  const keyY = selY.value;

  if (!keyX || !keyY || !rawData[keyX] || !rawData[keyY]) {
    Plotly.purge(container);
    return;
  }

  const sX = rawData[keyX];
  const sY = rawData[keyY];
  const dictY = {};
  for (let i = 0; i < sY.dates.length; i++) {
    dictY[sY.dates[i]] = sY.values[i];
  }

  const xVals = [];
  const yVals = [];

  for (let i = 0; i < sX.dates.length; i++) {
    const yr = sX.years[i];
    if (yr >= startYear && yr <= endYear) {
      const vX = sX.values[i];
      const vY = dictY[sX.dates[i]];
      if (vX !== null && vY !== null && !isNaN(vX) && !isNaN(vY)) {
        xVals.push(vX);
        yVals.push(vY);
      }
    }
  }

  if (xVals.length < 5) return;

  const meanX = xVals.reduce((a, b) => a + b, 0) / xVals.length;
  const meanY = yVals.reduce((a, b) => a + b, 0) / yVals.length;

  let num = 0;
  let den = 0;
  for (let i = 0; i < xVals.length; i++) {
    num += (xVals[i] - meanX) * (yVals[i] - meanY);
    den += Math.pow(xVals[i] - meanX, 2);
  }

  const slope = den === 0 ? 0 : num / den;
  const intercept = meanY - slope * meanX;
  const r = calculatePairwiseCorrelation(keyX, keyY);
  const r2 = r !== null ? Math.pow(r, 2) : 0;

  const statsGrid = document.getElementById('scatter-stats-grid');
  if (statsGrid) {
    statsGrid.innerHTML = `
      <div class="stat-box">
        <div class="stat-label">Coeficiente R²</div>
        <div class="stat-value">${r2.toFixed(3)}</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Correlação (r)</div>
        <div class="stat-value">${r !== null ? r.toFixed(3) : '0'}</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Inclinação (Slope m)</div>
        <div class="stat-value">${slope.toFixed(4)}</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Observações (N)</div>
        <div class="stat-value">${xVals.length}</div>
      </div>
    `;
  }

  const minX = Math.min(...xVals);
  const maxX = Math.max(...xVals);
  const lineX = [minX, maxX];
  const lineY = [slope * minX + intercept, slope * maxX + intercept];

  const tracePoints = {
    x: xVals,
    y: yVals,
    mode: 'markers',
    name: 'Observações Mensais',
    marker: { color: '#00f2fe', opacity: 0.6, size: 6 }
  };

  const traceLine = {
    x: lineX,
    y: lineY,
    mode: 'lines',
    name: `Ajuste Linear (y = ${slope.toFixed(2)}x + ${intercept.toFixed(2)})`,
    line: { color: '#ef4444', width: 2.5 }
  };

  const layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#9ca3af', family: 'Inter, sans-serif' },
    margin: { l: 50, r: 20, t: 20, b: 50 },
    xaxis: { title: `${keyX.toUpperCase()}`, gridcolor: '#1f293d' },
    yaxis: { title: `${keyY.toUpperCase()}`, gridcolor: '#1f293d' }
  };

  Plotly.react(container, [tracePoints, traceLine], layout, { responsive: true });
}

// Tab Switching
function switchTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

  if (event && event.currentTarget) {
    event.currentTarget.classList.add('active');
  }
  const targetTab = document.getElementById(`tab-${tabName}`);
  if (targetTab) targetTab.classList.add('active');

  updateDashboard();
}

// Render Catalog Table
function renderCatalogTable(filteredData = null) {
  const tbody = document.getElementById('catalog-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  const list = filteredData || metadata;

  list.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${m.index.toUpperCase()}</strong></td>
      <td>${m.description || ''}</td>
      <td><span class="badge-tag">${m.category || ''}</span></td>
      <td><a href="${m.source_url}" target="_blank" style="color:var(--primary-cyan); text-decoration:none;">${m.source || 'Link'}</a></td>
      <td>${m.start_date.substring(0, 7)} até ${m.end_date.substring(0, 7)}</td>
      <td>${m.units || ''}</td>
      <td>${m.reference || 'NOAA PSL'}</td>
    `;
    tbody.appendChild(tr);
  });
}

function filterCatalogTable() {
  const input = document.getElementById('catalog-search');
  if (!input) return;
  const query = input.value.toLowerCase();
  const filtered = metadata.filter(m => {
    return (m.index && m.index.toLowerCase().includes(query)) ||
           (m.description && m.description.toLowerCase().includes(query)) ||
           (m.source && m.source.toLowerCase().includes(query)) ||
           (m.category && m.category.toLowerCase().includes(query));
  });
  renderCatalogTable(filtered);
}

// Export CSV of Filtered Selected Data
function exportDataCSV() {
  if (selectedIndices.length === 0) return;

  const header = ['date', 'year', 'month', ...selectedIndices].join(',');
  const rows = [header];

  const baseSeries = rawData[selectedIndices[0]];
  if (!baseSeries) return;

  for (let i = 0; i < baseSeries.dates.length; i++) {
    const yr = baseSeries.years[i];
    if (yr >= startYear && yr <= endYear) {
      const d = baseSeries.dates[i];
      const m = baseSeries.months[i];
      const rowVals = [d, yr, m];

      selectedIndices.forEach(k => {
        const s = rawData[k];
        if (s) {
          const idxDate = s.dates.indexOf(d);
          rowVals.push(idxDate !== -1 && s.values[idxDate] !== null ? s.values[idxDate] : '');
        } else {
          rowVals.push('');
        }
      });

      rows.push(rowVals.join(','));
    }
  }

  const csvContent = "data:text/csv;charset=utf-8," + rows.join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `climate_indices_selection_${startYear}_${endYear}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

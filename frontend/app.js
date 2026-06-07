const form = document.querySelector("#prediction-form");
const runButton = document.querySelector("#run-button");
const daysInput = document.querySelector("#days-ahead");
const daysLabel = document.querySelector("#days-label");
const chart = document.querySelector("#chart");
const ctx = chart.getContext("2d");
const toast = document.querySelector("#toast");
const emptyState = document.querySelector("#empty-state");
const forecastBody = document.querySelector("#forecast-body");
const forecastCaption = document.querySelector("#forecast-caption");
const chartTitle = document.querySelector("#chart-title");
const modelLabel = document.querySelector("#model-label");
const tabs = document.querySelectorAll(".tab");

let activeView = "price";
let latestResult = null;

daysInput.addEventListener("input", () => {
  daysLabel.textContent = daysInput.value;
});

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    activeView = tab.dataset.view;
    render();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setLoading(true);
  hideToast();

  const formData = new FormData(form);
  const payload = {
    ticker: formData.get("ticker"),
    start: formData.get("start"),
    end: formData.get("end"),
    daysAhead: Number(formData.get("daysAhead")),
    model: formData.get("model"),
  };

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Prediction failed.");
    }

    latestResult = data;
    renderSummary(data);
    renderTable(data);
    render();
  } catch (error) {
    showToast(error.message);
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  runButton.disabled = isLoading;
  runButton.textContent = isLoading ? "Running..." : "Run prediction";
}

function renderSummary(data) {
  document.querySelector("#latest-close").textContent = formatMoney(data.latestClose, data.currency);
  document.querySelector("#mae").textContent = formatMoney(data.metrics.mae, data.currency);
  document.querySelector("#r2").textContent = data.metrics.r2.toFixed(3);
  modelLabel.textContent = data.model;
  chartTitle.textContent = `${data.ticker} close price and indicators`;
}

function renderTable(data) {
  forecastCaption.textContent = `${data.forecast.length} business-day forecast using ${data.model}.`;
  forecastBody.innerHTML = data.forecast
    .map((row) => `<tr><td>${row.date}</td><td>${formatMoney(row.close, data.currency)}</td></tr>`)
    .join("");
}

function render() {
  resizeCanvas();
  ctx.clearRect(0, 0, chart.width, chart.height);

  if (!latestResult) {
    emptyState.hidden = false;
    return;
  }

  emptyState.hidden = true;
  if (activeView === "rsi") {
    drawChart([{ name: "RSI", color: "#b7791f", values: latestResult.history.map(point("rsi")) }], 0, 100);
    chartTitle.textContent = `${latestResult.ticker} relative strength index`;
    return;
  }

  if (activeView === "forecast") {
    drawChart([{ name: "Forecast", color: "#2f855a", values: latestResult.forecast.map(point("close")) }]);
    chartTitle.textContent = `${latestResult.ticker} forecast`;
    return;
  }

  drawChart([
    { name: "Close", color: "#126e82", values: latestResult.history.map(point("close")) },
    { name: "SMA 20", color: "#b7791f", values: latestResult.history.map(point("sma20")) },
    { name: "EMA 20", color: "#2f855a", values: latestResult.history.map(point("ema20")) },
  ]);
  chartTitle.textContent = `${latestResult.ticker} close price and indicators`;
}

function point(key) {
  return (item) => ({ date: item.date, value: item[key] });
}

function drawChart(series, forcedMin, forcedMax) {
  const size = canvasSize();
  const padding = { top: 28, right: 28, bottom: 42, left: 68 };
  const width = size.width - padding.left - padding.right;
  const height = size.height - padding.top - padding.bottom;
  const values = series.flatMap((line) => line.values.map((item) => item.value)).filter((value) => value !== null);

  if (!values.length) {
    return;
  }

  const min = forcedMin ?? Math.min(...values);
  const max = forcedMax ?? Math.max(...values);
  const range = max - min || 1;

  drawAxes(padding, width, height, min, max);

  series.forEach((line) => {
    const cleanValues = line.values.filter((item) => item.value !== null);
    ctx.beginPath();
    cleanValues.forEach((item, index) => {
      const x = padding.left + (index / Math.max(cleanValues.length - 1, 1)) * width;
      const y = padding.top + height - ((item.value - min) / range) * height;
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    ctx.strokeStyle = line.color;
    ctx.lineWidth = 3;
    ctx.stroke();
  });

  drawLegend(series, padding.left, 18);
}

function drawAxes(padding, width, height, min, max) {
  ctx.strokeStyle = "#d9e2ec";
  ctx.lineWidth = 1;
  ctx.fillStyle = "#667085";
  ctx.font = "14px Segoe UI, sans-serif";

  for (let index = 0; index <= 4; index += 1) {
    const y = padding.top + (height / 4) * index;
    const value = max - ((max - min) / 4) * index;
    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(padding.left + width, y);
    ctx.stroke();
    ctx.fillText(value.toFixed(2), 12, y + 4);
  }
}

function drawLegend(series, x, y) {
  let cursor = x;
  ctx.font = "14px Segoe UI, sans-serif";
  series.forEach((line) => {
    ctx.fillStyle = line.color;
    ctx.fillRect(cursor, y - 10, 16, 4);
    ctx.fillStyle = "#344054";
    ctx.fillText(line.name, cursor + 22, y - 4);
    cursor += ctx.measureText(line.name).width + 64;
  });
}

function resizeCanvas() {
  const rect = chart.getBoundingClientRect();
  const scale = window.devicePixelRatio || 1;
  chart.width = Math.max(640, Math.floor(rect.width * scale));
  chart.height = Math.max(360, Math.floor(rect.height * scale));
  ctx.setTransform(scale, 0, 0, scale, 0, 0);
}

function canvasSize() {
  const scale = window.devicePixelRatio || 1;
  return {
    width: chart.width / scale,
    height: chart.height / scale,
  };
}

function formatMoney(value, currency) {
  return `${currency}${Number(value).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function showToast(message) {
  toast.textContent = message;
  toast.hidden = false;
}

function hideToast() {
  toast.hidden = true;
}

window.addEventListener("resize", render);
render();

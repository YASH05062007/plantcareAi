/* ── API URL helpers ───────────────────────────────────────────── */
const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getAPIBaseUrl() {
  const host  = window.location.hostname;
  const proto = window.location.protocol;
  if (host.includes(".app.github.dev")) {
    const base = host.replace(/-\d+\.app\.github\.dev$/, "");
    return `${proto}//${base}-8000.app.github.dev`;
  }
  return DEFAULT_API_BASE_URL;
}

async function loadFrontendEnv() {
  try {
    const res = await fetch("./.env", { cache: "no-store" });
    if (!res.ok) return {};
    const text = await res.text();
    const env  = {};
    text.split("\n").forEach((line) => {
      const t = line.trim();
      if (!t || t.startsWith("#") || !t.includes("=")) return;
      const idx = t.indexOf("=");
      env[t.slice(0, idx).trim()] = t.slice(idx + 1).trim();
    });
    return env;
  } catch {
    return {};
  }
}

let apiBaseUrl = getAPIBaseUrl();
(async () => {
  const env = await loadFrontendEnv();
  if (env.API_BASE_URL) apiBaseUrl = env.API_BASE_URL;
  console.log("🌿 PlantCare API:", apiBaseUrl);
})();

/* ── DOM refs ──────────────────────────────────────────────────── */
const form            = document.getElementById("predict-form");
const dropZone        = document.getElementById("drop-zone");
const fileInput       = document.getElementById("image-input");
const previewImg      = document.getElementById("preview-img");
const dropPlaceholder = document.getElementById("drop-placeholder");
const fileBadge       = document.getElementById("file-badge");
const fileNameText    = document.getElementById("file-name-text");
const clearBtn        = document.getElementById("clear-btn");
const submitBtn       = document.getElementById("submit-btn");
const loadingEl       = document.getElementById("loading");
const resultBox       = document.getElementById("result");
const predictionText  = document.getElementById("prediction-text");
const confidenceText  = document.getElementById("confidence-text");
const confidenceBar   = document.getElementById("confidence-bar");
const retryBtn        = document.getElementById("retry-btn");
const errorBox        = document.getElementById("error-box");
const errorMsg        = document.getElementById("error");

/* ── State helpers ─────────────────────────────────────────────── */
function showPreview(file) {
  const url = URL.createObjectURL(file);
  previewImg.src = url;
  previewImg.classList.remove("hidden");
  dropPlaceholder.classList.add("hidden");
  dropZone.classList.add("has-image");

  fileNameText.textContent = file.name;
  fileBadge.classList.remove("hidden");

  submitBtn.disabled = false;
}

function clearAll() {
  fileInput.value       = "";
  previewImg.src        = "";
  previewImg.classList.add("hidden");
  dropPlaceholder.classList.remove("hidden");
  dropZone.classList.remove("has-image");
  fileBadge.classList.add("hidden");
  submitBtn.disabled    = true;
  hideResult();
  hideError();
}

function showLoading()  { loadingEl.classList.remove("hidden"); }
function hideLoading()  { loadingEl.classList.add("hidden"); }

function showResult(prediction, confidence) {
  predictionText.textContent = prediction;
  const pct = (confidence * 100).toFixed(1);
  confidenceText.textContent = `${pct}%`;

  resultBox.classList.remove("hidden");
  // Animate bar after paint
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      confidenceBar.style.width = `${pct}%`;
    });
  });
}

function hideResult() {
  resultBox.classList.add("hidden");
  confidenceBar.style.width = "0%";
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.classList.add("hidden");
  errorMsg.textContent = "";
}

/* ── File input change ─────────────────────────────────────────── */
fileInput.addEventListener("change", () => {
  const file = fileInput.files?.[0];
  if (file) {
    hideError();
    hideResult();
    showPreview(file);
  }
});

/* ── Drag & drop ───────────────────────────────────────────────── */
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

["dragleave", "dragend"].forEach((evt) =>
  dropZone.addEventListener(evt, () => dropZone.classList.remove("drag-over"))
);

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");

  const file = e.dataTransfer?.files?.[0];
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    showError("Please drop an image file (PNG, JPG, WEBP …).");
    return;
  }

  // Assign to native input so FormData picks it up
  const dt = new DataTransfer();
  dt.items.add(file);
  fileInput.files = dt.files;

  hideError();
  hideResult();
  showPreview(file);
});

/* ── Clear button ──────────────────────────────────────────────── */
clearBtn.addEventListener("click", clearAll);

/* ── Retry button ──────────────────────────────────────────────── */
retryBtn.addEventListener("click", clearAll);

/* ── Keyboard accessibility for drop zone ─────────────────────── */
dropZone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    fileInput.click();
  }
});

/* ── Form submit ───────────────────────────────────────────────── */
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();
  hideResult();

  const file = fileInput.files?.[0];
  if (!file) {
    showError("Please select an image first.");
    return;
  }

  submitBtn.disabled = true;
  showLoading();

  const formData = new FormData();
  formData.append("image", file);

  try {
    const url = `${apiBaseUrl}/predict`;
    console.log("📤 POST", url);

    const res  = await fetch(url, { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Prediction request failed.");

    console.log("✅ Result:", data);
    showResult(data.prediction, data.confidence);
  } catch (err) {
    console.error("❌", err);
    showError(err.message || "Could not connect to the backend.");
  } finally {
    hideLoading();
    submitBtn.disabled = false;
  }
});

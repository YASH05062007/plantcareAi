const form = document.getElementById("predict-form");
const imageInput = document.getElementById("image-input");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction-text");
const confidenceText = document.getElementById("confidence-text");
const errorText = document.getElementById("error");

const DEFAULT_API_BASE_URL = "http://localhost:8000";

function getAPIBaseUrl() {
  // Check if running in GitHub Codespaces
  if (window.location.hostname.includes("app.github.dev")) {
    // Extract the base hostname and replace port with 8000
    // e.g., "solid-space-meme-4qjxjqw695xfq7vg-5500.app.github.dev" 
    // becomes "solid-space-meme-4qjxjqw695xfq7vg-8000.app.github.dev"
    const baseHostname = window.location.hostname.replace(/-\d+\.app\.github\.dev$/, "");
    return `${window.location.protocol}//${baseHostname}-8000.app.github.dev`;
  }
  return DEFAULT_API_BASE_URL;
}

async function loadFrontendEnv() {
  try {
    const response = await fetch("./.env", { cache: "no-store" });
    if (!response.ok) {
      return {};
    }

    const text = await response.text();
    const env = {};

    text.split("\n").forEach((line) => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) {
        return;
      }

      const separatorIndex = trimmed.indexOf("=");
      const key = trimmed.slice(0, separatorIndex).trim();
      const value = trimmed.slice(separatorIndex + 1).trim();
      env[key] = value;
    });

    return env;
  } catch {
    return {};
  }
}

let apiBaseUrl = getAPIBaseUrl();

(async () => {
  const env = await loadFrontendEnv();
  if (env.API_BASE_URL) {
    apiBaseUrl = env.API_BASE_URL;
  }
  console.log("🌿 PlantCare API Base URL:", apiBaseUrl);
})();

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorText.textContent = "";
  resultBox.classList.add("hidden");

  const file = imageInput.files?.[0];
  if (!file) {
    errorText.textContent = "Please select an image file.";
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  try {
    const predictUrl = `${apiBaseUrl}/predict`;
    console.log("📤 Sending prediction request to:", predictUrl);
    
    const response = await fetch(predictUrl, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Prediction request failed.");
    }

    predictionText.textContent = data.prediction;
    confidenceText.textContent = `${(data.confidence * 100).toFixed(2)}%`;
    resultBox.classList.remove("hidden");
    console.log("✅ Prediction successful:", data);
  } catch (error) {
    console.error("❌ Error:", error);
    errorText.textContent = error.message || "Failed to connect to backend. Check console for details.";
  }
});

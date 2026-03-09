const form = document.getElementById("predict-form");
const imageInput = document.getElementById("image-input");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction-text");
const confidenceText = document.getElementById("confidence-text");
const errorText = document.getElementById("error");

const DEFAULT_API_BASE_URL = "http://localhost:8000";

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

let apiBaseUrl = DEFAULT_API_BASE_URL;

(async () => {
  const env = await loadFrontendEnv();
  apiBaseUrl = env.API_BASE_URL || DEFAULT_API_BASE_URL;
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
    const response = await fetch(`${apiBaseUrl}/predict`, {
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
  } catch (error) {
    errorText.textContent = error.message;
  }
});

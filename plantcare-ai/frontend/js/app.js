const form = document.getElementById("predict-form");
const imageInput = document.getElementById("image-input");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction-text");
const confidenceText = document.getElementById("confidence-text");
const errorText = document.getElementById("error");

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
    const response = await fetch("http://localhost:8000/predict", {
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

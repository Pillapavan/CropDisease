document.getElementById("predictBtn").addEventListener("click", predictDisease);

function predictDisease() {
  console.log("🚀 Button Clicked!");
  let imageFile = document.getElementById("imageUpload").files[0];

  if (!imageFile) {
    alert("Please upload an image before predicting.");
    return;
  }

  let formData = new FormData();
  formData.append("file", imageFile);

  console.log("✅ Sending request to backend..."); // Debug

  fetch("http://127.0.0.1:5001/predict", {
    // Change from 5500 to 5000
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("✅ Response Data:", data); // Debug
      document.getElementById("disease").innerText = "Disease: " + data.disease;
      document.getElementById("suggestion").innerText =
        "Suggestion: " + data.suggestion;
      document.getElementById("pesticide").innerText =
        "Recommended Pesticide: " + data.pesticide;
    })
    .catch((error) => console.error("❌ Error in Prediction:", error));
}

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let isDrawing = false;
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

canvas.addEventListener("mousedown", () => isDrawing = true);
canvas.addEventListener("mouseup", () => isDrawing = false);
canvas.addEventListener("mousemove", draw);

function draw(e) {
  if (!isDrawing) return;
  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(e.offsetX, e.offsetY, 15, 0, Math.PI * 2);
  ctx.fill();
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  document.getElementById("result").innerText = "";
}

function predict() {
  const resized = document.createElement("canvas");
  resized.width = 28;
  resized.height = 28;
  resized.getContext("2d").drawImage(canvas, 0, 0, 28, 28);
  
  resized.toBlob(blob => {
    const formData = new FormData();
    formData.append("image", blob, "digit.png");

    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText = `Predicted Digit: ${data.digit}`;
    });
  }, "image/png");
}

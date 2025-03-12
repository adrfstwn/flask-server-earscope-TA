const videoElement = document.getElementById("video");
const canvasElement = document.getElementById("canvas");
const ctx = canvasElement.getContext("2d");

let videoStream = null;
let sendFrames = false;
const socket = io();

function startCamera() {
  if (videoStream) return;
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      videoStream = stream;
      videoElement.srcObject = stream;
      console.log("Kamera dimulai.");
      startRecording();
    })
    .catch((err) => console.error("Gagal mengakses kamera!", err));
}

function stopCamera() {
  if (videoStream) {
    videoStream.getTracks().forEach((track) => track.stop());
    videoElement.srcObject = null;
    videoStream = null;
    console.log("Kamera dihentikan.");
  }
  // document.getElementById("popup").style.display = "block";
  stopRecording();
  document.getElementById("popup").classList.add("show");
}

function processFrames() {
  if (!sendFrames || !videoStream) return;

  canvasElement.width = videoElement.videoWidth;
  canvasElement.height = videoElement.videoHeight;
  ctx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

  const imageData = canvasElement.toDataURL("image/jpeg", 0.7);
  socket.emit("process_frame", { image: imageData });

  setTimeout(processFrames, 40);
  //requestAnimationFrame(processFrames);
}

function startRecording() {
  if (!videoStream || sendFrames) return;
  sendFrames = true;
  socket.emit("start_recording");
  console.log("Perekaman dimulai.");
  processFrames();
}

function stopRecording() {
  if (!sendFrames) return;
  sendFrames = false;
  socket.emit("stop_recording");
  console.log("Perekaman dihentikan.");
  ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
}

socket.on("processed_frame", (data) => {
  if (data.error) {
    console.error("Error dari backend:", data.error);
    return;
  }

  if (data.processed_image) {
    console.log("Menerima frame hasil proses dari backend.");
    const img = new Image();
    img.src = data.processed_image;

    img.onload = () => {
      ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      ctx.drawImage(img, 0, 0, canvasElement.width, canvasElement.height);
    };
  }
});

function resetPage() {
  location.reload();
}

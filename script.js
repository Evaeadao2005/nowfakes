// Funções para mover os sliders
let videoIndex = 0;
let priceIndex = 0;

function moveVideoSlider(direction) {
  const videos = document.getElementById('videoImages');
  const totalVideos = videos.children.length;
  videoIndex = (videoIndex + direction + totalVideos) % totalVideos;
  videos.style.transform = `translateX(-${videoIndex * 100}%)`;
}

function movePriceSlider(direction) {
  const prices = document.getElementById('priceImages');
  const totalPrices = prices.children.length;
  priceIndex = (priceIndex + direction + totalPrices) % totalPrices;
  prices.style.transform = `translateX(-${priceIndex * 100}%)`;
}
    // Exibir o popup após 3 segundos
    setTimeout(() => {
      document.getElementById("discountPopup").style.display = "block";
      startCountdown();
    }, 3000);

    // Função para fechar o popup
    function closePopup() {
      document.getElementById("discountPopup").style.display = "none";
    }

    // Função para calcular o tempo restante até 23:59 e atualizar o cronômetro
    function startCountdown() {
      const timerElement = document.getElementById("timer");

      function updateTimer() {
        const now = new Date();
        const endOfDay = new Date();
        endOfDay.setHours(23, 59, 59, 999);

        const timeRemaining = endOfDay - now;

        if (timeRemaining > 0) {
          const hours = Math.floor((timeRemaining / (1000 * 60 * 60)) % 24);
          const minutes = Math.floor((timeRemaining / (1000 * 60)) % 60);
          const seconds = Math.floor((timeRemaining / 1000) % 60);

          timerElement.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        } else {
          timerElement.textContent = "00:00:00";
        }
      }

      updateTimer();
      setInterval(updateTimer, 1000);
    }

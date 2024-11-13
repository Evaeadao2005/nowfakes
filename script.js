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
 

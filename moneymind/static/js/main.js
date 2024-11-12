(function () {
  //===== Prealoder

  window.onload = function () {
    window.setTimeout(fadeout, 2000);
  };

  function fadeout() {
    document.querySelector(".preloader").style.opacity = "1";
    document.querySelector(".preloader").style.display = "none";
  }
})();

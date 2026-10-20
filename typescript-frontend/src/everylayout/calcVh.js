const isIOSiPhone = /iPhone/.test(navigator.userAgent) && !window.MSStream;
const isSafari = !!navigator.userAgent.match(/Version\/[\d\.]+.*Safari/);
let listenerAdded = false;

function calcVh() {
  if (!isIOSiPhone || !isSafari) {
    return;
  }

  const viewportHeight = window.visualViewport?.height ?? window.innerHeight;
  document.documentElement.style.setProperty('--vh', `${viewportHeight * 0.01}px`);

  if (!listenerAdded) {
    window.addEventListener('resize', calcVh);
    listenerAdded = true;
  }
}

export function initCalcVh() {
  calcVh();
}

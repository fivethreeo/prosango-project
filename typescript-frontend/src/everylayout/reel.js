const toggleOverflowClass = elem => {
  elem.classList.toggle('overflowing', elem.scrollWidth > elem.clientWidth);
};

export function initReels() {
  const reels = document.querySelectorAll('.reel');

  for (const reel of reels) {
    toggleOverflowClass(reel);

    if ('ResizeObserver' in window) {
      new ResizeObserver((entries) => {
        toggleOverflowClass(entries[0].target);
      }).observe(reel);
    }

    if ('MutationObserver' in window) {
      new MutationObserver((entries) => {
        toggleOverflowClass(entries[0].target);
      }).observe(reel, { childList: true });
    }
  }
}
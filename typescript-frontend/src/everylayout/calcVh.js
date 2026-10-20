//const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

const isIOSiPhone = /iPhone/.test(navigator.userAgent) && !window.MSStream;

const isSafari = !!navigator.userAgent.match(/Version\/[\d\.]+.*Safari/);

const listenerAdded = false;

function calcVh() {
    // Only in safari mobile
	if (isIOSiPhone && isSafari) {
		// First we get the viewport height and we multiple it by 1% to get a value for a vh unit
		let vh = window.visualViewport.height * 0.01;
		// Then we set the value in the --vh custom property to the root of the document
		document.documentElement.style.setProperty('--vh', `${vh*1.19}px`);
		if (!listenerAdded) {
			window.addEventListener('resize', calcVh);
			listenerAdded = true;
		}
	}
}

// We listen to the resize event
// calcVh();

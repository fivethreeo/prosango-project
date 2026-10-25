(() => {
  const updatePreview = async (widget) => {
    const input = widget.querySelector('input');
    const image = widget.querySelector('img');
    const imageId = input.value.trim();

    if (!/^\d+$/.test(imageId)) {
      image.hidden = true;
      image.removeAttribute('src');
      return;
    }

    const response = await fetch(
      widget.dataset.previewUrl.replace('__image_id__', imageId),
      { credentials: 'same-origin' },
    );
    if (!response.ok) {
      image.hidden = true;
      image.removeAttribute('src');
      return;
    }

    const { url } = await response.json();
    image.src = url;
    image.hidden = false;
  };

  document.addEventListener('click', (event) => {
    const button = event.target.closest('.filer-image-preview-button');
    if (button) {
      updatePreview(button.closest('.filer-image-preview-widget'));
    }
  });

  document.addEventListener('change', (event) => {
    const widget = event.target.closest('.filer-image-preview-widget');
    if (widget) {
      updatePreview(widget);
    }
  });

  window.addEventListener('focus', () => {
    document.querySelectorAll('.filer-image-preview-widget').forEach(updatePreview);
  });
})();

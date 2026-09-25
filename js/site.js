(() => {
  const config = window.SITE_CONFIG || {};
  const phone = String(config.phone || '').replace(/[^\d+]/g, '');
  const digits = phone.replace(/\D/g, '');
  const message = encodeURIComponent(config.whatsappMessage || 'Hello, I would like to book a photography session.');
  const whatsapp = `https://web.whatsapp.com/send?phone=${digits}&text=${message}&type=phone_number&app_absent=0`;
  const map = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(config.address || '')}`;

  document.title = config.studio || document.title;
  document.querySelectorAll('.js-studio').forEach(el => el.textContent = config.studio);
  document.querySelectorAll('.js-phone').forEach(el => el.textContent = config.displayPhone || config.phone);
  document.querySelectorAll('.js-address').forEach(el => el.textContent = config.address);
  document.querySelectorAll('.js-whatsapp').forEach(el => { el.href = whatsapp; el.target = '_blank'; el.rel = 'noopener'; });
  document.querySelectorAll('.js-phone-link').forEach(el => el.href = `tel:${phone}`);
  document.querySelectorAll('.js-instagram').forEach(el => { el.href = config.instagram; el.target = '_blank'; el.rel = 'noopener'; });
  document.querySelectorAll('.js-map').forEach(el => { el.href = map; el.target = '_blank'; el.rel = 'noopener'; });
  document.getElementById('year').textContent = new Date().getFullYear();

  const button = document.querySelector('.menu-button');
  const menu = document.getElementById('main-menu');
  button.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    button.setAttribute('aria-expanded', String(open));
  });
  menu.addEventListener('click', () => { menu.classList.remove('open'); button.setAttribute('aria-expanded', 'false'); });

  const strip = document.getElementById('portfolio-strip');
  const galleryData = window.GALLERY_DATA || {};
  document.querySelectorAll('[data-gallery]').forEach(gallery => {
    const category = gallery.dataset.gallery;
    const photos = galleryData[category];
    if (!photos || !photos.length) return;
    gallery.innerHTML = photos.map((photo, index) => `
      <figure>
        <img src="${encodeURI(photo.src)}" alt="${photo.alt}" width="${photo.width}" height="${photo.height}"
          loading="${category === 'portfolio' && index < 2 ? 'eager' : 'lazy'}" decoding="async">
      </figure>`).join('');
    const heading = gallery.closest('.portfolio-category')?.querySelector('h2');
    if (heading && !heading.querySelector('.photo-count')) {
      heading.insertAdjacentHTML('beforeend', `<small class="photo-count">${photos.length} photos</small>`);
    }
  });
  if (strip) {
    document.querySelectorAll('[data-strip-direction]').forEach(control => {
      control.addEventListener('click', () => {
        const direction = control.dataset.stripDirection === 'next' ? 1 : -1;
        strip.scrollBy({ left: strip.clientWidth * .82 * direction, behavior: 'smooth' });
      });
    });
  }

  const categoryTabs = [...document.querySelectorAll('[data-category-tab]')];
  const categoryPanels = [...document.querySelectorAll('[data-category-panel]')];
  if (categoryTabs.length && categoryPanels.length) {
    const categories = new Set(categoryPanels.map(panel => panel.dataset.categoryPanel));
    const showCategory = (requested, shouldScroll = false) => {
      const category = categories.has(requested) ? requested : 'portfolio';
      categoryPanels.forEach(panel => { panel.hidden = panel.dataset.categoryPanel !== category; });
      categoryTabs.forEach(tab => {
        const active = tab.dataset.categoryTab === category;
        tab.classList.toggle('active', active);
        if (active) tab.setAttribute('aria-current', 'page');
        else tab.removeAttribute('aria-current');
      });
      if (shouldScroll) {
        document.querySelector(`[data-category-panel="${category}"]`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    };

    categoryTabs.forEach(tab => tab.addEventListener('click', event => {
      event.preventDefault();
      const category = tab.dataset.categoryTab;
      history.pushState(null, '', `#${category}`);
      showCategory(category, true);
    }));
    window.addEventListener('hashchange', () => showCategory(location.hash.slice(1), true));
    const initialCategory = location.hash.slice(1);
    showCategory(initialCategory, false);
    if (categories.has(initialCategory)) {
      requestAnimationFrame(() => document.querySelector(`[data-category-panel="${initialCategory}"]`)?.scrollIntoView({ block: 'start' }));
    }
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
  }
})();

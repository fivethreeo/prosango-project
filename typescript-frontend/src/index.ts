import { initEveryLayout } from './everylayout';
import './index.scss';

const rootEl = document.querySelector('#root');
if (rootEl) {
  rootEl.innerHTML = `
    <div class="site-shell">
      <header class="site-header container">
        <nav class="cluster cluster:between cluster:center" aria-label="Main navigation">
          <a class="brand" href="/" aria-label="Prosango home">prosango<span>.</span></a>
          <div class="nav-actions cluster cluster:center">
            <a class="text-link" href="#approach">Our approach</a>
            <a class="button button--quiet" href="#contact">Get in touch</a>
          </div>
        </nav>
      </header>

      <main>
        <section class="hero container">
          <div class="hero-copy stack">
            <p class="eyebrow">Care, in motion</p>
            <h1>Make every moment of care feel considered</h1>
            <p class="hero-intro">
              Prosango brings people, plans, and progress into one calm place
              so teams can spend more time on what matters.
            </p>
            <div class="cluster hero-actions">
              <a class="button button--primary" href="#contact">Start a conversation <span aria-hidden="true">→</span></a>
              <a class="button button--text" href="#approach">See how it works</a>
            </div>
          </div>

          <div class="hero-art" aria-hidden="true">
            <div class="orbit orbit--one"></div>
            <div class="orbit orbit--two"></div>
            <div class="care-card care-card--main stack">
              <div class="care-card__top cluster cluster:between cluster:center">
                <span class="care-card__label">Today’s focus</span>
                <span class="status-dot"></span>
              </div>
              <div>
                <p class="care-card__title">A clearer path forward</p>
                <p class="care-card__detail">Three thoughtful steps, shared by everyone who needs to know.</p>
              </div>
              <div class="progress"><span></span></div>
            </div>
            <div class="care-card care-card--note">
              <span class="note-mark">✦</span>
              <p>Small details make a meaningful difference.</p>
            </div>
          </div>
        </section>

        <section class="principles container" id="approach">
          <div class="section-heading stack">
            <p class="eyebrow">Designed for people</p>
            <h2>Care gets better when the work feels lighter.</h2>
          </div>
          <div class="grid principle-grid">
            <article class="principle-card stack">
              <span class="principle-number">01</span>
              <h3>See the whole picture</h3>
              <p>Keep the latest context, decisions, and next steps close at hand.</p>
            </article>
            <article class="principle-card stack">
              <span class="principle-number">02</span>
              <h3>Move together</h3>
              <p>Give every contributor a shared view without adding another layer of noise.</p>
            </article>
            <article class="principle-card stack">
              <span class="principle-number">03</span>
              <h3>Make space for care</h3>
              <p>Let simple, intentional tools support the human work behind every outcome.</p>
            </article>
          </div>
        </section>

        <section class="callout container" id="contact">
          <div class="callout__inner stack">
            <p class="eyebrow">A more considered way to work</p>
            <h2>Built for the moments that matter most.</h2>
            <a class="button button--light" href="mailto:hello@prosango.com">Let’s talk <span aria-hidden="true">→</span></a>
          </div>
        </section>
      </main>

      <footer class="site-footer container cluster cluster:between cluster:center">
        <a class="brand" href="/" aria-label="Prosango home">prosango<span>.</span></a>
        <p>Thoughtful systems for better care.</p>
      </footer>
    </div>
  `;

  initEveryLayout();
}

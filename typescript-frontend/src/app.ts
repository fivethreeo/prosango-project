import { initEveryLayout } from './everylayout/init';
import './index.scss';

const rootEl = document.querySelector<HTMLElement>('#root');

if (rootEl) {
  const faviconUrl = rootEl.dataset.faviconUrl;
  if (!faviconUrl) {
    throw new Error('The root element must include a favicon URL.');
  }

  rootEl.innerHTML = `
    <div class="stack space-s5">
      <header class="box box:raised padding-s1">
        <div class="center">
          <nav class="cluster cluster:between cluster:center gap-s1" aria-label="Main navigation">
            <a href="/" aria-label="Prosango home">prosango.</a>
            <div class="cluster cluster:center gap-s1">
              <a href="#approach">Approach</a>
              <a href="#principles">Principles</a>
              <a href="#contact">Contact</a>
            </div>
          </nav>
        </div>
      </header>

      <main class="stack space-s5">
        <section class="center" aria-labelledby="hero-title">
          <div class="cover box box:raised box:invert padding-s3">
            <p>Prosango / care in motion</p>
            <div class="stack space-s2" data-cover-main>
              <h1 id="hero-title">Make the next step visible to everyone involved in care.</h1>
              <p>Prosango gives people a calm place to hold context, decisions, and progress together.</p>
              <div class="cluster gap-s1">
                <a class="with-icon" href="#approach">Explore the approach <svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor"/></svg></a>
                <a href="#contact">Start a conversation</a>
              </div>
            </div>
            <p>Designed for the work between conversations.</p>
          </div>
        </section>

        <section class="center stack space-s3" id="approach" aria-labelledby="approach-title">
          <div class="with-sidebar with-sidebar:left sidebar-width-16 sidebar-min-66 gap-s2">
            <aside class="box box:raised stack padding-s1 space-s1">
              <p>01 / approach</p>
              <p>Use structure to create room for the human part of the work.</p>
            </aside>
            <div class="stack space-s2">
              <h2 id="approach-title">A shared picture makes thoughtful action easier.</h2>
              <div class="switcher switcher:max5 gap-s1">
                <span class="box box:raised box:raised--aqua padding-s-1">Clear context</span>
                <span class="box box:raised padding-s-1">Shared momentum</span>
                <span class="box box:raised box:raised--sun padding-s-1">Thoughtful detail</span>
              </div>
            </div>
          </div>

          <div class="grid grid-min-16 gap-s1">
            <article class="box box:raised stack padding-s1 space-s1">
              <p>01</p>
              <h3>See the whole picture</h3>
              <p>Keep the latest context, decisions, and next steps close at hand.</p>
            </article>
            <article class="box box:raised stack padding-s1 space-s1">
              <p>02</p>
              <h3>Move together</h3>
              <p>Give every contributor a shared view without adding more noise.</p>
            </article>
            <article class="box box:raised stack padding-s1 space-s1">
              <p>03</p>
              <h3>Make room for care</h3>
              <p>Let simple tools support the human work behind every outcome.</p>
            </article>
          </div>
        </section>

        <section class="center stack space-s3" id="principles" aria-labelledby="principles-title">
          <div class="with-sidebar with-sidebar:right sidebar-width-20 sidebar-min-66 gap-s2">
            <div class="stack space-s1">
              <p>02 / in practice</p>
              <h2 id="principles-title">A rhythm that holds up from first note to next action.</h2>
            </div>
            <div class="imposter-container frame">
              <img src="${faviconUrl}" alt="">
              <p class="imposter box box:raised box:raised--sun padding-s0">Care<br>in flow</p>
            </div>
          </div>

          <div class="reel" aria-label="Prosango principles">
            <article class="box box:raised stack padding-s1 space-s1">
              <p>Context</p>
              <h3>Let the work carry its history.</h3>
              <p>Make decisions legible to the people who need them next.</p>
            </article>
            <article class="box box:raised box:invert stack padding-s1 space-s1">
              <p>Attention</p>
              <h3>Keep the important things close.</h3>
              <p>Small prompts help teams notice what changes the outcome.</p>
            </article>
            <article class="box box:raised stack padding-s1 space-s1">
              <p>Momentum</p>
              <h3>Turn insight into a next step.</h3>
              <p>Progress becomes easier when each handoff has a clear shape.</p>
            </article>
          </div>
          <p class="instruction">Scroll horizontally to see more.</p>
        </section>

        <section class="center" id="contact" aria-labelledby="contact-title">
          <div class="cover box box:raised padding-s3">
            <p>03 / begin</p>
            <div class="stack space-s1" data-cover-main>
              <h2 id="contact-title">Build a more considered way to work.</h2>
              <p>Tell us where the work is getting harder than it needs to be.</p>
              <a class="with-icon" href="mailto:hello@prosango.com">hello@prosango.com <svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor"/></svg></a>
            </div>
            <p>Thoughtful systems for better care.</p>
          </div>
        </section>
      </main>

      <footer class="box box:raised padding-s1">
        <div class="center">
          <div class="cluster cluster:between cluster:center gap-s1">
            <a href="/" aria-label="Prosango home">prosango.</a>
            <p>Care, in motion.</p>
          </div>
        </div>
      </footer>
    </div>
  `;

  initEveryLayout();
}

import './everylayout.scss';
import { initCalcVh } from './everylayout/calcVh.js';
import { initReels } from './everylayout/reel.js';

export function initEveryLayout() {
  initCalcVh();
  initReels();
}

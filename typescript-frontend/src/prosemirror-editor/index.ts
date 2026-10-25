import { DOMParser, DOMSerializer } from 'prosemirror-model';
import { EditorState } from 'prosemirror-state';
import { EditorView } from 'prosemirror-view';
import 'prosemirror-view/style/prosemirror.css';
import 'prosemirror-menu/style/menu.css';
import 'prosemirror-example-setup/style/style.css';
import '../../prosemirror-breadcrumbs/style/breadcrumbs.css';
import { prosangoSchema, prosangoSrt } from './setup';

function saveEditorOutput(editor: EditorView, element: HTMLTextAreaElement) {
  const output = document.createElement('div');
  output.append(
    DOMSerializer.fromSchema(prosangoSchema).serializeFragment(editor.state.doc.content),
  );
  element.value = output.innerHTML;
  element.dispatchEvent(new Event('input', { bubbles: true }));
}

export function setupEditor(element: HTMLTextAreaElement): EditorView {
  const content = document.createElement('div');
  content.innerHTML = element.value;

  const editorElement = document.createElement('div');
  editorElement.className = 'editor';
  element.insertAdjacentElement('afterend', editorElement);
  element.hidden = true;

  let editor: EditorView;
  editor = new EditorView(editorElement, {
    state: EditorState.create({
      doc: DOMParser.fromSchema(prosangoSchema).parse(content),
      plugins: prosangoSrt(),
    }),
    dispatchTransaction(transaction) {
      const state = editor.state.apply(transaction);
      editor.updateState(state);
      saveEditorOutput(editor, element);
    },
  });
  return editor;
}

function initializeEditors() {
  document
    .querySelectorAll<HTMLTextAreaElement>('[data-prosemirror]')
    .forEach(setupEditor);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeEditors);
} else {
  initializeEditors();
}

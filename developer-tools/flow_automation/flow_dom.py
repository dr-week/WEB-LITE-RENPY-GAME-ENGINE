"""DOM inspection and Reuse-Prompt automation scripts for Google Flow."""

import json

INSPECT_JS = """(() => {
  const input = document.querySelector('textarea, [contenteditable="true"][role="textbox"], [contenteditable="true"]');
  const buttons = [...document.querySelectorAll('button')];
  const reuse = buttons.filter(b => /reuse|prompt|undo|reply/i.test((b.getAttribute('aria-label') || '') + ' ' + (b.title || '') + ' ' + (b.innerText || '')));
  const send = buttons.find(b => b.type === 'submit' || /send|submit|generate|arrow/i.test((b.getAttribute('aria-label') || '') + ' ' + (b.title || '')));
  return {
    url: location.href,
    title: document.title,
    hasInput: Boolean(input),
    inputTag: input ? input.tagName : null,
    reuseCount: reuse.length,
    reuseLabels: reuse.slice(0, 5).map(b => b.getAttribute('aria-label') || b.title || b.innerText.trim()),
    hasSend: Boolean(send),
  };
})()"""

CLICK_REUSE_JS = """(() => {
  const buttons = [...document.querySelectorAll('button')];
  const btn = buttons.find(b => /reuse/i.test((b.getAttribute('aria-label') || '') + ' ' + (b.title || '') + ' ' + (b.innerText || '')));
  if (!btn) return {clicked: false, reason: 'reuse_button_not_found'};
  btn.scrollIntoView({block: 'center'});
  btn.click();
  return {clicked: true, label: btn.getAttribute('aria-label') || btn.title || 'reuse'};
})()"""

CLICK_SEND_JS = """(() => {
  const buttons = [...document.querySelectorAll('button')];
  const btn = buttons.find(b => !b.disabled && (b.type === 'submit' || /send|submit|generate/i.test((b.getAttribute('aria-label') || '') + ' ' + (b.title || ''))));
  if (!btn) return {submitted: false, reason: 'send_button_not_found'};
  btn.click();
  return {submitted: true};
})()"""


def build_set_prompt_js(text: str) -> str:
    """Return JS that selects all and replaces the Flow chat input cleanly for React."""
    encoded = json.dumps(text)
    return f"""(() => {{
  const el = document.querySelector('textarea, [contenteditable="true"][role="textbox"], [contenteditable="true"]');
  if (!el) return {{ok: false, reason: 'input_not_found'}};
  el.focus();
  const val = {encoded};
  if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {{
    const setter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value')?.set;
    if (setter) setter.call(el, val); else el.value = val;
    el.dispatchEvent(new Event('input', {{bubbles: true}}));
    el.dispatchEvent(new Event('change', {{bubbles: true}}));
  }} else {{
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, val);
  }}
  return {{ok: true, length: val.length}};
}})()"""

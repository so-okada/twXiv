// ==UserScript==
// @name        arXiv Linkifier for X.com
// @namespace   https://arxiv.org/
// @match       https://x.com/*
// @match       https://twitter.com/*
// @grant       none
// @version     1.1
// @description Turn arXiv:YYMM.NNNNN into clickable links on X.com. This userscript is a part of twXiv project: https://github.com/so-okada/twXiv
// ==/UserScript==

(function () {
  'use strict';

  // Matches arXiv:YYMM.NNNNN (with optional vN version suffix)
  const ARXIV_RE = /arXiv:\d{4}\.\d{4,5}(?:v\d+)?/g;

  function linkifyTextNode(textNode) {
    const text = textNode.nodeValue;
    if (!ARXIV_RE.test(text)) return;
    ARXIV_RE.lastIndex = 0; // reset after .test()

    const frag = document.createDocumentFragment();
    let lastIndex = 0;
    let match;

    while ((match = ARXIV_RE.exec(text)) !== null) {
      // text before the match
      if (match.index > lastIndex) {
        frag.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
      }
      // the link
      const id = match[0].slice(6); // strip "arXiv:"
      const a = document.createElement('a');
      a.href = `https://arxiv.org/abs/${id}`;
      a.textContent = match[0];
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.style.cssText = 'color: #1d9bf0; text-decoration: underline;';
      frag.appendChild(a);
      lastIndex = ARXIV_RE.lastIndex;
    }

    if (lastIndex < text.length) {
      frag.appendChild(document.createTextNode(text.slice(lastIndex)));
    }

    textNode.parentNode.replaceChild(frag, textNode);
  }

  function processNode(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        // Skip if already inside a link, script, style, or editable area
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (parent.closest('a, script, style, textarea, [contenteditable="true"]')) {
          return NodeFilter.FILTER_REJECT;
        }
        const hasMatch = ARXIV_RE.test(node.nodeValue);
        ARXIV_RE.lastIndex = 0; // reset after .test()
        return hasMatch
          ? NodeFilter.FILTER_ACCEPT
          : NodeFilter.FILTER_REJECT;
      },
    });

    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // Process collected nodes (can't mutate DOM during walk)
    nodes.forEach(linkifyTextNode);
  }

  // Initial pass
  processNode(document.body);

  // Watch for dynamically loaded tweets
  const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          processNode(node);
        }
      }
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
})();

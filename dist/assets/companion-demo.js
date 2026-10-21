/*
 * Offline illustrated case study: not an AI model or a hosted companion.
 * Fictional records, no network requests, no storage, no personal data.
 */
(() => {
  "use strict";
  const root = document.querySelector("[data-companion-demo]");
  if (!root) return;
  const buttons = Array.from(root.querySelectorAll("[data-demo-choice]"));
  const target = root.querySelector("[data-demo-response]");
  if (!target) return;
  const scenarios = {
    handoff: {
      title: "A handoff grounded in records",
      known: [
        "Record A, board decision: a trial at one help desk location was approved.",
        "Record B, privacy review: personal case information cannot be used externally without additional approval."
      ],
      uncertain: ["Record C mentions wider rollout, but contains no approval or named decision-maker."],
      next: "Tell the successor what is documented, keep the expansion marked unapproved, and identify who can make the next decision."
    },
    challenge: {
      title: "A correction is not automatically a fact",
      known: ["Record A only authorizes the one-site trial. No signed expansion decision appears in the fictional record."],
      uncertain: ["The colleague may have new evidence, but the source and authority have not been checked."],
      next: "Request the decision record and its owner. Keep the claim as a proposed correction until it can be verified; do not quietly rewrite the history."
    },
    next: {
      title: "Leave decisions with the people responsible",
      known: ["The approved trial is limited to one location (Record A). The privacy condition remains open (Record B)."],
      uncertain: ["No record confirms whether the proposed expansion was approved (Record C)."],
      next: "Ask the incoming lead to confirm ownership, obtain the privacy decision, and agree on next steps before any broader rollout."
    }
  };
  function element(tag, content, cls) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (content) el.textContent = content;
    return el;
  }
  function group(title, values) {
    target.append(element("h4", title));
    const list = element("ul");
    values.forEach(value => list.append(element("li", value)));
    target.append(list);
  }
  function show(key) {
    const data = scenarios[key];
    if (!data) return;
    buttons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.demoChoice === key)));
    target.replaceChildren();
    target.append(element("h3", data.title));
    group("Supported by the fictional record", data.known);
    group("Not yet established", data.uncertain);
    target.append(element("h4", "Suggested next step"));
    target.append(element("p", data.next));
    target.append(element("p", "Illustration only · no live AI analysis", "demo-small"));
  }
  buttons.forEach(button => {
    button.setAttribute("aria-pressed", "false");
    button.addEventListener("click", () => show(button.dataset.demoChoice));
  });
})();

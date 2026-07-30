(() => {
  'use strict';

  const survey = window.QW_DISCOVERY_SURVEY;
  if (!survey || survey.schema !== 'quietwire.discovery.survey') {
    document.body.innerHTML = '<main style="padding:2rem;font-family:sans-serif"><h1>Discovery data could not be loaded.</h1><p>No answers were collected or transmitted.</p></main>';
    return;
  }

  const allQuestions = survey.sections.flatMap(section => section.questions.map(question => ({ ...question, section })));
  const questionById = new Map(allQuestions.map(question => [question.id, question]));
  const sectionById = new Map(survey.sections.map(section => [section.id, section]));

  const state = {
    path: null,
    selectedRole: null,
    selectedAreas: [],
    activeSectionIds: [],
    activeQuestionIds: [],
    currentSectionId: null,
    currentView: 'questions',
    answers: {},
    sessionStartedAt: null,
    sourceFileName: null
  };

  const pages = [...document.querySelectorAll('.page')];
  const welcome = document.getElementById('welcome');
  const guidedSetup = document.getElementById('guided-setup');
  const workspace = document.getElementById('workspace');
  const sectionList = document.getElementById('section-list');
  const questionsView = document.getElementById('questions-view');
  const reviewView = document.getElementById('review-view');
  const privacyView = document.getElementById('privacy-view');
  const searchInput = document.getElementById('question-search');
  const workingFileInput = document.getElementById('working-file-input');
  const navToggle = document.querySelector('[data-nav-toggle]');
  const siteNav = document.querySelector('[data-nav]');

  function closeNavigation() {
    document.body.classList.remove('nav-open');
    navToggle.setAttribute('aria-expanded', 'false');
  }

  navToggle.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  siteNav.addEventListener('click', event => {
    if (event.target.closest('a')) closeNavigation();
  });

  function showPage(id) {
    pages.forEach(page => page.classList.toggle('active', page.id === id));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function escapeHtml(value = '') {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function nowIso() {
    return new Date().toISOString();
  }

  function humanDate(value) {
    if (!value) return '';
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
  }

  function slug(value) {
    return String(value).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  function ensureAnswer(id) {
    if (!state.answers[id]) {
      state.answers[id] = {
        status: '',
        response: '',
        owner: '',
        target_date: '',
        evidence: '',
        phase: '',
        notes: '',
        updated_at: nowIso()
      };
    }
    return state.answers[id];
  }

  function isAnswered(answer) {
    return Boolean(answer && (answer.status || answer.response.trim() || answer.owner.trim() || answer.notes.trim()));
  }

  function activeQuestions() {
    return state.activeQuestionIds.map(id => questionById.get(id)).filter(Boolean);
  }

  function configurePath(path, role = null, areas = []) {
    state.path = path;
    state.selectedRole = role;
    state.selectedAreas = [...areas];
    state.sessionStartedAt ||= nowIso();

    if (path === 'quick') {
      state.activeQuestionIds = survey.quick_question_ids.filter(id => questionById.has(id));
      state.activeSectionIds = [...new Set(state.activeQuestionIds.map(id => questionById.get(id).section.id))];
    } else if (path === 'guided') {
      const selected = survey.sections.filter(section => {
        const roleMatch = role ? section.roles.includes(role) : false;
        const areaMatch = areas.length ? areas.some(area => section.areas.includes(area)) : false;
        return roleMatch || areaMatch;
      });
      const fallback = selected.length ? selected : survey.sections.slice(0, 3);
      state.activeSectionIds = fallback.map(section => section.id);
      state.activeQuestionIds = fallback.flatMap(section => section.questions.map(question => question.id));
    } else {
      state.activeSectionIds = survey.sections.map(section => section.id);
      state.activeQuestionIds = allQuestions.map(question => question.id);
    }

    state.currentSectionId = state.activeSectionIds[0] || null;
    searchInput.value = '';
    showPage('workspace');
    renderWorkspace();
  }

  function renderGuidedOptions() {
    const roleOptions = document.getElementById('role-options');
    const areaOptions = document.getElementById('area-options');

    roleOptions.innerHTML = Object.entries(survey.roles).map(([id, role]) => `
      <label class="choice">
        <input type="radio" name="primary-role" value="${escapeHtml(id)}">
        <span><strong>${escapeHtml(role.label)}</strong><span>${escapeHtml(role.description)}</span></span>
      </label>`).join('');

    const preferredAreas = ['strategy','people','customers','sales','field','products','equipment','inventory','quality','maintenance','finance','digital','reporting','data','integrations','cap','privacy','ai-governance','technology','workflow','pilot'];
    areaOptions.innerHTML = preferredAreas.filter(id => survey.areas[id]).map(id => `
      <label class="choice">
        <input type="checkbox" name="interest-area" value="${escapeHtml(id)}">
        <span><strong>${escapeHtml(survey.areas[id])}</strong></span>
      </label>`).join('');
  }

  function renderWorkspace() {
    renderSectionList();
    renderCurrentView();
    updateProgress();
  }

  function renderSectionList() {
    const current = state.currentSectionId;
    const answeredBySection = new Map();
    state.activeSectionIds.forEach(sectionId => {
      const section = sectionById.get(sectionId);
      const applicable = section.questions.filter(q => state.activeQuestionIds.includes(q.id));
      const answered = applicable.filter(q => isAnswered(state.answers[q.id])).length;
      answeredBySection.set(sectionId, `${answered}/${applicable.length}`);
    });

    sectionList.innerHTML = state.activeSectionIds.map(sectionId => {
      const section = sectionById.get(sectionId);
      return `<button class="section-button ${current === sectionId ? 'active' : ''}" data-section-id="${sectionId}">
        <span class="section-number">${sectionId}</span>
        <span>${escapeHtml(section.title)}</span>
        <span class="section-count">${answeredBySection.get(sectionId)}</span>
      </button>`;
    }).join('');
  }

  function renderCurrentView() {
    document.querySelectorAll('.workspace-view').forEach(view => view.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(tab => {
      const active = tab.dataset.view === state.currentView;
      tab.classList.toggle('active', active);
      tab.setAttribute('aria-selected', String(active));
    });

    if (state.currentView === 'review') {
      reviewView.classList.add('active');
      renderReview();
      return;
    }
    if (state.currentView === 'privacy') {
      privacyView.classList.add('active');
      renderPrivacy();
      return;
    }

    questionsView.classList.add('active');
    renderQuestions();
  }

  function renderQuestions() {
    const term = searchInput.value.trim().toLowerCase();
    if (term) {
      const results = activeQuestions().filter(question =>
        question.id.toLowerCase().includes(term) ||
        question.prompt.toLowerCase().includes(term) ||
        question.section.title.toLowerCase().includes(term)
      );
      questionsView.innerHTML = `
        <header class="section-header">
          <p class="eyebrow">Search results</p>
          <h1>${results.length} question${results.length === 1 ? '' : 's'} found</h1>
          <p>Search is performed locally in this page. The search text and results are not transmitted.</p>
        </header>
        <div class="question-stack">${results.length ? results.map(renderQuestionCard).join('') : '<p class="empty-state">No questions match this search.</p>'}</div>`;
      return;
    }

    const section = sectionById.get(state.currentSectionId);
    if (!section) {
      questionsView.innerHTML = '<p class="empty-state">No section is selected.</p>';
      return;
    }
    const questions = section.questions.filter(question => state.activeQuestionIds.includes(question.id));
    questionsView.innerHTML = `
      <header class="section-header">
        <p class="eyebrow">Section ${escapeHtml(section.id)} · ${questions.length} question${questions.length === 1 ? '' : 's'}</p>
        <h1>${escapeHtml(section.title)}</h1>
        <p>${escapeHtml(section.description)}</p>
      </header>
      <div class="question-stack">${questions.map(renderQuestionCard).join('')}</div>`;
  }

  function renderQuestionCard(question) {
    const answer = state.answers[question.id] || { status:'', response:'', owner:'', target_date:'', evidence:'', phase:'', notes:'' };
    const statuses = [
      ['confirmed','Confirmed'],
      ['unresolved','Unresolved'],
      ['not_applicable','Not applicable'],
      ['skipped','Skipped']
    ];
    return `<article class="question-card ${isAnswered(answer) ? 'answered' : ''}" data-question-id="${question.id}">
      <div class="question-topline">
        <span class="question-id">${escapeHtml(question.id)}</span>
        <span class="question-type">${escapeHtml(question.response_type)}</span>
      </div>
      <h3>${escapeHtml(question.prompt)}</h3>
      <div class="status-options" role="radiogroup" aria-label="Decision status for question ${question.id}">
        ${statuses.map(([value,label]) => `<label class="status-pill"><input type="radio" name="status-${question.id}" value="${value}" ${answer.status === value ? 'checked' : ''}>${label}</label>`).join('')}
      </div>
      <label class="response-label">Response or details
        <textarea data-field="response" placeholder="Write only what is useful. It is acceptable to leave this blank.">${escapeHtml(answer.response)}</textarea>
      </label>
      <button class="metadata-toggle" type="button" aria-expanded="${answer.owner || answer.target_date || answer.evidence || answer.phase || answer.notes ? 'true' : 'false'}">${answer.owner || answer.target_date || answer.evidence || answer.phase || answer.notes ? 'Hide' : 'Add'} owner, evidence, phase, or notes</button>
      <div class="metadata-grid" ${answer.owner || answer.target_date || answer.evidence || answer.phase || answer.notes ? '' : 'hidden'}>
        <label>Decision owner<input data-field="owner" value="${escapeHtml(answer.owner)}" autocomplete="off"></label>
        <label>Target decision date<input data-field="target_date" type="date" value="${escapeHtml(answer.target_date)}"></label>
        <label>Evidence or source<input data-field="evidence" value="${escapeHtml(answer.evidence)}" autocomplete="off"></label>
        <label>Implementation phase<select data-field="phase">
          <option value="">Not selected</option>
          ${['Pilot','Phase 1','Phase 2','Later'].map(value => `<option value="${value}" ${answer.phase === value ? 'selected' : ''}>${value}</option>`).join('')}
        </select></label>
        <label class="wide">Notes<textarea data-field="notes">${escapeHtml(answer.notes)}</textarea></label>
      </div>
    </article>`;
  }

  function updateAnswerFromCard(card, field, value) {
    const id = card.dataset.questionId;
    const answer = ensureAnswer(id);
    answer[field] = value;
    answer.updated_at = nowIso();
    card.classList.toggle('answered', isAnswered(answer));
    updateProgress();
    renderSectionList();
  }

  function updateProgress() {
    const questions = activeQuestions();
    const answered = questions.filter(question => isAnswered(state.answers[question.id])).length;
    const total = questions.length;
    const percent = total ? Math.round((answered / total) * 100) : 0;
    document.getElementById('progress-text').textContent = `${answered} of ${total} answered`;
    document.getElementById('progress-percent').textContent = `${percent}%`;
    document.getElementById('progress-bar').style.width = `${percent}%`;
  }

  function statusLabel(value) {
    return ({ confirmed:'Confirmed', unresolved:'Unresolved', not_applicable:'Not applicable', skipped:'Skipped' })[value] || 'No status';
  }

  function reviewMetrics() {
    const questions = activeQuestions();
    const entries = questions.map(question => ({ question, answer: state.answers[question.id] })).filter(item => isAnswered(item.answer));
    return {
      total: questions.length,
      answered: entries.length,
      confirmed: entries.filter(item => item.answer.status === 'confirmed').length,
      unresolved: entries.filter(item => item.answer.status === 'unresolved').length,
      notApplicable: entries.filter(item => item.answer.status === 'not_applicable').length,
      skipped: entries.filter(item => item.answer.status === 'skipped').length,
      entries
    };
  }

  function renderReview() {
    const metrics = reviewMetrics();
    const unresolved = metrics.entries.filter(item => item.answer.status === 'unresolved');
    const substantive = metrics.entries.filter(item => item.answer.status !== 'not_applicable' && item.answer.status !== 'skipped');
    const pathName = state.path === 'quick' ? 'Quick orientation' : state.path === 'guided' ? 'Guided discovery' : 'Full discovery';

    reviewView.innerHTML = `
      <div class="review-hero">
        <p class="eyebrow">Local review · nothing has been sent</p>
        <h1>Discovery working summary</h1>
        <p><strong>Path:</strong> ${escapeHtml(pathName)} · <strong>Survey:</strong> ${escapeHtml(survey.title)} · <strong>Generated:</strong> ${escapeHtml(new Date().toLocaleString())}</p>
        <p>This review is assembled inside the browser from the current session. It is not an assessment, decision, or QuietWire recommendation.</p>
      </div>
      <div class="review-grid">
        <div class="metric"><strong>${metrics.answered}</strong><span>questions touched</span></div>
        <div class="metric"><strong>${metrics.confirmed}</strong><span>confirmed</span></div>
        <div class="metric"><strong>${metrics.unresolved}</strong><span>unresolved</span></div>
      </div>
      <section class="review-section">
        <h2>Open decisions</h2>
        <div class="review-list">${unresolved.length ? unresolved.map(renderReviewItem).join('') : '<p class="empty-state">No questions are currently marked unresolved.</p>'}</div>
      </section>
      <section class="review-section">
        <h2>Answered and confirmed material</h2>
        <div class="review-list">${substantive.length ? substantive.map(renderReviewItem).join('') : '<p class="empty-state">No substantive answers have been entered yet.</p>'}</div>
      </section>
      <section class="review-section">
        <h2>Architectural boundary</h2>
        <div class="code-note">${survey.principles.map(escapeHtml).join('<br><br>')}</div>
      </section>`;
  }

  function renderReviewItem(item) {
    const { question, answer } = item;
    const details = [
      answer.response,
      answer.owner ? `Owner: ${answer.owner}` : '',
      answer.target_date ? `Target: ${answer.target_date}` : '',
      answer.evidence ? `Evidence/source: ${answer.evidence}` : '',
      answer.phase ? `Phase: ${answer.phase}` : '',
      answer.notes ? `Notes: ${answer.notes}` : ''
    ].filter(Boolean).join('\n');
    return `<article class="review-item">
      <strong>${escapeHtml(question.id)} · ${escapeHtml(question.section.title)} · ${escapeHtml(statusLabel(answer.status))}</strong>
      <p>${escapeHtml(question.prompt)}</p>
      ${details ? `<p>${escapeHtml(details)}</p>` : ''}
    </article>`;
  }

  function renderPrivacy() {
    privacyView.innerHTML = `
      <div class="privacy-view-content">
        <p class="eyebrow">Current custody boundary</p>
        <h1>Your answers are still here—not at QuietWire.</h1>
        <p>This candidate is intentionally static and local-first. It contains no account system, form endpoint, database, advertising tracker, behavioural analytics, or third-party JavaScript.</p>
        <div class="privacy-ledger">
          <article><h2>Answers held now</h2><p>In JavaScript memory inside this open browser tab. Refreshing or closing the page clears unsaved work.</p></article>
          <article><h2>Automatic browser persistence</h2><p>Off. This application does not use localStorage, sessionStorage, IndexedDB, cookies, or a service worker for answers.</p></article>
          <article><h2>Network transmission</h2><p>Blocked by design. The Content Security Policy sets <code>connect-src 'none'</code> and <code>form-action 'none'</code>.</p></article>
          <article><h2>Saving your work</h2><p>“Save to this device” creates a local file through the browser. It may contain sensitive organizational information and remains your responsibility to protect.</p></article>
          <article><h2>Sharing</h2><p>No direct-send function exists in this release. Sharing a downloaded copy is a separate deliberate act outside the application.</p></article>
          <article><h2>Server logs</h2><p>The web server may observe an ordinary page request, such as time, network address, and requested static files. It does not receive the answers typed into the page.</p></article>
        </div>
      </div>`;
  }

  function workingPackage() {
    return {
      schema: 'quietwire.discovery.responses',
      schema_version: '1.0',
      survey_id: survey.survey_id,
      survey_version: survey.survey_version,
      created_at: state.sessionStartedAt || nowIso(),
      updated_at: nowIso(),
      path: state.path,
      selected_role: state.selectedRole,
      selected_areas: state.selectedAreas,
      active_section_ids: state.activeSectionIds,
      active_question_ids: state.activeQuestionIds,
      answers: state.answers,
      custody_notice: 'Created locally in the user browser. QuietWire did not receive this working file through the discovery application.'
    };
  }

  function downloadText(filename, text, type) {
    const blob = new Blob([text], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function saveWorkingFile() {
    const date = new Date().toISOString().slice(0, 10);
    downloadText(`quietwire-discovery-${date}.qwd.json`, JSON.stringify(workingPackage(), null, 2), 'application/json');
  }

  function reportHtml() {
    const metrics = reviewMetrics();
    const pathName = state.path === 'quick' ? 'Quick orientation' : state.path === 'guided' ? 'Guided discovery' : 'Full discovery';
    const items = metrics.entries.map(item => {
      const answer = item.answer;
      return `<section class="item"><h3>${escapeHtml(item.question.id)} · ${escapeHtml(item.question.section.title)}</h3><h4>${escapeHtml(item.question.prompt)}</h4><p><b>Status:</b> ${escapeHtml(statusLabel(answer.status))}</p>${answer.response ? `<p>${escapeHtml(answer.response).replaceAll('\n','<br>')}</p>` : ''}<dl>${answer.owner ? `<dt>Owner</dt><dd>${escapeHtml(answer.owner)}</dd>` : ''}${answer.target_date ? `<dt>Target date</dt><dd>${escapeHtml(answer.target_date)}</dd>` : ''}${answer.evidence ? `<dt>Evidence/source</dt><dd>${escapeHtml(answer.evidence)}</dd>` : ''}${answer.phase ? `<dt>Phase</dt><dd>${escapeHtml(answer.phase)}</dd>` : ''}${answer.notes ? `<dt>Notes</dt><dd>${escapeHtml(answer.notes).replaceAll('\n','<br>')}</dd>` : ''}</dl></section>`;
    }).join('');
    return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>QuietWire Discovery Report</title><style>body{font-family:Georgia,serif;max-width:850px;margin:40px auto;padding:0 24px;color:#173338;line-height:1.5}h1{font-size:2.5rem}h2,h3{color:#102f34}.notice{background:#eef6f3;border:1px solid #afc0bc;border-radius:12px;padding:16px}.metrics{display:flex;gap:12px;flex-wrap:wrap}.metrics span{padding:10px 14px;background:#f8f3e8;border-radius:999px}.item{border-top:1px solid #d7dfdc;padding:18px 0;break-inside:avoid}.item h3{font-size:.9rem;color:#2f766f}.item h4{font-size:1.15rem;margin:.4rem 0}dl{display:grid;grid-template-columns:130px 1fr;gap:4px 12px}dt{font-weight:bold}dd{margin:0}@media print{@page{size:letter;margin:.65in}body{margin:0;max-width:none}}</style></head><body><p>QuietWire</p><h1>Discovery working report</h1><p><b>Path:</b> ${escapeHtml(pathName)}<br><b>Survey:</b> ${escapeHtml(survey.title)}<br><b>Generated:</b> ${escapeHtml(new Date().toLocaleString())}</p><div class="notice"><b>Custody notice:</b> This report was generated locally in the browser. The discovery application did not transmit its contents to QuietWire.</div><div class="metrics"><span>${metrics.answered} touched</span><span>${metrics.confirmed} confirmed</span><span>${metrics.unresolved} unresolved</span></div><h2>Responses</h2>${items || '<p>No responses were entered.</p>'}<h2>Architectural boundary</h2>${survey.principles.map(p => `<p>${escapeHtml(p)}</p>`).join('')}</body></html>`;
  }

  function downloadReport() {
    const date = new Date().toISOString().slice(0, 10);
    downloadText(`quietwire-discovery-report-${date}.html`, reportHtml(), 'text/html');
  }

  function loadWorkingFile(file) {
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert('This working file is larger than the five-megabyte safety limit. Nothing was uploaded.');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result);
        if (data.schema !== 'quietwire.discovery.responses' || data.schema_version !== '1.0') throw new Error('Unsupported working-file schema.');
        if (data.survey_id !== survey.survey_id) throw new Error('This working file belongs to a different discovery edition.');
        const safeAnswers = {};
        Object.entries(data.answers || {}).forEach(([id, answer]) => {
          if (!questionById.has(id) || typeof answer !== 'object' || !answer) return;
          safeAnswers[id] = {
            status: ['confirmed','unresolved','not_applicable','skipped',''].includes(answer.status) ? answer.status : '',
            response: String(answer.response || '').slice(0, 20000),
            owner: String(answer.owner || '').slice(0, 500),
            target_date: String(answer.target_date || '').slice(0, 20),
            evidence: String(answer.evidence || '').slice(0, 2000),
            phase: ['Pilot','Phase 1','Phase 2','Later',''].includes(answer.phase) ? answer.phase : '',
            notes: String(answer.notes || '').slice(0, 10000),
            updated_at: String(answer.updated_at || nowIso()).slice(0, 50)
          };
        });
        state.answers = safeAnswers;
        state.sessionStartedAt = data.created_at || nowIso();
        state.sourceFileName = file.name;
        const path = ['quick','guided','full'].includes(data.path) ? data.path : 'full';
        configurePath(path, data.selected_role || null, Array.isArray(data.selected_areas) ? data.selected_areas : []);
      } catch (error) {
        alert(`The selected file could not be opened: ${error.message}\n\nNothing was uploaded or transmitted.`);
      }
    };
    reader.onerror = () => alert('The file could not be read. Nothing was uploaded or transmitted.');
    reader.readAsText(file);
  }

  document.querySelectorAll('[data-start-path]').forEach(button => {
    button.addEventListener('click', () => {
      const path = button.dataset.startPath;
      if (path === 'guided') {
        showPage('guided-setup');
      } else {
        configurePath(path);
      }
    });
  });

  document.querySelectorAll('[data-go-home]').forEach(button => button.addEventListener('click', () => showPage('welcome')));

  document.getElementById('begin-guided').addEventListener('click', () => {
    const role = document.querySelector('input[name="primary-role"]:checked')?.value || null;
    const areas = [...document.querySelectorAll('input[name="interest-area"]:checked')].map(input => input.value);
    if (!role && areas.length === 0) {
      alert('Choose a role or at least one area of interest.');
      return;
    }
    configurePath('guided', role, areas);
  });

  sectionList.addEventListener('click', event => {
    const button = event.target.closest('[data-section-id]');
    if (!button) return;
    state.currentSectionId = button.dataset.sectionId;
    state.currentView = 'questions';
    searchInput.value = '';
    renderWorkspace();
    document.querySelector('.workspace-main').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  document.querySelector('.workspace-main').addEventListener('input', event => {
    const card = event.target.closest('.question-card');
    if (!card) return;
    if (event.target.matches('input[type="radio"]')) updateAnswerFromCard(card, 'status', event.target.value);
    if (event.target.dataset.field) updateAnswerFromCard(card, event.target.dataset.field, event.target.value);
  });

  document.querySelector('.workspace-main').addEventListener('click', event => {
    const toggle = event.target.closest('.metadata-toggle');
    if (!toggle) return;
    const grid = toggle.nextElementSibling;
    const willOpen = grid.hasAttribute('hidden');
    grid.toggleAttribute('hidden', !willOpen);
    toggle.setAttribute('aria-expanded', String(willOpen));
    toggle.textContent = `${willOpen ? 'Hide' : 'Add'} owner, evidence, phase, or notes`;
  });

  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      state.currentView = tab.dataset.view;
      renderCurrentView();
    });
  });

  searchInput.addEventListener('input', () => {
    state.currentView = 'questions';
    renderCurrentView();
  });

  document.getElementById('save-working-file').addEventListener('click', saveWorkingFile);
  document.getElementById('download-report').addEventListener('click', downloadReport);
  document.getElementById('print-report').addEventListener('click', () => {
    state.currentView = 'review';
    renderCurrentView();
    setTimeout(() => window.print(), 80);
  });
  document.getElementById('clear-session').addEventListener('click', () => {
    if (!confirm('Clear every answer in this open browser session? This cannot be undone unless you already downloaded a working file.')) return;
    state.answers = {};
    state.sessionStartedAt = nowIso();
    renderWorkspace();
  });

  document.getElementById('open-working-file').addEventListener('click', () => workingFileInput.click());
  workingFileInput.addEventListener('change', () => {
    loadWorkingFile(workingFileInput.files?.[0]);
    workingFileInput.value = '';
  });

  const privacyModal = document.getElementById('privacy-modal');
  function openPrivacyModal() { privacyModal.hidden = false; document.getElementById('close-privacy').focus(); }
  function closePrivacyModal() { privacyModal.hidden = true; document.getElementById('show-privacy').focus(); }
  document.getElementById('show-privacy').addEventListener('click', openPrivacyModal);
  document.getElementById('close-privacy').addEventListener('click', closePrivacyModal);
  document.getElementById('privacy-understood').addEventListener('click', closePrivacyModal);
  privacyModal.addEventListener('click', event => { if (event.target === privacyModal) closePrivacyModal(); });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (!privacyModal.hidden) closePrivacyModal();
    closeNavigation();
  });

  renderGuidedOptions();
})();

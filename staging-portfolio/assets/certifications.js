(() => {
  "use strict";
  const DATA_URL = "/data/certifications.json";
  const el = {
    total: document.getElementById("total-count"), courses: document.getElementById("course-count"),
    credentials: document.getElementById("verified-count"), jd: document.getElementById("jd-text"),
    match: document.getElementById("match-jd"), clear: document.getElementById("clear-jd"),
    matchStatus: document.getElementById("match-status"), search: document.getElementById("search"),
    focus: document.getElementById("focus"), onlyCredentialUrl: document.getElementById("only-credential-url"),
    count: document.getElementById("results-count"), results: document.getElementById("results"),
    error: document.getElementById("load-error")
  };
  const aliases = {
    "machine-learning": ["ml", "machine learning"], "artificial-intelligence": ["ai", "artificial intelligence"],
    "generative-ai": ["gen ai", "genai", "generative ai"], "llm": ["large language model", "large language models"],
    "software-engineering": ["software engineer", "software engineering", "swe"],
    "object-oriented-programming": ["oop", "object oriented programming"], "data-science": ["data science"],
    "data-analysis": ["data analysis", "data analytics"], "deep-learning": ["deep learning"],
    "neural-networks": ["neural network", "neural networks"], "cloud-computing": ["cloud computing"],
    "project-management": ["project management"], "web-development": ["web development"],
    "prompt-engineering": ["prompt engineering"], "responsible-ai": ["responsible ai"]
  };
  let records = [], matchedTags = new Set(), matchingActive = false;

  function makePhraseRegex(phrase) {
    const parts = phrase.trim().split(/[\s-]+/).filter(Boolean);
    return parts.length ? new RegExp("(^|[^a-z0-9])" + parts.join("[\\s-]+") + "(?=$|[^a-z0-9])", "i") : null;
  }
  function extractMatchingTags(text) {
    const found = new Set(), lowerText = text.toLocaleLowerCase();
    new Set(records.flatMap(record => record.tags)).forEach(tag => {
      const phrases = [tag.replace(/-/g, " "), ...(aliases[tag] || [])];
      if (tag.length > 2) phrases.push(tag);
      if (phrases.some(phrase => { const pattern = makePhraseRegex(phrase); return pattern && pattern.test(lowerText); })) found.add(tag);
    });
    return found;
  }
  function safeExternalLink(value) {
    if (!value) return null;
    try { const parsed = new URL(value); return parsed.protocol === "https:" ? parsed.href : null; }
    catch (_error) { return null; }
  }
  function appendText(parent, tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    node.textContent = text;
    parent.appendChild(node);
    return node;
  }
  function appendExternalLink(parent, url, label, className) {
    const safe = safeExternalLink(url);
    if (!safe) return;
    const link = document.createElement("a");
    link.href = safe; link.textContent = label; link.className = className || "";
    link.target = "_blank"; link.rel = "noopener noreferrer";
    parent.appendChild(link);
  }
  function buildCard(record, matching) {
    const card = document.createElement("article");
    card.className = "credential-card"; card.dataset.recordId = record.id;
    const top = document.createElement("div"); top.className = "credential-top";
    appendText(top, "span", "credential-area", record.focus_areas[0] || "Learning");
    appendText(top, "span", "credential-date", "Recorded " + record.date); card.appendChild(top);
    appendText(card, "h3", "", record.title);
    appendText(card, "p", "issuer", record.issuer);
    appendText(card, "p", "platform", "Platform: " + record.platform);
    const tagList = document.createElement("div"); tagList.className = "tag-list";
    record.tags.forEach(tag => appendText(tagList, "span", "tag", tag)); card.appendChild(tagList);
    if (matchingActive && matching.length) {
      const matchBox = document.createElement("div"); matchBox.className = "match-result";
      appendText(matchBox, "strong", "", matching.length + " matching tag" + (matching.length === 1 ? "" : "s"));
      appendText(matchBox, "span", "", matching.join(", ")); card.appendChild(matchBox);
    }
    const links = document.createElement("div"); links.className = "card-links";
    if (record.link) appendExternalLink(links, record.link, "Verify this credential ↗", "verify-link");
    else appendText(links, "span", "missing-link", "Personal verification URL not supplied");
    if (record.course_url) appendExternalLink(links, record.course_url, "View public course page ↗", "course-link");
    else appendText(links, "span", "missing-link", "No mapped public course page");
    card.appendChild(links); return card;
  }
  function render() {
    const query = el.search.value.trim().toLocaleLowerCase(), focus = el.focus.value;
    const onlyCredentialUrl = el.onlyCredentialUrl.checked;
    const filtered = records.map(record => ({record, matching:record.tags.filter(tag => matchedTags.has(tag))}))
      .filter(({record}) => {
        if (focus && !record.focus_areas.includes(focus)) return false;
        if (onlyCredentialUrl && !record.link) return false;
        const words = [record.title, record.issuer, record.platform, ...record.tags, ...record.focus_areas].join(" ").toLocaleLowerCase();
        return !query || words.includes(query);
      });
    filtered.sort((a,b) => {
      if (matchingActive && b.matching.length !== a.matching.length) return b.matching.length-a.matching.length;
      return a.record.title.localeCompare(b.record.title);
    });
    el.results.replaceChildren();
    if (!filtered.length) appendText(el.results, "p", "notice", "No records match these filters. Try another search or focus area.");
    else {
      const fragment = document.createDocumentFragment();
      filtered.forEach(({record,matching}) => fragment.appendChild(buildCard(record,matching)));
      el.results.appendChild(fragment);
    }
    el.count.textContent = filtered.length + " of " + records.length + " entries" + (matchingActive ? " · sorted by job-description tag overlap" : "");
  }
  function runMatch() {
    const text = el.jd.value.trim();
    if (!text) {
      matchingActive = false; matchedTags = new Set();
      el.matchStatus.textContent = "Paste a job description first. No data is uploaded by this page.";
      render(); return;
    }
    matchedTags = extractMatchingTags(text); matchingActive = true;
    el.matchStatus.textContent = matchedTags.size
      ? "Detected " + matchedTags.size + " inventory tag(s): " + Array.from(matchedTags).sort().join(", ") + ". Results are ranked by tag overlap, not credential quality."
      : "No inventory tags matched the pasted text. Try explicit tools, topics, or skills from the job description.";
    render();
  }
  el.match.addEventListener("click", runMatch);
  el.clear.addEventListener("click", () => {
    el.jd.value = ""; matchingActive = false; matchedTags = new Set();
    el.matchStatus.textContent = "Job description cleared. Use search and focus filters to browse the inventory."; render();
  });
  el.search.addEventListener("input", render);
  el.focus.addEventListener("change", render);
  el.onlyCredentialUrl.addEventListener("change", render);
  fetch(DATA_URL, {credentials:"same-origin"})
    .then(response => { if (!response.ok) throw new Error("HTTP " + response.status); return response.json(); })
    .then(data => {
      if (!Array.isArray(data)) throw new Error("Certification JSON must contain a list.");
      records = data; el.total.textContent = records.length;
      el.courses.textContent = records.filter(record => record.course_url).length;
      el.credentials.textContent = records.filter(record => record.link).length; render();
    })
    .catch(() => { el.count.textContent = "Catalog unavailable"; el.error.hidden = false; });
})();

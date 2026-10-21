(() => {
  "use strict";
  const DATA_URL = "/data/certifications.json";
  const search = document.getElementById("search");
  const focus = document.getElementById("focus");
  const count = document.getElementById("results-count");
  const results = document.getElementById("results");
  const error = document.getElementById("load-error");
  let records = [];

  function externalUrl(value) {
    if (!value) return null;
    try {
      const url = new URL(value);
      return url.protocol === "https:" ? url.href : null;
    } catch (_error) {
      return null;
    }
  }

  function textElement(parent, tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = text;
    parent.appendChild(element);
    return element;
  }

  function externalLink(parent, href, label, className) {
    const url = externalUrl(href);
    if (!url) return;
    const link = document.createElement("a");
    link.href = url;
    link.textContent = label;
    link.className = className || "";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    parent.appendChild(link);
  }

  function cardFor(record) {
    const card = document.createElement("article");
    card.className = "credential-card";
    const top = document.createElement("div");
    top.className = "credential-top";
    textElement(top, "span", "credential-area", record.focus_areas[0] || "Learning");
    textElement(top, "span", "credential-date", "Recorded " + record.date);
    card.appendChild(top);

    textElement(card, "h3", "", record.title);
    textElement(card, "p", "issuer", record.issuer);
    textElement(card, "p", "platform", "Platform: " + record.platform);

    const tagList = document.createElement("div");
    tagList.className = "tag-list";
    record.tags.forEach(tag => textElement(tagList, "span", "tag", tag));
    card.appendChild(tagList);

    const links = document.createElement("div");
    links.className = "card-links";
    if (record.link) externalLink(links, record.link, "Verify credential ↗", "verify-link");
    else textElement(links, "span", "missing-link", "Personal credential link not supplied");
    if (record.course_url) externalLink(links, record.course_url, "View course page ↗", "course-link");
    else textElement(links, "span", "missing-link", "No course page available");
    card.appendChild(links);
    return card;
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    const selectedFocus = focus.value;
    const filtered = records.filter(record => {
      if (selectedFocus && !record.focus_areas.includes(selectedFocus)) return false;
      const terms = [record.title, record.issuer, record.platform, ...record.tags, ...record.focus_areas]
        .join(" ").toLocaleLowerCase();
      return !query || terms.includes(query);
    }).sort((a, b) => a.title.localeCompare(b.title));

    results.replaceChildren();
    if (!filtered.length) {
      textElement(results, "p", "missing-link", "No certifications match this search. Try another term or area.");
    } else {
      const fragment = document.createDocumentFragment();
      filtered.forEach(record => fragment.appendChild(cardFor(record)));
      results.appendChild(fragment);
    }
    count.textContent = filtered.length + " of " + records.length + " records";
  }

  search.addEventListener("input", render);
  focus.addEventListener("change", render);

  fetch(DATA_URL, { credentials: "same-origin" })
    .then(response => {
      if (!response.ok) throw new Error("Could not load certification data.");
      return response.json();
    })
    .then(data => {
      if (!Array.isArray(data)) throw new Error("Certification data must be a list.");
      records = data;
      render();
    })
    .catch(() => {
      count.textContent = "Certification records unavailable";
      error.hidden = false;
    });
})();

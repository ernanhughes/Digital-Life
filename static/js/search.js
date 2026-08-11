(() => {
  const initSearch = () => {
    const form = document.querySelector('[data-site-search-form]');
    const input = document.querySelector('[data-site-search-input]');
    const results = document.querySelector('[data-search-results]');
    const status = document.querySelector('[data-search-status]');
    const indexNode = document.getElementById('site-search-index');
    const template = document.getElementById('site-search-result-template');
    const filters = [...document.querySelectorAll('[data-search-filter]')];

    if (!form || !input || !results || !status || !indexNode || !template) return;

    let parsedRecords = [];
    try {
      parsedRecords = JSON.parse(indexNode.textContent || '[]');
    } catch (error) {
      console.error('Programmer.ie search index parse failed', error);
      status.textContent = 'Search index could not be loaded. Please refresh the page and try again.';
      return;
    }

    const asString = (value) => (value == null ? '' : String(value));
    const asTags = (value) => {
      if (Array.isArray(value)) return value.map(asString);
      if (!value) return [];
      return [asString(value)];
    };

    const records = (Array.isArray(parsedRecords) ? parsedRecords : [])
      .filter((record) => record && typeof record === 'object')
      .map((record) => ({
        title: asString(record.title),
        url: asString(record.url),
        type: asString(record.type),
        series: asString(record.series),
        description: asString(record.description),
        date: asString(record.date),
        tags: asTags(record.tags),
      }))
      .filter((record) => record.title && record.url && record.type);

    let activeFilter = 'All';
    const normalize = (value) => asString(value).toLowerCase().normalize('NFKD');

    const searchableText = (record) => [
      record.title,
      record.type,
      record.series,
      record.description,
      ...record.tags,
    ].map(normalize);

    const scoreRecord = (record, query) => {
      const terms = normalize(query).trim().split(/\s+/).filter(Boolean);
      if (!terms.length) return 0;

      const title = normalize(record.title);
      const series = normalize(record.series);
      const type = normalize(record.type);
      const description = normalize(record.description);
      const tags = normalize(record.tags.join(' '));
      const all = searchableText(record).join(' ');

      let score = 0;
      for (const term of terms) {
        if (!all.includes(term)) return 0;
        if (title === term) score += 20;
        else if (title.startsWith(term)) score += 12;
        else if (title.includes(term)) score += 8;
        if (series.includes(term)) score += 5;
        if (type.includes(term)) score += 3;
        if (tags.includes(term)) score += 3;
        if (description.includes(term)) score += 2;
      }

      const phrase = normalize(query).trim();
      if (phrase.length > 2 && title.includes(phrase)) score += 14;
      if (phrase.length > 2 && series.includes(phrase)) score += 6;
      return score;
    };

    const clearResults = () => {
      while (results.firstChild) results.removeChild(results.firstChild);
    };

    const syncUrl = (query) => {
      const url = new URL(window.location.href);
      if (query) url.searchParams.set('q', query);
      else url.searchParams.delete('q');
      window.history.replaceState({}, '', url);
    };

    const render = ({ updateUrl = false } = {}) => {
      const query = input.value.trim();
      clearResults();

      if (updateUrl) syncUrl(query);

      if (!query) {
        status.textContent = `Search ${records.length} indexed resources across books, solutions, learning paths, chapters, AI prompts and articles.`;
        return;
      }

      const matches = records
        .filter((record) => activeFilter === 'All' || record.type === activeFilter)
        .map((record) => ({ record, score: scoreRecord(record, query) }))
        .filter((item) => item.score > 0)
        .sort((a, b) => b.score - a.score || (b.record.date || '').localeCompare(a.record.date || ''))
        .slice(0, 60);

      status.textContent = matches.length
        ? `${matches.length}${matches.length === 60 ? '+' : ''} result${matches.length === 1 ? '' : 's'} for “${query}”${activeFilter === 'All' ? '' : ` in ${activeFilter}`}.`
        : `No results for “${query}”${activeFilter === 'All' ? '' : ` in ${activeFilter}`}.`;

      matches.forEach(({ record }) => {
        const node = template.content.cloneNode(true);
        const type = node.querySelector('[data-result-type]');
        const series = node.querySelector('[data-result-series]');
        const date = node.querySelector('[data-result-date]');
        const link = node.querySelector('[data-result-link]');
        const description = node.querySelector('[data-result-description]');
        const action = node.querySelector('[data-result-action]');

        type.textContent = record.type;
        if (record.series) series.textContent = record.series;
        else series.remove();

        if (record.date) {
          date.dateTime = record.date;
          date.textContent = record.date;
        } else {
          date.remove();
        }

        link.href = record.url;
        link.textContent = record.title;
        description.textContent = record.description;
        action.href = record.url;

        results.appendChild(node);
      });
    };

    filters.forEach((button) => {
      button.addEventListener('click', () => {
        activeFilter = button.dataset.searchFilter || 'All';
        filters.forEach((item) => item.classList.toggle('is-active', item === button));
        render();
      });
    });

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      render({ updateUrl: true });
    });

    input.addEventListener('input', () => render());

    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get('q');
    if (initialQuery) input.value = initialQuery;
    render();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch, { once: true });
  } else {
    initSearch();
  }
})();

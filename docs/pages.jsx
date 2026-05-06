/* global React, Icon, CodeBlock, DOCS_CONTENT */
const { useState: useS, useEffect: useE, useRef: useR, useMemo } = React;

function LandingPage({ toolName, tagline, onDonate, onNav }) {
  const installCmd = `curl -fsSL https://evgeni-genchev.com/omurtag/install.sh | sh`;
  return (
    <main className="landing" data-screen-label="01 Landing">
      <div className="landing-inner">
        <div className="eyebrow">V0.4.5 · BSD-3-Clause licensed</div>
        <h1 className="hero-title">
          A <em>builder</em> for builders.
        </h1>
        <p className="hero-desc">{tagline}</p>
        <div className="hero-cta">
          <button className="btn btn-primary" onClick={() => onNav("docs")}>
            Read the docs <Icon name="arrow" size={14} />
          </button>
          <button className="btn" onClick={() => onNav("about")}>
            About the project
          </button>
        </div>

        <CodeBlock lang="bash">{installCmd}</CodeBlock>

        <div className="donate-row">
          <div className="donate-label">If it saved you time,</div>
          <div className="donate-buttons">
            <button className="donate-btn" onClick={() => onDonate("btc")}>
              <span className="sym btc">₿</span> Donate Bitcoin
            </button>
            <button className="donate-btn" onClick={() => onDonate("eth")}>
              <span className="sym eth">Ξ</span> Donate Ethereum
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

function renderText(str) {
  const re = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))/g;
  const result = [];
  let last = 0, m;
  while ((m = re.exec(str)) !== null) {
    if (m.index > last) result.push(str.slice(last, m.index));
    const p = m[0];
    if (p[0] === "`") result.push(<code key={m.index}>{p.slice(1, -1)}</code>);
    else if (p.startsWith("**")) result.push(<strong key={m.index}>{p.slice(2, -2)}</strong>);
    else if (p[0] === "*") result.push(<em key={m.index}>{p.slice(1, -1)}</em>);
    else {
      const lm = p.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (lm) result.push(<a key={m.index} href={lm[2]} target="_blank" rel="noreferrer">{lm[1]}</a>);
    }
    last = m.index + p.length;
  }
  if (last < str.length) result.push(str.slice(last));
  return result;
}

function DocsPage({ toolName }) {
  const sections = useMemo(() => DOCS_CONTENT, []);
  const [active, setActive] = useS(sections[0].id);
  const [query, setQuery] = useS("");
  const searchRef = useR(null);
  const mainRef = useR(null);

  useE(() => {
    const onKey = (e) => {
      const t = e.target;
      const isInput = t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable);
      if (e.key === "/" && !isInput) {
        e.preventDefault();
        searchRef.current?.focus();
      }
      if (e.key === "Escape" && document.activeElement === searchRef.current) {
        searchRef.current?.blur();
        setQuery("");
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  useE(() => {
    const handler = () => {
      const root = mainRef.current;
      if (!root) return;
      const headings = [...root.querySelectorAll("h2[id]")];
      const scrollY = window.scrollY + 120;
      let cur = headings[0]?.id || sections[0].id;
      for (const h of headings) {
        if (h.offsetTop <= scrollY) cur = h.id;
      }
      setActive(cur);
    };
    handler();
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, [sections]);

  const onJump = (id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const top = el.getBoundingClientRect().top + window.scrollY - 80;
    window.scrollTo({ top, behavior: "smooth" });
  };

  const q = query.trim().toLowerCase();
  const matches = (s) => {
    if (!q) return true;
    const body = s.body(toolName);
    const blob = [s.title, body.lead, ...(body.paragraphs || []), ...(body.list || []), body.code?.text || ""].join(" ").toLowerCase();
    return blob.includes(q);
  };

  const groups = {};
  for (const s of sections) {
    if (!groups[s.group]) groups[s.group] = [];
    groups[s.group].push(s);
  }

  return (
    <div className="docs" data-screen-label="02 Docs">
      <aside className="docs-side">
        <div className="docs-search">
          <span className="magnify"><Icon name="search" size={13} /></span>
          <input
            ref={searchRef}
            type="text"
            placeholder="Search docs"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {!query && <kbd>/</kbd>}
        </div>
        {Object.entries(groups).map(([gname, items]) => (
          <div className="docs-nav-section" key={gname}>
            <div className="docs-nav-title">{gname}</div>
            {items.map((s) => {
              const ok = matches(s);
              return (
                <a
                  key={s.id}
                  className={
                    "docs-nav-link" +
                    (active === s.id ? " active" : "") +
                    (!ok ? " dim" : "")
                  }
                  onClick={(e) => { e.preventDefault(); onJump(s.id); }}
                  href={`#${s.id}`}
                >
                  {s.title}
                </a>
              );
            })}
          </div>
        ))}
      </aside>

      <article className="docs-main" ref={mainRef}>
        <h1>Documentation</h1>
        <div className="docs-meta">
          <span>V0.4.5</span>
          <span className="dot">/</span>
          <span>Updated May 2026</span>
          <span className="dot">/</span>
          <span>Press <span className="kbd">/</span> to search</span>
        </div>

        {sections.map((s, i) => {
          const body = s.body(toolName);
          return (
            <section key={s.id}>
              <h2 id={s.id}>{s.title}</h2>
              {body.lead && <p className="lead">{renderText(body.lead)}</p>}
              {(body.paragraphs || []).map((p, j) => <p key={j}>{renderText(p)}</p>)}
              {body.list && (
                <ul>{body.list.map((li, j) => <li key={j}>{renderText(li)}</li>)}</ul>
              )}
              {body.code && <CodeBlock lang={body.code.lang}>{body.code.text}</CodeBlock>}
              {i < sections.length - 1 && <hr />}
            </section>
          );
        })}
      </article>
    </div>
  );
}

function AboutPage({ toolName, onNav }) {
  return (
    <main className="about" data-screen-label="03 About">
      <h1>About {toolName}</h1>
      <p>
        {toolName} is a personal project, built and maintained by one person in
        the evenings. It exists because the alternatives were heavier than the
        problem warranted.
      </p>
      <p className="muted">
        Cookiecutter and Copier both solve the scaffolding problem, but neither
        one runs a security scan on what you pull in. When templates come from
        third-party repos, it matters to know whether a baked-in dependency has
        known CVEs before you build on top of it.
      </p>
      <p className="muted">
        Free, open source, no telemetry. Releases come when they're ready.
      </p>

      <dl className="factsheet">
        <dt>License</dt><dd>BSD-3-Clause</dd>
        <dt>First release</dt><dd>TBD</dd>
        <dt>Latest</dt><dd>0.4.2</dd>
        <dt>Source</dt><dd><a href="https://github.com/EvgeniGenchev/omurtag">github.com/EvgeniGenchev/omurtag</a></dd>
        <dt>Author</dt><dd><a href="https://evgeni-genchev.com">evgeni-genchev.com</a></dd>
        <dt>Contact</dt><dd><a href="mailto:me@evgeni-genchev.com">me@evgeni-genchev.com</a></dd>
      </dl>
    </main>
  );
}

Object.assign(window, { LandingPage, DocsPage, AboutPage });

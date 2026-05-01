/* global React */
const { useState, useEffect, useRef, useCallback } = React;

function Icon({ name, size = 16 }) {
  const s = { width: size, height: size, fill: "none", stroke: "currentColor", strokeWidth: 1.6, strokeLinecap: "round", strokeLinejoin: "round" };
  switch (name) {
    case "sun": return (<svg viewBox="0 0 24 24" {...s}><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>);
    case "moon": return (<svg viewBox="0 0 24 24" {...s}><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>);
    case "star": return (<svg viewBox="0 0 24 24" {...s} fill="currentColor" stroke="none"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>);
    case "github": return (<svg viewBox="0 0 24 24" {...s} fill="currentColor" stroke="none"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.87-1.54-3.87-1.54-.52-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.76 2.69 1.25 3.35.96.1-.74.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.28 1.18-3.08-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.62 1.58.23 2.75.11 3.04.74.8 1.18 1.82 1.18 3.08 0 4.42-2.7 5.39-5.27 5.68.41.36.78 1.06.78 2.13 0 1.54-.01 2.78-.01 3.16 0 .31.21.68.8.56C20.21 21.39 23.5 17.08 23.5 12c0-6.35-5.15-11.5-11.5-11.5z"/></svg>);
    case "search": return (<svg viewBox="0 0 24 24" {...s}><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>);
    case "copy": return (<svg viewBox="0 0 24 24" {...s}><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>);
    case "check": return (<svg viewBox="0 0 24 24" {...s}><path d="M5 13l4 4L19 7"/></svg>);
    case "close": return (<svg viewBox="0 0 24 24" {...s}><path d="M6 6l12 12M18 6L6 18"/></svg>);
    case "arrow": return (<svg viewBox="0 0 24 24" {...s}><path d="M5 12h14M13 5l7 7-7 7"/></svg>);
    case "terminal": return (<svg viewBox="0 0 24 24" {...s}><polyline points="4,7 9,12 4,17"/><line x1="13" y1="17" x2="20" y2="17"/></svg>);
    default: return null;
  }
}

function CopyButton({ text, label = "Copy" }) {
  const [copied, setCopied] = useState(false);
  const onCopy = () => {
    navigator.clipboard?.writeText(text).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 1400);
  };
  return (
    <button className={"copy-btn" + (copied ? " copied" : "")} onClick={onCopy}>
      <Icon name={copied ? "check" : "copy"} size={12} />
      {copied ? "Copied" : label}
    </button>
  );
}

function CodeBlock({ lang = "bash", children, copyText }) {
  const text = typeof children === "string" ? children : copyText || "";
  const html = highlight(text, lang);
  return (
    <div className="code">
      <div className="code-header">
        <span className="code-lang">{lang}</span>
        <CopyButton text={text} />
      </div>
      <pre><code dangerouslySetInnerHTML={{ __html: html }} /></pre>
    </div>
  );
}

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function highlight(src, lang) {
  const esc = escapeHtml(src);
  if (lang === "bash" || lang === "sh") {
    return esc;
  }
  if (lang === "yaml" || lang === "yml") {
    return esc
      .replace(/(^|\n)([ \t]*)([\w\-.]+)(:)/g, '$1$2<span class="kw">$3</span>$4')
      .replace(/(#[^\n]*)/g, '<span class="com">$1</span>')
      .replace(/("[^"]*"|'[^']*')/g, '<span class="str">$1</span>');
  }
  if (lang === "js" || lang === "javascript") {
    return esc
      .replace(/\b(const|let|var|function|return|if|else|await|async|import|from|export|new)\b/g, '<span class="kw">$1</span>')
      .replace(/("[^"]*"|'[^']*'|`[^`]*`)/g, '<span class="str">$1</span>')
      .replace(/\b(\d+)\b/g, '<span class="num">$1</span>')
      .replace(/(\/\/[^\n]*)/g, '<span class="com">$1</span>');
  }
  return esc;
}

function useTheme() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("__theme") || "light";
  });
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("__theme", theme);
  }, [theme]);
  return [theme, setTheme];
}

function useToast() {
  const [msg, setMsg] = useState(null);
  const show = (m) => {
    setMsg(m);
    setTimeout(() => setMsg(null), 1800);
  };
  const node = msg ? <div className="toast">{msg}</div> : null;
  return [show, node];
}

Object.assign(window, { Icon, CopyButton, CodeBlock, useTheme, useToast, highlight, escapeHtml });

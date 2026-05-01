/* global React, ReactDOM, Icon, useTheme, useToast, DonationModal,
   LandingPage, DocsPage, AboutPage,
   TweaksPanel, useTweaks, TweakSection, TweakText, TweakColor */
const { useState: uS, useEffect: uE } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "toolName": "omurtag",
  "tagline": "Your templates, scaffolded reliably, with a security audit built in.",
  "accent": "#b65a35"
}/*EDITMODE-END*/;

function App() {
  const [tweaks, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [theme, setTheme] = useTheme();
  const [route, setRoute] = uS(() => {
    const h = (location.hash || "").replace(/^#\/?/, "");
    return ["docs", "about"].includes(h) ? h : "landing";
  });
  const [donate, setDonate] = uS(null);
  const [showToast, toast] = useToast();
  const [stars, setStars] = uS(null);

  uE(() => {
    fetch("https://api.github.com/repos/EvgeniGenchev/omurtag")
      .then(r => r.ok ? r.json() : null)
      .then(d => d && setStars(d.stargazers_count))
      .catch(() => {});
  }, []);

  // sync route to hash
  uE(() => {
    const h = route === "landing" ? "" : `#/${route}`;
    if (location.hash !== h) history.replaceState(null, "", location.pathname + (h || location.search));
  }, [route]);

  uE(() => {
    const onHash = () => {
      const h = (location.hash || "").replace(/^#\/?/, "");
      setRoute(["docs", "about"].includes(h) ? h : "landing");
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  // accent color → CSS var (also derive a soft variant)
  uE(() => {
    document.documentElement.style.setProperty("--accent", tweaks.accent);
    document.documentElement.style.setProperty(
      "--accent-soft",
      hexToRgba(tweaks.accent, 0.13)
    );
  }, [tweaks.accent]);

  const onNav = (r) => {
    setRoute(r);
    window.scrollTo({ top: 0, behavior: "instant" });
  };

  const onStarClick = () => {
    window.open("https://github.com/EvgeniGenchev/omurtag", "_blank", "noreferrer");
  };

  const fmtStars = (n) => n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, "") + "k" : String(n);

  return (
    <div className="shell">
      <nav className="topnav">
        <div className="brand" onClick={() => onNav("landing")}>
          <span className="dot"></span>
          {tweaks.toolName}
        </div>
        <div className="navlinks">
          <span className={"navlink" + (route === "docs" ? " active" : "")} onClick={() => onNav("docs")}>Docs</span>
          <span className={"navlink" + (route === "about" ? " active" : "")} onClick={() => onNav("about")}>About</span>
        </div>
        <div className="navtools">
          <button className="starbadge" onClick={onStarClick} title="GitHub stars">
            <Icon name="github" size={13} />
            <span>star</span>
            <span className="sep">·</span>
            <Icon name="star" size={11} />
            {stars !== null && <span>{fmtStars(stars)}</span>}
          </button>
          <button
            className="iconbtn"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            title="Toggle theme"
          >
            <Icon name={theme === "light" ? "moon" : "sun"} size={14} />
          </button>
        </div>
      </nav>

      {route === "landing" && (
        <LandingPage
          toolName={tweaks.toolName}
          tagline={tweaks.tagline}
          onDonate={(k) => setDonate(k)}
          onNav={onNav}
        />
      )}
      {route === "docs" && <DocsPage toolName={tweaks.toolName} />}
      {route === "about" && <AboutPage toolName={tweaks.toolName} onNav={onNav} />}

      {donate && <DonationModal kind={donate} onClose={() => setDonate(null)} />}
      {toast}

      <TweaksPanel title="Tweaks">
        <TweakSection title="Identity">
          <TweakText
            label="Tool name"
            value={tweaks.toolName}
            onChange={(v) => setTweak("toolName", v)}
          />
          <TweakText
            label="Tagline"
            value={tweaks.tagline}
            onChange={(v) => setTweak("tagline", v)}
          />
        </TweakSection>
        <TweakSection title="Color">
          <TweakColor
            label="Accent"
            value={tweaks.accent}
            onChange={(v) => setTweak("accent", v)}
          />
        </TweakSection>
      </TweaksPanel>
    </div>
  );
}

function hexToRgba(hex, a) {
  const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex || "");
  if (!m) return `rgba(0,0,0,${a})`;
  const [r, g, b] = [m[1], m[2], m[3]].map((x) => parseInt(x, 16));
  return `rgba(${r},${g},${b},${a})`;
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);

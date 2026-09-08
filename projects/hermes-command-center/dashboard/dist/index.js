(function () {
  "use strict";
  const SDK = window.__HERMES_PLUGIN_SDK__;
  const React = SDK.React;
  const { useEffect, useState } = SDK.hooks;
  const { Card, CardContent, CardHeader, CardTitle, Badge, Button } = SDK.components;
  const h = React.createElement;

  function tone(status) {
    if (["fresh", "healthy", "ok", "done"].includes(status)) return "cc-good";
    if (["unknown", "stale", "paused", "never-run"].includes(status)) return "cc-warn";
    return "cc-bad";
  }
  function Status(props) { return h("span", { className: "cc-status " + tone(props.value) }, props.value || "unknown"); }
  function Link(props) { return props.url ? h("a", { href: props.url, target: props.url.startsWith("http") ? "_blank" : undefined, rel: "noopener noreferrer" }, props.children) : h("span", null, props.children); }
  function Section(props) {
    return h(Card, { className: "cc-card" },
      h(CardHeader, null, h(CardTitle, { className: "cc-title" }, props.title), h(Status, { value: props.status })),
      h(CardContent, null,
        props.source && h("p", { className: "cc-provenance" }, "Source: ", h("strong", null, props.source.name), " · ", props.source.updated_at ? new Date(props.source.updated_at).toLocaleString(undefined, { timeZoneName: "short" }) : "updated unknown"),
        props.children));
  }
  function Rows(props) {
    const items = props.items || [];
    if (!items.length) return h("p", { className: "cc-muted" }, "No data available.");
    return h("div", { className: "cc-rows" }, items.slice(0, props.limit || 8).map((x, i) =>
      h("div", { className: "cc-row", key: x.id || x.name || i },
        h("div", { className: "cc-grow" }, h(Link, { url: x.url }, x.name || x.title || x.id), x.assignee && h("small", null, x.assignee)),
        h(Status, { value: x.status }))));
  }
  function SourceList(props) {
    return h("div", { className: "cc-sources" }, h("h2", null, "Provenance"), props.sources.map(s =>
      h("div", { className: "cc-source", key: s.name }, h("strong", null, s.name), h(Status, { value: s.status }), h("time", null, s.updated_at ? new Date(s.updated_at).toLocaleString() : "updated: unknown"), s.error && h("small", null, s.error))));
  }
  function App() {
    const [data, setData] = useState(null), [error, setError] = useState(null), [tick, setTick] = useState(0);
    useEffect(() => { let live = true; SDK.fetchJSON("/api/plugins/command-center/overview").then(x => { if (live) { setData(x); setError(null); } }).catch(e => live && setError(String(e))); return () => { live = false; }; }, [tick]);
    if (error) return h("div", { className: "cc-error" }, h("h1", null, "Command Center unavailable"), h("p", null, error), h(Button, { onClick: () => setTick(tick + 1) }, "Retry"));
    if (!data) return h("p", { className: "cc-loading" }, "Loading read-only operational data…");
    const s = data.sections;
    return h("div", { className: "cc-shell" },
      h("header", { className: "cc-hero" }, h("div", null, h("p", { className: "cc-kicker" }, "READ-ONLY OPERATIONS"), h("h1", null, "Hermes Command Center"), h("p", null, "Observe here. Coordinate in Discord #general.")), h("div", null, h(Badge, null, "No mutations"), h(Button, { onClick: () => setTick(tick + 1) }, "Refresh"))),
      h("p", { className: "cc-generated" }, "Snapshot: " + new Date(data.generated_at).toLocaleString(undefined, { timeZoneName: "short" })),
      h("main", { className: "cc-grid" },
        h(Section, { title: "Kanban", status: s.kanban.status, source: s.kanban.source }, h("div", { className: "cc-counts" }, Object.entries(s.kanban.counts).map(([k,v]) => h("span", { key:k }, h("b", null, v), " ", k))), h(Rows, { items: s.kanban.active })),
        h(Section, { title: "Deployments", status: s.deployments.status, source: s.deployments.source }, h("div", { className: "cc-counts" }, Object.entries(s.deployments.counts).map(([k,v]) => h("span", { key:k }, h("b", null, v), " ", k))), h(Rows, { items: s.deployments.items })),
        h(Section, { title: "Cron health", status: s.cron.status, source: s.cron.source }, h("div", { className: "cc-counts" }, Object.entries(s.cron.counts).map(([k,v]) => h("span", { key:k }, h("b", null, v), " ", k))), h(Rows, { items: s.cron.items })),
        h(Section, { title: "Models & limits", status: s.models.status, source: s.models.source }, s.models.primary ? h("p", null, h("strong", null, "Primary: "), s.models.primary.provider + " / " + s.models.primary.model) : null, h("p", null, h("strong", null, "Fallbacks: "), s.models.fallbacks.map(x => x.provider + "/" + x.model).join(" → ") || "none"), h("p", { className: "cc-muted" }, "Quota: " + s.models.quota.status + " — " + s.models.quota.message)),
        h(Section, { title: "Recent artifacts", status: s.kanban.status, source: s.kanban.source }, h(Rows, { items: s.kanban.artifacts.map(x => ({name:x.name,status:x.content_type,url:x.url})) }))),
      h(SourceList, { sources: data.sources }));
  }
  window.__HERMES_PLUGINS__.register("command-center", App);
})();

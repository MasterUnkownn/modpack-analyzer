import { useEffect, useState } from "react";
import { connectWebSocket } from "../services/websocket";

export default function Dashboard() {

  const [logs, setLogs] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [assets, setAssets] = useState([]);
  const [comparison, setComparison] = useState(null);
  const [errors, setErrors] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    connectWebSocket((msg) => {

      if (msg.type === "log") {
        setLogs(prev => [msg.data, ...prev].slice(0, 50));
      }

      if (msg.type === "recipe_issues") {
        setRecipes(msg.data);
      }

      if (msg.type === "asset_issues") {
        setAssets(msg.data);
      }

      if (msg.type === "comparison") {
        setComparison(msg.data);
      }

      if (msg.type === "mapped_errors") {
        setErrors(msg.data);
      }

      if (msg.type === "suggestions") {
        setSuggestions(msg.data);
      }

    });
  }, []);

  return (
    <div style={{ padding: 20 }}>

      <h1>🧠 Modpack Analyzer</h1>

      <h2>Comparison</h2>
      {comparison && (
        <div>
          <div>Missing Server: {comparison.missing_on_server?.join(", ")}</div>
          <div>Missing Client: {comparison.missing_on_client?.join(", ")}</div>
          <div>Version Mismatch: {comparison.version_mismatch?.join(", ")}</div>
        </div>
      )}

      <h2>Recipe Issues</h2>
      {recipes.map((r, i) => (
        <div key={i} style={{ color: "orange" }}>{r.message}</div>
      ))}

      <h2>Asset Issues</h2>
      {assets.map((a, i) => (
        <div key={i} style={{ color: "purple" }}>{a.message}</div>
      ))}

      <h2>Mapped Errors</h2>
      {errors.map((e, i) => (
        <div key={i} style={{ color: "red" }}>
          [{e.type}] {e.source || ""} → {e.message}
        </div>
      ))}

      <h2>Suggestions</h2>
      {suggestions.map((s, i) => (
        <div key={i} style={{ color: "green" }}>
          {s.title} → {s.action}
        </div>
      ))}

      <h2>Logs</h2>
      {logs.map((l, i) => (
        <div key={i}>{l.raw}</div>
      ))}

    </div>
  );
}

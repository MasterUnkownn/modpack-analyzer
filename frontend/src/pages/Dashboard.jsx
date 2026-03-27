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

      <h2>Recipe Isimport { useEffect, useState } from "react";
import { connectWebSocket } from "../services/websocket";
import Panel from "../components/panels/Panel";

export default function Dashboard() {

  const [data, setData] = useState({
    mods: 0,
    errors: 0,
    conflicts: 0
  });

  useEffect(() => {
    connectWebSocket((msg) => {

      if (msg.type === "mapped_errors") {
        setData(prev => ({ ...prev, errors: msg.data.length }));
      }

      if (msg.type === "comparison") {
        const conflicts = (msg.data.version_mismatch || []).length;
        setData(prev => ({ ...prev, conflicts }));
      }

    });
  }, []);

  return (
    <div>

      <Panel title="Overview">
        <div>Errors: {data.errors}</div>
        <div>Conflicts: {data.conflicts}</div>
      </Panel>

      <Panel title="System Status">
        Running and connected.
      </Panel>

    </div>
  );
}

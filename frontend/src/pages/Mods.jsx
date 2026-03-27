import { useEffect, useState } from "react";
import Panel from "../components/panels/Panel";
import SearchBar from "../components/panels/SearchBar";
import { connectWebSocket } from "../services/websocket";

export default function Mods() {

  const [mods, setMods] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    connectWebSocket((msg) => {
      if (msg.type === "mods_updated") {
        setMods(msg.data || []);
      }
    });
  }, []);

  const filtered = mods.filter(m =>
    m.name?.toLowerCase().includes(search.toLowerCase()) ||
    m.mod_id?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: "flex", gap: 20 }}>

      {/* LEFT PANEL */}
      <div style={{ flex: 1 }}>
        <Panel title="Mods List">

          <SearchBar value={search} onChange={setSearch} />

          {filtered.map((mod, i) => (
            <div
              key={i}
              onClick={() => setSelected(mod)}
              style={{
                padding: 8,
                cursor: "pointer",
                borderBottom: "1px solid #333"
              }}
            >
              {mod.name}
            </div>
          ))}

        </Panel>
      </div>

      {/* RIGHT PANEL */}
      <div style={{ flex: 1 }}>
        <Panel title="Details">

          {!selected && <div>Select a mod</div>}

          {selected && (
            <div>
              <div><b>Name:</b> {selected.name}</div>
              <div><b>ID:</b> {selected.mod_id}</div>
              <div><b>Version:</b> {selected.version || "Unknown"}</div>
            </div>
          )}

        </Panel>
      </div>

    </div>
  );
}

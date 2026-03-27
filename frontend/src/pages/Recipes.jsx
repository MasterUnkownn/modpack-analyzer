import { useEffect, useState } from "react";
import Panel from "../components/panels/Panel";
import SearchBar from "../components/panels/SearchBar";
import RecipeGrid from "../components/panels/RecipeGrid";
import ItemPalette from "../components/panels/ItemPalette";
import { connectWebSocket } from "../services/websocket";

export default function Recipes() {

  const [recipes, setRecipes] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);

  const [editor, setEditor] = useState("");

  const [grid, setGrid] = useState({
    width: 3,
    height: 3,
    slots: [
      [null, null, null],
      [null, null, null],
      [null, null, null]
    ]
  });

  const [output, setOutput] = useState("minecraft:diamond");
  const [type, setType] = useState("shaped");

  const [items, setItems] = useState([
    "minecraft:stone",
    "minecraft:stick",
    "minecraft:iron_ingot"
  ]);

  // =========================
  // WEBSOCKET
  // =========================
  useEffect(() => {
    connectWebSocket((msg) => {

      if (msg.type === "datapack_recipes") {
        setRecipes(msg.data || []);
      }

    });
  }, []);

  // =========================
  // FILTER
  // =========================
  const filtered = recipes.filter(r =>
    JSON.stringify(r).toLowerCase().includes(search.toLowerCase())
  );

  // =========================
  // SELECT RECIPE
  // =========================
  const selectRecipe = (r) => {
    setSelected(r);
    setEditor(JSON.stringify(r.raw, null, 2));

    // Future: auto-convert JSON → grid
  };

  // =========================
  // SAVE RECIPE
  // =========================
  const saveRecipe = async () => {
    try {
      await fetch("http://localhost:8000/api/recipes/save", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          type,
          grid,
          output,
          original_path: selected?.path || "custom/generated",
          raw: JSON.parse(editor || "{}")
        })
      });

      alert("Saved to datapack!");
    } catch (e) {
      console.error(e);
      alert("Error saving recipe");
    }
  };

  return (
    <div style={{ display: "flex", gap: 20 }}>

      {/* LEFT PANEL */}
      <div style={{ flex: 1 }}>
        <Panel title="Recipes">

          <SearchBar value={search} onChange={setSearch} />

          {filtered.map((r, i) => (
            <div
              key={i}
              onClick={() => selectRecipe(r)}
              style={{
                padding: 8,
                cursor: "pointer",
                borderBottom: "1px solid #334155"
              }}
            >
              {r.output?.item || JSON.stringify(r.output)}
            </div>
          ))}

        </Panel>
      </div>

      {/* RIGHT PANEL */}
      <div style={{ flex: 2, display: "flex", flexDirection: "column", gap: 20 }}>

        {/* JSON EDITOR */}
        <Panel title="JSON Editor">

          {!selected && <div>Select a recipe</div>}

          {selected && (
            <textarea
              value={editor}
              onChange={(e) => setEditor(e.target.value)}
              style={{
                width: "100%",
                height: 200,
                background: "#020617",
                color: "white",
                border: "1px solid #334155"
              }}
            />
          )}

        </Panel>

        {/* VISUAL EDITOR */}
        <Panel title="Visual Editor">

          {/* TYPE SELECTOR */}
          <h4>Recipe Type</h4>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="shaped">Shaped</option>
            <option value="shapeless">Shapeless</option>
            <option value="custom">Custom (Raw JSON)</option>
          </select>

          <div style={{ display: "flex", gap: 20, marginTop: 10 }}>

            {/* GRID */}
            <div>
              <RecipeGrid grid={grid} onChange={setGrid} />
            </div>

            {/* SIDE PANEL */}
            <div style={{ minWidth: 200 }}>

              <h4>Items</h4>
              <ItemPalette items={items} />

              <h4 style={{ marginTop: 10 }}>Output</h4>
              <input
                value={output}
                onChange={(e) => setOutput(e.target.value)}
                style={{
                  width: "100%",
                  padding: 5
                }}
              />

              <button
                onClick={saveRecipe}
                style={{
                  marginTop: 10,
                  padding: 10,
                  background: "#38bdf8",
                  border: "none",
                  cursor: "pointer",
                  width: "100%"
                }}
              >
                Save to Datapack
              </button>

            </div>

          </div>

        </Panel>

      </div>

    </div>
  );
}

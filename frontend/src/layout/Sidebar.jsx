export default function Sidebar() {
  return (
    <div style={{
      width: 220,
      background: "#020617",
      padding: 20
    }}>
      <h3>Analyzer</h3>

      <a href="/">Dashboard</a><br/>
      <a href="/mods">Mods</a><br/>
      <a href="/recipes">Recipes</a><br/>
      <a href="/assets">Assets</a><br/>
      <a href="/logs">Logs</a><br/>
      <a href="/conflicts">Conflicts</a>
    </div>
  );
}

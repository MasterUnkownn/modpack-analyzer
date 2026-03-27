import "../../styles/panels.css";

export default function Panel({ title, children }) {
  return (
    <div className="panel">
      <div className="panel-title">{title}</div>
      <div>{children}</div>
    </div>
  );
}

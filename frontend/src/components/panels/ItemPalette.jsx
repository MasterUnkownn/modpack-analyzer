export default function ItemPalette({ items }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>
      {items.map((item, i) => (
        <div
          key={i}
          draggable
          onDragStart={(e) => {
            e.dataTransfer.setData("item", item);
          }}
          style={{
            padding: 5,
            background: "#1e293b",
            cursor: "grab"
          }}
        >
          {item}
        </div>
      ))}
    </div>
  );
}

import "./recipegrid.css";

export default function RecipeGrid({ grid, onChange }) {

  const handleDrop = (x, y, item) => {
    const newGrid = [...grid.slots];
    newGrid[y][x] = item;

    onChange({
      ...grid,
      slots: newGrid
    });
  };

  return (
    <div
      className="grid"
      style={{
        gridTemplateColumns: `repeat(${grid.width}, 60px)`
      }}
    >
      {grid.slots.flat().map((item, i) => {
        const x = i % grid.width;
        const y = Math.floor(i / grid.width);

        return (
          <div
            key={i}
            className="slot"
            onDrop={(e) => {
              const item = e.dataTransfer.getData("item");
              handleDrop(x, y, item);
            }}
            onDragOver={(e) => e.preventDefault()}
          >
            {item || "+"}
          </div>
        );
      })}
    </div>
  );
}

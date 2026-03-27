export default function SearchBar({ value, onChange }) {
  return (
    <input
      placeholder="Search..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{
        width: "100%",
        padding: 8,
        marginBottom: 10
      }}
    />
  );
}

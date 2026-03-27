import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layout/MainLayout";

import Dashboard from "./pages/Dashboard";
import Mods from "./pages/Mods";
import Recipes from "./pages/Recipes";

export default function App() {
  return (
    <BrowserRouter>
      <MainLayout>
	<Routes>
	  <Route path="/" element={<Dashboard />} />
	  <Route path="/mods" element={<Mods />} />
	  <Route path="/recipes" element={<Recipes />} />
	</Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

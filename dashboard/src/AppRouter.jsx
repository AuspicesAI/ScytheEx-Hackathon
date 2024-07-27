import { lazy, Suspense } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

const App = lazy(() => import("./App"));
const Navbar = lazy(() => import("./components/Navbar"));
const Sidebar = lazy(() => import("./components/Sidebar"));
const ConfigEditor = lazy(() => import("./pages/config-editor/ConfigEditor"));
const Alerts = lazy(() => import("./pages/alerts/Alerts"));

const AppRouter = () => {
  return (
    <Router>
      {/* Fallback UI during component lazy loading */}
      <Suspense
        fallback={
          <div className="loaderdiv">
            <span className="loader"></span>
          </div>
        }
      >
        {/* Layout with sidebar, navbar, and main content */}
        <div className="min-h-screen flex flex-col flex-auto flex-shrink-0 antialiased bg-white dark:bg-gray-700 text-black dark:text-white">
          <Sidebar />
          <Navbar />
          <div className="h-full ml-14 mt-14 mb-10 md:ml-64">
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<App />} />
              <Route path="/config-editor" element={<ConfigEditor />} />
              <Route path="/alerts" element={<Alerts />} />
            </Routes>
          </div>
        </div>
      </Suspense>
    </Router>
  );
};

export default AppRouter;

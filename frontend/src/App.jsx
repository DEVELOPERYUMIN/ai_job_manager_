import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import ResumePage from './pages/ResumePage';
import InterviewPage from './pages/InterviewPage';
import DashboardPage from './pages/DashboardPage';
import ExportPage from './pages/ExportPage';

export default function App() {
  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
        <div className="container">
          <NavLink to="/" className="navbar-brand fw-bold">
            JobPrep
          </NavLink>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navLinks"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navLinks">
            <ul className="navbar-nav ms-auto">
              {[
                { to: '/resume', label: 'Resume' },
                { to: '/interview', label: 'Interview' },
                { to: '/dashboard', label: 'Dashboard' },
                { to: '/export', label: 'Export' },
              ].map((item) => (
                <li className="nav-item" key={item.to}>
                  <NavLink
                    to={item.to}
                    className={({ isActive }) =>
                      isActive ? 'nav-link active' : 'nav-link'
                    }
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </nav>
      <div className="container mt-5">
        <Routes>
          <Route path="/resume" element={<ResumePage />} />
          <Route path="/interview" element={<InterviewPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/export" element={<ExportPage />} />
          <Route path="*" element={<ResumePage />} />
        </Routes>
      </div>
    </Router>
  );
}


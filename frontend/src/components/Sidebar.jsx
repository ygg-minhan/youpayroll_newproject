import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, FileText, Files, LifeBuoy, LogOut, User, BookOpen } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import LogoutModal from './LogoutModal';

const Sidebar = ({ isOpen, onClose }) => {
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogoutConfirm = () => {
    logout();
    setIsLogoutModalOpen(false);
    navigate('/login');
  };

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="logo-container">
          <img src="http://127.0.0.1:8000/media/branding/logo.jpg" alt="YOU GotaGift Logo" className="logo" />
        </div>

        <div className="menu-group">
          <div className="menu-label">MAIN MENU</div>
          <nav className="nav-menu">
            <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <LayoutDashboard size={22} />
              <span>Overview</span>
            </NavLink>
            <NavLink to="/payslips" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <FileText size={22} />
              <span>Payslips</span>
            </NavLink>
            <NavLink to="/documents" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <Files size={22} />
              <span>Documents</span>
            </NavLink>
          </nav>
        </div>

        <div className="menu-group">
          <div className="menu-label">OTHER</div>
          <nav className="nav-menu">
            <a
              href="https://yougotagift.atlassian.net/servicedesk/customer/portal/14"
              target="_blank"
              rel="noopener noreferrer"
              className="nav-item"
            >
              <LifeBuoy size={22} />
              <span>Support</span>
            </a>
          </nav>
        </div>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={() => setIsLogoutModalOpen(true)}>
            <LogOut size={22} />
            <span>Logout</span>
          </button>
        </div>

        <style>{`
        .sidebar {
          width: 250px;
          height: 100vh;
          background: var(--sidebar-bg);
          padding: 2.5rem 1.5rem;
          display: flex;
          flex-direction: column;
          border-right: 1px solid var(--border-color);
          position: fixed;
          left: 0;
          top: 0;
          z-index: 1000;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .sidebar-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          backdrop-filter: blur(4px);
          z-index: 999;
          animation: fadeIn 0.2s ease-out;
        }

        @media (max-width: 1200px) {
            .sidebar {
                transform: translateX(-100%);
            }
            .sidebar.open {
                transform: translateX(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .logo-container {
          margin-bottom: 3rem;
          padding-left: 0.5rem;
        }

        .logo {
          width: 110px;
          height: auto;
          transition: filter 0.3s ease;
        }

        body.dark-mode .logo {
          filter: invert(1) hue-rotate(180deg) contrast(1.4) saturate(1.2) brightness(1.1);
          mix-blend-mode: screen;
        }
        
        .menu-group {
            margin-bottom: 2.5rem;
        }

        .menu-label {
          font-size: 0.7rem;
          color: var(--text-secondary);
          margin-bottom: 1.25rem;
          padding-left: 1rem;
          letter-spacing: 0.1em;
          font-weight: 700;
        }
        
        .nav-menu {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .nav-item {
          display: flex;
          align-items: center;
          gap: 1.25rem;
          padding: 0.85rem 1.25rem;
          border-radius: 16px;
          color: var(--text-secondary);
          transition: all 0.2s;
          font-weight: 600;
          text-decoration: none;
        }
        
        .nav-item:hover {
          color: #B800C4;
          background: #fdf4ff;
        }

        body.dark-mode .nav-item:hover {
          background: rgba(184, 0, 196, 0.1);
        }
        
        .nav-item.active {
          color: #B800C4;
          background: #fdf4ff;
        }

        body.dark-mode .nav-item.active {
          background: rgba(184, 0, 196, 0.15);
        }

        .sidebar-footer {
            margin-top: auto;
        }

        .logout-btn {
            display: flex;
            align-items: center;
            gap: 1.25rem;
            padding: 0.85rem 1.25rem;
            color: #ef4444;
            font-weight: 700;
            width: 100%;
            text-align: left;
            background: none;
            border: none;
            cursor: pointer;
            border-radius: 16px;
            transition: all 0.2s;
        }
        
        .logout-btn:hover {
            background: #fef2f2;
        }

        body.dark-mode .logout-btn:hover {
            background: rgba(239, 68, 68, 0.1);
        }
      `}</style>
      </aside>

      <LogoutModal
        isOpen={isLogoutModalOpen}
        onClose={() => setIsLogoutModalOpen(false)}
        onConfirm={handleLogoutConfirm}
      />
    </>
  );
};

export default Sidebar;

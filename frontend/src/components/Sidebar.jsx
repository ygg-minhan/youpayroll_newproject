import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, FileText, Files, LifeBuoy, LogOut, User, BookOpen } from 'lucide-react'; // Added User, BookOpen
import { useAuth } from '../context/AuthContext';
import LogoutModal from './LogoutModal';

const Sidebar = () => {
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const navItems = [
    { icon: LayoutDashboard, label: 'Overview', path: '/' },
    { icon: User, label: 'Profile', path: '/profile' }, // Added Profile
    { icon: FileText, label: 'Payslips', path: '/payslips' },
    { icon: Files, label: 'Documents', path: '/documents' },
    { icon: BookOpen, label: 'Tech Wiki', path: '/wiki' },
  ];

  const handleLogoutConfirm = () => {
    logout();
    setIsLogoutModalOpen(false);
    navigate('/login');
  };

  return (
    <>
      <aside className="sidebar">
        <div className="logo-container">
          <img src="http://127.0.0.1:8000/media/branding/logo.jpg" alt="YOU GotaGift Logo" className="logo" />
        </div>

        <div className="menu-label">MAIN MENU</div>

        <nav className="nav-menu">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `nav-item ${isActive ? 'active' : ''}`
              }
            >
              <item.icon size={20} />
              <span>{item.label}</span>
            </NavLink>
          ))}
          {/* Support Link */}
          <NavLink to="/support" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <LifeBuoy size={20} />
            <span>Support</span>
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <button className="logout-link" onClick={() => setIsLogoutModalOpen(true)}>
            <LogOut size={20} />
            <span>Log Out</span>
          </button>
        </div>

        <style>{`
        .sidebar {
          width: 250px;
          height: 100vh;
          background: var(--sidebar-bg);
          padding: 2rem;
          display: flex;
          flex-direction: column;
          border-right: 1px solid var(--border-color);
          position: fixed;
          left: 0;
          top: 0;
          z-index: 50;
        }
        
        .logo-container {
          margin-bottom: 3rem;
        }
        
        .logo-text {
          font-size: 1.5rem;
          font-weight: 700;
          color: var(--primary-color);
        }
        
        .logo {
          width: 130px;
          height: auto;
        }

        @media (max-width: 768px) {
          .logo {
            width: 120px;
          }
        }
        
        .logo-highlight {
           color: var(--secondary-color);
        }
        
        .menu-label {
          font-size: 0.75rem;
          color: var(--text-secondary);
          margin-bottom: 1rem;
          letter-spacing: 0.05em;
          text-transform: uppercase;
        }
        
        .nav-menu {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          flex: 1;
        }
        
        .nav-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem 1rem;
          border-radius: var(--radius-md);
          color: var(--text-secondary); /* Grey icons/text by default */
          transition: all var(--transition-fast);
          font-weight: 500;
        }
        
        /* Hover Effect: Prominent purple */
        .nav-item:hover {
          color: var(--primary-color);
          background: rgba(168, 85, 247, 0.05);
        }
        
        .nav-item.active {
          color: var(--primary-color);
          background: rgba(168, 85, 247, 0.1);
          border-right: 3px solid var(--primary-color); 
        }

        .sidebar-footer {
            margin-top: auto;
        }

        .logout-link {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 1rem;
            color: #ef4444; /* Red font */
            font-weight: 600;
            width: 100%;
            text-align: left;
            border-radius: var(--radius-md);
            transition: background 0.2s;
        }
        
        .logout-link:hover {
            background: #fef2f2;
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

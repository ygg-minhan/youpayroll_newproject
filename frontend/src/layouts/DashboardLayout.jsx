import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const DashboardLayout = () => {
    return (
        <div className="dashboard-layout">
            <Sidebar />
            <main className="main-content">
                <Outlet />
            </main>

            <style>{`
        .dashboard-layout {
          display: flex;
          min-height: 100vh;
          background-color: var(--bg-color);
        }
        
        .main-content {
          margin-left: 250px; /* Width of sidebar */
          flex: 1;
          padding: 2rem;
          max-width: 1600px; 
        }
      `}</style>
        </div>
    );
};

export default DashboardLayout;

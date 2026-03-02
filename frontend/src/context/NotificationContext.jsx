import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useAuth } from './AuthContext';
import { API_BASE_URL } from '../api';

const NotificationContext = createContext(null);

export const NotificationProvider = ({ children }) => {
    const { isAuthenticated } = useAuth();
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchNotifications = useCallback(async () => {
        const token = localStorage.getItem('token');
        if (!token || !isAuthenticated) return;

        try {
            const response = await fetch(`${API_BASE_URL}/user-notifications/`, {
                headers: { 'Authorization': `Token ${token}` }
            });
            if (response.ok) {
                const data = await response.json();
                setNotifications(data);
            }
        } catch (err) {
            console.error('Failed to fetch notifications:', err);
        }
    }, [isAuthenticated]);

    // Initial fetch and polling
    useEffect(() => {
        fetchNotifications();
        const interval = setInterval(fetchNotifications, 30000); // Poll every 30s
        return () => clearInterval(interval);
    }, [fetchNotifications]);

    const markAsRead = async (notifId) => {
        const token = localStorage.getItem('token');
        if (!token) return;

        try {
            const response = await fetch(`${API_BASE_URL}/user-notifications/${notifId}/`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
                body: JSON.stringify({ is_read: true })
            });

            if (response.ok) {
                setNotifications(prev => prev.map(n =>
                    n.id === notifId ? { ...n, is_read: true } : n
                ));
            } else {
                console.error('Failed to mark notification as read on server:', response.status);
            }
        } catch (err) {
            console.error('Failed to mark notification as read:', err);
        }
    };

    const refreshNotifications = () => {
        fetchNotifications();
    };

    const unreadCount = notifications.filter(n => !n.is_read).length;
    const actionRequiredNotification = notifications.find(n => n.notification_type === 'ACTION_REQUIRED' && !n.is_read);

    return (
        <NotificationContext.Provider value={{
            notifications,
            unreadCount,
            actionRequiredNotification,
            markAsRead,
            refreshNotifications,
            loading
        }}>
            {children}
        </NotificationContext.Provider>
    );
};

export const useNotifications = () => {
    const context = useContext(NotificationContext);
    if (!context) {
        throw new Error('useNotifications must be used within a NotificationProvider');
    }
    return context;
};

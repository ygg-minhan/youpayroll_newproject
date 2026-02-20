import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isDarkMode, setIsDarkMode] = useState(localStorage.getItem('theme') === 'dark');

    useEffect(() => {
        const initializeAuth = async () => {
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                const parsedUser = JSON.parse(storedUser);
                setUser(parsedUser);
                setIsAuthenticated(true);

                // Background sync with backend to get latest profile updates
                try {
                    await login(parsedUser.email);
                } catch (err) {
                    console.error('Failed to sync profile on load:', err);
                }
            }

            // Initial Theme Apply
            if (isDarkMode) {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }

            setLoading(false);
        };

        initializeAuth();
    }, []);

    const toggleDarkMode = () => {
        const newMode = !isDarkMode;
        setIsDarkMode(newMode);
        localStorage.setItem('theme', newMode ? 'dark' : 'light');
        if (newMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    };

    const login = async (email) => {
        try {
            // Fetch real user data from backend
            const response = await fetch(`http://127.0.0.1:8000/api/profile-by-email/${email}/`);
            if (response.ok) {
                const profileData = await response.json();

                // Construct full URL for profile picture
                let avatarUrl = profileData.profile_picture;
                if (avatarUrl && !avatarUrl.startsWith('http')) {
                    avatarUrl = `http://127.0.0.1:8000${avatarUrl}`;
                }

                const firstName = profileData.user?.first_name || '';
                const lastName = profileData.user?.last_name || '';
                const fullName = `${firstName} ${lastName}`.trim();

                const userObj = {
                    email: profileData.user?.email || email,
                    name: fullName || profileData.user?.username || 'User',
                    role: profileData.designation || 'Consultant',
                    avatar: avatarUrl || `https://ui-avatars.com/api/?name=${firstName || 'User'}+${lastName}&background=B800C4&color=fff`,
                    consultantId: profileData.consultant_id,
                    gender: profileData.gender,
                    dob: profileData.dob,
                    contractStart: profileData.contract_start,
                    contractEnd: profileData.contract_end,
                    consultantFee: profileData.consultant_fee,
                    reportingTo: {
                        name: profileData.reporting_to_name,
                        role: profileData.reporting_to_role
                    },
                    bankDetails: {
                        accountNumber: profileData.account_number,
                        ifscCode: profileData.ifsc_code,
                        micrCode: profileData.micr_code,
                        branchAddress: profileData.branch_address
                    }
                };
                setUser(userObj);
                setIsAuthenticated(true);
                localStorage.setItem('user', JSON.stringify(userObj));
                if (profileData.token) {
                    localStorage.setItem('token', profileData.token);
                }
                return true;
            } else {
                return false;
            }
        } catch (error) {
            console.error('Login error:', error);
            return false;
        }
    };

    const logout = () => {
        setUser(null);
        setIsAuthenticated(false);
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, login, logout, loading, isDarkMode, toggleDarkMode }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);

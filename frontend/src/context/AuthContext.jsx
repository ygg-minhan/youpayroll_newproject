import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isDarkMode, setIsDarkMode] = useState(localStorage.getItem('theme') === 'dark');

    useEffect(() => {
        // Check localStorage on mount
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
            setIsAuthenticated(true);
        }

        // Initial Theme Apply
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }

        setLoading(false);
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
                const userObj = {
                    email: profileData.user.email,
                    name: `${profileData.user.first_name} ${profileData.user.last_name}`.trim() || profileData.user.username,
                    role: profileData.designation || 'Consultant',
                    avatar: profileData.profile_picture || `https://ui-avatars.com/api/?name=${profileData.user.first_name}+${profileData.user.last_name}&background=0D8ABC&color=fff`,
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
                return true;
            } else {
                // Fallback for demo if user not found in DB
                const mockUser = {
                    email,
                    name: 'Paul Barber',
                    role: 'Consultant',
                    avatar: 'https://ui-avatars.com/api/?name=Paul+Barber&background=0D8ABC&color=fff'
                };
                setUser(mockUser);
                setIsAuthenticated(true);
                localStorage.setItem('user', JSON.stringify(mockUser));
                return true;
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

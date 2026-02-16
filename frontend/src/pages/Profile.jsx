import React, { useState } from 'react';
import { User, Calendar, Mail, Briefcase, CreditCard, Files, Edit2, Moon, Sun, ChevronUp, ChevronDown, Building, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import ProfileImageModal from '../components/ProfileImageModal';
import LogoutModal from '../components/LogoutModal';

const Profile = () => {
    const { user, logout, isDarkMode, toggleDarkMode } = useAuth();

    // Profile Modal State
    const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
    const [profileImage, setProfileImage] = useState(user?.avatar || `https://ui-avatars.com/api/?name=${user?.name || 'User'}&background=0D8ABC&color=fff&size=128`);

    // Bank Details Expand State
    const [isBankDetailsOpen, setIsBankDetailsOpen] = useState(false);

    // Logout Modal State
    const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);

    const navigate = useNavigate();
    const handleProfileSave = (newImage) => {
        setProfileImage(newImage);
        setIsProfileModalOpen(false);
    };

    const handleProfileRemove = () => {
        setProfileImage("https://ui-avatars.com/api/?name=P&background=cbd5e1&color=fff&size=128");
        setIsProfileModalOpen(false);
    };

    const handleLogoutConfirm = () => {
        logout();
        setIsLogoutModalOpen(false);
        navigate('/login');
    };

    return (
        <div className={`profile-page ${isDarkMode ? 'dark' : ''}`}>
            <header className="page-header">
                <h1>My Profile</h1>
                <div className="header-actions">
                    <button className="theme-toggle" onClick={toggleDarkMode}>
                        {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
                    </button>
                    <button className="logout-btn-header" onClick={() => setIsLogoutModalOpen(true)}>
                        <LogOut size={20} />
                        <span>Log Out</span>
                    </button>
                </div>
            </header>

            <div className="profile-grid">
                {/* Left Column: Avatar & Basic Info */}
                <div className="profile-card-large">
                    <div className="avatar-section">
                        <div className="avatar-container-large">
                            <img src={profileImage} alt="Profile" className="avatar-large" />
                            <button className="edit-btn-large" onClick={() => setIsProfileModalOpen(true)}>
                                <Edit2 size={16} color="white" />
                            </button>
                        </div>
                        <h2 className="profile-name-large">{user?.name || 'User'}</h2>
                        <p className="profile-role-large">{user?.role || 'Consultant'}</p>
                    </div>

                    <div className="reporting-card">
                        <div className="info-item">
                            <div className="info-label">
                                <User size={16} className="text-gray-400" />
                                <span>Reporting to</span>
                            </div>
                            <span className="info-value">{user?.reportingTo?.name || 'Admin'} - {user?.reportingTo?.role || 'Manager'}</span>
                        </div>
                    </div>
                </div>

                {/* Right Column: Detailed Info */}
                <div className="details-column">
                    {/* Personal Info Panel */}
                    <div className="info-card">
                        <div className="info-header">
                            <h3>Personal Information</h3>
                        </div>

                        <div className="info-list">
                            <InfoItem icon={Briefcase} label="Consultant ID" value={user?.consultantId || 'N/A'} />
                            <InfoItem icon={User} label="Gender" value={user?.gender || 'N/A'} />
                            <InfoItem icon={Calendar} label="Date Of Birth" value={user?.dob || 'N/A'} />
                            <InfoItem icon={Mail} label="Email" value={user?.email || 'N/A'} />
                            <InfoItem icon={Briefcase} label="Contract Start" value={user?.contractStart || 'N/A'} />
                            <InfoItem icon={Briefcase} label="Contract End" value={user?.contractEnd || 'N/A'} />
                            <InfoItem icon={CreditCard} label="Consultant Fee" value={user?.consultantFee || '0'} />
                        </div>
                    </div>

                    {/* Bank Details Card (Expandable) */}
                    <div className="bank-card">
                        <div
                            className="bank-header"
                            onClick={() => setIsBankDetailsOpen(!isBankDetailsOpen)}
                        >
                            <h3>Your Bank details</h3>
                            {isBankDetailsOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                        </div>

                        {isBankDetailsOpen && (
                            <div className="bank-content fade-in">
                                <InfoItem icon={CreditCard} label="Account number" value={user?.bankDetails?.accountNumber || 'N/A'} />
                                <InfoItem icon={Building} label="IFSC Code" value={user?.bankDetails?.ifscCode || 'N/A'} />
                                <InfoItem icon={Files} label="MICR Code" value={user?.bankDetails?.micrCode || 'N/A'} />
                                <div className="footer-text">
                                    {user?.bankDetails?.branchAddress || 'N/A'}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <ProfileImageModal
                isOpen={isProfileModalOpen}
                currentImage={profileImage}
                onClose={() => setIsProfileModalOpen(false)}
                onSave={handleProfileSave}
                onRemove={handleProfileRemove}
            />

            <LogoutModal
                isOpen={isLogoutModalOpen}
                onClose={() => setIsLogoutModalOpen(false)}
                onConfirm={handleLogoutConfirm}
            />

            <style>{`
                .profile-page {
                    padding-bottom: 2rem;
                    max-width: 1200px;
                    margin: 0 auto;
                }

                .page-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 2rem;
                }

                .page-header h1 {
                    font-size: 2rem;
                    font-weight: 800;
                    color: var(--text-primary);
                }

                .header-actions {
                    display: flex;
                    gap: 1rem;
                }

                .logout-btn-header {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    border: 1px solid #ef4444;
                    color: #ef4444;
                    border-radius: var(--radius-md);
                    font-weight: 600;
                    transition: all 0.2s;
                }

                .logout-btn-header:hover {
                    background: #fef2f2;
                }

                .profile-grid {
                    display: grid;
                    grid-template-columns: 1fr 2fr;
                    gap: 2rem;
                }
                
                @media (max-width: 768px) {
                    .profile-grid {
                        grid-template-columns: 1fr;
                    }
                }

                .profile-card-large {
                    background: var(--card-bg);
                    padding: 2rem;
                    border-radius: var(--radius-lg);
                    box-shadow: var(--shadow-sm);
                    display: flex;
                    flex-direction: column;
                    gap: 2rem;
                    height: fit-content;
                }

                .avatar-section {
                    text-align: center;
                }

                .avatar-container-large {
                    position: relative;
                    width: 150px;
                    height: 150px;
                    margin: 0 auto 1.5rem;
                }
                
                .avatar-large {
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 4px solid var(--bg-color);
                    box-shadow: var(--shadow-md);
                }

                .edit-btn-large {
                    position: absolute;
                    bottom: 5px;
                    right: 5px;
                    background: #d946ef;
                    padding: 8px;
                    border-radius: 50%;
                    border: 3px solid white;
                    display: flex;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                
                .edit-btn-large:hover {
                    transform: scale(1.1);
                }

                .profile-name-large {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: var(--text-primary);
                    margin-bottom: 0.25rem;
                }
                
                .profile-role-large {
                    color: var(--text-secondary);
                    font-weight: 500;
                }

                .details-column {
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }

                .info-card, .reporting-card, .bank-card {
                   background: var(--card-bg);
                   border-radius: var(--radius-lg);
                   padding: 2rem;
                   box-shadow: var(--shadow-sm);
                }
                
                .info-header {
                    margin-bottom: 1.5rem;
                    border-bottom: 1px solid var(--border-color);
                    padding-bottom: 1rem;
                }
                
                .info-header h3 {
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: var(--text-primary);
                }

                .info-list, .bank-content {
                   display: flex;
                   flex-direction: column;
                   gap: 1.25rem;
                }
                
                .bank-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: pointer;
                }
                
                .bank-header h3 {
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: var(--text-primary);
                }
                
                .footer-text {
                    font-size: 0.8rem;
                    color: var(--text-secondary);
                    margin-top: 1rem;
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                }

                .theme-toggle {
                   background: var(--card-bg);
                   color: var(--text-primary);
                   padding: 0.5rem;
                   border-radius: 50%;
                   box-shadow: var(--shadow-sm);
                   border: 1px solid var(--border-color);
                   display: flex;
                   justify-content: center;
                   align-items: center;
                }
            `}</style>
        </div>
    );
};

const InfoItem = ({ icon: Icon, label, value }) => (
    <div className="info-item">
        <div className="info-label">
            <Icon size={18} className="text-gray-400" />
            <span>{label}</span>
        </div>
        <span className="info-value">{value}</span>

        <style>{`
        .info-item {
           display: flex;
           justify-content: space-between;
           align-items: center;
           font-size: 0.95rem;
        }
        
        .info-label {
           display: flex;
           align-items: center;
           gap: 1rem;
           color: var(--text-secondary);
        }
        
        .info-value {
           font-weight: 600;
           color: var(--text-primary);
           text-align: right;
        }
        .text-gray-400 { color: #94a3b8; }
    `}</style>
    </div>
);

export default Profile;

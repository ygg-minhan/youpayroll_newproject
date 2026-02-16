import React, { useState, useEffect } from 'react';
import { Folder, AlertTriangle, Moon, Sun, ArrowRight, X, CheckCircle, Upload, FileText, ChevronRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

// --- Sub-Modals for Admin Workflow ---

// 1. Admin Update Notification Modal
const AdminUpdateModal = ({ isOpen, onAcknowledge, onReject }) => {
   if (!isOpen) return null;
   return (
      <div className="modal-overlay">
         <div className="modal-content admin-modal">
            <h2 className="admin-title">Let’s get this done!</h2>
            <p className="admin-text">
               Please review admin updates to your profile and provide a confirmation screenshot for payment processing.
            </p>
            <div className="modal-actions">
               <button onClick={onReject} className="reject-btn">Reject</button>
               <button onClick={onAcknowledge} className="acknowledge-btn">Acknowledge</button>
            </div>
         </div>
         <style>{`
                .admin-modal { padding: 2rem; max-width: 400px; text-align: left; }
                .admin-title { font-size: 1.5rem; font-weight: 800; margin-bottom: 1rem; color: var(--text-primary); }
                .admin-text { color: var(--text-secondary); margin-bottom: 2rem; line-height: 1.6; }
                .reject-btn { color: #d946ef; background: white; border: 1px solid #d946ef; padding: 0.75rem 1.5rem; border-radius: var(--radius-md); font-weight: 600; flex: 1; cursor: pointer; }
                .acknowledge-btn { color: white; background: #d946ef; border: none; padding: 0.75rem 1.5rem; border-radius: var(--radius-md); font-weight: 600; flex: 1; cursor: pointer; }
            `}</style>
      </div>
   );
};

// 2. Reject Reason Modal
const RejectModal = ({ isOpen, onClose, onSubmit }) => {
   if (!isOpen) return null;
   const [reason, setReason] = useState('');
   const charCount = reason.length;

   return (
      <div className="modal-overlay">
         <div className="modal-content reject-modal">
            <h2 className="admin-title">Incorrect Modifications</h2>
            <p className="admin-text">
               Please specify the reason for the rejection, and the admin will review and make the required changes.
            </p>
            <textarea
               className="reason-input"
               placeholder="Type your message here..."
               maxLength={300}
               value={reason}
               onChange={(e) => setReason(e.target.value)}
            />
            <div className="char-count">{charCount}/300</div>

            <div className="modal-actions-right">
               <button onClick={onClose} className="cancel-link-btn">Cancel</button>
               <button
                  onClick={() => onSubmit(reason)}
                  className="submit-btn"
                  disabled={!reason.trim()}
               >
                  Submit
               </button>
            </div>
         </div>
         <style>{`
                .reject-modal { padding: 2rem; max-width: 450px; }
                .reason-input { width: 100%; height: 120px; padding: 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); resize: none; margin-bottom: 0.5rem; font-family: inherit; }
                .char-count { text-align: right; font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 1.5rem; }
                .modal-actions-right { display: flex; justify-content: flex-end; gap: 1rem; }
                .cancel-link-btn { color: #d946ef; background: none; border: none; font-weight: 600; cursor: pointer; }
                .submit-btn { background: #d946ef; color: white; padding: 0.5rem 1.5rem; border-radius: var(--radius-md); font-weight: 600; cursor: pointer; }
                .submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            `}</style>
      </div>
   );
};

// 3. Updated Details Modal (Shown after Acknowledge)
const UpdatedDetailsModal = ({ isOpen, onClose }) => {
   if (!isOpen) return null;
   return (
      <div className="modal-overlay">
         <div className="modal-content details-modal">
            <button className="close-corner-btn" onClick={onClose}><X size={20} /></button>
            <h3>Take a screenshot of the updated profile</h3>
            <p className="sub-text">Upload the screenshot in the pending document section on the Home page to process the payment</p>

            <div className="updated-field-highlight">
               <div className="field-label">Account Number</div>
               <div className="field-value">1234567890 <span className="highlight-badge">Updated</span></div>
            </div>
         </div>
         <style>{`
                .details-modal { padding: 2.5rem 2rem; max-width: 400px; text-align: center; position: relative; }
                .close-corner-btn { position: absolute; top: 1rem; right: 1rem; color: var(--text-secondary); }
                .details-modal h3 { font-size: 1.25rem; font-weight: 800; margin-bottom: 0.5rem; }
                .sub-text { color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 2rem; }
                .updated-field-highlight { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 1.5rem; border-radius: var(--radius-md); }
                .field-label { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem; }
                .field-value { font-size: 1.25rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
                .highlight-badge { background: #22c55e; color: white; font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; }
            `}</style>
      </div>
   );
};

// 4. Upload Screenshot Modal (Action Required)
const UploadScreenshotModal = ({ isOpen, onClose, onUpload }) => {
   if (!isOpen) return null;
   return (
      <div className="modal-overlay">
         <div className="modal-content upload-modal">
            <button className="close-corner-btn" onClick={onClose}><X size={20} /></button>
            <div className="status-badge-container">
               <span className="status-badge alert">Action required!</span>
            </div>

            <h2 className="admin-title">Action Required!</h2>
            <p className="admin-text">
               Please review admin updates to your profile and provide a confirmation screenshot for payment processing.
            </p>

            <div className="upload-area">
               <Upload size={32} className="upload-icon" />
               <p>Click to upload screenshot</p>
               <span className="file-types">Supports JPG, PNG, SVG</span>
               <input type="file" className="file-input-hidden" onChange={onUpload} />
            </div>
         </div>
         <style>{`
                .upload-modal { padding: 2.5rem 2rem; max-width: 450px; text-align: center; position: relative; }
                .status-badge-container { display: flex; justify-content: flex-start; margin-bottom: 1rem; }
                .status-badge.alert { color: #eab308; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem; }
                .upload-area { border: 2px dashed #cbd5e1; border-radius: var(--radius-lg); padding: 3rem; margin-top: 1.5rem; cursor: pointer; transition: all 0.2s; position: relative; }
                .upload-area:hover { border-color: #d946ef; background: #fdf4ff; }
                .upload-icon { color: #d946ef; margin-bottom: 1rem; }
                .file-types { font-size: 0.75rem; color: var(--text-secondary); display: block; margin-top: 0.5rem; }
                .file-input-hidden { position: absolute; top:0; left:0; width:100%; height:100%; opacity: 0; cursor: pointer; }
            `}</style>
      </div>
   );
};


// --- Main Overview Component ---

const Overview = () => {
   const { user, isDarkMode, toggleDarkMode } = useAuth();

   // --- Admin Workflow State ---
   const [hasAdminUpdate, setHasAdminUpdate] = useState(true); // Mock: Admin made an update
   const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);

   // Reject Flow
   const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);

   // Acknowledge Flow
   const [isUpdatedDetailsOpen, setIsUpdatedDetailsOpen] = useState(false);
   const [isPendingDocActive, setIsPendingDocActive] = useState(false); // Enable tile

   // Upload Flow
   const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
   const [uploadSuccess, setUploadSuccess] = useState(false);

   useEffect(() => {
      // Time Update
      const timer = setInterval(() => setCurrentTime(new Date()), 60000);

      // Greeting Logic
      const hour = new Date().getHours();
      if (hour >= 5 && hour < 12) setGreeting('Good Morning');
      else if (hour >= 12 && hour < 18) setGreeting('Good Afternoon');
      else setGreeting('Good Evening');

      // Mock: Show Admin Modal on load if updates exist
      if (hasAdminUpdate && !isPendingDocActive && !uploadSuccess) {
         const timeout = setTimeout(() => setIsAdminModalOpen(true), 1000);
         return () => clearTimeout(timeout);
      }

      return () => clearInterval(timer);
   }, [hasAdminUpdate, isPendingDocActive, uploadSuccess]);

   const navigate = useNavigate();
   const [currentTime, setCurrentTime] = useState(new Date());
   const [greeting, setGreeting] = useState('Good Morning');

   // --- Handlers ---

   const handleAcknowledge = () => {
      setIsAdminModalOpen(false);
      setIsUpdatedDetailsOpen(true);
      // After seeing details, the "Pending Documents" tile becomes active
      setIsPendingDocActive(true);
   };

   const handleReject = () => {
      setIsAdminModalOpen(false);
      setIsRejectModalOpen(true);
   };

   const handleSubmitRejection = (reason) => {
      console.log("Rejected with reason:", reason);
      setIsRejectModalOpen(false);
      setHasAdminUpdate(false); // Clear update state as it's rejected
      // Ideally show a "Submitted" toast here
   };

   const handlePendingDocClick = () => {
      if (isPendingDocActive) {
         setIsUploadModalOpen(true);
      }
   };

   const handleUpload = (e) => {
      if (e.target.files[0]) {
         // Mock Upload
         setTimeout(() => {
            setIsUploadModalOpen(false);
            setUploadSuccess(true);
            setIsPendingDocActive(false); // Task done
            setHasAdminUpdate(false); // Clear notification
         }, 1000);
      }
   };

   const formattedDate = currentTime.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

   return (
      <div className={`overview-page ${isDarkMode ? 'dark' : ''}`}>
         <div className="content-left">
            {/* Header */}
            <header className="header-section">
               <div className="greeting-container">
                  <span className="wave">👋</span>
                  <h2>Hi {user?.name?.split(' ')[0] || 'User'}, {greeting}</h2>
               </div>
               <h1 className="hero-title">Have a Productive day!</h1>
               <p className="current-date">{formattedDate}</p>
            </header>

            {/* Upload Success Message */}
            {uploadSuccess && (
               <div className="success-banner pop-in">
                  <div className="success-content">
                     <CheckCircle size={24} className="text-white" />
                     <div>
                        <h3>Document uploaded successfully</h3>
                        <p>Admin will review your submission shortly.</p>
                     </div>
                  </div>
               </div>
            )}

            {/* Dashboard Cards */}
            <div className="cards-grid">
               {/* Payslips Card (Navigates to /payslips) */}
               <div className="dashboard-card payslip-card" onClick={() => navigate('/payslips')}>
                  <div className="card-content">
                     <h3>Your</h3>
                     <h2>Payslips</h2>
                  </div>
                  <div className="card-icon-container bg-purple">
                     <Folder size={32} color="white" />
                     <div className="add-badge">+</div>
                  </div>
               </div>

               {/* Pending Documents Card */}
               <div
                  className={`dashboard-card documents-card ${isPendingDocActive ? 'active-action' : 'disabled-card'}`}
                  onClick={handlePendingDocClick}
               >
                  <div className="card-content">
                     <h3>Pending</h3>
                     <h2>Documents</h2>
                     {isPendingDocActive && <span className="action-tag">Action Required</span>}
                  </div>
                  <div className="card-icon-container bg-pink">
                     <AlertTriangle size={32} color="white" />
                  </div>
               </div>
            </div>
         </div>

         {/* Right Profile Sidebar */}
         <aside className="profile-section">
            <div className="profile-header-top">
               <h3>Profile Summary</h3>
               <button className="theme-toggle" onClick={toggleDarkMode}>
                  {isDarkMode ? <Sun size={16} /> : <Moon size={16} />}
               </button>
            </div>

            <div className="profile-card-mini">
               <div className="avatar-container-mini">
                  <img src={user?.avatar || `https://ui-avatars.com/api/?name=${user?.name || 'User'}&background=0D8ABC&color=fff&size=128`} alt="Profile" className="avatar-mini" />
               </div>
               <h2 className="profile-name">{user?.name || 'User'}</h2>
               <p className="profile-role">{user?.role || 'Consultant'}</p>

               <Link to="/profile" className="view-profile-btn">
                  View Full Profile <ArrowRight size={16} />
               </Link>
            </div>

            <div className="quick-stats-card">
               <h3>Quick Stats</h3>
               <div className="stat-row">
                  <span>Leave Balance</span>
                  <span className="stat-value">12 Days</span>
               </div>
               <div className="stat-row">
                  <span>Next Payday</span>
                  <span className="stat-value">Oct 31</span>
               </div>
            </div>

            <footer className="profile-footer">
               UCL Cyberpark branch, Nellikode P.O, Calicut 673016
            </footer>
         </aside>

         {/* --- Modals --- */}
         <AdminUpdateModal
            isOpen={isAdminModalOpen}
            onAcknowledge={handleAcknowledge}
            onReject={handleReject}
         />

         <RejectModal
            isOpen={isRejectModalOpen}
            onClose={() => setIsRejectModalOpen(false)}
            onSubmit={handleSubmitRejection}
         />

         <UpdatedDetailsModal
            isOpen={isUpdatedDetailsOpen}
            onClose={() => setIsUpdatedDetailsOpen(false)}
         />

         <UploadScreenshotModal
            isOpen={isUploadModalOpen}
            onClose={() => setIsUploadModalOpen(false)}
            onUpload={handleUpload}
         />

         <style>{`
                /* Existing Styles preserved */
                .overview-page {
                   display: grid;
                   grid-template-columns: 2fr 1fr;
                   gap: 2rem;
                   height: 100%;
                }

                .content-left {
                   display: flex;
                   flex-direction: column;
                   gap: 3rem;
                }
                
                /* Keep previous header styles */
                .greeting-container { display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary); margin-bottom: 0.5rem; font-weight: 500; font-size: 1.1rem; }
                .hero-title { font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem; }
                .current-date { color: var(--text-secondary); font-size: 1rem; }

                /* Card Styles */
                .cards-grid { display: flex; flex-direction: column; gap: 2rem; }
                .dashboard-card {
                   background: var(--card-bg);
                   border-radius: var(--radius-lg);
                   padding: 2rem;
                   display: flex;
                   justify-content: space-between;
                   align-items: center;
                   box-shadow: var(--shadow-sm);
                   min-height: 180px;
                   transition: transform 0.2s;
                   cursor: pointer;
                }
                .dashboard-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
                
                .card-content h3 { font-size: 1.5rem; font-weight: 600; color: var(--text-primary); }
                .card-content h2 { font-size: 2rem; font-weight: 800; color: var(--text-primary); }
                
                .card-icon-container { width: 80px; height: 60px; border-radius: 20px; display: flex; align-items: center; justify-content: center; position: relative; }
                .bg-purple { background: #d946ef; }
                .bg-pink { background: #db2777; }
                .add-badge { position: absolute; bottom: -5px; left: -5px; background: white; width: 20px; height: 20px; border-radius: 50%; color: #d946ef; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }

                /* Pending Document Logic */
                .disabled-card { opacity: 0.6; cursor: default; }
                .disabled-card:hover { transform: none; box-shadow: var(--shadow-sm); }
                .active-action { border: 2px solid #eab308; background: #fefce8; }
                .action-tag { display: inline-block; background: #eab308; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 700; margin-top: 0.5rem; }

                /* Success Banner */
                .success-banner { background: #22c55e; color: white; padding: 1.5rem; border-radius: var(--radius-lg); margin-bottom: 1rem; box-shadow: var(--shadow-md); animation: slideDown 0.5s ease-out; }
                .success-content { display: flex; align-items: center; gap: 1rem; }
                .success-content h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem; }
                .success-content p { font-size: 0.9rem; opacity: 0.9; }
                @keyframes slideDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

                /* Profile Sidebar (Right) */
                .profile-section { background: var(--card-bg); padding: 2rem; border-left: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 2rem; }
                .profile-header-top { display: flex; justify-content: space-between; align-items: center; }
                .profile-header-top h3 { font-size: 1rem; font-weight: 600; color: var(--text-primary); }
                .profile-card-mini { text-align: center; background: var(--bg-color); padding: 2rem; border-radius: var(--radius-lg); }
                .avatar-container-mini { width: 100px; height: 100px; margin: 0 auto 1rem; }
                .avatar-mini { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; box-shadow: var(--shadow-sm); }
                .profile-name { font-weight: 700; color: var(--text-primary); margin-bottom: 0.25rem; }
                .profile-role { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem; }
                .view-profile-btn { display: inline-flex; align-items: center; gap: 0.5rem; color: #d946ef; font-weight: 600; font-size: 0.9rem; padding: 0.5rem 1rem; border: 1px solid #d946ef; border-radius: var(--radius-md); transition: all 0.2s; }
                .view-profile-btn:hover { background: #d946ef; color: white; }
                .quick-stats-card { background: var(--bg-color); padding: 1.5rem; border-radius: var(--radius-lg); }
                .quick-stats-card h3 { font-size: 0.9rem; margin-bottom: 1rem; }
                .stat-row { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.875rem; color: var(--text-secondary); }
                .stat-value { font-weight: 600; color: var(--text-primary); }
                .profile-footer { font-size: 0.75rem; color: var(--text-secondary); text-align: center; margin-top: auto; }
                .theme-toggle { background: var(--card-bg); border: 1px solid var(--border-color); color: var(--text-primary); padding: 0.5rem; border-radius: 50%; cursor: pointer; }
            `}</style>
      </div>
   );
};

export default Overview;

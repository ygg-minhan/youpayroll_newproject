import React, { useState } from 'react';
import { X, ArrowRight } from 'lucide-react';

const ProfileImageModal = ({ isOpen, onClose, currentImage, onRemove, onSave }) => {
    if (!isOpen) return null;

    const [view, setView] = useState('main'); // 'main', 'change', 'remove'
    const [selectedImage, setSelectedImage] = useState(null);

    const handleClose = () => {
        setView('main');
        setSelectedImage(null);
        onClose();
    }

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setSelectedImage(reader.result);
                setView('change');
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content profile-modal">
                {/* Header */}
                <div className="modal-header">
                    <h2>
                        {view === 'main' && 'Profile Picture'}
                        {view === 'change' && 'New Profile Picture'}
                        {view === 'remove' && 'Remove Profile Picture?'}
                    </h2>
                    <button className="close-btn" onClick={handleClose}>
                        <X size={20} />
                    </button>
                </div>

                {view === 'main' && (
                    <div className="modal-body-content">
                        <div className="image-preview-large">
                            <img src={currentImage} alt="Current Profile" />
                        </div>

                        <p className="modal-subtitle">
                            To make your profile unique, you can easily change or remove your profile picture.
                        </p>

                        <div className="modal-actions">
                            <button onClick={() => setView('remove')} className="remove-btn">Remove</button>
                            <label className="change-btn">
                                Change
                                <input type="file" hidden accept="image/*" onChange={handleFileChange} />
                            </label>
                        </div>
                    </div>
                )}

                {view === 'change' && (
                    <div className="modal-body-content">
                        <div className="image-preview-large">
                            <img src={selectedImage} alt="New Profile" />
                        </div>

                        <p className="modal-subtitle">
                            Do you want to save this as your new profile picture?
                        </p>

                        <div className="modal-actions">
                            <button onClick={() => { setView('main'); setSelectedImage(null); }} className="cancel-btn">Cancel</button>
                            <button onClick={() => { onSave(selectedImage); handleClose(); }} className="save-btn-full">Save Changes</button>
                        </div>
                    </div>
                )}

                {view === 'remove' && (
                    <div className="modal-body-content">
                        <div className="remove-preview-container">
                            <div className="img-circle">
                                <img src={currentImage} alt="Old" />
                            </div>
                            <ArrowRight className="arrow-icon" />
                            <div className="img-circle placeholder-circle">
                                <span>P</span>
                            </div>
                        </div>

                        <p className="modal-subtitle">
                            Your previous picture will be replaced with the new image.
                        </p>

                        <div className="modal-actions">
                            <button onClick={() => setView('main')} className="cancel-btn">Cancel</button>
                            <button onClick={() => { onRemove(); handleClose(); }} className="confirm-remove-btn">Remove</button>
                        </div>
                    </div>
                )}
            </div>

            <style>{`
        .profile-modal {
           width: 100%;
           max-width: 480px;
           padding: 2rem;
           background: white;
           border-radius: var(--radius-lg);
        }
        
        .modal-header {
           display: flex;
           justify-content: space-between;
           align-items: center;
           margin-bottom: 2rem;
        }
        
        .modal-header h2 {
           font-size: 1.5rem;
           font-weight: 700;
           color: var(--text-primary);
           margin: 0;
           text-align: left;
        }
        
        .close-btn {
           color: var(--text-secondary);
           padding: 0.5rem;
           border-radius: 50%;
           transition: background 0.2s;
        }
        .close-btn:hover {
            background: #f1f5f9;
        }
        
        .modal-body-content {
           text-align: center;
        }
        
        .image-preview-large {
           width: 140px;
           height: 140px;
           margin: 0 auto 1.5rem;
           border-radius: 50%;
           overflow: hidden;
           border: 4px solid white;
           box-shadow: var(--shadow-md);
        }
        
        .image-preview-large img {
           width: 100%;
           height: 100%;
           object-fit: cover;
        }
        
        .modal-subtitle {
           color: var(--text-secondary);
           margin-bottom: 2rem;
           font-size: 0.95rem;
           line-height: 1.5;
           padding: 0 1rem;
        }
        
        .modal-actions {
           display: flex;
           gap: 1rem;
        }
        
        button, label {
            transition: transform 0.1s, opacity 0.2s;
        }
        button:active, label:active {
            transform: scale(0.98);
        }

        /* Styles for Main View Buttons */
        .remove-btn {
           flex: 1;
           padding: 0.875rem;
           border: 1px solid #e2e8f0; /* Light gray border */
           background: white;
           color: #ef4444; /* Red text */
           border-radius: var(--radius-md);
           font-weight: 600;
           cursor: pointer;
        }
        .remove-btn:hover {
            background: #fef2f2;
            border-color: #fecaca;
        }
        
        .change-btn {
           flex: 1;
           padding: 0.875rem;
           background: #d946ef; /* Purple */
           color: white;
           border-radius: var(--radius-md);
           font-weight: 600;
           cursor: pointer;
           display: flex;
           align-items: center;
           justify-content: center;
        }
        .change-btn:hover {
            background: #c026d3;
        }

        /* Styles for Change/Remove Confirmation Buttons */
        .cancel-btn {
           flex: 1;
           padding: 0.875rem;
           border: 1px solid #e2e8f0;
           background: white;
           color: var(--text-primary);
           border-radius: var(--radius-md);
           font-weight: 600;
           cursor: pointer;
        }
        .cancel-btn:hover {
            background: #f8fafc;
        }
        
        .save-btn-full {
            flex: 1;
            background: #d946ef;
            color: white;
            padding: 0.875rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            cursor: pointer;
        }
        
        .confirm-remove-btn {
           flex: 1;
           padding: 0.875rem;
           background: #ef4444;
           color: white;
           border-radius: var(--radius-md);
           font-weight: 600;
           cursor: pointer;
        }

        /* Remove Preview */
        .remove-preview-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .img-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid #e2e8f0;
        }
        
        .img-circle img {
           width: 100%;
           height: 100%;
           object-fit: cover;
        }
        
        .placeholder-circle {
           background: #cbd5e1;
           display: flex;
           align-items: center;
           justify-content: center;
           font-size: 2rem;
           font-weight: bold;
           color: white;
        }
        
        .arrow-icon {
           color: #d946ef;
        }
      `}</style>
        </div>
    );
};

export default ProfileImageModal;

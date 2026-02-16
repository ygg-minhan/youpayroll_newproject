import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";

const Login = () => {
    const { login, isAuthenticated } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/', { replace: true });
        }
    }, [isAuthenticated, navigate]);

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const decoded = jwtDecode(credentialResponse.credential);
            const success = await login(decoded.email);
            if (success) {
                navigate('/');
            }
        } catch (error) {
            console.error('Google login decode error:', error);
        }
    };

    const handleGoogleError = () => {
        console.log('Login Failed');
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="brand-header">
                    <img src="http://127.0.0.1:8000/media/branding/logo.jpg" alt="YOU GotaGift Logo" className="logo" />
                    <p className="welcome-text">Welcome to YOUPayroll</p>
                    <p className="subtitle">Please sign in with your Google account to continue</p>
                </div>

                <div className="social-login-section">
                    <div className="google-login-wrapper" style={{ display: 'flex', justifyContent: 'center' }}>
                        <GoogleLogin
                            onSuccess={handleGoogleSuccess}
                            onError={handleGoogleError}
                            useOneTap
                            theme="outline"
                            size="large"
                            width="320"
                            shape="pill"
                        />
                    </div>
                </div>

                <div className="login-footer">
                    <p>By signing in, you agree to our Terms of Service</p>
                </div>
            </div>

            <style>{`
        .login-container {
          height: 100vh;
          width: 100vw;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        }

        .login-card {
          background: white;
          padding: 3.5rem 2.5rem;
          border-radius: 2rem;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
          width: 100%;
          max-width: 420px;
          text-align: center;
          border: 1px solid rgba(255, 255, 255, 0.8);
          backdrop-filter: blur(10px);
        }

        .brand-header {
          margin-bottom: 2.5rem;
        }

        .logo {
          width: 180px;
          height: auto;
          margin-bottom: 2rem;
        }

        .welcome-text {
          font-size: 1.5rem;
          font-weight: 800;
          color: #1e293b;
          margin-bottom: 0.5rem;
        }

        .subtitle {
          font-size: 0.95rem;
          color: #64748b;
          line-height: 1.5;
        }

        .social-login-section {
            margin: 2rem 0;
        }
        
        .login-footer {
            margin-top: 2rem;
            font-size: 0.8rem;
            color: #94a3b8;
        }

        @media (max-width: 768px) {
          .login-card {
            max-width: 90%;
            padding: 2.5rem 1.5rem;
          }
          .logo {
            width: 130px;
          }
        }
      `}</style>
        </div>
    );
};

export default Login;

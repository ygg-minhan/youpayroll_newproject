const API_URL = 'http://127.0.0.1:8000/api';

export const getProfile = async (token) => {
    const response = await fetch(`${API_URL}/profile/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
};

export const getPayslips = async (token) => {
    const response = await fetch(`${API_URL}/payslips/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
};

export const uploadDocument = async (token, formData) => {
    const response = await fetch(`${API_URL}/documents/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    return response.json();
};

export const getNotifications = async (token) => {
    const response = await fetch(`${API_URL}/notifications/`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.json();
};

export const updateProfile = async (token, data) => {
    const response = await fetch(`${API_URL}/profile/`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
};

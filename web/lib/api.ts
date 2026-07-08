import axios from 'axios';

const getBaseURL = () => {
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        return `http://${hostname}:5000/api/v1`;
    }
    return process.env.NEXT_PUBLIC_API_URL || 'http://192.168.1.5:5000/api/v1';
};

const api = axios.create({
    baseURL: getBaseURL(),
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
    (config) => {
        // Safe check for localStorage in SSR
        if (typeof window !== 'undefined') {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor for global error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            // Token expired or unauthorized
            if (typeof window !== 'undefined') {
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
        }

        const message = error.response
            ? `API Error (${error.response.status}): ${JSON.stringify(error.response.data)}`
            : `Network Error: ${error.message} - BaseURL: ${error.config?.baseURL}${error.config?.url}`;
        
        console.error('API Error:', message);
        return Promise.reject(error);
    }
);

export { api };
export default api;

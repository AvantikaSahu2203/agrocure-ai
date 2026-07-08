import axios from 'axios';

const getBaseURL = () => {
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        const port = window.location.port;
        // If we are developing locally, use port 5000. Under production Nginx, routing is handled on port 80.
        if (hostname === 'localhost' || hostname === '127.0.0.1' || port === '3000') {
            return `http://${hostname}:5000/api/v1`;
        }
        // In production, Nginx proxies API calls under /api/v1 (port 80)
        return `http://${hostname}/api/v1`;
    }
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';
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

import axios from 'axios';
import Constants from 'expo-constants';

const getBaseUrl = () => {
  const host = Constants.expoConfig?.hostUri?.split(':').shift();
  if (host) {
    return `http://${host}:8000`;
  }
  return 'http://127.0.0.1:8000'; // Fallback
};

const apiClient = axios.create({
  baseURL: getBaseUrl(),
  timeout: 30000,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export default apiClient;

import axios from "axios";

// Base URL for the backend API
const API_URL = "http://127.0.0.1:8000/api";

// AUTHENTICATION
export const login_user = async (username, password) => {
    return await axios.post(`${API_URL}/token/`, {username, password});
};

export const register_user = async (username, password) => {
    return await axios.post(`${API_URL}/register/`, {username, password});
};

// DATA FETCHING from HISTORY
export const get_history = async (token) => {
    return await axios.get(`${API_URL}/equipment/`, {
        headers: {Authorization: `Bearer ${token}`}
    });
};

// FILE UPLOAD
export const upload_file = async (file, token) => {
    const form_data = new FormData();
    form_data.append("file", file);
    return await axios.post(`${API_URL}/equipment/`, form_data, {
        headers: {"Content-Type": "multipart/form-data", Authorization: `Bearer ${token}`},
    });
};

// PDF DOWNLOAD
// Function to handle PDF data as Blobs
export const download_PDF = async (reportId, token) => {
  return await axios.get(`${API_URL}/report/${reportId}/`, {
    headers: {Authorization: `Bearer ${token}`}, responseType: 'blob', 
  });
};

// CSV DOWNLOAD
// Function to handle CSV data as text
export const download_CSV = async (csvId, token) => {
  return await axios.get(`${API_URL}/csv/${csvId}/`, {
    headers: {Authorization: `Bearer ${token}`},
  });
};
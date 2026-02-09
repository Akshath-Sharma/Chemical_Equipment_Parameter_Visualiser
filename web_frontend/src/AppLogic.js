import {useState, useEffect} from "react";
import {login_user, register_user, get_history, upload_file, download_PDF, download_CSV} from "./api"; 

export const useAppLogic = () => {
    // STATES 
    const [token, set_token] = useState(null);
    const [username, set_username] = useState("");
    const [password, set_password] = useState("");
    const [is_registering, set_is_registering] = useState(false);
    const [file, set_file] = useState(null);
    const [stats, set_stats] = useState(null);
    const [history, set_history] = useState([]);
    const [error, set_error] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [show_distribution, set_show_distribution] = useState(false);
    const [show_csv_modal, set_show_csv_modal] = useState(false);
    const [csv_data, set_csv_data] = useState(null);
    const load_history = async (authToken) => {
        try {
        const res = await get_history(authToken);
        set_history(res.data);
        } catch (err) {
        console.error("Failed to load history", err);
        }
    };

    // Tooltip generator for equipment breakdown
    const get_breakdown_Tooltip = () => {
        if (!stats || !stats.type_distribution) return "";
        let text = "Equipment Breakdown:\n";
        Object.entries(stats.type_distribution).forEach(([type, count]) => {
        text += `• ${type}: ${count}\n`;
        });
        return text;
    };

    // Only loading history on initial login or token changes using effects
    useEffect(() => {
        const storedToken = sessionStorage.getItem("token");
        if (storedToken && !token) {
            set_token(storedToken);
        }
        if (token) load_history(token);
    }, [token]);

    const handle_authentication = async (e) => {
        e.preventDefault();
        set_error("");
        if (!username || !password){
        set_error("Please fill in all fields.");
        return;
        }
        try{
        if (is_registering){
            await register_user(username, password);
            set_is_registering(false);
            alert("Account created! Please log in.");
        } else{
            const res = await login_user(username, password);
            const access_token = res.data.access;
            set_token(access_token);
            sessionStorage.setItem("token", access_token);
            load_history(access_token); 
        }
        } catch (err){
        set_error("Authentivation failed. Check your details.");
        }
    };

    // Very important function to clear all user data onlogout and prevent data leaks between sessions
    const logout = () => {
        set_token(null);
        sessionStorage.removeItem("token");
        set_stats(null);
        set_history([]);
        set_username("");
        set_password("");
        set_file(null); 
        set_error("");
        set_show_distribution(false);
        set_show_csv_modal(false);
        set_csv_data(null);
    };

    const handle_upload = async () => {
        if (!file) return;
        setIsLoading(true); 
        set_error("");
        try{
        const res = await upload_file(file, token);
        set_stats(res.data);
        load_history(token); 
        } catch (err){
        set_error("Upload failed.");
        } finally{
            setIsLoading(false);
        }
    };

    const handle_download_PDF = async (reportId) => {
        try{
        const response = await download_PDF(reportId, token);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `report_${reportId}.pdf`);
        document.body.appendChild(link);
        link.click(); 
        link.parentNode.removeChild(link);
        window.URL.revokeObjectURL(url);
        } catch (err){
        console.error("PDF download error:", err);
        alert("Could not download PDF. Check browser console for details.");
        }
    };

    const handle_view_CSV = async (csvId) => {
        try {
            const response = await download_CSV(csvId, token);
            const csv_text = response.data;
            
            // Parse CSV text
            const lines = csv_text.trim().split('\n');
            if (lines.length === 0) {
                alert("CSV file is empty.");
                return;
            }
            
            const headers = lines[0].split(',').map(h => h.trim());
            const rows = lines.slice(1).map(line => {
                const values = line.split(',').map(v => v.trim());
                const row = {};
                headers.forEach((header, index) => {
                    row[header] = values[index] || '';
                });
                return row;
            });
            
            set_csv_data({ headers, rows });
            set_show_csv_modal(true);
        } catch (err) {
            alert("Could not view CSV file.");
        }
    };

    // EXPORT 
    return {
        token, username, set_username, password, set_password,
        is_registering, set_is_registering, file, set_file,
        stats, history, error, isLoading, show_distribution,
        handle_authentication, logout, handleUpload: handle_upload, handleDownloadPDF: handle_download_PDF,
        getBreakdownTooltip: get_breakdown_Tooltip, set_show_distribution,
        show_csv_modal, set_show_csv_modal, csv_data, set_csv_data,
        handleViewCSV: handle_view_CSV
    };
};
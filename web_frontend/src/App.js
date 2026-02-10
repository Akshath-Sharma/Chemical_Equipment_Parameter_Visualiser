import React, {useState} from 'react';
import {Chart as ChartJS,CategoryScale,LinearScale,BarElement,Title,Tooltip, Legend,ArcElement} from "chart.js";
import {Bar,Pie} from "react-chartjs-2";
import "./App.css";
import {useAppLogic} from "./AppLogic";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function App() {
  const{
    token, username, set_username, password, set_password,
    is_registering, set_is_registering, file, set_file,
    stats, history, error, isLoading, show_distribution, 
    handle_authentication, logout, handleUpload: handle_upload, handleDownloadPDF: handle_download_PDF,
    set_show_distribution, show_csv_modal, set_show_csv_modal, csv_data,
    handleViewCSV: handle_view_CSV,
  } = useAppLogic();

  const [selectedHistory, setSelectedHistory] = useState(null);
  const [selectedPos, setSelectedPos] = useState(null); // {x, y} for context menu positioning
  
  // --- LOGIN SCREEN ---
  if (!token){
    return (
      <div className={`authentication_container ${is_registering ? "register_bg" : "login_bg"}`}>        
        <div className="authentication_card">          <h1 className="login_title">🧪 Equip Visualizer</h1>
          <h3 className="panel_title">{is_registering ? "Create Account" : "Welcome Back"}</h3>
          <form onSubmit={handle_authentication}>
            <input 
              className="input_field"
              type="text" placeholder="Username" 
              value={username} onChange={(e) => set_username(e.target.value)} 
            />
            <input 
              className="input_field"
              type="password" placeholder="Password" 
              value={password} onChange={(e) => set_password(e.target.value)} 
            />
            <button type="submit" className="primary_button">
              {is_registering ? "Sign Up" : "Log In"}
            </button>
          </form>
          <p className="link_text" onClick={() => {set_is_registering(!is_registering)}}>
            {is_registering ? "Already have an account? Log In" : "Need an account? Sign Up"}
          </p>
          {error && <p className="error-msg">{error}</p>}
        </div>
      </div>
    );
  }

  // --- MAIN DASHBOARD ---
  return (
    <div className="app_container">
      <nav className="topbar">
        <h2>🧪 Chemical Equipment Parameter Visualizer Dashboard</h2>
        <button onClick={logout} className="logout_button">Logout</button>
      </nav>
      <div className="dashboard_grid">
        {/*LEFT PANEL*/}
        <aside className="left_panel">
          <div className="panel_card full_height">
            <h3 className="panel_title">Equipment Data Preview</h3>
            {stats && stats.equipment_data ? (
              <div className="table_container">
                <table className="data_table">
                  <thead>
                    <tr>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.equipment_data.slice(0, 10).map((row, index) => (
                      <tr key={index}>
                        <td>{row.type}</td>
                        <td>{row.flowrate}</td>
                        <td>{row.pressure}</td>
                        <td>{row.temperature}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="footer_text">*Showing first 10 rows</p>
              </div>
            ) : (
              <p className="empty_text">No data loaded.</p>
            )}
          </div>
        </aside>

        {/*CENTER PANEL*/}
        <main className="center_panel">
          <div className="panel_card upload_section">
            <div className="upload_row">
              <label className="file_upload_button">
                Browse files...
                <input type="file" onChange={(e) => set_file(e.target.files[0])}/>
              </label>
              <span className="file_name">{file ? file.name : "No file selected."}</span>
              <button onClick={handle_upload} className="anaylse_button">Analyze CSV File</button>
            </div>
          </div>

          <div className="panel_card chart_section">
            <h3 className="panel_title">📊 Summary</h3>
            {stats ? (
              <>
                {show_distribution ? (
                  <div className="pie_chart_fullscreen">
                    <div className="pie_chart_header">
                      <h2 style={{ color: '#2d3748', margin: 0 }}>Equipment Type Distribution</h2>
                      <button onClick={() => set_show_distribution(false)} className="back_button">
                        ← Back to Summary
                      </button>
                    </div>
                    <div className="pie_chart_wrapper">
                      <Pie 
                        data={{
                          labels: Object.keys(stats.type_distribution),
                          datasets: [{
                            data: Object.values(stats.type_distribution),
                            backgroundColor: ['#48bb78', '#38a169', '#2d5a27', '#1a3a16', '#a8e063', '#86efac'],
                          }]
                        }} 
                        options={{ 
                          maintainAspectRatio: false,
                          plugins: {
                            legend: {
                              position: 'bottom',
                              labels: { 
                                boxWidth: 15, 
                                padding: 15,
                                font: { size: 13 }
                              }
                            },
                            tooltip: {
                              callbacks: {
                                label: function(context) {
                                  const label = context.label || '';
                                  const value = context.parsed || 0;
                                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                  const percentage = ((value / total) * 100).toFixed(1);
                                  return `${label}: ${value} (${percentage}%)`;
                                }
                              }
                            },
                            datalabels: {
                              color: '#fff',
                              font: {
                                weight: 'bold',
                                size: 14
                              },
                              formatter: (value, context) => {
                                return value;
                              }
                            }
                          }
                        }} 
                      />
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="stats_row">
                      <div 
                        className="stat_card clickable" 
                        onClick={() => set_show_distribution(true)} 
                      >
                        <div className="star_badge">★</div>
                        <div className="card_content_wrapper">
                          <div className="stat_value total_count_display">{stats.total_count}</div>
                          <div className="stat_label">Total</div>
                        </div>
                      </div>                      
                      <div className="stat_card">
                        <div className="stat_value">{stats.averages.flowrate.toFixed(2)}</div>
                        <div className="stat_label">AvgFlowrate</div>
                      </div>
                      <div className="stat_card">
                        <div className="stat_value">{stats.averages.pressure.toFixed(2)}</div>
                        <div className="stat_label">AvgPressure</div>
                      </div>
                      <div className="stat_card">
                        <div className="stat_value">{stats.averages.temperature.toFixed(2)}</div>
                        <div className="stat_label">AvgTemperature</div>
                      </div>
                    </div>
                    
                    <div className="chart_container">
                      <Bar 
                        data={{
                          labels: Object.keys(stats.type_distribution),
                          datasets: [{
                            label: 'Count',
                            data: Object.values(stats.type_distribution),
                            backgroundColor: '#48bb78',
                            borderColor: '#2d5a27',
                            borderWidth: 1,
                          }]
                        }} 
                        options={{ 
                          responsive: true, 
                          maintainAspectRatio: false, 
                          plugins: {legend: {onClick: () => {}}},
                          scales: {
                            x: { ticks: {maxRotation: 45, minRotation: 45, autoSkip: false } },
                            y: { beginAtZero: true }
                          } 
                        }}
                      />
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className="empty-state">
                {isLoading ? (
                  <div className="loading_text">
                    <span className="spinner"></span> Processing Data...
                  </div>
                ) : !file ? (
                  "Please upload a CSV file to begin analysis."
                ) : (
                  "File selected! Click 'Analyze CSV File' to view results."
                )}
              </div>
            )}
          </div>
        </main>

        {/*RIGHT PANEL*/}
        <aside className="right_panel">
          <div className="panel_card full_height">
            <h3 className="panel_title">📜 History</h3>
            <p className="subtitle">Last 5 Uploads</p>
            <ul className="history_list">
              {history.length === 0 ? <p className="empty-text">No history found.</p> : history.map((item) => (
                <li
                  key={item.id}
                  className="history_item"
                  onClick={() => { setSelectedPos(null); setSelectedHistory(item); }}
                  onContextMenu={(e) => { e.preventDefault(); setSelectedPos({ x: e.clientX, y: e.clientY }); setSelectedHistory(item); }}
                >
                   <span className="doc-icon">📄</span>
                   <div className="history_info">
                     <span className="history_name">{item.filename}</span>
                     <span className="history_date">{new Date(item.upload_date).toLocaleDateString()}</span>
                   </div>
                   <div className="history_buttons">
                     <button onClick={(e) => { e.stopPropagation(); handle_view_CSV(item.id); }} className="csv_button"><span className="button_icon">📊</span><span className="button_label">View CSV</span></button>
                     <button onClick={(e) => { e.stopPropagation(); handle_download_PDF(item.id); }} className="pdf_button"><span className="button_icon">📑</span><span className="button_label">PDF</span></button>
                   </div>
                </li>
              ))}
            </ul>

            {selectedHistory && (
              <div className="modal_overlay" onClick={() => { setSelectedHistory(null); setSelectedPos(null); }}>
                <div
                  className="modal_content"
                  onClick={(e) => e.stopPropagation()}
                  style={{
                    maxWidth: '360px',
                    position: 'fixed',
                    left: selectedPos ? `${selectedPos.x}px` : '50%',
                    top: selectedPos ? `${selectedPos.y}px` : '50%',
                    transform: selectedPos ? 'translate(0, 0)' : 'translate(-50%, -50%)',
                    zIndex: 9999,
                  }}
                >
                  <div className="modal_header">
                    <h3 style={{margin: 0}}>{selectedHistory.filename}</h3>
                    <button className="modal_close" onClick={() => setSelectedHistory(null)}>✕</button>
                  </div>
                  <div style={{padding: '16px 24px'}}>
                    <p style={{marginTop: 0, color: '#4a5568'}}>Choose an action</p>
                    <div style={{display: 'flex', gap: '8px'}}>
                      <button onClick={() => { handle_view_CSV(selectedHistory.id); setSelectedHistory(null); }} className="primary_button">View CSV</button>
                      <button onClick={() => { handle_download_PDF(selectedHistory.id); setSelectedHistory(null); }} className="pdf_button">Download PDF</button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </aside>

      </div>

      {show_csv_modal && csv_data && (
        <div className="modal_overlay" onClick={() => set_show_csv_modal(false)}>
          <div className="modal_content" onClick={(e) => e.stopPropagation()}>
            <div className="modal_header">
              <h2>CSV Data Preview</h2>
              <button className="modal_close" onClick={() => set_show_csv_modal(false)}>✕</button>
            </div>
            <div className="csv_table_container">
              <table className="csv_table">
                <thead>
                  <tr>
                    {csv_data.headers.map((header, index) => (
                      <th key={index}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {csv_data.rows.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {csv_data.headers.map((header, colIndex) => (
                        <td key={colIndex}>{row[header]}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="modal_footer">
              <button onClick={() => set_show_csv_modal(false)} className="primary_button">Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
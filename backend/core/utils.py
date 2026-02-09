# Made new file to try and separate data processing logic from API views. Basically promoting code reusability...
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from xhtml2pdf import pisa
from .models import EquipmentHistory
matplotlib.use('Agg')
from django.utils.timezone import localtime

# Function to handle all data processing logic SEPERATELY from the API views.
def process_equipment_file(file_obj):
    # Verify file extension
    if not file_obj.name.lower().endswith('.csv'):
        raise ValueError("Invalid file type! Only .csv files are allowed.")
    
    # Limit file size to 10MB
    MAX_SIZE_MB = 10
    if file_obj.size > MAX_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File is too large! Maximum limit is {MAX_SIZE_MB}MB.")
    
    try:
        df = pd.read_csv(file_obj)
        df.columns = df.columns.str.strip().str.lower()
        required_cols = {'flowrate', 'pressure', 'type', 'temperature'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"CSV is missing required columns: {missing}")
        stats = {
            "total_count": int(len(df)),
            "averages": {
                # Fill NaN values with 0 to prevent JSON errors
                "flowrate": float(df['flowrate'].fillna(0).mean()),
                "pressure": float(df['pressure'].fillna(0).mean()),
                "temperature": float(df['temperature'].fillna(0).mean())
            },
            # Count equipment types and convert to dict for JSON serialization 
            "type_distribution": df['type'].value_counts().to_dict(),
            "equipment_data": df.head(10).to_dict(orient='records')
        }
        return stats
    except Exception as e:
        raise ValueError(f"Error processing CSV: {str(e)}")

# Helper function to generate chart image 
def get_chart(stats):
    # Graph for PDF
    plt.figure(figsize=(6, 4))
    types = list(stats['type_distribution'].keys())
    counts = list(stats['type_distribution'].values())
    plt.bar(types, counts, color='#2d5a27')
    plt.title("Equipment Distribution")
    plt.ylabel("Count")
    plt.tight_layout()

    plt.xticks(rotation=45, ha='right')  
    plt.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100)
    plt.close()
    img_buffer.seek(0)
    
    # Convert to Base64 string for embedding in HTML
    return base64.b64encode(img_buffer.read()).decode('utf-8')

# Function to generate PDF report based on the processed data
def generate_pdf_report(history_instance):
    # A buffer to hold pdf data in memory instead of going to disk
    buffer = io.BytesIO()
    stats = history_instance.summary_data
    chart_image = get_chart(stats)
    
    #Timezone converted to IST 
    local_time = localtime(history_instance.upload_date)
    html_string = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{ size: a4 portrait; margin: 2cm; }}
            body {{ font-family: Helvetica; color: #333333; }}
            
            .header {{ text-align: center; border-bottom: 2px solid #2d5a27; padding-bottom: 10px; margin-bottom: 20px; }}
            h1 {{ color: #2d5a27; font-size: 24px; margin: 0; }}
            .meta {{ color: #666; font-size: 12px; margin-top: 5px; }}
            
            h2 {{ background-color: #f0fdf4; color: #1a4216; padding: 5px; border-bottom: 1px solid #2d5a27; font-size: 16px; margin-top: 20px; }}
            
            .stats-table {{ width: 100%; margin-bottom: 20px; }}
            .stats-table td {{ width: 25%; text-align: center; background-color: #eee; padding: 10px; border-radius: 5px; }}
            .stat-val {{ font-size: 18px; font-weight: bold; color: #2d5a27; display: block; }}
            .stat-label {{ font-size: 10px; color: #555; }}
            
            .chart-container {{ text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
    
        <div class="header">
            <h1>Equipment Report: {history_instance.filename}</h1>
            <div class="meta">
                Date: {local_time.strftime('%H:%M %d/%m/%Y')} (IST)
            </div>
        </div>

        <h2>Summary</h2>
        <table class="stats-table">
            <tr>
                <td>
                    <span class="stat-val">{stats['total_count']}</span>
                    <span class="stat-label">Total Units</span>
                </td>
                <td>
                    <span class="stat-val">{stats['averages']['flowrate']:.2f}</span>
                    <span class="stat-label">Avg Flow (m3/h)</span>
                </td>
                <td>
                    <span class="stat-val">{stats['averages']['pressure']:.2f}</span>
                    <span class="stat-label">Avg Pressure (bar)</span>
                </td>
                <td>
                    <span class="stat-val">{stats['averages']['temperature']:.2f}</span>
                    <span class="stat-label">Avg Temp (°C)</span>
                </td>
            </tr>
        </table>

        <h2>Equipment Distribution</h2>
        <div class="chart-container">
            <img src="data:image/png;base64,{chart_image}" width="400" />
        </div>

    </body>
    </html>
    """

    result = pisa.CreatePDF(io.BytesIO(html_string.encode("utf-8")), dest=buffer)
    
    if result.err:
        raise ValueError("PDF generation error")

    buffer.seek(0)
    return buffer
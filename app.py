from flask import Flask, render_template, request, send_file
from services.vip_status import calculate_vip_status
import pandas as pd
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

def search_results_by_name(name, api_key, cx):
    url = f"https://www.googleapis.com/customsearch/v1?q={name}&key={api_key}&cx={cx}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        search_results = data.get('items', [])[:5]
        return search_results
    else:
        return None

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/status', methods=['POST'])
def process_file():
    print("Inside status method")
    if 'file' not in request.files:
        return render_template('upload.html', error="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('upload.html', error="No selected file")
    
    if file:
        try:
            print("we found a file")
            df = pd.read_excel(file)
            names = df[['First Name', 'Middle Name', 'Last Name']].apply(lambda x: ' '.join(x.dropna()), axis=1).tolist()
            
            api_key = os.getenv('API_KEY')
            cx = os.getenv('CX')

            results = []
            for name in names:
                search_results = search_results_by_name(name, api_key, cx)
                general_keywords = ["general", "keyword"]  # Replace with actual general keywords
                doctor_keywords = ["doctor", "keyword"]  # Replace with actual doctor keywords
                
                vip_status, links = calculate_vip_status(name, search_results, general_keywords, doctor_keywords)
                result = {
                    "Name": name,
                    "VIP Status": vip_status
                }
                for i, link in enumerate(links):
                    result[f"Link {i+1}"] = link
                
                results.append(result)
                
            result_df = pd.DataFrame(results)
            result_df.to_excel('VIP_results.xlsx', index=False)
            result_dict = result_df.to_dict(orient='records')  # Convert DataFrame to dictionary

        except Exception as e:
            return render_template('upload.html', error=f"Error reading file: {str(e)}")

    return render_template('status.html', results=result_dict)

@app.route('/download')
def download_file():
    return send_file('VIP_results.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

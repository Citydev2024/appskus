
from flask import Flask, request, render_template, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def upload_files():
    return render_template('index.html')

@app.route('/update_sku', methods=['POST'])
def update_sku():
    if 'file1' not in request.files or 'file2' not in request.files:
        return 'No file part'
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Read the uploaded files
    hoja_1_df = pd.read_excel(file1, engine='odf')
    wc_export_df = pd.read_csv(file2)

    # Rename columns for clarity
    hoja_1_df = hoja_1_df.rename(columns={
        'Código interno': "Codigo_interno",
        'SKU': "Nuevo_SKU"
    })

    # Update SKUs
    sku_mapping = hoja_1_df.set_index('Codigo_interno')['Nuevo_SKU'].to_dict()
    wc_export_df['SKU'] = wc_export_df['SKU'].map(sku_mapping).fillna(wc_export_df['SKU'])

    # Save the updated file to a BytesIO object
    output = BytesIO()
    wc_export_df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, mimetype='text/csv', download_name='updated_wc_export.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from Classifiers.model import prepare_data, calculate_sma_ema, plot_data
from Data.db_functions import get_company_data_by_code, get_all_company_codes

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/select_company', methods=['GET'])
def company_selector():
    # Fetch all company codes from the database
    company_codes = get_all_company_codes()
    return render_template('select_company.html', company_codes=company_codes)

@app.route('/analyze', methods=['POST','GET'])
def analyze():
    company_code = request.form.get('company_code')
    data = get_company_data_by_code(company_code)
    data_dict = prepare_data(data)
    _, _, monthly_data = data_dict

    # Add SMA and EMA calculations
    monthly_with_indicators = calculate_sma_ema(monthly_data)

    # Generate Plotly graph
    fig = plot_data(monthly_with_indicators, f"Monthly Data for {company_code} with SMA & EMA")
    graph_html = fig.to_html(full_html=False)

    return render_template('dashboard.html', company_code=company_code, graph_html=graph_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)

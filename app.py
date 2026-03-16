from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    ticker = ""
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        try:
            # Running popstock.py using the virtual environment python
            # Make sure popstock.py is in the same directory
            result = subprocess.check_output(['/home/pop/shardi_venv/bin/python3', 'popstock.py', ticker], text=True)
        except Exception as e:
            result = f"Error running Popstock: {str(e)}"
    
    return render_template('index.html', result=result, ticker=ticker)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

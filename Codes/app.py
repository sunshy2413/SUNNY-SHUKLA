from flask import Flask, request, render_template_string
import joblib

app = Flask(__name__)
model = joblib.load('rf_model.pkl')

HTML = open('templates_index.html').read()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duration = float(request.form['duration'])
        protocol = request.form['protocol_type']
        src_bytes = float(request.form['src_bytes'])
        dst_bytes = float(request.form['dst_bytes'])
        flag = request.form['flag']

        protocol_map = {'TCP': 0, 'UDP': 1, 'ICMP': 2}
        flag_map = {'SF': 0, 'REJ': 1, 'RSTO': 2}

        features = [duration, protocol_map[protocol], src_bytes, dst_bytes, flag_map[flag]]
        prediction = model.predict([features])[0]
        result = "Normal" if prediction == 0 else "Attack"
        return render_template_string(HTML, result=result)
    return render_template_string(HTML, result=None)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import plotly.io as pio
import analysis


app = Flask(__name__)

@app.route('/')
def home():

    fig = analysis.build_graph("Iga Swiatek", "average_game_length")
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('home.html',graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
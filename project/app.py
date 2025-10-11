from flask import Flask, request, render_template
import plotly.io as pio
import analysis


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():

    player = request.form.get('fname', 'Iga Swiatek')
    fig = analysis.build_graph(player, "average_game_length")
    graph_html = pio.to_html(fig, full_html=False)
    return render_template('home.html',graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
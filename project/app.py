from flask import Flask, request, render_template
import plotly.io as pio
import analysis

#requests allows access to HTTP form inputs, 
#render_template allows generation of HTML content with dynamic content
#plotly.io allows rendering of plotly graphs with dynamic content

app = Flask(__name__)
#creates a flask app instance

@app.route('/', methods=['GET','POST'])
#defining route (home() will handle requests to the route directory)
#home() can handle both GET requests (like opening the page) and POST requests (like submitting a form)

def home():

    stat_type = request.form.get('types', 'serving')
    #key and default

    if stat_type == 'serving':
        fig = analysis.build_serve_stats_graph()
        graph_html = pio.to_html(fig, full_html=False)
        return render_template('home.html',graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
import csv
import pandas as pd
import plotly.graph_objs as go
from flask import Flask, render_template_string

# Load the CSV file into a DataFrame
csv_file_path = r'network_data_log.csv'
df = pd.read_csv(csv_file_path)

# Create a plotly graph with a dark theme
def create_graph():
    fig = go.Figure()

    # Add traces for inbound and outbound data
    fig.add_trace(go.Scatter(
        x=df['Time Elapsed (s)'],
        y=df['Inbound Data (Mbps)'],
        mode='lines',
        name='Inbound Data (Mbps)',
        line=dict(color='cyan')
    ))

    fig.add_trace(go.Scatter(
        x=df['Time Elapsed (s)'],
        y=df['Outbound Data (Mbps)'],
        mode='lines',
        name='Outbound Data (Mbps)',
        line=dict(color='magenta')
    ))

    # Update the layout to apply the dark theme
    fig.update_layout(
        title='Network Data Usage',
        xaxis_title='Time Elapsed (s)',
        yaxis_title='Data (Mbps)',
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    # Return the graph as an HTML div
    return fig.to_html(full_html=False)

# Create a Flask web app
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    graph_html = create_graph()
    # Minimalistic HTML page to embed the graph
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Network Usage Graph</title>
        <style>
            body { background-color: #1e1e1e; color: white; font-family: Arial, sans-serif; }
            h1 { text-align: center; margin-top: 30px; }
            .graph-container { width: 80%; margin: auto; }
        </style>
    </head>
    <body>
        <h1>Network Usage</h1>
        <div class="graph-container">
            {{ graph_html|safe }}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template, graph_html=graph_html)

# Automatically open the web app in the browser
if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=False, use_reloader=False)

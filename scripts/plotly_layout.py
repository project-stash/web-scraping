import plotly.express as px
import plotly.graph_objects as go
def create_plotly(data,options):
    if (options == "hist"):
        fig = go.Figure([go.Scatter(x=data['Date'], y=data['Close'])])
    else:
        fig = px.bar(data, x="year", y="Dividends")
    return fig
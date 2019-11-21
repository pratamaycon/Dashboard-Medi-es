from plotly.offline import plot
import plotly.graph_objs as go
fig = go.Figure({
    "data": [{"type": "bar",
              "x": [1, 2, 3,4,5,6],
              "y": [1, 3, 2,4,5,6]}],
    "flamengo": {"title": {"text": "A Bar Chart"}}
})
fig.show()
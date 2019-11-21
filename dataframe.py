import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

obj = {'col1': [1, 'flamengo'], 'col2': [3, 4]}

df = pd.DataFrame(data=obj)

print(df)
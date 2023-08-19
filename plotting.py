import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df_list=[]

for i in range(0,3):
  j=200+i
  df_list.append(pd.read_csv('data/{}.zip'.format(j)))

dataset = pd.concat(df_list,ignore_index=True)

gb = dataset.groupby('density')

densities = np.round(np.linspace(0.200,0.202,3),3)
print(densities)

fig = go.Figure()

for density in densities:
  fig.add_trace(
      go.Contour(
      z=(gb.get_group(density))['potential_energy'],
      x=(gb.get_group(density))['lambda_value'],
      y=(gb.get_group(density))['mu_value'],
      colorbar=dict(title='Potential Energy', titleside='right'),
      contours=dict(showlabels= True),colorscale='sunset',
      line_smoothing=0.0))

fig.update_layout(
{
    "showlegend": True,
    "xaxis": {"title": "Plane Parameter Lambda"},
    "yaxis": {"title": "Plane Parameter Mu"},
    "autosize":False,
    "width":800,
    "height":800})

for i in range(1,len(densities)):
  fig.data[i].visible = False

fig.data[0].visible=True

steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Potential Energy for a Relative Density = " + str(densities[i])}],  # layout attribute
        label=densities[i]
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Relative Density: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()
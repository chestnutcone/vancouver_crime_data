# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 13:38:20 2020

@author: Oliver
"""

import pandas as pd
import geopandas as gpd
import json
import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
import os
import pickle


FOLDER = "2018"
with open("cov_localareas_with_id.json", 'r') as f:
    van_geojson = json.load(f)
    
with open(os.path.join("2018_cleaned_data.pickle"), 'rb') as f:
    df_dict = pickle.load(f)
    
neighborhood_names = [van_geojson['features'][x]['id'] for x in range(len(van_geojson['features']))]

# need to change some index
index_ref = {'Arbutus Ridge':'Arbutus-Ridge',
             'Kensington-CedarCottage':'Kensington-Cedar Cottage',
             'Central Business District':'Downtown'}
# rename
files = [f.name for f in os.scandir(FOLDER) if f.is_file()]
for filename in files:
    cur_df = df_dict[filename]
    df_dict[filename] = cur_df.rename(index=index_ref)
    
for filename in files:
    cur_df = df_dict[filename]
    for row in cur_df.index:
        if row not in neighborhood_names:
            cur_df = cur_df.drop(row)
    df_dict[filename] = cur_df
    
sorted_filename = sorted(files)

sorted_df = [df_dict[f] for f in sorted_filename]

# normalize to total population of census 2016
total_pop = pd.read_pickle(r"")  ## total population file here, from Vancouver Census 2016
total_pop = total_pop.iloc[:,0]

total_pop.drop(["Vancouver CSD"
                , "Vancouver CMA"], inplace=True)

for i in range(len(sorted_df)):
    sorted_df[i] = sorted_df[i].apply(lambda x: x.divide(total_pop))
    
COL = 'Offensive Weapons'

def make_choropleth(fig, df, col, max_z):
    fig.add_trace(
        go.Choroplethmapbox(geojson=van_geojson, # geojson with 'id'
                            locations=df.index,   # index is the neighborhood names, which will match to 'id' of geojson
                            z=df[col], # values of data you want to plot
                            colorscale='Magma', # your colorscale
                            marker_opacity=0.5, 
                            marker_line_width=0, 
                            name=col,
                            zmin=0,
                            zmax=max_z,
                            visible=False
        )
    )
    return fig

def create_graphs(COL):
    max_z = max([sorted_df[i][COL].max() for i in range(len(sorted_df))])
    # print(max_z)
    fig = go.Figure() # empty figure
    for df in sorted_df:
        fig = make_choropleth(fig, df, COL, max_z)
    fig.data[0].visible = True # make first data visible
        
    # create slider
    steps = []
    date_ref = {0:"Jan", 1:"Feb", 2:"Mar", 3:"Apr", 4:"May", 5:"Jun", 6:"Jul", 7:"Aug", 8:"Sept", 9:"Oct", 10:"Nov", 11:"Dec"}
    for i in range(len(fig.data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(fig.data)],
                    label=date_ref[i],
                    )
        step['args'][1][i] = True
        steps.append(step)
        
    sliders = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]    
    
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=11, # how much zoom you want at the start
                      mapbox_center={'lat': 49.24, 'lon':-123.1},
                  sliders=sliders,
                      title=COL+' 2019')
    try:
        pio.write_html(fig, file="vancouver_crime_{}_2018_normalized.html".format(COL))
    except Exception as e:
        new_name = COL.replace("<", "")
        new_name = new_name.replace(">", "")
        pio.write_html(fig, file="vancouver_crime_{}_2018_normalized.html".format(new_name))
        
    # fig.show()
        
        
for c in sorted_df[0].columns:
    create_graphs(c)
    
    
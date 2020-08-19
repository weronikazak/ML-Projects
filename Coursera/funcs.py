import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as soup
import requests
from funcs import *
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors
import folium



# ----------------TABLES-------------------
def get_close_venues(names, latitudes, longitudes, CLIENT_ID, CLIENT_SECRET):
    LIMIT = 80
    VERSION = '20180605'
    radius = 500
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):

        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        results = requests.get(url).json()["response"]['groups'][0]['items']
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


def df_to_oneshot(df_data_venues):
    df_onehot = pd.get_dummies(df_data_venues[['Venue Category']], prefix="", prefix_sep="")

    df_onehot['Neighborhood'] = df_data_venues['Neighborhood'] 

    fixed_columns = [df_onehot.columns[-1]] + list(df_onehot.columns[:-1])
    df_onehot = df_onehot[fixed_columns]

    return df_onehot



def places_by_frequency(df_oneshot, num_top_venues = 5):
    df_grouped = df_oneshot.groupby('Neighborhood').mean().reset_index()
    
    for hood in df_grouped['Neighborhood']:
        print("----"+hood+"----")
        temp = df_grouped[df_grouped['Neighborhood'] == hood].T.reset_index()
        temp.columns = ['venue','freq']
        temp = temp.iloc[1:]
        temp['freq'] = temp['freq'].astype(float)
        temp = temp.round({'freq': 2})
        print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
        print('\n')
    return df_grouped



def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


def return_dataframe_most_common_venues(df_grouped, num_top_venues = 6):
    indicators = ['st', 'nd', 'rd']
    columns = ['Neighborhood']
    for ind in np.arange(num_top_venues):
        try:
            columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
        except:
            columns.append('{}th Most Common Venue'.format(ind+1))

    df_venues_sorted = pd.DataFrame(columns=columns)
    df_venues_sorted['Neighborhood'] = df_grouped['Neighborhood']

    for ind in np.arange(df_grouped.shape[0]):
        df_venues_sorted.iloc[ind, 1:] = return_most_common_venues(df_grouped.iloc[ind, :], num_top_venues)

    return df_venues_sorted


# ------------------ CLUSTERING ---------------------

def cluster_venues(kclusters, df_grouped, df_venues_sorted, df):
  # kclusters = 8
  df_grouped_clustering = df_grouped.drop('Neighborhood', 1)
  kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(df_grouped_clustering)
  df_venues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

  df_merged = df

  df_merged = df_merged.join(df_venues_sorted.set_index('Neighborhood'), on='Neighborhood')

  return df_merged


def show_most_common_venue_count(df_merged, num_top_venues = 5):
  for i in range(1, num_top_venues+1):
    if i == 1:
        label = "1st Most Common Venue"
    elif i == 2:
        label = "2nd Most Common Venue"
    elif i == 3:
        label = "3rd Most Common Venue"
    else:
        label = f"{i}th Most Common Venue"
    print(label.upper())
    print(df_merged[label].value_counts()[:5])
    print("\n") 


# ---------- VISUALIZE ----------


def show_map_clusters(kclusters, df_merged, df_coords):
  x = np.arange(kclusters)
  ys = [i + x + (i*x)**2 for i in range(kclusters)]
  colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
  rainbow = [colors.rgb2hex(i) for i in colors_array]

  df_map = folium.Map(location=df_coords, zoom_start=10)

  for i, row in df_merged.iterrows():
      lat = row["Latitude"]
      poi = row["Neighborhood"]
      lon = row["Longitude"]
      try:
          cluster = int(row["Cluster Labels"])
      except:
          continue
      label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
      folium.CircleMarker(
          [lat, lon],
          radius=5,
          popup=label,
          color=rainbow[cluster-1],
          fill=True,
          fill_color=rainbow[cluster-1],
          fill_opacity=0.7).add_to(df_map)
  return df_map


def show_cluster_number(df_merged, cluster_num):
  cluster = df_merged.loc[df_merged['Cluster Labels'] ==  cluster_num, df_merged.columns[[1] + list(range(5, df_merged.shape[1]))]]
  return cluster
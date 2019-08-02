import pandas as pd
import geopandas as gpd
from shapely import wkt



pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GTFS/'



# fromto function
def fromto(ft):
    ft['geom']='LINESTRING('+', '.join(ft['shape_pt_lon']+' '+ft['shape_pt_lat'])+')'
    ft=ft[['shape_id','route_short_name','route_long_name','route_desc','trip_headsign','direction_id','geom']].drop_duplicates(keep='first').reset_index(drop=True)
    return ft



# Reading files
stops=pd.read_csv(path+'stops.txt',dtype=str)
shapes=pd.read_csv(path+'shapes.txt',dtype=str)
stoptimes=pd.read_csv(path+'stop_times.txt',dtype=str)
trips=pd.read_csv(path+'trips.txt',dtype=str)
routes=pd.read_csv(path+'routes.txt',dtype=str)
stoptimes=stoptimes[['trip_id','stop_id']].drop_duplicates(keep='first').reset_index()
trips=trips[['trip_id','route_id','shape_id','trip_headsign','direction_id']].drop_duplicates(keep='first').reset_index()
routes=routes[['route_id','route_short_name','route_long_name','route_desc']].drop_duplicates(keep='first').reset_index()



# Stops
stops2=pd.merge(stops,stoptimes,how='left',on='stop_id')
stops2=pd.merge(stops2,trips,how='left',on='trip_id')
stops2=pd.merge(stops2,routes,how='left',on='route_id')
stops2=stops2.groupby(['stop_id','stop_name','stop_lat','stop_lon','route_short_name'],as_index=False).agg({'trip_id':'count'})
stops2=stops2.sort_values(['stop_id','trip_id'],ascending=[True,False]).reset_index(drop=True)
stops2=stops2.groupby(['stop_id','stop_name','stop_lat','stop_lon'])['route_short_name'].apply('/'.join).reset_index(drop=False)
stops2=gpd.GeoDataFrame(stops2,geometry=gpd.points_from_xy(pd.to_numeric(stops2['stop_lon']),pd.to_numeric(stops2['stop_lat'])),crs={'init' :'epsg:4326'})
stops2=stops2[['stop_id','stop_name','route_short_name','geometry']]
stops2.to_file(path+'stops.shp')



# Routes
shapes2=pd.merge(shapes,trips,how='left',on='shape_id')
shapes2=pd.merge(shapes2,routes,how='left',on='route_id')
shapes2=shapes2[['shape_id','shape_pt_lat','shape_pt_lon','shape_pt_sequence','route_short_name','route_long_name','route_desc','trip_headsign','direction_id']].drop_duplicates().reset_index(drop=True)
shapes2['shape_pt_sequence']=pd.to_numeric(shapes2['shape_pt_sequence'])
shapes2=shapes2.sort_values(['shape_id','shape_pt_sequence'],ascending=True).reset_index(drop=True)
shapes2=shapes2.groupby('shape_id').apply(fromto).reset_index(drop=True)
shapes2=shapes2[['route_short_name','route_long_name','route_desc','trip_headsign','direction_id','geom']]
shapes2=shapes2.sort_values(['route_short_name','direction_id','trip_headsign']).drop_duplicates(keep='first').reset_index(drop=True)
shapes2['geom']=shapes2['geom'].apply(wkt.loads)
shapes2=gpd.GeoDataFrame(shapes2,geometry=shapes2['geom'],crs={'init' :'epsg:4326'})
shapes2=shapes2.drop('geom',axis=1)
shapes2=shapes2.dissolve(by=['route_short_name','direction_id','trip_headsign']).reset_index()
shapes2=shapes2[['route_short_name','route_long_name','route_desc','direction_id','trip_headsign','geometry']]
shapes2.to_file(path+'routes.shp')



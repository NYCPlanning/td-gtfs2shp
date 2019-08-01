import arcpy

env='C:/Users/Y_Ma2/DESKTOP/BUSGTFS'
arcpy.CreateFileGDB_management(env,'BUSGTFS.gdb')

for i in ['google_transit','google_transit_bronx','google_transit_brooklyn','google_transit_manhattan','google_transit_queens','google_transit_staten_island']:
    arcpy.TableToTable_conversion(in_rows=env+'/'+i+'/stops2.txt',out_path=env+'/BUSGTFS.gdb',out_name=i+'_stoptable')
    stoplyr=arcpy.MakeXYEventLayer_management(table=env+'/BUSGTFS.gdb/'+i+'_stoptable',in_x_field='stop_lon',in_y_field='stop_lat',out_layer=i+'_stop',spatial_reference='4326')
    arcpy.management.CopyFeatures(stoplyr,env+'/BUSGTFS.gdb/'+i+'_stop')
    
    arcpy.TableToTable_conversion(in_rows=env+'/'+i+'/shape2.txt',out_path=env+'/BUSGTFS.gdb',out_name=i+'_shapetable')
    arcpy.XYToLine_management(in_table=env+'/BUSGTFS.gdb/'+i+'_shapetable',out_featureclass=env+'/BUSGTFS.gdb/'+i+'_shape',startx_field='shape_from_lon',starty_field='shape_from_lat',endx_field='shape_to_lon',endy_field='shape_to_lat',spatial_reference='4326')
    shapelyr=arcpy.MakeFeatureLayer_management(env+'/BUSGTFS.gdb/'+i+'_shape')
    shapelyr=arcpy.AddJoin_management(in_layer_or_view=shapelyr,in_field='OID',join_table=env+'/BUSGTFS.gdb/'+i+'_shapetable',join_field='OBJECTID')
    arcpy.Dissolve_management(in_features=shapelyr,out_feature_class=env+'/BUSGTFS.gdb/'+i+'_route',dissolve_field=[str(i)+'_shapetable.'+x for x in ['route_short_name','route_long_name','route_desc','trip_headsign','direction']])
    for j in ['route_short_name','route_long_name','route_desc','trip_headsign','direction']:
        arcpy.AlterField_management(in_table=env+'/BUSGTFS.gdb/'+i+'_route',field=str(i)+'_shapetable_'+j,new_field_name=j)

arcpy.Merge_management(inputs=[env+'/BUSGTFS.gdb/'+x+'_stop' for x in ['google_transit','google_transit_bronx','google_transit_brooklyn','google_transit_manhattan','google_transit_queens','google_transit_staten_island']],output=env+'/BUSGTFS.gdb/'+'MTA_NYC_Bus_Stops')
arcpy.Merge_management(inputs=[env+'/BUSGTFS.gdb/'+x+'_route' for x in ['google_transit','google_transit_bronx','google_transit_brooklyn','google_transit_manhattan','google_transit_queens','google_transit_staten_island']],output=env+'/BUSGTFS.gdb/'+'MTA_NYC_Bus_Routes')

print('Done!')

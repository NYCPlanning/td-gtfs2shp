library(dplyr)

path='C:/Users/Y_MA2/Desktop/BUSGTFS/'

for (i in c('google_transit','google_transit_bronx','google_transit_brooklyn','google_transit_manhattan','google_transit_queens','google_transit_staten_island')) {
  # Unzip and read data
  unzip(zipfile = paste0(path,i,'.zip'), exdir = paste0(path,i))
  stop=read.csv(paste0(path,i,'/stops.txt'),stringsAsFactors = F)
  shape=read.csv(paste0(path,i,'/shapes.txt'),stringsAsFactors = F)
  time=read.csv(paste0(path,i,'/stop_times.txt'),stringsAsFactors = F)
  trip=read.csv(paste0(path,i,'/trips.txt'),stringsAsFactors = F)
  route=read.csv(paste0(path,i,'/routes.txt'),stringsAsFactors = F)
  
  time=distinct(select(time,trip_id,stop_id))
  trip=distinct(select(trip,trip_id,route_id,shape_id,trip_headsign,direction_id))
  route=distinct(select(route,route_id,route_short_name,route_long_name,route_desc))
  
  # Create new stop file
  stop2=merge(stop,time,by='stop_id',all.x=T)
  stop2=merge(stop2,trip,by='trip_id',all.x=T)
  stop2=merge(stop2,route,by='route_id',all.x=T)
  stop2=stop2 %>% group_by(stop_id,stop_name,stop_lat,stop_lon,route_short_name) %>% summarise(count=n())
  stop2=arrange(stop2,stop_id,desc(count))
  stop2=stop2%>% group_by(stop_id,stop_name,stop_lat,stop_lon) %>% summarise(route_name=paste0(route_short_name,collapse='/'))
  write.csv(stop2,paste0(path,i,'/stops2.txt'),row.names = F)
  
  # Create new shape file
  shape2=merge(shape,trip,by='shape_id',all.x=T)
  shape2=merge(shape2,route,by='route_id',all.x=T)
  shape2=select(shape2,shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,route_short_name,route_long_name,route_desc,trip_headsign,direction_id)
  shape2=distinct(shape2)
  shape2=arrange(shape2,shape_id,shape_pt_sequence)
  shape3=data.frame()
  for (j in unique(shape2$shape_id)){
    from=subset(shape2,shape_id==j)
    colnames(from)=c('shape_from_id','shape_from_lat','shape_from_lon','shape_from_sequence','from_route_short_name','from_route_long_name','from_route_desc','from_trip_headsign','from_direction')
    to=from[-1,]
    colnames(to)=c('shape_to_id','shape_to_lat','shape_to_lon','shape_to_sequence','to_route_short_name','to_route_long_name','to_route_desc','to_trip_headsign','to_direction')
    from=from[1:(nrow(from)-1),]
    df=cbind(from,to)
    df=select(df,shape_from_id,shape_from_lat,shape_from_lon,shape_from_sequence,shape_to_lat,shape_to_lon,from_route_short_name,from_route_long_name,from_route_desc,from_trip_headsign,from_direction)
    colnames(df)=c('shape_id','shape_from_lat','shape_from_lon','shape_from_sequence','shape_to_lat','shape_to_lon','route_short_name','route_long_name','route_desc','trip_headsign','direction')
    shape3=rbind(shape3,df)
  }
  shape3=distinct(select(shape3,route_short_name,route_long_name,route_desc,trip_headsign,direction,shape_from_lat,shape_from_lon,shape_to_lat,shape_to_lon))
  shape3=arrange(shape3,route_short_name,direction,shape_from_lat,shape_from_lon)
  write.csv(shape3,paste0(path,i,'/shape2.txt'),row.names = F)
}

print('Done!')






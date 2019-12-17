#!/usr/bin/env pythonimport grass.script as gscript
#tabs beachten, python ist da sensitiv
def main():

#    gscript.run_command('g.region', flags='p')#adapt region to tarragona study area
#setting the resolution to 1km (1000m), the flag "m" shows the the resolution in meters
    gscript.run_command('g.region', vector='tarragona_region@PERMANENT', res=1000, flags='mp')

#import of Corine Landcover,in Python the path is writen different, so r"C:\."
    gscript.run_command('r.import', overwrite=True, output='landcover', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\corine_landcover_2018\CLC2018_tarragona.tif")
#import of DEM N41E001
    gscript.run_command('r.import', overwrite=True, output='dem_N41E001', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\dem\N41E001.hgt")
#import of DEM N41E000
    gscript.run_command('r.import', overwrite=True, output='dem_N41E000', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\dem\N41E000.hgt")
#import of DEM N40E000
    gscript.run_command('r.import', overwrite=True, output='dem_N40E000', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\dem\N40E000.hgt")
#import of OSM data\buildings
    gscript.run_command('v.import', overwrite=True, output='buildings', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\osm\buildings.geojson")
#import of OSM data\fire_stations

    gscript.run_command('v.import', overwrite=True, output='fire_stations', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\osm\fire_stations.geojson")
#import of OSM data\region
    gscript.run_command('v.import', overwrite=True, output='region_osm', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\osm\tarragona_region.geojson")
#import of Wildfire incidents
    gscript.run_command('v.import', overwrite=True, output='wildfire_incidents', input=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\assignment4_data\fire_incidents\fire_archive_V1_89293.shp")
#the region is covering 3 different DEMS, so they are merged to one raster with i.image.mosaic

    gscript.run_command('r.patch', overwrite=True, output='dem_tarragona', input=['dem_N41E000', 'dem_N40E000', 'dem_N41E001'])
#calculating slope with r.slope.aspect, degree is used

    gscript.run_command('r.slope.aspect', overwrite=True, elevation='dem_tarragona', slope='slope')
#reclass is in 4 hazard categories
    gscript.run_command('r.reclass', overwrite=True, input='slope', output='reclass', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_slope_hazard_class.txt")
#for making the result permanent, r.resample is used
    gscript.run_command('r.resample', overwrite=True, input='reclass', output='slope_hazardclass')

    gscript.run_command('r.reclass', overwrite=True, input='landcover', output='landcover_hazard', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_landcover_hazard_class.txt")
#fire probability
    gscript.run_command('v.mkgrid', overwrite=True, map='grid3', box='1000,1000')
#points_column=cat, because every incident has a cat (which is their ID).
    gscript.run_command('v.vect.stats', overwrite=True, points='wildfire_incidents', areas='grid3', method='sum', points_column='cat', count_column='fire_count', stats_column='stat')
    gscript.run_command('v.to.rast', overwrite=True, input='grid3', output='incidents_cells', use='attr', attribute_column='fire_count', label_column='fire_count')

    gscript.run_command('r.mapcalc', overwrite=True, expression = "'probability'= if('incidents_cells'> 15, 15, 'incidents_cells')* 100/ 15")
    gscript.run_command('r.reclass', overwrite=True, input='probability', output='probability_class', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_fire_probability.txt")
#the calculation of the centroid is unnassasary, because in GRASS GIS it is already in the area Information 

#    gscript.run_command('v.type', overwrite=True, input='buildings', output='buildings_boundary', from_type='line', to_type='boundary')
#    gscript.run_command('v.centroids', overwrite=True, input='buildings_boundary', output='buildings_centroids')
#the building density, is calculated as the numbers of buildings per Grid(1km*1km),like the calculation of fire_incidents per cell 
    gscript.run_command('v.vect.stats', overwrite=True, points='buildings', areas='grid3', type='centroid', count_column='buildings_count')

    gscript.run_command('v.to.rast', overwrite=True, input='grid3', output='building_density', use='attr', attribute_column='buildings_count', label_column='buildings_count')
    gscript.run_command('r.reclass', overwrite=True, input='building_density', output='building_reclass', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_building_density.txt")
    gscript.run_command('v.vect.stats', overwrite=True, points='fire_stations', areas='grid3', type='centroid', count_column='fire_station')
#for calcualtion the distance to the fire stations, the input dile must be a raster file, so v.to.rast is used
    gscript.run_command('v.to.rast', overwrite=True, input='grid3', output='fire_stations_raster', use='attr', attribute_column='fire_station')
#r.grow.distance calculate the distance of every zell in a raster file from the input file. The flage -m shows the distance in m

    gscript.run_command('r.reclass', overwrite=True, input='fire_stations_raster', output='fire_station_reclass', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_NULL.txt")   
    gscript.run_command('r.grow.distance', overwrite=True, flags='m', input='fire_station_reclass', distance='distance_to_fire_stations')
    gscript.run_command('r.reclass', overwrite=True, input='distance_to_fire_stations', output='firestation_distance_reclass', rules=r"C:\Users\carst\fossgis_gawlas\fossgis19_1\fossgis_ws19_assignment4\rule_fire_station_distance.txt")



#for checking if all files are created

    gscript.run_command('g.list', overwrite=True, type='all')

if __name__ == '__main__':
      main()




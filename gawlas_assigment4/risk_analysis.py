#!/usr/bin/env python

import grass.script as gscript

#tabs beachten, python ist da sensitiv
#def definiert main
def main():

#adapt region to tarragona study area
    gscript.run_command('g.region', vector='tarragona_region@PERMANENT', flags='mp')
#hazard = (fire probability*weight of the fire probability) + ( reclassified slope*weight of the reclassified slope) + (reclassified CORINE land cover* weight of the reclassified land cover), the weight is 1
    gscript.run_command('r.mapcalc', overwrite=True, expression = "'Hazard' = 'probability_class' + 'slope_hazardclass' + 'landcover_hazard'")
#risk = hazard * exposure * vulnerability (Exposure: density of buildings ('building_reclass'); vulnerability: proximity to fire stations(firestation_distance_reclass))
    gscript.run_command('r.mapcalc', overwrite=True, expression = "'risk' = 'Hazard' * 'building_reclass' * 'firestation_distance_reclass'")

if __name__ == '__main__':
    main()

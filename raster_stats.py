import os
import grass.script as grass
import calendar
from datetime import date

# Define the folder containing your raster files
raster_dir = r"C:\Users\Christon Ledge\Documents\GIS projects\naga_solar\DSM_tiles\projects"

# Get a list of all .tif files in the folder
for file_name in os.listdir(raster_dir):
    if file_name.endswith(".tif"):
        # Get full file path
        file_path = os.path.join(raster_dir, file_name)
        
        # Create a clean map name (no spaces or dots)
        map_name = os.path.splitext(file_name)[0]
        print(file_path)
        grass.run_command('r.in.gdal', input=file_path, output=map_name, overwrite=True)
        grass.run_command("g.region", raster=map_name)

        slope_name = map_name + '_slope'
        aspect_name = map_name + '_aspect'
        grass.run_command('r.slope.aspect', elevation=map_name, slope=slope_name,
                    aspect=aspect_name, overwrite=True)
        
        horizon_name = map_name + '_horizon'
        grass.run_command('r.horizon', elevation=map_name, step='15',
                    output=horizon_name, overwrite=True)
        

        year = 2026

        for month in range(1, 13):
            ndays = calendar.monthrange(year, month)[1]
            daily_maps = []

            for day in range(1, ndays + 1):

                doy = date(year, month, day).timetuple().tm_yday
                output = f"{map_name}_solar_{doy:03d}"

                grass.run_command(
                    "r.sun",
                    elevation=map_name,
                    slope=slope_name,
                    aspect=aspect_name,
                    horizon_basename=horizon_name,
                    day=doy,
                    glob_rad=output,
                    horizon_step='15',
                    overwrite=True
                )

                daily_maps.append(output)
            
            grass.run_command(
                "r.series",
                input=",".join(daily_maps),
                output=f"{map_name}_sum_{month:02d}",
                method="sum"
            )

            grass.run_command(
                "r.series",
                input=",".join(daily_maps),
                output=f"{map_name}_avg_{month:02d}",
                method="average"
            )

      
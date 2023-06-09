# SKRIPS-runcase-scaffold
This project is a scaffold for running SKRIPS model


# Summary

- `generate_ocean_grid`: A matlab based code using wavewatch3 (ww3) library to generate bathymetry binary file for MITgcm to use.
- `produce_ocean_data`: Download hycom data and convert it to MITgcm binaries, i.e. initial conditions and open boundary conditions. By the time to generate MITgcm binaries, it needs the bathymetry binary (`generate_ocean_grid` ww3 steps) and grid data (`generate_ocean_grid/auxilary_run`).
- `case_scaffold`: Provides an empty case (same resolution and grid setup)



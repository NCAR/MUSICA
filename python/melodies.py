# Run a box model without advection over each grid cell
# For each gird cell, run a box model with the same reactions
# Calculate the percent error at each grid cell

import musica
import xarray as xr
import melodies_monet as mm
import itertools

fp = mm.tutorial.fetch_example("camchem:fv")
ds = xr.open_dataset(fp)

species = list(data.data_vars.keys())

# remove all variables that aren't chemical species involved in solving
filtered_columns = ['Precip', 'utcoffset', 'units']

species = [{
    'name': s,
    'type': 'CHEM_SPEC'
} for s in species if s not in filtered_columns]

reactions = [
    musica.Arrhenius(
        reactants=[musica.Reactant(species='O3', stoichiometry=1)],
        products=[musica.Product(species='O2', stoichiometry=1)],
    ),
    musica.Photolysis(
        species='O3',
        rate=1e-5,
        label = "o3"
    ),
    musica.Troe(
        reactants=[musica.Reactant(species='NO', stoichiometry=1)],
        products=[musica.Product(species='NO2', stoichiometry=1)]
    )
    # ...
]

photolysis_reactions = reactions.filter(
    lambda r: isinstance(r, musica.Photolysis))

solver = musica.solver(species=species, reactions=reactions, backend=musica.MICM)
photolysis = musica.photolysis(photolysis_reactions, backend=musica.TUVX)

output = xr.copy(ds, deep=True)
output = output.drop_vars(filtered_columns)

# assign NaN to all data variables
output = output.fillna(np.nan)

# Now assign the initial conditions to the first time step
for var in ds.data_vars:
    output[var][0, :] = ds[var][0, :]

# Option 1, solve each grid cell indepdently

# Now we can iterate over the time steps and run a box model at each location
for x, y in itertools.product(ds.x, ds.y):
    last_time = ds.time[0]
    for t in ds.time[1:]:
        temperature = ds.temperature[t, x, y]
        pressure = ds.pressure[t, x, y]
        air_density = ds.air_density[t, x, y]

        solver.set_rate(
            # photolysis.rates would produce something like {o2: 1e-5, o3: 1e-5, ...} 
            # and this function would know how to appropriatley set the values
            photolysis = photolysis.rates(temperature, pressure, air_density),
            emissions = {"nox": 2}, # emissions at this grid cell]
            loss = {"BC": 1} # loss at this grid cell
        )

        solver.solve(timestep=t-last_time, temperature=temperature,
                      pressure=pressure, air_density=air_density, 
                      concentrations=output[t - 1, x, y])

        output[t, x, y] = solver.concentrations
        last_time = t

# Option 2 solve all grid cells simultaneously
for t in ds.time[1:]:
    temperature = ds.temperature[t]
    pressure = ds.pressure[t]
    air_density = ds.air_density[t]

    solver.set_rate(
        # photolysis.rates would produce something like {o2: 1e-5, o3: 1e-5, ...} 
        # and this function would know how to appropriatley set the values
        photolysis = photolysis.rates(temperature, pressure, air_density),
        emissions = {}, # emissions at this grid cell]
        loss = [] # loss at this grid cell
    )

    solver.solve(timestep=t-last_time, temperature=temperature,
                  pressure=pressure, air_density=air_density, 
                  concentrations=output[t - 1])

    output[t] = solver.concentrations
    last_time = t

# Now we can calculate the percent error at each grid cell
for x in ds.x:
    for y in ds.y:
        for time in ds.time:
            for var in output.data_vars:
                error = abs(output[var][time, x, y] - ds[var][time, x, y]) / ds[var][time, x, y]
                print(f'Percent error for {var} at {time} in grid cell {x}, {y}: {error}')
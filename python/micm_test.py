import musica

#tests python micm package
time_step = 200.0
temperature = 272.5
pressure = 101253.3
num_concentrations = 5
concentrations = [0.75, 0.4, 0.8, 0.01, 0.02]

print(concentrations)

# What we have now
# solver = musica.create_micm("configs/chapman")  
# musica.micm_solve(solver, time_step, temperature, pressure, concentrations)

# Option 1
solver = musica.CreateMICM("configs/chapman")  
photolysis = musica.TUVX("configs/tuvx")

for time in range(0, 1000):
  solver.set_rate(photolysis.rates(temperature, pressure, air_density))
  solver.solve(time_step, temperature, pressure, concentrations)

# Option 2
# Only support configurations like this for muisca modules that work with C/C++
chemistry = musica.Chemistry(["stratosphere", "troposphere"], solver=musica.MICM, photolysis=musica.CloudJ)

for time in range(0, 1000):
  chemistry.solve(time_step, temperature, pressure, concentrations)

# Option 3 -- date time time step
import xarray as xr

conditions = xr.Dataset("chem_conditions.nc")
# latitude = [-90, -80]
# longtidue = [90, 80]
# time = [12/12/2020]
# species = ["a", "b", "c", "d", "e"]
#    - latitude
#    - longitude
#    - time
conditions["a"] = xr.array_like(conditions["temperature"], fill = np.nan)

conditions["time"] = [12/13/2020, 12/14/2020, 12/15/2020, 12/16/2020, 12/17/2020]

solver = musica.CreateMICM("configs/chapman")  
photolysis = musica.TUVX("configs/tuvx")

species_map = solver.species_map
# Ar -> 4
# N2 -> 3
# O2 -> 1

conditions.rename({
  "Argon": "Ar", 
  "Oxygen2": "O2"
}, inplace=True)

# reorder columns based on species_map
columns = conditions.columns[species_map.values()]

last_time = conditions.time[0]

for time in conditions.time[1:]:
  concentrations = conditions[columns].loc[last_time]
  solver.set_rate(photolysis.rates(temperature, pressure, air_density))

  temperature, pressure, air_density = conditions[time]["temperature", "pressure", "air_density"]

  new_concentrations = solver.solve(last_time=last_time, current_time=time, temperature, pressure, concentrations)

  conditions.loc[time] = new_concentrations
  last_time = time

# Option 4 -- musica defined state
import xarray as xr

conditions = xr.Dataset("chem_conditions.nc")

solver = musica.CreateMICM("configs/chapman")  
photolysis = musica.TUVX("configs/tuvx")
states = musica.State(conditions)

for state in states:
  solver.set_rate(photolysis.rates(temperature, pressure, air_density))
  time, temperature, pressure, air_density = *state
  solver.solve(time, temperature, pressure, concentrations)
  conditions.loc[time] = concentrations

# Option 5 -- only photolysis
  
photolysis = musica.TUVX("configs/tuvx")
rates = photolysis.rates(temperature, pressure, air_density)

# Option 6 -- chemistry cafe

solver, photolysis = musica.ChemistryCafe.TS1

# Option 7 -- defining the system in memory



print(concentrations)

assert concentrations[0] == 0.75
assert concentrations[1] != 0.4
assert concentrations[2] != 0.8
assert concentrations[3] != 0.01
assert concentrations[4] != 0.02

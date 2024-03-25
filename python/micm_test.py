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

print(concentrations)

assert concentrations[0] == 0.75
assert concentrations[1] != 0.4
assert concentrations[2] != 0.8
assert concentrations[3] != 0.01
assert concentrations[4] != 0.02

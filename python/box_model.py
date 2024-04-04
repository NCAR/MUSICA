import musica
import datetime
import json

# Use Case 1
# Simple MICM simulation
with open('flowtube.micm.json') as file:
  flow_tube = musica.Create(chemistry = musica.MICM(json.load(file)))

time_step = datetime.timedelta(seconds=200)  # s
conditions = {
  "temperature": 298.43,  # K
  "pressure": 101325.2,  # Pa
  "air density": 2.54e19 / 6.022e23 * 100 ^ 3 # mol m-3
}
initial_concentrations = {"O3": 0.1, "ISOPRENE": 0.05, "SOA1": 0.0, "SOA2": 0.0}

final_concentrations = flow_tube.solve(time_step, conditions, initial_concentrations)

# output something like:
# final_concentrations = {
# "O3": 0.08,
# "ISOPRENE": 0.03,
# "SOA1": 0.01,
# "SOA2": 0.0
# }

################################################################################

# Use Case 2
# Simple MICM and TUV-x calculation for a single grid cell over multiple time steps
# (assumes that TUV-x and MICM are configured with matching labels for photolysis rate constants)
with open('outdoor-chamber.micm.json') as micm_file:
  with open('outdoor-chamber.tuvx.json') as tuvx_file:
    outdoor_chamber = musica.Create(chemistry=musica.MICM(json.load(micm_file)),
                                    photolysis=musica.TUVX(json.load(tuvx_file)))

times = [datetime.datetime(2022, 1, 1, 0, 0),
         datetime.datetime(2022, 1, 1, 2, 0),
         datetime.datetime(2022, 1, 1, 4, 0),
         datetime.datetime(2022, 1, 1, 6, 0),
         datetime.datetime(2022, 1, 1, 8, 0),
         datetime.datetime(2022, 1, 1, 10, 0)]  # UTC
conditions = {
  "temperature": [297.8, 297.9, 298.0, 298.1, 298.2],  # K
  "pressure": [101320.0, 101330.0, 101340.0, 101310.0, 101325.0],  # Pa
  "air density" : [231.2, 231.3, 231.4, 231.5, 231.6],  # mol m-3
  "latitude" : 37.7749,  # deg N
  "longitude" : -122.4194,  # deg E
  "altitude" : 50.0,  # m
}
initial_concentrations = {"O3": 0.1, "ISOPRENE": 0.05, "SOA1": 0.0, "SOA2": 0.0}

# Solves for all times and conditions starting from initial_concentrations and returns final concentrations at each time step
# (this internally calculates TUV-x photolysis rates and passes them to MICM at each timestep)
final_concentrations = outdoor_chamber.solve(conditions, initial_concentrations)

# output something like:
# final_concentrations = {
# "O3": [0.1, 0.09, 0.08, 0.07, 0.06, 0.05],
# "ISOPRENE": [0.05, 0.04, 0.03, 0.02, 0.01, 0.0],
# "SOA1": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
# "SOA2": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]
# }

################################################################################

# A&M MusicBox example

box_model = BoxModel()

# configures box model
conditions_path = "configs/test_config_1/my_config.json"
camp_path = "configs/test_config_1/camp_data"

box_model.readConditionsFromJson(conditions_path)
box_model.create_solver(camp_path)

# solves and saves output
output = box_model.solve()

conc_a_index = output[0].index('CONC.A')
conc_b_index = output[0].index('CONC.B')
conc_c_index = output[0].index('CONC.C')

#extracts model concentrations from data output
model_concentrations = [[row[conc_a_index], row[conc_b_index], row[conc_c_index]] for row in output[1:]]



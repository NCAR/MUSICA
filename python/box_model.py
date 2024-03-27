import musica
import datetime

# Simple MICM simulation
flow_tube = musica.Create(chemistry = musica.MICM("flowtube.micm.json"))

time_step = 200.0  # s
conditions = {
  "temperature": 298.43,  # K
  "pressure": 101325.2,  # Pa
  "air density": 2.54e19 / 6.022e23 * 100 ^ 3 # mol m-3
}
initial_concentrations = {"O3": 0.1, "ISOPRENE": 0.05, "SOA1": 0.0, "SOA2": 0.0}

final_concentrations = flow_tube.solve(time_step, conditions, initial_concentrations)


# Simple MICM and TUV-x calculation
# (assumes that TUV-x and MICM are configured with matching labels for photolysis rate constants)
outdoor_chamber = musica.Create(chemistry = musica.MICM("outdoor-chamber.micm.json"),
                                photolysis = musica.TUV("outdoor-chamber.tuvx.json"))

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

# (this internally calculates TUV-x photolysis rates and passes them to MICM)
final_concentrations = outdoor_chamber.solve(times, conditions, initial_concentrations)



import musica

# Simple MICM simulation
micm = musica.CreateChemistrySolver("flowtube.mech.json")

time_step = 200.0  # s
conditions = {
  "temperature": 298.43,  # K
  "pressure": 101325.2,  # Pa
  "air density": 2.54e19 / 6.022e23 * 100 ^ 3 # mol m-3
}
initial_concentrations = {"O3": 0.1, "ISOPRENE": 0.05, "SOA1": 0.0, "SOA2": 0.0}

final_concentrations = micm.solve(time_step, conditions, initial_concentrations)


# Simple MICM and TUV-x calculation

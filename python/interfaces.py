class Photolysis():
    def __init__(self):
      pass

    def rates(self, temperature, pressure, air_density):
        # calculate the photolysis rates
        return {self.species: self.rate}

class TUVX(Photolysis):
    def __init__(self, config):
        self.config = config
        self.species = config.species
        self.calculator = musica.create_tuvx(config)
      
    def rates(self, temperature, pressure, air_density):
        return self.calculator.calculate(temperature, pressure, air_density)

class CloudJ(Photolysis):
    def __init__(self, config):
        self.config = config
        self.species = config.species
        import harvard.cloudj as cloudj
        self.calculator = cloudj.create(config)
      
    def rates(self, temperature, pressure, air_density):
        return self.calculator.calculate(temperature, pressure, air_density)
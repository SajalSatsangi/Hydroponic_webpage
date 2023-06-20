air_temperature_C_high = 35
air_temperature_C_low = 5
air_temperature = self.condition("{asdf1234}")
if air_temperature is not None:
    if air_temperature > air_temperature_C_high:
        self.message += "Air temperature is too high! ({} C) \n".format(air_temperature)
    elif air_temperature < air_temperature_C_low:
        self.message += "Air temperature is too low! ({} C) \n".format(air_temperature)
    else:
        return
    self.run_action("{qwer5678}", message=self.message)
else:
    self.message += "Cold not find an air temperature measurement. Check your sensor!"
    self.run_action("{qwer5678}", message=self.message)
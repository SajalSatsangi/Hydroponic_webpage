bool_water_float = self.condition("{asdf1234}")
if bool_water_float is not None:
    if bool_water_float == 1:
        self.message += "The water level is low. Add water.\n"
        self.run_action("{qwer5678}", message=self.message)
else:
    self.message += "No water float measurement found!"
    self.run_action("{qwer5678}", message=self.message)
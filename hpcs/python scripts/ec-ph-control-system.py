import time
# Desired range for electrical conductivity (hopefully)
range_ec_high = 1300
range_ec_low = 1000
# Desired range for pH (hopefully)
range_ph_high = 6.2
range_ph_low = 5.5
# pH range that will immediately cause a pH correction (DANGER ZONE)
range_ph_high_danger = 7.0
range_ph_low_danger = 5.0
### Edit below to set the IDs for Conditions and Actions ###
condition_id_measurement_ph_id = "PH_MEASURE_ID"  # Condition: measurement, last, pH Input
condition_id_measurement_ec_id = "EC_MEASURE_ID"  # Condition: measurement, last, EC Input
action_id_pump_1_acid = "PUMP_1_ID"  # Action: Acid
action_id_pump_2_base = "PUMP_2_ID"  # Action: Base
action_id_pump_3_nutrient_a = "PUMP_3_ID"  # Action: Nutrient 1
action_id_pump_4_nutrient_b = "PUMP_4_ID"  # Action: Nutrient 2
action_id_email_notification = "EMAIL_ID"  # Action: Email Notification
if 'notify_ec' not in self.variables:  # Initiate EC timer
    self.variables['notify_ec'] = 0
if 'notify_ph' not in self.variables:  # Initiate pH timer
    self.variables['notify_ph'] = 0
if 'notify_none' not in self.variables:  # Initiate None measurement notification timer
    self.variables['notify_none'] = 0
measure_ec = self.condition(condition_id_measurement_ec_id)
measure_ph = self.condition(condition_id_measurement_ph_id)
self.logger.debug(f"Conditional check. EC: {measure_ec}, pH: {measure_ph}")
if None in [measure_ec, measure_ph]:
    if measure_ec is None:
        self.message += "\nWarning: No EC Measurement! Check sensor!"
    if measure_ph is None:
        self.message += "\nWarning: No pH Measurement! Check sensor!"
    if self.variables['notify_none'] < time.time():  
        self.variables['notify_none'] = time.time() + 43200  
        self.run_action(action_id_email_notification, message=self.message)  
    return
if measure_ph < range_ph_low_danger:  # pH dangerously low, add base (pH up)
    msg = f"pH is dangerously low: {measure_ph}. Should be > {range_ph_low_danger}. Dispensing 1 ml base"
    self.logger.debug(msg)
    self.message += msg
    self.run_action(action_id_pump_2_base)  
    if self.variables['notify_ph'] < time.time(): 
        self.variables['notify_ph'] = time.time() + 43200  
        self.run_action(action_id_email_notification, message=self.message)  
elif measure_ph > range_ph_high_danger:  # pH dangerously high, add acid (pH down)
    msg = f"pH is dangerously high: {measure_ph}. Should be < {range_ph_high_danger}. Dispensing 1 ml acid"
    self.logger.debug(msg)
    self.message += msg
    self.run_action(action_id_pump_1_acid)  
    if self.variables['notify_ph'] < time.time():  
        self.variables['notify_ph'] = time.time() + 43200 
        self.run_action(action_id_email_notification, message=self.message) 
# If pH isn't dangerously low or high, check if EC is within range
elif measure_ec < range_ec_low:  # EC too low, add nutrient
    self.logger.debug(f"EC: {measure_ec}. Should be > {range_ec_low}. Dosing 3 ml Nut A, 3 ml Nut B")
    self.run_action(action_id_pump_3_nutrient_a)  # Dispense 3 ml nutrient 1
    self.run_action(action_id_pump_4_nutrient_b)  # Dispense 3 ml nutrient 2
elif measure_ec > range_ec_high:  # EC too high, add nutrient
    msg = f"EC: {measure_ec}. Should be < {range_ec_high}. Need to add water to dilute!"
    self.logger.debug(msg)
    if self.variables['notify_ec'] < time.time():  
        self.variables['notify_ec'] = time.time() + 43200 
        self.message += msg
        self.run_action(action_id_email_notification, message=self.message)  
# If EC is in range, make sure pH is within range
elif measure_ph < range_ph_low:  # pH too low, add base (pH up)
    self.logger.debug(f"pH is {measure_ph}. Should be > {range_ph_low}. Dispensing 1 ml base")
    self.run_action(action_id_pump_2_base)  # Dispense 1 ml base (pH up)
elif measure_ph > range_ph_high:  # pH too high, add acid (pH down)
    self.logger.debug(f"pH is {measure_ph}. Should be < {range_ph_high}. Dispensing 1 ml acid")
    self.run_action(action_id_pump_1_acid)  # Dispense 1 ml acid (pH down)
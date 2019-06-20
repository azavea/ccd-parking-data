DTD = {
    'mo': 10,
    'tu': 11,
    'we': 12,
    'th': 13,
    'fr': 14,
    'sa': 15,
    'su': 16
}

REGULATIONS = {
    'No Stopping': {'type': 'reg_is'},
    'No Parking (Driveway)': {'type': 'reg_is'},
    'No Parking': {'type': 'reg_is'},
    'Bicycles Only': {'type': 'reg_is'},
    'No Stopping (Except Bicycles)': {'type': 'reg_is'},
    'No Standing': {'type': 'reg_is'},
    'Indego Bike Zone': {'type': 'reg_is'},
    'CCD Only Parking': {'type': 'reg_is'},
    'Judges Only': {'type': 'reg_is'},
    'Seniors Only': {'type': 'reg_is'},
    'SEPTA Vehicles Only': {'type': 'reg_is'},
    'Philadelphia Tours Only': {'type': 'reg_is'},
    'Inspector General Only': {'type': 'reg_is'},
    'City Controler Only': {'type': 'reg_is'},
    'Love Park Authorized Vehicles Only': {'type': 'reg_is'},
    'Private Parking': {'type': 'reg_is'},
    'Handicaped Parking': {'type': 'reg_is'},
    'Hub of Hope Volunteers Only': {'type': 'reg_is'},
    'City Council Only': {'type': 'reg_is'},
    'Press Only Parking': {'type': 'reg_is'},
    'Philadelphia Trolley Works Only': {'type': 'reg_is'},
    'District Attorney Only': {'type': 'reg_is'},
    'Red Cross Only': {'type': 'reg_is'},
    'Military Parking Only': {'type': 'reg_is'},
    'Police Only Parking': {'type': 'reg_is'},
    'Carriage Only': {'type': 'reg_is'},
    'Consoul Vehicles Only': {'type': 'reg_is'},
    'Authoirzed Vehicles Only': {'type': 'reg_is'},
    'Tour Bus Loading Only': {'type': 'reg_is'},
    'Registered Package Delivery Companies Only ': {'type': 'reg_is'},
    'Federal Governemnt Parking Only': {'type': 'reg_is'},
    'Municipal Government Vehicles Prohibited': {'type': 'reg_is_not'},
    'Truck Loading Only': {'type': 'reg_is'},
    'Loading Zone': {'type': 'reg_is'},
    'Motorcycle Parking': {'type': 'reg_is'},
    'Bus Zone': {'type': 'reg_is'},
    'Passenger Loading Only': {'type': 'reg_is'},
    'Truck Only Parking': {'type': 'reg_is'},
    'Valet Parking': {'type': 'reg_is'},
    'Passenger Drop Off / Pick Up': {'type': 'reg_is'},
    'Fire Zone': {'type': 'reg_is'},
    'Enterprise Car Share Reserved Parking': {'type': 'reg_is'},
    'Hotel Loading Only': {'type': 'reg_is'},
    'Ambulance Zone': {'type': 'reg_is'},
    'Taxi Parking': {'type': 'reg_is'},
    'Electric Vehicle Only': {'type': 'reg_is'},
    'Time Limited Auto Parking': {'type': 'reg_is'},
    'Contractor Placard Not Valid': {'type': 'contractor_placard'},
    'No Truck Idling': {'type': 'reg_is_not'},
    'Truck Parking Prohibited': {'type': 'reg_is_not'},
    'Other (See Notes)': {'type': 'reg_is_not'},
    'No Regulations Listed': {'type': 'reg_is'},
    'Snow Emergency Zone': {'type': 'snow_reg'}
}

REGULATION_HIERARCHY = [
    'Registered Package Delivery Companies Only ',
    'Passenger Drop Off / Pick Up',
    'No Stopping',
    'Truck Loading Only',
    'Time Limited Auto Parking',
    'Valet Parking',
    'Federal Governemnt Parking Only',
    'City Council Only',
    'Passenger Loading Only',
    'Authoirzed Vehicles Only',
    'Fire Zone',
    'Bus Zone',
    'Consoul Vehicles Only',
    'CCD Only Parking',
    'Press Only Parking',
    'Philadelphia Tours Only',
    'Ambulance Zone',
    'Judges Only',
    'Inspector General Only',
    'No Parking',
    'No Parking (Driveway)',
    'Loading Zone',
    'Handicaped Parking',
    'Taxi Parking',
    'Enterprise Car Share Reserved Parking'
]

# Default values
REG_IS_DEFAULT = 'Unlimited Parking'
REG_IS_NOT_DEFAULT = 'None'
CONTRACTOR_PLACARD_DEFAULT = 'Valid'
PAID_DEFAULT = 'No'
TIME_LIMIT_DEFAULT = 'None'
PERMIT_ZONE_DEFAULT = 'None'
CHECK_FLAG_DEFAULT = 'No'
SNOW_EMERGENCY_DEFAULT = 'No'

COLUMNS = ['id', 'length', 'block', 'street', 'day', 'hour', 'reg_is', 'reg_is_not',
           'time_limit', 'paid', 'tow_zone', 'contractor_placard', 'permit_zone',
           'snow_emergency_zone', 'check']
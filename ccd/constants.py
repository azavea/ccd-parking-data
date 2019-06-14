dtd = {
    'mo': 10,
    'tu': 11,
    'we': 12,
    'th': 13,
    'fr': 14,
    'sa': 15,
    'su': 16
}

non_regs = ['Contractor Placard Not Valid']

regulations = {
    'No Stopping': {'type': 'reg_is_not'},
    'No Parking (Driveway)': {'type': 'reg_is_not'},
    'No Parking': {'type': 'reg_is_not'},
    'Bicycles Only': {'type': 'reg_is'},
    'No Stopping (Except Bicycles)': {'type': 'reg_is_not'},
    'No Standing': {'type': 'reg_is_not'},
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
    'Contractor Placard Not Valid': {'type': 'reg_is_not'},
    'No Truck Idling': {'type': 'reg_is_not'},
    'Truck Parking Prohibited': {'type': 'reg_is_not'},
    'Other (See Notes)': {'type': 'reg_is'},
    'No Regulations Listed': {'type': 'reg_is_not'},
    'Snow Emergency Zone': {'type': 'reg_is_not'}
}

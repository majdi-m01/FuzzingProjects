"""
This is the grammar to be used in the project. Please do not modify.
"""

PRINTER_GRAMMAR = {
    '<start>': ['<json>'],
    '<json>': ['{<printer_info>}'],
    '<printer_info>': ['<manufacturer>, <model>, <serial_number>, <printer_type>, <status>, <resolution>, <copies_printed>, <os_compatibility>, <security_features>, <has_warranty>, <needs_check>'],
    '<manufacturer>': ['"manufacturer": <manufacturer_values>'],
    '<manufacturer_values>': [
        '"Canon"', '"HP"', '"Epson"', '"Samsung"',
        '"Brother"', '"Lexmark"', '"Kyocera"', '"Ricoh"',
        '"Xerox"', '"Konica Minolta"', '"Panasonic"', '"Toshiba"',
        '"Sharp"', '"Dell"', '"OKI"', '"Fujifilm"'
    ],
    '<model>': ['"model": <model_values>'],
    '<serial_number>': ['"serialNumber": <serial_values>'],
    '<printer_type>': ['"type": <type_values>'],
    '<status>': ['"status": <status_values>'],
    '<resolution>': ['"resolution": [<resolution_values>]'],
    '<os_compatibility>': ['"operatingSystem": [<os_values>]'],
    '<security_features>': ['"securityFeatures": [<security_values>]'],
    '<model_values>': [
        '"Canon Laser Pixma MG3620"',
        '"Canon Maxify MB5420"',
        '"Canon Laser ImageClass LBP622Cdw"',
        '"HP OfficeJet Pro 9015"',
        '"HP LaserJet Pro M15w"',
        '"HP DeskJet 3755"',
        '"Epson EcoTank ET-3760"',
        '"Epson WorkForce WF-2830"',
        '"Samsung Expression Photo HD XP-15000"',
        '"Brother Xpress M2020W"',
        '"Samsung ProXpress C3060FW"',
        '"Brother HL-L2395DW"',
        '"Lexmark MC3224dwe"',
        '"Kyocera ECOSYS P5026cdw"',
        '"Ricoh SP C261DNw"',
        '"Xerox Laser 6510/DNI"',
        '"Konica Minolta Bizhub C458"',
        '"Panasonic Laser KX-MB2170"',
        '"Toshiba Laser e-STUDIO5005AC"',
        '"Sharp MX-3070N"',
        '"Dell C1760NW"',
        '"OKI C612dn"',
        '"Fujifilm Laser Share SP-3"'
    ],
    '<serial_values>': [
        '<digits>',
    ],
    '<digits>': ['<digit><digits>', '<digit>'],
    '<digit>': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    '<type_values>': ['"inkjet"', '"laser"'],
    '<status_values>': [
        '"ready"',
        '"offline"',
        '"error"',
        '"busy"'],
    '<resolution_values>': [
        '<resolution_single>',
        '<resolution_single>, <resolution_values>',
    ],
    '<resolution_single>': [
        '"600x600 DPI"',
        '"1200x1200 DPI"',
        '"2400x1200 DPI"',
        '"4800x2400 DPI"'
    ],
    '<copies_printed>': ['"copiesPrinted": <digitsCopiesPrinted>'],
    "<digitsCopiesPrinted>": ['<digits>'],
    '<os_values>': [
        '<os_single>',
        '<os_single>, <os_values>'],
    '<os_single>': [
        '"Windows"',
        '"Linux"',
        '"MacOS"'
    ],
    '<security_values>': [
        '',
        '<security_something>',
    ],
    '<security_something>': [
        '<security_single>',
        '<security_single>, <security_something>',
    ],
    '<security_single>': [
        '"Password Protection"',
        '"Secure Print"',
        '"Network Security"',
        '"Encryption"'
    ],
    '<has_warranty>': ['"hasWarranty": <warranty_values>'],
    '<warranty_values>': ['0', '1'],
    '<needs_check>': ['"needsCheck": <check_values>'],
    '<check_values>': ['0', '1'],
}

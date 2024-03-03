"""
These are the oracles to be used in the project. Please do not modify.
"""


def structure_must_be_valid(printer: dict) -> bool:
    assert type(printer["manufacturer"]) == str
    assert type(printer["model"]) == str
    assert type(printer["serialNumber"]) == int
    assert type(printer["type"]) == str
    assert type(printer["status"]) == str
    assert type(printer["copiesPrinted"]) == int
    assert type(printer["resolution"]) == list
    assert type(printer["operatingSystem"]) == list
    assert type(printer["securityFeatures"]) == list
    assert type(printer["hasWarranty"]) == int
    assert type(printer["needsCheck"]) == int


def has_warranty_xor_needs_check(printer: dict) -> bool:
    """
    Check if the printer has a warranty XOR needs a check.

    Args:
        printer (dict): A dictionary representing the printer with keys 'hasWarranty' and 'needsCheck'.

    Returns:
        bool: The result of the XOR operation between 'hasWarranty' and 'needsCheck'.
    """
    structure_must_be_valid(printer)
    has_warranty = printer['hasWarranty']
    needs_check = printer['needsCheck']
    return has_warranty ^ needs_check


def manufacturer_in_model_with_check_must_be_zero(printer: dict) -> bool:
    """
    Check if the manufacturer is included in the model name and if the 'needsCheck' value is equal to zero.

    Args:
        printer (dict): A dictionary containing information about the printer.

    Returns:
        bool: True if the manufacturer is included in the model name and the 'needsCheck' value is equal to zero, False otherwise.
    """
    structure_must_be_valid(printer)
    manufacturer = printer['manufacturer']
    model = printer['model']
    needs_check = printer['needsCheck']
    return manufacturer in model and needs_check == 0


def serial_in_model_and_check_not_in_model(printer: dict) -> bool:
    """
    Check if the serial number is included in the model name and if the 'needsCheck' value is not included in the model name.

    Args:
        printer (dict): A dictionary containing information about the printer.

    Returns:
        bool: True if the serial number is included in the model name and if the 'needsCheck' value is not included in the model name, False otherwise.
   """
    structure_must_be_valid(printer)
    serial_number = printer['serialNumber']
    model = printer['model']
    needs_check = printer['needsCheck']
    return str(serial_number) in model and str(needs_check) not in model


def status_length_equals_copies_printed(printer: dict) -> bool:
    """
    Check if the length of the status is equal to the number of copies printed.

    Args:
        printer (dict): A dictionary representing the printer information.

    Returns:
        bool: True if the length of the status is equal to the number of copies printed; False otherwise.
    """
    structure_must_be_valid(printer)
    status = printer['status']
    copies_printed = printer['copiesPrinted']
    return len(status) == copies_printed


def type_length_xor_copies_printed_equals_one(printer: dict) -> bool:
    """
    Check if the XOR with the length of the type name and the number of copies printed is one.

    Args:
        printer (dict): A dictionary representing the printer information.

    Returns:
        bool: True if the XOR with the length of the type name and the number of copies printed is one; False otherwise.
    """
    structure_must_be_valid(printer)
    printer_type = printer['type']
    copies_printed = printer['copiesPrinted']
    return len(printer_type) ^ copies_printed == 1


def type_length_xor_status_length_equals_zero(printer: dict) -> bool:
    """
    Check if the XOR with the length of the type name and the length of the status is zero.

    Args:
        printer (dict): A dictionary representing the printer information.

    Returns:
        bool: True if the XOR with the length of the type name and the length of the status is zero; False otherwise.
    """
    structure_must_be_valid(printer)
    printer_type = printer['type']
    status = printer['status']
    return len(printer_type) ^ len(status) == 0


#validation of fields that are required
def validate_required(row, variable, metadata, formater,pre_checks=[]):
    """

    :param row:
    :param variable:
    :param metadata:
    :param formater:
    :param pre_checks:
    :return:
    """
    errors=[]
    for fun in pre_checks:
        if fun(row,variable,metadata)==False:
            return errors

    if metadata.get_is_required(variable) is True:
        if row[variable] is None:
            errors.append(formater(row, variable, error_type="Required", message="'{}' is required".format(metadata.get_label(variable))))
    return errors

# validation of fields that are not required but have no entries
def validate_no_entry(row,variable,metadata,formater,pre_checks=[]):
    errors=[]
    for fun in pre_checks:
        if fun(row,variable,metadata)==False:
            return errors
    if metadata.get_is_required(variable) is None:
        if row[variable] == '':
            errors.append(formater(row, variable, error_type="No entry", message="'{}' has no data!".format(metadata.get_label(variable))))
    return errors

# validation of range
def validate_range(row, variable, metadata,formater,pre_checks=[]):
    """

    :param row:
    :param variable:
    :param metadata:
    :param formater:
    :param pre_checks:
    :return: whether or not a value falls into the required range

    """
    errors = []
    for fun in pre_checks:
        if fun(row,variable,metadata)==False:
            return errors

    l = row[variable]
    if l is None:
        return errors
    if metadata.get_valid_range(variable) is not None:
        min, max = metadata.get_valid_range(variable)

        if(min is not None):
            if (l<min): errors.append(formater(row, variable, error_type="is_below_minimum", message="'{}' is below minimum.".format(metadata.get_label(variable))))

        if (max is not None):
            if (l> max):errors.append(formater(row, variable, error_type="is_above_maximum", message="'{}' is above maximum.".format(metadata.get_label(variable))))

    return errors


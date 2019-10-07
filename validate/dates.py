

def date_checks(row, variable, d1=None, d2=None, formater=None, metadata=None, error_text="Date out of range", pre_checks=[]):
    errors = []
    for fun in pre_checks:
        if fun(row,variable,metadata)==False:
            return errors
    errors2 = []
    if row[variable] is None:
        return errors

    if (d1 is not None):
        if (row[d1] is not None):
            if row[variable] < row[d1]:
                errors.append(formater(row, variable=variable, error_type=error_text, message="{} should come after {}".format(metadata.get_label(variable), metadata.get_label(d1))))

    if (d2 is not None):
        if (row[d2] is not None):
            if row[variable] > row[d2]:
                errors.append(formater(row, variable=variable, error_type=error_text, message="{} should come before {}".format(metadata.get_label(variable), metadata.get_label(d2))))

    for i in errors:
        if type(i) == list:
            if len(i) > 0:
                errors2.append(i)
        else:
            errors2.append(i)

    return errors2


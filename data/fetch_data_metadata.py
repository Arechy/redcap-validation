import requests
import json
import pandas as pd
from datetime import datetime


# gets data from redcap
def get_data(project, start=None, stop=None,variables=None):
    """
    :param project: A project object
    :param start: start date eg '2009-01-01'. leave None for beginning of study
    :param stop: stop date eg '2009-01-02'. leave None for latest input
    :param variables:
    :return:
    """


    data = {
        'token': project.token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'fields[0]': project.id_var,
        'fields[1]': project.date_var,
        #'record[]': outputTwo(),
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    request = requests.post(project.url, data=data, verify=False)
    data = json.loads(request.text)
    data2 = pd.DataFrame(data)
    data2[project.date_var] = pd.to_datetime(data2[project.date_var])

    if start is not None:
        data2 = data2.loc[data2[project.date_var] >= pd.to_datetime(start), :]

    if stop is not None:
        data2 = data2.loc[data2[project.date_var] <= pd.to_datetime(stop), :]

    # print(data2)
    if data2.shape[0] == 0:
        return []

    x = {}

    for i, j in enumerate(data2[project.id_var]):
        x["records[{}]".format(i)] = '{}'.format(j)

    data = {
        'token': project.token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    for k, v in x.items():
        data[k] = v

    if variables is not None:
        for i,v in enumerate(variables):
            data[f'fields[{i}]'] = v

    request = requests. post(project.url, data=data, verify=False)
    data = json.loads(request.text)


    return data


# gets metadata from redcap

def get_metadata(project):
    """

    :param project: project object
    :returns: metadata
    """
    data1 = {
        'token': project.token,
        'content': 'metadata',
        'format': 'json',
        'returnFormat': 'json'
    }

    request1 = requests.post(project.url, data=data1, verify=False)
    data1 = json.loads(request1.text)
    return data1



class Metadata:

    def __init__(self, metadata):
        self.metadata = metadata
        self.vars_expanded = []
        self.vars_non_expanded = []
        self.metadata_expanded = {}
        self.metadata_non_expanded = {}
        for v in metadata:
            self.vars_non_expanded.append(v['field_name'])
            self.metadata_non_expanded[v['field_name']] = v
            if v['field_type'] == 'checkbox':
                t = v['select_choices_or_calculations']
                t2 = t.split("|")
                t3 = list(map(lambda x: x.split(",")[0], t2))
                t3b=[str.strip(i) for i in t3]
                t4 = [v['field_name'] + "___" + i for i in t3b]
                t5 = [i.replace("-", "_") for i in t4]
                self.vars_expanded = self.vars_expanded+t5
                for v2 in t5:
                    self.metadata_expanded[v2] = v

            else:
                self.vars_expanded.append(v['field_name'])
                self.metadata_expanded[v['field_name']] = v


    def exists(self, variable):
        """

        :param variable: variable
        :return: True or False depending on whether the variable exists in the metadata
        """
        result = variable in (self.vars_expanded + self.vars_non_expanded)
        return result

    def get_variables(self, expand_checkbox=True):
        """
        :param expand_checkbox: if true the function returns expanded variables and vice versa
        :return:
        """
        if expand_checkbox:
            return self.vars_expanded
        else:
            return self.vars_non_expanded

    def get_variables_without_description(self):
        """
        :return: variables which
        """
        variables = self.get_variables(expand_checkbox=True)
        for variable in variables:
            if self.metadata_expanded[variable]['field_type'] == 'descriptive':
                variables.remove(variable)
        return variables

    def get_label(self, variable):
        """
               :param variable: variable
               :return: the label of the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        label=self.metadata_expanded[variable]['field_label']
        return label

    def get_type(self, variable):
        """
               :param variable: variable
               :return: the type of the data in the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        type_=self.metadata_expanded[variable]['text_validation_type_or_show_slider_number']
        v_type='str'
        if type_ == '':
            v_type = 'str'
        elif 'date' in type_:
            v_type = 'date'
        elif type_ == "number":
            v_type = 'float'
        elif type_ == 'integer':
            v_type = 'int'

        return v_type

    def get_valid_range(self, variable):

        """
               :param variable: variable
               :return: the range of the given variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        min = self.metadata_expanded[variable]['text_validation_min']
        if min == '':
            min=None
        else:
            type_=self.get_type(variable)
            if type_ == 'float':
                min=float(min)
            elif type_ == 'date':
                min=datetime.strptime(min,'%Y-%m-%d')
            elif type_ == 'int':
                min = int(min)

        max = self.metadata_expanded[variable]['text_validation_max']
        if max == '':
            max=None
        else:
            type_ = self.get_type(variable)
            if type_ == 'float':
                max = float(max)
            elif type_ == 'date':
                max = datetime.strptime(max, '%Y-%m-%d')
            elif type_ == 'int':
                max = int(max)

        range=None
        if (min is not None) | (max is not None): range = (min, max)
        return range

    def get_is_required(self,variable):
        """
               :param variable: variable
               :return: true or false depending on whether a variable is required or not
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        required = self.metadata_expanded[variable]['required_field']
        if required == '': required = False
        else: required = True
        return required

    def get_choices(self, variable):
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        choice = self.metadata_expanded[variable]['select_choices_or_calculations']
        choices = dict(item.split(",") for item in choice.split("|"))

        return choices

    def get_branching_logic(self, variable):
        """
        :param variable: variable
        :return: the branching logic of the variable
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        logic = self.metadata_expanded[variable]['branching_logic']
        if logic == '':
            logic2 = None
        else:
            logic2 = logic
        return logic2

    def get_hidden(self, variable):
        """
               :param variable: variable
               :returns: true or false whether the variable is hidden or not
        """
        if not self.exists(variable):
            raise Exception("Variable {} does not exist".format(variable))
        hidden = self.metadata_expanded[variable]['field_annotation']
        if hidden == '':
            return False
        elif '@HIDDEN' in hidden:
            return True
        else:
            return False

    def format_data(self, row=None):

        """
               :param variable: row
               :return: a row whose values have been converted to their respective types
        """
        new_row = {}
        for variable, value in row.items():
            if value == '':
                new_row[variable] = None
                continue
            type_ = self.get_type(variable=variable)
            if type_ == 'str':
                new_row[variable] = value
            elif type_ == 'float':
                new_row[variable] = float(value)
            elif type_ == 'int':
                new_row[variable] = int(value)
            elif type_ == 'date':
                new_row[variable] = datetime.strptime(value, '%Y-%m-%d')
        return new_row







#!/usr/bin/env python
# File created on 10 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from copy import deepcopy
from qiime.sort import signed_natsort
from qiime.filter import filter_mapping_file

def resample_mapping_file(data, headers, sampling_period, subject, time):
    """ """
    data = deepcopy(data)
    headers = deepcopy(headers)

    time_index = headers.index(time)
    subject_index = headers.index(subject)

    headers.append(INTERPOLATION_COLUMN_NAME)
    data = [row.append('No') for row in data]

    list_of_subjects = list(set([data[subject_index] for row in data]))
    for single_subject in list_of_subjects:
        per_subject_data = [row for row in data if row[subject_index] ==\
            single_subject]

        time_tuples = [(per_subject_data[0], per_subject_data[time_index])\
            for line in per_subject_data]

        resampled_time_tuples = resample_ids_for_time(time_tuples,\
            sampling_period)

    return data, headers

def resample_ids_for_time(data, sampling_period):
    """ """

    # sort using the first element as key
    data = signed_natsort(data)
    out_data = data

    for i in range(len(data)-1):
        if (data[i][1]+sampling_period) != data[i+1][1]:
            out_data = None

    return data

def linear_interpolation(data, gradient, sampling_period):
    """ """
    for element in data:
        pass


INTERPOLATION_COLUMN_NAME = 'InterpolatedByQIIME'

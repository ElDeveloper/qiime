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


from qiime.resample import resample_mapping_file

from biom.parse import parse_biom_table
from qiime.parse import parse_mapping_file
from qiime.filter import filter_mapping_file
from qiime.util import (parse_command_line_parameters, make_option,get_options_lookup)

options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    options_lookup['otu_table_as_primary_input'],
    options_lookup['mapping_fp'],
    make_option('-s','--subject_column_name', type='string', help='mapping file'
    ' column describing the subject of the study; commonly HOST_SUBJECT_ID'),
    make_option('-t','--time_column_name', type='string', help='mapping file '
    'column describing the temporal gradient in the study, all the elements '
    'must be real numbers. It is recommended for all the subjects to be in the'
    'same scale'),
    make_option('-f','--sampling_period', type='float', help='sampling period '
    'after the resampling is computed; the difference between samples in the '
    'temporal gradient (--time_column_name)')
]
script_info['optional_options'] = [
    make_option('-o','--output_biom_fp',type='new_filepath', help='the output '
    'otu table in biom format (recommended extension: .biom) with added interpo'
    'lated points [default: %default]', default='interpolated_otu_table.biom'),
    make_option('-n','--output_mapping_fp',type='new_filepath', help='output '
    'mapping file with new mockup sample identifiers for the interpolated '
    'points [default: %default]', default='interpolated_mapping_file.biom')
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_otu_table_fp = opts.otu_table_fp
    input_mapping_file_fp = opts.mapping_fp
    sampling_period = opts.sampling_period
    time_column_name = opts.time_column_name
    subject_column_name = opts.subject_column_name

    output_otu_table_fp = opts.output_biom_fp
    output_mapping_file_fp = opts.output_mapping_fp

    mapping_file_data, mapping_file_headers, _ = parse_mapping_file(open(
        input_mapping_file_fp, 'U'))
    biom_object = parse_biom_table(open(input_otu_table_fp, 'U'))

    missing_fields = [field for field in [time_column_name, subject_column_name]
        if field not in mapping_file_headers]
    if missing_fields:
        option_parser.error('The mapping file does not contain the following '
            'headers: %s.' % ', '.join(missing_fields))

    usable_sample_ids = list(biom_object.SampleIds)
    mapping_file_headers, mapping_file_data = filter_mapping_file(
        mapping_file_data, mapping_file_headers, usable_sample_ids, True)

    time_column_index = mapping_file_headers.index(time_column_name)

    offending_ids = []
    for line in mapping_file_data:
        try:
            dummy = float(line[time_column_index])
        except:
            offending_ids.append(line[0])
    if len(offending_ids):
        option_parser.error('The column \'%s\' of the '% (time_column_name)+\
            'mapping file must have only real numbers, the following sample '
            'identifiers, were found to not meet this criteria: {0}.'.format(
            ', '.join(offending_ids)))

    mapping_file_data, mapping_file_headers = resample_mapping_file(
        mapping_file_data, mapping_file_headers, sampling_period,
        subject_column_name, time_column_name)

if __name__ == "__main__":
    main()
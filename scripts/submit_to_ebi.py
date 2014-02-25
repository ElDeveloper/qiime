#!/usr/bin/env python
# File created on 25 Feb 2014
from __future__ import division

__author__ = "AUTHOR_NAME"
__copyright__ = "Copyright 2014, The Qiita Project"
__credits__ = ["Emily Jean Of The TerAvest", "Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "AUTHOR_NAME"
__email__ = "AUTHOR_EMAIL"


from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
# Members of the tuple in script_usage are (title, description, example call)
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    # Example required option
    #make_option('-i', '--input_fp', type='existing_filepath',
    #            help='the input filepath')
]
script_info['optional_options'] = [
    # Example optional option
    #make_option('-o', '--output_dir', type="new_dirpath",
    #            help='the output directory [default: %default]')
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

if __name__ == "__main__":
    main()
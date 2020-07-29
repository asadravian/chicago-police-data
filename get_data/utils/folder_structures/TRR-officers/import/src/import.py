#!usr/bin/env python3
#


'''import script for TRR-officers_2004-2016_2016-09_p046360'''

import pandas as pd
import __main__
import sys


from import_functions import standardize_columns, collect_metadata
import setup


def create_metadata_filename(filename):
    file_split = filename.split('/')
    return file_split[0] + '/metadata_' + file_split[1]


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': sys.argv[1],
        'output_file': sys.argv[2],
        'metadata_file': create_metadata_filename(sys.argv[2]),
        'main_sheet': 'TRRData',
        'star_sheet': 'Star #',
        'notes_sheet': ['Notes', 'Source Info and Notes'],
        'main_keep_columns': [
            'TRR_REPORT_ID', 'POLAST', 'POFIRST', 'POGNDR',
            'PORACE', 'POYRofBIRTH', 'APPOINTED_DATE', 'UNITASSG',
            'UNITDETAIL', 'ASSGNBEAT', 'RANK', 'DUTYSTATUS',
            'POINJURED', 'MEMBER_IN_UNIFORM'
            ],
        'main_column_names_key': 'TRR-officers_2004-2016_2016-09_p046360',
        'star_column_names_key': 'TRR-stars_2004-2016_2016-09_p046360'
        }

    assert args['input_file'].startswith('input/'),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

for value in cons.notes_sheet:
    try:
        notes_df = pd.read_excel(cons.input_file, sheet_name=value,
                            header=None)
    except ValueError:
        log.info(f'{value} Not found in sterilized doc')
notes = '\n'.join(notes_df.ix[notes_df[0].isin([cons.main_sheet,
                                                cons.star_sheet]),
                              1].dropna())
cons.write_yamlvar('Notes', notes)
log.info('Notes written to cons: {}'.format(notes))

main_df = pd.read_excel(cons.input_file, sheet_name=cons.main_sheet)
main_df = main_df[cons.main_keep_columns]
log.info('{} columns selected from main sheet.'.format(cons.main_keep_columns))
main_df.columns = standardize_columns(main_df.columns, cons.main_column_names_key)

star_df = pd.read_excel(cons.input_file, sheet_name=cons.star_sheet)
star_df.columns = standardize_columns(star_df.columns,  cons.star_column_names_key)

df = main_df.merge(star_df,
                   how='outer',
                   on=list(set(main_df.columns) &
                           set(star_df.columns)))

assert (main_df.shape[0] == df.shape[0] and
        star_df.shape[0] == df.shape[0]),\
        print('Incorrect row counts, check merging')
df.insert(0, 'row_id', df.index+1)
df.to_csv(cons.output_file, **cons.csv_opts)

meta_df = collect_metadata(df, cons.input_file, cons.output_file)
meta_df.to_csv(cons.metadata_file, **cons.csv_opts)

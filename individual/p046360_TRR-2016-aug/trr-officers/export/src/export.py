import pandas as pd
import __main__

import setup


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': 'input/trr-officers.csv.gz',
        'input_demo_file': 'input/trr-officers_demographics.csv.gz',
        'output_file': 'output/trr-officers.csv.gz',
        'output_demo_file': 'output/trr-officers_demographics.csv.gz',
        'export_cols': ['Unit', 'Start.Date', 'End.Date'],
        'id': 'trr_officers_ID'
        }

    assert (args['input_file'].startswith('input/') and
            args['input_file'].endswith('.csv.gz')),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

df = pd.read_csv(cons.input_file)
print(df.columns)
'''
df = df[[cons.id] + cons.export_cols]
df.to_csv(cons.output_file, **cons.csv_opts)

demo_df = pd.read_csv(cons.input_demo_file)
demo_df.to_csv(cons.output_demo_file, **cons.csv_opts)
'''
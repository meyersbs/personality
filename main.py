import argparse
import os

from personality import constants

def aggregate(args):
    if os.path.exists(args.data):
        aggregate_data(data=args.data)
    else:
        pass

def clean(args):
    if os.path.exists(args.data_in) and os.path.exists(args.data_out):
        clean_data(data_in=args.data_in, data_out=args.data_out)
    else:
        pass

def predict(args):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description=''
        )
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True


    parser_aggregate = subparsers.add_parser(
            'aggregate', help="Aggregate word-level 'ENACO' scores from the "
                              "provided 'training' data."
        )
    parser_aggregate.add_argument(
            '-d', '--data', default=constants.DATASET_CLEANED_PATH,
            help='The absolute path of the file to aggregate.'
        )
    parser_aggregate.set_defaults(handler=aggregate)

    parser_clean = subparsers.add_parser(
            'clean', help="Remove irrelevant columns from the dataset.",
        )
    parser_clean.add_argument(
            '-i', '--data_in', default=constants.DATASET_ORIGINAL_PATH,
            help="The absolute path of the file to be cleaned."
        )
    parser_clean.add_argument(
            '-o', '--data_out', default=constants.DATASET_CLEANED_PATH,
            help="The absolute path to save the cleaned input to."
        )
    parser_clean.set_defaults(handler=clean)

    args = parser.parse_args()

    from personality.clean import clean_data
    from personality.aggregate import aggregate_data
    args.handler(args)

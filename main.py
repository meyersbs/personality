import argparse
import csv
import os
import _pickle

from personality import constants, helpers

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
    if args.str_in is None:
        if os.path.exists(args.file_in):
            pred.predict(os.path.abspath(args.file_in), text_type='file')
    else:
        pred.predict(args.str_in, text_type='str')

def performance(args):
    print("Starting Up...")
    performance_data(args.train_split)

def print_data(args):
    # TODO: Move this elsewhere.
    with open(constants.AGGREGATE_INFO_FILE, 'rb') as f:
        preds = _pickle.load(f)

    results = {'eRatio_y': 0, 'eRatio_n': 0, 'nRatio_y': 0, 'nRatio_n': 0,
               'aRatio_y': 0, 'aRatio_n': 0, 'cRatio_y': 0, 'cRatio_n': 0,
               'oRatio_y': 0, 'oRatio_n': 0}
    for key, pred in preds.items():
        if pred.eRatio_y > pred.eRatio_n:
            results['eRatio_y'] += 1
        else:
            results['eRatio_n'] += 1
        if pred.nRatio_y > pred.nRatio_n:
            results['nRatio_y'] += 1
        else:
            results['nRatio_n'] += 1
        if pred.aRatio_y > pred.aRatio_n:
            results['aRatio_y'] += 1
        else:
            results['aRatio_n'] += 1
        if pred.cRatio_y > pred.cRatio_n:
            results['cRatio_y'] += 1
        else:
            results['cRatio_n'] += 1
        if pred.oRatio_y > pred.oRatio_n:
            results['oRatio_y'] += 1
        else:
            results['oRatio_n'] += 1

    helpers.print_preds(results, '')
    with open('results.pkl', 'wb') as f:
        _pickle.dump(results, f)

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

    parser_performance = subparsers.add_parser(
            'performance', help="Get preformance for the 'classifier'.",
        )
    parser_performance.add_argument(
            '-t', '--train_split', default=0.75,
            help="The percentage of the data to keep as 'training' data."
        )
    parser_performance.set_defaults(handler=performance)


    parser_print = subparsers.add_parser(
            'print', help="Print the an 'ENACO' scores for the whole dataset.",
        )
    parser_print.set_defaults(handler=print_data)


    parser_predict = subparsers.add_parser(
            'predict', help="Predict an 'ENACO' score.",
        )
    group = parser_predict.add_mutually_exclusive_group(required=True)
    group.add_argument(
            '-s', '--str_in', type=str,
            help="Use to specify a str input."
        )
    group.add_argument(
            '-f', '--file_in', type=str,
            help="Use to specify a filename."
        )
    parser_predict.set_defaults(handler=predict)


    args = parser.parse_args()

    from personality.clean import clean_data
    from personality.aggregate import aggregate_data
    import personality.predict as pred
    from personality.performance import performance_data
    args.handler(args)

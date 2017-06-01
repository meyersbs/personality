from pkg_resources import resource_filename

DATASET_ORIGINAL_PATH = resource_filename(
        'personality', 'data/mypersonality_final.csv'
    )
DATASET_CLEANED_PATH = resource_filename(
        'personality', 'data/mypersonality_new.csv'
    )
AGGREGATE_INFO_FILE = resource_filename(
        'personality', 'data/aggregate_info.pkl'
    )
VERBS_PATH = resource_filename('personality', 'data/verbs.txt')

AGGREGATE_TRAINING = resource_filename(
        'personality', 'data/aggregate_train.pkl'
    )
AGGREGATE_TESTING = resource_filename(
        'personality', 'data/aggregate_test.pkl'
    )
AGGREGATE_TESTING_STATUSES = resource_filename(
        'personality', 'data/aggregate_test_statuses.pkl'
    )
TRAIN_PREDICTIONS = resource_filename(
        'personality', 'data/training_predictions.pkl'
    )
TEST_PREDICTIONS = resource_filename(
        'personality', 'data/testing_predictions.pkl'
    )

RATIO_KEYS = [
        'eRatio_n', 'eRatio_y', 'nRatio_n', 'nRatio_y', 'aRatio_n', 'aRatio_y',
        'cRatio_n', 'cRatio_y', 'oRatio_n', 'oRatio_y'
    ]
FREQ_KEYS = [
        'eFreq_n', 'eFreq_y', 'nFreq_n', 'nFreq_y', 'aFreq_n', 'aFreq_y',
        'cFreq_n', 'cFreq_y', 'oFreq_n', 'oFreq_y'
    ]

CY = "\033[1;48;5;51;38;5;232m"
MA = "\033[1;48;5;201;38;5;232m"
YE = "\033[1;48;5;220;38;5;232m"
GR = "\033[1;48;5;46;38;5;232m"
OR = "\033[1;48;5;202;38;5;232m"
RE = "\033[1;48;5;88;38;5;232m"
XX = "\x1b[0m"


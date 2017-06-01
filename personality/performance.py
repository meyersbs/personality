from . import predict, helpers
from .constants import CY, MA, YE, GR, OR, XX

def avg_tot(metric, support):
    tot, avg = (0.0,)*2
    for key, val in metric.items():
        avg += float(val*support[key])
        tot += support[key]

    return float( avg / tot ), tot

def prfs(predictions):
    results = {
            'e': {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0},
            'n': {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0},
            'a': {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0},
            'c': {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0},
            'o': {'fp': 0, 'fn': 0, 'tp': 0, 'tn': 0}
        }
    print("Evaluating Predictions...")
    for key, val in predictions.items():
        print("Prediction: " + str(key))
        sentence = val[0]
        train = val[1]
        test = val[2]
        for label in ['e', 'n', 'a', 'c', 'o']:
            if train[label] == 'y':
                if test[label] == 'y':
                    results[label]['tp'] += 1
                else:
                    results[label]['fp'] += 1
            elif train[label] == 'n':
                if test[label] == 'y':
                    results[label]['fn'] += 1
                else:
                    results[label]['tn'] += 1
            else:
                helpers.print_warning(
                        label, sentence, test[label], train[label]
                    )

    p, r, f, s = ({},)*4
    for key, val in results.items():
        p[key] = float( val['tp'] / (val['tp'] + val['fp']) )
        r[key] = float( val['tp'] / (val['tp'] + val['fn']) )
        f[key] = float( (2*val['tp'])/((2*val['tp']) + val['fp'] + val['fn']) )
        s[key] = val['tp'] + val['tn'] + val['fp'] + val['fn']

    return p, r, f, s

def performance_data(train_size):
    predictions = predict.predict_split(train_size)
    p, r, f, s = prfs(predictions)
    print_preformance(p, r, f, s)

def print_preformance(p, r, f, s):
    p_avg, s_tot = avg_tot(p, s)
    r_avg, _ = avg_tot(r, s)
    f_avg, _ = avg_tot(f, s)

    out  = "\n==== RESULTS: ==============================================="
    out += "\n                   | precision | recall | f-score | support |"
    out += "\n-------------------------------------------------------------"
    out += "\n{:s}{: >16s}{:s} | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(CY, "EXTRAVERSION:", XX, p['e'], r['e'], f['e'], s['e'])
    out += "\n{:s}{: >16s}{:s} | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(MA, "NEUROTICISM:", XX, p['n'], r['n'], f['n'], s['n'])
    out += "\n{:s}{: >16s}{:s} | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(YE, "AGREEABLENESS:", XX, p['a'], r['a'], f['a'], s['a'])
    out += "\n{:s}{: >16s}{:s} | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(GR, "CONSCIENTIOUSNESS:", XX, p['c'], r['c'], f['c'], s['c'])
    out += "\n{:s}{: >16s}{:s} | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(OR, "OPENNESS:", XX, p['o'], r['o'], f['o'], s['o'])
    out += "\n-------------------------------------------------------------"
    out += "\n      AVG / TOT: | {: >9.2f} | {: >6.2f} | {: >7.2f} | {: >7d} |" \
           .format(p_avg, r_avg, f_avg, int(s_tot))
    out += "\n=============================================================\n"

    print(out)

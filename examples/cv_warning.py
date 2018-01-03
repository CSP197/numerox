#!/usr/bin/env python

import pandas as pd
import numerox as nx


def cv_warning(data, nsamples=100):

    model = nx.logistic()
    results_cve = pd.DataFrame()
    results_cv = pd.DataFrame()

    for i in range(nsamples):

        # cv across eras
        cve = nx.CVSplitter(data, seed=i)
        prediction = nx.run(model, cve, verbosity=0)
        df, info = prediction.performance_df(data)
        results_cve = results_cve.append(df, ignore_index=True)

        # cv ignoring eras but y balanced
        cv = nx.IgnoreEraCVSplitter(data, seed=i)
        prediction = nx.run(model, cv, verbosity=0)
        df, info = prediction.performance_df(data)
        results_cv = results_cv.append(df, ignore_index=True)

        # display results
        rcve = results_cve.mean(axis=0)
        rcv = results_cv.mean(axis=0)
        rcve.name = 'cve'
        rcv.name = 'cv'
        r = pd.concat([rcve, rcv], axis=1)
        print("\n{} runs".format(i+1))
        print(r)


if __name__ == '__main__':
    data = nx.numerai.download_data_object(verbose=True)
    data = data['train']
    cv_warning(data)

# datautil.py
import pandas as pd
from datetime import datetime, timedelta
import warnings


warnings.simplefilter(action='ignore')

PMTs = ['conan', 'vcpkg', 'meson', 'xmake', 'pc-config', 'gitsubmodule', 'deb']

def get_mig(language):
    return pd.read_csv(f'dataset/{language}_migration.csv')
    # return pd.read_excel('dataset/migration_c_kb.xlsx')

def get_by_src(df, src):
    return df[df['src']==src]

def get_mig_stats(language):
    mig_df = get_mig(language)
    mig_rule = mig_df.value_counts(subset=['rule'])
    mig_proj = mig_df.value_counts(subset=['url'])
    mig_commit = mig_df.value_counts(subset=['commit'])
    return {
        'mig_commit': len(mig_commit),
        'mig': len(mig_df),
        'mig_proj': len(mig_proj),
        'mig_rule': len(mig_rule),
    }


def get_mig_stats_by_src(language, src):
    mig_df = get_mig(language)
    mig_df = mig_df[mig_df['src']==src]
    mig_rule = mig_df.value_counts(subset=['rule'])
    mig_proj = mig_df.value_counts(subset=['url'])
    mig_commit = mig_df.value_counts(subset=['commit'])
    return {
        'src': src,
        'mig_commit': len(mig_commit),
        'mig': len(mig_df),
        'mig_proj': len(mig_proj),
        'mig_rule': len(mig_rule),
    }



def get_year_mig(df, year):
    df.loc[:, 'year'] = df['time_stamp'].copy().apply(lambda x: datetime.utcfromtimestamp(int(x[:-5])).year)
    return df[df['year']==year]

def get_year_mig_trend(df):
    trend = pd.DataFrame()
    for year in range(2000, 2023):
        num = len(get_year_mig(df, year))
        if num > 0:
            trend = pd.concat([trend, pd.DataFrame([{'year': year, 'num': len(get_year_mig(df, year))}])], ignore_index=True)
    return trend

def get_trend_by_src(df, src):
    mig_src = get_by_src(df, src)
    trend = get_year_mig_trend(mig_src)
    return trend
    
import re

def simplify(lib):
    lib = re.sub('(\[.*\])|(<.*>)|<|>|=|\(|\)','',lib).strip().lower()
    if lib and lib[-1] in ['-']:
        return lib[:-1]
    else:
        return lib

def preprocess(df):
    df = get_mig("c")
    df['add_lib'] = df['add_lib'].apply(simplify)
    df['rem_lib'] = df['rem_lib'].apply(simplify)
    df = df.fillna('')
    df.dropna(axis='index', how='any', subset=['add_lib', 'rem_lib'])
    return df

import re
def simplify_lib(lib):
    lib = re.sub('(\[.*\])|(<.*>)|<|>|=|\(|\)','',lib).strip().lower()
    if lib and lib[-1] in ['-']:
        return lib[:-1]
    else:
        return lib
    

def get_sankey(df, domain=''):
    df['add_lib'] = df['add_lib'].apply(simplify_lib)
    df['rem_lib'] = df['rem_lib'].apply(simplify_lib)
    df['pattern'] = df['rem_lib'] + ' ' + df['add_lib']
    if domain:
        pattern_with_value = df[df['domain']==domain].pattern.value_counts()[:9].to_dict()
    else:
        pattern_with_value = df.cross_pattern.value_counts().to_dict()
    labels = list(set([t for x in pattern_with_value.keys() for t in x.split(" ",1) ]))
    label_index = {label: i for i, label in enumerate(labels)}
    source = []
    target = []
    num = []
    print('-'* 10)
    print(domain)
    for pattern, value in pattern_with_value.items():
        source.append(label_index[pattern.split(" ")[0]])
        target.append(label_index[pattern.split(" ")[1]])
        num.append(value)
        print(labels[label_index[pattern.split(" ")[0]]], f'[{value}]',labels[label_index[pattern.split(" ")[1]]])

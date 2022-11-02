import pandas as pd

def fix(df_):
    df = df_.copy()
    for (weekday, group, subject, start), sub_df in df.groupby(['weekday', 'group', 'subject', 'start']):
        if len(sub_df) > 1:
            teachers = sub_df['teacher'].values
            places = sub_df['place'].values
            new_df = sub_df.iloc[0].copy()
            new_df['teacher'] = ', '.join(teachers)
            new_df['place'] = ', '.join(places)

            indexes = sub_df.index
            df.drop(indexes, axis=0, inplace=True)
            df.loc[len(df)] = new_df
    return df

import pandas as pd

def _multiple_lessons(df):
    for (weekday, group, subject, start), sub_df in df.groupby(['weekday', 'group', 'subject', 'start']):
        if len(sub_df) > 1:
            teachers = sub_df['teacher'].values
            places = sub_df['place'].values
            new_df = sub_df.iloc[0].copy()
            new_df['teacher'] = ', '.join(teachers)
            new_df['place'] = ', '.join(places)

            indexes = sub_df.index
            df.drop(indexes, axis=0, inplace=True)
            df.loc[len(df)+1] = new_df
            
    indexes_for_new_df = pd.Series(list(range(len(df))))
    df.set_index(indexes_for_new_df, inplace=True)
    
    return df

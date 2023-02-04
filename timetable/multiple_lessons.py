import logging

import pandas as pd

_logger = logging.getLogger(__name__)


def multiple_lessons(lessons):
    """
    Соединяет пары, у которых одинаковые ['weekday', 'group', 'subject', 'start'], в одну строчку.
    Очень важно, чтобы значения в ['teacher', 'place'] были hashable.
    """
    _logger.info("Начинаю соединять одинаковые пары...")

    # Может быть так, что одну пару разбили на две пары с разной четностью.
    for _, sub_df in lessons.groupby(['weekday', 'num', 'group', 'subject', 'teacher', 'place']):
        if len(sub_df) > 1:
            new_df = sub_df.head(1).copy()
            new_df['odd'] = any(sub_df["odd"].values)
            new_df['even'] = any(sub_df["even"].values)

            lessons.drop(sub_df.index, axis=0, inplace=True)
            lessons = pd.concat([lessons, new_df])

    for _, sub_df in lessons.groupby(["odd", "even", 'weekday', 'num', 'group', 'subject']):
        if len(sub_df) > 1:
            index = sub_df.index
            teachers = sub_df['teacher'].values
            places = sub_df['place'].values

            new_df = sub_df.head(1).copy()
            new_df.at[index[0], 'teacher'] = list(teachers)
            new_df.at[index[0], 'place'] = list(places)

            lessons.drop(index, axis=0, inplace=True)
            lessons = pd.concat([lessons, new_df])

    lessons = lessons.reset_index(drop=True)

    return lessons

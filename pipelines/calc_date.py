import pandas as pd
from datetime import timedelta, datetime


def calc_date(lessons):
    semester_begin = "09/01/2022"
    semester_end = "12/31/2022"

    begin = datetime.strptime(semester_begin, "%m/%d/%Y")
    end = datetime.strptime(semester_end, "%m/%d/%Y")

    day_number = (end-begin).days
    lessons_new = []

    for i in range(day_number):
        num = ((i + begin.weekday() + 1)//7 + 1) % 2
        for j, row in lessons.iterrows():
            if (num == 1 and row['odd']) or (num == 0 and row['even']):
                row_new = row
                day = begin + timedelta(days=i)
                if row['weekday'] == day.weekday():

                    hours_start, minutes_start = row['start'].split(':')
                    hours_end, minutes_end = row['end'].split(':')

                    date_start = day + timedelta(hours=int(hours_start), minutes=int(minutes_start))
                    date_end = day + timedelta(hours=int(hours_end), minutes=int(minutes_end))

                    seconds_start = date_start.timestamp()
                    seconds_end = date_end.timestamp()

                    row_new['start'] = seconds_start
                    row_new['end'] = seconds_end

                    lessons_new.append(row_new)

    lessons_new = pd.DataFrame(lessons_new)
    lessons_new.pop('odd')
    lessons_new.pop('even')
    lessons_new.pop('weekday')
    lessons_new.pop('num')

    return lessons_new


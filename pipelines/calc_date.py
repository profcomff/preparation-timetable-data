import pandas as pd
import datetime
from datetime import timedelta


def calc_date(lessons):
    #print(lessons)
    semester_begin = "09/01/2022"
    semester_end = "12/31/2022"

    begin = datetime.datetime.strptime(semester_begin, "%m/%d/%Y")
    end = datetime.datetime.strptime(semester_end, "%m/%d/%Y")

    a = str(end - begin)
    day_number = int(a.split()[0])

    # day_number += begin.weekday()
    # day_number += 7 - end.weekday()

    lessons_new = []

    for i in range(day_number):
        num = int((i + begin.weekday() + 1)//7 + 1) % 2
        for j, row in lessons.iterrows():
            if (num == 1 and row['odd']) or (num == 0 and row['even']):
                row_new = row
                day = begin + timedelta(days=i)
                if row['weekday'] - 1 == day.weekday():
                    date = day.strftime('%m/%d/%Y') + ' ' + row['start']
                    date1 = day.strftime('%m/%d/%Y') + ' ' + row['end']
                    date_ = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M')
                    date1_ = datetime.datetime.strptime(date1, '%m/%d/%Y %H:%M')
                    seconds = int(date_.timestamp())
                    seconds1 = int(date1_.timestamp())
                    row_new['start'] = str(seconds)
                    row_new['end'] = str(seconds1)
                    lessons_new.append(row_new)

    lessons_new = pd.DataFrame(lessons_new)
    lessons_new.pop('odd')
    lessons_new.pop('even')
    lessons_new.pop('weekday')
    lessons_new.pop('num')

    lessons_new.to_excel("foo.xlsx", sheet_name="Sheet1")
    return lessons_new


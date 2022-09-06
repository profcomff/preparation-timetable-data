import pandas as pd


def fix_eng(lessons, groups):
    new_lessons = []

    n_lessons = []
    for i, row in lessons.iterrows():
        row['place'] = [int(row['place'])] if not pd.isna(row["place"]) else []
        n_lessons.append(row)

    lessons = pd.DataFrame(n_lessons)

    for i, group in groups.iterrows():
        for j in range(7):
            table = []

            for k, row in lessons.iterrows():
                if row['group'] == group[0] and row['weekday'] == j:
                    table.append(row)
            table = pd.DataFrame(table)
            # table1 = table

            row1 = pd.DataFrame()
            ar = []
            boo = False

            # k = 0
            # for row in table:
            #     if "странный язык" in row['subject']:
            #         row1 = row
            #         boo = True
            #         ar.append(k)
            #         break
            #     k += 1
            #
            # k = 0
            # for row in table:
            #     if "странный язык" in row['subject'] and row['teacher'][0] != row1['teacher'][0]:
            #         ar.append(k)
            #         row1['teacher'].append(row['teacher'][0])
            #         row1['place'].append(row['place'][0])
            #     k += 1
            #
            # new_lessons.append(row1)
            # print(row1)
            # for l in range(len(table)):
            #     if not l in ar:
            #         new_lessons.append(table[l])
            #         # print(table[l])

            for k, row in table.iterrows():
                if "странный язык" in row['subject']:
                    row1 = row
                    boo = True
                    ar.append(k)
                    break

            for k, row in table.iterrows():
                if "странный язык" in row['subject'] and row['teacher'][0] != row1['teacher'][0]:
                    ar.append(k)
                    row1['teacher'].append(row['teacher'][0])
                    row1['place'].append(row['place'][0])

            table.drop(labels = ar, axis = 0, inplace=True)
            if boo:
                new_lessons.append(row1)

            for k, row in table.iterrows():
                new_lessons.append(row)
                #print(row)

            # ar = []
            # b = False
            # for k, row in table.iterrows():
            #     for l, row1 in table.iterrows():
            #         if not k in ar and not l in ar:
            #             if "странный язык" in row['subject'] and l != k and row['place'] != [] and row1['place'] != [] and row['teacher'] != [] and row1['teacher'] != []:
            #                 row['teacher'].append(row1['teacher'][0])
            #                 row['place'].append(row1['place'][0])
            #                 print(row1['teacher'][0])
            #
            #                 b = True
            #                 ar.append(l)
            #
            #     if b:
            #         new_lessons.append(row)
            #         #print(row)
            #         print("______________________________")
            #         b = False

            # table.drop(labels = ar, axis=0)
            # for k, row in table.iterrows():
            #     new_lessons.append(row)
            #     print(row)

    new_lessons = pd.DataFrame(new_lessons)
    return new_lessons

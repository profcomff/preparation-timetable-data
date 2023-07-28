import pandas as pd


def separate(lessons):
    res = []
    for weekday in range(7):
        for num in range(6):
            part = []
            for i, row in lessons.iterrows():
                if row["weekday"] == weekday and row["num"] == num:
                    part.append(row)
            if len(part) > 0:
                res.append(part)
    return res


def part_to_array(lessons):
    res = []
    length = len(lessons)
    while length > 0:
        buf = lessons[0]
        modif = buf
        modif["group"] = [buf["group"]]
        lessons.pop(0)
        length -= 1
        i = 0
        while i < length:
            a = buf.drop(labels=["group"])
            b = lessons[i].drop(labels=["group"])
            boo = True
            for l in range(len(a)):
                if a[l] != b[l]:
                    boo = False
                    break
            if boo:
                modif["group"].append(lessons[i]["group"])
                lessons.pop(i)
                length -= 1
                i -= 1
            i += 1
        res.append(modif)
    return res


def all_to_array(lessons):
    parts = separate(lessons)
    res = []
    for part in parts:
        res1 = part_to_array(part)
        for item in res1:
            res.append(item)
    res = pd.DataFrame(res)
    res.reset_index(drop=True, inplace=True)
    return res

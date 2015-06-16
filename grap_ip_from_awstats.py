#!/usr/bin/env python

from pymongo import MongoClient

def getfilename(year, month, prefix):
    str_month = (''.join(['0', str(month)]) if (month < 10) else str(month))
    suffix = ".mirrors.cqu.edu.cn.txt"
    return prefix + str_month + str(year) + suffix


def savetofile(ips, filename):
    with open(filename, "w") as outfile:
        comment = "Host Pages Hits Bandwidth Last visit date [Start date of last visit] [Last page of last visit]"
        outfile.write(comment + '\n')
        for line in ips:
            outfile.write(' '.join(line))
            outfile.write('\n')


def savetodb(ips, collection):
    db = MongoClient("localhost", 27017)["mirrors"]
    coll = db[collection]
    fields = ["host", "pages", "hits", "bandwidth", "last_visit"]
    for line in ips:
        if len(line) < 5:
            line.append('')
        obj = {
            "host": line[0],
            "pages": int(line[1]),
            "hits": int(line[2]),
            "bandwidth": int(line[3]),
            "last_visit": line[4]
        }
        coll.insert_one(obj)


def grap(filename):
    ips = []
    with open(filename, 'r') as infile:
        flag = False
        count = None
        for line in infile:
            words = line.split()
            if not words: continue
            if words[0] == "END_VISITOR": flag = False
            if flag: ips.append(words)
            if words[0] == "BEGIN_VISITOR":
                flag = True
                count = int(words[1])
        if len(ips) != count:
            print len(ips), count
            raise Exception("CountNotMatch")

    if not ips:
        raise Exception("IPListIsEmpty")

    savetodb(ips, ''.join(["ip", filename.lstrip("awstats").rstrip(".mirrors.cqu.edu.cn.txt")]))
    # Sort by bandwidth
    # ips.sort(key=(lambda x: int(x[3])), reverse=True)
    # savetofile(ips, ''.join(["ip", filename.lstrip("awstats")]))


def indexbyip(ipinfos, targetip):
    if not ipinfos: return -1
    for (index, ipinfo) in enumerate(ipinfos):
        if ipinfo[0] == targetip: return index
    return -1


def addipinfo(ipinfoa, ipinfob):
    return [ipinfoa[0]] + map(lambda x, y: str(int(x) + int(y)), ipinfoa[1:4], ipinfob[1:4])


def merge(year, months):
    db = MongoClient("localhost", 27017)["mirrors"]
    coll = db[''.join(["ip", '_'.join([str(months[0]), str(months[-1])])])]
    for m in months:
        str_m = (''.join(['0', str(m)]) if m < 10 else str(m))
        pcoll = db[''.join(["ip", str_m, str(year)])]
        for record in pcoll.find():
            target = coll.find_one({"host": record["host"]})
            if target is None:
                coll.insert_one(record)
                continue

            for key in ["pages", "hits", "bandwidth"]:
                target[key] += record[key]
            target["last_visit"] = max(target["last_visit"], record["last_visit"])
            pcoll.save(target)


def main():
    months = [1, 2, 3, 4, 5]
    #for m in months:
    #    grap(getfilename(2015, m, "awstats"))
    merge(2015, [1, 2])


def test():
    import StringIO
    s = '''123 231213 233
    asdfasd asdf  sdf

    a
    '''
    buf = StringIO.StringIO(s)
    for line in buf:
        ws = line.split()
        print ws


if __name__ == "__main__":
    main()

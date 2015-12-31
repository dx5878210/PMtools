from PMtools.models import mzitemscode
import re


def load_model():
    items = mzitemscode.query.filter().all()
    dis = {}
    for i in items:
        name, uid = i.get_name_uid()
        dis[str(name)] = int(uid)
    return dis


def textprocess(totle):
    totle = totle.strip()
    b = totle.replace(',', '').\
        replace('，', '').\
        replace('•', '·').\
        replace('：', ':').\
        replace("X", "x")

    temp_list = b.split('\n')
    temp_list =[x for x in temp_list if x!='']
    range_list = []
    item_list = []
    items_dict = load_model()

    for e in temp_list:
        #print (e)
        range1 = re.findall(r'\d+', e.split(':')[0])
        range_list.append(range1[0])
        itemline = e.split(':')[1]
        items = itemline.split('、')
        itemidstr = ''
        for item in items:
            if len(item.split('x')) == 2:
                itemid = search(item.split('x')[0], items_dict)
                itemidstr = itemidstr + \
                    str(itemid) + ',' + str(item.split('x')[1]) + ';'
            elif len(item.split('x')) == 1 and len(re.findall(r'\D+', item)) == 2:
                itemname = re.findall(r'\D+', item)
                itemid = search(itemname[0], items_dict)
                if itemname[1] == '萬':
                    num = int(re.findall(r'\d+', item)[0]) * 10000
                    itemidstr = itemidstr + str(itemid) + ',' + str(num) + ';'
            else:
                for k in re.findall(r'\D+', item):
                    itemidstr += "??????，"
                for k in re.findall(r'\d+', item):
                    itemidstr += "??????，"
        item_list.append(itemidstr)
    return range_list, item_list


def search(itemtext, dict):

    for i in dict:
        if i == itemtext:
            return dict[i]
    templist = {}
    print(itemtext)
    for k in dict:
        if len(k) == len(itemtext):
            for j in itemtext[::-1]:
                if k[itemtext.index(j)] == j:
                    if k in templist:
                        templist[k] += 1
                    else:
                        templist[k] = 1
    result = sorted(templist.items(), key=lambda d: d[1], reverse=True)
    if len(result) >= 2:
        if result[0][1] == result[1][1]:
            return '??????'
        else:
            return dict[result[0][0]]
    elif len(result) == 1:
        return dict[result[0][0]]
    elif len(result) == 0:
        return '?????'


def codetable(strp):
    rlist, itemlist = textprocess(strp)
    rstr = ''
    for i in itemlist:
        rstr = rstr + rlist[itemlist.index(i)] + '\t' + i + '\n'
    return rstr

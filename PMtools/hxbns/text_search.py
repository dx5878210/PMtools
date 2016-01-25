from PMtools.models import hxbnsitemscode
import re


def load_model():
    items = hxbnsitemscode.query.filter().all()
    dis = {}
    for i in items:
        name, names,itemid = i.get_name_names_itemid()
        dis[str(name)] = names+':'+str(itemid)
    return dis


def textprocess(totle):
    totle = totle.strip()
    b = totle.replace('X', 'x').\
        replace('*', 'x').\
        replace('、', '\n').\
        replace(',', '\n').\
        replace('，', '\n')

    temp_list = b.split('\n')
    temp_list = [x for x in temp_list if x != '']
    items_dict = load_model()
    items_str = ''
    for e in temp_list:
        item_name_id = search(e.split('x')[0], items_dict)
        item_count = e.split('x')[1]
        itemstr = item_name_id + ':' + item_count + ':' + '1'
        items_str = items_str + itemstr+','
    return items_str[:-1]


def search(itemtext, dict):
    if itemtext in dict.keys():
        return dict[itemtext]
    templist = {}
    #print(itemtext)
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
    items_str = textprocess(strp)
    return items_str


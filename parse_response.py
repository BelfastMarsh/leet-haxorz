def parse_reponse(dimensions, values):
    dimension_compiled = {}
    for d in dimensions.keys():
        # dimension_compiled.append([])
        # print(dimensions[d]['category']['label'])
        tmparray = []
        for lst in dimensions[d]['category']['label'].keys():
            tmparray.append(dimensions[d]['category']['label'][lst])
        dimension_compiled[d] = tmparray

    n = 0
    lst2 = [[""]]
    while n < len(dimension_compiled):
        lst2.append([])
        for d in dimension_compiled[list(dimension_compiled.keys())[n]]:
            for l in lst2[n]:
                lst2[n + 1].append(l + "_" + d)
        n = n + 1

    m = 0
    data_dict = []
    for l in lst2[len(lst2) - 1]:
        tmpd = {}
        f = l.split("_")
        r = 1
        for lbl in list(dimension_compiled.keys()):
            tmpd[lbl] = f[r]
            r = r + 1
        tmpd["value"] = values[m]
        data_dict.append(tmpd)
        m = m + 1
    return data_dict

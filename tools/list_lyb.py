def extend_list(list_to_extend, list_to_add):
    # test if list exixt
    if list_to_extend:
        list_to_extend.extend(list_to_add)
    else:
        list_to_extend = list_to_add


def append_list(list_to_extend, list_to_add):
    # test if list exixt
    if list_to_extend:
        list_to_extend.append(list_to_add)
    else:
        list_to_extend = list_to_add

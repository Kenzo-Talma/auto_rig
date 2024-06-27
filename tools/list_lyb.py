def extend_list(list_to_extend, list_to_add):
    # test if list exixt
    if list_to_extend:
        list_to_return = list_to_extend+list_to_add
        return list_to_return
    else:
        return list_to_add


def append_list(list_to_append, list_to_add):
    # test if list exixt
    if list_to_append:
        list_to_return = list_to_append+[list_to_add]
        return list_to_return
    else:
        return [list_to_add]

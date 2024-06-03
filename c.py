arr = [['admin','admin','admin','admin'],['user','123','qwe','123'],['admin','admin','admin','admin'],['admn','hehe','admin','123']]

def remove_duplicates_nested_array(arr):
    seen = set()
    result = []
    for sub_arr in arr:
        sub_arr_tuple = tuple(sub_arr)
        if sub_arr_tuple not in seen:
            seen.add(sub_arr_tuple)
            result.append(sub_arr)
    return result

print(arr)
cleaned_arr = remove_duplicates_nested_array(arr)
print(cleaned_arr)

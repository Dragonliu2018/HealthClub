import pinyin
def get_str_all_aplha(str):
    return pinyin.get_initial(str, delimiter="").upper()

def get_str_first_aplha(str):
    str = get_str_all_aplha(str)
    str = str[0:1]
    return str.upper()
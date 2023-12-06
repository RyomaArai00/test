from flaskr.src.main_serch_by_keyword import SerchByKeyword

def run_sbk(key_word, user_id):
    
    output_list_index = 1
    sbk = SerchByKeyword()

    remove_word = ""
    limit_page = 1

    rs = sbk.execute(key_word, output_list_index, remove_word, limit_page, user_id)
    return rs

if __name__ == '__main__':
    print(run_sbk("化粧品"))
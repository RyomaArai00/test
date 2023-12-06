from flaskr.src.custom_search_api import GoogleCustomSearch

class SerchByKeyword():
    def __init__(self):
        pass

    def execute(self, key_word, index, remove_word, result_page, user_id):
        # キーワードリストを元にGoogle検索を実行する
        gcs = GoogleCustomSearch()
        search_word = 'intitle:"会社概要" {}'.format(key_word)

        # 検索実行
        data_list = gcs.search(search_word, result_page)

        search_result_list = []
        rank = 1

        for data in data_list:
            if 'items' not in data:
                continue

            for info in data['items']:
                search_result_list.append([
                    user_id,
                    index,
                    key_word,
                    rank,
                    info['title'],
                    info['link']
                ])
                rank += 1
                index += 1

        # 検索結果を保存する
        return search_result_list
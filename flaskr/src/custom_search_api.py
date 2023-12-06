from time import sleep
from googleapiclient.discovery import build

class GoogleCustomSearch:

    """
    Google Custom Search API

    # リファレンス
    https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list#response-body

    APIの仕様上、1リクエストあたりの検索結果は最大10個まで
    ページランクは最大100位まで

    検索結果は最大10ページまで
    """

    __google_api_key          = "AIzaSyDdCy2igfeMtVwWYv0maUIWtjn6hsBjwnI"
    __custom_search_engine_id = "09599596728a928bb"

    def __init__(self):
        # APIに接続
        self.__service = build("customsearch", "v1", developerKey=self.__google_api_key)

    @property
    def page_limit(self):
        return self.__page_limit

    @page_limit.setter
    def page_limit(self, page_limit):
        max_page = 10
        if type(page_limit) is not int or page_limit < 1 or max_page < page_limit:
            raise ValueError("page_limitは、1-10の間で指定してください。")
        self.__page_limit = page_limit

    def search(self, keyword, page_limit=1):

        # 最大検索ページ数
        self.page_limit = page_limit

        response    = []
        start_index = 1

        for n_page in range(0, self.page_limit):

            # ログ出力
            # print("検索実行 キーワード:{} 検索回数:{}".format(keyword, n_page+1) )

            try:
                # APIは1分間に最大100回までの呼び出し制限のため待機時間を設ける
                sleep(0.7)

                # 検索実行
                # 検索結果ページの件数が10未満であってもエラーは発生しないのでnumは10で固定する
                rs = self.__service.cse().list(
                    q=keyword,
                    cx=self.__custom_search_engine_id,
                    lr='lang_ja',
                    num=10,
                    start=start_index
                ).execute()
                
                response.append(rs)

                # 検索結果の次ページが存在するかチェック
                if 'nextPage' not in rs['queries']:
                    break

                # 検索結果の次ページの開始Indexを取得する
                start_index = rs['queries']['nextPage'][0]['startIndex']

            except Exception as e:
                print(e)
                break

        return response
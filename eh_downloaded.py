from APIList import GetSearchResult, GetPageContent
from Config import config
from package import make_imagepack
import re


def download_images_from_search(query):
    def sanitize_filename(filename):
        # 只保留字母、数字、汉字、空格和常用符号，替换掉非法字符
        return re.sub(r'[<>:"/\\|?*]', "_", filename)
    name_and_url = GetSearchResult(query)
    
    # 按标题关键词匹配度排序
    sorted_results = sorted(
        name_and_url.items(),
        key=lambda x: sum(word in x[0].lower() for word in query.lower().split()),
        reverse=True
    )
    
    # 取匹配度最高的结果
    if sorted_results:
        clear_name, url = sorted_results[0]
    else:
        print("No results found for query:", query)
        return None

    clear_name, url = list(name_and_url.items())[0]
    name = sanitize_filename(clear_name)

    # 保存详情页HTML
    GetPageContent(url, "resp.txt")

    # 从详情页html抓取图片文件并打包为zip
    make_imagepack(name, "resp.txt")

    return name  # 返回 name 的值

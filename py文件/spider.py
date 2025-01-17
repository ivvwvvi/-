import requests
import csv

def get_content(maxid,url,headers):
    params={
        'is_reload': '1',
        'id': '5123449591171734',
        'is_show_bulletin' : '2',
        'is_mix': '0',
        'max_id': maxid, #作为形参传入，一多页采集
        'count': '20',
        'uid': '3266943013',
        'fetch_level': '0',
        'locale':'zh-CN',
    }   #预览中找到

    resp=requests.get(url=url,headers=headers,params=params)
    json_data=resp.json()
    data_list=json_data['data']
    all_comments = []  # 用于存储所有评论和子评论

    # 遍历每条评论
    for index in data_list:
        # 主评论
        main_comment = {
            '地区': index.get('source', '未知'),
            '内容': index.get('text_raw', '无内容'),
        }
        all_comments.append(main_comment)

        # 遍历子评论
        if 'comments' in index:
            for subindex in index['comments']:
                sub_comment = {
                    '地区': subindex.get('source', '未知'),
                    '内容': subindex.get('text_raw', '无内容'),
                }
                all_comments.append(sub_comment)
#写入文件内
    with open('data.csv', mode='a', encoding='utf-8-sig', newline='') as file:  #utf-8-sig处理excel乱码
        writer = csv.DictWriter(file, fieldnames=['地区', '内容'])
        writer.writeheader()
        for comment in all_comments:
            writer.writerow(comment)
    max_id = json_data.get('max_id','')
    """
    采集多页，分析请求参数变化规律(负载）：
    max_id:
        第一页：0/无内容
        第n页：无规律：0
        尝试：第n+1页max_id来自第n页返回参数(预览)
    count:
        第一页：10
        第n页：20
        尝试：把第一页统一为20，看是否还能得到数据；不能则保留
    """
    return max_id
def main():
    #network中找到
    headers = {
        'cookie': 'SCF=AqqnlHDc8WwYwL9A-crQNC4x19BZxqqh9Fj85pUqqbBIMMLat7W0MVklMkdfh83NIOp-YbpoA62XXtKA1x49QBw.; SUB=_2A25KjJYRDeRhGeBJ61ES8ynEyDmIHXVp45fZrDV8PUNbmtANLXKnkW9NRnYo13dZMZRimjyJK98ZYocXf_1c6mSU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFc2HMMBIPLvjLx39Ze-VKp5NHD95QcS050e0eN1hefWs4DqcjCi--NiKLFiKyWqc_k9g80wP9o; ALF=02_1739617089; _s_tentry=passport.weibo.com; Apache=6773499318546.541.1737025099084; SINAGLOBAL=6773499318546.541.1737025099084; ULV=1737025099088:1:1:1:6773499318546.541.1737025099084:; WBPSESS=jMsWWVilG5uqiWuLVl4HZAety0kw6oqKplfQiUIsEykeHs60orBgbOHNnyFwt54ybXcPtjjIHDRE30cqtJ-vQVwD49XE-X9cCcDnfzHo1qAS8Xxk327HRaj75sXMZrF3NNTYgdjhbdIjoo3GUAzRfg==',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'}
    url = 'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5123449591171734&is_show_bulletin=2&is_mix=0&count=10&uid=3266943013&fetch_level=0&locale=zh-CN'

    max_id=''
    for page in range(1,21):    #采集多页
        print(f'正在采集{page}页内容')
        max_id=get_content(max_id,url,headers)

if __name__=="__main__":
    main()
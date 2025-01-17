import pandas as pd
def analy(df_comm):

    df_comm['地区']=df_comm['地区'].str.replace('来自','',regex=False)
    df_comm=df_comm[df_comm['地区']!='地区']   #保留df中除表头外，所有第一列名不是“地区”的行
    df_comm.reset_index(drop=True,inplace=True) #重置索引
    df_comm=df_comm.drop_duplicates(subset=['内容'])
    df_comm.to_csv('standard_location_comment.csv',index=None,encoding='utf-8-sig')

    #评论ip地统计
    location=df_comm['地区'].value_counts().reset_index()
    location.columns=['地区','次数']
    #为了方便画地图，修改名称
    for index in range(len(location)):
        if index == 2 or index == 3 or index == 15:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '市'
        elif index == 14:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '壮族自治区'
        elif index == 23:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '自治区'
        elif index == 24:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '维吾尔自治区'
        elif index == 29:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '回族自治区'
        elif index == 34:
            location.loc[index, '地区'] = '香港特别行政区'
        else:
            location.loc[index, '地区'] = location.loc[index, '地区'] + '省'
    location.to_csv('standard_location_counts.csv', index=None, encoding='utf-8-sig')

    #评论
    comment_list = pd.DataFrame(df_comm['内容'])
    comment_list.to_csv('standard_comment.csv', index=None, encoding='utf-8-sig')


def main():
    df=pd.read_csv('data.csv')
    analy(df)

if __name__=="__main__":
    main()
import pandas as pd
from pyecharts.charts import Map, Bar, Pie
from pyecharts import options as opts
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt



def map(df_location):

    map_chart = Map()
    map_chart.add(
        "评论数量",
        [(loc, count) for loc, count in zip(df_location['地区'], df_location['次数'])],
        "china"
    )

    # 设置全局配置
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="博文IP地址分布图"),
        visualmap_opts=opts.VisualMapOpts(
            min_=df_location['次数'].min(),  # 设置最小值为数据的最小次数
            max_=df_location['次数'].max(),  # 设置最大值为数据的最大次数
            is_piecewise=True,  # 允许分段显示
            pieces=[
                {"min": df_location['次数'].min(), "max": df_location['次数'].min() + 10, "color": "#f2f4f6"},
                {"min": df_location['次数'].min() + 10, "max": df_location['次数'].min() + 20, "color": "#c9d6e3"},
                {"min": df_location['次数'].min() + 20, "max": df_location['次数'].min() + 30, "color": "#99b3c4"},
                {"min": df_location['次数'].min() + 30, "max": df_location['次数'].min() + 40, "color": "#668ba5"},
                {"min": df_location['次数'].min() + 40, "max": df_location['次数'].max(), "color": "#336b7a"}
            ]
        )
    )
    map_chart.render("china_comment_distribution.html")
    return map

def create_wordcloud(df1):
    text=''.join(df1['内容'].dropna())
    words=jieba.cut(text)
    print(words)
    word_list=''.join(words)

    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',
        width=500,
        height=500,
        background_color='white',
        max_words=200,
        ).generate(word_list)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")  # 不显示坐标轴
    plt.show()

def bar_chart(df):
    bar=(
        Bar()
        .add_xaxis(df['地区'].tolist())
        .add_yaxis("评论数", df['次数'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="地区评论数柱状图"),
            datazoom_opts=[
                opts.DataZoomOpts(type_="slider"),
                opts.DataZoomOpts(type_="inside"),
            ]
        )
        .render("bar.html"
        )
    )
    return bar
def emo_count(df):
    df['内容']=pd.to_numeric(df['内容'], errors='coerce')
    emo_counts=df['内容'].value_counts()
    print("Emotion counts:", emo_counts)

    positive_count=emo_counts.get(1, 0)
    negative_count=emo_counts.get(0, 0)
    emo_data=[("正面", positive_count), ("负面", negative_count)]
    print(emo_data)



def main():
    df=pd.read_csv('standard_location_counts.csv')
    df2=pd.read_csv('standard_comment_unique_deduplicated.csv')
    create_wordcloud(df2)
    bar = bar_chart(df)
    map_=map(df)
    df3=pd.read_csv('predictions.csv')
    emo_count(df3)

if __name__ == "__main__":
    main()


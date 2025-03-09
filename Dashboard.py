import streamlit as st
import pandas as pd
import json
from pyecharts.charts import Geo, Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from collections import Counter
from pyecharts.datasets import COORDINATES
import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import plotly.express as px
import os

#  Set page configuration
st.set_page_config(page_title="Ne Zha Comprehensive Dashboard", layout="wide")

#  Page title
st.title("🌟 Ne Zha Audience Insights Dashboard")

#  Sidebar navigation
menu = st.sidebar.selectbox("Choose a Chart:", ["Geo Map", "Bar Chart", "Box Office", "Word Cloud"])

#  Process geographic data for city names
def handle(cities):
    try:
        with open("city_coordinates.json", mode="r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data_new = data.copy()
    for city in set(cities):
        for k in data:
            if k.startswith(city):
                data_new[city] = data[k]
                break
    with open("city_coordinates.json", mode="w", encoding="utf8") as f:
        json.dump(data_new, f, ensure_ascii=False)

#  Read comments and extract city information
def get_comment_data():
    cities = []
    with open('comments.txt', mode='r', encoding='utf8') as f:
        for row in f:
            try:
                city = row.split(',')[2].strip()
                if city:
                    cities.append(city)
            except IndexError:
                continue
    handle(cities)
    data = Counter(cities).most_common()
    valid_data = [(city, count) for city, count in data if city in COORDINATES]
    return valid_data

#  Generate Geo Map
def generate_geo():
    valid_data = get_comment_data()
    total_observations = sum([item[1] for item in valid_data])
    num_points = len(valid_data)

    geo = Geo(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    geo.add_schema(maptype="china")
    geo.add("", valid_data, symbol_size=15)
    geo.set_global_opts(
        title_opts=opts.TitleOpts(
            title="",
            subtitle=f"Data source: Maoyan | Total Observations: {total_observations}\nEach Point Represents the number of Fans from a City in China",
            pos_top="2%",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=20),
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12, color='black')
        ),
        visualmap_opts=opts.VisualMapOpts(max_=6500, is_piecewise=True)
    )
    return geo.render_embed(), total_observations, num_points

#  Generate Bar Chart with Translated City Names
def generate_bar():
    valid_data = get_comment_data()

    # Translate city names to English
    city_translation = {
        '北京': 'Beijing', '上海': 'Shanghai', '广州': 'Guangzhou',
        '深圳': 'Shenzhen', '杭州': 'Hangzhou', '南京': 'Nanjing',
        '天津': 'Tianjin', '重庆': 'Chongqing', '成都': 'Chengdu',
        '西安': 'Xi\'an', '武汉': 'Wuhan', '长春': 'Changchun',
        '沈阳': 'Shenyang', '青岛': 'Qingdao', '大连': 'Dalian',
        '厦门': 'Xiamen', '福州': 'Fuzhou', '苏州': 'Suzhou',
        '无锡': 'Wuxi', '哈尔滨': 'Harbin', '东莞': 'Dongguan',
        '长沙': 'Changsha', '郑州': 'Zhengzhou', '佛山': 'Foshan',
        '昆明': 'Kunming', '南宁': 'Nanning'
    }

    # Use translated names for the X-axis
    translated_xaxis = [city_translation.get(city, city) for city, _ in valid_data[:20]]

    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar.add_xaxis(translated_xaxis)
    bar.add_yaxis("Number of fans", [item[1] for item in valid_data[:20]])
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="Data source: Maoyan"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30, font_size=12, color='gray', interval=0))
    )
    return bar.render_embed()

#  Generate Box Office Plot
df = pd.read_csv("box_office.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

def generate_box_office():
    fig = px.line(df, x='Date', y='BoxOffice', color='Region', title='Box Office Trends')
    fig.update_layout(template='plotly_dark')
    return fig

#  Generate Word Cloud
def get_comments():
    with open('comments.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        comments = []
        for comment in rows:
            try:
                comment = comment.split(',')[3]
            except:
                continue
            else:
                comments.append(comment)
        return comments

def generate_wordcloud(comments):
    comments_after_split = jieba.cut(str(comments), cut_all=False)
    words = ' '.join(comments_after_split)

    stopwords = STOPWORDS.copy()
    stopwords.update(['哪吒', '电影', '我命', '不由'])

    # Use relative paths for assets
    base_path = os.path.dirname(os.path.abspath(__file__))
    bg_img_path = os.path.join(base_path, 'circle.png')
    font_path = os.path.join(base_path, 'STKAITI.TTF')

    bg_img = plt.imread(bg_img_path)
    wc = WordCloud(
        width=1024, height=768, background_color='white', mask=bg_img,
        stopwords=stopwords, max_font_size=200, random_state=50,
        font_path=font_path
    )
    wc.generate_from_text(words)
    wc.to_file("wordcloud.png")
    return "wordcloud.png"

# Display selected charts based on user choice
if menu == "Geo Map":
    st.subheader("Ne Zha Fan Distribution")
    geo_html, total_observations, num_points = generate_geo()
    st.components.v1.html(geo_html, height=600, scrolling=True)
elif menu == "Bar Chart":
    st.subheader("Top 20 Fan Sources")
    st.components.v1.html(generate_bar(), height=600, scrolling=True)
elif menu == "Box Office":
    st.subheader("Box Office Trends")
    st.plotly_chart(generate_box_office(), use_container_width=True)
elif menu == "Word Cloud":
    st.subheader("Word Cloud of Comments")
    st.image(generate_wordcloud(get_comments()), use_column_width=True)





from collections import Counter
from pyecharts.charts import Geo, Bar
from pyecharts import options as opts
import json

#  Process place name data to ensure that city names match geographical coordinates
def handle(cities):
    """
    Ensures that city names in the comments match the geographical coordinates
    stored in 'city_coordinates.json'. If a city is not found, it is removed from the list.

    Args:
        cities (list): A list of city names extracted from comments.
    """
    try:
        # Load existing city coordinates data
        with open("city_coordinates.json", mode="r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Create a copy of city data to update
    data_new = data.copy()

    # Match and update city coordinates
    for city in set(cities):
        count = 0
        for k in data:
            count += 1
            if k == city:
                break
            if k.startswith(city):  # Handle shorthand names
                data_new[city] = data[k]
                break
            if k.startswith(city[:-1]) and len(city) >= 3:  # Handle administrative changes
                data_new[city] = data[k]
                break
        if count == len(data):
            print(f"{city} not found, deleting...")
            # Remove cities that cannot be matched
            cities = [c for c in cities if c != city]  # Fixed dead loop issues

    # Save updated coordinates
    with open("city_coordinates.json", mode="w", encoding="utf-8") as f:
        json.dump(data_new, f, ensure_ascii=False)

#  Import pyecharts built-in geographical coordinates
from pyecharts.datasets import COORDINATES

#  Render map & bar chart
def render():
    """
    Extracts city information from comments, processes it, and generates:
    1. A geographical distribution map of fans using a Geo chart.
    2. A bar chart showing the top 20 cities by fan count.
    """
    # Extract city information from comments
    cities = []
    with open('C://Users/ljysg/project1/final-project/comments.txt', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            try:
                city = row.split(',')[2].strip()
            except IndexError:
                continue
            if city:
                print(f"Extract to city: {city}")  # Debug output
                cities.append(city)

    # Handle empty city data case
    if not cities:
        print("Warning: No city data was extracted, please check comments.txt for content!")
        return

    # Process city names and coordinates
    handle(cities)

    # Count city occurrences
    data = Counter(cities).most_common()

    # Handle empty data case after processing
    if not data:
        print("Warning: Statistics are empty, all cities may have been deleted during processing.")
        return

    # Filter cities based on available coordinates in pyecharts
    valid_data = [(city, count) for city, count in data if city in COORDINATES]

    # Handle no valid data case
    if not valid_data:
        print("There is no valid city data to draw, please check if the city name matches the place name supported by 'pyecharts'!")
        return
    
    total_observations = sum(count for city, count in valid_data)
    
    # Manually add missing city coordinates
    COORDINATES["延边"] = [129.5132, 42.9048]

    #  Create Geo map for fan distribution
    geo = Geo()
    geo.add_schema(maptype="china")  

    # Prepare data for Geo chart
    attr, value = zip(*valid_data)
    geo.add("", list(zip(attr, value)), symbol_size=15)

    # Configure Geo chart options
    geo.set_global_opts(
        title_opts=opts.TitleOpts(
            title="Where Fans of Ne Zha Come From: Popularity and Distribution Insights",
            subtitle=f"Data source: Maoyan | Total Observations: {total_observations}\nEach Point Represents the number of Fans from a City in China",
            pos_top="2%",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(font_size=20),
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12, color='black')
        ),
        visualmap_opts=opts.VisualMapOpts(max_=6500, is_piecewise=True)
    )

    # Render Geo chart as HTML
    geo.render('location distribution of fans.html')

    #  Create Bar chart for top 20 cities by fan count
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

    bar = Bar()
    bar.add_xaxis(translated_xaxis)
    bar.add_yaxis("Number of fans", list(value))

    # Configure Bar chart options
    bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title="Unveiling Ne Zha's Fan Origins: Top Source List",
            subtitle="DataSource: Maoyan",
            pos_top="5%",
            pos_left="center"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30, font_size=12, color='gray', interval=0))
    )

    # Render Bar chart as HTML
    bar.render('Source Leaderboard- Bar chart.html')

#  Entry point for script execution
if __name__ == '__main__':
    render()

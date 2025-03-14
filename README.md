### **Ne Zha Audience Insights Dashboard**  

---

## **Project Overview**  

The **Ne Zha Audience Insights Dashboard** is an interactive visualization project that provides insights into the audience demographics, regional box office trends, and sentiment analysis based on user comments. This project leverages **Python, Streamlit, Plotly, and Pyecharts** to create a comprehensive dashboard with four key visualizations:  

- **Geo Map:** Displays the geographic distribution of fans across cities in China.  
- **Bar Chart:** Highlights the top 20 cities with the highest number of fans.  
- **Box Office Trends:** Presents an interactive time-series analysis of box office revenue across different regions.  
- **Word Cloud:** Visualizes the most common words in audience comments.  

The goal is to analyze how *Ne Zha* performed in various regions, where the audience engagement was highest, and what people were saying about the movie.  

---

## **Installation Instructions**  

### **1. Clone the Repository**  
To get started, clone the repository to your local machine using:  
```bash
git clone https://github.com/jingyi821/Ne-Zha-Audience-Insights.git
cd Ne-Zha-Audience-Insights
```

### **2. Set Up a Virtual Environment (Recommended)**  
It is recommended to use a virtual environment to manage dependencies:  
```bash
python -m venv env
source env/bin/activate  # For Mac/Linux
env\Scripts\activate  # For Windows
```

### **3. Install Dependencies**  
Install all required packages using:  
```bash
pip install -r requirements.txt
```

### **4. Run the Dashboard**  
Launch the interactive dashboard using Streamlit:  
```bash
streamlit run Dashboard.py
```

This will open a browser window where you can interact with the visualizations.  

---

## **Usage Guide**  

### **1. Navigating the Dashboard**  
Once the dashboard is running, you will see a **sidebar menu** where you can select different visualizations:  

📌 **Geo Map:** View the distribution of Ne Zha fans across Chinese cities.  
📌 **Bar Chart:** See which cities had the most engaged audience.  
📌 **Box Office Trends:** Track revenue performance over time.  
📌 **Word Cloud:** Explore audience sentiments and frequently mentioned words.  

### **2. Interacting with Visualizations**  
- **Hover over data points** to see detailed information.  
- **Click on dropdowns** (for Box Office Trends) to filter by region.  
- **Zoom in/out** on the Geo Map for better clarity.  

---

## **Project Structure**  
```
Ne-Zha-Audience-Insights/
│── box_office_Echarts/          # Contains the ECharts-based box office visualization
│── nezha_fan_analysis/          # Scripts for data processing and visualization
│── wordcloud_of_comments/       # Word cloud generation files
│── Dashboard.py                 # Streamlit-based interactive dashboard
│── README.md                    # Project documentation
│── requirements.txt              # Dependencies
│── box_office.csv                # Box office data
│── comments.txt                  # User comments dataset
│── city_coordinates.json         # City latitude and longitude mapping
│── circle.png                    # Background mask for the word cloud
│── wordcloud.png                 # Generated word cloud image
│── STKAITI.TTF                   # Chinese font for word cloud
```

---

## **Acknowledgments**  
- **Data Sources:** Maoyan  
- **Tools Used:** Streamlit, Plotly, Pyecharts, WordCloud, Pandas  

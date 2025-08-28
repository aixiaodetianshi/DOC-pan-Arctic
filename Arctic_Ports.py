import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pandas as pd
import folium

# 限定国家或地区为“北极相关区域”
ARCTIC_COUNTRIES = [
    "Norway", "Russia", "Canada", "United States", "Greenland", "Iceland", "Finland", "Sweden"
]

BASE_URL = "https://www.worldportsource.com"

def get_country_ports(country_name):
    """从指定国家页面抓取港口列表链接"""
    url = f"{BASE_URL}/ports/index/{country_name}.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    port_links = soup.select("a[href*='/ports/']")  # 港口链接
    port_urls = [BASE_URL + a['href'] for a in port_links if '/ports/' in a['href']]
    return list(set(port_urls))  # 去重

def get_port_info(port_url):
    """从港口页面获取详细信息"""
    response = requests.get(port_url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        name = soup.find("h1").text.strip()
    except:
        name = None

    info_table = soup.find("table", {"class": "portInfo"})
    if not info_table:
        return None

    data = {
        "port_name": name,
        "country": None,
        "latitude": None,
        "longitude": None,
        "url": port_url
    }

    for row in info_table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].text.strip()
            val = cols[1].text.strip()
            if "Country" in key:
                data["country"] = val
            elif "Latitude" in key:
                data["latitude"] = val
            elif "Longitude" in key:
                data["longitude"] = val

    return data

def scrape_arctic_ports():
    all_ports = []
    for country in ARCTIC_COUNTRIES:
        print(f"Fetching ports from: {country}")
        try:
            port_urls = get_country_ports(country)
            for url in port_urls:
                info = get_port_info(url)
                if info:
                    all_ports.append(info)
                    print(f"Got: {info['port_name']}")
                time.sleep(1)  # 避免过快访问被封
        except Exception as e:
            print(f"Error fetching {country}: {e}")

    # 保存为 CSV
    df = pd.DataFrame(all_ports)
    df.to_csv("arctic_ports_info.csv", index=False)
    print("Scraping complete. Saved to arctic_ports_info.csv.")

if __name__ == "__main__":
    scrape_arctic_ports()


import pandas as pd
import folium

def visualize_arctic_ports(csv_file="arctic_ports_info.csv", output_map="arctic_ports_map.html"):
    # 读取数据
    df = pd.read_csv(csv_file)

    # 清洗数据，确保坐标是数字
    def convert_coord(coord_str):
        if pd.isna(coord_str): return None
        coord_str = coord_str.replace("°", "").replace("N", "").replace("E", "").replace("S", "-").replace("W", "-")
        return float(coord_str.strip())

    df['latitude'] = df['latitude'].apply(convert_coord)
    df['longitude'] = df['longitude'].apply(convert_coord)

    # 初始化地图：中心为北极区域
    arctic_map = folium.Map(location=[72, 0], zoom_start=2, tiles='CartoDB positron')

    # 添加港口标记
    for _, row in df.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
            popup = folium.Popup(f"""
                <b>Port:</b> {row['port_name']}<br>
                <b>Country:</b> {row['country']}<br>
                <b>URL:</b> <a href="{row['url']}" target="_blank">Link</a>
            """, max_width=300)
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=popup,
                icon=folium.Icon(color='blue', icon='ship', prefix='fa')
            ).add_to(arctic_map)

    # 保存为 HTML 文件
    arctic_map.save(output_map)
    print(f"Map saved as {output_map}")

# 运行地图可视化函数
visualize_arctic_ports()

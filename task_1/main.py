import requests
from bs4 import BeautifulSoup
import json

def generate_html(data, filename="index.html"):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Новости Hacker News</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f0f2f5 0%, #e0e5ec 100%); /* Мягкий градиент */
                margin: 0;
                padding: 20px;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                max-width: 1000px;
                margin: 30px auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            }}
            h1 {{
                color: #f60;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                border-bottom: 3px solid #f60;
                padding-bottom: 15px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #e0e0e0;
                padding: 15px;
                text-align: left;
            }}
            th {{
                background-color: #f60;
                color: white;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            tr:nth-child(even) {{
                background-color: #f8f8f8;
            }}
            tr:hover {{
                background-color: #f1f1f1;
                transform: translateY(-2px);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }}
            .source-link {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px dashed #ccc;
            }}
            .source-link a {{
                color: #f60;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1em;
            }}
            .source-link a:hover {{
                text-decoration: underline;
                color: #e55e00;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Последние новости с Hacker News</h1>
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Заголовок</th>
                        <th>Комментарии</th>
                    </tr>
                </thead>
                <tbody>
    """

    for i, item in enumerate(data):
        html_content += f"""
                    <tr>
                        <td>{i + 1}</td>
                        <td>{item['title']}</td>
                        <td>{item['comments']}</td>
                    </tr>
        """
    html_content += f"""
                </tbody>
            </table>
            <div class="source-link">
                <p>Оригинальный источник данных: <a href="https://news.ycombinator.com/" target="_blank">Hacker News</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML-страница успешно сгенерирована в файл {filename}")


def save_to_json(data, filename="data.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Информация успешно сохранена в файл {filename}")

def scrape_hacker_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []
    
    # Ищем все основные строки статей
    article_rows = soup.find_all('tr', class_='athing')

    for i, row in enumerate(article_rows):
        # Заголовок
        title_tag = row.find('span', class_='titleline').find('a')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Ищем следующую строку, где находятся комментарии и другая подтекстовая информация
        subtext_row = row.find_next_sibling('tr', class_='spacer') # или просто find_next_sibling('tr')
        if not subtext_row:
             subtext_row = row.find_next_sibling('tr') 
        
        comments_count = 0
        if subtext_row:
            comments_tag = subtext_row.find('a', string=lambda text: text and 'comment' in text)
            if comments_tag:
                try:
                    comments_text = comments_tag.get_text(strip=True)
                    # Извлекаем число перед словом 'comments'
                    comments_count = int(comments_text.split(' ')[0])
                except (ValueError, IndexError):
                    pass 
            else:
                # Если нет ссылки на комментарии, но есть 'discuss', значит 0 комментариев
                discuss_tag = subtext_row.find('a', string='discuss')
                if discuss_tag:
                    comments_count = 0 

        news_data.append({"title": title, "comments": comments_count})
        print(f"{i+1}. Title: {title}; Comments: {comments_count};")
        
    return news_data

if __name__ == "__main__":
    print("Запуск программы:")
    print("Собираем новости с Hacker News:")
    scraped_data = scrape_hacker_news()
    save_to_json(scraped_data)
    generate_html(scraped_data)
    print("Программа завершила работу.")
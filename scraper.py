from requests_html import HTML
import json
import os
import re

def scrape_hero_data():
    local_page = "local_page.html"
    avatar_folder = "local_page_files"  # 头像文件夹
    
    # 检查文件和文件夹是否存在
    if not os.path.exists(local_page):
        print(f"错误：未找到本地页面 {local_page}")
        print(f"当前目录：{os.getcwd()}")
        return
    
    if not os.path.exists(avatar_folder):
        print(f"错误：未找到头像文件夹 {avatar_folder}")
        print(f"当前目录：{os.getcwd()}")
        print(f"请确认文件夹名称正确，且与脚本在同一目录下")
        return
    
    # 检查文件夹中的文件
    avatar_files = os.listdir(avatar_folder)
    print(f"头像文件夹 {avatar_folder} 中找到 {len(avatar_files)} 个文件")
    if len(avatar_files) > 0:
        print(f"示例文件：{', '.join(avatar_files[:3])}...")
    
    try:
        with open(local_page, 'r', encoding='utf-8') as f:
            html_content = f.read()
        html = HTML(html=html_content)
        
        hero_links = html.find('#heroList-all ul li a[href^="https://300data.com/hero/"]')
        print(f"找到 {len(hero_links)} 个英雄链接")
        
        if not hero_links:
            print("未找到英雄链接")
            return
        
        heroes = []
        for link in hero_links:
            try:
                img = link.find('img', first=True)
                if not img or 'src' not in img.attrs:
                    continue
                
                img_src = img.attrs['src']
                img_filename = os.path.basename(img_src)
                
                # 详细的文件检查
                local_img_path = os.path.join(avatar_folder, img_filename)
                absolute_path = os.path.abspath(local_img_path)
                
                if not os.path.exists(local_img_path):
                    print(f"警告：头像文件不存在")
                    print(f"预期路径：{absolute_path}")
                    print(f"文件名：{img_filename}")
                    continue
                
                # 检查文件大小
                file_size = os.path.getsize(local_img_path)
                if file_size < 100:  # 小于100字节的文件可能损坏
                    print(f"警告：文件可能损坏（{file_size}字节）：{img_filename}")
                
                # 提取名称
                spans = link.find('span')
                name_span = None
                for span in reversed(spans):
                    if 'glyphicon' not in span.attrs.get('class', []) and span.text.strip():
                        name_span = span
                        break
                if not name_span:
                    continue
                name = name_span.text.strip()
                
                # 生成前端可访问的路径
                avatar_url = f"/local_page_files/{img_filename}"
                print(f"生成头像URL：{avatar_url}")
                
                heroes.append({
                    "name": name,
                    "avatar": avatar_url,
                    "debug": {
                        "filename": img_filename,
                        "local_path": absolute_path,
                        "file_size": file_size
                    }
                })
                print(f"已获取: {name}")
                
            except Exception as e:
                print(f"处理出错: {e}")
                continue
        
        unique_heroes = list({h['name']: h for h in heroes}.values())
        with open('heroes.json', 'w', encoding='utf-8') as f:
            json.dump(unique_heroes, f, ensure_ascii=False, indent=2)
        
        print(f"完成！共提取 {len(unique_heroes)} 个英雄")
        
    except Exception as e:
        print(f"解析出错: {e}")

if __name__ == "__main__":
    scrape_hero_data()

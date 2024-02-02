import pygame
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_clipboard_id():
    
id = id.replace("[r", "")
id = id.replace("]", "")

c = Options()
c.add_argument("--hardless")
c.page_load_strategy = "eager"
driver = webdriver.Chrome(options = c)

info = {}
info["pos"] = []
info["title"] = []
info["duration"] = []

def getInfo(album_id):
    try:
        driver.get("https://www.discogs.com/release/" + album_id)

        info["name"] = driver.find_element(By.CLASS_NAME, "title_1q3xW").text
        
        info_23nnx = driver.find_elements(By.XPATH, """//*[@id="page"]/div/div[2]/div/div[2]/table/tbody/tr/td""")
        info["label"] = info_23nnx[0].text
        info["format"] = info_23nnx[1].text
        info["country"] = info_23nnx[2].text
        info["released"] = info_23nnx[3].text
        info["genre"] = info_23nnx[4].text
        info["style"] = info_23nnx[5].text
        
        statistics = driver.find_elements(By.XPATH, """//*[@id="release-stats"]/div/div/ul/li/a""")
        info["have"] = statistics[0].text
        info["want"] = statistics[1].text
        info["avg_rating"] = driver.find_element(By.XPATH, """//*[@id="release-stats"]/div/div/ul[1]/li[3]/span[2]""").text
        info["ratings"] = statistics[2].text
        info["low"] = driver.find_element(By.XPATH, """//*[@id="release-stats"]/div/div/ul[2]/li[2]/span[2]""").text
        info["median"] = driver.find_element(By.XPATH, """//*[@id="release-stats"]/div/div/ul[2]/li[3]/span[2]""").text
        info["high"] = driver.find_element(By.XPATH, """//*[@id="release-stats"]/div/div/ul[2]/li[4]/span[2]""").text
        try:
            info["sells"] = driver.find_element(By.XPATH, """//*[@id="release-marketplace"]/div/div[1]/div""").text
        except:
            info["sells"] = "无出售信息"
        info["jacket_url"] = driver.find_element(By.XPATH, """//*[@id="page"]/div/div[2]/div/div[1]/div/a/div/picture/img""").get_attribute("src")

        # with open('./jacket.png', 'wb') as file:
            # file.write(driver.find_element(By.XPATH, """//*[@id="page"]/div/div[2]/div/div[1]/div/a/div/picture/img""").screenshot_as_png)
        try:
            track_pos = driver.find_elements(By.CLASS_NAME, "trackPos_2RCje")
            track_title = driver.find_elements(By.XPATH, """//*[@id="release-tracklist"]/div/table/tbody//span[@class="trackTitle_CTKp4"]""")
            track_duration = driver.find_elements(By.CLASS_NAME, "duration_2t4qr")
            for pos in track_pos:
                info["pos"].append(pos.text)
            for title in track_title:
                info["title"].append(title.text)
            for duration in track_duration:
                info["duration"].append(duration.text)
        except:
            pass

        driver.quit()
        print(info)

    except Exception as e:
        print("wrong id or error while get album info.", e)
        quit()

getInfo(id)

pygame.init()
clock = pygame.time.Clock()

width = 1000
height = 700

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("DisCogs Viewer")

pygame.scrap.init()

input_box = pygame.Rect(8, 8, 70, 24)
input_color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
input_color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
input_color = input_color_inactive  # 当前颜色，初始为未激活颜色
input_active = False
input_text = ''
input_done = False
input_font = pygame.font.Font(None, 18)

font_genei = pygame.font.Font("./fonts/genei-pople.ttf", 20)
font_doki = pygame.font.Font("./fonts/DokiDokiFantasia.otf", 43)
font_natsumi = pygame.font.Font("./fonts/natsuzemi-maru-gothic-black.ttf", 30)
font_spoqa = pygame.font.Font("./fonts/SpoqaHanSansJPRegular.ttf", 16)
font_yaheib = pygame.font.FontType("./fonts/msyhbd.ttc", 14)
font_yahei = pygame.font.FontType("./fonts/msyh.ttc", 16)

while True:
    window.fill((0, 0 ,0))

    name_render = font_natsumi.render(info["name"], True, (255, 255, 255), None)
    x, y = name_render.get_size()
    if x > width:
        y = y /(x / (width - 25))
        name_render = pygame.transform.scale(name_render, (width - 25, y))
    
    window.blit(name_render, (14, 20))
    window.blit(font_spoqa.render("厂牌: " + info["label"], True, (255, 255, 255), None), (8, 75))
    window.blit(font_spoqa.render("媒体形式: " + info["format"], True, (255, 255, 255), None), (8, 95))
    window.blit(font_spoqa.render("发行地: " + info["country"], True, (255, 255, 255), None), (8, 115))
    window.blit(font_spoqa.render("发行日期: " + info["released"], True, (255, 255, 255), None), (8, 135))
    window.blit(font_spoqa.render("分类: " + info["genre"], True, (255, 255, 255), None), (8, 155))
    window.blit(font_spoqa.render("风格: " + info["style"], True, (255, 255, 255), None), (8, 175))

    window.blit(font_yaheib.render("Discogs数据中," + info["have"] + "人持有," + info["want"] + "人想要", True, (255, 255, 255), None), (8, 201))
    window.blit(font_yaheib.render("共" + info["ratings"] + "人打分:  " + info["avg_rating"], True, (255, 255, 255), None), (8, 217))
    window.blit(font_yaheib.render("最低价: " + info["low"] + "  平均价: " + info["median"] + "  最高价: " + info["high"], True, (255, 255, 255), None), (8, 233))
    window.blit(font_yaheib.render(info["sells"], True, (255, 255, 255), None), (8, 249))

    if len(info["title"]) > 0:
        for i in range(0, len(info["title"])):
            window.blit(font_yahei.render(info["pos"][i] , True, (255, 255, 255), None), (325, 300 + (i * 20)))
            window.blit(font_yahei.render(info["title"][i] , True, (255, 255, 255), None), (365, 300 + (i * 20)))

    try:
        urllib.request.urlretrieve(info["jacket_url"], "./jacket.jpeg")
        img = pygame.image.load("./jacket.jpeg").convert()
        img = pygame.transform.scale(img, (300, 300))
        window.blit(img, (3, 300))
    except:
        window.blit(font_natsumi.render("无法获取封面图片", True, (222, 222, 222), None), (20, 300))

    input_txtSurface = input_font.render(input_text, True, input_color)  # 文字转换为图片
    input_box.w = max(200, input_txtSurface.get_width()+10)  # 当文字过长时，延长文本框
    window.blit(input_txtSurface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(window, input_color, input_box, 2)

    pygame.display.flip()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(input_box.collidepoint(event.pos)):  # 若按下鼠标且位置在文本框
                input_active = True
            else:
                input_active = False
            input_color = input_color_active if(input_active) else input_color_inactive
        if(event.type == pygame.KEYDOWN):  # 键盘输入响应
            if(input_active):
                if(event.key == pygame.K_RETURN):
                    print(input_text)
                elif(event.key == pygame.K_BACKSPACE):
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
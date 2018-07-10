# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 16:52:50 2018

@author: dell
"""
import requests,re
from bs4 import BeautifulSoup 
url_1= 'http://222.197.183.99/TutorList.aspx'
def make_WordCloud(chtext,save = False,name=''):
    import jieba #中文分词包  
    from wordcloud import WordCloud  
    import matplotlib.pyplot as plt  
    import matplotlib
    jieba.add_word('电子科技大学')
    cha=''
    cha =' '.join(jieba.cut(chtext))
    font = 'C:\Windows\Fonts\STXIHEI.TTF'
    wc = WordCloud(
            background_color='white',
            font_path=font, 
            width=1000, height=860, 
            max_font_size=150,
            max_words = 50,)
    myfont = matplotlib.font_manager.FontProperties(fname=font)
    wc.generate(cha)   
    plt.title(name,fontproperties=myfont)
    plt.imshow(wc)  
    plt.axis("off")  
    plt.show() 
    
    if save == True:   
        wc.to_file(name+".png")  
def getHtml(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print("err")
        return None
    
def find_teacherUrl(name):
    html = getHtml(url_1)
    soup =BeautifulSoup(html,"html.parser") 
    teacher = soup.find_all('a',{'href':re.compile(r'TutorDetails.*?')})
    for each_teacher in teacher:
        if name == each_teacher.text.strip()[6:]:
            return each_teacher['href']
    print("not find")
    return None

def get_teacherInfrom(teacherUrl):
    url_head ='http://222.197.183.99/'
    #regex
    find_direct = r'<td class="alignleft">\s+(.*?)\s+</td>'
    find_acade = r'<span id="Labelxymc">(.*?)</span>'
    find_acadeExper = r'<span id="Labelxsjl">([\s\S]*?)</span>'
    find_personIntroduce = r'<span id="Labelgrjj">([\s\S]*?)</span>'
    find_project = r'<span id="Labelgrjj">([\s\S]*?)</span>'
    teacher_Infrom = ' '
    html = getHtml(url_head+teacherUrl)
    direct = re.findall(find_direct,html)
    acade = re.findall(find_acade,html)
    acadeExper = re.findall(find_acadeExper,html)
    personIntroduce = re.findall(find_personIntroduce,html)
    project = re.findall(find_project,html)
    teacher_Infrom = teacher_Infrom.join(direct)
    teacher_Infrom += "".join(acade[0]+acadeExper[0]+personIntroduce[0]+project[0])
    return teacher_Infrom

if __name__ == '__main__':  
    techerName= '周雪'
    url = find_teacherUrl(techerName)
    teacher_Infrom = get_teacherInfrom(url)
    make_WordCloud(teacher_Infrom,name = techerName)

import konlpy
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

okt=Okt()

text = konlpy.utils.read_txt('이용수할머니기자회견문.txt', encoding=u'utf-8') 
nouns = okt.nouns(text)

words = []
for i in nouns:
    if len(i) > 1:
        words.append(i)

count = Counter(words)

most = count.most_common(100)

tags = {}
for i, j in most:
    tags[i] = j

wc = WordCloud(font_path = 'NANUMSQUARE.TTF', width=1200, height=1200, scale = 2.0, max_font_size = 250)

gen = wc.generate_from_frequencies(tags)

plt.figure()
plt.imshow(gen, interpolation='bilinear')
wc.to_file('mh2.png')

plt.close()

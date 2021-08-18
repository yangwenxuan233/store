from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = open('alice.txt').read()
print(text)
wd = WordCloud(background_color='white').generate(text)
plt.axis('off')
plt.imshow(wd)
plt.show()

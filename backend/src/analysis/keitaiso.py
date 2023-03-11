import numpy as np
import pandas as pd
import MeCab
import collections
import csv

## ネガポジ判定部分
pn_data = pd.read_table('./data/pn.tsv', names=('単語', 'ネガポジ', '分類'))
pn_word_list = list(pn_data['単語'])


## 形態素解析部分
sentence1 = '私はりんごは好きだけど、バナナは好きではない。なぜなら、バナナには水分が多く含まれていないため、果物特有の瑞々しさを感じないからだ。同じような理由で、パンもそんなに好きではない。どちらかと言えば、ご飯やうどんの方が好きだ。'

m = MeCab.Tagger('-Ochasen')

word_data_string_list = m.parse(sentence1).split('\n')
sentence_data_list = []

for word_data_string in word_data_string_list:
    word_data = word_data_string.split('\t')
    if word_data[0] == 'EOS':
        break
    if not word_data[3].startswith('助詞'):
        sentence_data_list.append(word_data)

sentence_word_data = pd.DataFrame(
    sentence_data_list,
    columns = ['表層刑', '読み', '原型', '品詞', '活用形', '活用型']
)


## 文章のネガポジカウント
p_count = 0
n_count = 0
last_count = None
for word_data in sentence_word_data.iloc:
    word = word_data['表層刑']
    if word_data['活用形'] == '特殊・ナイ':
        if last_count == 'p':
            p_count = p_count - 1
            n_count = n_count + 1
        if last_count == 'n':
            p_count = p_count + 1
            n_count = n_count - 1
        last_count = None

    if word in pn_word_list:
        nega_poji = pn_data[pn_data['単語']==word]['ネガポジ'].iat[0]
        if nega_poji == 'p':
            last_count = nega_poji
            p_count = p_count + 1
        if nega_poji == 'n':
            last_count = nega_poji
            n_count = n_count + 1

print('ポジティブカウント: %d' % p_count)
print('ネガティブカウント: %d' % n_count)

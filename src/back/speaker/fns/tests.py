from django.test import TestCase
import re
# Create your tests here.

a= 'пишите код так, как будто сопровождать его будет склонный к насилию психопат, который знает, где вы живете'


substring = 'сопровождать'
index = a.find('сопровождать')


result = re.sub('сопровождать', 'поддерживать', a)

res = a.split(',')
b = ','.join(res)


NUM = 12345
sums= 0
for i in str(NUM):
    sums += int(i)

letters = 'ЫгВЫоЯСремДШНККАыкЩЙФа'
h= letters.lower()


for x in  [1, 4, 5, 6, 2, 3, 7, 8, 9, 10]:
      if x in (2 , 3 , 7):
           break
      if x % 2 == False:
       x

strt = 'Лазер Боре хер обрезал'
a= strt[::-1]
print(strt.replace(' ', '').lower() == a.replace(' ', '').lower())

from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests
urls=["https://www.guitarcenter.com/Guitars.gc#pageName=department-page&N=18144&Nao=0&recsPerPage=90&&Ns=bS&profileCountryCode=CA&profileCurrencyCode=CAD","https://www.guitarcenter.com/Guitars.gc#pageName=department-page&N=18144&Nao=90&recsPerPage=90&&Ns=bS&profileCountryCode=CA&profileCurrencyCode=CAD","https://www.guitarcenter.com/Guitars.gc#pageName=department-page&N=18144&Nao=180&recsPerPage=90&&Ns=bS&profileCountryCode=CA&profileCurrencyCode=CAD","https://www.guitarcenter.com/Guitars.gc#pageName=department-page&N=18144&Nao=270&recsPerPage=90&&Ns=bS&profileCountryCode=CA&profileCurrencyCode=CAD"]
name_list=[]
price_list=[]
price_match_list=[]
namee_list=[]
review_list=[]
rating=[]
revieww_list=[]
for i in range(len(urls)):
    source=requests.get(urls[i])
    soup=BeautifulSoup(source.text,'html')
    gname=soup.find_all('div',class_='productTitle')
    price=soup.find_all('div',class_='mainPrice')
    ratings=soup.find_all('div',class_='ratingReviewsDisplayLinks')
    # Guitar Name list
    for i in gname:
        a = i.find('a')
        name_list.append(a.string)
        namee_list=list(map(lambda x:x.strip(),name_list))

    #Guitar actual price
    for i in price:
        p = i.find('span').contents[2]
        price_list.append(p.string)

    #Guitar MRP and low price list
    for j in price:
        b=j.find('var')
        price_match_list.append(b.string)

    #Guitar ratings list
    for k in ratings:
        c=k.find('span').contents[0]
        rating.append(c.text)

    #Guitar number of reviews
    for l in ratings:
        d=l.find('span').contents[1]
        review_list.append(d.string)
        revieww_list=list(map(lambda x:x.strip(),review_list))

df = pd.DataFrame({'Name': namee_list,'Price':price_list,'Price_match':price_match_list,'Ratings':rating,'reviews':revieww_list})
df.to_csv('guitar_data.csv')




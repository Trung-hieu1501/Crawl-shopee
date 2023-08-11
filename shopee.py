from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()


driver.get("https://shopee.vn/buyer/login?next=https%3A%2F%2Fshopee.vn%2Fgzzifriend.vn%3Fpage%3D0%26sortBy%3Dpop")
# #login
username = "YourUserName"
password = "YourPassWord"

time.sleep(3)
username_field = driver.find_element(By.CSS_SELECTOR,".D3QIf1 .pDzPRp")
username_field.send_keys(username)
time.sleep(3)
password_field = driver.find_element(By.CSS_SELECTOR, '.vkgBkQ .pDzPRp')
password_field.send_keys(password)
time.sleep(3)
  # Bấm nút đăng nhập
login_button = driver.find_element(By.CSS_SELECTOR, ".wyhvVD")
login_button.click()

time.sleep(5)
link, sold, price, name, cost, product_id,score=[],[],[],[], [],[],[]

k=0
while True:
    elems = driver.find_elements(By.CSS_SELECTOR , '.col-xs-2-4 [href]')
    link = link+ [elem.get_attribute('href') for elem in elems]
            
   
    if k!=1:
        next_page = driver.find_element(By.CSS_SELECTOR, ".shopee-icon-button--right")
        next_page.click()
        time.sleep(4)
        k+=1
    else:
        break
print('Lấy link thành công')
reviews=[]
df2 = pd.DataFrame(columns = ['product_id','cmt_name','product_type', 'order_date', 'cmt'])
for i in range(0, len(link)-1):
    driver.get(link[i])
    time.sleep(5)
    name.append(driver.title)
    prices= driver.find_element(By.CSS_SELECTOR,'.pqTWkA')
    price.append(prices.text)
    
    costs= driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]')
    cost.append(costs.text)
    
    solds = driver.find_element(By.CSS_SELECTOR,'.eaFIAE')
    sold.append(solds.text)
    try:
        scores = driver.find_element(By.CSS_SELECTOR,'._046PXf')
        score.append(scores.text+'/5.0')
    except:
        score.append(' ')
        
    product_id_element = driver.find_element('xpath', '//script[contains(text(),"productID")]')
    script_text = product_id_element.get_attribute("innerHTML")
    product_id_start = script_text.find('"productID":"') + len('"productID":"')
    product_id_end = script_text.find('",', product_id_start)
    product_ids = script_text[product_id_start:product_id_end]
    product_id.append(product_ids)
    
    k=0
    cmt_name, cmt, product_type, order_date= [],[],[],[]
    while True:
        try:
            #cmt_name, cmt, product_type, order_date= [],[],[],[]
            for j in range(1,7):
                docs=driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/div[{}]/div/div[2]'.format(j))
                doc =docs.text
                date_type = doc.split('|')
                if len(date_type) == 2:
                    order_date.append(date_type[0].strip())
                    product_type.append(date_type[1].strip())
                else:
                    order_date.append(' ')
                    product_type.append(' ')
                # order_date.append(date_type[0].strip())
                # product_type.append(date_type[1].strip())
                cmt_names = driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/div[{}]/div/a'.format(j)).text
                cmt_name.append(cmt_names)
                cmts =driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[3]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/div[{}]/div/div[3]'.format(j)).text
                cmt.append(cmts)
                
            
            next_page_cmt = driver.find_element(By.CSS_SELECTOR, ".shopee-icon-button--right")
            next_page_cmt.click()
            time.sleep(3)
            k+=1
            if(k==3):
               break
        except NoSuchElementException:
            break
    df3 = pd.DataFrame(list(zip(cmt_name,product_type, order_date, cmt)), columns = ['cmt_name','product_type', 'order_date', 'cmt'])
    df3.insert(0, 'product_id',product_ids)
    df2=pd.concat([df2,df3], ignore_index=True)
    print('Lấy thông tin sản phẩm {} thành công'.format(i))


df1 = pd.DataFrame(list(zip(product_id,name, link,price, cost,sold,score)), columns = ['product_id','name', 'link','price', 'cost','sold','score'])
df1.to_csv('product.csv', index=False)
#df2 = pd.DataFrame(reviews)
df2.to_csv('review.csv', index=False)









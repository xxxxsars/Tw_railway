## 台灣鐵路自動訂票 
### 配置 
一般selenium都是預設使用FireFox做開啟，這邊透過driver來透過chorme開啟  
1. [下載chormdriver](https://chromedriver.storage.googleapis.com/index.html?path=2.24/) 請下載2.24版(其他版本有問題)    
2. 配置解壓縮後的chormedriver路徑於系統變數中  
![](https://github.com/xxxxsars/TW_Railway/blob/master/RdPic/Ms_path.png)  
3. python file導入chromedriver，並透過Options的設定解決chorme安全性問題，若沒有此配置會出現下圖下的問題  
```python
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 解決chrome所限制的安全性問題
chromedriver = r"C:\selenimu_chrom\chromedriver.exe"  # chromedriver.exe執行檔所存在的路徑
self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
self.driver.implicitly_wait(100)
```
![](https://github.com/xxxxsars/TW_Railway/blob/master/RdPic/security.png)  
## Python2+安裝opencv
1.  安裝numpy
```
pip install numpy
```
2.  到opencv官網下載(window.exe)[http://opencv.org/downloads.html]並解壓縮在解壓縮的資料夾下可以看到cv2.pyd (opencv\build\python\2.7\x64)，將此檔案移到python27\Lib\site-packages的目錄下   
3.  進行測試
```
import cv2
cv2.__version__
```
## Python3+安裝opencv
1.  安裝numpy
```
pip install numpy
```

2. 到此(下載相關whl檔)[http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv]    
3. cd到目錄安裝whl
```
pip install "numpy-1.11.2rc1+mkl-cp35-cp35m-win32.whl"

```
4.  進行測試
```
import cv2
cv2.__version__
```
## 透過firefox錄製自動化python code
1.  安裝firefox附加元件(下載)[https://addons.mozilla.org/zh-tw/firefox/addon/selenium-ide/]  
2.  下載後於右上角選單>開發者設定即會看到錄製檔
![](https://github.com/xxxxsars/TW_Railway/blob/master/RdPic/firefox.png)    
3.  當按下IDE的錄製後即會開始記錄動作
![](https://github.com/xxxxsars/TW_Railway/blob/master/RdPic/selenium.png)
4.  透過urlretrieve來存取抓到元素的圖片(詳細code參閱auto)
```
image = driver.find_element_by_id("idRandomPic")
img = image.get_attribute('src')
urlretrieve(img,"captcha2.png")
```
## osx安裝selsnium 
1. 到上面網址安裝firefox套件
2. 下載chromedriver並解壓縮到目錄下
3. 程式執行修改dirver
4. 下載opencv for osx 一樣解壓縮到目錄下

```python
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 解決chrome所限制的安全性問題
chromedriver = "/Users/mac/Python/chromedriver"  # chromedriver.exe執行檔所存在的路徑注意重點 不用加上exe
self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
self.driver.implicitly_wait(100)
```


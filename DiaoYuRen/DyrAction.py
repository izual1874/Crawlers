'''
点击到进入
MobileElement el1 = (MobileElement) driver.findElementById("com.lchr.diaoyu:id/rtv_start");
el1.click();
MobileElement el2 = (MobileElement) driver.findElementByXPath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.RelativeLayout[2]/android.widget.LinearLayout/android.widget.TextView[7]");
el2.click();
MobileElement el3 = (MobileElement) driver.findElementById("com.lchr.diaoyu:id/btn_tab_local");
el3.click();

'''
'''
地方页面, 这里有数量
MobileElement el1 = (MobileElement) driver.findElementByXPath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.view.View/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]");
el1.click();


#钓场返回定位页面
MobileElement el1 = (MobileElement) driver.findElementById("com.lchr.diaoyu:id/back_btn_img");
el1.click();

#商铺，点击的数量
MobileElement el1 = (MobileElement) driver.findElementByXPath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.view.View/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]");
el1.click();

#刷新页面
MobileElement el1 = (MobileElement) driver.findElementByXPath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ImageView");
el1.click();

'''

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random






class Action():
    def __init__(self):
        self.server = 'http://localhost:4723/wd/hub'
        self.desired_caps = {
          "platformName": "Android",
          "deviceName": "XiaoMi",
          "appPackage": "com.lchr.diaoyu",
          "appActivity": "com.lchr.diaoyu.SplashActivity",
          "resetKeyboard": True
        }
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        self.wait = WebDriverWait(self.driver, 40)
        self.action = TouchAction(self.driver)

    def wait_xpath(self, xpath):
        el = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return el

    def wait_ID(self, ids):
        el = self.wait.until(EC.presence_of_element_located((By.ID, ids)))
        return el

    def to_login(self):
        Tiyan = self.wait_ID("com.lchr.diaoyu:id/rtv_start")
        Tiyan.click()
        Tiaokuan = self.wait_ID("android:id/button1")
        Tiaokuan.click()
        # Qiehuan = self.wait_ID("com.lchr.diaoyu:id/tb_title")
        bendi = self.wait_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]")
        bendi.click()
    def to_city(self, city):
        #选择地区，在这里，默认定位
        chengshi = self.wait_ID("com.lchr.diaoyu:id/tv_city_name")
        chengshi.click()
        shuru = self.wait_ID("com.lchr.diaoyu:id/filter_edit")
        shuru.clear()
        shuru.send_keys(city)
        self.wait_ID("com.lchr.diaoyu:id/title").click()

    def to_fishings(self):
        fishings = self.wait_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.view.View/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]")
        fishings.click()

    def to_shops(self):
        shops = self.wait_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout/android.view.View/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]")
        shops.click()

    def scroll(self):
        #滑动
        while True:
            x = random.randint(400, 425)
            y = random.randint(360, 389)
            d = random.randint(650, 700)
            self.driver.swipe(x, y + d, x, y)
            sleep(1)
            shop_end = self.wait_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.View/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.TextView")
            fish_end = self.wait_xpath("	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.view.View/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.TextView")
    def main(self):
        self.to_login()
        # self.to_city()
        # self.to_fishings()
        self.to_shops()
        self.scroll()


if __name__ == '__main__':
    action = Action()
    action.main()
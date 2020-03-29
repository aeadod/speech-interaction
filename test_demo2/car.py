#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import os

class MockCar:

    def setup(self):
        pass

    def move_forward(self):
        print("The car moved forward")
    
    def stop(self):
        print("The car stopped")

    def switch_on_light(self):
        print("The light has been switched on")
    
    def switch_off_light(self):
        print("The light has been switched off")


class Car: 

    A1 = '//input[@data-reactid=".1.2.0.2.1.2.0.0.0:$A1.2.0.0.0.0.1.0"]'
    MOTOR1 = '//input[@data-reactid=".1.2.0.2.1.2.0.0.0:$MOTOR1.2.0.0.0.0.1.0"]'
    MOTOR2 = '//input[@data-reactid=".1.2.0.2.1.2.0.0.0:$MOTOR2.2.0.0.0.0.1.0"]'

    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:9009/#/project/5d7d42d6-236d-4196-a89a-c71d00eecc6f")
        explore_button = self.driver.find_element_by_xpath('//a[@class="button explore"]')
        explore_button.click()
        time.sleep(2)

        logic_flow_button = self.driver.find_elements_by_xpath("//*[contains(text(), 'LOGIC FLOW')]")
        logic_flow_button[0].click()

    def move_forward(self):
        
        m1_input = self.driver.find_element_by_xpath(Car.MOTOR1)
        m1_input.clear()
        m1_input.send_keys("20")
        m2_input = self.driver.find_element_by_xpath(Car.MOTOR2)
        m2_input.clear()
        m2_input.send_keys("20")
        time.sleep(3)
        self.__upload()
        print("The car moved forward")
    
    def stop(self):
        
        m1_input = self.driver.find_element_by_xpath(Car.MOTOR1)
        m1_input.clear()
        m1_input.send_keys("0")
        m2_input = self.driver.find_element_by_xpath(Car.MOTOR2)
        m2_input.clear()
        m2_input.send_keys("0")
        time.sleep(3)
        self.__upload()
        print("The car stopped")
    
    def switch_on_light(self):
        a1_input = self.driver.find_element_by_xpath(Car.A1)
        a1_input.send_keys(Keys.ARROW_UP)
        time.sleep(3)
        self.__upload()
        print("The light has been switched on")
    
    def switch_off_light(self):
        a1_input = self.driver.find_element_by_xpath(Car.A1)
        a1_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(3)
        self.__upload()
    
        print("The light has been switched off")

    def __upload(self):
        upload_button = self.driver.find_element_by_xpath('//img[@alt="Upload"]')
        upload_button.click()

def create_car(**kwargs):
    if kwargs.get("real", False):
        return Car()
    return MockCar()

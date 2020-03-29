from test_demo import input_record, recognition_speech
import time
import azure.cognitiveservices.speech as speechsdk

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

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


car = create_car()
car.setup()

while(1):
    a = input("Please choose C(Chinese) or E(English?):")
    print(a)

    if a == 'E' :
        speech_key, service_region = "649abba625264cb9b7f66ab40c8618a3", "southeastasia"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

        print("Say something...")

        result = speech_recognizer.recognize_once()


        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        if result.text=='Move forward.':
            car.move_forward()
        elif result.text=='Stop.':
            car.stop()
        elif result.text=='Switch on lights.':
            car.switch_on_light()
        elif result.text=='Switch off lights.':
            car.switch_off_light()
        else:
            print('Failed')


    elif a == 'C' :

        file_path = "record-audio.wav"
        APP_ID = '16827721'
        API_KEY = 'RihNGLWOeendn2qvYbPmOAUS'
        SECRET_KEY = 'O7QnPsKsnGsRMvf49wzSkaUnUB38E6zj'

        input_record.record(file_path)
        input_message = recognition_speech.voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
        print(input_message)
        if input_message[0]=='前进':
            car.move_forward()
        elif input_message[0]=='停止':
            car.stop()
        elif input_message[0]=='开灯':
            car.switch_on_light()
        elif input_message[0]=='关灯':
            car.switch_off_light()
        else:
            print('Failed')

    else:
        print('Failed')
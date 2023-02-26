from flask import Flask, request,render_template
import time
import undetected_chromedriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import display
import os


app = Flask(__name__)
current_dir = os.getcwd()
global driver_new


@app.route("/")
def hello_world():
    return render_template("steveChatGPT.html")


@app.route("/login", methods=["GET","POST"])
def chatgpt_login():
    #driver = webdriver.Chrome("chromedriver.exe")
    chrome_ver = int(input("Enter the chrome browser version:"))
    driver = undetected_chromedriver.Chrome(version_main=chrome_ver)
    driver.get("https://chat.openai.com/chat")
    
    time.sleep(5)
    count = 0
    while True:
        if count >= 2:
            break
        #driver.refresh()
        #This checks if it's already logged in
        try:
            textarea = driver.find_element_by_tag_name("textarea")
            if textarea:
                return "Login success"
        except:
            pass
        
        time.sleep(5)
        #this is to verify when chatGPT websites asks for verification
        try:
            verify_human = driver.find_element_by_tag_name("input")
            verify_human.click()
            break
        except Exception as e:
            print(e)

        time.sleep(5)
        try:
            verify_human = driver.find_element_by_class_name("mark")
            verify_human.click()
            break
        except Exception as e:
            print(e)
        count += 1
        driver.refresh()
        time.sleep(5)

    time.sleep(5)
    #This is to look for login button and click on it
    while True:
        try:
            login_button = driver.find_element_by_tag_name("button")
            login_button.click()
            break
        except Exception as e:
            print(e)
            time.sleep(10)
            driver.refresh()

    time.sleep(5)
    q = 0
    while True:
        if q > 2:
            break
        try:
            login_button = driver.find_element_by_tag_name("button")
            login_button.click()
            break
        except Exception as e:
            print("did not find login button")
            q += 1
            time.sleep(5)
            driver.refresh()

    #looks for login with google button and clicks
    while True:
        try:
            login_with_google = driver.find_elements_by_tag_name("button")
            print(len(login_with_google))
            #this will click the 2nd button in the list. Since 2nd is the login with google button.
            login_with_google[1].click()
            break
        except Exception as e:
            print(e)

    time.sleep(10)
    while True:
        try:
            email = driver.find_element_by_name("identifier").send_keys("YOUR_GMAIL_ID_HERE")
            ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
            time.sleep(5)
            passwd = driver.find_element_by_name("password").send_keys("YOUR_GMAIL_PASSWORD_HERE")
            ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
            break
        except Exception as e:
            print(e)
    #app.config['LOGGER'] = driver
    time.sleep(5)
    time.sleep(5)
    #clicks the next buttons on chatgpt
    while True:
        try:
            driver.find_element_by_class_name("btn-neutral").click()
            time.sleep(1)
            driver.find_elements_by_class_name("btn-neutral")[1].click()
            time.sleep(1)
            driver.find_element_by_class_name("btn-primary").click()
            time.sleep(1)
            break
        except Exception as e:
            print(e)

    #app.config['LOGGER'] = driver
    #os.environ['DRIVER'] = driver
    global driver_new
    driver_new = driver
    return "Login Success!!"


@app.route("/requestChatGPT")
def chatgpt():
    try:
        #display.Display(visible=0, size=(500,500)).start()
        #query = st.text_input("Enter your query","")
        #if query.lower() == "exit":
        #query = str(input("Enter your query:"))
        print(os.getppid())
        #driver = os.environ.get('DRIVER')
        driver = driver_new
        #driver = app.config['LOGGER']
        query = request.args.get('q')
        print(query)
        textarea = driver.find_element_by_tag_name("textarea")
        print("debug 1")
        textarea.send_keys(query)
        print("debug 2")
        ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        #st.text("generating response...")
        print("debug 3")
        time.sleep(5)
        resp = ""
        while True:
            response = driver.find_elements_by_class_name("markdown")
            print("------Response------")
            print("\n"+response[-1].text)
            print("\n\n")
            if resp == response[-1].text:
                break
            else:
                resp = response[-1].text
                time.sleep(3)
            
        #st.write(response[-1].text)
        return resp
    except Exception as e:
        print(e)
        return "Somthing went wrong!!"


'''if __name__ == "__main__":'''
app.run(debug=True,)

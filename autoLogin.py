# MailAutoLogin

from selenium import webdriver
from time import sleep


while True:
    print("Choose the mail you want to log in, type 'qq' or '163'")
    print('The mail you want to choose is:')
    mail = input()
    if mail in ['qq', '163']:
        break
    print("Sorry, there is no such an account!\nPlease enter 'qq' or '163'\n")

browser = webdriver.Chrome()
# browser.maximize_window()  # 可有可无


if mail == 'qq':
    try:
        browser.get('http://mail.qq.com/')

        browser.switch_to.frame(browser.find_element_by_id('login_frame'))
        # browser.switch_to.frame('login_frame')  # It's OK!
        # 登录的操作标签在某一个frame内，所以在进行访问元素的时候要先转到相应的frame

        browser.find_element_by_id('u').clear()
        browser.find_element_by_id('u').send_keys('wangkx0105@qq.com')
        browser.find_element_by_id('p').clear()
        browser.find_element_by_id('p').send_keys('WKX299792458QQ')
        sleep(2)
        browser.find_element_by_id('login_button').click()
        # browser.find_element_by_id('login_button').submit()报错！！！

        print('log in ...')
        print('--------------')

        sleep(2)
        # browser.find_element_by_css_selector('#composebtn').click()
        browser.find_element_by_id('composebtn').click()
        # 以上两种访问方式都可以
        sleep(2)

        browser.switch_to.frame('mainFrame')
        # browser.refresh()
        '''
        # browser.find_element_by_css_selector("input[class='js_input']").\
        #     send_keys('wangkx0105@outlook.com')
        # browser.find_element_by_css_selector("#addr_text>input[class='js_input']").\
        #     send_keys('wangkx0105@outlook.com')
        这些方法不行，shit！！！！！
        '''
        browser.find_element_by_id('toAreaCtrl').find_element_by_class_name('js_input').\
            send_keys('wangkx0105@outlook.com')  # 收件人 肯定有更简单的方法
        browser.find_element_by_id('subject').send_keys('test')  # 主题

        browser.switch_to.frame(browser.find_element_by_class_name('qmEditorIfrmEditArea'))  # switch frame

        browser.find_element_by_css_selector("body[contenteditable='true']").send_keys('secret test!')  #邮件正文

        browser.switch_to.parent_frame()
        # browser.switch_to.default_content()  # failed
        '''
        注意切换frame,在使用switch时注意方法的选择
        driver.switch_to.frame(reference)
        driver.switch_to.parent_frame()
        driver.switch_to.default_content()
        注意灵活运用
        
        学习网站：
        http://blog.csdn.net/huilan_same/article/details/52200586
        http://www.cnblogs.com/qingchunjun/p/4208159.html
        '''

        sleep(2)

        browser.find_element_by_xpath("//*[@id='toolbar'][@class='clear']/div/a[1]").click()
        # xpath的使用方法


    except ValueError:
        print('something went wrong with qq email!')

else:
    try:
        browser.get('http://mail.163.com/')

        sleep(2)
        browser.switch_to.frame('x-URS-iframe')
        browser.find_element_by_name('email').clear()
        browser.find_element_by_name('password').clear()

        browser.find_element_by_name('email').send_keys('prettybug125')
        browser.find_element_by_name('password').send_keys('a19841984*')

        # browser.find_element_by_name('email').send_keys('wangkx0105')
        # browser.find_element_by_name('password').send_keys('******')

        browser.find_element_by_css_selector('#dologin').click()  # 登录
        print('log in ...')
        print('--------------')

        sleep(3)
        browser.find_element_by_id('_mail_component_68_68').click()
        sleep(1)
        browser.find_element_by_class_name('nui-editableAddr-ipt').\
            send_keys('wangkx0105@outlook.com')  # 收件人
        browser.find_element_by_css_selector("input[id$='_subjectInput']").\
            send_keys('auto mail test')  # 邮件主题

        # browser.switch_to.frame('APP-editor-iframe')  # 此切换Failed!!!
        browser.switch_to.frame(browser.find_element_by_class_name('APP-editor-iframe'))  # switch frame

        browser.find_element_by_class_name('nui-scroll').send_keys('secret test!')  #邮件正文

        browser.switch_to.default_content()  # 注意切换frame

        sleep(2)
        browser.find_element_by_css_selector("div.js-component-button.nui-mainBtn.nui-btn.nui-btn-hasIcon.nui-mainBtn-hasIcon").\
            click()


    except ValueError:  # 可以修改
        print('Something went wrong with 163mail!')


# browser.close()

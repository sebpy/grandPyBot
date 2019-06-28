from splinter import Browser


URL = 'http://localhost:5000'



def test_app():
    browser = Browser()
    browser.visit(URL)
    assert browser.is_text_present('Bonjour !')
browser.quit()

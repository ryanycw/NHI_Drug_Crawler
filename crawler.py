from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

class Drug:
    def __init__(self, drug_names):
        self.drug_names = drug_names

    def ATC_code(self,):

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get("https://www.nhi.gov.tw/QueryN/Query1.aspx")

        result = []
        for drug_name in self.drug_names:
            print(drug_name)
            drug = browser.find_element_by_name("ctl00$ContentPlaceHolder1$tbxElementName")
            drug.clear()
            drug.send_keys(drug_name)

            select_mix = Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$ddlMixture"))
            select_mix.select_by_value("N")

            history = browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rblType_1"]') # history = browser.find_element_by_name("ctl00$ContentPlaceHolder1$rblType") 有問題因為上下兩個 radio 的 name 一樣
            history.click()
            
            submit = browser.find_element_by_name("ctl00$ContentPlaceHolder1$btnSubmit")
            submit.click()

            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "lxml")
            table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvQuery1Data"})
            elements = table.find_all("td", attrs={'style':'width:8%;'})
            data = (drug_name,) + tuple(element.getText() for element in elements)
                    
            result.append(data)

        print(result)

if __name__ == "__main__":
    drug_name = ['Paracetamol', 'HYDROXYUREA']
    search = Drug(drug_name)
    search.ATC_code()
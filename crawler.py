from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

class Drug:
    def __init__(self, drug_names):
        self.drug_names = drug_names

    def ATC_code(self,):

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get("https://www.nhi.gov.tw/QueryN/Query1.aspx")

        result = 'drug_id' + ',' + 'drug_name_en' + ',' + 'drug_name_zh' + ',' + 'ingre' + ',' + 'ingre_unit' + ',' + \
                 'stand_unit' + ',' + 'mixture' + ',' + 'sales' + ',' + 'form' + ',' + 'classify_code' + ',' + 'class_gr_name' + ',' + 'act_code'

        for drug_name in self.drug_names:
            result += '\n' + drug_name + ','
            drug_name_en_list, drug_name_zh_list, ingre_list, ingre_unit_list, stand_unit_list, mixture_list, sales_list, form_list, \
            classify_code_list, class_gr_name_list, act_code_list = set(), set(), set(), set(), set(), set(), set(), set(), set(), set(), set()
            all_data = [drug_name_en_list, drug_name_zh_list, ingre_list, ingre_unit_list, stand_unit_list, mixture_list, sales_list, form_list, classify_code_list, class_gr_name_list, act_code_list]
            try:
                print(drug_name)
                drug = browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_tbxQ1ID"]')
                drug.clear()
                drug.send_keys(drug_name)

                select_mix = Select(browser.find_element_by_name("ctl00$ContentPlaceHolder1$ddlMixture"))
                select_mix.select_by_value("N")

                history = browser.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rblType_1"]') # history = browser.find_element_by_name("ctl00$ContentPlaceHolder1$rblType") 有問題因為上下兩個 radio 的 name 一樣
                history.click()
                
                submit = browser.find_element_by_name("ctl00$ContentPlaceHolder1$btnSubmit")
                submit.click()

                time.sleep(1)
                
                soup = BeautifulSoup(browser.page_source, "lxml")
                table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvQuery1Data"})
                if table != None:
                    rows = table.find_all("tr")
                    for i, row in enumerate(rows):
                        if i != 0:
                            drug_id = row.find("td", recursive=False).findNext("td")
                            drug_name_en = drug_id.findNext("td")
                            drug_name_en_list.add(drug_name_en.find("span").getText())
                            drug_name_zh = drug_name_en.findNext("td")
                            drug_name_zh_list.add(drug_name_zh.find("span").getText())
                            ingre = drug_name_zh.findNext('td')
                            ingre_list.add(ingre.getText().strip())
                            ingre_unit = ingre.findNext('td')
                            ingre_unit_list.add(ingre_unit.getText().strip())
                            stand_unit = ingre_unit.findNext('td')
                            stand_unit_list.add(stand_unit.find("span").getText())
                            mixture = stand_unit.findNext('td')
                            mixture_list.add(mixture.find("span").getText())
                            sales = mixture.findNext('td').findNext('td').findNext('td')
                            sales_list.add(sales.find("span").getText())
                            form = sales.findNext('td')
                            form_list.add(form.find("span").getText())
                            classify_code = form.findNext('td')
                            classify_code_list.add(classify_code.find("span").getText())
                            class_gr_name = classify_code.findNext('td')
                            class_gr_name_list.add(class_gr_name.find("span").getText())
                            act_code = class_gr_name.findNext('td')
                            act_code_list.add(act_code.getText())

                    for data in all_data:
                        if len(data) == 1:
                            result += "".join(map(str,data)) + ','
                        else:
                            text = ""
                            for i in range(len(data)):
                                text += " ".join(map(str,data))
                            result += text + ','

                    result = result[:-1]
                
            except Exception as e:
                if e == TimeoutException:
                    print(e)
                    result += 'Time Out'
                else:
                    print(e)
                    result += 'Not Found'

        return result

def main():
    drug_list = pd.read_csv("outpatient_drug_id.csv")
    search = Drug(list(drug_list["drug_id"]))
    result = search.ATC_code()
    f = open('Drug_ActCode.csv','w')
    f.write(result)
    f.close()

if __name__ == "__main__":
    main()
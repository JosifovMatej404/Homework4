from datetime import datetime
from Models import Company,CompanyData
from Scraper import SeleniumWorker
from Data.db_functions import add_company,insert_company_data,get_company_data_by_code,insert_company_data_object,add_company_object
#worker = SeleniumWorker()
#worker.fetch_data_with_dates_and_key("01.01.2023", "31.12.2023", "alkb")
#print(obj.text + "\n" for obj in worker.web_objects)

date_string = '2024-12-25'
date_format = "%Y-%m-%d"

# Specify the format of the input date string

#date_object = datetime.strftime(date_string,date_format).date()


#add_company("ALKB","12.24.2024")
#insert_company_data("GRSN",date_string,125.5,1232.5,12325.5,12323.5,12.23,12,12,12)


#companiesObject = get_company_data_by_code("ALK")
#for company in companiesObject:
    #print(company.code,company.last_update)


#company = Company("SSNN","12.24.2024")

#company_record = CompanyData("ABDD",date_string,125.5,1232.5,12325.5,12323.5,12.23,12,12,12)


#insert_company_data_object(company_record)
#add_company_object(company)
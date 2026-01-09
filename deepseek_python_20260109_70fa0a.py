import requests
from datetime import datetime
import xml.etree.ElementTree as ET

def get_key_rate_simple(date_str):
    """Простая версия через SOAP API"""
    
    soap_request = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
               xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <KeyRateXML xmlns="http://www.cbr.ru">
      <fromDate>2013-09-13</fromDate>
      <ToDate>{date_str}</ToDate>
    </KeyRateXML>
  </soap:Body>
</soap:Envelope>'''
    
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': 'http://www.cbr.ru/KeyRateXML'
    }
    
    try:
        response = requests.post(
            'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx',
            data=soap_request,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            # Поиск последней ставки в ответе
            namespaces = {
                'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
                'm': 'http://www.cbr.ru'
            }
            
            key_rates = root.findall('.//m:KeyRate', namespaces)
            if key_rates:
                # Берем последнюю ставку (самую свежую)
                last_rate = key_rates[-1]
                rate_elem = last_rate.find('m:Rate', namespaces)
                if rate_elem is not None:
                    return float(rate_elem.text)
        
        return None
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

# Пример использования
date_input = input("Введите дату (ГГГГ-ММ-ДД): ")
rate = get_key_rate_simple(date_input)
if rate:
    print(f"Ключевая ставка на {date_input}: {rate}%")
else:
    print("Не удалось получить данные")
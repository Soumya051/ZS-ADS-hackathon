import regex as re

class Extractor:

    def __init__(self, query):
        self.query = query

    def extract_order_details(self):
        
        result = {}
        order_pattern = r"ORD-[0-9]{5}"
        match = re.search(order_pattern, self.query, flags=re.IGNORECASE)
        if match:
            order_id = match.group().upper()
            result['order_id'] = order_id
        
        tracking_pattern = r"TRACK-([0-9A-Z]){6}"
        match = re.search(tracking_pattern, self.query, flags=re.IGNORECASE)
        if match:
            tracking_id = match.group().upper()
            result['tracking_id'] = tracking_id

        return result
    
    def extract_customer_details(self):

        result = {}
        customer_pattern = r"CUST-[0-9]{3}"
        match = re.search(customer_pattern, self.query, flags = re.IGNORECASE)
        if match:
            customer_id = match.group()
            result['customer_id'] = customer_id

        phone_pattern = r"(\+91)?(\+91-)?[0-9]{10}"
        match = re.search(phone_pattern, self.query, flags=re.IGNORECASE)
        if match:
            phone = match.group()
            result['phone'] = phone

        email_pattern = r"\b[A-Z0-9._%+-]+@[A-Z0-9-]+(\.[A-Z]{2,}){1,2}\b"
        match = re.search(email_pattern, self.query, flags=re.IGNORECASE)
        if match:
            email = match.group()
            result['email'] = email

        case_pattern = r"CASE-[A-Z0-9]{6}"
        match = re.search(case_pattern, self.query, flags=re.IGNORECASE)
        if match:
            case_id = match.group()
            result['case_id'] = case_id

        return result
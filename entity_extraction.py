import regex as re

class Extractor:

    def extract_order_details(text):
        
        order_pattern = r"ORD-[0-9]{5}"
        match = re.search(order_pattern, text, flags=re.IGNORECASE)
        order_id = match.group().upper()
        
        tracking_pattern = r"TRACK-([0-9A-Z]){6}"
        match = re.search(tracking_pattern, text, flags=re.IGNORECASE)
        tracking_id = match.group().upper()

        return {'order_id': order_id, 'tracking_id': tracking_id}
    
    def extract_customer_details(text):

        customer_pattern = r"CUST-[0-9]{3}"
        match = re.search(customer_pattern, text, flags = re.IGNORECASE)
        customer_id = match.group()

        phone_pattern = r"(\+91)?(\+91-)?[0-9]{10}"
        match = re.search(phone_pattern, text, flags=re.IGNORECASE)
        phone = match.group()

        case_pattern = r"CASE-[A-Z0-9]{6}"
        match = re.search(case_pattern, text, flags=re.IGNORECASE)
        case_id = match.group()

        return {'customer_id': customer_id, 'phone': phone, 'case_id': case_id}
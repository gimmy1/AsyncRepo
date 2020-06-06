import json
import os

from settings import GELATO_KEY
G_HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": GELATO_KEY
}
def return_order(country, addr_one, addr_two, state, city, postcode):
    return {
		"order": {
			"orderReferenceId": "20a26b30-3896-11ea-a2ba-acde48001122",
			"customerReferenceId": "20a26b30-3896-11ea-a2ba-acde48001122",
			"currencyIsoCode": "USD"
		},
		"recipient": {
			"countryIsoCode": f"{country}",
			"companyName": "Maxim Integrated Products Inc",
			"firstName": "Gamal",
			"lastName": "Ali",
			"addressLine1": f"{addr_one}",
			"addressLine2": f"{addr_two}",
			"stateCode": f"{state}",
			"city": f"{city}",
			"postcode": f"{postcode}",
			"email": "gamalali@carveredison.com"
		},
		"products": [{
			"itemReferenceId": "postcard03-848-6795",
			"productUid": "cards_pf_a6_pt_130-lb-cover-coated-silk_cl_4-4_ct_matt-protection_prt_1-1_hor",
			"pdfUrl": "https://carveredison-carbon-dev.s3.amazonaws.com/company/maxim-integrated-products-inc/materials/espp/pdf/maximintegratedproductsinccampaign1/postcard3.pdf?AWSAccessKeyId=AKIAT2QF3VULL6M2W6LR&Signature=TirCpFPXhQxdjG%2BFt69wz03EIZE%3D&Expires=1579203103",
			"quantity": 1
		}]
	}

def return_order_2():
	return {
        "order": {
            "orderReferenceId": "123456",
            "customerReferenceId": "12345678}",
            "currencyIsoCode": "USD"
        },
        "recipient": {
             "countryIsoCode": "US",
             "companyName": "Example",
             "firstName": "Paul",
             "lastName": "Smith",
             "addressLine1": "451 Clarkson Ave",
             "addressLine2": "Brooklyn",
             "stateCode": "NY",
             "city": "New York",
             "postcode": "11203",
             "email": "gamalali@carveredison.com",
             "phone": "123456789"
         },
        "products": [
            {
                "itemReferenceId": "393939393",
                "productUid": "cards_pf_bx_pt_110-lb-cover-uncoated_cl_4-4_hor",
                "pdfUrl": "https://s3-eu-west-1.amazonaws.com/developers.gelato.com/product-examples/test_print_job_BX_4-4_hor_none.pdf",
                "quantity": 100
            }
        ]
    }
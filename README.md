# test_amazon

this is a gift card auto claim program :

##endponit and what they do:

- the first endpoint is /user, it accept post method, here you create a user in the platform. the body for this endpoint :
{
    "email": "",
    "password": "",
    "zip_code": "",
    "phone_number": ""
}

- the second endpoint is :/redeem this endpoint accept a post method, here you can claim aws code, the body for this is:
{
    "email":"",
    "code":""
}


- the third endpoint is /user-code here you can check what codes a user had been used and the state of the claim, the body is :
{
    "email":"",
    
}

- the last one is /code here you can see all the codes that have been used and the state of those.

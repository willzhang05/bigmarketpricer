case "$1" in 
	login)
		curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{  "emailId": "dylanjones2011@gmail.com",  "password": "4foPaNW7EJ2TzA8a",  "loggedIn": true}' 'https://www.bigparser.com/APIServices/api/common/login' | grep -oP "(?<=\"authId\":\").{36}"
		;;
	get)
		curl -s -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'authId:'"$(sh request.sh login)"'' -d '{"gridId":"58d772aa478af70572b6106a","rowCount":1,"tags":[{"columnValue":"'"$2"'","columnStoreName":"0"}]}' 'https://www.bigparser.com/APIServices/api/query/table'
		;;
	*)
		echo "BAD ARGS"
		exit -1
		;;
esac

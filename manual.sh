#/bin/sh

APPNAME=$(curl "http://generator.cocsfe01.demo.yandex.net/")
PROFILE=$APPNAME-profile
GROUP=$APPNAME-group

echo "
# Step-By-Step
## Create application and Deploy

# 1
git clone https://github.com/noxiouz/cocaine-laboratory.git

# 2
cocaine-tool profile upload --name $PROFILE --profile profile.json --host cocsfe01.demo.yandex.net --timeout=10

# 3
cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name $APPNAME --timeout 20000 --host cocsfe01.demo.yandex.net

# 4
cocaine-tool app restart --name $APPNAME --profile $PROFILE --host cocsbe01.demo.yandex.net --timeout=200
cocaine-tool app restart --name $APPNAME --profile $PROFILE --host cocsbe02.demo.yandex.net --timeout=200

# 5
curl -v http://$APPNAME.cocsfe01.demo.yandex.net


## Routing groups and rolling update
# 6.
cocaine-tool group list --host cocsfe01.demo.yandex.net

# 7.
cocaine-tool group create $GROUP '{\"$APPNAME\": 1}' --host cocsfe01.demo.yandex.net
cocaine-tool group refresh --host cocsfe01.demo.yandex.net

# 8
curl -v http://$GROUP.cocsfe01.demo.yandex.net

# 9
cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name $APPNAME-version2 --timeout 20000 --host cocsfe01.demo.yandex.net

# 10
cocaine-tool app restart --name $APPNAME-version2 --profile $PROFILE --host cocsbe01.demo.yandex.net --timeout=200
cocaine-tool app restart --name $APPNAME-version2 --profile $PROFILE --host cocsbe02.demo.yandex.net --timeout=200

# 11
curl -v http://$APPNAME-version2.cocsfe01.demo.yandex.net

# 12
cocaine-tool group push $GROUP $APPNAME-version2 1 --host cocsfe01.demo.yandex.net

# 13
cocaine-tool group view $GROUP --host cocsfe01.demo.yandex.net
cocaine-tool group refresh --host cocsfe01.demo.yandex.net
" > MANUAL.md

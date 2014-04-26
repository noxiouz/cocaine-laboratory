#/bin/sh

APPNAME=$(curl "http://generator.cocsfe01.demo.yandex.net/")
PROFILE=$APPNAME-profile
GROUP=$APPNAME-group
HEADER="#/bin/sh"

# Step-By-Step
## Create application and Deploy

echo "$HEADER
# 1. Clone repository
git clone https://github.com/noxiouz/cocaine-laboratory.git
" > step01_clone_repository.sh

echo "$HEADER
# 2. Upload application profile
cocaine-tool profile upload --name $PROFILE --profile profile.json --host cocsfe01.demo.yandex.net --timeout=10
" > step02_upload_profile.sh

echo "$HEADER
# 3. Upload application code
cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name $APPNAME --timeout 20000 --host cocsfe01.demo.yandex.net
" > step03_upload_application.sh

echo "$HEADER
# 4. Start application
cocaine-tool app restart --name $APPNAME --profile $PROFILE --host cocsbe01.demo.yandex.net --timeout=200
cocaine-tool app restart --name $APPNAME --profile $PROFILE --host cocsbe02.demo.yandex.net --timeout=200
" > step04_restart_app_version1.sh

echo "$HEADER
# 5
curl -v http://$APPNAME.cocsfe01.demo.yandex.net
" > step05_test_app_version1.sh

## Routing groups and rolling update

echo "$HEADER
# 6. List routing groups
cocaine-tool group list --host cocsfe01.demo.yandex.net
" > step06_list_routing_groups.sh

echo "$HEADER
# 7. Create routing group $GROUP
cocaine-tool group create $GROUP '{\"$APPNAME\": 1}' --host cocsfe01.demo.yandex.net
cocaine-tool group refresh --host cocsfe01.demo.yandex.net
" > step07_create_routing_group.sh

echo "$HEADER
# 8. Test application via group url
curl -v http://$GROUP.cocsfe01.demo.yandex.net
" > step08_test_app_via_group_url.sh

echo "$HEADER
# 9. Upload application version2
cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name $APPNAME-version2 --timeout 20000 --host cocsfe01.demo.yandex.net
" > step09_upload_app_version2.sh

echo "$HEADER
# 10. Start application version2
cocaine-tool app restart --name $APPNAME-version2 --profile $PROFILE --host cocsbe01.demo.yandex.net --timeout=200
cocaine-tool app restart --name $APPNAME-version2 --profile $PROFILE --host cocsbe02.demo.yandex.net --timeout=200
" > step10_start_app_version2.sh

echo "$HEADER
# 11. Test version2 of application
curl -v http://$APPNAME-version2.cocsfe01.demo.yandex.net
" > step11_test_app_version2.sh

echo "$HEADER
# 12. Add version2 to routing group
cocaine-tool group push $GROUP $APPNAME-version2 1 --host cocsfe01.demo.yandex.net
" > step12_add_version2_to_routing.sh

echo "$HEADER
# 13. Refresh routing group configuration
cocaine-tool group view $GROUP --host cocsfe01.demo.yandex.net
cocaine-tool group refresh --host cocsfe01.demo.yandex.net
" > step13_refresh_group_configuration.sh

echo "$HEADER
# 14. Test application via group url
curl -v http://$GROUP.cocsfe01.demo.yandex.net
" > step14_test_app_via_group_url.sh

chmod a+x step*.sh

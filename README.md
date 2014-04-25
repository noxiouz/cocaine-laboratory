# Step-By-Step

## Create application and Deploy

1. git clone https://github.yandex-team.ru/noxiouz/cocaine-lab.git
2. cocaine-tool profile upload --name cocaine-lab-profile --profile profile.json --host cocsfe01.demo.yandex.net --timeout=10
3. cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name cocaine-lab --timeout 20000 --host cocsfe01.demo.yandex.net
4. cocaine-tool app restart --name cocaine-lab --profile cocaine-lab-profile --host cocsbe01.demo.yandex.net --timeout=200
5. cocaine-tool app restart --name cocaine-lab --profile cocaine-lab-profile --host cocsbe02.demo.yandex.net --timeout=200
6. curl -v http://cocaine-lab.cocsfe01.demo.yandex.net


## Routing groups and rolling update
1. cocaine-tool group list --host cocsfe01.demo.yandex.net
2. cocaine-tool group create cocaine-lab-group '{"cocaine-lab": 1}' --host cocsfe01.demo.yandex.net
3. cocaine-tool group refresh --host cocsfe01.demo.yandex.net
4. curl -v http://cocaine-lab-group.cocsfe01.demo.yandex.net
5. cocaine-tool app upload --docker=http://cocsfe01.demo.yandex.net:5432 --registry=cocsfe01.demo.yandex.net:5000 --manifest manifest.json --name cocaine-lab-version2 --timeout 20000 --host cocsfe01.demo.yandex.net
6. cocaine-tool app restart --name cocaine-lab-version2 --profile cocaine-lab-profile --host cocsbe01.demo.yandex.net --timeout=200
6. cocaine-tool app restart --name cocaine-lab-version2 --profile cocaine-lab-profile --host cocsbe02.demo.yandex.net --timeout=200
7. curl -v http://cocaine-lab-version2.cocsfe01.demo.yandex.net
8. cocaine-tool group push cocaine-lab-group cocaine-lab-version2 1 --host cocsfe01.demo.yandex.net
9. cocaine-tool group view cocaine-lab-group --host cocsfe01.demo.yandex.net
10. cocaine-tool group refresh --host cocsfe01.demo.yandex.net

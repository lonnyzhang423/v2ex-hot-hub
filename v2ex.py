import sys
import time

import requests

HOT_URL = "https://www.v2ex.com/api/topics/hot.json"


def version():
    print("python version")
    print(sys.version)


def getJsonArray():
    try:
        r = requests.get(HOT_URL)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(e.strerror)


def parseItemInfo(item):
    info = {}
    info['id'] = item['id']
    info['title'] = item['title']
    info['content'] = item['content']
    info['url'] = item['url']
    return info

def generateReadme(items):
    pass

def main():
    items = []
    for _ in range(3):
        # 重试3次
        arr = getJsonArray()
        if arr:
            for i in range(len(arr)):
                info = parseItemInfo(arr[i])
                items.append(info)
            break
        time.sleep(3)


if __name__ == "__main__":
    version()
    main()

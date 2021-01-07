import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import AnyStr

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)

HOT_URL = "https://www.v2ex.com/api/topics/hot.json"

retries = Retry(total=2,
                backoff_factor=0.1,
                status_forcelist=[k for k in range(400, 600)])


def getJsonArray():
    try:
        with requests.session() as s:
            s.mount("http://", HTTPAdapter(max_retries=retries))
            s.mount("https://", HTTPAdapter(max_retries=retries))
            return s.get(HOT_URL).json()
    except RequestException as e:
        log.warning("request failed:%r", e)


def parseItemInfo(item):
    info = {}
    info['id'] = item['id']
    info['title'] = item['title']
    info['content'] = item['content']
    info['url'] = item['url']
    return info


def currentTimeStr():
    return datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z')


def currentDateStr():
    return datetime.now().astimezone().strftime('%Y-%m-%d')


def ensureDir(file):
    directory = os.path.abspath(os.path.dirname(file))
    if not os.path.exists(directory):
        os.makedirs(directory)


def writeText(file: str, text: AnyStr):
    ensureDir(file)
    with open(file, 'w') as f:
        f.write(text)


def generateArchiveReadme(items):
    """生成归档readme
    """
    def topic(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    topics = '暂无数据'
    if items:
        topics = '\n'.join([topic(item) for item in items])

    date = '# '+currentDateStr()+'\n'
    now = currentTimeStr()
    lastUpdate = '```最后更新时间：{}```'.format(now)+'\n'

    readme = '\n'.join([date, lastUpdate, topics])
    return readme


def generateTodayReadme(items):
    """生成今日readme
    """
    def topic(item):
        return '1. [{}]({})'.format(item['title'], item['url'])

    topics = '暂无数据'
    if items:
        topics = '\n'.join([topic(item) for item in items])

    readme = ''
    with open('README_template.md', 'r') as f:
        readme = f.read()

    timeInfo = '```更新时间：{}```'.format(currentTimeStr())
    readme = readme.replace("<!-- update time -->", timeInfo)
    readme = readme.replace("<!-- topics -->", topics)

    return readme


def handleTodayMd(md):
    log.info('today md:%s', md)
    writeText('README.md', md)


def handleArchiveMd(md):
    log.info('archive md:%s', md)
    name = currentDateStr()+'.md'
    file = os.path.join('archives', name)
    writeText(file, md)


def handleRawJson(json: str):
    log.info('raw json:%s', json)
    name = currentDateStr()+'.json'
    file = os.path.join('raw', name)
    writeText(file, json)


def run():
    items = None
    # 获取数据
    arr = getJsonArray()
    if arr:
        items = [parseItemInfo(item) for item in arr]

    if items:
        # 最新数据
        todayMd = generateTodayReadme(items)
        handleTodayMd(todayMd)
        # 归档
        archiveMd = generateArchiveReadme(items)
        handleArchiveMd(archiveMd)
        # 原始数据
        raw = json.dumps(arr, ensure_ascii=False)
        handleRawJson(raw)


if __name__ == "__main__":
    run()

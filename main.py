import json
import os
import traceback

import util
from util import logger
from v2ex import V2ex


def generateArchiveMd(items):
    """生成归档readme
    """
    def topic(item):
        title = item['title']
        url = item['url']
        return '1. [{}]({})'.format(title, url)

    topicMd = '暂无数据'
    if items:
        topicMd = '\n'.join([topic(item) for item in items])

    md = ''
    file = os.path.join('template', 'archive.md')
    with open(file) as f:
        md = f.read()

    now = util.current_time()
    md = md.replace("{updateTime}", now)
    md = md.replace("{topics}", topicMd)

    return md


def generateReadme(items):
    """生成今日readme
    """
    def topic(item):
        title = item['title']
        url = item['url']
        return '1. [{}]({})'.format(title, url)

    topicMd = '暂无数据'
    if items:
        topicMd = '\n'.join([topic(item) for item in items])

    readme = ''
    file = os.path.join('template', 'README.md')
    with open(file) as f:
        readme = f.read()

    now = util.current_time()
    readme = readme.replace("{updateTime}", now)
    readme = readme.replace("{topics}", topicMd)

    return readme


def saveReadme(md):
    logger.debug('today md:%s', md)
    util.write_text('README.md', md)


def saveArchiveMd(md):
    logger.debug('archive md:%s', md)
    name = util.current_date()+'.md'
    file = os.path.join('archives', name)
    util.write_text(file, md)


def saveRawResponse(content: str):
    logger.debug('raw content:%s', content)
    name = util.current_date()+'.json'
    file = os.path.join('raw', name)
    util.write_text(file, content)


def run():
    # 获取数据
    v2ex = V2ex()
    topics, resp = v2ex.get_hot_topic()
    if resp:
        # 原始数据
        text = json.dumps(json.loads(resp.text), ensure_ascii=False)
        saveRawResponse(text)

    # 最新数据
    readme = generateReadme(topics)
    saveReadme(readme)
    # 归档
    archiveMd = generateArchiveMd(topics)
    saveArchiveMd(archiveMd)


if __name__ == "__main__":
    run()

# coding = utf-8
import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import os
import time
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.type.ttypes import NoteSortOrder
import re

def format_url(url):
    return "<a href='" + url + "'>" + url + "</a>"

def add_to_note(title, newline):# 需输入笔记标题和需要添加的内容
    # auth_token申请地址：https://dev.yinxiang.com/doc/articles/dev_tokens.php
    auth_token = "your token"
    # 关掉沙盒模式
    sandbox = False# True代表使用的国内的印象笔记，而不是Evernote国际版
    china = True
    # 创建一个印象笔记client对象
    client = EvernoteClient(token = auth_token, sandbox = sandbox, china = china)
    # user_store = client.get_user_store()
    # 通过client对象获取note_store对象
    note_store = client.get_note_store()
    # # 下面代码为了获取所有的笔记本数量、笔记本名和对应的GUID，目前是注释状态，为了找到对应的笔记本GUID
    # notebooks = note_store.listNotebooks()
    # print("Found", len(notebooks), " notebooks:")
    # for notebook in notebooks:
    #     print(notebook.name, notebook.guid)
    
    notebookGuid="笔记本的GUID" # api笔记本
    # 生成查找笔记的规则，使用笔记创建排序，指定笔记本GUID为api笔记本，使用标题名搜索
    updated_filter = NoteFilter(order=NoteSortOrder.CREATED, notebookGuid=notebookGuid, words=title)
    # 偏移0
    offset = 0
    # 只取一条笔记
    max_notes = 1
    # 查找出符合条件的笔记
    result_list = note_store.findNotes(updated_filter, offset, max_notes)
    # # 如果找到对应笔记则，在这个笔记里加一条，否则创建一条新笔记加进去
    if result_list.totalNotes:
        # 获取找到笔记的GUID
        note_guid = result_list.notes[0].guid
        # 获取到对应笔记
        note = note_store.getNote(note_guid,1,1,1,1)
        # 使用正则匹配出笔记里的内容文本
        match_res = re.search(r'<en-note>(.*)<\/en-note>', note.content, re.M|re.I)
        # 如果能匹配到内容，则获取内容设置变量名为old_content，否则old_content为空
        if match_res:
            old_content = match_res.group(1)
        else:
            old_content = ""
        # 构建待更新的笔记内容
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
                        '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>' + newline + '<br/>' + old_content # 将新内容添加在最前
        note.content += '</en-note>'
        
        res = note_store.updateNote(auth_token, note)
        print(note.title + "添加成功，GUID： ", note.guid)
    # 没有找到旧的笔记，则新建一个
    else:
        # 创建note对象
        note = Types.Note()
        # 设置笔记名称
        note.title = title
        # 读取evenote.txt里的内容
        
        # 构建note的内容，把句子加到<en-note>标签中
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
                        '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>' + newline
        note.content += '</en-note>'
        # 指定笔记本GUID
        note.notebookGuid = notebookGuid
        # 创建笔记
        created_note = note_store.createNote(note)
        # 打印创建好的笔记标题和GUID
        print(note.title + "创建成功，GUID： ", created_note.guid)
 
# if __name__ == '__main__':
    # #############
    # note_title = 'test log'
    # newline = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) + ' say hi ;) ' + format_url('https://github.com/guu120')
    # add_to_note(note_title, newline)
    # ##############
 

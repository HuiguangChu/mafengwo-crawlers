#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import re
from models import Dest
from httper import Httper

class MainDestCtrl(object):
    """docstring for MainDestCtrl"""
    def __init__(self):
        super(MainDestCtrl, self).__init__()
        self.url = 'http://www.mafengwo.cn/mdd/'

    def save_pvc_dest_list(self, dest_id_name):
        for dest in dest_id_name:
            md_id = re.findall('\d+', dest[0])
            print(dest)
            if md_id:
                dst = Dest.create(
                    dest_id = uuid.uuid4(),
                    name = dest[1],
                    m_dest_id = md_id[0],
                    province = dest[1]
                )

    def save_city_dest_list(self, dest_id_name):
        for dest in dest_id_name:
            md_id = re.findall('\d+', dest[0])
            print(dest)
            if md_id:
                dst = Dest.create(
                    dest_id = uuid.uuid4(),
                    name = dest[1],
                    m_dest_id = md_id[0],
                    city = dest[1]
                )

    def read_pvc_dest_list(self):
        return Dest.select(Dest.dest_id, Dest.province, Dest.m_dest_id).where(Dest.province != '')

    def dest_list(self):
        hr = Httper(
            self.url,
            rtype = 'text',
            dtype = 'pq',
            selector = '.sub-title a',
            attr = 'href'
        )
        hr.request()
        # destination href
        _, dest_href_pvc = hr.get_data()
        # destination name
        _, dest_name_pvc = hr.get_data(attr = 'text')
        _, dest_href_city = hr.get_data(
            selector = '.bd-china > dl:nth-child(1) > dd > ul li a',
            attr = 'href'
        )
        _, dest_name_city = hr.get_data(
            selector = '.bd-china > dl:nth-child(1) > dd > ul li a',
            attr = 'text'
        )
        self.save_pvc_dest_list(zip(dest_href_pvc, dest_name_pvc))
        self.save_city_dest_list(zip(dest_href_city, dest_name_city))


class DestCtrl(object):
    """docstring for DestCtrl"""
    def __init__(self, **kwargs):
        super(DestCtrl, self).__init__()
        # mafengwo mddid
        self.m_dest_id = kwargs.get('m_dest_id', '')
        self.name = kwargs.get('name', '')
        # dest uuid
        self.dest_id = kwargs.get('dest_id', '')
        self.page = 1
        self.total = 2
        self.url = 'http://www.mafengwo.cn/mdd/base/list/pagedata_citylist'

    def base_dest_list(self):
        data = {
            'mddid': self.m_dest_id,
            'page': self.page
        }
        hr = Httper(
            self.url,
            method = 'post',
            data = data,
            rtype = 'json',
            rkey = 'list',
            dtype = 'pq',
            selector = '.item .img a',
            attr = 'data-id'
        )
        # send request
        hr.request()
        # get total page count
        _, self.total = hr.get_data(
            rkey = 'page',
            selector = '.pg-last',
            attr = 'data-page'
        )[0]
        # get destination list
        _, dest_id_list = hr.get_data()
        _, dest_name_list = hr.get_data(
            selector = '.item .title',
            attr = 'text'
        )
        return zip(dest_id_list, dest_name_list)

    def save_dest_list(self, dest_id_name):
        for dest in dest_id_name:
            dst = Dest.create(
                dest_id = uuid.uuid4(),
                name = dest[1],
                m_dest_id = dest[0],
                province = self.dest_name,
                parent_dest_id = self.dest_id
            )

    def dest_list(self):
        while self.page <= self.total:
            dest_id_name = self.base_dest_list()
            self.save_dest_list(dest_id_name)
            self.page += 1
        
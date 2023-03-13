#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 13:55:19 2023

@author: eee
"""
import os

# from functools import wraps

from _pydbs_conn.base_mongo import BaseMongoOperator
from utils.datetime_tools import get_now


class chatOperator(BaseMongoOperator):
    def __init__(self):
        db_name = "maedchen_ai_conv"
        DB_USER = "chatroom_manager"
        MTB_DOMAIN = os.getenv("MTB_DOMAIN")
        MONGO_PASSWD = os.getenv("MONGO_PASSWD_chat")
        MONGO_PORT = 7788
        DB_NAME = db_name
        mongo_uri = f"mongodb://{DB_USER}:{MONGO_PASSWD}@{MTB_DOMAIN}:{MONGO_PORT}/?serverSelectionTimeoutMS=5000&connectTimeoutMS=30000&authSource={DB_NAME}&authMechanism=SCRAM-SHA-256"

        super().__init__(mongo_uri, db_name)

    def _table_dispatch(self):
        # TODO: can change here if we need different chat_id as table identifier
        return "conv_test"

    def is_chat_exist(self, chat_id):
        table_name = self._table_dispatch()
        col = self.conn[table_name]
        return col.find_one({"chat_id": chat_id}) is not None

    def _serialize_messages(self, chat_id, messages):
        ts = get_now()
        d = {
            "update_time": ts,
            "create_time": ts,
            "messages": messages,  ## TODO: maybe JSON serialization problem?
            "chat_id": chat_id,
        }
        return d

    def get_conv(self, chat_id, latest_records=0):
        table_name = self._table_dispatch()
        col = self.conn[table_name]
        data = col.find_one({"chat_id": chat_id})
        if latest_records > 0 and data.get("messages") is not None:
            data["messages"] = data["messages"][:latest_records]
        return data

    def create_one(self, chat_id, messages):
        table_name = self._table_dispatch()
        s_messages = self._serialize_messages(chat_id, messages)
        col = self.conn[table_name]
        col.insert_one(s_messages)
        return

    def update_exist(self, chat_id, messages):
        table_name = self._table_dispatch(chat_id)
        col = self.conn[table_name]
        update = {"update_time": get_now(), "messages": messages}
        col.update_one({"chat_id": chat_id}, {"$set": update})
        return

    def delete_many(self, chat_ids):
        table_name = self._table_dispatch()
        col = self.conn[table_name]
        col.delete_many({"chat_id": {"$in": chat_ids}})
        return

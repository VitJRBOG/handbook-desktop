import json
import os
from typing import Tuple, List, Any
import requests

from tools import logging


HANDBOOK_API_URL = os.environ.get('HANDBOOK_API_URL')


class Note:
    id: int
    title: str
    date: int

    def __init__(self, id: int, title: str, date: int):
        self.id = id
        self.title = title
        self.date = date


def get_notes() -> List[Note]:
    notes: List[Note] = []

    global HANDBOOK_API_URL
    url_ = f'{HANDBOOK_API_URL}/api/get-notes'
    resp_text, ok = __send_request(url_)
    if ok:
        json_loads = json.loads(resp_text)

        if json_loads['status_code'] == 200:
            items = json_loads['items']
        else:
            logging.Logger('warning').warning(json_loads['error'])
            return notes

        notes = __parse_notes(items)

    return notes


def __parse_notes(items: List[dict[str, Any]]) -> List[Note]:
    notes: List[Note] = []

    for item in items:
        note_id: int
        try:
            note_id = int(item['id'])
        except ValueError as e:
            logging.Logger('critical').critical(e, stack_info=True)
            return notes

        title = item['title']

        date: int
        try:
            date = int(item['date'])
        except ValueError as e:
            logging.Logger('critical').critical(e, stack_info=True)
            return notes

        notes.append(Note(note_id, title, date))

    return notes


def __send_request(url_: str) -> Tuple[str, bool]:
    response = requests.get(url_)
    if response.status_code == 200:
        return response.text, True
    else:
        logging.Logger('critical').critical(response.text, stack_info=True)
        return "", False

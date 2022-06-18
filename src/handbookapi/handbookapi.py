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

    request = __compose_get_request_url('get-notes')
    resp_text, ok = __send_get_request(request)
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


class Version:
    id: int
    text: str
    date: int
    checksum: str
    note_id: int

    def __init__(self, id: int, text: str, date: int,
                 checksum: str, note_id: int):
        self.id = id
        self.text = text
        self.date = date
        self.checksum = checksum
        self.note_id = note_id


def get_versions(note_id: int) -> List[Version]:
    versions: List[Version] = []

    params = {'id': note_id}
    request = __compose_get_request_url('get-versions', params)
    resp_text, ok = __send_get_request(request)
    if ok:
        json_loads = json.loads(resp_text)

        if json_loads['status_code'] == 200:
            items = json_loads['items']
        else:
            logging.Logger('warning').warning(json_loads['error'])
            return versions

        versions = __parse_versions(items)

    return versions


def __parse_versions(items: List[dict[str, Any]]) -> List[Version]:
    versions: List[Version] = []

    for item in items:
        version_id: int
        try:
            version_id = int(item['id'])
        except ValueError as e:
            logging.Logger('critical').critical(e, stack_info=True)
            return versions

        text = item['text']

        date: int
        try:
            date = int(item['date'])
        except ValueError as e:
            logging.Logger('critical').critical(e, stack_info=True)
            return versions

        checksum = item['checksum']

        note_id: int
        try:
            note_id = int(item['note_id'])
        except ValueError as e:
            logging.Logger('critical').critical(e, stack_info=True)
            return versions

        versions.append(Version(version_id, text, date, checksum, note_id))

    return versions


def __compose_get_request_url(method_name: str,
                              params: dict[str, Any] | None = None) -> str:
    global HANDBOOK_API_URL
    url_ = f'{HANDBOOK_API_URL}/api/{method_name}'

    if params is not None:
        url_ += '?'
        param_keys = list(params.keys())
        for i, key in enumerate(param_keys):
            url_ += f'{key}={params[key]}'
            if i < len(param_keys)-1:
                url_ += '&'

    return url_


def __send_get_request(url_: str) -> Tuple[str, bool]:
    response = requests.get(url_)
    if response.status_code == 200:
        return response.text, True
    else:
        logging.Logger('critical').critical(response.text, stack_info=True)
        return "", False

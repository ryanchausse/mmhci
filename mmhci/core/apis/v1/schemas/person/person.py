from ninja import Schema
from typing import Dict

class PersonResponse(Schema):
    first_name: str
    last_name: str

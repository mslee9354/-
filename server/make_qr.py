import json
import qrcode
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    rank: str
    birth: str
    service_no: str

    def to_json(self) -> str:
        return json.dumps({
            'name': self.name,
            'rank': self.rank,
            'birth': self.birth,
            'service_no': self.service_no,
        }, ensure_ascii=False)


def create_qr(person: Person, filename: str) -> None:
    img = qrcode.make(person.to_json())
    img.save(filename)


if __name__ == '__main__':
    p = Person(name='홍길동', rank='상병', birth='1998-01-01', service_no='12345678')
    create_qr(p, 'person_qr.png')
    print('QR saved to person_qr.png')

import json
from pathlib import Path

from .models import CarMake, CarModel


def initiate():
    data_path = Path(__file__).resolve().parents[1] / 'database' / 'data' / 'car_records.json'
    data = json.loads(data_path.read_text(encoding='utf-8'))
    for car in data['cars']:
        make, _created = CarMake.objects.get_or_create(
            name=car['make'],
            defaults={'description': f'{car["make"]} vehicles'},
        )
        CarModel.objects.get_or_create(
            car_make=make,
            name=car['model'],
            year=car['year'],
            defaults={
                'type': car['bodyType'],
                'dealer_id': car['dealer_id'],
            },
        )

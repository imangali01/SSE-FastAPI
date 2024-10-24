import json
import pytest
import random
from generator import simple_event_generator, match_event_generator


@pytest.mark.asyncio
async def test_simple_event_generator():
    # Создаём асинхронный генератор
    generator = simple_event_generator()

    # Проверяем первое событие
    event = await generator.__anext__()
    assert event == {"data": "This is a server-sent event!"}


@pytest.mark.asyncio
async def test_match_event_generator():
    team_a = "Inter"
    team_b = "Milan"
    match_duration_seconds = 5

    generator = match_event_generator(team_a, team_b, match_duration_seconds)

    # Проверяем первое событие - старт матча
    start_event = await generator.__anext__()
    start_data = json.loads(start_event.data)
    assert start_data['event'] == "Start"
    assert start_data['team_a'] == team_a
    assert start_data['team_b'] == team_b
    assert start_data['score'] == "0:0"

    # Итерируем события в течение времени матча
    current_time = 0
    while True:
        event = await generator.__anext__()
        event_data = json.loads(event.data)

        assert 'score' in event_data
        assert 'event' in event_data

        if event_data['event'] == "End": break
import json
import random
import asyncio

from sse_starlette.sse import ServerSentEvent


async def simple_event_generator():
    for i in range(10):
        await asyncio.sleep(1)
        yield {"data": "This is a server-sent event!"}


async def match_event_generator(team_a, team_b, match_duration_seconds):
    current_time = 0  # время в секундах
    score_a, score_b = 0, 0

    # Генерация события начала матча
    yield ServerSentEvent(
        data=json.dumps({
            'team_a': team_a,
            'team_b': team_b,
            'score': f'{score_a}:{score_b}',
            'event': 'Start'
        })
    )

    while current_time < match_duration_seconds:
        # Случайный интервал между событиями (1-5 секунд)
        sleep_time = random.randint(1, 5)
        await asyncio.sleep(sleep_time)
        current_time += sleep_time

        if current_time >= match_duration_seconds:
            break

        # Случайное событие гола
        scoring_team = random.choice([team_a, team_b])
        if scoring_team == team_a:
            score_a += 1
            yield ServerSentEvent(
                data=json.dumps({
                    'team_a': team_a,
                    'team_b': team_b,
                    'score': f'{score_a}:{score_b}',
                    'event': f'Scored Team {team_a}'
                })
            )
        else:
            score_b += 1
            yield ServerSentEvent(
                data=json.dumps({
                    'team_a': team_a,
                    'team_b': team_b,
                    'score': f'{score_a}:{score_b}',
                    'event': f'Scored Team {team_b}'
                })
            )

    # Генерация события окончания матча
    yield ServerSentEvent(
        data=json.dumps({
            'team_a': team_a,
            'team_b': team_b,
            'score': f'{score_a}:{score_b}',
            'event': 'End'
        })
    )

from dataclasses import dataclass
from operator import attrgetter
from typing import Optional, List

import boto3
import requests

client = boto3.client('rekognition')


@dataclass
class Emotion:
    type: str
    confidence: float


def get_emotions(content: bytes) -> Optional[List[Emotion]]:



    response = client.detect_faces(
        Image={'Bytes': content}, Attributes=['ALL']
    )

    if response['FaceDetails']:

        emotions = response['FaceDetails'][0]['Emotions']

        emotions = [
            Emotion(type=e['Type'], confidence=e['Confidence'])
            for e in emotions
        ]

        emotions = sorted(emotions, key=attrgetter('confidence'), reverse=True)

        return emotions

    return None

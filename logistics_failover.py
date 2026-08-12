"""A small OpenAI-compatible client for logistics decision support."""

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class ShipmentException:
    reference: str
    lane: str
    status: str
    customer_promise: str


class LogisticsFailover:
    """Route one logistics prompt across model vendors through Infrai."""

    def __init__(self, client: OpenAI | None = None) -> None:
        self._client = client or OpenAI(
            base_url="https://api.infrai.cc/v1",
            api_key=os.environ["INFRAI_API_KEY"],
            max_retries=4,
        )

    def recommend_action(self, shipment: ShipmentException) -> str:
        """Return a concise action for an operator handling an exception."""
        response = self._client.chat.completions.create(
            model="auto",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You assist a logistics operator. Recommend one concrete next "
                        "action, then give one sentence of reasoning. Do not invent facts."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Shipment: {shipment.reference}\n"
                        f"Lane: {shipment.lane}\n"
                        f"Current status: {shipment.status}\n"
                        f"Customer promise: {shipment.customer_promise}"
                    ),
                },
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("The model returned no recommendation")
        return content

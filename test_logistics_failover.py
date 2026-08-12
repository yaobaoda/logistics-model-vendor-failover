"""Focused contract test for the logistics routing call."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from logistics_failover import LogisticsFailover, ShipmentException


class LogisticsFailoverTest(unittest.TestCase):
    def test_routes_with_auto_model_and_returns_recommendation(self) -> None:
        client = Mock()
        client.chat.completions.create.return_value = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="Reserve the next sailing and notify the consignee."
                    )
                )
            ]
        )
        shipment = ShipmentException(
            reference="SHIP-2048",
            lane="Shenzhen to Rotterdam",
            status="Departure moved back",
            customer_promise="Friday 17:00",
        )

        result = LogisticsFailover(client).recommend_action(shipment)

        self.assertEqual(
            result, "Reserve the next sailing and notify the consignee."
        )
        call = client.chat.completions.create.call_args.kwargs
        self.assertEqual(call["model"], "auto")
        self.assertIn("SHIP-2048", call["messages"][1]["content"])


if __name__ == "__main__":
    unittest.main()

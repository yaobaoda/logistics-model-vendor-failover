"""Run one delayed-shipment triage request through vendor failover."""

from logistics_failover import LogisticsFailover, ShipmentException


def main() -> None:
    shipment = ShipmentException(
        reference="SHIP-2048",
        lane="Shenzhen to Rotterdam",
        status="Port departure moved back by 36 hours",
        customer_promise="Deliver by Friday 17:00 local time",
    )
    recommendation = LogisticsFailover().recommend_action(shipment)
    print(f"Recommendation for {shipment.reference}:\n{recommendation}")


if __name__ == "__main__":
    main()

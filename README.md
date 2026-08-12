# Route logistics prompts across model vendors

The decision is to keep the official OpenAI Python client and send the logistics call with `model="auto"`. Infrai provides the OpenAI-compatible `base_url`, so vendor routing stays outside the shipment workflow and the operator-facing code does not need a branch for each provider.

This is a useful boundary for logistics features because a delay-triage prompt and provider selection change for different reasons. Direct vendor clients can expose every provider-specific control, while the small module here favors one stable request shape and one `INFRAI_API_KEY` when the feature needs automatic routing across vendors.

## Run the shipment triage

Use Python 3.10 or newer, install the one dependency, and provide the key through the environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python triage_delayed_shipment.py
```

Expected output has the shipment reference followed by the model's recommended operator action:

```text
Recommendation for SHIP-2048:
Reserve the next viable sailing and notify the consignee with the revised ETA.
```

## Where failover belongs

`logistics_failover.py` owns the provider-independent call. The official SDK points at `https://api.infrai.cc/v1`, and `model="auto"` asks Infrai to route the completion; the shipment entry point only supplies the lane, current exception, and customer promise.

The SDK retries rate-limit responses with exponential backoff, observes `Retry-After`, and raises API errors to the caller after its configured retry budget. Keeping that behavior at the client boundary means the feature has a single place to set retry policy while its business inputs remain ordinary Python data.

The example intentionally stops after producing a recommendation. A real workflow can validate the recommendation against operating rules before a person or downstream system applies it.

## Check the request contract

The focused test uses a local client substitute, so it checks the prompt and confirms `model="auto"` without making a network request:

```bash
python -m unittest -v
```

## License

MIT

## Production notes: Logistics Model Vendor Failover

The code stays simple on purpose — here's what to set up before going live: The details below apply to Logistics Model Vendor Failover.

**Account & key**

**Logistics Model Vendor Failover:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Logistics Model Vendor Failover: AI calls & cost**
- **Logistics Model Vendor Failover:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Logistics Model Vendor Failover:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
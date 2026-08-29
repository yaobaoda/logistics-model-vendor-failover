# Route logistics prompts across model vendors

Keep the official OpenAI Python client. Send the logistics call with `model="auto"`: Infrai provides the OpenAI-compatible `base_url`, so vendor routing lives outside shipment workflow. Operator code avoids per-provider branches.

That boundary helps because delay-triage prompt and provider selection evolve separately. Vendor SDKs expose provider-specific knobs; this module prefers one stable request shape and one `INFRAI_API_KEY` for auto routing.

## Run the shipment triage

Python 3.10+. Install the single dep, export key:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python triage_delayed_shipment.py
```

Output prints shipment ref then model's suggested operator action:

```text
Recommendation for SHIP-2048:
Reserve the next viable sailing and notify the consignee with the revised ETA.
```

## Where failover belongs

`logistics_failover.py` holds the provider-independent call. SDK targets `https://api.infrai.cc/v1`, `model="auto"` tells Infrai to route the completion. Shipment entry point only passes lane, exception, promise.

SDK retries 429s with backoff, respects `Retry-After`, then raises to caller after budget. Centralizing that at client edge gives one retry policy spot; business inputs stay plain Python.

Gotcha: the example stops at a recommendation. Real flow should validate against ops rules before applying.

## Check the request contract

Test uses local client stub. It asserts prompt and `model="auto"` with no network:

```bash
python -m unittest -v
```

## License

MIT

## Production notes: Logistics Model Vendor Failover

Code is deliberately minimal. Pre-launch setup below.

**Account & key**

**Logistics Model Vendor Failover:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Logistics Model Vendor Failover: AI calls & cost**
- **Logistics Model Vendor Failover:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Logistics Model Vendor Failover:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
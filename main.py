import sys
import uuid
import time

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from prompt import classify_query
from entity_extraction import Extractor
from agent_actions import *


app = FastAPI()

class QueryRequest(BaseModel):
    message: str
    session_id: str

class Trace(BaseModel):
    trace_id: str
    session_id: str
    latency_ms: int
    tool_calls: list

class QueryResponse(BaseModel):
    response: str
    trace: Trace



def generate_query_id():
    return f"QRY-{uuid.uuid4().hex[:8].upper()}"

def generate_trace_id():
    return f"TRC-{uuid.uuid4().hex[:8].upper()}"


def customer_care_agent(query: str, trace: Trace) -> dict:
    processed_query = classify_query(query)

    query_id = generate_query_id()
    extractor = Extractor(query)
    order_details = extractor.extract_order_details()
    customer_details = extractor.extract_customer_details()

    subqueries = processed_query.queries
    action_log = {}

    for subquery in subqueries:
        relevance = subquery.relevance.value
        if relevance != 'relevant':
            continue

        intent = subquery.intent.value
        match intent:
            case 'Track Order':
                track_order(order_details['order_id'])
                action_log[intent] = [order_details]
                trace.tool_calls.append({"tool": "track_order", "order_id": order_details['order_id']})

            case 'Cancel Order':
                item_details = {}
                cancel_order(order_details['order_id'], item_details)
                action_log[intent] = [order_details, item_details]
                trace.tool_calls.append({"tool": "cancel_order", "order_id": order_details['order_id']})

            case 'Update Delivery Address':
                new_delivery_address = {}
                update_order(order_details['order_id'], 'Address', new_delivery_address)
                action_log[intent] = [order_details, new_delivery_address]
                trace.tool_calls.append({"tool": "update_address", "order_id": order_details['order_id']})

            case 'Update Phone Number':
                update_order(order_details['order_id'], 'Phone', customer_details['phone'])
                action_log[intent] = [order_details, customer_details]
                trace.tool_calls.append({"tool": "update_phone", "order_id": order_details['order_id']})

            case 'Issue a Refund':
                item_details = {}
                returns(order_details['order_id'], item_details)
                action_log[intent] = [order_details, item_details]
                trace.tool_calls.append({"tool": "issue_refund", "order_id": order_details['order_id']})

    return {'query_id': query_id, 'queries': action_log}


@app.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):
    start_time = time.time()

    trace = Trace(
        trace_id=generate_trace_id(),
        session_id=request.session_id,
        latency_ms=0,
        tool_calls=[],
    )

    result = customer_care_agent(request.message, trace)

    trace.latency_ms = int((time.time() - start_time) * 1000)

    response_text = f"Processed query {result['query_id']}. Actions taken: {list(result['queries'].keys())}"
    trace.tool_calls = list(result['queries'].keys())

    return QueryResponse(response=response_text, trace=trace)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
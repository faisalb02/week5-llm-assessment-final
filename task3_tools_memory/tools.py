def get_order_status(order_id: str):
    """Get the status of an order using its order ID."""

    orders = {
        "ORD100": "Shipped",
        "ORD101": "Delivered",
        "ORD102": "Processing"
    }

    return orders.get(order_id, "Order not found")


def get_customer(customer_id: str):
    """Get customer details using customer ID."""

    customers = {
        "CUST1": {
            "name": "Rahul",
            "email": "rahul@example.com"
        },
        "CUST2": {
            "name": "Priya",
            "email": "priya@example.com"
        }
    }

    return customers.get(customer_id, "Customer not found")


def calculate_discount(price: float, discount_percent: float):
    """Calculate the discounted price."""

    discount = price * discount_percent / 100

    final_price = price - discount

    return {
        "original_price": price,
        "discount": discount,
        "final_price": final_price
    }



TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get order status using order ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID"
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "Get customer details using customer ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer ID"
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_discount",
            "description": "Calculate discounted price",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {
                        "type": "number",
                        "description": "Original price"
                    },
                    "discount_percent": {
                        "type": "number",
                        "description": "Discount percentage"
                    }
                },
                "required": ["price", "discount_percent"],
                "additionalProperties": False
            }
        }
    }
]

import json


def execute_tool(tool_name, arguments):

    try:
        if isinstance(arguments, str):
            arguments = json.loads(arguments)

        if tool_name == "get_order_status":
            return get_order_status(**arguments)

        elif tool_name == "get_customer":
            return get_customer(**arguments)

        elif tool_name == "calculate_discount":
            return calculate_discount(**arguments)

        else:
            return {
                "error": f"Unknown tool: {tool_name}"
            }

    except Exception as e:
        return {
            "error": str(e)
        }



import asyncio


async def execute_tool_async(tool_name, arguments):
    return await asyncio.to_thread(
        execute_tool,
        tool_name,
        arguments
    )


async def execute_tools_parallel(tool_calls):

    tasks = []

    for tool_call in tool_calls:

        tool_name = tool_call["name"]
        arguments = tool_call["arguments"]

        task = execute_tool_async(
            tool_name,
            arguments
        )

        tasks.append(task)

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    final_results = []

    for tool_call, result in zip(
        tool_calls,
        results
    ):

        if isinstance(result, Exception):
            result = {
                "error": str(result)
            }

        final_results.append({
            "tool_call_id": tool_call["tool_call_id"],
            "result": result
        })

    return final_results    
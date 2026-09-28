"""Call the OpenJEV public gateway to Jev (TypeSafe's model).

OpenJEV (https://openjev.sh) is a free community gateway to the same Jev model
built by TypeSafe (https://typesafe.ai). It speaks the same System One contract
as this verifier and as the TypeSafe direct API, so the existing TypeSafe SDK
works unchanged — only the base URL, model id and API key differ.

  Endpoint  https://api.openjev.sh/v1/systemone
  Model     openjev
  Key       OPENJEV_API_KEY from https://openjev.sh/dashboard

Set OPENJEV_API_KEY and run:

  uv run python examples/openjev.py

TypeSafe stays the default for anyone with a TypeSafe key; OpenJEV is an
optional alternative when you do not want to self-host or run TypeSafe direct.
"""

import os

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

# The TypeSafe SDK accepts a custom base_url, so it works against OpenJEV too.
# Provider selection: an explicit base_url (as here) wins; otherwise TypeSafe is
# used when its key is set, and OpenJEV when only OPENJEV_API_KEY is set.
with TypeSafeClient(
    api_key=os.environ["OPENJEV_API_KEY"],
    base_url="https://api.openjev.sh",
) as client:
    result = client.system_one(
        model="openjev",
        state="I was charged twice. Please refund the extra payment today.",
        questions={
            "team": Choice(
                instructions="Route this ticket",
                criteria={
                    "billing": "Charges and refunds",
                    "technical": "Software bugs",
                },
            ),
            "urgency": Score(
                instructions="How urgent?",
                criteria=["No deadline", "Due today"],
            ),
            "refund": Noul(instructions="Does the customer request a refund?"),
        },
    )
    print(result.model_dump_json(indent=2))

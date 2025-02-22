#!/usr/bin/env python3
import os
import time
from openai import OpenAI

client = OpenAI(api_key="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")


# Define FIFO paths – these must match what your DOOM mod uses.
REQ_FIFO = "/tmp/doom_dialogue_req"
RES_FIFO = "/tmp/doom_dialogue_res"


def generate_dialogue(context: str) -> str:
    """
    Uses OpenAI's Chat Completions API to generate dialogue for DOOM NPCs.
    The system prompt sets the tone, and the user message provides the context.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # You can use "gpt-3.5-turbo" or another available model.
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a gritty, in-character dialogue generator for DOOM NPCs. "
                    "Keep responses short, snappy, and true to the dark, brutal tone of DOOM."
                    "You will be given an NPC type and some attributes. You are to generate a response as if your were that NPC."
                    "Keep your responses really short but in character."
                ),
            },
            {"role": "user", "content": context},
        ],
    )
    return completion.choices[0].message.content.strip()


def main():
    # Ensure both FIFO files exist; create them if they don't.
    for fifo in [REQ_FIFO, RES_FIFO]:
        if not os.path.exists(fifo):
            os.mkfifo(fifo)

    print("Dialogue server started. Listening on request FIFO:", REQ_FIFO)

    while True:
        # Open the request FIFO and read the context.
        with open(REQ_FIFO, "r") as req_fifo:
            context = req_fifo.read().strip()
            if not context:
                continue
            print("Received context:", context)

            dialogue = generate_dialogue(context)
            print("Generated dialogue:", dialogue)

        # Write the generated dialogue to the response FIFO.
        with open(RES_FIFO, "w") as res_fifo:
            res_fifo.write(dialogue)

        # Delay briefly to avoid a tight loop.
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Dialogue server shutting down.")

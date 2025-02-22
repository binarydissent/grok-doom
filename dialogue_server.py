#!/usr/bin/env python3
import os
import time
import textwrap
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class DoomDialogueServer:
    def __init__(self):
        self.LLM = os.environ.get("LLM", "openai")
        self.MODEL = os.environ.get("MODEL", "gpt-4o-mini")
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.XAI_API_KEY = os.environ.get("XAI_API_KEY")

        # Initialize the client based on the LLM.
        if self.LLM == "XAI":
            self.client = OpenAI(
                api_key=self.XAI_API_KEY,
                base_url="https://api.x.ai/v1",
            )
        else:
            self.client = OpenAI(api_key=self.OPENAI_API_KEY)

        # Define FIFO paths – these must match what your DOOM mod uses.
        self.REQ_FIFO = "/tmp/doom_dialogue_req"
        self.RES_FIFO = "/tmp/doom_dialogue_res"

        self.SYSTEM_PROMPT = (
            "You are a gritty, R18 dialogue generator for DOOM NPCs. "
            "Respond with raw, explicit, and brutal dialogue, using a maximum of 10 words. "
            "Your output must be snappy, dark, and true to the DOOM universe. "
            "You will be given some context around the NPC for whom you are generating the dialogue. "
            "<NPC> is the monster that is speaking. "
            "<Health> is their current health attribute. "
            "<Event> is what has triggered the dialogue."
        )

        self.init_fifo()

    def init_fifo(self):
        # Ensure both FIFO files exist; create them if they don't.
        for fifo in [self.REQ_FIFO, self.RES_FIFO]:
            if not os.path.exists(fifo):
                os.mkfifo(fifo)

    def wrap_text(self, text: str, width: int = 80) -> str:
        """
        Wrap text so that each line is at most `width` characters.
        This avoids splitting words by disabling break_long_words.
        """
        return textwrap.fill(
            text, width=width, break_long_words=False, break_on_hyphens=False
        )

    def read_request(self) -> str:
        """
        Read context from the request FIFO.
        """
        with open(self.REQ_FIFO, "r") as req_fifo:
            context = req_fifo.read().strip()
        return context

    def write_response(self, response: str):
        """
        Write the generated dialogue (response) to the response FIFO.
        """
        with open(self.RES_FIFO, "w") as res_fifo:
            res_fifo.write(response)

    def generate_dialogue(self, context: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": context},
            ],
        )
        dialogue = completion.choices[0].message.content.strip()
        # Format the dialogue with line breaks so that each line is ≤80 chars.
        return self.wrap_text(dialogue, width=80)

    def run(self):
        print("Dialogue server started. Listening on request FIFO:", self.REQ_FIFO)

        while True:
            context = self.read_request()
            if not context:
                time.sleep(0.1)
                continue
            print("Received context:", context)

            dialogue = self.generate_dialogue(context)
            print("Generated dialogue (wrapped):\n", dialogue)

            self.write_response(dialogue)
            # Delay briefly to avoid a tight loop.
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        server = DoomDialogueServer()
        server.run()
    except KeyboardInterrupt:
        print("Dialogue server shutting down.")

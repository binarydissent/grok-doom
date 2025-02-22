#!/usr/bin/env python3
import os
import time
import re
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()


class Dialogue(BaseModel):
    text: str


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
            "You are a gritty, R18 dialogue generator for DOOM NPCs. Be chaotic and hilarious. Don't be repetitive. "
            "Respond with raw, explicit, and brutal dialogue in no more than 40 characters. "
            "Your output must be snappy, dark, and true to the DOOM universe. "
            "Input context will be provided in the following format: "
            "<NPC> is the speaking entity, "
            "<HEALTH> is the NPC's current health, "
            "<EVENT> is the trigger event."
            "Your response should be a single line of text."
        )

        # No conversation history is maintained.
        self.init_fifo()

    def init_fifo(self):
        # Ensure both FIFO files exist; create them if they don't.
        for fifo in [self.REQ_FIFO, self.RES_FIFO]:
            if not os.path.exists(fifo):
                os.mkfifo(fifo)

    def wrap_text(self, text: str, width: int = 70) -> str:
        """
        Wrap text so that each line is at most `width` characters.
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

    def extract_npc(self, context: str) -> str:
        """
        Extract the NPC's name from the context string.
        Looks for a pattern like '<NPC> npcname </NPC>'.
        If not found, returns "unknown".
        """
        match = re.search(r"<NPC>\s*(.*?)\s*</NPC>", context)
        if match:
            return match.group(1).strip()
        return "unknown"

    def generate_dialogue(self, context: str) -> str:
        # Prepare the messages list with system prompt and the current context.
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": context},
        ]
        completion = self.client.beta.chat.completions.parse(
            model=self.MODEL,
            messages=messages,
            response_format=Dialogue,
        )
        dialogue = completion.choices[0].message.parsed
        text = dialogue.text.strip()
        # Wrap dialogue to ensure lines are ≤80 characters.
        wrapped_dialogue = self.wrap_text(text, width=80)
        return wrapped_dialogue

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

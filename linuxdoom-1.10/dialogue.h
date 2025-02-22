#ifndef DIALOGUE_H
#define DIALOGUE_H

/* FIFO paths used for dialogue exchange */
#define REQ_FIFO "/tmp/doom_dialogue_req"
#define RES_FIFO "/tmp/doom_dialogue_res"

#include "hu_lib.h"

/*
 * fetch_dialogue:
 *   Sends a context string (describing the NPC's state and event) to the
 *   external Python dialogue service via FIFO pipes and returns the dialogue.
 *   The returned string is malloc()’ed and must be freed by the caller.
 */
char *fetch_dialogue(const char *context);

/*
 * NPCDialogue_Init
 *  Initializes the NPC dialogue system.
 *  Must be called after the HUD fonts are loaded (i.e. after I_InitGraphics).
 */
void NPCDialogue_Init(void);

/*
 * NPCDialogue_AddLine
 *  Adds a new dialogue line from an NPC to the HUD.
 *  'speaker' is a string (e.g. the NPC's name), and 'text' is the dialogue message.
 *  Also sets a timer so the message fades out after 3 seconds.
 */
void NPCDialogue_AddLine(const char *speaker, const char *text);

/*
 * NPCDialogue_UpdateAndDraw
 *  Updates and renders the NPC dialogue text on-screen.
 *  Call this once per frame in your HUD drawing routine.
 */
void NPCDialogue_UpdateAndDraw(void);

/*
 * NPCDialogue_Ticker
 *  Should be called once per tic to decrement the dialogue fade-out timer.
 */
void NPCDialogue_Ticker(void);


/*
 * MobjTypeToString
 * Maps doomednum to npc name
 */
const char* MobjTypeToString(mobjtype_t type);

#endif /* DIALOGUE_H */

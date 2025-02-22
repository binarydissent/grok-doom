#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include "dialogue.h"
#include "hu_lib.h"
#include "r_defs.h"    // For patch_t definition
#include "hu_stuff.h"  // For HU_FONTSTART, HU_FONTSIZE, etc.

#define BUFFER_SIZE 1024

//
// FIFO-based dialogue fetching
//
char *fetch_dialogue(const char *context) {
    int fd;
    char *response = malloc(BUFFER_SIZE);
    if (!response)
        return NULL;
    memset(response, 0, BUFFER_SIZE);

    // Open the request FIFO for writing and send the context.
    fd = open(REQ_FIFO, O_WRONLY);
    if (fd < 0) {
        free(response);
        return NULL;
    }
    write(fd, context, strlen(context));
    close(fd);

    // Open the response FIFO for reading the dialogue.
    fd = open(RES_FIFO, O_RDONLY);
    if (fd < 0) {
        free(response);
        return NULL;
    }
    int n = read(fd, response, BUFFER_SIZE - 1);
    if (n < 0) {
        free(response);
        close(fd);
        return NULL;
    }
    response[n] = '\0';
    close(fd);
    return response;
}

//
// NPC Dialogue HUD Integration
//

hu_stext_t npc_dialogue_stext;
boolean npc_dialogue_on = true;

// Global timer (in tics) for how long the dialogue remains visible.
// Assuming TICRATE is defined (e.g., 35 tics per second).
int npc_dialogue_timer = 0;

void NPCDialogue_Init(void) {
    extern patch_t *hu_font[HU_FONTSIZE];
    
    // Use HU_FONTSTART (e.g., '!') as the start character.
    HUlib_initSText(&npc_dialogue_stext,
                    10,
                    SCREENHEIGHT - 40,
                    2,
                    hu_font,
                    HU_FONTSTART,
                    &npc_dialogue_on);
}

void NPCDialogue_AddLine(const char *speaker, const char *text) {
    // Clear the previous dialogue from the widget.
    HUlib_eraseSText(&npc_dialogue_stext);
    
    // Add the new dialogue line.
    HUlib_addMessageToSText(&npc_dialogue_stext, (char*)speaker, (char*)text);
    
    // Ensure dialogue is visible.
    npc_dialogue_on = true;
    
    // Set the timer to 3 seconds (assuming TICRATE tics per second).
    npc_dialogue_timer = 3 * TICRATE;
}

void NPCDialogue_UpdateAndDraw(void) {
    if (npc_dialogue_on) {
        HUlib_drawSText(&npc_dialogue_stext);
    }
}

void NPCDialogue_Ticker(void) {
    if (npc_dialogue_timer > 0) {
        npc_dialogue_timer--;
        if (npc_dialogue_timer <= 0) {
            // Fade out: clear the dialogue widget.
            HUlib_eraseSText(&npc_dialogue_stext);
            npc_dialogue_on = false;  // Stop drawing the dialogue.
        }
    }
}


const char* MobjTypeToString(mobjtype_t type) {
    switch (type) {
        case 3004: return "possessed";
        case 9:    return "shotguy";
        case 64:   return "vile";
        case 66:   return "undead";
        case 67:   return "fatso";
        case 65:   return "chainguy";
        case 3001: return "troop";
        case 3002: return "sergeant";
        case 58:   return "shadows";
        case 3005: return "head";
        case 3003: return "bruiser";
        case 69:   return "knight";
        case 3006: return "skull";
        case 7:    return "spider";
        case 68:   return "baby";
        case 16:   return "cyborg";
        case 71:   return "pain";
        case 84:   return "wolfss";
        case 72:   return "keen";
        case 88:   return "bossbrain";
        case 89:   return "bossspit";
        case 87:   return "bosstarget";
        case 14:   return "teleportman";
        default: {
            static char unknown[32];
            sprintf(unknown, "unknown.%d", type);
            return unknown;
        }
    }
}

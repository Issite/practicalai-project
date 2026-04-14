### Sprint One: April 7 - April 14:

#### Work done:
- (very) basic functions for document querying (found in `src/document_reader.py`). It currently only grabs specific json information (i.e. not vector search), but made me realize I needed to work on:
- Filled out plot documents for the trial story (found in `data/stories/trial/`). I decided to use json instead of markdown for documents, though this may come back to bite me when I integrate ChromaDB. I may end up writing a simple json->md converter for vector store this week.
- I didn't do as much this week as I should have, but I did spend some time designing how the system will integrate everything together (LLM, tools, user input, etc.). I'll have to put everything in work-notes.

#### Challenges and setbacks:
Mostly just realizing that at this stage instead of writing code to make progress, I'll need to take a break and fill out more of my plot/character documents, as well as writing a *comprehensive* system prompt to guide the LLM. Hopefully I can do some of this with GenAI, but the whole point of the project was to have strict control over the integrated AI, and have it follow my creative vision for the story, not Copilot's. If I want to have a viable demo for the presentation though, I can't spend all of my time writing a bunch of documents, so I'll have to find a balance.

#### Next sprint:
- **Time**: I should be able to spend 3-4 hours next week on this project, especially since there's not a lot of work this week for Cryptography/Capstone. I could put an hour or two in Thursday afternoon, but Friday's completely clear and I could spend pretty much all day working until the work is done.
- **Goals**: My main goal is to improve my RAG with ChromaDB (rag-lab should be a big help), and to make a comprehensive system prompt (in that order since I'd like to make the system prompt after all the tools are done). I think I can leave most of the plot/character documents until after the presentation, since I can keep it simple for the demo. That means this sprint can finish all the little bits and peices of the system, then the overnext sprint can compose everything together.
- **Work products**: I'd like to see `src/document_reader.py` at least double in size, with vector store/query functionality. I'll also create `data/agent/prompts.yaml` with my system prompt, including tool examples and instructions for how the agent should use them. If I have time, I can also start filling out some of the character documents, but that's not a priority for this sprint.
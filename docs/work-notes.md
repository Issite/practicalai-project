But what if... we were to use JSON for ouput?
I do like parsers.

L'sig'h, smolagents's "code agents" seem frisky, but that's what's in the
tutorial. Mleh.

Okay, The Plan: The AI Agent will actually have no output. It will produce scripts via tools. Tools I will need: Dialogue tool, Sprite tool, Menu tool, Plot tool,
and a Profile tool.

Gradio is integrated with both huggingface and smolagents so it's probably easier to use, but looking into streamlit probably isn't a terrible idea.

Okay, smolagents doesn't like instance methods as tools (at least not when you're using the `@tool` decorator), so here's the workaround: create a wrapper method (like `get_tools()`) that defines UNBOUND (i.e. `self`less) methods wrapped with the `@tool` decorator. Because it's inside `get_tools()`, it has access to `self` and can use instance variables.

Decided to use json instead of markdown for documents, since I realized I don't want to write a md parser.

Four sprints remaining, but the presentation is in only two. Hopefully I can get the project into an MVP by then, with only polishing done for the last two sprints.

Each story will have a starter section, which will define author-written messages for the agent, which will A. Start the story the same way everytime (and hopefully ease the user into the dynamic environment), and B. Jumpstart the agent into already using its tools the "proper" way.

Currently, I'm not planning on having the user interface with the agent directly. Instead when the user submits a message, the system will process it and add a *system* message to the chat history saying something like "The user said: [user message]." The agent will then take this information and call more tools with further script content, then those tools will format the content into Ren'py script (and human-readible output for cmdln/gradio) and output it. In this way the application acts as a "translation layer" between the user and the agent.

The system will prompt the agent ahead of time with "Continue the story (no user input).", even if waiting to see if the user inputs a message. This way it can build up a buffer of content for the user to click through, if they don't have anything to say. (I'm currently planning on treating a blank user message or `.` as "no input".)

I would like the agent to constantly bring plot/character details into recent context, but I'm not certain of the best way to go about that. I'll have to instruct it somewhere in the prompt to do so, but I don't know if that will make it consistent. Maybe vector-based search will make the problem go away (Example: If a character is supposed to act in some manner when surprised, will the agent know to reference their profile? Vector-search of the most recent script lines/model thoughts might be able to automatically return relevant information), but we'll see.

Just had a thought: What if I used managed models for each character? They can keep their own internall monologue, which should help with consistency. Probably too much work, (especially for the demo,) but if I work on the project after the end of the semester...

Copilot was surprisingly good at writing the system prompt. I'm thinking of using it to write out a dummy story other than "The Trial" for the demo, since I realized I have to focus on user-integration.
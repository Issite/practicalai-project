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
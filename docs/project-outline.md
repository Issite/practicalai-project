### System desc.

I will create a system capable of generating visual novels in the Ren'py script format. It will use a foundational model to generate structured output to continue the script, and potentially an image generation model for creating new sprites, though some sprites will be built in to the system. It will use RAG, reading pre-written "plot summary" documents that will guide the course of the plot. It will also use tool calls to integrate Ren'py's user choice mechanics, though it will also allow the user to input dialogue for their character at any time. The system will be primarily designed to output to the CL and a script file, though integration with Gradio is planned and I will attempt to get Ren'py working with the live stream of output from the model.

### Outline
- What AI system do you plan to design, develop, and experiment with?
     Ren'py integrated VN writer.
- What AI concepts and techniques will you need to focus on?
     Tool definitions, Image generation APIs
- What computing resources, tools, platforms, datasets, existing implementations do you plan to use for your project?.
     smolagents, Mistral Small, (image generation API), Ren'py, gradio, RAG for plot
- What risks might be posed by the development and use of the AI system? How can the risks be mitigated? Consider the following issues:
- Safety and security
     Without output validation, you must rely on easily jailbroken models to prevent misuse.
- Protection of data privacy and against algorithmic discrimination
     No data stored
- Transparency
     Attribution, open source
- Explanation
     Open source


### Learning and Work Plan
What's your learning and work plan for the duration of the project? 
#### Week 1
Ren'py language analysis, agentic framework/model research
#### Week 2
Structured output w/ foundational model
#### Week 3
Tool calling
#### Week 4
Tool development
#### Week 5
Retrieval Augmented Generation
#### Week 6/7 (lol)
Gradio/Ren'py integrations
#### Week 8
Presentation
### Notes
 - ASCII art?
 - User supplied stories?
 - Small story domain
 - No fine tuning, any model should work
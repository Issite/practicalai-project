# Ren'Py Visual Novel Generation Agent

An AI-powered system that generates interactive visual novel scripts in Ren'Py format using agentic RAG (Retrieval-Augmented Generation). The system uses large language models to create dynamic storylines, dialogue, and character interactions guided by plot outlines and character profiles.

## Overview

This project implements an intelligent agent that:
- **Generates Ren'Py scripts** with dialogue, sprite actions, and user choice menus
- **Uses Retrieval-Augmented Generation (RAG)** to ground story generation in plot outlines and character profiles
- **Employs tool calling** to interact with document stores and write output scripts
- **Provides interactive storytelling** through agentic reasoning and planning

The agent leverages the `smolagents` framework with large language models to create structured, coherent visual novel content that can be executed by Ren'Py or displayed through web interfaces.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `huggingface_hub` - Model access and inference
  - `smolagents` - Agentic framework
  - `dotenv` - Environment configuration
  - `pytz` - Timezone handling (Only used in early tests, not critical)
  - `chromadb` - Vector database for RAG

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the visual novel generation agent:

```bash
python main.py
```

This launches an interactive Gradio interface where you can:
- Submit user dialogue and story direction
- Receive generated Ren'Py script output
- Make choices at decision points in the story

## Project Structure

```
.
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── data/
│   ├── agent/                       # Main agent configuration
│   │   ├── agent.json
│   │   └── prompts.yaml
│   ├── agent_test/                  # Test agent configuration
│   │   ├── agent.json
│   │   └── prompts.yaml
│   └── stories/
│       └── trial/                   # Example story data
│           ├── alice.json           # Character profile
│           ├── bob.json             # Character profile
│           └── plot.json            # Plot outline
├── output/
│   └── script.rpy                   # Generated script output
├── src/
│   ├── document_reader.py           # RAG document retrieval
│   ├── rpy_character.py             # Character representation
│   ├── rpy_generation_agent.py      # Main agent implementation
│   ├── script_writer.py             # Script generation and output
│   └── learning/
│       ├── agent_test.py            # Agent testing utilities
│       └── learning_test.py         # Learning experiments
└── docs/
    ├── project-outline.md           # Initial project design
    ├── design.md                    # System architecture
    ├── sprint-log.md                # Development progress
    ├── work-notes.md                # Technical notes
    └── copilot.md                   # AI assistance notes
```

## Key Components

### RpyGenerationAgent (`src/rpy_generation_agent.py`)
The main agentic system that coordinates story generation using:
- **Model**: Qwen2.5-Coder-32B (configurable)
- **Tools**: Document reader + script writer
- **Framework**: smolagents CodeAgent with planning

### DocumentReader (`src/document_reader.py`)
Implements RAG by:
- Loading character profiles and plot outlines from JSON files
- Providing tools for the agent to query story documents
- Enabling context-aware generation

### ScriptWriter (`src/script_writer.py`)
Handles output generation:
- Converts agent output into Ren'Py script format
- Manages dialogue, sprite actions, and menus
- Supports multiple output modes (file, console, both)

### RpyCharacter (`src/rpy_character.py`)
Represents character data including:
- Name and visual description
- Personality and background
- Dialogue patterns and reactions

## Story Format

Stories are defined through JSON files:
- **Character profiles** (`*.json`): Character attributes and dialogue patterns
- **Plot outlines** (`plot.json`): Story progression, branching points, and events

Example structure in `data/stories/trial/`:
```
plot.json           # Overall story narrative
alice.json          # Alice character profile
bob.json            # Bob character profile
```

## Output

Generated scripts are saved to `output/script.rpy` in Ren'Py format, featuring:
- Character dialogue
- Sprite positioning and animations
- User choice menus for interactive branching
- Scene transitions and descriptions

## Future Enhancements

- Image generation integration for sprite creation
- Advanced Ren'Py UI integration with live output streaming
- Support for complex branching narratives
- Multi-agent collaboration for diverse story elements

## License

This project is part of the Practical AI course (Spring 2026).

## References

- [Ren'Py Documentation](https://www.renpy.org/)
- [smolagents Framework](https://github.com/agentic-ai/smolagents)
- [Retrieval-Augmented Generation](https://en.wikipedia.org/wiki/Prompt_engineering#Retrieval-augmented_generation)

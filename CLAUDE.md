# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) system for workflow generation. It uses FAISS vector search to retrieve relevant workflow templates based on natural language queries, then uses an LLM to generate new workflows in JSON format.

**Core workflow:**
1. `indexing.py` - Builds FAISS vector index from workflow templates
2. `main.py` - Accepts user queries, retrieves top-5 similar templates, generates new workflow JSON

## Commands

### Environment Setup
```bash
# Install dependencies using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Running the Application
```bash
# Build the FAISS index (run once or when templates change)
python indexing.py

# Run the main query interface
python main.py
```

### Development
```bash
# Launch Jupyter for exploring check.ipynb
jupyter notebook check.ipynb
```

## Architecture

### Data Flow
```
User Query → FAISS Similarity Search → Top 5 Templates Retrieved →
Formatted into MASTER_PROMPT → OpenAI LLM → Generated Workflow JSON
```

### Key Components

**indexing.py** - Vector index creation
- Loads workflow templates from `templates.py`
- Each template is a tuple: `(task_description, template_json)`
- Embeds task descriptions using OpenAI `text-embedding-3-large`
- Saves FAISS index to `/embeddings` directory

**main.py** - Query and generation pipeline (main.py:1-28)
- Loads FAISS index from `/embeddings`
- Searches for top 5 similar templates via `similarity_search(query, k=5)`
- Extracts template metadata from retrieved documents
- Populates `MASTER_PROMPT` with 5 examples (`temp1` through `temp5`)
- Uses OpenAI model for generation (currently set to "o3")

**prompt.py** - System prompt template
- `MASTER_PROMPT` contains instructions for workflow generation
- Expects workflows as DAGs (directed acyclic graphs)
- Enforces specific rules for node connections and targetHandle formats
- Critical constraint: nodes must follow type-prefixed handle patterns (e.g., "str-prompt", "uri-str-image_urls")

**templates.py** - Workflow template database
- Large file (~1.8MB) containing `LIST` of workflow examples
- Each entry: `[task_description_string, workflow_json_dict]`
- Templates include nodes, edges, model metadata, and API configurations

## Important Details

### API Keys
The codebase contains hardcoded OpenAI API keys in `main.py` and `indexing.py`. These should be:
- Moved to environment variables (`OPENAI_API_KEY`)
- Never committed to version control
- Replaced immediately if exposed

### FAISS Index Location
- Index saved to absolute path `/embeddings`
- On Windows, this may cause issues (should be relative path or configurable)
- Consider changing to `./embeddings` or using environment variable

### Template Metadata Structure
Templates in FAISS store JSON as strings in metadata:
```python
Document(
    page_content=task_desc,
    metadata={"template": json.dumps(temp)}
)
```
Retrieved via `doc.metadata['template']` (already JSON string, ready for prompt)

### Model Configuration
- Embeddings: `text-embedding-3-large` (OpenAI)
- Generation: Currently set to "o3" model in main.py:25
- FAISS: CPU version (no GPU dependencies)

## Critical Workflow Rules (from MASTER_PROMPT)

When generating or modifying workflows:
1. All workflows must be DAGs (no cycles)
2. Every workflow needs at least one output node
3. All nodes must be connected (no orphan nodes)
4. TargetHandle format is type-specific:
   - `"str-parameter_name"` for strings
   - `"uri-str-parameter_name"` for URI strings
   - `"int-parameter_name"` for integers
   - `"float-parameter_name"` for floats
   - `"bool-parameter_name"` for booleans
5. Models must reference entries from `models.json` (referenced but not in repo)
6. Amazon S3 links should be preserved as-is

## Logging

The API service includes comprehensive logging:

- **General logs**: `logs/api.log` - Contains timestamped log entries for all requests
- **Detailed request logs**: `logs/request_NNNN.json` - Individual JSON files for each request containing:
  - Request number and timestamp
  - User query
  - All 5 retrieved documents with their page_content
  - Document rankings

Logs are automatically created when the API starts. Each request increments a counter and creates a new numbered JSON file (e.g., `request_0001.json`, `request_0002.json`, etc.).

## Development Notes

- `check.ipynb` - Jupyter notebook for testing/exploration
- No test suite currently exists
- No linting configuration present
- Dependencies managed via `pyproject.toml` (Python >=3.12 required)
- Logs directory is created automatically on API startup

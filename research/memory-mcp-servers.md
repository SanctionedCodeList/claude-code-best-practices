# Memory MCP Servers for Claude Code

Research compiled: 2025-12-31

This document catalogs MCP (Model Context Protocol) servers and tools that provide memory capabilities for Claude Code and other AI assistants.

---

## 1. Official MCP Memory Servers

### @modelcontextprotocol/server-memory (Reference Implementation)

The official memory server from Anthropic provides persistent memory using a local knowledge graph.

- **Repository**: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- **NPM**: [@modelcontextprotocol/server-memory](https://www.npmjs.com/package/@modelcontextprotocol/server-memory)
- **License**: MIT
- **Latest Version**: 2025.11.25

**Features**:
- Knowledge graph structure with entities, relations, and observations
- Entities are primary nodes; relations define directed connections (stored in active voice)
- Observations are discrete pieces of information about entities
- Configurable storage via `MEMORY_FILE_PATH` environment variable
- Human-readable JSON storage format

**Installation**:
```bash
npm i @modelcontextprotocol/server-memory
```

---

## 2. Community Memory Solutions

### MCP Memory Service (doobidoo)

Automatic context memory that captures project context, architecture decisions, and code patterns.

- **Repository**: [doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)
- **Supported Clients**: Claude Desktop, Claude Code, VS Code, Cursor, and 13+ AI apps
- **Storage Backends**: SQLite-vec, Cloudflare hybrid options

**Key Benefits**:
- Eliminates re-explaining project context in new sessions
- Automatic capture of architecture decisions and code patterns
- Works across multiple AI tool integrations

---

### MCP Memory Keeper (mkreyman)

Persistent context management for Claude AI coding assistants.

- **Repository**: [mkreyman/mcp-memory-keeper](https://github.com/mkreyman/mcp-memory-keeper)

**Features**:
- Preserves work history, decisions, and progress
- Maintains context across sessions
- Designed specifically for coding workflows

---

### MCP Knowledge Graph (shaneholloman)

Local knowledge graph for persistent memory with synced folder storage.

- **Repository**: [shaneholloman/mcp-knowledge-graph](https://github.com/shaneholloman/mcp-knowledge-graph)

**Features**:
- Stores memories in `memory.jsonl` as master database
- Synced folder storage for portability
- Local development focused

---

### MCP Persistent Memory (dirkenglund)

Graph memory with automatic disk storage.

- **Server**: [dirkenglund/mcp-persistent-memory](https://lobehub.com/mcp/dirkenglund-mcp-persistent-memory)

**Environment Variables**:
- `MEMORY_STORAGE_DIR`: Directory for storing graph data
- `MAX_BACKUPS`: Maximum backup files to retain
- `PORT`: HTTP server port
- `HOST`: HTTP server host

**Features**:
- Automatic saving of graph data to disk
- Entity relationship storage
- Cross-session context maintenance

---

### Claude Memory MCP (@whenmoon-afk)

Local, persistent memory service using SQLite.

- **Server**: [@whenmoon-afk/memory-mcp](https://www.pulsemcp.com/servers/whenmoon-memory)

**Features**:
- Portable `memory.db` SQLite file
- Full-text search support
- All data stays on local machine
- Audit-friendly memory store

---

## 3. Vector Database MCP Integrations

### Qdrant MCP Server (Official)

Official Qdrant Model Context Protocol server implementation.

- **Repository**: [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant)

**Tools**:
- `qdrant-store`: Store code snippets with descriptions
- `qdrant-find`: Search for relevant code using natural language

---

### Milvus MCP Server

Vector search integration for AI applications.

- **Documentation**: [Milvus MCP Documentation](https://milvus.io/docs/milvus_and_mcp.md)

**Tools**:
- `milvus-text-search`: Full text search
- `milvus-vector-search`: Vector similarity search
- `milvus-hybrid-search`: Combined vector similarity and attribute filtering

---

### Claude Context (Zilliz)

Codebase indexing with hybrid search capabilities.

- **Repository**: [zilliztech/claude-context](https://github.com/zilliztech/claude-context)
- **Token Reduction**: ~40% compared to loading entire directories

**Features**:
- Hybrid search (BM25 + dense vector)
- Natural language codebase queries
- Supports OpenAI, VoyageAI, Ollama, Gemini embeddings
- Works with Milvus or Zilliz Cloud

---

### Claude Vector DB (isthatamullet)

Automated vector database for Claude Code conversations.

- **Repository**: [isthatamullet/claude-vector-db](https://github.com/isthatamullet/claude-vector-db)

**Features**:
- Hooks-based real-time indexing
- Semantic search with intelligent relevance boosting
- 16 consolidated MCP tools
- ChromaDB vector store with CPU-optimized embeddings
- FastMCP integration

---

### ChromaDB MCP Server

Memory layer for AI agents using ChromaDB.

- **Core Repository**: chroma-core/chroma-mcp
- **Community Fork**: HumainLabs fork (adds document versioning and hybrid search)

**Compatible Clients**: Cursor, LobeChat, and custom applications

---

### Vector Memory MCP Server

SQLite-vec based vector memory with sentence-transformers.

- **Server**: [cornebidouil/vector-memory-mcp](https://lobehub.com/mcp/cornebidouil-vector-memory-mcp)

**Features**:
- Persistent semantic memory
- SQLite vector indexing
- Fast embedding generation
- Local operation (no external API required)

---

### CodeWeaver MCP Server

Extensible MCP server with pluggable architecture.

- **Server**: [knitli/codeweaver-mcp](https://lobehub.com/mcp/knitli-codeweaver-mcp)

**Supported Components**:
- **Embedding Providers**: Voyage AI, OpenAI, Cohere, HuggingFace
- **Vector Databases**: Qdrant, Pinecone, Weaviate, ChromaDB
- **Data Sources**: Filesystem, git, database, API, web

---

### OpenSearch MCP

Full-text and vector search capabilities.

- **Reference**: [OpenSearch MCP Integration](https://developer.mamezou-tech.com/en/blogs/2025/09/02/opensearch_mcp/)

**Features**:
- Semantic search extension for Claude Code
- Full-text search engine connectivity

---

## 4. Knowledge Graph MCP Servers

### Neo4j MCP Integration

Graph database integration for AI context.

- **Documentation**: [Neo4j MCP Integration](https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/)
- **Blog**: [Neo4j Model Context Protocol Guide](https://neo4j.com/blog/developer/model-context-protocol/)

**Features**:
- mcp-neo4j-memory: Stores entities with observations and relationships
- Subgraph search and retrieval
- Upgraded from example knowledge graph implementation

---

### Memory Graph MCP Server (samwang0723)

Long-term memory using Redis Graph.

- **Server**: [samwang0723/memory-graph](https://www.pulsemcp.com/servers/samwang0723-memory-graph)
- **Released**: March 2025
- **Language**: TypeScript

**Requirements**:
- Docker and Docker Compose
- Node.js v16+

**Installation**:
```bash
# Start Redis with RedisGraph module
docker-compose up -d

# Add to Claude Code
claude mcp add-json "mcp-memory" '{"command":"npx","args":["-y","mcp-memory"]}'
```

**Features**:
- Persistent knowledge graphs across conversations
- Complex information networks
- Powerful search capabilities
- Relationship creation between memory nodes

---

### Redis MCP Servers (Official)

Official Redis MCP implementation.

- **Repository**: [redis/mcp-redis](https://github.com/redis/mcp-redis)
- **Blog**: [Redis MCP Introduction](https://redis.io/blog/introducing-model-context-protocol-mcp-for-redis/)

**Use Cases**:
- Session management
- Conversation history
- Real-time caching
- Rate limiting
- Recommendations
- Semantic search for RAG

---

### Weaviate MCP Server

Knowledge base and chat memory integration.

- **Reference**: [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

**Features**:
- Connect to Weaviate collections as knowledge base
- Chat memory store functionality

---

## 5. Curated Resource Lists

### Awesome MCP Servers

Community-curated collection of MCP servers.

- **Repository**: [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

### Official MCP Examples

Reference implementations demonstrating core MCP features.

- **Documentation**: [MCP Example Servers](https://modelcontextprotocol.io/examples)

### Knowledge and Memory Category

Dedicated category for memory-focused MCP servers.

- **Catalog**: [mcp.so Knowledge and Memory](https://mcp.so/category/knowledge-and-memory)

### MCP Servers Directory

Searchable directory of MCP servers.

- **Site**: [mcpservers.org](https://mcpservers.org/servers/modelcontextprotocol/memory)

---

## 6. Summary Comparison

| Server | Storage Type | Best For |
|--------|--------------|----------|
| @modelcontextprotocol/server-memory | JSON file | Simple persistent memory |
| MCP Memory Service | SQLite-vec | Multi-tool context preservation |
| Qdrant MCP | Vector DB | Code snippet search |
| Milvus MCP | Vector DB | Hybrid search at scale |
| Claude Context | Vector DB | Codebase indexing |
| Neo4j MCP | Graph DB | Complex entity relationships |
| Memory Graph (Redis) | Graph DB | Conversation context graphs |
| Vector Memory MCP | SQLite-vec | Local semantic search |

---

## 7. MCP Specification Notes

- **Current Spec Version**: 2025-11-25 (One-year anniversary release)
- **Key Updates in 2025**: OAuth support, tool annotations, batching, streaming HTTP transport
- **Specification**: [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification/2025-11-25)

---

## References

- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Official Site](https://modelcontextprotocol.io/)
- [MCP GitHub Organization](https://github.com/modelcontextprotocol)
- [MCP Index](https://mcpindex.net/)
- [PulseMCP Server Directory](https://www.pulsemcp.com/)
- [LobeHub MCP Servers](https://lobehub.com/mcp)

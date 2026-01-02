# Titans Architecture Research

Google's Titans architecture for neural long-term memory in AI systems.

---

## Overview

**Paper:** [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)
**Authors:** Ali Behrouz, Peilin Zhong, Vahab Mirrokni (Google Research)
**Published:** December 2024

Titans introduces a neural long-term memory module that learns to memorize at test time, enabling context windows beyond 2 million tokens.

---

## The Problem Titans Solves

| Approach | Strength | Weakness |
|----------|----------|----------|
| **Attention** | Precise dependency modeling | Quadratic cost, limited context |
| **RNNs** | Efficient inference | Fixed-size memory, loses information |
| **Titans** | Combines both | Learns what to memorize dynamically |

---

## Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    TITANS ARCHITECTURE                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                    │
│  │ PERSISTENT      │  Fixed weights after training      │
│  │ MEMORY          │  Stores task-independent knowledge │
│  └─────────────────┘                                    │
│                                                         │
│  ┌─────────────────┐                                    │
│  │ LONG-TERM       │  Neural network (MLP) that learns  │
│  │ MEMORY          │  to memorize at test time          │
│  └─────────────────┘  Uses "surprise" signal to decide  │
│                       what to store                     │
│                                                         │
│  ┌─────────────────┐                                    │
│  │ CORE            │  Standard attention mechanism      │
│  │ (Short-term)    │  Limited window, precise recall    │
│  └─────────────────┘                                    │
└─────────────────────────────────────────────────────────┘
```

---

## The "Surprise" Mechanism

Titans decides what to memorize using a **surprise metric**:

1. If input matches expectations → low surprise → minimal memory update
2. If input conflicts with model's beliefs → high surprise → immediate memory update

This mimics human memory: we forget routine events but remember surprising ones.

**Technical implementation:** The gradient of the neural network with respect to its input acts as the surprise signal.

---

## Three Architectural Variants

### 1. Memory as Context (MAC)
- Memory output serves as additional context for attention
- Like a research assistant providing background information
- Memory and attention work in parallel

### 2. Memory as Gate (MAG)
- Combines memory and attention outputs through gating
- Parallel processors for short-term and long-term memory
- Gating controls information flow

### 3. Memory as Layer (MAL)
- Stacks memory and attention layers sequentially
- Integrates long-term memory directly into network structure
- Sequential processing

---

## Performance

- Scales to **2M+ token context windows**
- Outperforms Transformers on needle-in-haystack tasks
- Better than GPT-4 on BABILong benchmark (reasoning across long documents)
- Effective on: language modeling, common-sense reasoning, genomics, time series

---

## Implementations

### Primary: lucidrains/titans-pytorch
**GitHub:** https://github.com/lucidrains/titans-pytorch
**Stars:** 1.8k+ | **Install:** `pip install titans-pytorch`

```python
from titans_pytorch import NeuralMemory, MemoryAsContextTransformer

# Neural Memory Module
mem = NeuralMemory(dim=384, chunk_size=64)
retrieved, mem_state = mem(seq, prev_state=mem_state)

# Full Transformer with Memory
model = MemoryAsContextTransformer(
    num_tokens=256,
    dim=256,
    depth=2,
    segment_len=128,
    num_persist_mem_tokens=4,
    num_longterm_mem_tokens=16
)

loss = model(token_ids, return_loss=True)
sampled = model.sample(prompt_ids, max_len=100)
```

### Other Implementations

| Repo | Framework | Notes |
|------|-----------|-------|
| [Yuan-ManX/Titans-PyTorch](https://github.com/Yuan-ManX/Titans-PyTorch) | PyTorch | Clean implementation |
| [aheschl1/titans](https://github.com/aheschl1/titans) | PyTorch | NeuralMemory + MAC |
| [Mohammed-Saajid/tf-titans](https://github.com/Mohammed-Saajid/tf-titans) | TensorFlow | MAC only |
| [ddidacus/llama-titans](https://github.com/ddidacus/llama-titans) | PyTorch | Llama integration |

### Official Code
Google plans to release PyTorch and JAX implementations for training/evaluation.

---

## Implications for AI Agents

### Current State
- Agent memory stored in external databases (JSON, SQL, vector DBs)
- Context windows limited (128K-200K typical)
- Long sessions require summarization or context truncation

### With Titans
- **Memory inside model weights** - retrieval becomes instant and semantic
- **Long-running agents feasible** - weeks of operation without context reset
- **Learning on the fly** - agent adapts to user's coding style over time
- **No external memory management** - eliminates RAG complexity for some use cases

### Potential Claude Code Applications

1. **Session persistence** - Remember project context across sessions without CLAUDE.md
2. **Codebase understanding** - Internalize large codebases beyond context limits
3. **User preference learning** - Adapt to individual coding styles over time
4. **Long-term task tracking** - Multi-day projects without context loss

---

## Current Status

- **Research stage** - Not yet in production APIs
- **Google internal** - May appear in future Gemini versions
- **Open implementations** - Community PyTorch versions available for experimentation

---

## Related: MIRAS Framework

Google also released **MIRAS** (Memory in Recurrent Attention-based Sequence models), a unifying framework for understanding memory in sequence models. Titans + MIRAS together provide both the architecture and theoretical foundation for long-term AI memory.

---

## Sources

- [Titans Paper (arXiv)](https://arxiv.org/abs/2501.00663)
- [Google Research Blog: Titans + MIRAS](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)
- [lucidrains/titans-pytorch](https://github.com/lucidrains/titans-pytorch)
- [@behrouz_ali on X](https://x.com/behrouz_ali/status/1878859086227255347)
- [@BrianRoemmele on X](https://x.com/BrianRoemmele/status/1879610700303376502)
- [Shaped.ai Blog](https://www.shaped.ai/blog/titans-learning-to-memorize-at-test-time-a-breakthrough-in-neural-memory-systems)

# RAGLab Data Model

## 1. Purpose

The database stores documents, evaluation datasets, retrieval experiments,
retrieval results, metrics, and failure analysis information.

The schema must support reproducible comparisons between RAG retrieval
configurations.

---

## 2. Core Entities

### Dataset

Represents a versioned collection of evaluation cases.

Fields:
- id
- name
- description
- version
- created_at
- updated_at

---

### Document

Represents a source document imported into RAGLab.

Fields:
- id
- source_name
- source_type
- source_uri
- created_at

---

### DocumentVersion

Represents a specific processed version of a document.

Fields:
- id
- document
- content_hash
- extracted_text
- processing_status
- created_at

Relationship:
- One Document can have many DocumentVersions.

---

### Chunk

Represents a retrievable passage created from a DocumentVersion.

Fields:
- id
- document_version
- text
- chunk_index
- start_offset
- end_offset
- chunking_config
- created_at

Relationship:
- One DocumentVersion can have many Chunks.

---

### EvaluationCase

Represents one benchmark question.

Fields:
- id
- dataset
- question
- expected_answer
- category
- difficulty
- answer_expected
- created_at

An EvaluationCase can reference one or more relevant chunks/documents.

---

### EvaluationRun

Represents one execution of an evaluation.

Fields:
- id
- dataset
- configuration
- started_at
- completed_at
- status

---

### RunConfiguration

Stores the exact retrieval configuration used by an EvaluationRun.

Examples:
- retrieval strategy
- chunk size
- chunk overlap
- top_k
- embedding model
- embedding model version
- retrieval parameters

The configuration must be stored so that an experiment can be reproduced.

---

### QueryResult

Represents the result of running one EvaluationCase during an EvaluationRun.

Fields:
- id
- evaluation_run
- evaluation_case
- retrieval_latency_ms
- retrieved_count
- error
- created_at

---

### RetrievedPassage

Represents an individual passage returned for a QueryResult.

Fields:
- id
- query_result
- chunk
- rank
- score
- relevance_label

---

### MetricResult

Stores calculated evaluation metrics.

Fields:
- id
- evaluation_run
- metric_name
- k
- value
- created_at

Initial metrics:
- Recall@K
- Precision@K
- MRR
- nDCG@K

---

### FailureAnnotation

Stores a diagnosed or manually reviewed failure.

Fields:
- id
- query_result
- category
- explanation
- confirmed
- created_at

Initial failure categories:

1. Relevant evidence was not retrieved.
2. Relevant evidence was retrieved but ranked too low.
3. Retrieved passages omitted necessary context.
4. Source documents were incomplete or outdated.
5. Retrieved evidence did not support the answer.
6. Answer was incorrect despite sufficient evidence.
7. Question was ambiguous.
8. System should have abstained.
9. Embedding, retrieval, or generation operation failed.

---

## 3. Relationships

Dataset
    |
    +-- EvaluationCase
    |
    +-- EvaluationRun
            |
            +-- RunConfiguration
            |
            +-- QueryResult
                    |
                    +-- RetrievedPassage
                    |
                    +-- FailureAnnotation
            |
            +-- MetricResult

Document
    |
    +-- DocumentVersion
            |
            +-- Chunk
                    |
                    +-- RetrievedPassage

EvaluationCase
    |
    +-- relevant Chunk references

---

## 4. Design Principles

- Preserve source document identity.
- Preserve document version information.
- Preserve chunk identity.
- Store retrieval results rather than only aggregate metrics.
- Store configuration snapshots for reproducibility.
- Keep retrieval quality separate from answer quality.
- Support multiple relevant passages per evaluation case.
- Avoid storing only a final aggregate score.
- Avoid unnecessary duplicate entities.

---

## 5. Initial Scope

The first implementation will focus on:

1. Dataset
2. EvaluationCase
3. Document
4. DocumentVersion
5. Chunk
6. EvaluationRun
7. RunConfiguration
8. QueryResult
9. RetrievedPassage
10. MetricResult

FailureAnnotation can be added with the failure-analysis milestone if it is
not needed earlier.

Vector embedding storage will be introduced when pgvector is integrated.

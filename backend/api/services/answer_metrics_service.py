import re
from api.services.embedding_service import generate_embedding

def normalize_answer(answer):
    if not answer:
        return ""

    answer = answer.lower()

    answer = re.sub(
        r"[^\w\s]",
        " ",
        answer,
    )

    answer = re.sub(
        r"\s+",
        " ",
        answer,
    )

    return answer.strip()


def calculate_exact_match(expected_answer, generated_answer):
    expected = normalize_answer(expected_answer)
    generated = normalize_answer(generated_answer)

    if not expected:
        return None

    return 1.0 if expected == generated else 0.0

def calculate_token_f1(expected_answer, generated_answer):
    expected = normalize_answer(expected_answer)
    generated = normalize_answer(generated_answer)

    if not expected or not generated:
        return None

    expected_tokens = expected.split()
    generated_tokens = generated.split()

    expected_counts = {}

    for token in expected_tokens:
        expected_counts[token] = expected_counts.get(token, 0) + 1

    generated_counts = {}

    for token in generated_tokens:
        generated_counts[token] = generated_counts.get(token, 0) + 1

    common_tokens = 0

    for token in expected_counts:
        common_tokens += min(
            expected_counts[token],
            generated_counts.get(token, 0),
        )

    if common_tokens == 0:
        return 0.0

    precision = common_tokens / len(generated_tokens)
    recall = common_tokens / len(expected_tokens)

    if precision + recall == 0:
        return 0.0

    return (
        2 * precision * recall
        / (precision + recall)
    )

def calculate_answer_relevance(question, generated_answer):
    if not question or not generated_answer:
        return None

    question_embedding = generate_embedding(question)
    answer_embedding = generate_embedding(generated_answer)

    dot_product = sum(
        q * a
        for q, a in zip(
            question_embedding,
            answer_embedding,
        )
    )

    question_norm = sum(
        q * q
        for q in question_embedding
    ) ** 0.5

    answer_norm = sum(
        a * a
        for a in answer_embedding
    ) ** 0.5

    if question_norm == 0 or answer_norm == 0:
        return None

    return dot_product / (
        question_norm * answer_norm
    )

def calculate_answer_correctness(
    expected_answer,
    generated_answer,
):
    if not expected_answer or not generated_answer:
        return None

    expected_embedding = generate_embedding(
        expected_answer
    )

    generated_embedding = generate_embedding(
        generated_answer
    )

    dot_product = sum(
        expected * generated
        for expected, generated in zip(
            expected_embedding,
            generated_embedding,
        )
    )

    expected_norm = sum(
        value * value
        for value in expected_embedding
    ) ** 0.5

    generated_norm = sum(
        value * value
        for value in generated_embedding
    ) ** 0.5

    if expected_norm == 0 or generated_norm == 0:
        return None

    return dot_product / (
        expected_norm * generated_norm
    )

def calculate_context_support(generated_answer, retrieved_context):
    if not generated_answer or not retrieved_context:
        return None

    answer_tokens = set(
        normalize_answer(generated_answer).split()
    )

    context_tokens = set(
        normalize_answer(retrieved_context).split()
    )

    if not answer_tokens:
        return None

    supported_tokens = answer_tokens.intersection(
        context_tokens
    )

    return len(supported_tokens) / len(answer_tokens)   


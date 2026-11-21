from rag.models import MetricResult


def persist_evaluation_metrics(
    evaluation_run,
    evaluation,
):
    retrieval_metrics = evaluation["retrieval_metrics"]
    answer_metrics = evaluation["answer_metrics"]

    metric_results = []

    for metric_name, value in retrieval_metrics.items():
        if value is None:
            continue

        k = 5 if metric_name.endswith("_at_k") else None

        metric_results.append(
            {
                "metric_name": metric_name,
                "k": k,
                "value": value,
            }
        )

    for metric_name, value in answer_metrics.items():
        if value is None:
            continue

        metric_results.append(
            {
                "metric_name": metric_name,
                "k": None,
                "value": value,
            }
        )

    persisted_results = []

    for metric in metric_results:
        metric_result, _ = MetricResult.objects.update_or_create(
            evaluation_run=evaluation_run,
            metric_name=metric["metric_name"],
            k=metric["k"],
            defaults={
                "value": metric["value"],
            },
        )

        persisted_results.append(metric_result)

    return persisted_results
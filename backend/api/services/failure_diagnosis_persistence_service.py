from rag.models import FailureDiagnosis


def persist_failure_diagnosis(
    query_result,
    diagnosis,
):
    failure_diagnosis, created = FailureDiagnosis.objects.update_or_create(
        query_result=query_result,
        defaults={
            "failure_type": diagnosis["failure_type"],
            "severity": diagnosis["severity"],
            "reason": diagnosis["reason"],
        },
    )

    return failure_diagnosis
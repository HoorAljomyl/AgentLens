from typing import Dict, List


def calculate_metrics(results: List[Dict]) -> Dict:

    total = len(results)

    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    failed = total - passed

    success_rate = round(
        (passed / total) * 100,
        2,
    )

    average_score = round(
        sum(result["score"] for result in results)
        / total,
        2,
    )

    return {
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": failed,
        "success_rate": success_rate,
        "average_score": average_score,
    }
from typing import Dict, List


def generate_report(results: List[Dict]) -> Dict:
    total_conversations = len(results)

    passed = sum(
        1 for result in results if result["passed"]
    )

    failed = total_conversations - passed

    if total_conversations == 0:
        average_score = 0
    else:
        average_score = round(
            sum(result["score"] for result in results)
            / total_conversations,
            2,
        )

    return {
        "total_conversations": total_conversations,
        "passed": passed,
        "failed": failed,
        "average_score": average_score,
    }


def generate_text_report(report: Dict) -> str:
    text = ""

    text += "=============================\n"
    text += "AgentLens Evaluation Report\n"
    text += "=============================\n\n"

    text += f"Total Users: {report['total_users']}\n"
    text += f"Passed Tests: {report['passed_tests']}\n"
    text += f"Failed Tests: {report['failed_tests']}\n"
    text += f"Average Score: {report['average_score']}%\n\n"

    text += "---------------------------------\n"

    for result in report["results"]:
        status = "PASSED" if result["passed"] else "FAILED"

        text += f"User: {result['user']}\n"
        text += f"Personality: {result['personality']}\n"
        text += f"Message: {result['message']}\n"
        text += f"Response: {result['response']}\n"
        text += f"Score: {result['score']}\n"
        text += f"Status: {status}\n"
        text += f"Reason: {result['reason']}\n"
        text += "---------------------------------\n"

    return text
def save_text_report(text: str, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
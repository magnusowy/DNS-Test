import json
import allure

def attach_stats_to_report(server: str, qname: str, stats: dict):
    allure.attach(
        json.dumps(stats),
        name=f"Server {server} Qname: {qname}",
        attachment_type=allure.attachment_type.JSON
    )
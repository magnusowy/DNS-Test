import yaml
import time
import statistics
from pathlib import Path

def config_return_list(value) -> list[str]:
    project_root = Path(__file__).resolve().parents[1]
    conf_file = project_root / "configs" / "variables.yaml"
    data = yaml.safe_load(conf_file.read_text())
    return data[value]

def config_return_proxies() -> tuple:
    project_root = Path(__file__).resolve().parents[1]
    conf_file = project_root / "configs" / "variables.yaml"
    with open(conf_file, "r") as f:
        config = yaml.safe_load(f)
    proxies = [(item["name"], item["url"]) for item in config["proxies"]]
    return proxies

def qname() -> list[str]:
    project_root = Path(__file__).resolve().parents[1]
    conf_file = project_root / "configs" / "variables.yaml"
    data = yaml.safe_load(conf_file.read_text())
    return data["url"]

def meansure_time_with_resolver(resolver, qname: str, qtype: str) -> float:

    t_start = time.monotonic()
    answers = resolver.resolve(qname, qtype)
    _ = list(answers) # it has to be fully received and read to remove lazy evaluation
    return time.monotonic()-t_start

def ret_stats(values: list[float]) -> dict[str:int]:
    return {
        "number_of_values": len(values),
        "min": min(values),
        "max": max(values),
        "median": statistics.median(values),
        "average": statistics.fmean(values)
    }

def nav_total_seconds(page) -> float:
    """ Returns total page load time [s] """
    e = page.evaluate(
        "(() => { const n = performance.getEntriesByType('navigation')[0]; "
        "return n && JSON.parse(JSON.stringify(n)); })()"
    )
    assert e, "Error Navigation Timing"
    return (e["loadEventEnd"] - e["startTime"]) / 1000.0 # ms -> s



def visit_once_using_playwright(browser, url: str, proxy_url):
    """ Visits page and returns count of requests and total page load time [s]. """
    pge = browser.new_context(proxy={"server": proxy_url} if proxy_url else None)
    page = pge.new_page()

    req_count = {"n": 0}
    page.on("request", lambda r: req_count.__setitem__("n", req_count["n"] + 1))

    page.goto("about:blank")
    page.goto(url, wait_until="load")  # 'load' = resources + onload

    total = nav_total_seconds(page)
    pge.close()
    return req_count["n"], total
import statistics
import pytest
import allure
from playwright.sync_api import sync_playwright
from resources.allure_helpers import attach_stats_to_report
from resources.global_helpers import ret_stats
from resources.global_helpers import config_return_list
from resources.global_helpers import config_return_proxies
from resources.global_helpers import visit_once_using_playwright

REPEATS = int(config_return_list("repeats_for_visit_request_test"))

@allure.epic("Network")
@allure.feature("DNS")
@allure.story("DNS time tests")
@pytest.mark.parametrize("proxy_label,proxy_url", config_return_proxies(), ids=lambda t: f"DNS:{t[0]}")
@pytest.mark.parametrize("url", config_return_list("urls"), ids=lambda u: f"VISIT:{u}")
def test_number_of_requests_and_pageload(proxy_label, proxy_url, url):
    """ Shows how many requests was created in visit time + time of loadpage"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # to have warm-cache
        try:
            visit_once_using_playwright(browser, url, proxy_url)
        except Exception:
            pass

        reqs, totals = [], []
        for _ in range(REPEATS):
            n, t = visit_once_using_playwright(browser, url, proxy_url)
            reqs.append(n)
            totals.append(t)
        browser.close()

    # generate statistics
    requests_stats = ret_stats(reqs)
    page_load_time = ret_stats(totals)

    med_req = statistics.median(reqs)
    med_total = statistics.median(totals)
    attach_stats_to_report(proxy_label, proxy_url, requests_stats)
    attach_stats_to_report(proxy_label, proxy_url, page_load_time)

    # assert exaples
    assert med_req > 0, "Requires at least 1 request"
    assert med_total < 5.0, f"Page is loading too long: {med_total:.2f}s"

    # print for cli

    print(
        f"\n[{proxy_label}] {url}\n"
        f"  Requests (median of {REPEATS}): {med_req}\n"
        f"  Load time (median): {med_total*1000:.0f} ms"
    )
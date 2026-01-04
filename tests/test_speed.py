import pytest
import allure

from resources.allure_helpers import attach_stats_to_report
from resources.global_helpers import config_return_list
from resources.global_helpers import meansure_time_with_resolver
from resources.global_helpers import ret_stats

@allure.epic("Network")
@allure.feature("DNS")
@allure.story("DNS latency")
@pytest.mark.parametrize("server", config_return_list("servers"), ids=lambda s: f"DNS:{s}")
def test_dns_speed_A_record(QNAME, NO_REPEATS, resolver_factory, server):
    """ Speed as a time to get ip address from DNS """
    r = resolver_factory.create([server])
    # warm-cache
    try:
        meansure_time_with_resolver(r, QNAME, "A")
    except Exception:
        pass
    data = [meansure_time_with_resolver(r, QNAME, "A") for _ in range(100)] # check 100 times, can be also parametrized

    # generate statistics
    data_results = ret_stats(data)
    attach_stats_to_report(server, QNAME, data_results)

    # Example asserts
    assert data_results["median"] < 0.05, f"Median {data_results['median']} ms is too high"

    # print for CLI debug
    print(f"DNS {server} → number_of_values={data_results['number_of_values']} | " 
          f"max={data_results['max']*1000:.1f} ms | "
          f"min={data_results['min']*1000:.1f} ms | "
          f"median={data_results['median']*1000:.1f} ms | "
          f"average={data_results['average']*1000:.1f} ms")
from typing import List

from decorators import calculate_execution_time



@calculate_execution_time
async def generate_candidates(customer_features: List[str]):
    # TODO: do the magic here
    candidates = ['468', '1043', '560', '944', '140']
    return candidates
import requests
import time


def get_remote_time_ms():
    res = requests.get("http://10.0.0.59:8001/time")
    return int(res.text)

def get_local_time_ms():
    return int(time.time() * 1000)

def get_delta_t():
    """       local
              |   network
              |   |   remote
    t0        *-->|   |
    remote_t  |   |<->*
    t1        *<--|   |

    Assumes remote_t - t0 ~= t1 - remote_t
    We know that higher t1 - t0 means more likely that remote_t - t0 != t1 - remote_t 
    """
    t0 = get_local_time_ms()
    remote_t = get_remote_time_ms()
    t1 = get_local_time_ms()

    local_t = (t0 + t1) // 2

    delta_t = local_t - remote_t
    rtt = t1 - t0

    skew = delta_t - (rtt * 0.5)

    if rtt > 50:
        bad = "(BAD)"
    else:
        bad = ""
    print(f"{bad}{skew:6} {delta_t:6} {rtt:6}")
    return skew


def main():
    predicted_delta_t = 0
    while 1:
        get_delta_t()
        time.sleep(0.5)

if __name__ == '__main__':
    main()
    
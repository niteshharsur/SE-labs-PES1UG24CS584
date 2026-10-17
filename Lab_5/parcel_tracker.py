"""Book parcels, track delivery progress, and provide courier helpers."""

import ipaddress
import os
import secrets
import shutil
# B404 reviewed: required for the validated, shell-free system ping.
import subprocess  # nosec B404
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
PARCELS = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and append its ID to the supplied or a fresh history."""
    if history is None:
        history = []
    tracking_id = "TRK" + str(10001 + len(PARCELS))
    PARCELS[tracking_id] = {
        "sender": sender, "receiver": receiver,
        "weight": weight_kg, "status": 0,
        "booked": str(date.today()),
    }
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Advance a known parcel by one stage, stopping at Delivered."""
    parcel = PARCELS[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Return the base fee plus the charge for weight above one kilogram."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Describe a parcel's route/status or report an unknown tracking ID."""
    try:
        parcel = PARCELS[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Return whether a known parcel is picked up or in transit."""
    status = STATUS_FLOW[PARCELS[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create a secure empty label file; the caller owns its cleanup."""
    descriptor, path = tempfile.mkstemp(suffix=".txt")
    os.close(descriptor)
    return path


def ping_hub(hub_address):
    """Ping a literal IPv4/IPv6 address once without invoking a shell."""
    address = str(ipaddress.ip_address(hub_address))
    executable = shutil.which("ping")
    if executable is None:
        raise FileNotFoundError("The system ping utility is unavailable")
    count_option = "-n" if os.name == "nt" else "-c"
    # B603 reviewed: resolved executable, valid IP, argument list, no shell.
    return subprocess.check_output(  # nosec B603
        [executable, count_option, "1", address], shell=False, timeout=10
    )


def main():
    """Demonstrate booking, status updates, pricing, and a secure OTP."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(PARCELS[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    delivery_otp = 1000 + secrets.randbelow(9000)
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(PARCELS))


if __name__ == "__main__":
    main()

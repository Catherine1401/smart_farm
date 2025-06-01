import urllib.request

def write_to_cnosdb(measurement, tags, fields):
    url = "http://localhost:8902/write?db=public"
    line = f"{measurement},{tags} {fields}"
    data = line.encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print("❌ Write failed:", response.status, response.read())
    except Exception as e:
        print("❌ Error writing to CnosDB:", e)

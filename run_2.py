import json
from src.parser import find_sku_position
import time

queries = ["корм для кошек сухой", "серый зонт", "масло гхи"]
sku = ["228861138", "1683355051", "276684382"]

def main():
    for i in range(len(queries)):
        result = find_sku_position(queries[i], sku[i])
        print(
            json.dumps(
                result.to_dict(),
                ensure_ascii=False
            )
        )
        time.sleep(30)

if __name__ == "__main__":
    main()
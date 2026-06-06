import json
from src.parser import find_sku_position

queries = ["корм для кошек сухой"]
sku = ["489093945"]

def main():
    for i in range(len(queries)):
        result = find_sku_position(queries[i], sku[i])
        print(
            json.dumps(
                result.to_dict(),
                ensure_ascii=False
            )
        )

if __name__ == "__main__":
    main()
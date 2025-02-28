from warehouse import Warehouse

class Reporting:
    @staticmethod
    def inventory_report(warehouse: Warehouse):
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ ІНВЕНТАРИЗАЦІЇ".center(50))
        print("=" * 50)
        for item in warehouse.get_inventory():
            print(item)
        print("=" * 50 + "\n")
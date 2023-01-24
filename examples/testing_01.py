from src.biosim.fauna import Herbivore


if __name__ == "__main__":
    print("working")
    herb1 = Herbivore(10, 20)
    print(herb1.age)
    print(herb1.fitness)

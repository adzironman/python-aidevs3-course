from src.tasks.poligon_task import PoligonTask

def main():
    task = PoligonTask()
    response = task.run()
    print(response)

if __name__ == "__main__":
    main() 
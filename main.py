import ModelBuilder
import os

def main():
    Model = ModelBuilder.ModelBuilder()
    print(Model.getSummary())
    Model.train()

if __name__ == "__main__":
    main()
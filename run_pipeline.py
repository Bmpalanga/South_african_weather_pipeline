from scripts.extract import main as extract
from scripts.transform import main as transform
from scripts.load import main as load


def main():
    print("Starting weather data pipeline...")

    print("\n--- Extracting weather data ---")
    extract()

    print("\n--- Transforming weather data---")
    transform()

    print("\n--- Loading weather data ---")
    load()

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()

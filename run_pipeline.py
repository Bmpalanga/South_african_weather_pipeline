from scripts.extract import main as extract
from scripts.transform import main as transform
from scripts.load import main as load


def main():
    print("Starting weather data pipeline...")

    print("\n--- Extract ---")
    extract()

    print("\n--- Transform ---")
    transform()

    print("\n--- Load ---")
    load()

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()

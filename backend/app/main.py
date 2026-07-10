from analyzer import analyze_csv

def main() -> None:
    file_path = input("Ingrese la ruta del archivo CSV: ")

    try:

        result = analyze_csv(file_path)

        print("\nResultado del analisis:")
        print("---------------------------")

        for key, value in result.items():
            print(f"{key}: {value}")

    except (FileNotFoundError, ValueError, UnicodeDecodeError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
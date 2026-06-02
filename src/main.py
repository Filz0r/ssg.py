from .builder import Builder

def main():
    builder = Builder()
    builder.copy_static_to_pub()
    builder.generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()

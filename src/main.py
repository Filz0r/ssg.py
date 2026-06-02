import sys
from .builder import Builder

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    builder = Builder()
    builder.copy_static_to_pub(dest="docs")
    builder.generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()

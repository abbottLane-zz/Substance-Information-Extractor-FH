from DataLoading import ServerQuery


def main():
    annotations = ServerQuery.get_annotations_from_server()
    iaa = calculate_iaa(annotations)
    print(iaa)


def calculate_iaa(annotations):
    iaa = 0
    raise NotImplementedError
    return iaa


if __name__ == '__main__':
    main()

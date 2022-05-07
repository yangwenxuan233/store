import csv


class CargoDataSource():
    def load(self, input_file_path):
        self.list = []
        with open(input_file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                print(i)
        pass

    def export(self, output_file_path):
        pass


if __name__ == '__main__':
    CargoDataSource.load('cargo.csv')

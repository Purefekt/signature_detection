import csv
import os

from src.loader import Loader
from src.extractor import Extractor
from src.cropper import Cropper
from src.judger import Judger


def read_input_files():

    with open("./private/signed-9622.csv") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            print(row)
            break


def main():
    # init workers
    loader = Loader()
    extractor = Extractor(amplfier=15)
    cropper = Cropper()
    judger = Judger()
    # detect
    output_file = "./private/res-pos.csv"
    input_file = "./private/signed-9622.csv"
    
    with open(output_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "signed"], delimiter=",")
        writer.writeheader()
    
    with open(output_file, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "signed"], delimiter=",")
        with open(input_file) as inputfile:
            reader = csv.DictReader(inputfile, delimiter=",")
            for row in reader:
                file = row['id']
                try:
                    masks = loader.get_masks("./private/files/" + str(file) + ".pdf")
                    is_signed = False
                    for mask in masks:
                        labeled_mask = extractor.extract(mask)
                        cropped_images = cropper.run(labeled_mask)
                        for cropped_image in cropped_images:
                            is_signed = judger.judge(cropped_image)
                            if is_signed:
                                break
                        if is_signed:
                            break
                    row = {}
                    row["id"] = file
                    row["signed"] = 1 if is_signed else 0
                    print(row)
                    writer.writerow(row)
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    main()
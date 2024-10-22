from .dataset import Dataset
from .flow import Era5Flow
from .dashboard import demo

from tqdm import tqdm 

import click

@click.command()
def preload():
    """Preload the dataset based on the deskriptors.jsonl and store the results in S3 bucket
    """
    print("Preloading the dataset")
    dataset = Dataset("deskriptors.jsonl",Era5Flow())

    for i in tqdm(range(len(dataset))):
        data = dataset[i]
        tqdm.write(str(data))


@click.command()
def dashboard():
    "Launch the dashboard"
    demo.launch()


@click.group()
def main():
    """sodeda-era5"""
    pass


main.add_command(preload)
main.add_command(dashboard)

if __name__ == "__main__":
    main()

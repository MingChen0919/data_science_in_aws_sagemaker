import h2o
import argparse

h2o.init()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-data', type=str, help='path to raw data')

    args = parser.parse_args()

    mort_df = h2o.upload_file(args.raw_data)
    h2o.export_file(mort_df.head(), '/opt/ml/processing/output/mortality_head.csv')
    print(mort_df.head())

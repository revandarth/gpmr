from __future__ import absolute_import

import getopt
import sys

from pet_race_job.data_importer import DataImporter


def main(arg):
    options, remainder = getopt.getopt(arg[1:], 'd:h', ['directory=', 'help'])

    # if options.d is None: # where foo is obviously your required option
    #    parser.print_help()
    #    sys.exit(1)

    for opt, arg in options:
        if opt in ('-d', '--directory'):
            data_dir = arg
        if opt in ('-h', '--help'):
            print("usage: --directory=data_directory")
            exit(0)

    if data_dir is None:
        exit("no parameter found")

    # TODO move this to config files
    loader = DataImporter(seeds=['cassandra-0.cassandra.default.svc.cluster.local',
                                 'cassandra-1.cassandra.default.svc.cluster.local'], keyspace='gpmr')
    loader.create_keyspace()
    loader.create_tables()

    # todo move path to config files
    pet_cats = loader.parse_pet_categories(data_dir + '/pet_categories.csv')
    loader.save_pet_categories(pet_cats)

    pets_data = loader.parse_pet_files(data_dir + '/pets/*.csv')

    for p in pets_data:
        loader.save_pets(p['pet'], p['cat'])


if __name__ == '__main__':
    main(sys.argv)
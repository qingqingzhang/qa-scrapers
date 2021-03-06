import sys
import os

from discretization import Discretizer


def main():
    program_name = os.path.basename(sys.argv[0])
    db_files = {'abap': 'abap.pydb'}
    try:
        db_names = sys.argv[1]
    except IndexError:
        raise Exception('No db name. Please, re-run as "{0} dbname.pydb"'.format(program_name))

    if db_names == 'all':
        discretizer = Discretizer(db_names, db_files)
    else:
        try:
            discretizer = Discretizer(db_names, {db_names: db_files.get(db_names)})
        except KeyError:
            raise Exception('Invalid db name {0}. Please, check the name and re-run.'.format(db_names))

    discretizer.load_db(check=False, fix=False, save_to_file=False)

    corpus = discretizer.build_corpus()
    stems = discretizer.build_stems(corpus)
    stemmed_vocabulary = discretizer.build_vocabulary(stems)
    distib_matrix = discretizer.build_distribution_matrix(stems)

    # grouping
    threads = discretizer.load_threads()
    # discretization and sorting
    threads = discretizer.compute_features(threads, stemmed_vocabulary, distib_matrix)
    discretizer.save_csv(threads)


if __name__ == "__main__":
    sys.exit(main())

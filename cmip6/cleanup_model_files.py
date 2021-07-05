import os
import glob
import sys
import errno

def createpath(path):
    '''Create path'''
    thispath = os.path.expanduser(path)
    if not os.path.exists(thispath):
        try:
            os.makedirs(thispath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        
        
def cleanup_model_files(datadir):
    '''Moves ESGF CMIP6 files into a directory structure'''
    filelist = glob.glob(os.path.join(datadir, '*.nc'))
    if filelist:
        for f in filelist:
            variable, table, model, experiment, member, grid, time_range = f.split('_')
            dirpath = os.path.join(datadir, variable, table, model, experiment, member)
            #print(dirpath, f, os.path.join(dirpath, os.path.basename(f)))
            #continue
#            try:
#                os.makedirs(dirpath)
            #except FileExistsError:
            #    continue  # It is OK is directory path exists
#            except:
#                print('Unexpected error: ', sys.exc_info()[0])
#                raise
            createpath(dirpath)
            os.rename(f, os.path.join(dirpath, os.path.basename(f)))
    else:
        print(f'No files found in {datadir}: nothing to be done')
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Moves files into directory structure")
    parser.add_argument('datadir', type=str, default='.', help="Directory path containing data")
    args = parser.parse_args()
    cleanup_model_files(args.datadir)
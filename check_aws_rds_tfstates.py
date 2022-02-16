import boto3
import os
import argparse
import re

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket', help='AWS S3 bucket', required=True)
    parser.add_argument('-p', '--path', help='AWS S3 bucket folder path to tfstate files', required=True)
    parser.add_argument('-f', '--folder', help='Local folder to write tfstate file to (default ./s3-bucket-tfstate-files)', default='./s3-bucket-tfstate-files')
    parser.add_argument('-a', '--appprefix', help='Application prefix on RDS IDs', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.folder):
        os.makedirs(args.folder)

    s3 = boto3.resource('s3')

    rds_bucket = s3.Bucket(args.bucket)

    print("Gathering RDS instances")
    dbnames = get_rds_instances(args.appprefix)
    tfstatefiles = []

    print("\nRetreiving tfstate files")
    for rds_bucket_obj in rds_bucket.objects.filter(Prefix=args.path):
        print(rds_bucket_obj.key)
        rds_bucket.download_file(rds_bucket_obj.key, args.folder+'/'+os.path.basename(rds_bucket_obj.key))
        tfstatefiles.append(args.folder+'/'+os.path.basename(rds_bucket_obj.key))

    print("\nSearching tfstate files for RDS instances")
    for dbname in dbnames:
        found = False
        for tfstatefile in tfstatefiles:
            if check_contents(tfstatefile, dbname):
                print("Found RDS instance: " + dbname)
                found = True
                break

        if not found:
            print('RDS ID: '+dbname+' was NOT found in any tfstate files in bucket: '+args.bucket+args.path)

def check_contents(file, pattern):
    with open(file, 'r') as f:
        contents = f.read()
        if pattern in contents:
            return True
    return False

def get_rds_instances(appname_prefix):
    rds = boto3.client('rds')
    clusters = []
    rdsnames = []

    print("\nSearching DB Clusters")
    response = rds.describe_db_clusters()
    for i in response['DBClusters']:
        db_cluster_name = i['DBClusterIdentifier']

        if re.match(appname_prefix, db_cluster_name):
            print(db_cluster_name)
            # Let's check if the cluster was created with "-cluster" at end of name
            match = (re.search("-cluster$", db_cluster_name))
            if match is not None:
                db_cluster_name = db_cluster_name[0:match.start()]
            clusters.append(db_cluster_name)

    # Build a regex of cluster names found
    strclusters = '|'.join(clusters)

    rdsnames = clusters
    print('\nSearching DB Instances not part of a cluster')
    reg_clusters = re.compile(strclusters)
    response = rds.describe_db_instances()
    for i in response['DBInstances']:
        db_name = i['DBInstanceIdentifier']

        if re.match(appname_prefix, db_name) and not reg_clusters.match(db_name):
            print(db_name)
            rdsnames.append(db_name)

    return rdsnames

if __name__ == "__main__":
    main()

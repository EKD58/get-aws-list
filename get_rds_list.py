import boto3
import csv

# ACCESS_KEYとSECRET_KEYを入力してください
ACCESS_KEY = 'ACCESSKEY'
SECRET_KEY = 'SECRETKEY'
REGION_NAME = 'ap-northeast-1'

# RDSインスタンスの情報を取得する
def get_rds_instances():
    # AWSの認証情報を設定する
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )
    
    # RDSクライアントを作成する
    rds_client = session.client('rds')
    
    # RDSインスタンスの情報を取得する
    response = rds_client.describe_db_instances()
    
    instances = []
    
    # レスポンスからインスタンスの情報を抽出する
    for db_instance in response['DBInstances']:
        #print(db_instance)
        print(db_instance['DBInstanceIdentifier'])

        db_instance_id = db_instance['DBInstanceIdentifier']
        db_instance_type = db_instance['DBInstanceClass']
        db_instance_engine = db_instance['Engine']
        db_instance_status = db_instance['DBInstanceStatus']
        db_instance_az = db_instance['AvailabilityZone']
        db_storage_type = db_instance['StorageType']
        db_allocated_storage = db_instance['AllocatedStorage']

        # カスタムタグの値を取得
        custom_tag_cost_product = ''
        custom_tag_cost_environment = ''
        for tag in db_instance.get('TagList', []):
            if tag['Key'] == 'cost_product':
                custom_tag_cost_product = tag['Value']
            if tag['Key'] == 'cost_environment':
                custom_tag_cost_environment = tag['Value']

        instances.append([db_instance_id, db_instance_type, db_instance_engine, db_instance_status, db_instance_az, db_storage_type, db_allocated_storage, custom_tag_cost_product, custom_tag_cost_environment])

    # インスタンス名でソートする
    instances.sort(key=lambda x: x[0])

    return instances

def write_instances_to_csv(instances):
    # CSVファイルに出力する
    with open('rds_instances.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['DB識別子', 'インスタンスタイプ', 'エンジン', 'インスタンスの状態', 'インスタンスAZ', 'ボリュームタイプ', 'ボリュームサイズ', 'cost_product', 'cost_environment'])
        
        for instance in instances:
            writer.writerow(instance)

# RDSインスタンスの情報を取得する
rds_instances = get_rds_instances()

# 取得した情報をCSVファイルに出力する
write_instances_to_csv(rds_instances)

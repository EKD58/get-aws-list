import boto3
import csv

# ACCESS_KEYとSECRET_KEYを入力してください
ACCESS_KEY = 'ACCESSKEY'
SECRET_KEY = 'SECRETKEY'
REGION_NAME = 'ap-northeast-1'

# EC2インスタンスの情報を取得する
def get_ec2_instances():
    # AWSの認証情報を設定する
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )
    
    # EC2クライアントを作成する
    ec2_client = session.client('ec2')
    
    # EC2インスタンスの情報を取得する
    response = ec2_client.describe_instances()
    
    instances = []
    
    # レスポンスからインスタンスの情報を抽出する
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            #print(instance)
            print(instance['InstanceId'])

            instance_name = ''
            instance_type = instance['InstanceType']
            instance_state = instance['State']['Name']
            instance_id = instance['InstanceId']
            instance_az = instance['Placement']['AvailabilityZone']
            subnet_id = ''
            if(instance_state == 'running'):
                subnet_id = instance['SubnetId']
            cost_product = ''
            cost_environment = ''
            system = ''
            status = ''
            environment = ''

            # カスタムタグの値を取得
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                elif tag['Key'] == 'cost_product':
                    cost_product = tag['Value']
                elif tag['Key'] == 'cost_environment':
                    cost_environment = tag['Value']
                elif tag['Key'] == 'System':
                    system = tag['Value']
                elif tag['Key'] == 'Status':
                    status = tag['Value']
                elif tag['Key'] == 'Environment':
                    environment = tag['Value']

            volume_id = ''
            volume_type = ''
            volume_size = ''
            for volume in instance['BlockDeviceMappings']:
                volume_id = volume['Ebs']['VolumeId']
                
                # ボリュームの情報を取得する
                volume_response = ec2_client.describe_volumes(VolumeIds=[volume_id])
                volume_info = volume_response['Volumes'][0]
                volume_type = volume_info.get('VolumeType', 'N/A')
                volume_size = volume_info.get('Size', 'N/A')
                
                instances.append([instance_name, instance_type, instance_state, instance_id, instance_az, subnet_id, volume_type, volume_size, volume_id, cost_product, cost_environment, system, status, environment])

    # インスタンス名でソートする
    instances.sort(key=lambda x: x[0])

    return instances

# 取得した情報をCSVファイルに出力する
def write_instances_to_csv(instances):
    with open('ec2_instances.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['インスタンス名', 'インスタンスタイプ', 'インスタンスの状態', 'インスタンスID', 'インスタンスAZ', 'サブネットID', 'ボリュームタイプ', 'ボリュームサイズ', 'ボリュームID', 'cost_product', 'cost_environment', 'system', 'status', 'environment'])
        
        for instance in instances:
            writer.writerow(instance)

# EC2インスタンスの情報を取得する
ec2_instances = get_ec2_instances()

# 取得した情報をCSVファイルに出力する
write_instances_to_csv(ec2_instances)
